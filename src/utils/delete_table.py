"""
Simple script to delete a table from our PostgreSQL database.
"""

import sys
from sqlalchemy import text
from src.db import engine
from pathlib import Path

def delete_table(table_name: str) -> None:
    print(f"Looking for table '{table_name}'...")

    with engine.begin() as conn:
        # check if table exists
        exists = conn.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = :table_name
                );
            """),
            {"table_name": table_name}
        ).scalar()

        if not exists:
            print(f"Table '{table_name}' not found.")
            return

        print("Table found!")
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        print(f"Table '{table_name}' deleted.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <table_name>")
        sys.exit(1)

    delete_table(sys.argv[1])
