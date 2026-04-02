#!/usr/bin/env python3
"""
Analyze CV data from a supercapacitor full cell.

Expected CSV columns:
- potential_v
- current_a
"""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"potential_v", "current_a"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

def estimate_capacitance(df: pd.DataFrame, scan_rate: float, dv_window=None):
    e = df["potential_v"].to_numpy()
    i = df["current_a"].to_numpy()
    area = np.trapz(np.abs(i), e)
    if dv_window is None:
        dv_window = float(np.max(e) - np.min(e))
    return area / (2.0 * scan_rate * dv_window)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("--scan-rate", type=float, required=True, help="Scan rate in V/s")
    parser.add_argument("--output", default="cv_supercap_plot.png")
    args = parser.parse_args()

    path = Path(args.csv_file)
    out_png = Path(args.output)
    df = load_csv(path)
    c_est = estimate_capacitance(df, args.scan_rate)

    plt.figure()
    plt.plot(df["potential_v"], df["current_a"])
    plt.xlabel("Potential (V)")
    plt.ylabel("Current (A)")
    plt.title("Supercapacitor CV")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

    print(f"Loaded {len(df)} rows from {path}")
    print(f"Estimated capacitance: {c_est:.6e} F")
    print(f"Saved plot to {out_png}")

if __name__ == "__main__":
    main()
