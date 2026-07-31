"""Cohort retention analysis.

Reads ./data/events.csv, builds a cohort x months-since-signup retention matrix
(as % of each cohort's month-0 size), prints it, and saves a heatmap to
./outputs/retention_heatmap.png.

Run `generate_events.py` first, then: python cohort_analysis.py
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "outputs")


def build_retention(df: pd.DataFrame) -> pd.DataFrame:
    signup = df["signup_month"].apply(lambda s: pd.Period(s, "M"))
    activity = df["activity_month"].apply(lambda s: pd.Period(s, "M"))
    df = df.assign(period_number=(activity - signup).apply(lambda x: x.n))

    cohort_sizes = (
        df[df["period_number"] == 0]
        .groupby("signup_month")["user_id"].nunique()
    )
    counts = (
        df.groupby(["signup_month", "period_number"])["user_id"]
        .nunique()
        .unstack("period_number")
    )
    retention = counts.divide(cohort_sizes, axis=0) * 100
    return retention.round(1)


def heatmap(retention: pd.DataFrame) -> None:
    os.makedirs(OUT, exist_ok=True)
    data = retention.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(11, 6))
    im = ax.imshow(np.ma.masked_invalid(data), cmap="Blues", aspect="auto",
                   vmin=0, vmax=100)

    ax.set_xticks(range(retention.shape[1]))
    ax.set_xticklabels(retention.columns)
    ax.set_yticks(range(retention.shape[0]))
    ax.set_yticklabels(retention.index)
    ax.set_xlabel("Months since signup")
    ax.set_ylabel("Signup cohort")
    ax.set_title("Cohort Retention (% of cohort active)")

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = data[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                        color="white" if v > 50 else "#16161a", fontsize=8)

    fig.colorbar(im, ax=ax, label="% active")
    fig.tight_layout()
    path = os.path.join(OUT, "retention_heatmap.png")
    fig.savefig(path, dpi=110)
    plt.close(fig)
    print(f"saved {path}")


def main() -> None:
    df = pd.read_csv(os.path.join(DATA, "events.csv"))
    retention = build_retention(df)
    print("=== Cohort Retention Matrix (% of month-0 cohort) ===")
    print(retention.to_string())

    m1 = retention[1].mean()
    m3 = retention[3].mean()
    print(f"\nAverage month-1 retention: {m1:.1f}%")
    print(f"Average month-3 retention: {m3:.1f}%")
    heatmap(retention)


if __name__ == "__main__":
    main()
