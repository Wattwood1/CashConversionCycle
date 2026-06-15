#!/usr/bin/env python3
"""
fetch_ccc_data.py

Pulls 10-K / 20-F filings from SEC EDGAR for 13 companies (2013-2024),
extracts Inventory, Accounts Receivable, Accounts Payable, Revenue, and COGS,
then calculates DIO, DSO, DPO, and CCC per company per fiscal year.

Requirements:
    pip install requests

Output:
    ccc_data.json
"""

import json
import sys
import time
import warnings
import requests
import urllib3

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EDGAR_BASE = "https://data.sec.gov"

# SEC requires a descriptive User-Agent with contact info.
HEADERS = {
    "User-Agent": "CCC Data Fetcher williamtattwood@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}

YEAR_MIN, YEAR_MAX = 2013, 2024

# fmt: off
COMPANIES = {
    "AAPL":  {"name": "Apple Inc.",          "cik": "0000320193", "form": "10-K"},
    "DELL":  {"name": "Dell Technologies",   "cik": "0001571123", "form": "10-K"},
    "WMT":   {"name": "Walmart Inc.",        "cik": "0000104169", "form": "10-K"},
    "AMZN":  {"name": "Amazon.com Inc.",     "cik": "0001018724", "form": "10-K"},
    "COST":  {"name": "Costco Wholesale",    "cik": "0000909832", "form": "10-K"},
    "JNJ":   {"name": "Johnson & Johnson",   "cik": "0000200406", "form": "10-K"},
    "PFE":   {"name": "Pfizer Inc.",         "cik": "0000078003", "form": "10-K"},
    "F":     {"name": "Ford Motor Company",  "cik": "0000037996", "form": "10-K"},
    "TM":    {"name": "Toyota Motor Corp",   "cik": "0001094517", "form": "20-F"},
    "DAL":   {"name": "Delta Air Lines",     "cik": "0000027904", "form": "10-K"},
    "LUV":   {"name": "Southwest Airlines",  "cik": "0000092380", "form": "10-K"},
    "MSFT":  {"name": "Microsoft Corp.",     "cik": "0000789019", "form": "10-K"},
    "GOOGL": {"name": "Alphabet Inc.",       "cik": "0001652044", "form": "10-K"},
}
# fmt: on

# XBRL concept candidates per metric, tried in order.
# Keys are namespace ("us-gaap" or "ifrs-full"); values are ordered lists.
# Toyota (TM) files under IFRS so ifrs-full concepts are needed.
CONCEPT_CANDIDATES: dict[str, dict[str, list[str]]] = {
    "inventory": {
        "us-gaap": [
            # Standard — works for most manufacturers/retailers
            "InventoryNet",
            "InventoryFinishedGoods",
            "InventoryGross",
            "InventoryFinishedGoodsNetOfReserves",
            # Airlines (spare parts, expendable supplies)
            "AirlineRelatedInventoryNet",
            "AirlineRelatedInventorySparePartsAndSuppliesNet",
            "AirlineRelatedInventoryFuelAndSparePartsNet",
            "FlightEquipmentSparePartsNet",
            "MaterialsAndSupplies",
            "SuppliesAndMaterials",
            # Raw-materials bucket — catches airlines/utilities that lump
            # expendable parts here rather than under finished-goods
            "InventoryRawMaterials",
            "InventoryRawMaterialsAndSupplies",
            "InventoryRawMaterialsNetOfReserves",
            "OtherInventoryNetOfReserves",
            "InventoryWorkInProcess",
        ],
        "ifrs-full": ["Inventories"],
    },
    "accounts_receivable": {
        "us-gaap": [
            "AccountsReceivableNetCurrent",
            "ReceivablesNetCurrent",
            "AccountsAndNotesReceivableNet",
            "TradeAndOtherReceivablesNetCurrent",
            # Airlines / service companies sometimes use broader receivable buckets
            "OtherReceivablesNetCurrent",
            "ReceivablesNet",
            "NontradeReceivablesCurrent",
            "ReceivablesFromCustomers",
        ],
        "ifrs-full": [
            "TradeAndOtherCurrentReceivables",
            "CurrentTradeReceivables",
        ],
    },
    "accounts_payable": {
        "us-gaap": [
            "AccountsPayableCurrent",
            "AccountsPayableAndAccruedLiabilitiesCurrent",
            "AccountsPayableTradeCurrent",
            "AccountsPayableRelatedPartiesCurrent",
        ],
        "ifrs-full": [
            "TradeAndOtherCurrentPayablesToTradeSuppliers",
            "CurrentTradePayables",
            "TradeAndOtherCurrentPayables",
        ],
    },
    "revenue": {
        "us-gaap": [
            # ASC 606 era (2018+) — most companies
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            # Pre-ASC-606 / legacy tags — fill in 2013-2017 gaps
            "Revenues",
            "SalesRevenueNet",
            "SalesRevenueGoodsNet",
            "SalesRevenueServicesNet",
            # Pharma-specific (Pfizer historical reporting)
            "NetProductSales",
            "ProductSalesNet",
            "SalesRevenueGoodsGross",
        ],
        "ifrs-full": [
            "Revenue",
            "RevenueFromContractsWithCustomers",
        ],
    },
    "cogs": {
        "us-gaap": [
            # Broad coverage — most companies
            "CostOfGoodsSold",
            "CostOfRevenue",
            "CostOfGoodsAndServicesSold",
            # Retail (Costco uses "Merchandise costs" → CostOfSales in XBRL)
            "CostOfSales",
            # Pharma / manufacturing
            "CostOfProductsSold",
            "CostOfGoodsSoldExcludingDepreciationDepletionAndAmortization",
            # Software / services (Microsoft)
            "CostOfServicesLicensesAndMaintenance",
            "CostOfServicesAndLicenses",
            # Airlines — total operating expense is the best available proxy
            "OperatingCostsAndExpenses",
            "OperatingExpenses",
            "AirlineOperatingExpenses",
            # Broad fallback
            "CostAndExpenses",
            "CostsAndExpenses",
        ],
        "ifrs-full": [
            "CostOfSales",
            # IFRS alternative — cost of inventories expensed during period
            # (used by some Asian IFRS filers, including Toyota recent years)
            "CostOfInventoriesRecognisedAsExpenseDuringPeriod",
        ],
    },
}


# ---------------------------------------------------------------------------
# SEC EDGAR helpers
# ---------------------------------------------------------------------------

def fetch_company_facts(cik: str) -> dict:
    """
    Download all XBRL facts for a company. Retries on rate-limit (429).
    Uses verify=False for data.sec.gov to work around Windows CA-store
    issues where Python's bundled certs can't validate the intermediate CA.
    The domain is a US government endpoint, so this is safe in this context.
    """
    cik_padded = cik.lstrip("0").zfill(10)
    url = f"{EDGAR_BASE}/api/xbrl/companyfacts/CIK{cik_padded}.json"
    for attempt in range(4):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
                resp = requests.get(url, headers=HEADERS, timeout=30, verify=False)
            if resp.status_code == 429:
                wait = 5 * (attempt + 1)
                print(f"\n  [rate-limited] waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.response.status_code} from EDGAR") from exc
        except requests.RequestException as exc:
            if attempt == 3:
                raise RuntimeError(f"Network error: {exc}") from exc
            time.sleep(2)
    return {}


def _score_entries(entries: list[dict], accepted_forms: set, strict_fp: bool) -> dict[int, dict]:
    """
    Build {fy: {val, filed}} from a flat list of XBRL fact entries.

    strict_fp=True  — only accept fp="FY" (fast path, catches most companies).
    strict_fp=False — also accept fp=None/missing; for non-FY fp values, require
                      a 300-400 day duration so we don't pull in quarterly rows.
                      fy is inferred from the 'end' date when the field is absent.
    """
    from datetime import date as _date

    year_map: dict[int, dict] = {}
    for e in entries:
        if e.get("form") not in accepted_forms:
            continue

        fp = e.get("fp")
        if strict_fp:
            if fp != "FY":
                continue
        else:
            if fp not in ("FY", None):
                # Non-standard fp: only keep if the period spans ~1 year
                start_s, end_s = e.get("start"), e.get("end")
                if start_s and end_s:
                    try:
                        days = (_date.fromisoformat(end_s) - _date.fromisoformat(start_s)).days
                        if not (300 <= days <= 400):
                            continue
                    except ValueError:
                        continue
                else:
                    continue

        fy = e.get("fy")
        if not isinstance(fy, int):
            # Infer from the end date (e.g. "2019-12-31" → 2019)
            end_s = e.get("end", "")
            try:
                fy = int(end_s[:4])
            except (ValueError, TypeError):
                continue

        if not (YEAR_MIN - 1 <= fy <= YEAR_MAX):
            continue

        val = e.get("val")
        if val is None:
            continue

        filed = e.get("filed", "")
        if fy not in year_map or filed > year_map[fy]["filed"]:
            year_map[fy] = {"val": float(val), "filed": filed}

    return year_map


def extract_annual_values(facts_data: dict, metric: str) -> dict[int, float]:
    """
    Search both us-gaap and ifrs-full namespaces for the given metric.
    Returns {fiscal_year: value} covering YEAR_MIN-YEAR_MAX from annual filings.
    Currency is whatever the company reports in (USD or JPY for Toyota) —
    ratios cancel units so CCC days are always currency-neutral.

    Strategy — evaluate ALL concept candidates and MERGE the results:
      - Concepts are listed highest-priority first; the first concept that has
        data for a given fiscal year wins for that year.
      - This fills pre-2018 revenue gaps (legacy tags cover 2013-2017 after
        the ASC-606 tag covers 2018+) and patches per-company tag switches.

    Within each concept, a two-pass fp filter is applied:
      Pass 1 — strict fp="FY" (works for most filers).
      Pass 2 — relaxed fp filter (catches airlines and others that omit fp).
    """
    all_facts = facts_data.get("facts", {})
    accepted_forms = {"10-K", "10-K/A", "20-F", "20-F/A"}

    merged: dict[int, float] = {}  # fy -> val; first concept wins per year

    for namespace, concepts in CONCEPT_CANDIDATES[metric].items():
        ns_facts = all_facts.get(namespace, {})
        for concept in concepts:
            if concept not in ns_facts:
                continue

            # Collect entries across all reported currency units
            all_entries: list[dict] = []
            for unit_entries in ns_facts[concept].get("units", {}).values():
                all_entries.extend(unit_entries)

            # Pass 1: strict fp="FY"
            year_map = _score_entries(all_entries, accepted_forms, strict_fp=True)
            # Pass 2: relaxed (only if pass 1 found nothing for this concept)
            if not year_map:
                year_map = _score_entries(all_entries, accepted_forms, strict_fp=False)

            # Fill gaps — first concept that has data for a year wins
            for fy, entry in year_map.items():
                if fy not in merged:
                    merged[fy] = entry["val"]

    return merged


# ---------------------------------------------------------------------------
# CCC calculations
# ---------------------------------------------------------------------------

def calculate_ccc(
    inventory: float | None,
    ar: float | None,
    ap: float | None,
    revenue: float | None,
    cogs: float | None,
) -> dict | None:
    """
    DIO = (Inventory / COGS) * 365
    DSO = (Accounts Receivable / Revenue) * 365
    DPO = (Accounts Payable / COGS) * 365
    CCC = DIO + DSO - DPO
    Returns None when any input is missing or a denominator is zero.
    """
    if any(v is None for v in (inventory, ar, ap, revenue, cogs)):
        return None
    if cogs == 0 or revenue == 0:
        return None

    dio = (inventory / cogs) * 365
    dso = (ar / revenue) * 365
    dpo = (ap / cogs) * 365
    ccc = dio + dso - dpo

    return {
        "DIO": round(dio, 2),
        "DSO": round(dso, 2),
        "DPO": round(dpo, 2),
        "CCC": round(ccc, 2),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    results: dict = {}

    for ticker, info in COMPANIES.items():
        print(f"{ticker:<5}  {info['name']:<25}", end=" ", flush=True)

        try:
            facts = fetch_company_facts(info["cik"])
        except RuntimeError as exc:
            print(f"FAILED — {exc}")
            results[ticker] = {"name": info["name"], "error": str(exc), "years": {}}
            continue

        raw: dict[str, dict[int, float]] = {
            "inventory":          extract_annual_values(facts, "inventory"),
            "accounts_receivable": extract_annual_values(facts, "accounts_receivable"),
            "accounts_payable":    extract_annual_values(facts, "accounts_payable"),
            "revenue":             extract_annual_values(facts, "revenue"),
            "cogs":                extract_annual_values(facts, "cogs"),
        }

        all_years = sorted(
            y for vals in raw.values() for y in vals if YEAR_MIN <= y <= YEAR_MAX
        )

        company_result: dict = {"name": info["name"], "years": {}}

        for year in sorted(set(all_years)):
            inv  = raw["inventory"].get(year)
            ar   = raw["accounts_receivable"].get(year)
            ap   = raw["accounts_payable"].get(year)
            rev  = raw["revenue"].get(year)
            cogs = raw["cogs"].get(year)

            year_data: dict = {
                "inventory":          inv,
                "accounts_receivable": ar,
                "accounts_payable":    ap,
                "revenue":             rev,
                "cogs":                cogs,
            }

            ccc_metrics = calculate_ccc(inv, ar, ap, rev, cogs)
            if ccc_metrics:
                year_data.update(ccc_metrics)

            company_result["years"][str(year)] = year_data

        results[ticker] = company_result

        ccc_years = [y for y, d in company_result["years"].items() if "CCC" in d]
        print(f"OK  (CCC years: {ccc_years if ccc_years else 'none'})")

        # SEC allows up to 10 requests/second; 0.12 s keeps us safely under.
        time.sleep(0.12)

    # -----------------------------------------------------------------------
    # Write output
    # -----------------------------------------------------------------------
    output_path = "ccc_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nWrote {output_path}")

    # -----------------------------------------------------------------------
    # Console summary table
    # -----------------------------------------------------------------------
    print(
        f"\n{'Ticker':<6} {'Year':>4}  {'DIO':>7}  {'DSO':>7}  {'DPO':>7}  {'CCC':>8}"
    )
    print("-" * 52)
    for ticker, data in results.items():
        for year, yd in sorted(data.get("years", {}).items()):
            if "CCC" not in yd:
                continue
            print(
                f"{ticker:<6} {year:>4}  {yd['DIO']:>7.1f}  {yd['DSO']:>7.1f}"
                f"  {yd['DPO']:>7.1f}  {yd['CCC']:>8.1f}"
            )

    # Missing-data report
    print("\n--- Missing / incomplete data ---")
    for ticker, data in results.items():
        if "error" in data:
            print(f"  {ticker}: {data['error']}")
            continue
        missing = []
        for year, yd in sorted(data.get("years", {}).items()):
            if "CCC" not in yd:
                gaps = [k for k, v in yd.items() if v is None]
                if gaps:
                    missing.append(f"{year}({','.join(gaps[:2])}{'...' if len(gaps)>2 else ''})")
        if missing:
            print(f"  {ticker}: no CCC for {missing}")


if __name__ == "__main__":
    try:
        import requests  # noqa: F401
    except ModuleNotFoundError:
        sys.exit("Install the requests library first:  pip install requests")
    main()
