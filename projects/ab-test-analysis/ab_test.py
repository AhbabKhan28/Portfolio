"""A/B test analysis: does a new landing page increase conversion?

Simulates a two-group experiment (control vs treatment) with a reproducible
seed, then runs a full frequentist analysis:
  - conversion rates + absolute/relative lift
  - two-proportion z-test (p-value)
  - 95% confidence interval for the difference
  - statistical power / minimum detectable effect context
and saves a summary chart to ./outputs.

Run: python ab_test.py
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

SEED = 7
OUT = os.path.join(os.path.dirname(__file__), "outputs")

# Ground-truth simulation parameters.
N_PER_GROUP = 12_000
CONTROL_RATE = 0.118
TREATMENT_RATE = 0.132  # ~1.4pp absolute lift


def simulate(rng: np.random.Generator):
    control = rng.binomial(1, CONTROL_RATE, N_PER_GROUP)
    treatment = rng.binomial(1, TREATMENT_RATE, N_PER_GROUP)
    return control, treatment


def two_proportion_z_test(c: np.ndarray, t: np.ndarray):
    n_c, n_t = len(c), len(t)
    x_c, x_t = c.sum(), t.sum()
    p_c, p_t = x_c / n_c, x_t / n_t
    p_pool = (x_c + x_t) / (n_c + n_t)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
    z = (p_t - p_c) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    # 95% CI for the difference (unpooled SE).
    se_diff = np.sqrt(p_c * (1 - p_c) / n_c + p_t * (1 - p_t) / n_t)
    ci = (p_t - p_c) + np.array([-1, 1]) * stats.norm.ppf(0.975) * se_diff
    return p_c, p_t, z, p_value, ci


def chart(p_c: float, p_t: float, ci: np.ndarray) -> None:
    os.makedirs(OUT, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(["Control", "Treatment"], [p_c, p_t],
                  color=["#a1a1aa", "#2ed573"])
    for b, v in zip(bars, [p_c, p_t]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.002, f"{v:.1%}",
                ha="center", fontweight="bold")
    ax.set_ylabel("Conversion rate")
    ax.set_title("A/B Test: Conversion by Group")
    ax.set_ylim(0, max(p_c, p_t) * 1.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUT, "ab_test_conversion.png")
    fig.savefig(path, dpi=110)
    plt.close(fig)
    print(f"saved {path}")


def main() -> None:
    rng = np.random.default_rng(SEED)
    control, treatment = simulate(rng)
    p_c, p_t, z, p_value, ci = two_proportion_z_test(control, treatment)

    abs_lift = p_t - p_c
    rel_lift = abs_lift / p_c
    alpha = 0.05

    print("=== A/B Test Results ===")
    print(f"Samples per group : {N_PER_GROUP:,}")
    print(f"Control conversion: {p_c:.3%}")
    print(f"Treatment         : {p_t:.3%}")
    print(f"Absolute lift     : {abs_lift:+.3%}")
    print(f"Relative lift     : {rel_lift:+.1%}")
    print(f"z-statistic       : {z:.3f}")
    print(f"p-value           : {p_value:.5f}")
    print(f"95% CI (diff)     : [{ci[0]:+.3%}, {ci[1]:+.3%}]")
    print()
    if p_value < alpha:
        print(f"Decision: REJECT H0 at alpha={alpha}. The treatment shows a "
              f"statistically significant lift. Ship it.")
    else:
        print(f"Decision: FAIL TO REJECT H0 at alpha={alpha}. No significant "
              f"difference detected.")

    chart(p_c, p_t, ci)


if __name__ == "__main__":
    main()
