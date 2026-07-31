# Retail Sales Analytics

End-to-end analysis of a retail sales dataset using **Python**, **SQL**, and **Power BI**.
The dataset is a synthetic but realistic star schema (2 years, 60k orders) with
built-in seasonality, regional, and category patterns to discover.

## Stack
- **Python** — `pandas`, `matplotlib` for data generation and EDA.
- **SQL** — SQLite schema + analytical queries (window functions, YoY, cohorts).
- **Power BI** — star-schema model + DAX measures ([build guide](powerbi/README.md)).

## Layout
```
generate_data.py      # build the star-schema CSVs into ./data (reproducible, seed=42)
analysis.py           # EDA -> KPIs + charts into ./outputs
sql/schema.sql        # table definitions
sql/queries.sql       # 6 business questions answered in SQL
sql/run_sql.py        # load CSVs into SQLite and run the queries
powerbi/README.md     # Power BI model + DAX + report layout
```

## Run it
```bash
pip install pandas matplotlib
cd projects/retail-sales-analytics
python generate_data.py     # writes ./data/*.csv
python analysis.py          # writes ./outputs/*.png and prints KPIs
python sql/run_sql.py       # runs the SQL analytics
# optional: persist a DB for Power BI / DBeaver
python sql/run_sql.py retail.db
```

## Headline results (seed=42)
- **Total revenue** ≈ $25.2M, **profit margin** ≈ 35.9% across 60k orders.
- **Electronics** is the top category by revenue; **Clothing/Beauty** have the best margins.
- Strong **Q4 seasonal peak** (Nov–Dec) in the monthly trend.
- **West** region leads revenue (~29.5%); **East** trails (~21.1%).

Charts are written to `./outputs/` (regenerate with `analysis.py`).
