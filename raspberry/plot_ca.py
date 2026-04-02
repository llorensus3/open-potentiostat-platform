#!/usr/bin/env python3
"""
plot_ca.py

Simple script to load chronoamperometry data from CSV and generate:
1. Current vs time
2. Current vs t^(-1/2)

Expected CSV columns:
- time_s
- current_a

Optional columns:
- voltage_v
- range
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required = {"time_s", "current_a"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df = df[df["time_s"] > 0].reset_index(drop=True)
    df["inv_sqrt_t"] = 1.0 / np.sqrt(df["time_s"])
    return df


def make_plots(df: pd.DataFrame, outdir: Path, show: bool = False) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # Plot 1: I(t)
    plt.figure()
    plt.plot(df["time_s"], df["current_a"])
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.title("Chronoamperometry: I(t)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "ca_current_vs_time.png", dpi=200)
    if show:
        plt.show()
    plt.close()

    # Plot 2: I vs t^(-1/2)
    plt.figure()
    plt.plot(df["inv_sqrt_t"], df["current_a"])
    plt.xlabel("t^(-1/2) (s^(-1/2))")
    plt.ylabel("Current (A)")
    plt.title("Cottrell Representation: I vs t^(-1/2)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "ca_current_vs_inv_sqrt_t.png", dpi=200)
    if show:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot chronoamperometry data from CSV.")
    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument("--outdir", default="plots_ca", help="Output directory for figures")
    parser.add_argument("--show", action="store_true", help="Display plots interactively")
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    outdir = Path(args.outdir)

    df = load_data(csv_path)
    make_plots(df, outdir, show=args.show)

    print(f"Loaded {len(df)} data points from {csv_path}")
    print(f"Saved plots to {outdir}")


if __name__ == "__main__":
    main()
