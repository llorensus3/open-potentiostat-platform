#!/usr/bin/env python3
"""
fit_randles_eis.py

Fit a simple Randles circuit to EIS data.

Model:
    Z(ω) = Rs + 1 / (1/Rct + jωCdl)

Expected CSV columns:
- freq_hz
- zreal_ohm
- zimag_ohm

Outputs:
- fitted parameters JSON
- Nyquist comparison plot
"""

from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.optimize import least_squares
except Exception as exc:
    raise SystemExit("This script requires scipy. Install with: pip install scipy") from exc


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"freq_hz", "zreal_ohm", "zimag_ohm"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df.sort_values("freq_hz", ascending=False).reset_index(drop=True)


def randles_impedance(freq_hz, rs, rct, cdl):
    w = 2.0 * np.pi * np.asarray(freq_hz, dtype=float)
    jwcdl = 1j * w * cdl
    z_parallel = 1.0 / ((1.0 / rct) + jwcdl)
    return rs + z_parallel


def residuals(params, freq_hz, z_meas):
    rs, rct, cdl = params
    if rs <= 0 or rct <= 0 or cdl <= 0:
        return np.full(2 * len(freq_hz), 1e9)
    z_fit = randles_impedance(freq_hz, rs, rct, cdl)
    return np.concatenate([(z_fit.real - z_meas.real), (z_fit.imag - z_meas.imag)])


def fit_randles(df: pd.DataFrame):
    freq = df["freq_hz"].to_numpy(dtype=float)
    z_meas = df["zreal_ohm"].to_numpy(dtype=float) + 1j * df["zimag_ohm"].to_numpy(dtype=float)

    rs0 = float(df.loc[df["freq_hz"].idxmax(), "zreal_ohm"])
    rct0 = max(float(df["zreal_ohm"].max() - rs0), 1e-6)
    cdl0 = 1e-3

    result = least_squares(
        residuals,
        x0=np.array([rs0, rct0, cdl0], dtype=float),
        bounds=([1e-9, 1e-9, 1e-9], [1e6, 1e6, 10.0]),
        args=(freq, z_meas),
        max_nfev=5000,
    )

    rs, rct, cdl = result.x
    z_fit = randles_impedance(freq, rs, rct, cdl)

    ss_res = float(np.sum(np.abs(z_meas - z_fit) ** 2))
    ss_tot = float(np.sum(np.abs(z_meas - np.mean(z_meas)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    params = {
        "Rs_ohm": float(rs),
        "Rct_ohm": float(rct),
        "Cdl_F": float(cdl),
        "cost": float(result.cost),
        "r2_complex": float(r2),
        "success": bool(result.success),
        "message": str(result.message),
    }
    return params, z_fit


def plot_nyquist(df: pd.DataFrame, z_fit, out_png: Path):
    plt.figure()
    plt.plot(df["zreal_ohm"], -df["zimag_ohm"], "o", label="Measured")
    plt.plot(z_fit.real, -z_fit.imag, "-", label="Randles fit")
    plt.xlabel("Z' (ohm)")
    plt.ylabel("-Z'' (ohm)")
    plt.title("Randles Fit - Nyquist")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Fit Randles circuit to EIS data.")
    parser.add_argument("csv_file", help="Input CSV file")
    parser.add_argument("--plot", default="randles_fit_nyquist.png", help="Output PNG file")
    parser.add_argument("--json", default="randles_fit_results.json", help="Output JSON file")
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    df = load_csv(csv_path)
    params, z_fit = fit_randles(df)

    plot_nyquist(df, z_fit, Path(args.plot))
    Path(args.json).write_text(json.dumps(params, indent=2), encoding="utf-8")

    print(f"Loaded {len(df)} rows from {csv_path}")
    print(json.dumps(params, indent=2))
    print(f"Saved plot to {args.plot}")
    print(f"Saved fit parameters to {args.json}")


if __name__ == "__main__":
    main()
