"""Datasets for Session 11 — Model Evaluation."""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 11:")
    # --- 40 points on a noisy straight line: enough to overfit badly ------
    r = rng(51)
    x = r.uniform(0, 10, 40)
    save(pd.DataFrame({"x": x.round(4), "y": (2 + 1.5*x + r.normal(0, 3, 40)).round(4)}),
         "noisy_line.csv")

    # --- Six independent samples from the SAME underlying truth -----------
    r = rng(52)
    frames = []
    for s in range(6):
        xs = r.uniform(0, 10, 30)
        frames.append(pd.DataFrame({"sample": s, "x": xs.round(4),
                                    "y": (2 + 1.5*xs + r.normal(0, 3, 30)).round(4)}))
    save(pd.concat(frames, ignore_index=True), "repeated_samples.csv")

    # --- Three features, a clean linear truth, moderate noise ------------
    r = rng(53)
    n = 120
    X = r.normal(size=(n, 3))
    y = X @ [3, -2, 1] + r.normal(0, 2.5, n)
    save(pd.DataFrame(X.round(4), columns=["f1", "f2", "f3"]).assign(target=y.round(4)),
         "three_features.csv")

    # --- Three residual pathologies: healthy, curved, fanning -------------
    r = rng(55)
    xs = r.uniform(1, 20, 300)
    save(pd.DataFrame({
        "x": xs.round(4),
        "healthy":       (3*xs + r.normal(0, 2, 300)).round(4),
        "curved":        (0.3*xs**2 + r.normal(0, 2, 300)).round(4),
        "growing_error": (3*xs + r.normal(0, 1, 300) * xs * .35).round(4),
    }), "residual_cases.csv")

    # --- Same model, two error distributions: normal vs heavy-tailed ------
    r = rng(56)
    n = 600
    X = r.normal(size=(n, 2))
    save(pd.DataFrame(X.round(4), columns=["f1", "f2"]).assign(
        target_normal=(X @ [3, -2] + r.normal(0, 1, n)).round(4),
        target_heavy=(X @ [3, -2] + r.standard_t(2.2, n)).round(4)), "error_shapes.csv")

    # --- A curved truth: linear underfits, a tree can learn it -----------
    r = rng(57)
    n = 600
    X = r.uniform(-3, 3, size=(n, 2))
    y = np.sin(X[:, 0]*2) * 4 + X[:, 1] + r.normal(0, .4, n)
    save(pd.DataFrame(X.round(4), columns=["f1", "f2"]).assign(target=y.round(4)),
         "curved_truth.csv")

    # --- A weak signal buried in noise: where peeking does most damage ----
    r = rng(77)
    n = 400
    X = r.normal(size=(n, 6))
    y = X[:, 0] * 1.2 + r.normal(0, 3.0, n)
    save(pd.DataFrame(X.round(4), columns=[f"f{i}" for i in range(1, 7)]).assign(
        target=y.round(4)), "weak_signal.csv")


if __name__ == "__main__":
    main()
