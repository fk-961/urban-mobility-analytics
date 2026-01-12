"""
Extracts data from NYC 311 API and stores it as JSON.
We are using public API version, check documentation at https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9.
"""

import os
from dotenv import load_dotenv

import requests
import json
from pathlib import Path
from tqdm import tqdm

from src.config import RAW_DATA_DIR

load_dotenv()

def extract_api(
    limit: int = 1000,
    date: int = 2024,
    MAX_ROWS: int = 100000,
) -> None:
    """Using pagination to get data since original dataset
    is huge (around 20M rows).

    Args:
        limit (int, optional): Batch size.
        date (int, optional): Date of the rows we want to extract.
        MAX_ROWS (int, optional): Max rows of our result dataset.
    """
    offset = 0
    data = []
    
    print("Getting data from API.")
    # initialize tqdm with max rows
    pbar = tqdm(total=MAX_ROWS, desc="Fetching rows", unit="rows", ncols=80, colour="blue")
    
    while True:
        params = {
            "$limit" : limit,
            "$offset" : offset,
            "$where" : f"created_date >= '{date}-01-01T00:00:00.000' AND created_date <= '{date+1}-01-01T00:00:00.000'",
            "$order" : "created_date"
        }
        
        batch_num = int(offset/limit+1)
        tqdm.write(f"Fetching batch {batch_num}...")
        response = requests.get(
            os.getenv("NYC_311_API_URL"),
            params = params,
            timeout = 30
        )
        response.raise_for_status()
        
        batch = response.json()
        pbar.update(len(batch))
        if len(batch) == 0:
            tqdm.write("No more data found.")
            break
            
        data.extend(batch)
        tqdm.write(f"Added batch {batch_num} to data ! Now data has {len(data)} rows.")

        if len(data) >= MAX_ROWS:
            tqdm.write("Max rows per dataset reached.")
            break
        
        offset+=limit
        
    pbar.close()
    print("Gotten data from API, saving as JSON now")
    
    output_dir = RAW_DATA_DIR/"nyc_311"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(
        output_dir/"nyc_311_2024.json",
        "w",
        encoding = "utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii = False,
            indent = 2
        )
    print ("Done !")
    
if __name__ == "__main__":
    extract_api()