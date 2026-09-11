"""Datasets for Session 8 — Exploratory Data Analysis and Visualization."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 8:")
    # --- 500 homes in three cities with different price-per-sqft rates -----
    r = rng(21)
    n = 500
    area = r.normal(1_200, 350, n).clip(350, 3_000)
    age = r.integers(0, 40, n)
    city = r.choice(["Mumbai", "Pune", "Nagpur"], n, p=[.45, .35, .20])
    premium = pd.Series(city).map({"Mumbai": 1.9, "Pune": 1.0, "Nagpur": 0.6}).values
    price = (area * 3_500 * premium - age * 60_000 + r.normal(0, 300_000, n)).clip(500_000, None)
    homes = pd.DataFrame({
        "area_sqft": area.round(0),
        "age_years": age,
        "city": city,
        "bedrooms": np.clip((area / 450).round(), 1, 6).astype(int),
        "price": price.round(-3),
    })
    homes.loc[r.choice(n, 25, replace=False), "area_sqft"] = np.nan   # real files have gaps
    save(homes, "city_homes.csv")

    # --- Four relationships: strong, weak, curved, none --------------------
    r = rng(22)
    x = r.uniform(0, 10, 250)
    save(pd.DataFrame({
        "x": x.round(4),
        "strong_positive": (3*x + r.normal(0, 1.5, 250)).round(4),
        "weak_positive":   (3*x + r.normal(0, 14, 250)).round(4),
        "curved":          ((x - 5)**2 + r.normal(0, 1.5, 250)).round(4),
        "unrelated":       r.normal(15, 5, 250).round(4),
    }), "four_relationships.csv")

    # --- Temperature drives BOTH ice cream sales and drownings -------------
    r = rng(23)
    t = r.uniform(15, 42, 400)
    save(pd.DataFrame({
        "temperature_c": t.round(2),
        "ice_cream_sales": (t * 120 + r.normal(0, 300, 400)).round(0),
        "drownings": (t * 0.4 + r.normal(0, 2, 400)).round(2),
    }), "icecream_drownings.csv")

    # --- A perfectly monotonic but curved pair: Pearson vs Spearman --------
    x = np.arange(1, 51)
    save(pd.DataFrame({"x": x, "x_cubed": x ** 3}), "cubic_pair.csv")


if __name__ == "__main__":
    main()
