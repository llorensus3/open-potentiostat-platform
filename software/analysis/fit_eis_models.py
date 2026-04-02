#!/usr/bin/env python3
"""
fit_eis_models.py

Extended EIS fitting script with:
- Randles model
- Randles + Warburg model
- automatic report export
- comparison-ready JSON outputs

Expected CSV columns:
- freq_hz
- zreal_ohm
- zimag_ohm
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


def warburg_sigma(freq_hz, sigma):
    w = 2.0 * np.pi * np.asarray(freq_hz, dtype=float)
    return sigma * (1 - 1j) / np.sqrt(w)


def randles_warburg_impedance(freq_hz, rs, rct, cdl, sigma):
    return randles_impedance(freq_hz, rs, rct, cdl) + warburg_sigma(freq_hz, sigma)


def residuals_randles(params, freq_hz, z_meas):
    rs, rct, cdl = params
    if rs <= 0 or rct <= 0 or cdl <= 0:
        return np.full(2 * len(freq_hz), 1e9)
    z_fit = randles_impedance(freq_hz, rs, rct, cdl)
    return np.concatenate([(z_fit.real - z_meas.real), (z_fit.imag - z_meas.imag)])


def residuals_randles_w(params, freq_hz, z_meas):
    rs, rct, cdl, sigma = params
    if rs <= 0 or rct <= 0 or cdl <= 0 or sigma <= 0:
        return np.full(2 * len(freq_hz), 1e9)
    z_fit = randles_warburg_impedance(freq_hz, rs, rct, cdl, sigma)
    return np.concatenate([(z_fit.real - z_meas.real), (z_fit.imag - z_meas.imag)])


def compute_r2(z_meas, z_fit):
    ss_res = float(np.sum(np.abs(z_meas - z_fit) ** 2))
    ss_tot = float(np.sum(np.abs(z_meas - np.mean(z_meas)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def fit_randles(df):
    freq = df["freq_hz"].to_numpy(dtype=float)
    z_meas = df["zreal_ohm"].to_numpy(dtype=float) + 1j * df["zimag_ohm"].to_numpy(dtype=float)

    rs0 = float(df.loc[df["freq_hz"].idxmax(), "zreal_ohm"])
    rct0 = max(float(df["zreal_ohm"].max() - rs0), 1e-6)
    cdl0 = 1e-3

    result = least_squares(
        residuals_randles,
        x0=np.array([rs0, rct0, cdl0], dtype=float),
        bounds=([1e-9, 1e-9, 1e-9], [1e6, 1e6, 10.0]),
        args=(freq, z_meas),
        max_nfev=5000,
    )
    rs, rct, cdl = result.x
    z_fit = randles_impedance(freq, rs, rct, cdl)

    params = {
        "model": "Randles",
        "Rs_ohm": float(rs),
        "Rct_ohm": float(rct),
        "Cdl_F": float(cdl),
        "cost": float(result.cost),
        "r2_complex": float(compute_r2(z_meas, z_fit)),
        "success": bool(result.success),
        "message": str(result.message),
    }
    return params, z_fit


def fit_randles_warburg(df):
    freq = df["freq_hz"].to_numpy(dtype=float)
    z_meas = df["zreal_ohm"].to_numpy(dtype=float) + 1j * df["zimag_ohm"].to_numpy(dtype=float)

    rs0 = float(df.loc[df["freq_hz"].idxmax(), "zreal_ohm"])
    rct0 = max(float(df["zreal_ohm"].max() - rs0), 1e-6)
    cdl0 = 1e-3
    sigma0 = 1.0

    result = least_squares(
        residuals_randles_w,
        x0=np.array([rs0, rct0, cdl0, sigma0], dtype=float),
        bounds=([1e-9, 1e-9, 1e-9, 1e-9], [1e6, 1e6, 10.0, 1e6]),
        args=(freq, z_meas),
        max_nfev=8000,
    )
    rs, rct, cdl, sigma = result.x
    z_fit = randles_warburg_impedance(freq, rs, rct, cdl, sigma)

    params = {
        "model": "Randles+Warburg",
        "Rs_ohm": float(rs),
        "Rct_ohm": float(rct),
        "Cdl_F": float(cdl),
        "sigma_warburg": float(sigma),
        "cost": float(result.cost),
        "r2_complex": float(compute_r2(z_meas, z_fit)),
        "success": bool(result.success),
        "message": str(result.message),
    }
    return params, z_fit


def plot_comparison(df, z_fit_r, z_fit_rw, out_png):
    plt.figure()
    plt.plot(df["zreal_ohm"], -df["zimag_ohm"], "o", label="Measured")
    plt.plot(z_fit_r.real, -z_fit_r.imag, "-", label="Randles")
    plt.plot(z_fit_rw.real, -z_fit_rw.imag, "--", label="Randles + Warburg")
    plt.xlabel("Z' (ohm)")
    plt.ylabel("-Z'' (ohm)")
    plt.title("EIS Model Fit Comparison")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def write_report(df, params_r, params_rw, out_md):
    best = params_rw if params_rw["cost"] < params_r["cost"] else params_r
    text = f"""# EIS Fit Report

## Input data
- Points: {len(df)}
- Frequency range: {df["freq_hz"].max()} Hz to {df["freq_hz"].min()} Hz

## Model 1: Randles
- Rs = {params_r["Rs_ohm"]:.6e} ohm
- Rct = {params_r["Rct_ohm"]:.6e} ohm
- Cdl = {params_r["Cdl_F"]:.6e} F
- Cost = {params_r["cost"]:.6e}
- R² (complex) = {params_r["r2_complex"]:.6f}

## Model 2: Randles + Warburg
- Rs = {params_rw["Rs_ohm"]:.6e} ohm
- Rct = {params_rw["Rct_ohm"]:.6e} ohm
- Cdl = {params_rw["Cdl_F"]:.6e} F
- Sigma = {params_rw["sigma_warburg"]:.6e}
- Cost = {params_rw["cost"]:.6e}
- R² (complex) = {params_rw["r2_complex"]:.6f}

## Best model
**{best["model"]}**

Selected using the lowest least-squares cost.

## Interpretation hints
- Rs approximates the high-frequency intercept and is often associated with electrolyte / wiring resistance.
- Rct reflects charge-transfer resistance or effective interfacial resistance.
- Cdl reflects interfacial capacitive storage.
- Sigma (Warburg) approximates diffusion-related impedance contributions.

## Suggested next step
Use the same workflow on:
- Gamry reference data
- open potentiostat data

Then compare fitted parameters directly in a table or figure.
"""
    Path(out_md).write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Extended EIS fitting with Randles and Randles+Warburg models.")
    parser.add_argument("csv_file", help="Input CSV file")
    parser.add_argument("--plot", default="eis_model_comparison.png", help="Output PNG file")
    parser.add_argument("--json", default="eis_fit_results.json", help="Output JSON file")
    parser.add_argument("--report", default="eis_fit_report.md", help="Output Markdown report")
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    df = load_csv(csv_path)

    params_r, z_fit_r = fit_randles(df)
    params_rw, z_fit_rw = fit_randles_warburg(df)

    plot_comparison(df, z_fit_r, z_fit_rw, Path(args.plot))

    combined = {
        "randles": params_r,
        "randles_warburg": params_rw,
    }
    Path(args.json).write_text(json.dumps(combined, indent=2), encoding="utf-8")
    write_report(df, params_r, params_rw, Path(args.report))

    print(f"Loaded {len(df)} rows from {csv_path}")
    print(json.dumps(combined, indent=2))
    print(f"Saved comparison plot to {args.plot}")
    print(f"Saved JSON results to {args.json}")
    print(f"Saved Markdown report to {args.report}")


if __name__ == "__main__":
    main()
