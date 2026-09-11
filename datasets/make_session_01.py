"""Datasets for Session 1 — Introduction to Data Science.

Run:  python datasets/make_session_01.py
"""
import json
import numpy as np
import pandas as pd
from _common import rng, save, DATA


def main():
    print("Session 1:")

    # --- The same three orders in three different shapes ---------------------
    # Used to show structured / semi-structured / unstructured data.
    structured = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer": ["Alice", "Bob", "Chan"],
        "amount":   [250.0, 90.0, 410.0],
    })
    save(structured, "orders.csv")

    semi = [
        {"order_id": 1, "customer": "Alice", "amount": 250.0},
        {"order_id": 2, "customer": "Bob", "amount": 90.0, "gift_wrap": True},
        {"order_id": 3, "customer": "Chan", "amount": 410.0,
         "delivery": {"city": "Mumbai", "express": False}},
    ]
    save(json.dumps(semi, indent=1), "orders.json")

    save("Alice ordered two books on Tuesday and paid 250 rupees.\n"
         "Bob picked up a single notebook for 90; he asked for it gift wrapped.\n"
         "Chan spent four hundred and ten rupees on stationery, delivered to Mumbai.\n",
         "order_notes.txt")

    # --- Daily demand: wobbles randomly around a stable level ----------------
    r = rng(0)
    save(pd.DataFrame({
        "day": np.arange(1, 401),
        "units_sold": (100 + r.normal(0, 12, 400)).round(1),
    }), "daily_demand.csv")

    # --- Ten flats, one with an unrecorded size (the lifecycle demo) ---------
    flats = pd.DataFrame({
        "sqft":    [500, 750, 1000, 1200, 1500, 900, 1100, np.nan, 1300, 600],
        "age_yrs": [10, 5, 2, 8, 1, 15, 3, 6, 4, 20],
        "rent":    [9000, 14000, 20000, 21000, 28000, 15000, 21000, 16000, 25000, 10000],
    })
    save(flats, "flats.csv")

    # --- Film ratings, 0 means not watched (the recommendation demo) ---------
    ratings = pd.DataFrame(
        [[5, 4, 0, 5, 1],
         [4, 5, 1, 4, 1],
         [1, 0, 5, 1, 4],
         [5, 4, 1, 0, 2]],
        index=["Asha", "Brij", "Chan", "You"],
        columns=["Action1", "Action2", "Romance1", "Action3", "Romance2"],
    )
    ratings.index.name = "viewer"
    save(ratings, "film_ratings.csv", index=True)

    # --- 100 days of a noisy upward price trend ------------------------------
    r = rng(42)
    days = np.arange(1, 101)
    save(pd.DataFrame({
        "day": days,
        "price": (50 + days * 0.5 + r.normal(0, 5, 100)).round(2),
    }), "daily_price.csv")


if __name__ == "__main__":
    main()
