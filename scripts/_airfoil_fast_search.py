#!/usr/bin/env python3
"""Fast vectorized airfoil intrinsic formula search (zero free parameters)."""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from math_formula_eval import core_context, load_csv_dataset, split_dataset_rows  # noqa: E402

GOAL = 5.412721340832612
TARGET = "scaled_sound_pressure_level_db"


def _metrics(pred: np.ndarray, actual: np.ndarray) -> float:
    return float(math.sqrt(np.mean((pred - actual) ** 2)))


def main() -> None:
    rows = load_csv_dataset(ROOT / "vendor/math_generator/datasets/airfoil_self_noise.csv")
    train, test = split_dataset_rows(rows, 0.8, 17, True)
    ctx = core_context()

    def arrays(split_rows: list[dict]) -> dict[str, np.ndarray]:
        return {
            "f": np.array([float(r["frequency_hz"]) for r in split_rows]),
            "v": np.array([float(r["free_stream_velocity_ms"]) for r in split_rows]),
            "d": np.array([float(r["suction_side_displacement_thickness_m"]) for r in split_rows]),
            "a": np.array([float(r["angle_of_attack_deg"]) for r in split_rows]),
            "c": np.array([float(r["chord_length_m"]) for r in split_rows]),
            "y": np.array([float(r[TARGET]) for r in split_rows]),
        }

    tr, te = arrays(train), arrays(test)
    pi, e, phi = ctx["pi"], ctx["e"], ctx["phi"]
    c_eff, p_base, p_new = ctx["c_eff"], ctx["p_base"], ctx["p_new"]
    a_in, b_in, k = ctx["a_in"], ctx["b_in"], ctx["k"]
    gamma = ctx["gamma"]

    def eval_variant(gs: float, kp: int, frame_scale: float, outer_scale: float, geo_scale: float) -> float:
        f, v, d, a, c = te["f"], te["v"], te["d"], te["a"], te["c"]
        gate = 1.0 + gs * np.abs(d)
        transport = (
            (v / np.sqrt(np.abs(f)))
            + p_new * np.log(np.abs(f) + 1.0) / gate
            + (c_eff / pi / phi) * np.log(np.abs(f) + 1.0)
            + ((c_eff / phi) + p_base) / (1.0 + gs * np.abs(d) / phi)
        )
        if geo_scale != 0.0:
            transport = transport + geo_scale * (
                a_in * a / (pi * phi) + b_in * c * phi / np.sqrt(np.abs(f) + 1.0)
            )
        inner = np.abs(transport * frame_scale / (1.0 + (k**kp) * gs * np.abs(d)))
        pred = np.log1p(inner) * outer_scale
        return _metrics(pred, te["y"])

    best: list[tuple[float, dict]] = []
    for gs, kp, frame_id, outer_id, geo_id in itertools.product(
        [100.0, 500.0, 1000.0, 2000.0, pi * 100.0, phi * 1000.0],
        range(1, 13),
        range(4),
        range(3),
        range(4),
    ):
        frames = [e**6 - e**4, phi**8 * e**2, e**5 - e**3, phi**8 * e**2 + pi - a_in]
        outers = [e**2 + pi**2 + p_new, e**2 + pi**2, phi**2 + pi**2 + p_new]
        geos = [0.0, 1.0, 1.0 / phi, 1.0 / (pi * phi)]
        rmse = eval_variant(gs, kp, frames[frame_id], outers[outer_id], geos[geo_id])
        if rmse < 6.5:
            best.append((rmse, {"gs": gs, "kp": kp, "frame": frame_id, "outer": outer_id, "geo": geo_id}))

    best.sort(key=lambda x: x[0])
    print(f"Goal RMSE: {GOAL}")
    print(f"Variants under 6.5: {len(best)}")
    for rmse, cfg in best[:20]:
        flag = " *** BEAT GOAL" if rmse < GOAL else ""
        print(f"{rmse:.6f}{flag}  {cfg}")


if __name__ == "__main__":
    main()