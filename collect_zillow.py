import pandas as pd

# set target group (onondaga) as "1" and comparing (controlled) group as "0")
TARGET_IDS = {
    2465: ("Onondaga County",  "NY", 1),
    157:  ("Erie County",      "NY", 0),
    1223: ("Monroe County",    "NY", 0),
    2949: ("Lackawanna County","PA", 0),
    616:  ("Lucas County",     "OH", 0),
}

META_COLS = ["RegionID", "SizeRank", "RegionName", "RegionType",
             "StateName", "State", "Metro", "StateCodeFIPS", "MunicipalCodeFIPS"]

def load_zillow(filepath, value_name, start_year=2018):

    df = pd.read_csv(filepath, dtype={"StateCodeFIPS": str, "MunicipalCodeFIPS": str})

    df = df[df["RegionID"].isin(TARGET_IDS.keys())].copy()

    date_cols = [c for c in df.columns if c not in META_COLS]
    date_cols = [c for c in date_cols if int(c[:4]) >= start_year]

    long = df.melt(
        id_vars=["RegionID", "RegionName", "State"],
        value_vars=date_cols,
        var_name="date",
        value_name=value_name
    )

    long["date"] = pd.to_datetime(long["date"]).dt.to_period("M").dt.to_timestamp()

    long["treated"] = long["RegionID"].map(lambda x: TARGET_IDS[x][2])

    return long

# import csv files into the function
zhvi = load_zillow("homevalue_county_zillow.csv", value_name="home_value")
zori = load_zillow("rent_county_zillow.csv", value_name="rent")

# merge two files based on regiion ID index
panel = zhvi.merge(
    zori[["RegionID", "date", "rent"]],
    on=["RegionID", "date"],
    how="left"
)

# set the data after Micron inveestment announcment as "post" for comparison
panel["post"] = (panel["date"] >= "2022-10-01").astype(int)
panel["did"]  = panel["treated"] * panel["post"]

panel = panel.sort_values(["RegionName", "date"]).reset_index(drop=True)
panel.to_csv("zillow_panel.csv", index=False)