#!/usr/bin/env python3
"""
Analyze galvanostatic charge/discharge data from a supercapacitor.

Expected CSV columns:
- time_s
- voltage_v
- current_a
"""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"time_s", "voltage_v", "current_a"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

def estimate_capacitance(df: pd.DataFrame):
    i = np.mean(np.abs(df["current_a"].to_numpy()))
    dt = float(df["time_s"].iloc[-1] - df["time_s"].iloc[0])
    dv = float(df["voltage_v"].iloc[0] - df["voltage_v"].iloc[-1])
    if dv == 0:
        raise ValueError("Voltage window is zero; cannot estimate capacitance.")
    return i * dt / abs(dv)

def estimate_esr(current_a: float, voltage_drop_v: float):
    if current_a == 0:
        raise ValueError("Current is zero; cannot estimate ESR.")
    return abs(voltage_drop_v / current_a)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("--output", default="gcd_supercap_plot.png")
    parser.add_argument("--voltage-drop", type=float, default=None, help="Instantaneous IR drop in volts")
    parser.add_argument("--current", type=float, default=None, help="Current used for ESR estimate in amperes")
    args = parser.parse_args()

    path = Path(args.csv_file)
    out_png = Path(args.output)
    df = load_csv(path)
    c_est = estimate_capacitance(df)

    plt.figure()
    plt.plot(df["time_s"], df["voltage_v"])
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Supercapacitor GCD")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

    print(f"Loaded {len(df)} rows from {path}")
    print(f"Estimated capacitance: {c_est:.6e} F")
    if args.voltage_drop is not None and args.current is not None:
        esr = estimate_esr(args.current, args.voltage_drop)
        print(f"Estimated ESR: {esr:.6e} ohm")
    print(f"Saved plot to {out_png}")

if __name__ == "__main__":
    main()
