#!/usr/bin/env python3
"""Symmetric trinary-string FO-211 airfoil eval: Strouhal (A), trinary fold (B), golden AoA (C)."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from math_formula_eval import (  # noqa: E402
    core_context,
    evaluate_dataset_formula_split,
    load_csv_dataset,
    split_dataset_rows,
)
from airfoil_benchmark_formula_eval import FO210_FORMULA, TARGET_COLUMN  # noqa: E402

GOAL = 5.412721340832612
SPLIT_FRAC = 0.8
SPLIT_SEED = 17


def _metrics(actual: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    err = pred - actual
    rmse = float(math.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
    r2 = 1.0 if ss_tot <= 1e-15 else 1.0 - ss_res / ss_tot
    return {"rmse": rmse, "mae": mae, "r2": r2}


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


def _trit(x: float, med: float) -> int:
    if x > med * 1.05:
        return 1
    if x < med * 0.95:
        return -1
    return 0


def delta_theta_a(f: np.ndarray, v: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Strouhal-symmetric phase: 2π f c / U."""
    return 2.0 * math.pi * f * c / np.maximum(v, 1e-6)


def delta_theta_b(
    f: np.ndarray, v: np.ndarray, d: np.ndarray, *, med_f: float, med_v: float, med_d: float
) -> np.ndarray:
    """Trinary fold: sum of trits maps to {-π/3, 0, π/3}."""
    out = np.zeros_like(f)
    for i in range(len(f)):
        t = _trit(float(f[i]), med_f) + _trit(float(v[i]), med_v) + _trit(float(d[i]), med_d)
        if t >= 2:
            out[i] = math.pi / 3.0
        elif t <= -2:
            out[i] = -math.pi / 3.0
        elif t == 1:
            out[i] = math.pi / 6.0
        elif t == -1:
            out[i] = -math.pi / 6.0
        else:
            out[i] = 0.0
    return out


def delta_theta_c(aoa: np.ndarray) -> np.ndarray:
    """Golden partition: (π/φ) scaled by angle of attack in radians."""
    return (math.pi / ((1.0 + math.sqrt(5.0)) / 2.0)) * np.deg2rad(aoa)


def _symmetric_predict(
    rows: list[dict],
    variant: str,
    *,
    readout: str,
    medians: dict[str, float] | None = None,
) -> np.ndarray:
    ctx = core_context()
    pi, phi = ctx["pi"], ctx["phi"]
    a_bleed, a_in, b_in = ctx["a_bleed"], ctx["a_in"], ctx["b_in"]
    c_eff, p_var = ctx["c_eff"], ctx["p_var"]
    p_new = ctx["p_new"]
    k = ctx["k"]
    outer = ctx["e"] ** 2 + pi**2 + p_new

    arr = _row_arrays(rows)
    f, v, d, aoa, chord = arr["frequency_hz"], arr["free_stream_velocity_ms"], arr[
        "suction_side_displacement_thickness_m"
    ], arr["angle_of_attack_deg"], arr["chord_length_m"]

    if variant == "A":
        dt = delta_theta_a(f, v, chord)
    elif variant == "B":
        if medians is None:
            raise ValueError("medians required for variant B")
        dt = delta_theta_b(f, v, d, med_f=medians["f"], med_v=medians["v"], med_d=medians["d"])
    elif variant == "C":
        dt = delta_theta_c(aoa)
    else:
        raise ValueError(variant)

    sin2 = np.sin(dt) ** 2
    cos2 = np.cos(dt) ** 2
    gate = 1.0 + (k**7) * 1000.0 * np.abs(d)

    # T1 inflow string — transport × cos²(Δθ)
    t1 = (v / np.sqrt(np.abs(f) + 1e-12)) * a_in * cos2
    # T2 geometry string — chord × c_eff with boundary moderation
    t2 = chord * c_eff / phi * (1.0 / (1.0 + 1000.0 * np.abs(d) / phi))
    # T3 bleed string — frequency × sin²(Δθ)
    t3 = np.log(np.abs(f) + 1.0) * a_bleed * sin2

    # Symmetric b2 shell (unity + coupled bleed/inflow partition)
    b2 = 1.0 + a_bleed * sin2 / phi + a_in * cos2 / phi
    # Superposition moderator b3
    b3 = 1.0 + b_in * p_var / gate

    if readout == "additive":
        core = t1 + t2 + t3
    elif readout == "multiplicative":
        core = t1 * t2 * t3
    elif readout == "balanced_additive_b2":
        core = (t1 + t2 + t3) * b2
    elif readout == "full_scalar_term3":
        core = (t1 + t2 + t3) * b2 * b3
    else:
        raise ValueError(readout)

    return np.log1p(np.abs(core)) * outer


def evaluate_variants(dataset_path: Path) -> dict:
    rows = load_csv_dataset(dataset_path)
    train, test = split_dataset_rows(rows, SPLIT_FRAC, SPLIT_SEED, True)
    arr_train = _row_arrays(train)
    medians = {
        "f": float(np.median(arr_train["frequency_hz"])),
        "v": float(np.median(arr_train["free_stream_velocity_ms"])),
        "d": float(np.median(arr_train["suction_side_displacement_thickness_m"])),
    }

    readouts = ["additive", "multiplicative", "balanced_additive_b2", "full_scalar_term3"]
    variants = ["A", "B", "C"]
    results: list[dict] = []

    y_test = _row_arrays(test)[TARGET_COLUMN]
    y_train = arr_train[TARGET_COLUMN]

    # FO-210 baseline via formula parser
    fo210 = evaluate_dataset_formula_split(
        rows, TARGET_COLUMN, FO210_FORMULA, SPLIT_FRAC, SPLIT_SEED, True
    )
    results.append(
        {
            "id": "FO-210",
            "variant": "baseline",
            "readout": "collapsed_ln_transport",
            "train_metrics": fo210["train_metrics"],
            "test_metrics": fo210["test_metrics"],
        }
    )

    for variant in variants:
        for readout in readouts:
            pred_tr = _symmetric_predict(train, variant, readout=readout, medians=medians)
            pred_te = _symmetric_predict(test, variant, readout=readout, medians=medians)
            entry = {
                "id": f"FO-211-{variant}",
                "variant": variant,
                "readout": readout,
                "train_metrics": _metrics(y_train, pred_tr),
                "test_metrics": _metrics(y_test, pred_te),
                "delta_theta": {
                    "A": "2*pi*f*chord/U",
                    "B": "trinary_fold(f,U,δ)->{-π/3,0,π/3}",
                    "C": "(pi/phi)*deg2rad(angle_of_attack_deg)",
                }[variant],
            }
            results.append(entry)

    results.sort(key=lambda r: float(r["test_metrics"]["rmse"]))
    best = results[0]
    return {
        "goal_rmse": GOAL,
        "goal_hit": float(best["test_metrics"]["rmse"]) < GOAL,
        "best": best,
        "ranked": results,
        "medians_for_B": medians,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate symmetric trinary airfoil variants")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=ROOT / "vendor/math_generator/datasets/airfoil_self_noise.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/airfoil_symmetric_trinary_report.json",
    )
    args = parser.parse_args()
    report = evaluate_variants(args.dataset)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    best = report["best"]
    print(f"Goal RMSE: {GOAL}")
    print(
        f"Best: {best['id']} readout={best.get('readout')} "
        f"test_rmse={best['test_metrics']['rmse']:.6f} "
        f"{'*** BEAT GOAL ***' if report['goal_hit'] else ''}"
    )
    print("\nTop 8:")
    for row in report["ranked"][:8]:
        tm = row["test_metrics"]["rmse"]
        flag = " ***" if tm < GOAL else ""
        print(
            f"  {row['id']:10} {row.get('readout',''):22} "
            f"rmse={tm:.6f}{flag}  ({row.get('variant','')})"
        )
    print(f"\nWrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())