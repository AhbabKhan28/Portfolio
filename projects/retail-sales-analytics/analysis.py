"""Exploratory data analysis for the retail sales dataset.

Loads the star-schema CSVs from ./data, computes headline KPIs, and writes a
set of charts to ./outputs. Run `generate_data.py` first.
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import pandas as pd

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "outputs")

plt.rcParams.update({
    "figure.figsize": (9, 5),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})


def load() -> pd.DataFrame:
    fact = pd.read_csv(os.path.join(DATA, "fact_sales.csv"))
    dim_date = pd.read_csv(os.path.join(DATA, "dim_date.csv"), parse_dates=["date"])
    dim_product = pd.read_csv(os.path.join(DATA, "dim_product.csv"))
    dim_store = pd.read_csv(os.path.join(DATA, "dim_store.csv"))
    df = (
        fact.merge(dim_date, on="date_key", how="left")
        .merge(dim_product, on="product_id", how="left")
        .merge(dim_store, on="store_id", how="left")
    )
    return df


def kpis(df: pd.DataFrame) -> None:
    total_rev = df["revenue"].sum()
    total_profit = df["profit"].sum()
    print("=== Headline KPIs ===")
    print(f"Orders            : {len(df):,}")
    print(f"Total revenue     : ${total_rev:,.0f}")
    print(f"Total profit      : ${total_profit:,.0f}")
    print(f"Profit margin     : {total_profit / total_rev:.1%}")
    print(f"Avg order value   : ${df['revenue'].mean():,.2f}")
    print(f"Unique customers  : {df['customer_id'].nunique():,}")


def _save(fig, name: str) -> None:
    path = os.path.join(OUT, name)
    fig.tight_layout()
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")


def chart_monthly_revenue(df: pd.DataFrame) -> None:
    monthly = df.groupby(pd.Grouper(key="date", freq="MS"))["revenue"].sum()
    fig, ax = plt.subplots()
    ax.plot(monthly.index, monthly.values, marker="o", color="#3a7bd5")
    ax.set_title("Monthly Revenue Trend")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    _save(fig, "monthly_revenue.png")


def chart_revenue_by_category(df: pd.DataFrame) -> None:
    cat = df.groupby("category")["revenue"].sum().sort_values()
    fig, ax = plt.subplots()
    ax.barh(cat.index, cat.values, color="#00d2ff")
    ax.set_title("Revenue by Category")
    ax.set_xlabel("Revenue ($)")
    _save(fig, "revenue_by_category.png")


def chart_region_profit(df: pd.DataFrame) -> None:
    reg = df.groupby("region")[["revenue", "profit"]].sum().sort_values("revenue")
    fig, ax = plt.subplots()
    reg.plot(kind="bar", ax=ax, color=["#3a7bd5", "#2ed573"])
    ax.set_title("Revenue vs Profit by Region")
    ax.set_ylabel("$")
    ax.set_xlabel("Region")
    plt.xticks(rotation=0)
    _save(fig, "region_profit.png")


def chart_weekend_effect(df: pd.DataFrame) -> None:
    grp = df.groupby("is_weekend")["revenue"].mean()
    labels = ["Weekday", "Weekend"]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(labels, [grp.get(False, 0), grp.get(True, 0)], color=["#a1a1aa", "#ffa502"])
    ax.set_title("Average Order Revenue: Weekday vs Weekend")
    ax.set_ylabel("Avg revenue ($)")
    _save(fig, "weekend_effect.png")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    df = load()
    kpis(df)
    chart_monthly_revenue(df)
    chart_revenue_by_category(df)
    chart_region_profit(df)
    chart_weekend_effect(df)
    print("\nEDA complete.")


if __name__ == "__main__":
    main()
