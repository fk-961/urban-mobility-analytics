"""
Extracts NYC socioeconomic data from the US Census ACS 5-Year API.
Check documenatation at: https://www.census.gov/data/developers/data-sets/acs-5year.html
"""

import os
from dotenv import load_dotenv

import requests
import json
from pathlib import Path

from src.config import RAW_DATA_DIR

NYC_COUNTIES = ["005", "047", "061", "081", "085"]  # Bronx, Brooklyn, Manhattan, Queens, Staten Island

load_dotenv()

def extract_census_acs() -> None:
    """
    Extracts socioeconomic indicators for NYC counties from the Census API
    and saves them as a JSON file.
    """

    params = {
        "get": ",".join([
            "NAME",              # Geography name
            "B19013_001E",        # Median household income
            "B01003_001E",        # Total population
            "B25077_001E",        # Median home value
            "B23025_005E"         # Unemployment count
        ]),
        "for": "county:" + ",".join(NYC_COUNTIES),
        "in": "state:36",  # New York
        "key": os.getenv("CENSUS_API_KEY")
    }

    print("Requesting Census ACS data...")
    print(os.getenv("CENSUS_API_URL"))
    response = requests.get(os.getenv("CENSUS_API_URL"), params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    # response returns list of lists with first element the headers
    headers = data[0]
    rows = data[1:]

    records = [dict(zip(headers, row)) for row in rows]
    
    output_dir = RAW_DATA_DIR / "census"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir/"acs_nyc_2022.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Saved {len(records)} rows.")


if __name__ == "__main__":
    extract_census_acs()