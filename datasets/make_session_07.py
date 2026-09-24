"""Datasets for Session 7 — Descriptive Statistics."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 7:")
    save(pd.DataFrame({"student": list("ABCDEFGH"),
                       "mark": [52, 61, 48, 61, 70, 55, 61, 39]}), "class_marks.csv")

    # Nine ordinary salaries and one founder
    save(pd.DataFrame({"employee": [f"E{i:02d}" for i in range(1, 11)],
                       "salary": [28_000, 31_000, 33_000, 35_000, 36_000,
                                  38_000, 40_000, 42_000, 45_000, 950_000]}),
         "team_salaries.csv")

    # Two suppliers with identical averages and very different spread
    save(pd.DataFrame({"week": [1, 2, 3, 4, 5, 6],
                       "steady": [48, 49, 50, 50, 51, 52],
                       "erratic": [10, 25, 50, 55, 85, 75]}), "supplier_deliveries.csv")

    # 200 incomes: 190 ordinary, 10 very high
    r = rng(11)
    save(pd.DataFrame({"income": np.concatenate([r.normal(45_000, 9_000, 190),
                                                 r.normal(280_000, 40_000, 10)]).round(0)}),
         "incomes_200.csv")

    # One student's marks against two very different class distributions
    save(pd.DataFrame({
        "maths":   [55, 62, 71, 78, 45, 59, 66, 70, 52, 68],
        "physics": [40, 45, 38, 65, 42, 39, 44, 41, 43, 46],
    }), "subject_marks.csv")

    # Three shapes: right-skewed, symmetric, left-skewed
    r = rng(12)
    save(pd.DataFrame({
        "income_right_skewed": r.gamma(2, 20_000, 3_000).round(1),
        "height_symmetric":    r.normal(165, 8, 3_000).round(2),
        "easy_exam_left_skewed": (100 - r.gamma(2, 6, 3_000)).round(2),
    }), "three_shapes.csv")

    # Daily returns: same mean and spread, different tail weight
    r = rng(13)
    normal = r.normal(0, 1, 20_000)
    heavy = r.standard_t(df=3, size=20_000)
    heavy = heavy / heavy.std()
    save(pd.DataFrame({"normal_tails": normal.round(5),
                       "heavy_tails": heavy.round(5)}), "daily_returns.csv")

    # Two age cohorts in one column: invisible at three bins, obvious at twelve
    r = rng(15)
    save(pd.DataFrame({"age": np.concatenate([r.normal(28, 4, 1_000),
                                              r.normal(52, 5, 1_000)]).round(1)}),
         "two_cohorts.csv")

    # 200 ages for the frequency-table demo
    r = rng(14)
    save(pd.DataFrame({"age": r.integers(18, 71, 200)}), "respondent_ages.csv")

    # Two exam classes, 30 students each, nearly the same average mark but very
    # different spread — the same idea as supplier_deliveries.csv, at a size
    # closer to a real classroom.
    r = rng(16)
    save(pd.DataFrame({"class_a": r.normal(70, 4, 30).round(0),
                       "class_b": r.normal(70, 16, 30).round(0)}),
         "exam_scores_two_classes.csv")


if __name__ == "__main__":
    main()
