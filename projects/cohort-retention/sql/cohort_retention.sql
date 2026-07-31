-- Cohort retention in pure SQL (SQLite), from a flat events table
--   events(user_id, signup_month, activity_month)  -- months as 'YYYY-MM'
--
-- Load with:
--   .mode csv
--   .import data/events.csv events
-- (or use ../run_cohort_sql.py which does this for you)

-- Months since signup for every activity event.
WITH periods AS (
    SELECT
        user_id,
        signup_month,
        activity_month,
        (CAST(substr(activity_month, 1, 4) AS INTEGER) * 12
            + CAST(substr(activity_month, 6, 2) AS INTEGER))
      - (CAST(substr(signup_month, 1, 4) AS INTEGER) * 12
            + CAST(substr(signup_month, 6, 2) AS INTEGER)) AS period_number
    FROM events
),
cohort_size AS (
    SELECT signup_month, COUNT(DISTINCT user_id) AS n0
    FROM periods
    WHERE period_number = 0
    GROUP BY signup_month
),
active AS (
    SELECT signup_month, period_number, COUNT(DISTINCT user_id) AS n
    FROM periods
    GROUP BY signup_month, period_number
)
SELECT
    a.signup_month,
    a.period_number,
    a.n,
    ROUND(100.0 * a.n / c.n0, 1) AS retention_pct
FROM active a
JOIN cohort_size c ON c.signup_month = a.signup_month
ORDER BY a.signup_month, a.period_number;
