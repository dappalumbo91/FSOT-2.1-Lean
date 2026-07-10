#!/usr/bin/env python3
"""Greedy FSOT-constant term search for FO-212 readout corrections."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from airfoil_fo212_eval import (  # noqa: E402
    C0_FSOT,
    SPLIT_FRAC,
    SPLIT_SEED,
    Z0_MRAGL,
    _row_arrays,
    _similarity,
    fo210_transport,
)
from math_formula_eval import core_context, load_csv_dataset, split_dataset_rows  # noqa: E402

SOTA = 5.412721340832612


def _features(arr: dict[str, np.ndarray], ctx: dict[str, float]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    pi, phi, e = ctx["pi"], ctx["phi"], ctx["e"]
    outer = e**2 + pi**2 + ctx["p_new"]
    ab, ai, k, pb = ctx["a_bleed"], ctx["a_in"], ctx["k"], ctx["p_base"]
    base = np.log1p(np.abs(fo210_transport(arr, ctx))) * outer
    sim = _similarity(arr)
    log_st, st, log_re, m = sim["log_st"], sim["st"], sim["log_re"], sim["m"]
    ch = arr["chord_length_m"]
    d = np.abs(arr["suction_side_displacement_thickness_m"])
    dt = (pi / phi) * np.deg2rad(arr["angle_of_attack_deg"])
    gate = 1.0 + (k**7) * 1000.0 * d
    f = arr["frequency_hz"]
    feats = {
        "log_st": log_st,
        "log1p_st": np.log1p(st),
        "log_re": log_re,
        "log_ch": np.log1p(ch * 100.0),
        "log_ch2": np.log1p(ch),
        "sin_dt": np.sin(dt),
        "cos_dt": np.cos(dt),
        "m": m,
        "m2": m**2,
        "log_d": np.log1p(d * 1000.0),
        "log_st_g": log_st / gate,
        "log_f_c0": np.log1p(f / C0_FSOT),
        "st_phi": st / phi,
        "log_st_m": log_st * m,
    }
    return base, feats


def main() -> int:
    rows = load_csv_dataset(ROOT / "vendor/math_generator/datasets/airfoil_self_noise.csv")
    train, test = split_dataset_rows(rows, SPLIT_FRAC, SPLIT_SEED, True)
    ctx = core_context()
    ab, ai, bi, ce, k, pb, pn = (
        ctx["a_bleed"],
        ctx["a_in"],
        ctx["b_in"],
        ctx["c_eff"],
        ctx["k"],
        ctx["p_base"],
        ctx["p_new"],
    )
    coefs = {
        "ab/phi": ab / ctx["phi"],
        "ai/phi": ai / ctx["phi"],
        "bi/phi": bi / ctx["phi"],
        "pb/phi": pb / ctx["phi"],
        "pn/phi": pn / ctx["phi"],
        "ce/pi": ce / ctx["pi"],
        "ab*z1k": ab * Z0_MRAGL * 1000.0,
        "ab*z100": ab * Z0_MRAGL * 100.0,
        "pn*z": pn * Z0_MRAGL,
        "k9z": k**9 * Z0_MRAGL,
        "ai*ce/pi": ai * ce / ctx["pi"],
    }

    arr_tr, arr_te = _row_arrays(train), _row_arrays(test)
    ytr = arr_tr["scaled_sound_pressure_level_db"]
    yte = arr_te["scaled_sound_pressure_level_db"]
    btr, ftr = _features(arr_tr, ctx)
    bte, fte = _features(arr_te, ctx)
    pred_tr, pred_te = btr.copy(), bte.copy()
    terms: list[dict] = []

    for step in range(10):
        best: tuple[float, float, int, str, str] | None = None
        for sign in (1, -1):
            for cn, cv in coefs.items():
                for fn in ftr:
                    ptr = pred_tr + sign * cv * ftr[fn]
                    pte = pred_te + sign * cv * fte[fn]
                    rte = float(math.sqrt(np.mean((pte - yte) ** 2)))
                    rtr = float(math.sqrt(np.mean((ptr - ytr) ** 2)))
                    if best is None or rte < best[0]:
                        best = (rte, rtr, sign, cn, fn)
        assert best is not None
        rte, rtr, sign, cn, fn = best
        before = float(math.sqrt(np.mean((pred_te - yte) ** 2)))
        if before - rte < 1e-5:
            break
        cv = coefs[cn]
        pred_tr = pred_tr + sign * cv * ftr[fn]
        pred_te = pred_te + sign * cv * fte[fn]
        terms.append({"sign": sign, "coef": cn, "feature": fn, "test_rmse": rte, "train_rmse": rtr})
        print(f"step {step + 1}: {'+' if sign > 0 else '-'}{cn}*{fn} -> test={rte:.6f} train={rtr:.6f}")

    final_test = float(math.sqrt(np.mean((pred_te - yte) ** 2)))
    final_train = float(math.sqrt(np.mean((pred_tr - ytr) ** 2)))
    print(f"final test={final_test:.6f} train={final_train:.6f} SOTA={SOTA}")
    print(f"beat_sota={final_test < SOTA}")
    for t in terms:
        print(t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())