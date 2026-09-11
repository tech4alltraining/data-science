"""Datasets for Session 4 — Data Integration."""
import numpy as np, pandas as pd
from _common import save


def main():
    print("Session 4:")
    # --- Two months of sales, same columns: a concat example ---------------
    save(pd.DataFrame({"date": ["2024-01-05", "2024-01-19"], "amount": [250, 90]}), "sales_jan.csv")
    save(pd.DataFrame({"date": ["2024-02-02", "2024-02-27"], "amount": [410, 130]}), "sales_feb.csv")
    # March uses a capital A — the mismatch concat will not warn you about.
    save(pd.DataFrame({"date": ["2024-03-01"], "Amount": [500]}), "sales_mar.csv")

    # --- Customers and purchases: one customer buys twice, one purchase is
    #     by a user who is not in the customer table at all.
    save(pd.DataFrame({"user_id": [1, 2, 3, 4],
                       "name": ["Alice", "Bob", "Chan", "Devi"],
                       "city": ["Mumbai", "Delhi", "Mumbai", "Pune"]}), "customers.csv")
    save(pd.DataFrame({"purchase_id": [101, 102, 103, 104],
                       "user_id": [1, 1, 3, 5],
                       "amount": [250.0, 120.0, 75.5, 300.0]}), "purchases.csv")

    # --- A lookup table with Mumbai listed twice: the silent row-multiplier -
    save(pd.DataFrame({"city": ["Mumbai", "Delhi", "Pune", "Mumbai"],
                       "region": ["West", "North", "West", "West"]}), "regions_dirty.csv")

    # --- Two subscriber lists whose keys differ only in case and whitespace -
    save(pd.DataFrame({"email": ["ASHA@mail.com", "brij@mail.com "],
                       "plan": ["gold", "silver"]}), "subscribers_plan.csv")
    save(pd.DataFrame({"email": ["asha@mail.com", "brij@mail.com"],
                       "spend": [900, 400]}), "subscribers_spend.csv")

    # --- The same customer key under a different column name ---------------
    save(pd.DataFrame({"cust_ref": [1, 2], "total": [500, 250]}), "orders_by_ref.csv")


if __name__ == "__main__":
    main()
