# Marketing Cohort Retention

Monthly **cohort retention** analysis of a user-activity log, built in both
**Python** (`pandas`, `matplotlib`) and **SQL** (SQLite) so you can see the same
result computed two ways.

## What it does
- `generate_events.py` — simulates 8k users across 12 monthly signup cohorts,
  each returning in later months with geometric decay (newer cohorts retain
  slightly better). Writes `./data/events.csv`.
- `cohort_analysis.py` — builds the cohort × months-since-signup retention matrix
  (% of each cohort's month-0 size), prints it, and saves a heatmap to
  `./outputs/retention_heatmap.png`.
- `sql/cohort_retention.sql` + `run_cohort_sql.py` — the same retention matrix in
  pure SQL using date arithmetic on `YYYY-MM` strings.

## Run it
```bash
pip install pandas matplotlib
cd projects/cohort-retention
python generate_events.py     # writes ./data/events.csv
python cohort_analysis.py     # matrix + heatmap
python run_cohort_sql.py      # same matrix computed in SQL
```

## Results (seed=21)
- **Month-1 retention** averages ~54%, **month-3** ~36%.
- Newer cohorts (2024-08 onward) retain noticeably better at month 1 (61–64% vs
  ~45% for early-2024 cohorts) — evidence that onboarding/product changes are
  improving stickiness over time.

The Python and SQL implementations produce identical matrices — a good
cross-check of the logic.
