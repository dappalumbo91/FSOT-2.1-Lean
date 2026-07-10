#!/usr/bin/env python3
"""One-off intrinsic airfoil formula search (zero free parameters)."""

from __future__ import annotations

import itertools
from pathlib import Path

from math_formula_eval import evaluate_dataset_formula_split, load_csv_dataset

ROOT = Path(__file__).resolve().parents[1]
GOAL = 5.412721340832612


def main() -> None:
    rows = load_csv_dataset(ROOT / "vendor/math_generator/datasets/airfoil_self_noise.csv")
    target = "scaled_sound_pressure_level_db"
    best: list[tuple[float, str]] = []

    scales = ["1", "10", "100", "1000", "10000", "phi", "pi", "pi*phi", "pi*phi*10"]
    for s1, s2, s3, s4, s5 in itertools.product(scales, repeat=5):
        f = (
            f"(p_new/{s1})*frequency_hz^2"
            f"+(c_eff/({s2}))*frequency_hz*free_stream_velocity_ms"
            f"+(p_base*{s3})*free_stream_velocity_ms*suction_side_displacement_thickness_m"
            f"+(a_in/{s4})*angle_of_attack_deg"
            f"+(b_in*{s5})*chord_length_m"
            f"+gamma*10"
        )
        try:
            r = evaluate_dataset_formula_split(rows, target, f, 0.8, 17, True)
            rmse = float(r["test_metrics"]["rmse"])
            if rmse < 6.0:
                best.append((rmse, f))
        except Exception:
            pass

    fo210 = (
        "ln(1 + abs((((free_stream_velocity_ms / sqrt(abs(frequency_hz))) + p_new * "
        "(ln(abs(frequency_hz) + 1)) * (1 / (1 + 1000 * abs(suction_side_displacement_thickness_m)))) + "
        "((c_eff / pi) / phi) * (ln(abs(frequency_hz) + 1)) + (((c_eff / phi) + p_base) / "
        "(1 + (1000 * abs(suction_side_displacement_thickness_m)) / phi))) * (e^6 - e^4) / "
        "(1 + (k^7) * (1000 * abs(suction_side_displacement_thickness_m))))) * (e^2 + pi^2 + p_new)"
    )
    for wrap in ["", "ln(1+abs(", "sqrt(abs("]:
        for close, mult in [("", 1), (")", 1), ("))", 1), (")", "*(e^2+pi^2+p_new)")]:
            if wrap:
                f = f"{wrap}{fo210}{close}{mult}"
            else:
                f = fo210
            try:
                r = evaluate_dataset_formula_split(rows, target, f, 0.8, 17, True)
                rmse = float(r["test_metrics"]["rmse"])
                best.append((rmse, f[:100]))
            except Exception:
                pass

    hybrid_terms = [
        "+angle_of_attack_deg*a_in/(pi*phi)+chord_length_m*p_base/(phi*sqrt(abs(frequency_hz)))",
        "+angle_of_attack_deg*free_stream_velocity_ms/(pi*phi*sqrt(abs(frequency_hz)))",
        "+chord_length_m*angle_of_attack_deg*p_base/(pi*phi)",
    ]
    for gate_pow in [5, 6, 7, 8]:
        for term in hybrid_terms:
            f = fo210.replace("k^7", f"k^{gate_pow}").replace(
                "free_stream_velocity_ms / sqrt(abs(frequency_hz)))",
                f"free_stream_velocity_ms / sqrt(abs(frequency_hz)){term})",
                1,
            )
            try:
                r = evaluate_dataset_formula_split(rows, target, f, 0.8, 17, True)
                rmse = float(r["test_metrics"]["rmse"])
                best.append((rmse, f[:120]))
            except Exception:
                pass

    best.sort(key=lambda x: x[0])
    print(f"Goal RMSE: {GOAL}")
    for rmse, snippet in best[:20]:
        flag = " *** BEAT GOAL" if rmse < GOAL else ""
        print(f"{rmse:.4f}{flag} | {snippet}")


if __name__ == "__main__":
    main()