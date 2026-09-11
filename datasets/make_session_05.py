"""Datasets for Session 5 — Data Transformation."""
import numpy as np, pandas as pd
from _common import rng, save, DATA


def main():
    print("Session 5:")
    # --- Three people: A and B have similar incomes, A and C similar ages ---
    save(pd.DataFrame({"person": ["A", "B", "C"], "age": [25, 55, 26],
                       "income": [50_000, 51_000, 90_000]}), "three_people.csv")

    # --- The label depends on age AND income in equal measure. Unscaled,
    #     income's larger numbers dominate every distance calculation, so a
    #     distance-based model does badly until the columns are scaled.
    r = rng(0)
    n = 600
    age = r.normal(40, 12, n)
    income = r.normal(60_000, 25_000, n)
    score = (age - age.mean())/age.std() + (income - income.mean())/income.std()
    save(pd.DataFrame({"age": age.round(1), "income": income.round(0),
                       "high_value": (score > 0).astype(int)}), "customer_value.csv")

    # --- Six people, one of them a very high earner ------------------------
    save(pd.DataFrame({"age": [25, 32, 47, 51, 62, 29],
                       "income": [30_000, 42_000, 61_000, 58_000, 250_000, 35_000]}),
         "six_earners.csv")

    # --- Two documents with identical word proportions, different lengths --
    save(pd.DataFrame({"document": ["short", "long"], "data": [3, 30],
                       "model": [1, 10], "python": [0, 0]}), "word_counts.csv")

    # --- Exam marks, for the Binarizer pass/fail example -------------------
    save(pd.DataFrame({"student": list("ABCDE"), "mark": [35, 52, 67, 40, 88]}),
         "exam_marks.csv")

    # --- A strongly right-skewed income column -----------------------------
    r = rng(1)
    save(pd.DataFrame({"income": r.gamma(2, 20_000, 1_000).round(2)}), "skewed_incomes.csv")

    # --- Categories: one nominal (city), one ordinal (size), one target ----
    save(pd.DataFrame({"city": ["Mumbai", "Delhi", "Pune", "Mumbai", "Delhi"],
                       "size": ["small", "large", "medium", "medium", "small"],
                       "approved": ["yes", "no", "yes", "yes", "no"]}), "encoding_example.csv")

    # --- Rent where Mumbai is expensive and the other two are alike:
    #     there is no ordering, so label encoding must fail.
    r = rng(5)
    n = 300
    city = r.choice(["Delhi", "Mumbai", "Pune"], n)
    rent = np.where(city == "Mumbai", 40_000, 18_000) + r.normal(0, 2_000, n)
    save(pd.DataFrame({"city": city, "rent": rent.round(0)}), "city_rent.csv")

    # --- Small, skewed, three columns: the scaler-leakage experiment -------
    r = rng(3)
    X = r.lognormal(3, 1.1, size=(60, 3))
    y = X[:, 0] * 2 + X[:, 1] * 0.5 + r.normal(0, 1, 60)
    save(pd.DataFrame(X, columns=["f1", "f2", "f3"]).round(4).assign(target=y.round(4)),
         "lognormal_small.csv")

    # --- 60 rows, 200 columns of pure noise, target is a coin flip.
    #     Selecting features on all of it manufactures accuracy from nothing.
    r = rng(0)
    noise = pd.DataFrame(r.normal(size=(60, 200)).round(4),
                         columns=[f"n{i:03d}" for i in range(200)])
    noise["coin_flip"] = r.integers(0, 2, 60)
    save(noise, "pure_noise.csv")

    # --- A realistically imbalanced loan file. The catalog version is
    #     balanced 50/50, which is convenient for teaching but not what a
    #     lender's book looks like. Down-sample the approvals to about 8%,
    #     which is the range real default/approval rates live in, so that
    #     stratified splitting has something to protect.
    real = pd.read_csv(DATA / "loan_data_10k.csv")
    approved = real[real["loan_status"] == 1]
    refused = real[real["loan_status"] == 0]
    keep = int(len(refused) * 0.085 / (1 - 0.085))
    imbalanced = (pd.concat([refused, approved.sample(keep, random_state=0)])
                    .sample(frac=1, random_state=1).reset_index(drop=True))
    save(imbalanced, "loan_imbalanced.csv")

    # --- Loan applicants with gaps, for the pipeline demo ------------------
    r = rng(2)
    n = 400
    app = pd.DataFrame({
        "income": r.normal(60_000, 20_000, n).round(0),
        "age": r.integers(21, 65, n),
        "city": r.choice(["Mumbai", "Delhi", "Pune"], n),
        "approved": r.choice([0, 1], n, p=[.6, .4]),
    })
    app.loc[r.choice(n, 30, replace=False), "income"] = np.nan
    save(app, "loan_applicants.csv")


if __name__ == "__main__":
    main()
