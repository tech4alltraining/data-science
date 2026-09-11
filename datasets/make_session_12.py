"""Datasets for Session 12 — Model Saving and Deployment.

The model is trained on datasets/house_prices_simple.csv; the portfolio is the
batch-scoring input; the monthly files show input drift after launch.
"""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 12:")
    # --- 500 houses, two features, for the deployable model --------------
    r = rng(61)
    n = 500
    area = r.normal(1_200, 350, n).clip(400, 3_000).round(0)
    age = r.integers(0, 40, n)
    price = (3_200*area - 45_000*age + 400_000 + r.normal(0, 200_000, n)).round(-3)
    save(pd.DataFrame({"area_sqft": area, "age_years": age, "price": price}),
         "house_prices_simple.csv")

    # --- Eight properties awaiting valuation: the batch-scoring input ----
    save(pd.DataFrame({
        "property_id": [f"P{i:04d}" for i in range(1, 9)],
        "area_sqft": [900, 1250, 1800, 640, 2200, 1500, 1050, 3000],
        "age_years": [12, 3, 25, 40, 1, 8, 18, 5],
    }), "property_portfolio.csv")

    # --- Three months of live inputs. By month 8 the customers changed. ---
    r = rng(62)
    frames = []
    for label, mean in [("Month 1", 1_200), ("Month 4", 1_260), ("Month 8", 1_700)]:
        frames.append(pd.DataFrame({"month": label,
                                    "area_sqft": r.normal(mean, 370, 300).round(0)}))
    save(pd.concat(frames, ignore_index=True), "incoming_requests.csv")


if __name__ == "__main__":
    main()
