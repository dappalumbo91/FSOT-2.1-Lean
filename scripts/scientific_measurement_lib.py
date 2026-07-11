"""Scientific measurement metadata — σ-equivalent, Δ, uncertainty bands for benchmarks."""

from __future__ import annotations

import math
from typing import Any

from fsot_precision_constants import MAX_MEDIAN_ERROR_PCT, MAX_SCALAR_ERROR_PCT

# Standard gates (repo-wide precision spine)
GREEN_MEDIAN_PCT = MAX_MEDIAN_ERROR_PCT
GREEN_SCALAR_PCT = MAX_SCALAR_ERROR_PCT
ASPIRATION_SCALAR_PCT = 0.5


def relative_error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def delta_value(computed: float, measured: float) -> float:
    """Δ = computed − measured (signed residual)."""
    return computed - measured


def sigma_equivalent(error_pct: float, reference_uncertainty_pct: float | None) -> float | None:
    """σ = |error| / σ_ref when literature uncertainty is known."""
    if reference_uncertainty_pct is None or reference_uncertainty_pct <= 0:
        return None
    return error_pct / reference_uncertainty_pct


def precision_tier(
    error_pct: float | None,
    *,
    median: bool = False,
    contested: bool = False,
) -> str:
    if error_pct is None:
        return "structural"
    if contested:
        return "contested"
    limit = GREEN_MEDIAN_PCT if median else GREEN_SCALAR_PCT
    if error_pct <= limit:
        return "green"
    if error_pct <= ASPIRATION_SCALAR_PCT:
        return "yellow"
    return "red"


def measurement_envelope(
    record: dict,
    *,
    reference_uncertainty_pct: float | None = None,
    contested: bool = False,
) -> dict[str, Any]:
    """Attach standard scientific metadata to one benchmark record."""
    computed = record.get("computed")
    measured = record.get("measured")
    err = record.get("error_pct")

    out: dict[str, Any] = {}
    try:
        comp_f = float(computed) if computed is not None else None
        meas_f = float(measured) if measured is not None else None
    except (TypeError, ValueError):
        comp_f = meas_f = None

    if err is None and comp_f is not None and meas_f is not None:
        err = relative_error_pct(comp_f, meas_f)
    try:
        err_f = float(err) if err is not None else None
    except (TypeError, ValueError):
        err_f = None

    if comp_f is not None and meas_f is not None:
        out["delta"] = round(delta_value(comp_f, meas_f), 8)
        out["delta_pct"] = round(relative_error_pct(comp_f, meas_f), 6)

    if err_f is not None:
        out["sigma_equivalent"] = (
            round(sigma_equivalent(err_f, reference_uncertainty_pct), 4)
            if reference_uncertainty_pct
            else None
        )
        out["precision_tier"] = precision_tier(err_f, contested=contested)
        out["within_green_gate"] = err_f <= GREEN_SCALAR_PCT
        out["within_aspiration_gate"] = err_f <= ASPIRATION_SCALAR_PCT

    if reference_uncertainty_pct is not None:
        out["reference_uncertainty_pct"] = reference_uncertainty_pct

    unit = record.get("unit")
    if unit:
        out["unit"] = unit

    return out


def domain_precision_summary(records: list[dict]) -> dict[str, Any]:
    """Aggregate σ/Δ stats for a domain benchmark."""
    scalar_errs: list[float] = []
    deltas: list[float] = []
    tiers: dict[str, int] = {}

    for r in records:
        env = r.get("scientific_measurement") or measurement_envelope(r)
        err = env.get("delta_pct") or r.get("error_pct")
        if err is None:
            continue
        try:
            ef = float(err)
        except (TypeError, ValueError):
            continue
        scalar_errs.append(ef)
        if env.get("delta") is not None:
            deltas.append(float(env["delta"]))
        tier = env.get("precision_tier") or precision_tier(ef)
        tiers[tier] = tiers.get(tier, 0) + 1

    if not scalar_errs:
        return {"scalar_count": 0}

    sorted_errs = sorted(scalar_errs)
    med = sorted_errs[len(sorted_errs) // 2]
    return {
        "scalar_count": len(scalar_errs),
        "median_error_pct": med,
        "max_error_pct": max(scalar_errs),
        "mean_abs_delta": (sum(abs(d) for d in deltas) / len(deltas)) if deltas else None,
        "precision_tier_counts": tiers,
        "green_gate_fraction": tiers.get("green", 0) / len(scalar_errs),
        "matches_domain_spine": med <= GREEN_MEDIAN_PCT and max(scalar_errs) <= GREEN_SCALAR_PCT,
    }