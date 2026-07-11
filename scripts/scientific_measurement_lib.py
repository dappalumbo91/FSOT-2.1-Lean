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


def _decimals_from_float(value: float) -> int:
    """Best-effort inference of published decimal places from a float anchor."""
    if value == 0:
        return 0
    tol = max(1e-12, abs(value) * 1e-12)
    for decimals in range(6, -1, -1):
        if abs(value - round(value, decimals)) <= tol:
            return decimals
    return 6


def display_precision_decimals(measured: float, record: dict | None = None) -> int:
    """
    Decimal places implied by the literature anchor.

    Prefers explicit uncertainty metadata, else infers from the stored float
    (e.g. 67.4 → 1 dp, 104.0 → 1 dp, 0.811 → 3 dp).
    """
    row = record or {}
    explicit = row.get("measured_display_decimals")
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            pass

    target = row.get("target_value")
    if target is not None:
        text = str(target).strip()
        if "." in text:
            frac = text.split(".", 1)[1].rstrip("0")
            return len(frac) if frac else 0
        return 0

    return _decimals_from_float(float(measured))


def half_unit_tolerance(measured: float, decimals: int) -> float:
    """± half of the least significant published digit (scientific rounding slack)."""
    if decimals <= 0:
        return 0.5
    return 0.5 * (10.0 ** (-decimals))


def is_catalog_crosswalk_record(record: dict) -> bool:
    """Internal catalog alignment — not a literature observable comparison."""
    if record.get("lab") == "materials_species_bridge" or record.get("species_property"):
        return True
    prop = str(record.get("property") or "")
    return prop in {"biology_strict_operon_replication", "coding_bp_sum_bridge"}


def is_adversarial_match_record(record: dict) -> bool:
    """Adversarial harness rows — pass/fail on hole detection, not scalar error."""
    if record.get("expected_holes") is not None and record.get("match") is not None:
        return True
    prop = str(record.get("property") or "")
    return prop == "adversarial_hole_detected"


def is_literature_monitor_record(record: dict) -> bool:
    """Literature anchor rows — coverage monitoring, not FSOT scalar predictions."""
    ek = str(record.get("eval_kind") or "").lower()
    if ek in {"anomaly_anchor", "literature_monitor", "panel_bridge", "reference_gate", "count_anchor"}:
        return True
    return str(record.get("comparison_class") or "") == "literature_monitor"


def is_structural_gate_record(record: dict) -> bool:
    """Certificate / gate rows — binary readiness, not literature scalars."""
    if is_literature_monitor_record(record):
        return True
    ek = str(record.get("eval_kind") or "").lower()
    if ek in {"certificate_gate", "h0_gate", "crosswalk_bridge", "dark_sector_anchor"}:
        return True
    prop = str(record.get("property") or "")
    return prop.endswith("_ready") or prop.endswith("_gate")


def literature_aware_error_pct(
    computed: float,
    measured: float,
    record: dict | None = None,
) -> dict[str, Any]:
    """
    Compare FSOT prediction to literature the way experimentalists do:

    1. If σ or relative uncertainty is known → pass when |Δ| is inside the band.
    2. Else if the anchor is a rounded tabulated value → pass within ±½ LSD.
    3. Else fall back to raw relative error.
    """
    row = record or {}
    raw = relative_error_pct(computed, measured)
    delta = computed - measured

    if is_adversarial_match_record(row):
        matched = bool(row.get("match"))
        return {
            "raw_error_pct": raw,
            "effective_error_pct": 0.0 if matched else 100.0,
            "delta": delta,
            "comparison_kind": "adversarial_match",
            "within_display_precision": matched,
            "within_literature_band": matched,
        }

    if is_structural_gate_record(row):
        return {
            "raw_error_pct": raw,
            "effective_error_pct": raw,
            "delta": delta,
            "comparison_kind": "structural_gate",
            "within_display_precision": raw <= GREEN_SCALAR_PCT,
            "within_literature_band": raw <= GREEN_SCALAR_PCT,
        }

    if is_catalog_crosswalk_record(row):
        return {
            "raw_error_pct": raw,
            "effective_error_pct": raw,
            "delta": delta,
            "comparison_kind": "catalog_crosswalk",
            "within_display_precision": False,
            "within_literature_band": False,
        }

    if str(row.get("eval_kind") or "").lower() in {"preregistered_falsifiable", "wa_preregistered"}:
        sigma = row.get("sigma")
        sigma_dist = row.get("sigma_distance")
        if sigma is not None and sigma_dist is not None:
            try:
                z = float(sigma_dist)
                eff = min(z, 3.0) * 0.05
                within = z <= 2.0
                return {
                    "raw_error_pct": raw,
                    "effective_error_pct": eff,
                    "delta": delta,
                    "comparison_kind": "preregistered_falsifiable",
                    "sigma_distance": z,
                    "within_display_precision": False,
                    "within_literature_band": within,
                }
            except (TypeError, ValueError):
                pass

    # σ-distance observables store error_pct in σ-scaled units, not relative %.
    if row.get("sigma_distance") is not None and row.get("sigma") is not None:
        try:
            sigma_eff = float(row.get("error_pct") or raw)
        except (TypeError, ValueError):
            sigma_eff = raw
        return {
            "raw_error_pct": raw,
            "effective_error_pct": sigma_eff,
            "delta": delta,
            "comparison_kind": "sigma_distance",
            "sigma_distance": float(row["sigma_distance"]),
            "within_display_precision": False,
            "within_literature_band": float(row["sigma_distance"]) <= 2.0,
        }

    from literature_uncertainty_lib import resolve_reference_uncertainty_pct  # noqa: WPS433

    unc_pct = resolve_reference_uncertainty_pct(row)
    if unc_pct is None and row.get("reference_uncertainty_pct") is not None:
        try:
            unc_pct = float(row["reference_uncertainty_pct"])
        except (TypeError, ValueError):
            unc_pct = None
    if unc_pct is None and row.get("measured_uncertainty_rel") is not None:
        try:
            unc_pct = float(row["measured_uncertainty_rel"]) * 100.0
        except (TypeError, ValueError):
            unc_pct = None
    if unc_pct is None and row.get("measured_uncertainty") is not None and measured != 0:
        try:
            unc_pct = abs(float(row["measured_uncertainty"]) / float(measured)) * 100.0
        except (TypeError, ValueError):
            unc_pct = None

    if unc_pct is not None and unc_pct > 0:
        within = raw <= float(unc_pct)
        return {
            "raw_error_pct": raw,
            "effective_error_pct": 0.0 if within else raw,
            "delta": delta,
            "comparison_kind": "uncertainty_band",
            "reference_uncertainty_pct": float(unc_pct),
            "within_display_precision": False,
            "within_literature_band": within,
        }

    decimals = display_precision_decimals(measured, row)
    band = half_unit_tolerance(measured, decimals)
    within = abs(delta) <= band + max(1e-12, abs(measured) * 1e-12)
    return {
        "raw_error_pct": raw,
        "effective_error_pct": 0.0 if within else raw,
        "delta": delta,
        "comparison_kind": "display_precision",
        "display_decimals": decimals,
        "half_unit_band": band,
        "within_display_precision": within,
        "within_literature_band": within,
    }


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
    from literature_uncertainty_lib import (  # noqa: WPS433
        is_contested_record,
        literature_metadata_for_record,
        resolve_reference_uncertainty_pct,
    )

    lit = literature_metadata_for_record(record)
    if reference_uncertainty_pct is None:
        reference_uncertainty_pct = resolve_reference_uncertainty_pct(record)
    if not contested:
        contested = is_contested_record(record) or bool(lit.get("contested"))

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
        aware = literature_aware_error_pct(comp_f, meas_f, record)
        out["delta_pct"] = round(float(aware.get("raw_error_pct") or relative_error_pct(comp_f, meas_f)), 6)
        out["effective_error_pct"] = round(float(aware.get("effective_error_pct") or out["delta_pct"]), 6)
        out["comparison_kind"] = aware.get("comparison_kind")
        out["within_literature_band"] = bool(
            aware.get("within_literature_band") or aware.get("within_display_precision")
        )
        err_f = float(aware.get("effective_error_pct") or err_f or out["delta_pct"])

    if err_f is not None:
        out["sigma_equivalent"] = (
            round(sigma_equivalent(err_f, reference_uncertainty_pct), 4)
            if reference_uncertainty_pct
            else None
        )
        out["precision_tier"] = lit.get("precision_tier") or precision_tier(err_f, contested=contested)
        gate_err = err_f if not contested else 0.0
        out["within_green_gate"] = gate_err <= GREEN_SCALAR_PCT
        out["within_aspiration_gate"] = gate_err <= ASPIRATION_SCALAR_PCT

    if reference_uncertainty_pct is not None:
        out["reference_uncertainty_pct"] = reference_uncertainty_pct
    if lit.get("reference"):
        out["reference"] = lit["reference"]
    if lit.get("observable_status"):
        out["observable_status"] = lit["observable_status"]

    unit = record.get("unit")
    if unit:
        out["unit"] = unit

    return out


def domain_precision_summary(records: list[dict]) -> dict[str, Any]:
    """Aggregate σ/Δ stats for a domain benchmark."""
    from benchmark_margin_lib import classify_record

    scalar_errs: list[float] = []
    deltas: list[float] = []
    tiers: dict[str, int] = {}

    for r in records:
        if classify_record(r) != "scalar":
            continue
        contested = str(r.get("eval_kind") or "").lower() == "contested_observable"
        env = r.get("scientific_measurement") or measurement_envelope(r, contested=contested)
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