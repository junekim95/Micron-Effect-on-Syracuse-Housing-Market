import pandas as pd
import numpy as np

zillow = pd.read_csv("zillow_panel.csv", parse_dates=["date"])
census = pd.read_csv("census_controls.csv")
rates  = pd.read_csv("mortgage_rates.csv", parse_dates=["date"])

# adjustment for merge of the imported files
census["RegionName"] = census["NAME"].str.split(",").str[0].str.strip()
census["year"] = census["year"].astype(int)

zillow["year"] = zillow["date"].dt.year

census_cols = ["RegionName", "year", "pop_total", "median_income",
               "housing_total", "housing_owned", "median_rent_census", "labor_force"]

panel = zillow.merge(
    census[census_cols],
    on=["RegionName", "year"],
    how="left"
)

panel = panel.sort_values(["RegionName", "date"])
fill_cols = ["pop_total", "median_income", "housing_total",
             "housing_owned", "median_rent_census", "labor_force"]
panel[fill_cols] = panel.groupby("RegionName")[fill_cols].ffill()

panel = panel.merge(rates, on="date", how="left")

panel["ownership_rate"] = panel["housing_owned"]/panel["housing_total"]

base = panel[panel["date"] == "2022-01-01"].set_index("RegionName")[["home_value", "rent"]]
base.columns = ["home_value_base", "rent_base"]
panel = panel.merge(base, on="RegionName", how="left")
panel["home_value_idx"] = 100*panel["home_value"]/panel["home_value_base"]
panel["rent_idx"] = 100*panel["rent"]/panel["rent_base"]

panel = panel.drop(columns=["home_value_base", "rent_base", "year"])
panel = panel.sort_values(["RegionName", "date"]).reset_index(drop=True)
panel.to_csv("panel_final.csv", index=False)