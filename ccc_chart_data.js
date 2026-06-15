/**
 * ccc_chart_data.js
 *
 * Chart.js-ready CCC dataset for 13 companies, 2013-2024.
 * Generated from ccc_data.json (SEC EDGAR 10-K / 20-F XBRL data).
 *
 * Array index → fiscal year:
 *   0→2013  1→2014  2→2015  3→2016  4→2017  5→2018
 *   6→2019  7→2020  8→2021  9→2022 10→2023 11→2024
 *
 * null means the filing data was unavailable for that year.
 *
 * Color / dash legend by industry:
 *   Technology : blue / indigo family
 *   Retail     : green / teal family
 *   Healthcare : rose / purple family
 *   Automotive : orange / amber family
 *   Airlines   : red / pink family
 *
 * dash property maps to Chart.js dataset option `borderDash`.
 */

const YEARS = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];

const CCC_DATA = {

  // ─── Technology ────────────────────────────────────────────────────────────

  AAPL: {
    name:     "Apple Inc.",
    industry: "Technology",
    color:    "#2563EB",   // blue-600
    dash:     [],          // solid
    DIO: [  4.48,  7.33,  7.23,  7.64,  5.55, 13.49, 10.24,  9.15,  9.16, 14.16,  8.48, 10.34],
    DSO: [ 36.85, 30.56, 37.29, 33.64, 24.60, 30.25, 36.92, 31.51, 22.61, 34.94, 28.12, 27.31],
    DPO: [119.96, 92.93,103.39,115.39, 97.17,122.92,144.63,103.06, 95.42,117.89,109.88,102.23],
    CCC: [-78.62,-55.05,-58.87,-74.11,-67.01,-79.17,-97.47,-62.40,-63.65,-68.78,-73.28,-64.58],
  },

  MSFT: {
    name:     "Microsoft Corp.",
    industry: "Technology",
    color:    "#0EA5E9",   // sky-500
    dash:     [6, 3],      // dashed
    DIO: [ 26.64, 40.35, 47.63, 63.50, 38.38, 24.29, 28.36, 19.63, 16.12, 20.88, 26.15, 14.57],
    DSO: [ 82.35, 86.57, 91.63, 75.28, 71.29, 89.82,100.09, 97.65, 92.85, 97.09, 96.11, 89.63],
    DPO: [ 97.83,100.53,133.07,144.22,117.60, 82.29, 91.80, 89.29,106.58,120.11,132.77,105.42],
    CCC: [ 11.16, 26.40,  6.19, -5.44, -7.93, 31.82, 36.65, 27.99,  2.38, -2.14,-10.51, -1.23],
  },

  GOOGL: {
    name:     "Alphabet Inc.",
    industry: "Technology",
    color:    "#6366F1",   // indigo-500
    dash:     [2, 3],      // dotted
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [   null,  null,  null,  6.98,  3.47,  7.78,  8.86,  6.12,  3.70,  5.04,  null,  null],
    DSO: [   null,  null,  null, 63.91, 68.81, 74.14, 68.61, 67.56, 69.75, 78.60,  null,  null],
    DPO: [   null,  null,  null, 27.43, 26.45, 32.59, 35.06, 34.09, 28.37, 26.01,  null,  null],
    CCC: [   null,  null,  null, 43.45, 45.83, 49.33, 42.42, 39.60, 45.07, 57.63,  null,  null],
  },

  DELL: {
    name:     "Dell Technologies",
    industry: "Technology",
    color:    "#818CF8",   // indigo-400
    dash:     [8, 3, 2, 3], // dash-dot
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [   7.97,  null,  4.92,  6.46,  6.99,  6.64,  6.20,  6.68,  7.31,  5.02,  3.73,  3.97],
    DSO: [  53.29,  null, 47.41, 48.18, 59.66, 45.59, 55.38, 86.05, 86.10, 55.04, 52.50, 46.21],
    DPO: [  36.86,  null, 28.13, 30.35, 36.09, 30.76, 36.20, 41.08, 45.85, 33.26, 35.66, 34.85],
    CCC: [  24.39,  null, 24.21, 24.29, 30.56, 21.47, 25.38, 51.65, 47.55, 26.80, 20.57, 15.32],
  },

  // ─── Retail ────────────────────────────────────────────────────────────────

  WMT: {
    name:     "Walmart Inc.",
    industry: "Retail",
    color:    "#16A34A",   // green-600
    dash:     [],          // solid
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [  47.73,  null, 46.48, 46.01, 44.46, 43.52, 44.24, 43.27, 42.09, 41.58, 49.07, 48.14],
    DSO: [   5.53,  null,  5.20,  5.19,  4.23,  4.42,  4.26,  4.63,  4.49,  4.57,  5.44,  5.10],
    DPO: [  41.49,  null, 38.76, 39.15, 38.48, 41.89, 46.57, 46.00, 44.50, 45.45, 47.99, 45.72],
    CCC: [  11.77,  null, 12.91, 12.06, 10.21,  6.05,  1.92,  1.90,  2.09,  0.70,  6.53,  7.51],
  },

  AMZN: {
    name:     "Amazon.com Inc.",
    industry: "Retail",
    color:    "#0D9488",   // teal-600
    dash:     [6, 3],      // dashed
    DIO: [ 59.04, 58.84, 55.91, 59.58, 58.38, 66.36, 56.00, 53.76, 52.47, 51.06, 46.11, 42.10],
    DSO: [ 28.98, 28.48, 27.51, 23.19, 28.44, 35.33, 34.22, 32.62, 31.93, 31.10, 32.91, 37.11],
    DPO: [130.37,120.15,110.88,118.64,128.93,143.15,124.54,123.76,159.95,123.07,106.68,107.39],
    CCC: [-42.35,-32.83,-27.46,-35.87,-42.10,-41.45,-34.31,-37.37,-75.55,-40.91,-27.66,-28.18],
  },

  COST: {
    name:     "Costco Wholesale",
    industry: "Retail",
    color:    "#84CC16",   // lime-500
    dash:     [2, 3],      // dotted
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [  33.32, 33.19, 33.57, 33.02, 32.39, 34.88,  null, 33.77, 33.63, 35.80, 38.29, 30.48],
    DSO: [   4.21,  4.42,  3.98,  3.97,  3.93,  4.40,  null,  3.96,  3.70,  3.95,  4.17,  3.67],
    DPO: [  34.29, 33.09, 33.71, 33.41, 27.49, 34.08,  null, 34.61, 38.93, 40.99, 38.17, 32.01],
    CCC: [   3.24,  4.51,  3.85,  3.58,  8.83,  5.20,  null,  3.12, -1.60, -1.25,  4.30,  2.15],
  },

  // ─── Healthcare ────────────────────────────────────────────────────────────

  JNJ: {
    name:     "Johnson & Johnson",
    industry: "Healthcare",
    color:    "#BE185D",   // pink-700
    dash:     [],          // solid
    DIO: [134.37,132.77,133.70,129.22,138.03,146.83,123.38,121.53,123.77,133.37,160.15,165.92],
    DSO: [ 63.48, 63.60, 56.23, 52.71, 60.94, 68.49, 67.31, 64.79, 60.39, 67.55, 65.08, 67.87],
    DPO: [104.53,105.60,124.70,107.00,117.25,122.45,108.14,115.11,125.90,141.95,154.24,142.94],
    CCC: [ 93.31, 90.76, 65.23, 74.93, 81.72, 92.86, 82.55, 71.20, 58.25, 58.97, 70.99, 90.85],
  },

  PFE: {
    name:     "Pfizer Inc.",
    industry: "Healthcare",
    color:    "#A855F7",   // purple-500
    dash:     [6, 3],      // dashed
    DIO: [177.42,229.16,215.63,286.34,256.61,224.47,244.07,287.06,363.46,389.74,106.36,108.29],
    DSO: [ 63.84, 62.49, 59.44, 60.16, 61.45, 56.80, 55.74, 60.55, 70.61,100.59, 54.29, 41.73],
    DPO: [ 85.29,120.19,122.23,137.97,171.60,137.92,151.94,157.87,194.10,239.98, 80.64, 71.31],
    CCC: [155.96,171.45,152.85,208.53,146.46,143.36,147.87,189.74,239.97,250.35, 80.01, 78.70],
  },

  // ─── Automotive ────────────────────────────────────────────────────────────

  F: {
    name:     "Ford Motor Company",
    industry: "Automotive",
    color:    "#EA580C",   // orange-600
    dash:     [],          // solid
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [   null,  null,  null, 24.29, 26.10, 32.32, 31.19, 28.89, 29.29, 39.06, 44.82, 42.51],
    DSO: [   null,  null,  null, 27.97, 25.85, 25.49, 26.06, 21.03, 23.40, 32.64, 42.11, 36.03],
    DPO: [   null,  null,  null, 59.18, 62.46, 67.34, 59.81, 55.37, 60.17, 72.35, 81.52, 70.59],
    CCC: [   null,  null,  null, -6.92,-10.52, -9.53, -2.56, -5.46, -7.49, -0.65,  5.42,  7.94],
  },

  TM: {
    name:     "Toyota Motor Corp",
    industry: "Automotive",
    color:    "#D97706",   // amber-600
    dash:     [6, 3],      // dashed
    // Note: values are ratios of JPY figures — days metrics are currency-neutral.
    // 2017 and 2021-2024 missing due to IFRS XBRL gaps in EDGAR.
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [  39.65, 38.40, 39.03, 35.97,  null, 40.63, 36.21, 35.94,  null,  null,  null,  null],
    DSO: [  38.73, 33.68, 29.96, 26.81,  null, 27.19, 26.80, 28.65,  null,  null,  null,  null],
    DPO: [  48.84, 44.85, 44.02, 41.70,  null, 43.66, 36.88, 35.80,  null,  null,  null,  null],
    CCC: [  29.53, 27.23, 24.97, 21.08,  null, 24.17, 26.13, 28.79,  null,  null,  null,  null],
  },

  // ─── Airlines ──────────────────────────────────────────────────────────────

  DAL: {
    name:     "Delta Air Lines",
    industry: "Airlines",
    color:    "#DC2626",   // red-600
    dash:     [],          // solid
    // Note: COGS is proxied from total operating expenses (no separate COGS line
    // in airline XBRL). 2019-2021 missing due to inventory tag gap in EDGAR.
    //         2013   2014   2015   2016   2017   2018   2019   2020   2021   2022   2023   2024
    DIO: [   6.82,  7.47,  5.67,  3.63,  5.76, 10.30,  null,  null,  null, 13.56, 18.55, 10.22],
    DSO: [  17.60, 16.02, 22.20, 18.27, 18.51, 21.99,  null,  null,  null, 51.33, 38.77, 22.59],
    DPO: [  25.25, 24.34, 27.84, 26.24, 28.53, 40.87,  null,  null,  null, 52.35, 66.53, 34.59],
    CCC: [  -0.84, -0.85,  0.02, -4.35, -4.27, -8.58,  null,  null,  null, 12.54, -9.20, -1.78],
  },

  LUV: {
    name:     "Southwest Airlines",
    industry: "Airlines",
    color:    "#F43F5E",   // rose-500
    dash:     [6, 3],      // dashed
    // Note: Southwest does not use standard XBRL inventory tags — inventory
    // data is unavailable via the SEC EDGAR companyfacts API for all years,
    // so DIO/DSO/DPO/CCC cannot be calculated.
    DIO: [null, null, null, null, null, null, null, null, null, null, null, null],
    DSO: [null, null, null, null, null, null, null, null, null, null, null, null],
    DPO: [null, null, null, null, null, null, null, null, null, null, null, null],
    CCC: [null, null, null, null, null, null, null, null, null, null, null, null],
  },

};

// Convenience: group tickers by industry for filtered chart views.
const INDUSTRIES = {
  Technology: ["AAPL", "MSFT", "GOOGL", "DELL"],
  Retail:     ["WMT",  "AMZN", "COST"],
  Healthcare: ["JNJ",  "PFE"],
  Automotive: ["F",    "TM"],
  Airlines:   ["DAL",  "LUV"],
};
