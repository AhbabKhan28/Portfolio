-- Analytical queries answering common retail business questions (SQLite).
-- Each query is preceded by the question it answers.

-- Q1: Top 5 product categories by total revenue and profit margin.
SELECT p.category,
       ROUND(SUM(f.revenue), 2)              AS revenue,
       ROUND(SUM(f.profit), 2)               AS profit,
       ROUND(100.0 * SUM(f.profit) / SUM(f.revenue), 1) AS margin_pct
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
GROUP BY p.category
ORDER BY revenue DESC
LIMIT 5;

-- Q2: Monthly revenue trend with year-over-year comparison.
SELECT d.year,
       d.month,
       d.month_name,
       ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Q3: Revenue by region, with each region's share of the total.
SELECT s.region,
       ROUND(SUM(f.revenue), 2) AS revenue,
       ROUND(100.0 * SUM(f.revenue) / (SELECT SUM(revenue) FROM fact_sales), 1) AS pct_of_total
FROM fact_sales f
JOIN dim_store s ON s.store_id = f.store_id
GROUP BY s.region
ORDER BY revenue DESC;

-- Q4: Weekend vs weekday average order value.
SELECT CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
       COUNT(*)                    AS orders,
       ROUND(AVG(f.revenue), 2)    AS avg_order_value
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
GROUP BY day_type;

-- Q5: Top 10 customers by lifetime revenue.
SELECT f.customer_id,
       c.segment,
       COUNT(*)                 AS orders,
       ROUND(SUM(f.revenue), 2) AS lifetime_revenue
FROM fact_sales f
JOIN dim_customer c ON c.customer_id = f.customer_id
GROUP BY f.customer_id, c.segment
ORDER BY lifetime_revenue DESC
LIMIT 10;

-- Q6: Running (cumulative) revenue by month using a window function.
WITH monthly AS (
    SELECT d.year, d.month, SUM(f.revenue) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON d.date_key = f.date_key
    GROUP BY d.year, d.month
)
SELECT year,
       month,
       ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY year, month), 2) AS cumulative_revenue
FROM monthly
ORDER BY year, month;
