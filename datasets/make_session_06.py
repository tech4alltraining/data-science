"""Datasets for Session 6 — Data Reduction and Discretization."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 6:")
    # --- 3 columns that matter and 190 that do not -------------------------
    r = rng(0)
    n = 200
    signal = r.normal(size=(n, 3))
    y = signal @ [4.0, -2.0, 1.0] + r.normal(0, 1, n)
    noise = r.normal(size=(n, 190))
    df = pd.DataFrame(np.hstack([signal, noise]).round(4),
                      columns=[f"real_{i}" for i in range(1, 4)] +
                              [f"noise_{i:03d}" for i in range(1, 191)])
    df["target"] = y.round(4)
    save(df, "signal_and_noise.csv")

    # --- House features: three real drivers, three junk columns ------------
    r = rng(1)
    n = 300
    X = pd.DataFrame({
        "area": r.normal(1200, 300, n).round(0),
        "bedrooms": r.integers(1, 6, n),
        "age": r.integers(0, 40, n),
        "noise_1": r.normal(size=n).round(4),
        "noise_2": r.normal(size=n).round(4),
        "noise_3": r.normal(size=n).round(4),
    })
    X["price"] = (30*X["area"] + 50_000*X["bedrooms"] - 8_000*X["age"]
                  + r.normal(0, 20_000, n)).round(0)
    save(X, "house_features.csv")

    # --- Height, arm span and leg length: three columns, one hidden fact ---
    r = rng(2)
    n = 200
    size = r.normal(0, 1, n)
    save(pd.DataFrame({
        "height_cm":   (170 + size*10 + r.normal(0, 1.5, n)).round(1),
        "arm_span_cm": (170 + size*10 + r.normal(0, 1.5, n)).round(1),
        "leg_len_cm":  (80 + size*5 + r.normal(0, 1.0, n)).round(1),
    }), "body_measurements.csv")

    # --- 12 survey questions generated from 4 underlying attitudes ---------
    r = rng(4)
    n = 400
    hidden = r.normal(size=(n, 4))
    loadings = r.normal(size=(4, 12))
    X = hidden @ loadings + r.normal(0, 0.35, size=(n, 12))
    save(pd.DataFrame(X.round(4), columns=[f"q{i:02d}" for i in range(1, 13)]),
         "survey_responses.csv")

    # --- Three columns on wildly different scales --------------------------
    r = rng(6)
    save(pd.DataFrame({"age_years": r.normal(40, 12, 300).round(1),
                       "income_rs": r.normal(60_000, 20_000, 300).round(0),
                       "rating": r.normal(3.5, 0.8, 300).round(2)}), "mixed_scales.csv")

    # --- 200,000 salaries, for the numerosity-reduction demo ---------------
    r = rng(7)
    save(pd.DataFrame({"salary": r.normal(50_000, 12_000, 200_000).round(0)}),
         "salaries_large.csv")

    # --- Six months of daily sales for three shops in two regions ----------
    r = rng(8)
    days = pd.date_range("2024-01-01", "2024-06-30", freq="D")
    save(pd.DataFrame({
        "date": np.repeat(days, 3).astype(str),
        "shop": np.tile(["Andheri", "Bandra", "Colaba"], len(days)),
        "region": np.tile(["West", "West", "South"], len(days)),
        "amount": r.integers(5_000, 40_000, len(days)*3),
    }), "shop_daily_sales.csv")

    # --- Survey ages: mostly young, a long tail of older respondents -------
    r = rng(9)
    save(pd.DataFrame({"age": np.concatenate([r.integers(18, 35, 70),
                                              r.integers(35, 80, 30)])}), "survey_ages.csv")

    # --- Insurance purchase rate by five-year age band ---------------------
    save(pd.DataFrame({
        "age_group": [f"{a}-{a+4}" for a in range(20, 70, 5)],
        "n": [50, 55, 60, 58, 52, 49, 45, 40, 38, 35],
        "bought_rate": [.05, .06, .05, .07, .20, .22, .21, .45, .47, .46],
    }), "insurance_by_age.csv")

    # --- Two shops declining while a new shop lifts the total --------------
    save(pd.DataFrame({"month": ["Jan", "Jan", "Feb", "Feb", "Feb"],
                       "shop": ["A", "B", "A", "B", "C"],
                       "sales": [100, 100, 90, 90, 120]}), "simpsons_shops.csv")


if __name__ == "__main__":
    main()
