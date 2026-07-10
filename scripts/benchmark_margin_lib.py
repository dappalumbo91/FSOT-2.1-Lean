"""Shared benchmark margin metrics — scalar vs binary classifier evaluation."""

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


def classify_record(r: dict) -> str:
    """Return record kind: scalar | classifier | structural."""
    comp = r.get("computed")
    meas = r.get("measured")
    prop = (r.get("property") or "").lower()
    if comp in (0, 1, 0.0, 1.0) and meas in (0, 1, 0.0, 1.0):
        return "classifier"
    if (
        "classifier" in prop
        or "gate" in prop
        or prop == "exit_code_zero"
        or prop.endswith("_zero")
        or prop.endswith("_resolved")
    ):
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
        try:
            if int(round(float(r.get("computed", -1)))) == int(round(float(r.get("measured", -2)))):
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
    """Continuous prediction error metrics (excludes classifiers)."""
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

    # Official gate uses scalar-only pooled median when scalars exist.
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
        "green_gate_pass": green_pass and classifier["classifier_pass"],
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
        errs = [float(r["error_pct"]) for r in material_records if r.get("error_pct") is not None]
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