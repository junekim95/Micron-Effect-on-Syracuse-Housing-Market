# MICRON EFFECT ON SYRACUSE HOUSING MARKET

Analyzes whether Micron Technology's October 2022 semiconductor fab announcement 
in Clay, NY generated a measurable impact on local home values and rents — using 
a Diff-in-Differences design comparing Onondaga County against four comparable 
Rust Belt counties from 2018 to 2026.

## Purpose

Large-scale industrial announcements can reshape local housing markets years before 
a single worker is hired. This project quantifies that "announcement effect" for 
Micron's $100 billion fab project in Syracuse, NY. Given that the first fab is not 
expected to be operational until 2030, any price movement observed today reflects 
pure market expectation — not actual employment inflows.

This project:
- Collects county-level home value and rent data from Zillow Research
- Pulls socioeconomic controls from the U.S. Census ACS API
- Retrieves 30-year mortgage rate data from the FRED API
- Merges all sources into a single monthly panel dataset (2018–2026)
- Applies a Diff-in-Differences estimator to isolate Micron's announcement effect
- Generates four figures visualizing parallel trends, gap growth, and DiD estimates

## Example Output

| File | Description |
|---|---|
| `fig1_parallel_trends.png` | Onondaga vs. control group index, home value & rent |
| `fig2_gap_trend.png` | Monthly gap between Onondaga and control average |
| `fig3_did_estimates.png` | DiD bar chart: home value and rent |
| `fig4_county_trends.png` | Individual county trends, home value & rent |

## Key Findings

- **Home Value DiD: +6.92 index pts** (~$16,500 above trend, base Jan 2022 = 100)
- **Rent DiD: +1.76 index pts** (~$27/month above trend)
- Home values reacted nearly 4× stronger than rents — consistent with 
  expectation-driven asset pricing
- The gap between Onondaga and the control group began precisely at the 
  October 2022 announcement and has widened to +13 index points by early 2026
- Effect is observable before any construction or employment — purely driven 
  by market expectations

## Data Sources

| Dataset | Source | How to Access |
|---|---|---|
| Zillow ZHVI (home values) | Zillow Research | Download CSV at zillow.com/research/data — Geography: County |
| Zillow ZORI (rent) | Zillow Research | Download CSV at zillow.com/research/data — Geography: County |
| Census ACS 5-year | U.S. Census Bureau | Free API — save key in `apikey.txt` |
| 30-yr Mortgage Rate | FRED, Federal Reserve | Free API — save key in `fredkey.txt` |

### To get a Census API key (free):
1. Go to https://api.census.gov/data/key_signup.html
2. Register with your email
3. Save the key in a file called `apikey.txt` in the project directory

### To get a FRED API key (free):
1. Go to https://fredaccount.stlouisfed.org/login/secure/
2. Create an account and generate an API key
3. Save the key in a file called `fredkey.txt` in the project directory

## Scripts

| Script | Description |
|---|---|
| `collect_zillow.py` | Filters 5 counties from Zillow CSV, wide → long format, adds DiD columns |
| `collect_census.py` | Census ACS API call per county × year, cleans missing values |
| `collect_rates.py` | FRED API → weekly mortgage rate, aggregated to monthly average |
| `clean.py` | Merges all 3 sources, forward-fills Census gaps, builds Jan 2022 = 100 index |
| `analyze.py` | Computes DiD estimates and generates figures 1–4 |

## Limitations

- **Announcement effect only** — no actual employment inflows yet; first fab 
  operational in 2030
- **Control group is manually selected** — counties chosen based on comparable 
  size and economic structure, not statistical matching
- **No regression-based DiD** — socioeconomic variables from Census were collected 
  but not formally incorporated into the estimator; intended for future extension
