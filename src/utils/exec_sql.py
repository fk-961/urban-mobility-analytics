"""
Simple script used to execute SQL scripts in our database.
"""

import sys
from pathlib import Path
from sqlalchemy import text
from src.db import engine

def exec_sql(sql_path: str | Path) -> None:
    sql_path = Path(sql_path)

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    print(f"Executing SQL script: {sql_path}")

    with sql_path.open("r", encoding="utf-8") as f:
        sql = f.read()

    with engine.begin() as conn:
        for stmt in sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                conn.execute(text(stmt))

    print("Execution complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <sql_script>")
        sys.exit(1)

    exec_sql(sys.argv[1])