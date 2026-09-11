"""Rebuild every generated dataset in this folder.

    python datasets/make_all.py

Every generator is seeded, so this reproduces byte-identical files. The real
datasets listed in README.md are downloaded, not generated — see download_real.py.
"""
import importlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for n in range(1, 17):
    importlib.import_module(f"make_session_{n:02d}").main()
print("\nAll generated datasets rebuilt.")
