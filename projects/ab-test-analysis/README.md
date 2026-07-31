# A/B Test Analysis

A complete frequentist analysis of an A/B experiment: *does a new landing page
increase conversion?* Built with **Python** (`numpy`, `scipy`).

## What it does
`ab_test.py` simulates a reproducible two-group experiment (12k users/group) and:
- computes conversion rates and **absolute / relative lift**,
- runs a **two-proportion z-test** (pooled SE) and reports the p-value,
- builds a **95% confidence interval** for the difference in rates,
- makes a ship / no-ship decision at α = 0.05,
- saves a conversion comparison chart to `./outputs`.

## Run it
```bash
pip install numpy scipy matplotlib
cd projects/ab-test-analysis
python ab_test.py
```

## Results (seed=7)
| Group     | Conversion |
|-----------|-----------|
| Control   | 12.18%    |
| Treatment | 13.29%    |

- Absolute lift **+1.11pp**, relative lift **+9.1%**.
- z = 2.58, **p = 0.010** → reject H₀ at α = 0.05.
- 95% CI for the difference: **[+0.27pp, +1.95pp]** (excludes 0).

**Interpretation:** the treatment produces a statistically significant conversion
lift; the entire confidence interval is positive, so it's safe to ship.

> Because the data is simulated from a known ground truth (control 11.8%,
> treatment 13.2%), you can change `CONTROL_RATE` / `TREATMENT_RATE` /
> `N_PER_GROUP` at the top of the script to explore power and false-positive
> behavior.
