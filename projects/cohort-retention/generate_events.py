"""Generate a synthetic user-activity event log for cohort retention analysis.

Each user signs up in some month, then returns in later months with a
probability that decays over time (plus a small cohort-quality trend so newer
cohorts retain slightly better). Writes ./data/events.csv with columns:
    user_id, signup_month, activity_month
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

SEED = 21
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")

N_USERS = 8000
COHORT_MONTHS = pd.period_range("2024-01", "2024-12", freq="M")


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)

    # More recent cohorts get slightly more users and better base retention.
    weights = np.linspace(0.7, 1.3, len(COHORT_MONTHS))
    weights = weights / weights.sum()
    signup_idx = rng.choice(len(COHORT_MONTHS), size=N_USERS, p=weights)

    rows = []
    for user_id, ci in enumerate(signup_idx, start=1):
        signup = COHORT_MONTHS[ci]
        rows.append((user_id, str(signup), str(signup)))  # month 0 = signup

        # Newer cohorts (higher ci) retain a touch better.
        base = 0.45 + 0.02 * ci
        remaining = len(COHORT_MONTHS) - 1 - ci
        for k in range(1, remaining + 1):
            p_return = base * (0.82 ** (k - 1))  # geometric decay
            if rng.random() < p_return:
                rows.append((user_id, str(signup), str(signup + k)))

    df = pd.DataFrame(rows, columns=["user_id", "signup_month", "activity_month"])
    df.to_csv(os.path.join(OUT_DIR, "events.csv"), index=False)
    print(f"Wrote {len(df):,} activity events for {N_USERS:,} users to {OUT_DIR}")


if __name__ == "__main__":
    main()
