"""Download the two large real-world datasets used by the advanced big-data demos
in Sessions 13 and 14.

    python datasets/download_bigdata_real.py

These files are NOT committed to git (see .gitignore) because they are large
(~120 MB together) and fully reproducible from this script. Both are public
Hugging Face datasets, fetched with a plain HTTPS GET — no account, API key or
extra library needed.

| File | Source | Rows | Used in |
|---|---|---|---|
| covertype.csv    | huggingface.co/datasets/inria-soda/tabular-benchmark | 566,602 | Session 13 |
| imdb_train.parquet | huggingface.co/datasets/stanfordnlp/imdb            | 25,000  | Session 14 |
"""
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent / "bigdata"
HERE.mkdir(exist_ok=True)

FILES = {
    "covertype.csv": (
        "https://huggingface.co/datasets/inria-soda/tabular-benchmark/"
        "resolve/main/clf_num/covertype.csv"
    ),
    "imdb_train.parquet": (
        "https://huggingface.co/datasets/stanfordnlp/imdb/"
        "resolve/main/plain_text/train-00000-of-00001.parquet"
    ),
}

for name, url in FILES.items():
    dest = HERE / name
    if dest.exists():
        print(f"  already have {name:<22} {dest.stat().st_size/1e6:>7.1f} MB")
        continue
    print(f"  downloading {name} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"    saved {name:<22} {dest.stat().st_size/1e6:>7.1f} MB")

print("\nDone. Read with pandas exactly as in Sessions 13 and 14:")
print('  pd.read_csv("datasets/bigdata/covertype.csv")')
print('  pd.read_parquet("datasets/bigdata/imdb_train.parquet")   # needs pyarrow')
