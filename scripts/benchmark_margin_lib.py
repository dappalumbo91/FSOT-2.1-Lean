"""Shared benchmark margin metrics — scalar vs binary classifier vs structural evaluation."""

from __future__ import annotations

from statistics import median
from typing import Any

from fsot_precision_constants import (
    AUDIT_EXCLUDED_BENCHMARKS,
    MAX_MEDIAN_ERROR_PCT,
    MAX_SCALAR_ERROR_PCT,
    MIN_CLASSIFIER_ACCURACY_PCT,
    TIER_SCALAR_MAX_ERROR_PCT,
)

# Not FSOT predictions — must never enter scalar error gates.
STRUCTURAL_EVAL_KINDS = frozenset(
    {
        "catalog_consistency",
        "public_catalog_anchor",
        "crosswalk_bridge",
        "scalar_bridge",
        "structural",
        "meta_inventory",
        "inventory",
        "rollup",
        "prereg_scaffold",
        "gap_detection",
        "classifier_match",
        "panel_relay",
        "stability_index",
        "skipped",
        "jpl_physical",
        "jpl_orbital",
        "jpl_kepler",
        "reference_anchor",
        "jpl_elements",
        "panel_anchor",
        "contested_observable",
        "cross_domain_bridge",
        "bridge_observable",
        "fsot_compute",
        "certificate_gate",
        "fic_valve",
        "resonance_crosswalk",
        "live_formula",
        "summary_crosscheck",
        "artifact_present",
    }
)

STRUCTURAL_PROPERTIES = frozenset(
    {
        "detected_hole_count",
        "domain_benchmark_records",
        "positive_S_verse_count",
        "codon_weight_count",
        "gauntlet_pass_rate_pct",
        "domain_pooled_median",
        "child_domain_pooled_median",
        "strict_empirical_max_error_pct",
        "mean_codon_stability",
        "codon_unit_coverage",
        "pooled_igem_median",
        "schema_pass_rate_pct",
        "stabilization_margin",
        "kepler_mass_closure",
        "prediction_gap_fill",
        "info_uplift_fraction",
        "vib_avg_S",
        "archetype_mean_S",
        "stabilization_margin",
        "positive_s_verse_count",
        "discriminant_pass",
        "codon_stability",
        "mt_genome_bp",
    }
)

CLASSIFIER_PROPERTIES = frozenset(
    {
        "nebula_lensing_coupling",
        "nebula_framework_fit",
        "fic_fertile_classifier",
        "storm_classifier",
        "classifier_match",
        "kp_storm_classifier",
        "freezing_month_classifier",
        "dst_storm_classifier",
        "goes_storm_classifier",
        "shallow_depth_classifier",
        "mass_decline_classifier",
    }
)

CLASSIFIER_FIELD_PAIRS: tuple[tuple[str, str], ...] = (
    ("computed", "measured"),
    ("computed_coupled", "measured_coupled"),
    ("computed_freezing", "measured_freezing"),
    ("computed_quiet", "measured_quiet"),
    ("computed_repeater", "measured_repeater"),
    ("computed_shallow", "measured_shallow"),
    ("computed_loss", "measured_loss"),
    ("computed_decline", "measured_decline"),
    ("computed_crustal", "measured_crustal"),
    ("computed_quality", "measured_quality"),
    ("computed_mt", "measured_mt"),
    ("computed_margin", "measured_margin"),
)


def _classifier_field_pair(r: dict) -> tuple[str, str] | None:
    for comp_key, meas_key in CLASSIFIER_FIELD_PAIRS:
        if comp_key in r and meas_key in r:
            return comp_key, meas_key
    return None


def classify_record(r: dict) -> str:
    """Return record kind: scalar | classifier | structural."""
    explicit = r.get("record_kind")
    if explicit in ("scalar", "classifier", "structural"):
        return str(explicit)

    prop = (r.get("property") or "").lower()
    eval_kind = str(r.get("eval_kind") or "").lower()

    if eval_kind in STRUCTURAL_EVAL_KINDS:
        return "structural"
    if prop in {p.lower() for p in STRUCTURAL_PROPERTIES}:
        return "structural"
    pair = _classifier_field_pair(r)
    if pair and (
        prop in {p.lower() for p in CLASSIFIER_PROPERTIES}
        or prop.endswith("_classifier")
        or "classifier" in prop
        or eval_kind == "classifier_match"
    ):
        return "classifier"

    if (
        "gate" in prop
        or prop == "exit_code_zero"
        or prop.endswith("_zero")
        or prop.endswith("_resolved")
    ):
        return "structural"

    # Inventory / count rows where measured=0 is a target sentinel, not an observable.
    if prop.endswith("_count") or prop.endswith("_records"):
        return "structural"
    meas = r.get("measured")
    if meas in (0, 0.0) and prop.endswith("_median") and eval_kind != "scalar_prediction":
        return "structural"

    return "scalar"


def _median_or_none(values: list[float]) -> float | None:
    return float(median(values)) if values else None


def classifier_metrics(records: list[dict]) -> dict[str, Any]:
    """Accuracy-based metrics for binary {0,1} classifier records."""
    cls = [r for r in records if classify_record(r) == "classifier"]
    if not cls:
        return {
            "classifier_count": 0,
            "classifier_correct": 0,
            "classifier_misclass_count": 0,
            "classifier_accuracy_pct": None,
            "classifier_misclass_rate_pct": None,
            "classifier_pass": True,
        }
    correct = 0
    for r in cls:
        pair = _classifier_field_pair(r)
        if not pair:
            continue
        comp_key, meas_key = pair
        try:
            if int(round(float(r.get(comp_key, -1)))) == int(round(float(r.get(meas_key, -2)))):
                correct += 1
        except (TypeError, ValueError):
            pass
    n = len(cls)
    mis = n - correct
    acc = 100.0 * correct / n
    mis_rate = 100.0 * mis / n
    return {
        "classifier_count": n,
        "classifier_correct": correct,
        "classifier_misclass_count": mis,
        "classifier_accuracy_pct": round(acc, 6),
        "classifier_misclass_rate_pct": round(mis_rate, 6),
        "classifier_pass": acc >= MIN_CLASSIFIER_ACCURACY_PCT,
    }


def scalar_metrics(records: list[dict]) -> dict[str, Any]:
    """Continuous FSOT prediction error metrics (excludes classifiers/structural)."""
    errs = []
    max_err = 0.0
    max_row: dict | None = None
    for r in records:
        if classify_record(r) != "scalar":
            continue
        e = r.get("error_pct")
        if e is None:
            continue
        try:
            ef = float(e)
        except (TypeError, ValueError):
            continue
        errs.append(ef)
        if ef > max_err:
            max_err = ef
            max_row = r
    med = _median_or_none(errs)
    return {
        "scalar_count": len(errs),
        "scalar_median_error_pct": med,
        "max_scalar_error_pct": max_err if errs else None,
        "max_scalar_name": (max_row or {}).get("name"),
        "max_scalar_property": (max_row or {}).get("property"),
        "strict_scalar_pass": not errs or max_err <= MAX_SCALAR_ERROR_PCT,
        "tier_scalar_pass": not errs or max_err <= TIER_SCALAR_MAX_ERROR_PCT,
        "scalar_median_pass": med is None or med <= MAX_MEDIAN_ERROR_PCT,
    }


def analyze_benchmark(doc: dict, *, file_name: str = "") -> dict[str, Any]:
    """Full margin analysis for one benchmark JSON document."""
    if file_name in AUDIT_EXCLUDED_BENCHMARKS:
        return {
            "excluded": True,
            "file": file_name,
            "domain": doc.get("domain") or file_name,
            "exclusion_reason": "legacy_stub_non_v11_panel",
        }

    mat = doc.get("material_records") or doc.get("records") or []
    pooled_headline = doc.get("pooled_median_error_pct")
    if pooled_headline is None:
        pooled_headline = doc.get("median_error_pct")
    if pooled_headline is None:
        pooled_headline = doc.get("headline_median_error_pct")

    scalar = scalar_metrics(mat)
    classifier = classifier_metrics(mat)

    scalar_pooled = scalar["scalar_median_error_pct"]
    official_pooled = scalar_pooled if scalar_pooled is not None else (
        float(pooled_headline) if pooled_headline is not None else None
    )

    green_pass = official_pooled is None or official_pooled <= MAX_MEDIAN_ERROR_PCT

    return {
        "excluded": False,
        "file": file_name,
        "domain": doc.get("domain") or file_name,
        "records": doc.get("record_count") or doc.get("observable_count") or len(mat),
        "pooled_median_error_pct": float(pooled_headline) if pooled_headline is not None else None,
        "scalar_pooled_median_error_pct": scalar_pooled,
        "official_pooled_median_error_pct": official_pooled,
        "green_gate_pass": green_pass and classifier["classifier_pass"] and scalar["strict_scalar_pass"],
        "green_gate_pass_pooled_only": green_pass,
        **scalar,
        **classifier,
    }


def margin_summary_for_benchmark(material_records: list[dict]) -> dict[str, Any]:
    """Embed in benchmark JSON at write time."""
    scalar = scalar_metrics(material_records)
    classifier = classifier_metrics(material_records)
    official_pooled = scalar["scalar_median_error_pct"]
    if official_pooled is None:
        errs = [
            float(r["error_pct"])
            for r in material_records
            if classify_record(r) == "scalar" and r.get("error_pct") is not None
        ]
        official_pooled = _median_or_none(errs)
    return {
        "scalar_pooled_median_error_pct": official_pooled,
        "max_scalar_error_pct": scalar["max_scalar_error_pct"],
        **classifier,
        "fsot_precision_aligned": bool(
            (official_pooled is None or official_pooled <= MAX_MEDIAN_ERROR_PCT)
            and scalar["strict_scalar_pass"]
            and classifier["classifier_pass"]
        ),
    }