-- Star schema for the retail sales dataset (SQLite dialect).
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_customer;

CREATE TABLE dim_date (
    date_key    INTEGER PRIMARY KEY,
    date        TEXT,
    year        INTEGER,
    quarter     INTEGER,
    month       INTEGER,
    month_name  TEXT,
    day_of_week TEXT,
    is_weekend  INTEGER
);

CREATE TABLE dim_product (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    unit_price   REAL
);

CREATE TABLE dim_store (
    store_id   INTEGER PRIMARY KEY,
    store_name TEXT,
    region     TEXT
);

CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,
    signup_date TEXT,
    segment     TEXT
);

CREATE TABLE fact_sales (
    order_id    INTEGER PRIMARY KEY,
    date_key    INTEGER REFERENCES dim_date(date_key),
    product_id  INTEGER REFERENCES dim_product(product_id),
    store_id    INTEGER REFERENCES dim_store(store_id),
    customer_id INTEGER REFERENCES dim_customer(customer_id),
    quantity    INTEGER,
    discount    REAL,
    revenue     REAL,
    cost        REAL,
    profit      REAL
);

CREATE INDEX idx_fact_date ON fact_sales(date_key);
CREATE INDEX idx_fact_product ON fact_sales(product_id);
CREATE INDEX idx_fact_store ON fact_sales(store_id);
