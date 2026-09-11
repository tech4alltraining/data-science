"""Datasets for Session 15 — NoSQL Databases and Visualization at Scale."""
import json
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 15:")
    # --- A catalogue where three product types share almost no fields ------
    catalogue = [
        {"sku": "B-1", "name": "Data Science Handbook", "price": 899,
         "author": "R. Iyer", "pages": 412, "isbn": "978-1"},
        {"sku": "S-7", "name": "Cotton Shirt", "price": 1299,
         "size": "M", "colour": "blue", "material": "cotton"},
        {"sku": "L-9", "name": "UltraBook 14", "price": 74999,
         "ram_gb": 16, "cpu": "i7", "warranty_months": 24,
         "ports": ["USB-C", "HDMI"]},
    ]
    save(json.dumps(catalogue, indent=1), "product_catalog.json")

    # --- Sales as documents: one carries a field the others do not --------
    docs = [
        {"item": "laptop", "city": "Mumbai", "qty": 1, "price": 74999, "channel": "online"},
        {"item": "mouse", "city": "Mumbai", "qty": 4, "price": 499, "channel": "store"},
        {"item": "laptop", "city": "Delhi", "qty": 2, "price": 74999, "channel": "online",
         "loyalty_points": 300},
        {"item": "keyboard", "city": "Delhi", "qty": 3, "price": 1499, "channel": "store"},
        {"item": "mouse", "city": "Pune", "qty": 10, "price": 499, "channel": "online"},
    ]
    save(json.dumps(docs, indent=1), "store_sales.json")

    # --- 200,000 points in two clusters: a raw scatter hides the structure -
    r = rng(91)
    half = 100_000
    save(pd.DataFrame({
        "x": np.concatenate([r.normal(30, 6, half), r.normal(60, 9, half)]).round(3),
        "y": np.concatenate([r.normal(50, 9, half), r.normal(75, 11, half)]).round(3),
    }), "overplot_points.csv")

    # --- 300,000 request logs, for aggregate-before-you-plot ---------------
    r = rng(92)
    n = 300_000
    save(pd.DataFrame({
        "hour": r.integers(0, 24, n),
        "status": r.choice([200, 404, 500], n, p=[.93, .05, .02]),
        "response_ms": r.gamma(2, 40, n).round(2),
    }), "request_logs.csv")

    # --- Customers in signup order, with spend rising over time.
    #     head() is therefore a biased sample; sample() is not.
    r = rng(94)
    n = 200_000
    save(pd.DataFrame({
        "signup_order": np.arange(n),
        "spend": (np.linspace(200, 900, n) + r.normal(0, 40, n)).round(2),
    }), "customers_by_signup.csv")

    # --- A population to sample from, for the margin-of-error table -------
    save(pd.DataFrame({"value": rng(93).gamma(2, 40, 300_000).round(4)}),
         "sampling_population.csv")


if __name__ == "__main__":
    main()
