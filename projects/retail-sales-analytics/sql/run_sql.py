"""Load the CSV star schema into an in-memory SQLite DB and run the analytical
queries in queries.sql, printing each result.

Usage:
    python sql/run_sql.py            # in-memory (default)
    python sql/run_sql.py retail.db  # persist to a file for Power BI / DBeaver
"""
from __future__ import annotations

import os
import re
import sqlite3
import sys

import pandas as pd

BASE = os.path.dirname(__file__)
DATA = os.path.join(os.path.dirname(BASE), "data")

TABLES = ["dim_date", "dim_product", "dim_store", "dim_customer", "fact_sales"]


def build_db(conn: sqlite3.Connection) -> None:
    with open(os.path.join(BASE, "schema.sql")) as fh:
        conn.executescript(fh.read())
    for table in TABLES:
        df = pd.read_csv(os.path.join(DATA, f"{table}.csv"))
        df.to_sql(table, conn, if_exists="append", index=False)
    conn.commit()


def split_statements(sql: str) -> list[tuple[str, str]]:
    """Return (comment_label, statement) pairs, keying off leading -- comments."""
    blocks = [b.strip() for b in sql.split(";") if b.strip()]
    out = []
    for b in blocks:
        labels = re.findall(r"--\s*(Q\d[^\n]*)", b)
        label = labels[0] if labels else b.splitlines()[0][:60]
        stmt = "\n".join(l for l in b.splitlines() if not l.strip().startswith("--"))
        if stmt.strip():
            out.append((label, stmt))
    return out


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else ":memory:"
    conn = sqlite3.connect(db_path)
    build_db(conn)

    with open(os.path.join(BASE, "queries.sql")) as fh:
        for label, stmt in split_statements(fh.read()):
            print("\n" + "=" * 70)
            print(label)
            print("=" * 70)
            print(pd.read_sql_query(stmt, conn).head(12).to_string(index=False))

    conn.close()
    if db_path != ":memory:":
        print(f"\nPersisted database to {db_path}")


if __name__ == "__main__":
    main()
