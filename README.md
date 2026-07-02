CCC Analyzer — Cash Conversion Cycle Dashboard

Live Demo →

<img width="1698" height="877" alt="Screenshot 2026-07-02 at 4 25 36 PM" src="https://github.com/user-attachments/assets/e5d7bed5-2279-4125-9a27-640b5e3e649a" />

An interactive dashboard for analyzing the Cash Conversion Cycle (CCC) of 13 major public companies from 2013–2024, using financial data pulled directly from SEC EDGAR.

What it does


Fetches 10-K and 20-F filings from SEC EDGAR for 13 companies
Extracts Inventory, Accounts Receivable, Accounts Payable, Revenue, and COGS
Calculates three working capital metrics per company per fiscal year:

DIO — Days Inventory Outstanding
DSO — Days Sales Outstanding
DPO — Days Payable Outstanding
CCC = DIO + DSO − DPO





Features


Industry filters — view companies grouped by industry, with industry-average lines for context
Company Spotlight — deep-dive tab breaking down a single company's DIO, DSO, and DPO trends over time
Industry Compare — side-by-side comparison of CCC trends across all six industries
Supply Chain Events — overlay of major supply chain disruptions (2013–2024) on the metric timelines, showing how real-world events ripple through working capital


Companies covered

TickerCompanyAAPLApple Inc.DELLDell TechnologiesWMTWalmart Inc.AMZNAmazon.com Inc.COSTCostco WholesaleJNJJohnson & JohnsonPFEPfizer Inc.FFord Motor CompanyTMToyota Motor CorpDALDelta Air LinesLUVSouthwest AirlinesMSFTMicrosoft Corp.GOOGLAlphabet Inc.

Usage

1. Fetch the data

bashpip install requests
python fetch_ccc_data.py

This writes ccc_data.json and ccc_chart_data.js to the project directory.

2. Open the dashboard

Open index.html in a browser. No server required — it reads the local JS data file directly.

Files

FileDescriptionfetch_ccc_data.pyPulls XBRL data from SEC EDGAR and computes CCC metricsccc_data.jsonRaw output dataccc_chart_data.jsChart-ready data loaded by the dashboardindex.htmlInteractive Chart.js dashboard

How it was built

Prototyped as an interactive Chart.js dashboard in Claude Chat, then upgraded in Claude Code to replace sample data with real XBRL financial data from the SEC EDGAR API. Built as an internship project to explore how supply chain disruptions show up in companies' working capital metrics.

Requirements


Python 3.8+
requests library
A modern browser<img width="1698" height="877" alt="Screenshot 2026-07-02 at 4 25 36 PM" src="https://github.com/user-attachments/assets/93e02a3e-4f88-42c6-b252-4a962ddac814" />

