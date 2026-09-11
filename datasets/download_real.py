"""Download the real datasets this course borrows from the course catalog.

    python datasets/download_real.py

Source: https://github.com/tech4alltraining/aiml/tree/main/datasets
These are real, publicly published files — they are not generated, and their
imperfections (missing values, duplicates, skew) are the reason they are used.
"""
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/tech4alltraining/aiml/main/datasets"
FILES = [
    "regression/salary_data.csv",
    "regression/cardekho_dataset.csv",
    "regression/advertising.csv",
    "classification/iris.csv",
    "classification/heart_failure_raw.csv",
    "clustering/Mall_Customers.csv",
    "prepreprocessing/pre_data.csv",
    "loan_data_10k.csv",
]

here = Path(__file__).resolve().parent
for rel in FILES:
    name = rel.split("/")[-1]
    urllib.request.urlretrieve(f"{BASE}/{rel}", here / name)
    print(f"  downloaded {name:<30} {(here/name).stat().st_size/1e3:>9.1f} KB")
print("\nDone.")
