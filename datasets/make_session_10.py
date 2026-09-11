"""Datasets for Session 10 — Unsupervised Learning and Clustering.

The customer segmentation demos use the real datasets/Mall_Customers.csv.
"""
import numpy as np, pandas as pd
from _common import rng, save
from sklearn.datasets import make_moons


def main():
    print("Session 10:")
    # --- Three well-separated blobs, for watching the centres settle -------
    r = rng(41)
    pts = np.vstack([r.normal([2, 2], .6, (60, 2)),
                     r.normal([7, 3], .6, (60, 2)),
                     r.normal([4, 7], .6, (60, 2))])
    save(pd.DataFrame(pts.round(4), columns=["x", "y"]), "three_blobs.csv")

    # --- Two interleaved crescents: K-Means cannot do this, DBSCAN can -----
    X, y = make_moons(n_samples=400, noise=0.06, random_state=0)
    save(pd.DataFrame({"x": X[:, 0].round(4), "y": X[:, 1].round(4), "true_group": y}),
         "moons.csv")

    # --- Pure noise. Clustering it still returns tidy-looking clusters -----
    save(pd.DataFrame(rng(7).normal(size=(400, 2)).round(4), columns=["x", "y"]),
         "random_noise.csv")


if __name__ == "__main__":
    main()
