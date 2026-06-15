# CCC Analyzer — Cash Conversion Cycle Dashboard

An interactive dashboard for analyzing the Cash Conversion Cycle (CCC) of 13 major public companies from 2013–2024, using financial data pulled directly from SEC EDGAR.

## What it does

- Fetches 10-K and 20-F filings from SEC EDGAR for 13 companies
- Extracts Inventory, Accounts Receivable, Accounts Payable, Revenue, and COGS
- Calculates three working capital metrics per company per fiscal year:
  - **DIO** — Days Inventory Outstanding
  - **DSO** — Days Sales Outstanding
  - **DPO** — Days Payable Outstanding
  - **CCC** = DIO + DSO − DPO

## Companies covered

| Ticker | Company |
|--------|---------|
| AAPL | Apple Inc. |
| DELL | Dell Technologies |
| WMT | Walmart Inc. |
| AMZN | Amazon.com Inc. |
| COST | Costco Wholesale |
| JNJ | Johnson & Johnson |
| PFE | Pfizer Inc. |
| F | Ford Motor Company |
| TM | Toyota Motor Corp |
| DAL | Delta Air Lines |
| LUV | Southwest Airlines |
| MSFT | Microsoft Corp. |
| GOOGL | Alphabet Inc. |

## Usage

### 1. Fetch the data

```bash
pip install requests
python fetch_ccc_data.py
```

This writes `ccc_data.json` and `ccc_chart_data.js` to the project directory.

### 2. Open the dashboard

Open `index.html` in a browser. No server required — it reads the local JS data file directly.

## Files

| File | Description |
|------|-------------|
| `fetch_ccc_data.py` | Pulls XBRL data from SEC EDGAR and computes CCC metrics |
| `ccc_data.json` | Raw output data |
| `ccc_chart_data.js` | Chart-ready data loaded by the dashboard |
| `index.html` | Interactive Chart.js dashboard |

## Requirements

- Python 3.8+
- `requests` library
- A modern browser
