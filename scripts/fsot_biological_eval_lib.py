"""Biological-science evaluation metrics for Tier 95 developmental predictions.

Standard reporting (developmental / cell-tracking literature):
  Pearson r, Spearman ρ, R², RMSE, MAE, bias (signed mean residual),
  σ-equivalent vs literature uncertainty, within-band pass rate.
"""

from __future__ import annotations

import math
from typing import Any

from scientific_measurement_lib import (
    literature_aware_error_pct,
    measurement_envelope,
    relative_error_pct,
    sigma_equivalent,
)

MECHANISTIC_PROPERTIES = (
    "division_rate",
    "mean_track_duration_steps",
    "mean_displacement_um",
    "developmental_stability_proxy",
)

PROPERTY_UNITS: dict[str, str] = {
    "division_rate": "dimensionless",
    "mean_track_duration_steps": "imaging_frames",
    "mean_displacement_um": "micrometers",
    "developmental_stability_proxy": "dimensionless",
}


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def pearson_r(measured: list[float], computed: list[float]) -> float | None:
    if len(measured) < 2 or len(measured) != len(computed):
        return None
    mx, my = _mean(measured), _mean(computed)
    num = sum((x - mx) * (y - my) for x, y in zip(measured, computed))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in measured))
    den_y = math.sqrt(sum((y - my) ** 2 for y in computed))
    if den_x <= 0 or den_y <= 0:
        return None
    return num / (den_x * den_y)


def spearman_rho(measured: list[float], computed: list[float]) -> float | None:
    if len(measured) < 2 or len(measured) != len(computed):
        return None

    def _ranks(vals: list[float]) -> list[float]:
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        ranks = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg_rank = (i + j + 2) / 2.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg_rank
            i = j + 1
        return ranks

    return pearson_r(_ranks(measured), _ranks(computed))


def r_squared(measured: list[float], computed: list[float]) -> float | None:
    if len(measured) < 2 or len(measured) != len(computed):
        return None
    my = _mean(measured)
    ss_res = sum((m - c) ** 2 for m, c in zip(measured, computed))
    ss_tot = sum((m - my) ** 2 for m in measured)
    if ss_tot <= 0:
        return None
    return 1.0 - ss_res / ss_tot


def rmse(measured: list[float], computed: list[float]) -> float | None:
    if not measured or len(measured) != len(computed):
        return None
    return math.sqrt(_mean([(m - c) ** 2 for m, c in zip(measured, computed)]))


def mae(measured: list[float], computed: list[float]) -> float | None:
    if not measured or len(measured) != len(computed):
        return None
    return _mean([abs(m - c) for m, c in zip(measured, computed)])


def bias(measured: list[float], computed: list[float]) -> float | None:
    if not measured or len(measured) != len(computed):
        return None
    return _mean([c - m for m, c in zip(measured, computed)])


def nrmse_pct(measured: list[float], computed: list[float]) -> float | None:
    """Normalized RMSE as % of observed range (common in developmental imaging)."""
    val = rmse(measured, computed)
    if val is None or not measured:
        return None
    span = max(measured) - min(measured)
    if span <= 0:
        return None
    return val / span * 100.0


def enrich_biological_record(
    record: dict[str, Any],
    *,
    reference_anchor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Attach biological-science envelope to one prediction record."""
    prop = str(record.get("property") or "")
    measured = float(record.get("measured") or 0.0)
    computed = float(record.get("computed") or 0.0)
    anchor = dict(reference_anchor or {})
    anchor.setdefault("property", prop)
    anchor.setdefault("unit", PROPERTY_UNITS.get(prop, "dimensionless"))
    if anchor.get("reference_uncertainty_pct") is None:
        anchor["reference_uncertainty_pct"] = anchor.get("literature_cv_pct")

    row = {**record, **anchor}
    sci = measurement_envelope(
        row,
        reference_uncertainty_pct=anchor.get("reference_uncertainty_pct"),
    )
    aware = literature_aware_error_pct(computed, measured, row)
    delta = computed - measured
    unc = anchor.get("reference_uncertainty_pct")
    sigma = sigma_equivalent(float(aware.get("raw_error_pct") or 0.0), unc)

    margin_pct = float(aware.get("raw_error_pct") or relative_error_pct(computed, measured))
    return {
        **record,
        "unit": anchor.get("unit"),
        "delta": round(delta, 8),
        "abs_delta": round(abs(delta), 8),
        "margin_of_error_pct": round(margin_pct, 4),
        "raw_error_pct": round(margin_pct, 6),
        "effective_error_pct": round(float(aware.get("effective_error_pct") or 0.0), 6),
        "comparison_kind": aware.get("comparison_kind"),
        "within_literature_band": bool(aware.get("within_literature_band")),
        "reference": anchor.get("reference"),
        "reference_source": anchor.get("source"),
        "reference_uncertainty_pct": unc,
        "sigma_equivalent": round(sigma, 4) if sigma is not None else None,
        "scientific_measurement": sci,
    }


def property_aggregate_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-property biological metrics across datasets (LODO pooled)."""
    by_prop: dict[str, list[dict]] = {}
    for rec in records:
        prop = str(rec.get("property") or "")
        if prop:
            by_prop.setdefault(prop, []).append(rec)

    out: dict[str, Any] = {}
    for prop, rows in sorted(by_prop.items()):
        measured = [float(r["measured"]) for r in rows]
        computed = [float(r["computed"]) for r in rows]
        raw_errs = [float(r.get("raw_error_pct") or 0.0) for r in rows]
        sigmas = [float(r["sigma_equivalent"]) for r in rows if r.get("sigma_equivalent") is not None]
        within = sum(1 for r in rows if r.get("within_literature_band"))
        out[prop] = {
            "n": len(rows),
            "unit": PROPERTY_UNITS.get(prop),
            "pearson_r": round(pearson_r(measured, computed) or 0.0, 6)
            if pearson_r(measured, computed) is not None
            else None,
            "spearman_rho": round(spearman_rho(measured, computed) or 0.0, 6)
            if spearman_rho(measured, computed) is not None
            else None,
            "r_squared": round(r_squared(measured, computed) or 0.0, 6)
            if r_squared(measured, computed) is not None
            else None,
            "rmse": round(rmse(measured, computed) or 0.0, 6) if rmse(measured, computed) is not None else None,
            "mae": round(mae(measured, computed) or 0.0, 6) if mae(measured, computed) is not None else None,
            "bias": round(bias(measured, computed) or 0.0, 6) if bias(measured, computed) is not None else None,
            "nrmse_pct": round(nrmse_pct(measured, computed) or 0.0, 4)
            if nrmse_pct(measured, computed) is not None
            else None,
            "median_margin_of_error_pct": sorted(raw_errs)[len(raw_errs) // 2] if raw_errs else None,
            "mean_margin_of_error_pct": round(_mean(raw_errs), 4) if raw_errs else None,
            "max_margin_of_error_pct": round(max(raw_errs), 4) if raw_errs else None,
            "median_raw_error_pct": sorted(raw_errs)[len(raw_errs) // 2] if raw_errs else None,
            "mean_sigma_equivalent": round(_mean(sigmas), 4) if sigmas else None,
            "within_literature_band_fraction": round(within / len(rows), 4) if rows else None,
        }
    return out


def margin_of_error_scorecard(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Human-readable accuracy card: measured, computed, % margin, Δ, σ."""
    rows: list[dict[str, Any]] = []
    for rec in records:
        if rec.get("property") not in MECHANISTIC_PROPERTIES:
            continue
        margin = float(rec.get("margin_of_error_pct") or rec.get("raw_error_pct") or 0.0)
        rows.append(
            {
                "dataset_id": rec.get("dataset_id"),
                "property": rec.get("property"),
                "unit": rec.get("unit") or PROPERTY_UNITS.get(str(rec.get("property") or ""), ""),
                "measured": rec.get("measured"),
                "computed": rec.get("computed"),
                "margin_of_error_pct": round(margin, 4),
                "delta": rec.get("delta"),
                "abs_delta": rec.get("abs_delta"),
                "sigma_equivalent": rec.get("sigma_equivalent"),
                "reference_uncertainty_pct": rec.get("reference_uncertainty_pct"),
                "within_literature_band": rec.get("within_literature_band"),
                "comparison_kind": rec.get("comparison_kind"),
                "reference": rec.get("reference"),
            }
        )
    return sorted(rows, key=lambda r: (-float(r.get("margin_of_error_pct") or 0.0), str(r.get("dataset_id"))))


def mechanistic_biological_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Headline biological-science summary for mechanistic properties."""
    mech = [r for r in records if r.get("property") in MECHANISTIC_PROPERTIES]
    if not mech:
        return {"record_count": 0}

    measured = [float(r["measured"]) for r in mech]
    computed = [float(r["computed"]) for r in mech]
    raw_errs = [float(r.get("raw_error_pct") or 0.0) for r in mech]
    sigmas = [float(r["sigma_equivalent"]) for r in mech if r.get("sigma_equivalent") is not None]
    within = sum(1 for r in mech if r.get("within_literature_band"))

    return {
        "record_count": len(mech),
        "pearson_r": round(pearson_r(measured, computed) or 0.0, 6)
        if pearson_r(measured, computed) is not None
        else None,
        "spearman_rho": round(spearman_rho(measured, computed) or 0.0, 6)
        if spearman_rho(measured, computed) is not None
        else None,
        "r_squared": round(r_squared(measured, computed) or 0.0, 6)
        if r_squared(measured, computed) is not None
        else None,
        "pooled_rmse": round(rmse(measured, computed) or 0.0, 6) if rmse(measured, computed) is not None else None,
        "pooled_mae": round(mae(measured, computed) or 0.0, 6) if mae(measured, computed) is not None else None,
        "pooled_bias": round(bias(measured, computed) or 0.0, 6) if bias(measured, computed) is not None else None,
        "median_margin_of_error_pct": sorted(raw_errs)[len(raw_errs) // 2] if raw_errs else None,
        "mean_margin_of_error_pct": round(_mean(raw_errs), 4) if raw_errs else None,
        "max_margin_of_error_pct": round(max(raw_errs), 4) if raw_errs else None,
        "median_raw_error_pct": sorted(raw_errs)[len(raw_errs) // 2] if raw_errs else None,
        "mean_sigma_equivalent": round(_mean(sigmas), 4) if sigmas else None,
        "within_literature_band_fraction": round(within / len(mech), 4),
        "per_property": property_aggregate_metrics(mech),
        "accuracy_scorecard": margin_of_error_scorecard(mech),
    }