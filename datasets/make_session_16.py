"""Datasets for Session 16 — Capstone."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 16:")
    # --- A telecom churn file with the mess a real extract carries --------
    r = rng(101)
    n = 3_000
    df = pd.DataFrame({
        "customer_id": np.arange(1, n + 1),
        "tenure_months": r.integers(1, 72, n),
        "monthly_spend": r.gamma(4, 300, n).round(2),
        "support_calls": r.poisson(1.3, n),
        "city": r.choice(["Mumbai", "Delhi", "Pune", "Chennai"], n, p=[.35, .3, .2, .15]),
        "plan": r.choice(["basic", "standard", "premium"], n, p=[.45, .35, .20]),
    })
    # The truth: churn rises with support calls, falls with tenure,
    # and is higher on the basic plan.
    risk = (-2.4 + 0.42*df["support_calls"] - 0.030*df["tenure_months"]
            + 0.9*(df["plan"] == "basic"))
    df["churned"] = (r.random(n) < 1/(1 + np.exp(-risk))).astype(int)

    df.loc[r.choice(n, 120, replace=False), "monthly_spend"] = np.nan   # gaps
    df.loc[r.choice(n, 40, replace=False), "tenure_months"] = -1        # impossible
    df = pd.concat([df, df.sample(60, random_state=1)], ignore_index=True)  # duplicates
    save(df, "telecom_churn.csv")

    # --- Ten baskets, small enough to compute support and lift by hand ----
    small = ["bread butter jam", "bread butter", "bread butter jam milk", "milk eggs",
             "bread jam", "bread butter milk", "butter jam", "bread butter jam",
             "milk eggs bread", "bread butter jam"]
    save("\n".join(small) + "\n", "baskets_small.txt")

    # --- 4,000 baskets with three rules planted, so the algorithm can be
    #     checked against a truth we know.
    r = rng(102)
    products = ["bread", "butter", "jam", "milk", "eggs",
                "coffee", "sugar", "tea", "rice", "oil"]
    rows = []
    for i in range(4_000):
        basket = set(r.choice(products, r.integers(1, 4), replace=False))
        if "bread" in basket and r.random() < 0.80: basket.add("butter")
        if "butter" in basket and r.random() < 0.65: basket.add("jam")
        if "coffee" in basket and r.random() < 0.75: basket.add("sugar")
        rows.append({"basket_id": i + 1, "items": ",".join(sorted(basket))})
    save(pd.DataFrame(rows), "grocery_baskets.csv")


if __name__ == "__main__":
    main()
