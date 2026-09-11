"""Datasets for Session 14 — Distributed Data Processing.

The three city_sales chunk files stand in for three machines each holding a
slice of one logical dataset — which is what HDFS blocks are.
"""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 14:")
    # --- Three lines of text: the word-count example, as a real .txt file --
    save("the cat sat\nthe cat ran\nthe dog ran\n", "word_count_lines.txt")

    # --- One logical table split across three files ------------------------
    chunks = [
        [("Mumbai", 250), ("Delhi", 100), ("Mumbai", 300)],
        [("Pune", 80), ("Delhi", 150), ("Mumbai", 120)],
        [("Pune", 200), ("Pune", 60), ("Delhi", 90)],
    ]
    for i, rows in enumerate(chunks, 1):
        save(pd.DataFrame(rows, columns=["city", "amount"]), f"chunks/city_sales_{i}.csv")

    # --- Three machines, each with thousands of rows for a few cities.
    #     Used to measure what a combiner saves on network traffic.
    heavy = [
        [("Mumbai", 1)] * 4_000 + [("Delhi", 1)] * 3_000,
        [("Mumbai", 1)] * 5_000 + [("Pune", 1)] * 2_000,
        [("Delhi", 1)] * 6_000 + [("Pune", 1)] * 1_000,
    ]
    for i, rows in enumerate(heavy, 1):
        save(pd.DataFrame(rows, columns=["city", "one"]), f"chunks/city_counts_{i}.csv")

    # --- 60,000 server log rows, one server much busier than the rest ------
    r = rng(81)
    n = 60_000
    servers = [f"10.0.0.{i}" for i in range(1, 7)]
    save(pd.DataFrame({
        "server": r.choice(servers, n, p=[.10, .10, .10, .10, .10, .50]),
        "status": r.choice([200, 404, 500, 503], n, p=[.90, .05, .03, .02]),
        "response_ms": r.gamma(2, 40, n).round(2),
    }), "server_logs.csv")

    # --- Ten values in two groups of very unequal size: the average trap ---
    save(pd.DataFrame({"group": ["A"]*9 + ["B"],
                       "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}),
         "uneven_groups.csv")


if __name__ == "__main__":
    main()
