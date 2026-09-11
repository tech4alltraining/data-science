"""Shared helpers for the dataset generators.

Every generator is seeded, so re-running any script reproduces byte-identical files.
"""
from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent


def rng(seed):
    return np.random.default_rng(seed)


def save(df, name, index=False):
    path = DATA / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name.endswith(".csv"):
        df.to_csv(path, index=index)
    elif name.endswith(".json"):
        path.write_text(df if isinstance(df, str) else df.to_json(orient="records", indent=1))
    elif name.endswith(".txt"):
        path.write_text(df)
    elif name.endswith(".xlsx"):
        df.to_excel(path, index=index)
    size = path.stat().st_size
    unit = f"{size/1e6:.1f} MB" if size > 1e6 else f"{size/1e3:.1f} KB"
    rows = len(df) if hasattr(df, "__len__") and not isinstance(df, str) else "-"
    print(f"  wrote {name:<42} {str(rows):>9} rows  {unit:>9}")
    return path
