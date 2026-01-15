"""
Creates the first tables consisting of the raw datasets extracted.
No transformation is done here (beside type matching).
Raw data is at data/raw.
"""

import pandas as pd
from pathlib import Path
from src.db import engine

def load_raw_files(
    files_path : Path
) -> pd.DataFrame:
    """Checks type of files in a directory and converts them
    to pandas DataFrame depending on the extension of each file.

    Args:
        files_path (Path): Directories of the files.

    Returns:
        pd.DataFrame: Pandas dataframe of all the data.
    """
    df_list = []
    
    print(f"Looking for CSV/JSON/PARQUET data in {files_path}...")
    for p in files_path.rglob("*"):
        if p.is_file() and p.suffix == ".csv":
            print(f"Found {p}")
            df_list.append(pd.read_csv(p))
        if p.is_file() and p.suffix == ".parquet":
            print(f"Found {p}")
            df_list.append(pd.read_parquet(p))
        if p.is_file() and p.suffix == ".json":
            print(f"Found {p}")
            df_list.append(pd.read_json(p))
    
    return pd.concat(df_list, ignore_index=True)

def create_raw_table(
    table_name : str,
    files_path : Path,
    type_dict : dict,
    if_exists : str = "append"
) -> None:
    """Converts the metadata in the given files_path to tables in our
    postgres database.

    Args:
        table_name (str): Table name.
        files_path (str): Path to our raw metadata directory.
        type_dict (dict): Dictionary to type match with our database
        if_exists (str, optional): What happens if table already exists.
    """
    df = load_raw_files(files_path)
    df.columns = df.columns.str.lower().str.replace(" ","_")
    df = df[list(type_dict.keys())].astype(type_dict)
    
    df.to_sql(
        table_name,
        con = engine,
        if_exists = if_exists,
        index = False
    )
    
    print(f"Created {table_name} from raw data !")