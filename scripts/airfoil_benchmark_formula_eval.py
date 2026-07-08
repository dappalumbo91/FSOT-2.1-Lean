"""FO-210 airfoil benchmark_formula RMSE recompute."""

from __future__ import annotations

import json
from pathlib import Path

from math_formula_eval import (
    evaluate_dataset_formula,
    evaluate_dataset_formula_split,
    load_csv_dataset,
    review_with_fsot_read,
)

FO210_FORMULA = (
    "ln(1 + abs((((free_stream_velocity_ms / sqrt(abs(frequency_hz))) + p_new * "
    "(ln(abs(frequency_hz) + 1)) * (1 / (1 + 1000 * abs(suction_side_displacement_thickness_m)))) + "
    "((c_eff / pi) / phi) * (ln(abs(frequency_hz) + 1)) + (((c_eff / phi) + p_base) / "
    "(1 + (1000 * abs(suction_side_displacement_thickness_m)) / phi))) * (e^6 - e^4) / "
    "(1 + (k^9) * (1000 * abs(suction_side_displacement_thickness_m))))) * (e^2 + pi^2 + p_new)"
)
TARGET_COLUMN = "scaled_sound_pressure_level_db"
TRAIN_FRACTION = 0.8
SPLIT_SEED = 17
GOLDEN_HELD_OUT_RMSE = 6.247387360026391
GOLDEN_FULL_RMSE = 5.96094084765346


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
) -> dict:
    rows = load_csv_dataset(dataset_path)
    full_metrics = evaluate_dataset_formula(rows, TARGET_COLUMN, FO210_FORMULA)
    held_out = evaluate_dataset_formula_split(
        rows,
        TARGET_COLUMN,
        FO210_FORMULA,
        TRAIN_FRACTION,
        SPLIT_SEED,
        True,
    )
    report_rmse = _load_report_rmse(report_path) if report_path else GOLDEN_HELD_OUT_RMSE
    fsot_review = None
    if fsot_read_path is not None:
        fsot_review = review_with_fsot_read(
            fsot_read_path,
            dataset_path,
            TARGET_COLUMN,
            FO210_FORMULA,
            TRAIN_FRACTION,
            SPLIT_SEED,
            True,
        )
    held_out_source = "python_split"
    held_out_metrics = held_out["test_metrics"]
    if fsot_review and fsot_review.get("test_metrics"):
        held_out_metrics = fsot_review["test_metrics"]
        held_out_source = "fsot_read"

    return {
        "formula": FO210_FORMULA,
        "row_count": len(rows),
        "full_dataset_metrics": full_metrics,
        "held_out_metrics": held_out_metrics,
        "held_out_source": held_out_source,
        "train_row_count": held_out["train_row_count"],
        "test_row_count": held_out["test_row_count"],
        "report_test_rmse": report_rmse,
        "golden_full_rmse": GOLDEN_FULL_RMSE,
        "golden_held_out_rmse": GOLDEN_HELD_OUT_RMSE,
        "fsot_read_review": fsot_review,
    }