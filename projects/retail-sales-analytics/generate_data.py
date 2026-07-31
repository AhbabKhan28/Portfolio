"""Generate a realistic synthetic retail sales dataset (star schema).

Produces reproducible CSVs under ./data:
    dim_date.csv, dim_product.csv, dim_store.csv, dim_customer.csv, fact_sales.csv

The data has deliberate, discoverable patterns (weekend uplift, Q4 seasonality,
category price tiers, regional differences) so the downstream EDA/SQL/Power BI
work surfaces real insights.
"""
from __future__ import annotations

import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 42
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")

START_DATE = date(2023, 1, 1)
END_DATE = date(2024, 12, 31)
N_CUSTOMERS = 3000
N_ORDERS = 60000

CATEGORIES = {
    "Electronics": (150, 900),
    "Home & Kitchen": (20, 220),
    "Clothing": (12, 120),
    "Sports & Outdoors": (18, 260),
    "Books": (6, 45),
    "Beauty": (8, 90),
}
REGIONS = ["North", "South", "East", "West"]


def _build_dim_date() -> pd.DataFrame:
    days = pd.date_range(START_DATE, END_DATE, freq="D")
    df = pd.DataFrame({"date": days})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["day_of_week"] = df["date"].dt.strftime("%A")
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    return df[[
        "date_key", "date", "year", "quarter", "month",
        "month_name", "day_of_week", "is_weekend",
    ]]


def _build_dim_product(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    pid = 1
    for cat, (lo, hi) in CATEGORIES.items():
        n = rng.integers(12, 22)
        for i in range(n):
            base_price = round(float(rng.uniform(lo, hi)), 2)
            cost = round(base_price * float(rng.uniform(0.45, 0.75)), 2)
            rows.append({
                "product_id": pid,
                "product_name": f"{cat[:3].upper()}-{i+1:03d}",
                "category": cat,
                "unit_price": base_price,
                "unit_cost": cost,
            })
            pid += 1
    return pd.DataFrame(rows)


def _build_dim_store(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for i, region in enumerate(REGIONS, start=1):
        for j in range(1, 4):
            rows.append({
                "store_id": (i - 1) * 3 + j,
                "store_name": f"{region} Store {j}",
                "region": region,
                # West performs a bit better; East a bit worse.
                "region_multiplier": {"West": 1.15, "North": 1.0,
                                       "South": 0.95, "East": 0.85}[region],
            })
    return pd.DataFrame(rows)


def _build_dim_customer(rng: np.random.Generator) -> pd.DataFrame:
    signup = pd.to_datetime(
        rng.integers(
            pd.Timestamp(START_DATE).value // 10**9,
            pd.Timestamp(END_DATE).value // 10**9,
            N_CUSTOMERS,
        ),
        unit="s",
    ).normalize()
    return pd.DataFrame({
        "customer_id": np.arange(1, N_CUSTOMERS + 1),
        "signup_date": signup,
        "segment": rng.choice(
            ["Consumer", "Corporate", "Home Office"],
            N_CUSTOMERS, p=[0.55, 0.30, 0.15],
        ),
    })


def _seasonal_weight(d: pd.Timestamp) -> float:
    w = 1.0
    if d.month in (11, 12):  # Q4 holiday uplift
        w *= 1.6
    if d.month in (1, 2):    # post-holiday slump
        w *= 0.8
    if d.dayofweek >= 5:     # weekend uplift
        w *= 1.25
    return w


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)

    dim_date = _build_dim_date()
    dim_product = _build_dim_product(rng)
    dim_store = _build_dim_store(rng)
    dim_customer = _build_dim_customer(rng)

    # Sample order dates weighted by seasonality.
    day_weights = dim_date["date"].apply(lambda x: _seasonal_weight(pd.Timestamp(x))).to_numpy()
    day_weights = day_weights / day_weights.sum()
    order_dates = rng.choice(dim_date["date_key"].to_numpy(), size=N_ORDERS, p=day_weights)

    product_ids = rng.choice(dim_product["product_id"].to_numpy(), size=N_ORDERS)
    store_ids = rng.choice(dim_store["store_id"].to_numpy(), size=N_ORDERS)
    customer_ids = rng.choice(dim_customer["customer_id"].to_numpy(), size=N_ORDERS)
    quantities = rng.integers(1, 6, size=N_ORDERS)

    fact = pd.DataFrame({
        "order_id": np.arange(1, N_ORDERS + 1),
        "date_key": order_dates,
        "product_id": product_ids,
        "store_id": store_ids,
        "customer_id": customer_ids,
        "quantity": quantities,
    })

    fact = fact.merge(
        dim_product[["product_id", "unit_price", "unit_cost"]], on="product_id", how="left"
    ).merge(
        dim_store[["store_id", "region_multiplier"]], on="store_id", how="left"
    )

    discount = rng.choice([0.0, 0.05, 0.10, 0.20], size=N_ORDERS, p=[0.6, 0.2, 0.15, 0.05])
    fact["discount"] = discount
    fact["revenue"] = (
        fact["quantity"] * fact["unit_price"] * (1 - fact["discount"]) * fact["region_multiplier"]
    ).round(2)
    fact["cost"] = (fact["quantity"] * fact["unit_cost"]).round(2)
    fact["profit"] = (fact["revenue"] - fact["cost"]).round(2)

    fact = fact.drop(columns=["unit_price", "unit_cost", "region_multiplier"])

    dim_date.to_csv(os.path.join(OUT_DIR, "dim_date.csv"), index=False)
    dim_product.drop(columns=["unit_cost"]).to_csv(
        os.path.join(OUT_DIR, "dim_product.csv"), index=False)
    dim_store.drop(columns=["region_multiplier"]).to_csv(
        os.path.join(OUT_DIR, "dim_store.csv"), index=False)
    dim_customer.to_csv(os.path.join(OUT_DIR, "dim_customer.csv"), index=False)
    fact.to_csv(os.path.join(OUT_DIR, "fact_sales.csv"), index=False)

    print(f"Wrote {len(fact):,} sales rows and 4 dimension tables to {OUT_DIR}")


if __name__ == "__main__":
    main()
