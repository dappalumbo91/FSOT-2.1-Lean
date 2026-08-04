#!/usr/bin/env python3
"""FO-213 Higgs mass — SMILES Tier-18 intrinsic formula (MeV → GeV readout)."""

from __future__ import annotations

import math

from math_formula_eval import core_context, evaluate_formula

FO213_BASE_FORMULA = "(theta_s + e^3) / c_factor^7"
FO213_FORMULA = "((theta_s + e^3) / c_factor^7) * (1 + (poof * suction)^2)"
FO213_RULE_ID = "FO-213"
PLANCK_HIGGS_GEV = 125.25
# FO-213 base MeV * (1+(POOF·SUCTION)²) / 1000 → GeV golden (refreshed)
GOLDEN_MEV = 125263.77988177154
GOLDEN_GEV = GOLDEN_MEV / 1000.0
GOLDEN_ERROR_PCT = abs(GOLDEN_GEV - PLANCK_HIGGS_GEV) / PLANCK_HIGGS_GEV * 100.0


def evaluate_higgs_mass_mev() -> float:
    ctx = core_context()
    return float(evaluate_formula(FO213_FORMULA, ctx))


def evaluate_higgs_mass_gev() -> float:
    return evaluate_higgs_mass_mev() / 1000.0


def evaluate_higgs_mass() -> dict:
    mev = evaluate_higgs_mass_mev()
    gev = mev / 1000.0
    err = abs(gev - PLANCK_HIGGS_GEV) / PLANCK_HIGGS_GEV * 100.0
    return {
        "rule_id": FO213_RULE_ID,
        "formula": FO213_FORMULA,
        "base_formula": FO213_BASE_FORMULA,
        "computed_mev": mev,
        "computed_gev": gev,
        "measured_gev": PLANCK_HIGGS_GEV,
        "error_pct": err,
        "golden_mev": GOLDEN_MEV,
        "golden_gev": GOLDEN_GEV,
        "golden_error_pct": GOLDEN_ERROR_PCT,
    }