"""FO-212 airfoil benchmark RMSE recompute (FO-210 scaffold + gas/similarity readout)."""

from __future__ import annotations

import json
import math
from pathlib import Path

from airfoil_fo212_eval import (
    C0_FSOT,
    D_EFF_FLUID,
    DELTA_PSI_FLUID,
    Z0_MRAGL,
    _row_arrays,
    predict_fo212,
)
from math_formula_eval import (
    core_context,
    evaluate_dataset_formula,
    evaluate_dataset_formula_split,
    load_csv_dataset,
    review_with_fsot_read,
    split_dataset_rows,
)

FO210_FORMULA = (
    "ln(1 + abs((((free_stream_velocity_ms / sqrt(abs(frequency_hz))) + p_new * "
    "(ln(abs(frequency_hz) + 1)) * (1 / (1 + 1000 * abs(suction_side_displacement_thickness_m)))) + "
    "((c_eff / pi) / phi) * (ln(abs(frequency_hz) + 1)) + (((c_eff / phi) + p_base) / "
    "(1 + (1000 * abs(suction_side_displacement_thickness_m)) / phi))) * (e^6 - e^4) / "
    "(1 + (k^7) * (1000 * abs(suction_side_displacement_thickness_m))))) * (e^2 + pi^2 + p_new)"
)
FO212_RULE_ID = "FO-212"
FO212_DESCRIPTION = (
    "FO-210 coherent ln-transport plus FSOT gas/similarity readout: "
    "St/phi, Re_theta, Mach*log(St), Air c0 log(f/c0), boundary-layer log(delta), golden AoA cos."
)
TARGET_COLUMN = "scaled_sound_pressure_level_db"
TRAIN_FRACTION = 0.8
SPLIT_SEED = 17
SOTA_HELD_OUT_RMSE = 5.412721340832612
GOLDEN_HELD_OUT_RMSE = 5.102551799768952
GOLDEN_FULL_RMSE = 5.061015749458651
LEGACY_FO210_HELD_OUT_RMSE = 5.907214506805364
LEGACY_FO210_FULL_RMSE = 5.961109363514883


def _metrics(actual: list[float] | object, pred: object) -> dict[str, float]:
    import numpy as np

    y = np.asarray(actual, dtype=float)
    p = np.asarray(pred, dtype=float)
    err = p - y
    rmse = float(math.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot <= 1e-15 else 1.0 - ss_res / ss_tot
    return {"rmse": rmse, "mae": mae, "r2": r2, "bias": float(np.mean(err))}


def evaluate_fo212_rows(rows: list[dict]) -> dict[str, float]:
    ctx = core_context()
    arr = _row_arrays(rows)
    pred = predict_fo212(arr, ctx, variant=FO212_RULE_ID)
    return _metrics(arr[TARGET_COLUMN], pred)


def evaluate_fo212_split(rows: list[dict]) -> dict:
    train, test = split_dataset_rows(rows, TRAIN_FRACTION, SPLIT_SEED, True)
    return {
        "train_metrics": evaluate_fo212_rows(train),
        "test_metrics": evaluate_fo212_rows(test),
        "train_row_count": len(train),
        "test_row_count": len(test),
    }


def _load_report_rmse(report_path: Path) -> float | None:
    if not report_path.exists():
        return None
    report = json.loads(report_path.read_text(encoding="utf-8"))
    sandbox = report.get("sandbox") or {}
    best = sandbox.get("best_formula") or {}
    metrics = best.get("test_metrics") or {}
    rmse = metrics.get("rmse")
    return float(rmse) if rmse is not None else None


def evaluate_airfoil(
    dataset_path: Path,
    *,
    report_path: Path | None = None,
    fsot_read_path: Path | None = None,
    rule_id: str = FO212_RULE_ID,
) -> dict:
    rows = load_csv_dataset(dataset_path)
    if rule_id == FO212_RULE_ID:
        full_metrics = evaluate_fo212_rows(rows)
        held_out = evaluate_fo212_split(rows)
        formula = FO212_DESCRIPTION
        golden_full = GOLDEN_FULL_RMSE
        golden_held = GOLDEN_HELD_OUT_RMSE
    else:
        full_metrics = evaluate_dataset_formula(rows, TARGET_COLUMN, FO210_FORMULA)
        held_out = evaluate_dataset_formula_split(
            rows,
            TARGET_COLUMN,
            FO210_FORMULA,
            TRAIN_FRACTION,
            SPLIT_SEED,
            True,
        )
        formula = FO210_FORMULA
        golden_full = LEGACY_FO210_FULL_RMSE
        golden_held = LEGACY_FO210_HELD_OUT_RMSE

    report_rmse = _load_report_rmse(report_path) if report_path else SOTA_HELD_OUT_RMSE
    fsot_review = None
    if fsot_read_path is not None and rule_id != FO212_RULE_ID:
        fsot_review = review_with_fsot_read(
            fsot_read_path,
            dataset_path,
            TARGET_COLUMN,
            FO210_FORMULA,
            TRAIN_FRACTION,
            SPLIT_SEED,
            True,
        )

    held_out_metrics = held_out["test_metrics"]
    sota_beat = float(held_out_metrics["rmse"]) < SOTA_HELD_OUT_RMSE

    return {
        "rule_id": rule_id,
        "formula": formula,
        "row_count": len(rows),
        "full_dataset_metrics": full_metrics,
        "held_out_metrics": held_out_metrics,
        "held_out_source": "python_split_fo212" if rule_id == FO212_RULE_ID else "python_split",
        "train_row_count": held_out["train_row_count"],
        "test_row_count": held_out["test_row_count"],
        "report_test_rmse": report_rmse,
        "sota_held_out_rmse": SOTA_HELD_OUT_RMSE,
        "sota_beat": sota_beat,
        "golden_full_rmse": golden_full,
        "golden_held_out_rmse": golden_held,
        "gas_medium": {
            "air_c0_m_s": C0_FSOT,
            "air_20c_z0_mrayl": Z0_MRAGL,
        },
        "domain": {
            "name": "Fluid_Dynamics",
            "d_eff": D_EFF_FLUID,
            "delta_psi": DELTA_PSI_FLUID,
        },
        "legacy_fo210": {
            "held_out_rmse": LEGACY_FO210_HELD_OUT_RMSE,
            "full_rmse": LEGACY_FO210_FULL_RMSE,
        },
        "fsot_read_review": fsot_review,
    }