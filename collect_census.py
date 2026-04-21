import requests
import pandas as pd
import numpy as np

with open("apikey.txt", "r") as f:
    apikey = f.read().strip()

variables = {
    'B01001_001E': 'pop_total',
    'B19013_001E': 'median_income',
    'B25003_001E': 'housing_total',
    'B25003_002E': 'housing_owned',
    'B25064_001E': 'median_rent_census',
    'B23025_002E': 'labor_force'
}

var_string = "NAME," + ",".join(variables.keys())

# 067=onondaga, 029=erie, 055=monroe, 069=lackawanna, 059=lucas
target_counties = [
    ("36", "067"),
    ("36", "029"),
    ("36", "055"),
    ("42", "069"),
    ("39", "095"),
]

years = [2018, 2019, 2021, 2022, 2023]

all_data = []

for year in years:
    api_url = f"https://api.census.gov/data/{year}/acs/acs5"

    # make dictionary for API parameters by county
    for state, county in target_counties:
        payload = {
            "get": var_string,
            "for": f"county:{county}",
            "in": f"state:{state}",
            "key": apikey
        }

        response = requests.get(api_url, params=payload)

        if response.status_code != 200:
            print(f"  error {year} {state}-{county}: {response.status_code}")
            continue

        data = response.json()
        row = dict(zip(data[0], data[1]))
        row['year'] = year
        all_data.append(row)
        print(f"  ok: {year} - {row['NAME']}")

# list to dataframe
df = pd.DataFrame(all_data)
df = df.rename(columns=variables)
df = df.replace(-666666666, np.nan)
df['GEOID'] = df['state'] + df['county']

keep = ['GEOID', 'NAME', 'year'] + list(variables.values())
df = df[keep]

for col in variables.values():
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.to_csv("census_controls.csv", index=False)