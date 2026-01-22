"""
Entry point of our project
"""

from src.utils.create_raw_table import create_raw_table
from src.config import (
    RAW_ZONES_DIR,
    RAW_CENSUS_DIR,
    RAW_311_DIR,
    RAW_TRIPS_DIR
)

zones_type_dict = {
    "shape_geometry" : "string",
    "shape_length" : float,
    "shape_area" : float,
    "zone" : "string",
    "location_id" : float,
    "borough" : "string"
}

requests311_type_dict = {
    "created_date" : "datetime64[s]",
    "complaint_type" : "string",
    "incident_address" : "string",
    "city" : "string",
    "borough" : "string",
    "location" : "string",
    "location_type" : "string"
}

trips_type_dict = {
    'tpep_pickup_datetime' : 'datetime64[s]',
    'tpep_dropoff_datetime' : 'datetime64[s]',
    'passenger_count' : float,
    'trip_distance' : float, # in miles
    'PULocationID'.lower() : float,
    'DOLocationID'.lower() : float,
    'fare_amount' : float,
    'tip_amount' : float,
    'total_amount' : float
}

def main():
    print("Running ETL pipeline !")
    print(30*"=")
    
    print("\nExtracting Taxi Zones")
    print(30*"=")
    create_raw_table(
        "raw_zones",
        RAW_ZONES_DIR,
        zones_type_dict
    )
    
    print("\nExtracting ACS Census")
    print(30*"=")
    create_raw_table(
        "raw_census",
        RAW_CENSUS_DIR
    )
    
    print("\nExtracting 311 Service requests")
    print(30*"=")
    create_raw_table(
        "raw_311",
        RAW_311_DIR,
        requests311_type_dict
    )
    
    print("\nExtracting trip records")
    print(30*"=")
    create_raw_table(
        "raw_trips",
        RAW_TRIPS_DIR,
        trips_type_dict
    )
    
    print("Raw data extraction complete !")
    
if __name__ == "__main__":
    main()