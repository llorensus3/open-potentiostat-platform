#!/usr/bin/env python3
"""
plot_cv.py

Simple script to load cyclic voltammetry data from CSV and generate:
1. Current vs potential
2. Potential vs time
3. Current vs time

Expected CSV columns:
- time_s
- potential_v
- current_a

Optional columns:
- cycle
- range
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required = {"time_s", "potential_v", "current_a"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return df.copy()


def make_plots(df: pd.DataFrame, outdir: Path, show: bool = False) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # Plot 1: I vs E (voltammogram)
    plt.figure()
    plt.plot(df["potential_v"], df["current_a"])
    plt.xlabel("Potential (V)")
    plt.ylabel("Current (A)")
    plt.title("Cyclic Voltammetry: I(E)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "cv_current_vs_potential.png", dpi=200)
    if show:
        plt.show()
    plt.close()

    # Plot 2: E vs t
    plt.figure()
    plt.plot(df["time_s"], df["potential_v"])
    plt.xlabel("Time (s)")
    plt.ylabel("Potential (V)")
    plt.title("Cyclic Voltammetry: E(t)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "cv_potential_vs_time.png", dpi=200)
    if show:
        plt.show()
    plt.close()

    # Plot 3: I vs t
    plt.figure()
    plt.plot(df["time_s"], df["current_a"])
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.title("Cyclic Voltammetry: I(t)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "cv_current_vs_time.png", dpi=200)
    if show:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot cyclic voltammetry data from CSV.")
    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument("--outdir", default="plots_cv", help="Output directory for figures")
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