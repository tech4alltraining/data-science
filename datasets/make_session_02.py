"""Datasets for Session 2 — Data Collection and Pre-Processing Overview."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 2:")
    # --- A town where income genuinely differs by neighbourhood --------------
    r = rng(7)
    save(pd.DataFrame({
        "area":   ["north"] * 600 + ["south"] * 400,
        "income": np.concatenate([r.normal(30_000, 5_000, 600),
                                  r.normal(85_000, 9_000, 400)]).round(0),
    }), "town_incomes.csv")

    # --- Eight ages, one of them typed as 225 instead of 27 ------------------
    save(pd.DataFrame({"respondent": list("ABCDEFGH"),
                       "age_clean": [25, 31, 28, 35, 22, 29, 33, 27],
                       "age_as_typed": [25, 31, 28, 35, 22, 29, 33, 225]}),
         "survey_ages_typo.csv")

    # --- A small sales table used through Part C ----------------------------
    save(pd.DataFrame({
        "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Mouse", "Laptop"],
        "city":    ["Mumbai", "Delhi", "Mumbai", "Pune", "Mumbai", "Delhi"],
        "units":   [3, 20, 12, 5, 15, 2],
        "price":   [55000, 500, 1500, 12000, 500, 55000],
    }), "shop_sales.csv")

    # --- The messy customer file used in Sessions 2 and 3 -------------------
    # Deliberately contains: a duplicate row, an impossible age, a negative age,
    # missing values, four spellings of two cities, and mixed date formats.
    messy = pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 3, 9],
        "name":   ["Asha ", "Brij", "Chan", "Devi", "Esha", "Faiz", "Gita", "Hari", "Chan", "Isha"],
        "age":    [25, 31, 28, np.nan, 22, 225, 29, 33, 28, -4],
        "city":   ["Mumbai", "mumbai", "Delhi", "Bombay", "Delhi", "MUM", "delhi", "Pune", "Delhi", "Pune"],
        "income": [50000, 62000, np.nan, 58000, 45000, 71000, 900000, 55000, np.nan, 61000],
        "joined": ["2024-01-05", "05/02/2024", "2024-03-11", "2024-04-02", "2024-05-19",
                   "2024-06-30", "2024-07-08", "2024-08-15", "2024-03-11", "2024-09-01"],
        "subscribed": ["Yes", "Y", "No", "N", "Yes", "yes", "No", "Y", "No", "Yes"],
    })
    save(messy, "messy_customers.csv")

    # --- A small inventory, as Excel, to show a third file format -----------
    save(pd.DataFrame({"product": ["Pen", "Notebook", "Bag", "Bottle", "Lamp"],
                       "price": [20, 60, 950, 350, 1200],
                       "stock": [500, 220, 40, 90, 15]}), "inventory.xlsx")


if __name__ == "__main__":
    main()
