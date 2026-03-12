import requests
import pandas as pd
from pathlib import Path

print("Fetching exoplanet data from NASA Exoplanet Archive...")

url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+pl_name,hostname,disc_year,discoverymethod,"
    "pl_rade,pl_masse,pl_orbper,pl_eqt,sy_dist,disc_facility"
    "+from+pscomppars"
    "&format=csv"
)

response = requests.get(url, timeout=60)

if response.status_code == 200:
    output_path = Path("data/exoplanets_raw.csv")
    output_path.write_text(response.text)
    df = pd.read_csv(output_path)
    print(f"Success! {len(df)} exoplanets saved to {output_path}")
    print(df.head())
else:
    print(f"Error: {response.status_code} - {response.text}")
