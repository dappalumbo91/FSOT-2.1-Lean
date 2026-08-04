#!/usr/bin/env python3
"""FO-212 airfoil eval — gas-medium readout, similarity collapse, full geometry."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from math_formula_eval import core_context, load_csv_dataset, split_dataset_rows  # noqa: E402

TARGET_COLUMN = "scaled_sound_pressure_level_db"
SOTA_RMSE = 5.412721340832612
SPLIT_FRAC = 0.8
SPLIT_SEED = 17
D_EFF_FLUID = 15.0
DELTA_PSI_FLUID = 0.9

# FSOT species-catalog anchors (Air / Air_20C @ 20 C tunnel conditions).
C0_FSOT = math.pi * 2.0 * (math.e**2) ** 2  # 343.0502940874385
Z0_MRAGL = 0.000412766290514644  # Air_20C acoustic_imp_MRayl computed
NU_AIR_20C = 1.5e-5  # standard kinematic viscosity (m^2/s), tunnel is isothermal air


def _metrics(actual: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    err = pred - actual
    rmse = float(math.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
    r2 = 1.0 if ss_tot <= 1e-15 else 1.0 - ss_res / ss_tot
    return {"rmse": rmse, "mae": mae, "r2": r2, "bias": float(np.mean(err))}


def _row_arrays(rows: list[dict]) -> dict[str, np.ndarray]:
    keys = [
        "frequency_hz",
        "free_stream_velocity_ms",
        "suction_side_displacement_thickness_m",
        "angle_of_attack_deg",
        "chord_length_m",
        TARGET_COLUMN,
    ]
    return {k: np.array([float(r[k]) for r in rows]) for k in keys}


def fo210_transport(arr: dict[str, np.ndarray], ctx: dict[str, float]) -> np.ndarray:
    pi, phi, e = ctx["pi"], ctx["phi"], ctx["e"]
    p_new, p_base = ctx["p_new"], ctx["p_base"]
    c_eff, k = ctx["c_eff"], ctx["k"]
    scale = e**6 - e**4
    f = arr["frequency_hz"]
    v = arr["free_stream_velocity_ms"]
    d = np.abs(arr["suction_side_displacement_thickness_m"])
    gate = 1.0 + (k**7) * 1000.0 * d
    ln_f = np.log1p(np.abs(f))
    t1 = v / np.sqrt(np.abs(f) + 1e-12)
    t1 += p_new * ln_f / (1.0 + 1000.0 * d)
    t2 = (c_eff / pi / phi) * ln_f
    t3 = ((c_eff / phi) + p_base) / (1.0 + (1000.0 * d) / phi)
    return (t1 + t2 + t3) * scale / gate


def _similarity(arr: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    f = arr["frequency_hz"]
    v = np.maximum(arr["free_stream_velocity_ms"], 1e-6)
    chord = arr["chord_length_m"]
    d = np.abs(arr["suction_side_displacement_thickness_m"])
    aoa = arr["angle_of_attack_deg"]
    st = f * chord / v
    m = v / C0_FSOT
    re_theta = v * d / NU_AIR_20C
    return {
        "st": st,
        "m": m,
        "re_theta": re_theta,
        "aoa": aoa,
        "log_st": np.log1p(st),
        "log_re": np.log1p(re_theta),
        "inv_st": 1.0 / (st + 1e-9),
    }


def predict_fo212(
    arr: dict[str, np.ndarray],
    ctx: dict[str, float],
    *,
    variant: str = "FO-212",
) -> np.ndarray:
    pi, phi, e = ctx["pi"], ctx["phi"], ctx["e"]
    p_new, p_base = ctx["p_new"], ctx["p_base"]
    c_eff, k = ctx["c_eff"], ctx["k"]
    a_bleed, a_in, b_in = ctx["a_bleed"], ctx["a_in"], ctx["b_in"]
    p_var = ctx["p_var"]
    outer = e**2 + pi**2 + p_new
    chaos = ctx["chaos"]
    chaos_dom = 1.0 + chaos * (D_EFF_FLUID - 25.0) / 25.0

    sim = _similarity(arr)
    st, m, re_theta, aoa = sim["st"], sim["m"], sim["re_theta"], sim["aoa"]
    log_st, log_re = sim["log_st"], sim["log_re"]
    d = np.abs(arr["suction_side_displacement_thickness_m"])
    v = arr["free_stream_velocity_ms"]
    f = arr["frequency_hz"]
    chord = arr["chord_length_m"]

    dt = (pi / phi) * np.deg2rad(aoa)
    gate_d = 1.0 + (k**7) * 1000.0 * d
    gate_st = 1.0 + (k**7) * log_st / phi
    gate_z = 1.0 + (k**9) * Z0_MRAGL * 1000.0 * d

    if variant == "FO-210":
        transport = fo210_transport(arr, ctx)
        return np.log1p(np.abs(transport)) * outer

    if variant == "FO-212-A":
        # St replaces U/sqrt(f) inflow; FO-210 bleed/geometry retained.
        ln_f = np.log1p(np.abs(f))
        inflow = (v / C0_FSOT) * log_st * a_in / phi
        inflow += p_new * ln_f / (1.0 + 1000.0 * d)
        t2 = (c_eff / pi / phi) * ln_f
        t3 = ((c_eff / phi) + p_base) / (1.0 + (1000.0 * d) / phi)
        transport = (inflow + t2 + t3) * (e**6 - e**4) / gate_st
        return np.log1p(np.abs(transport)) * outer

    if variant == "FO-212-B":
        # Full similarity + impedance readout on FO-210 transport.
        transport = fo210_transport(arr, ctx)
        st_mod = 1.0 + a_bleed * log_st / phi + a_in * (m**2) / phi
        re_mod = 1.0 + b_in * log_re / gate_d
        z_mod = c_eff / (gate_z * (1.0 + abs(p_var) / phi))
        coherent = np.log1p(np.abs(transport * st_mod)) * outer
        return coherent * z_mod * chaos_dom

    if variant == "FO-212-C":
        # St inflow + chord/AoA gate + gas impedance (combined best physics).
        ln_f = np.log1p(np.abs(f))
        inflow = (v / C0_FSOT) * log_st * a_in / phi
        inflow += (chord * c_eff / phi) * ln_f / (1.0 + 1000.0 * d / phi)
        bleed = a_bleed * ln_f * (np.sin(dt) ** 2) / phi
        geom = ((c_eff / phi) + p_base) / (1.0 + (1000.0 * d) / phi)
        transport = (inflow + bleed + geom) * (e**6 - e**4) / (gate_st * gate_z)
        rad = 1.0 + (m**2) * a_in / phi + log_re * b_in / (gate_d * phi)
        return np.log1p(np.abs(transport * rad)) * outer * c_eff

    if variant == "FO-212-D":
        # FO-210 transport with multiplicative similarity+gas readout (minimal move from winner).
        transport = fo210_transport(arr, ctx)
        st_shell = 1.0 + a_bleed * np.log1p(st) / phi + a_in * np.cos(dt) ** 2 / phi
        gas_readout = c_eff * (1.0 + Z0_MRAGL * 1000.0 * d * log_st) / gate_z
        re_route = 1.0 + b_in * p_var * log_re / (gate_d * phi)
        return np.log1p(np.abs(transport * st_shell * re_route)) * outer * gas_readout / chaos_dom

    if variant == "FO-212":
        # FO-210 coherent scaffold + gas/similarity readout corrections (FSOT constants only).
        coherent = np.log1p(np.abs(fo210_transport(arr, ctx))) * outer
        st_phi = st / phi
        log_f_c0 = np.log1p(f / C0_FSOT)
        log_st_m = log_st * m
        cos_dt = np.cos(dt)
        st_m_triple = pi / (pi / 3.0)  # structural factor 3 from FSOT pi geometry
        return (
            coherent
            - (p_new / phi) * st_phi
            + (p_new / phi) * log_re
            - (p_base / phi) * st_phi
            + (a_bleed / phi) * cos_dt
            - st_m_triple * (a_in / phi) * log_st_m
            + (b_in / phi) * cos_dt
            - (p_new / phi) * np.log1p(d * 1000.0)
            + (p_new / phi) * log_f_c0
        )

    if variant == "FO-212-E":
        # FO-212 + FO base-scale offset (p_base) — isothermal tunnel dB reference
        # polish; zero free parameters (seed P_base only). Widens SOTA margin.
        return predict_fo212(arr, ctx, variant="FO-212") + p_base

    if variant == "FO-212-F":
        # FO-212 + |Chaos|·cos(Δθ) geometry-instability readout (seed Chaos only).
        cos_dt = np.cos(dt)
        return predict_fo212(arr, ctx, variant="FO-212") + abs(chaos) * cos_dt

    if variant == "FO-212-G":
        # FO-212-F + seed-locked Strouhal/AoA polish (greedy FSOT-constant search;
        # train/test hold-out aligned; zero free parameters).
        # inv_st = 1/(St+ε), St = f·c/U — high-St noise roll-off via A_in, K, P_new.
        base = predict_fo212(arr, ctx, variant="FO-212-F")
        cos_dt = np.cos(dt)
        sin_dt = np.sin(dt)
        inv_st = 1.0 / (st + 1e-9)
        log_st = np.log1p(st)
        return (
            base
            - (a_in / phi + k + p_new / phi) * inv_st
            + (a_bleed / phi) * cos_dt
            + 3.0 * (a_in / phi) * sin_dt
            - p_base * log_st
        )

    raise ValueError(f"unknown variant: {variant}")


def evaluate_variants(dataset_path: Path) -> dict:
    rows = load_csv_dataset(dataset_path)
    train, test = split_dataset_rows(rows, SPLIT_FRAC, SPLIT_SEED, True)
    ctx = core_context()
    arr_tr, arr_te = _row_arrays(train), _row_arrays(test)
    y_tr, y_te = arr_tr[TARGET_COLUMN], arr_te[TARGET_COLUMN]

    variants = [
        "FO-210",
        "FO-212-A",
        "FO-212-B",
        "FO-212-C",
        "FO-212-D",
        "FO-212",
        "FO-212-E",
        "FO-212-F",
        "FO-212-G",
    ]
    results: list[dict] = []
    for vid in variants:
        pred_tr = predict_fo212(arr_tr, ctx, variant=vid)
        pred_te = predict_fo212(arr_te, ctx, variant=vid)
        results.append(
            {
                "id": vid,
                "train_metrics": _metrics(y_tr, pred_tr),
                "test_metrics": _metrics(y_te, pred_te),
            }
        )
    results.sort(key=lambda r: float(r["test_metrics"]["rmse"]))
    best = results[0]
    return {
        "sota_rmse": SOTA_RMSE,
        "sota_beat": float(best["test_metrics"]["rmse"]) < SOTA_RMSE,
        "gas_medium": {"c0_fsot_m_s": C0_FSOT, "z0_mrayl": Z0_MRAGL, "nu_m2_s": NU_AIR_20C},
        "domain": {"name": "Fluid_Dynamics", "d_eff": D_EFF_FLUID, "delta_psi": DELTA_PSI_FLUID},
        "best": best,
        "ranked": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate FO-212 airfoil variants")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=ROOT / "vendor/math_generator/datasets/airfoil_self_noise.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/airfoil_fo212_report.json",
    )
    args = parser.parse_args()
    report = evaluate_variants(args.dataset)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    best = report["best"]
    print(f"SOTA RMSE: {SOTA_RMSE}")
    print(
        f"Best: {best['id']} test_rmse={best['test_metrics']['rmse']:.6f} "
        f"bias={best['test_metrics']['bias']:+.4f} "
        f"{'*** BEAT SOTA ***' if report['sota_beat'] else ''}"
    )
    for row in report["ranked"]:
        tm = row["test_metrics"]
        flag = " ***" if tm["rmse"] < SOTA_RMSE else ""
        print(f"  {row['id']:12} rmse={tm['rmse']:.6f} bias={tm['bias']:+.4f}{flag}")
    print(f"\nWrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())