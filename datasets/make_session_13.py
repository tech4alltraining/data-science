"""Datasets for Session 13 — Big Data Analytics Fundamentals."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 13:")
    # --- 200,000 transactions: big enough to need chunking on a small box --
    r = rng(73)
    n = 200_000
    save(pd.DataFrame({
        "shop": r.integers(0, 50, n),
        "city": r.choice(["Mumbai", "Delhi", "Pune"], n),
        "amount": r.normal(500, 120, n).round(2),
        "ts": pd.date_range("2024-01-01", periods=n, freq="min").astype(str),
    }), "transactions.csv")

    # --- A year of monthly sales: North declining, South and West growing --
    r = rng(74)
    months = pd.date_range("2024-01-01", periods=12, freq="MS")
    rows = []
    for i, m in enumerate(months):
        for region in ["North", "South", "West"]:
            trend = {"North": -900, "South": 400, "West": 500}[region] * i
            base = {"North": 50_000, "South": 40_000, "West": 30_000}[region]
            rows.append({"month": m.date().isoformat(), "region": region,
                         "sales": round(base + trend + r.normal(0, 800), 2)})
    save(pd.DataFrame(rows), "regional_sales.csv")


if __name__ == "__main__":
    main()
