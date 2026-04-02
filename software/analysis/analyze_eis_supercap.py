#!/usr/bin/env python3
"""
Analyze EIS data from a supercapacitor.

Expected CSV columns:
- freq_hz
- zreal_ohm
- zimag_ohm
"""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"freq_hz", "zreal_ohm", "zimag_ohm"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("--nyquist", default="eis_nyquist.png")
    parser.add_argument("--bode", default="eis_bode.png")
    args = parser.parse_args()

    path = Path(args.csv_file)
    df = load_csv(path)

    idx = df["freq_hz"].idxmax()
    esr = float(df.loc[idx, "zreal_ohm"])

    plt.figure()
    plt.plot(df["zreal_ohm"], -df["zimag_ohm"])
    plt.xlabel("Z' (ohm)")
    plt.ylabel("-Z'' (ohm)")
    plt.title("Nyquist Plot")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.nyquist, dpi=200)
    plt.close()

    zmag = np.sqrt(df["zreal_ohm"]**2 + df["zimag_ohm"]**2)
    plt.figure()
    plt.loglog(df["freq_hz"], zmag)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("|Z| (ohm)")
    plt.title("Bode Magnitude")
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(args.bode, dpi=200)
    plt.close()

    print(f"Loaded {len(df)} rows from {path}")
    print(f"Estimated ESR: {esr:.6e} ohm")
    print(f"Saved Nyquist plot to {args.nyquist}")
    print(f"Saved Bode plot to {args.bode}")

if __name__ == "__main__":
    main()
