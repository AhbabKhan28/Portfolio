"""Load events.csv into SQLite and run the cohort retention SQL, printing the
retention curve as a pivoted matrix.

Run `generate_events.py` first, then: python run_cohort_sql.py
"""
from __future__ import annotations

import os
import sqlite3

import pandas as pd

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")
SQL = os.path.join(BASE, "sql", "cohort_retention.sql")


def main() -> None:
    events = pd.read_csv(os.path.join(DATA, "events.csv"), dtype=str)
    conn = sqlite3.connect(":memory:")
    events.to_sql("events", conn, index=False)

    with open(SQL) as fh:
        # Strip the leading comment/instructions; keep the statement.
        query = "\n".join(l for l in fh if not l.lstrip().startswith("--"))

    result = pd.read_sql_query(query, conn)
    conn.close()

    pivot = result.pivot(index="signup_month", columns="period_number",
                         values="retention_pct")
    print("=== Cohort Retention via SQL (% of month-0 cohort) ===")
    print(pivot.to_string())


if __name__ == "__main__":
    main()
