"""Datasets for Session 3 — Data Cleaning.

Session 3 mostly reuses datasets/messy_customers.csv (Session 2) and the real
datasets/pre_data.csv. Only the sensor series is specific to this chapter.
"""
import numpy as np, pandas as pd
from _common import rng, save


def main():
    print("Session 3:")
    # --- A thermometer reading a real daily cycle, with noise on top --------
    r = rng(3)
    hours = np.arange(120)
    truth = 30 + 4 * np.sin(hours / 12)
    save(pd.DataFrame({
        "hour": hours,
        "sensor_reading": (truth + r.normal(0, 1.6, 120)).round(3),
        "true_temperature": truth.round(3),     # known only because we made it
    }), "sensor_readings.csv")


if __name__ == "__main__":
    main()
