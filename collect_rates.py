import requests
import pandas as pd

with open("fredkey.txt", "r") as f:
    fred_key = f.read().strip()

url = "https://api.stlouisfed.org/fred/series/observations"

payload = {
    "series_id": "MORTGAGE30US",
    "observation_start": "2018-01-01",
    "observation_end": "2026-03-31",
    "api_key": fred_key,
    "file_type": "json"
}

response = requests.get(url, params=payload)

if response.status_code != 200:
    print(f"error: {response.status_code}")
    print(response.text)
    assert False

data = response.json()

# trimming out unnecessary data, leaving date and interest rate value only
rates = pd.DataFrame(data['observations'])[['date', 'value']]
rates['date'] = pd.to_datetime(rates['date'])
rates['mortgage_rate'] = pd.to_numeric(rates['value'], errors='coerce')
rates = rates.drop(columns='value')

# monthly avererage for matching with zillow data
rates['date'] = rates['date'].dt.to_period('M').dt.to_timestamp()
monthly = rates.groupby('date')['mortgage_rate'].mean().reset_index()

monthly.to_csv("mortgage_rates.csv", index=False)