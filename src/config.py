import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Useful directories paths
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR/"data"
RAW_DATA_DIR = DATA_DIR/"raw"

RAW_CENSUS_DIR = RAW_DATA_DIR/"census"
RAW_311_DIR = RAW_DATA_DIR/"nyc_311"
RAW_ZONES_DIR = RAW_DATA_DIR/"nyc_taxi_zones"
RAW_TRIPS_DIR = RAW_DATA_DIR/"nyc_trip_records"

# DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"