"""Datasets for Session 9 — Supervised Learning Techniques.

Simple regression uses the real datasets/salary_data.csv from the course catalog.
"""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 9:")
    # --- 400 houses. The truth: 3200/sqft, 250k/bedroom, -45k/year --------
    r = rng(32)
    n = 400
    area = r.normal(1_200, 350, n).clip(400, 2_800)
    bedrooms = np.clip((area / 450).round(), 1, 5)
    age = r.integers(0, 40, n)
    price = (3_200*area + 250_000*bedrooms - 45_000*age + 400_000
             + r.normal(0, 250_000, n))
    save(pd.DataFrame({"area_sqft": area.round(0), "bedrooms": bedrooms.astype(int),
                       "age_years": age, "price": price.round(-3)}), "house_prices.csv")

    # --- Fuel efficiency peaks in the middle: a straight line cannot fit ---
    r = rng(34)
    speed = r.uniform(20, 120, 300)
    save(pd.DataFrame({
        "speed_kmh": speed.round(2),
        "efficiency_kmpl": (25 - 0.004*(speed - 65)**2 + r.normal(0, 0.8, 300)).round(3),
    }), "fuel_efficiency.csv")

    # --- 40 employees: experience against salary, for the one-line fit ----
    r = rng(31)
    exp = r.uniform(0, 15, 40)
    save(pd.DataFrame({"experience_years": exp.round(2),
                       "salary": (25_000 + exp*9_000 + r.normal(0, 12_000, 40)).round(0)}),
         "experience_salary.csv")


    # --- Five predictions against five actuals: metrics computed by hand ----
    save(pd.DataFrame({"actual": [100, 200, 300, 400, 500],
                       "predicted": [110, 190, 310, 380, 520]}), "predictions_small.csv")

    # --- Two models with the SAME mean error and very different worst cases -
    actual = np.full(100, 500.0)
    spread = actual + 20.0                 # every prediction off by 20
    disaster = actual.copy(); disaster[0] += 2000   # 99 perfect, 1 catastrophic
    save(pd.DataFrame({"actual": actual, "model_a_spread_out": spread,
                       "model_b_one_disaster": disaster}), "two_error_patterns.csv")

    # --- Three residual pathologies, for the diagnostic plot ---------------
    r = rng(33)
    x = r.uniform(1, 20, 250)
    save(pd.DataFrame({
        "x": x.round(4),
        "healthy":        (3*x + r.normal(0, 2, 250)).round(4),
        "curved":         (0.35*x**2 + r.normal(0, 2, 250)).round(4),
        "fanning_out":    (3*x + r.normal(0, 1, 250) * x * 0.4).round(4),
    }), "residual_shapes.csv")


if __name__ == "__main__":
    main()
