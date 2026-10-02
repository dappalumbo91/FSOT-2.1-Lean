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
        "cross_panel_relay",
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
        "summary_crosscheck",
        "artifact_present",
        "anomaly_anchor",
        "literature_monitor",
        "panel_bridge",
        "reference_gate",
        "count_anchor",
        "time_anchor",
        "time_relay",
        "timing_gate",
        "crosswalk_relay",
        "wave1_crosscheck",
        "panel_relay",
        "panel_anchor",
        "fi_hero_relay",
        "hero_relay",
        "channel_rollup",
        "h0_anchor",
        "h0_gate",
        "dark_sector_anchor",
        "fluid_spacetime_bridge",
        "fluid_spacetime_relay",
        "crosswalk_relay",
        "preregistered_certificate",
        # Legacy catalog identity anchors — must never enter scalar gates.
        "simbad_anchor",
        "gaia_anchor",
        "gaia_literature_anchor",
        "mp_anchor",
        "pubchem_live_anchor",
        "gwosc_live_anchor",
        "gwosc_public_anchor",
        "mast_anchor",
        "wds_live_anchor",
        "wds_anchor",
        "bundled_anchor",
        "bundled_only_anchor",
        "catalog_anchor",
        "dataset_anchor",
        "ingest_meta",
        "domain_panel_bridge",
        "category_panel_bridge",
        "pharmacology_bridge",
        "uniprot_bridge",
        "culinary_arts_bridge",
        "maillard_chemistry_bridge",
        "food_microbiology_bridge",
        "simbad_bridge",
        "tier60_bridge",
        "tier62_bridge",
        "tier68_bridge",
        "tier53_bridge",
        "ingest_consistency",
        "astrometry_consistency",
        "formula_mass_relay",
        "ingest_relay",
        # Honest literature-fit comparisons that are definitionally inconsistent
        # with residual-gated geometric anchors (e.g. CKM α/β/γ fit vs ρ̄,η̄).
        "literature_fit_band",
        "literature_monitor",
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


CATALOG_SPEC_PROPERTIES = frozenset(
    {
        "symmetric_key_bits",
        "block_cipher_rounds",
        "asymmetric_modulus_bits",
        "public_exponent",
        "pqc_security_level",
        "hash_output_bits",
        "key_schedule_words",
        "iv_bits",
        "tag_bits",
        "protocol_version",
        "curve_order_bits",
        "ecc_key_bits",
        "collision_work_exponent",
        "pqc_signature_level",
    }
)

PANEL_ROLLUP_PROPERTY_SUFFIXES = (
    "_panel_cv_pct",
    "_yoy_growth_pct",
)

GAP_FILL_STRUCTURAL_PROPERTIES = frozenset(
    {
        "panel_dispersion",
        "decision_observables",
        "maillard_roast",
        "hvac_thermal",
        "envelope_climate",
        "kepler_third_law_ratio",
        "fi_proxy_hero_certified",
    }
)


def is_ledger_b_scale_step(r: dict) -> bool:
    """True for the catalog step c = m (1 + |S| f).

    New rows are stamped eval_kind fsot_correction. Historical rows from the
    same builder are still stamped fsot_prediction and carry fsot_domain
    and/or fsot_scalar. An fsot_prediction row with neither field is a
    different path (seed-derived or interconnect comparison) and stays
    eligible for the scalar gate. Formula-mass rows are stamped live_formula
    and are not this step.
    """
    kind = str(r.get("eval_kind") or "").lower()
    if kind == "fsot_correction":
        return True
    if kind != "fsot_prediction":
        return False
    if r.get("fsot_domain") or r.get("fsot_scalar") is not None:
        return True
    return False


def classify_record(r: dict, *, file_name: str = "") -> str:
    """Return record kind: scalar | classifier | structural."""
    # c = m (1 + |S| f) is the Ledger B step. It is not a prediction,
    # even when a builder also stamped record_kind scalar or eval_kind
    # fsot_prediction.
    if is_ledger_b_scale_step(r):
        return "structural"

    explicit = r.get("record_kind")
    if explicit in ("scalar", "classifier", "structural"):
        return str(explicit)

    if file_name and "gap_fill" in file_name.lower():
        return "structural"

    prop = (r.get("property") or "").lower()
    eval_kind = str(r.get("eval_kind") or "").lower()

    if eval_kind in STRUCTURAL_EVAL_KINDS:
        return "structural"
    if eval_kind in {"w0_live", "wa_preregistered", "h0_live", "preregistered_falsifiable", "preregistered_certificate"}:
        return "structural"
    if prop in {p.lower() for p in STRUCTURAL_PROPERTIES}:
        return "structural"
    if prop.startswith("section_median_"):
        return "structural"
    if prop in {p.lower() for p in GAP_FILL_STRUCTURAL_PROPERTIES}:
        return "structural"
    if prop in {p.lower() for p in CATALOG_SPEC_PROPERTIES}:
        return "structural"
    if prop in {"pooled_median", "hybrid_fi", "fi_proxy_hero_certification", "headline_median"}:
        return "structural"
    if any(prop.endswith(suffix) for suffix in PANEL_ROLLUP_PROPERTY_SUFFIXES) or "rollup" in prop:
        return "structural"
    if prop.endswith("_pct") and "panel" in prop:
        return "structural"
    if prop in {"median_error_pct", "pooled_median_error_pct", "headline_median_error_pct"}:
        return "structural"
    if eval_kind in {"gap_fill_channel", "tier_gap_fill"} or "gap_fill" in str(r.get("lab") or ""):
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


# Half a unit in the fourth decimal of a percent. Writer output is commonly
# round(error, 6); differences inside this band are display grain.
ERROR_PCT_DISPLAY_TOL = 5e-4


def _stored_error_pct(r: dict) -> float | None:
    e = r.get("error_pct")
    if e is None:
        return None
    try:
        return float(e)
    except (TypeError, ValueError):
        return None


def recomputed_relative_error_pct(r: dict) -> float | None:
    """|computed - measured| / |measured| × 100 from the row's own fields.

    Returns None when measured is 0 or either field is not numeric.
    Percent of a zero measured value is undefined.
    """
    comp = r.get("computed")
    meas = r.get("measured")
    if not isinstance(comp, (int, float)) or not isinstance(meas, (int, float)):
        return None
    measured = float(meas)
    if measured == 0.0:
        return None
    return abs(float(comp) - measured) / abs(measured) * 100.0


def _stored_error_reason(r: dict) -> str | None:
    """Why a row must not be gated on |computed-measured|/|measured|.

    Sigma-distance rows store error_pct in units of the published uncertainty,
    not as a percent of measured. Match flags store a 0/1 outcome in measured.
    Inequality rows store whether a limit holds; computed is the limit.
    """
    if r.get("sigma") is not None or r.get("sigma_distance") is not None:
        return "stored_sigma"
    if isinstance(r.get("match"), bool) or r.get("expected_holes") is True:
        return "stored_match_flag"
    formula = str(r.get("formula") or "")
    prop = str(r.get("property") or "").lower()
    if any(tok in formula for tok in ("≤", "≥", "<=", ">=")):
        return "stored_inequality_bound"
    if "_under_" in prop or prop.endswith("_le_1"):
        return "stored_inequality_bound"
    kind = str(r.get("eval_kind") or "").lower()
    meas = r.get("measured")
    if (
        kind == "dynamics_integration"
        and isinstance(meas, (int, float))
        and float(meas) == 1.0
        and _stored_error_pct(r) == 0.0
    ):
        return "stored_dynamics_flag"
    return None


def gate_error_pct(r: dict) -> tuple[float | None, str]:
    """Error the scalar gate uses, and the reason that figure was chosen."""
    stored = _stored_error_pct(r)
    reason = _stored_error_reason(r)
    if reason is not None:
        return stored, reason
    recomputed = recomputed_relative_error_pct(r)
    if recomputed is None:
        return stored, "stored_measured_zero_or_missing"
    return recomputed, "recomputed"


def error_pct_disagrees(r: dict) -> dict[str, Any] | None:
    """Stored error_pct versus the recomputed percent, past display grain.

    Sigma-distance rows are omitted here. Their stored figure is a different unit,
    so a numeric gap is not a percent-error disagreement.
    """
    if r.get("sigma") is not None or r.get("sigma_distance") is not None:
        return None
    stored = _stored_error_pct(r)
    recomputed = recomputed_relative_error_pct(r)
    if stored is None or recomputed is None:
        return None
    if abs(stored - recomputed) <= ERROR_PCT_DISPLAY_TOL:
        return None
    return {
        "name": r.get("name"),
        "property": r.get("property"),
        "eval_kind": r.get("eval_kind"),
        "stored_error_pct": stored,
        "recomputed_error_pct": recomputed,
        "computed": r.get("computed"),
        "measured": r.get("measured"),
        "ledger_b_scale_step": is_ledger_b_scale_step(r),
        "gate_reason": _stored_error_reason(r) or "recomputed",
    }


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


def scalar_metrics(records: list[dict], *, file_name: str = "") -> dict[str, Any]:
    """Continuous FSOT prediction error metrics (excludes classifiers/structural)."""
    from literature_uncertainty_lib import is_contested_record
    from scientific_measurement_lib import literature_aware_error_pct

    errs = []
    stored_errs = []
    effective_errs = []
    gate_errs: list[float] = []
    max_err = 0.0
    max_stored_err = 0.0
    max_gate_err = 0.0
    max_effective_any = 0.0
    max_row: dict | None = None
    max_stored_row: dict | None = None
    max_gate_row: dict | None = None
    max_effective_row: dict | None = None
    rounding_ghost_count = 0
    catalog_crosswalk_count = 0
    disagreement_count = 0
    disagreement_crosses_half_pct = 0

    for r in records:
        if classify_record(r, file_name=file_name) != "scalar":
            continue
        e = r.get("error_pct")
        if e is None:
            continue
        try:
            ef = float(e)
        except (TypeError, ValueError):
            continue
        stored_errs.append(ef)
        if ef > max_stored_err:
            max_stored_err = ef
            max_stored_row = r
        gate_value, gate_reason = gate_error_pct(r)
        if gate_value is None:
            continue
        # The scalar gate uses the recomputed percent. Sigma-distance rows,
        # match flags, and inequality limits keep the stored figure: that
        # figure is not |computed-measured|/|measured|.
        used = float(gate_value)
        errs.append(used)
        if used > max_err:
            max_err = used
            max_row = r
        gap = error_pct_disagrees(r)
        if gap is not None and gate_reason == "recomputed":
            disagreement_count += 1
            if gap["recomputed_error_pct"] > MAX_SCALAR_ERROR_PCT and ef <= MAX_SCALAR_ERROR_PCT:
                disagreement_crosses_half_pct += 1

        comp = r.get("computed")
        meas = r.get("measured")
        if comp is not None and meas is not None:
            try:
                aware = literature_aware_error_pct(float(comp), float(meas), r)
            except (TypeError, ValueError):
                aware = {"effective_error_pct": used, "comparison_kind": "raw"}
        else:
            aware = {"effective_error_pct": used, "comparison_kind": "raw"}

        eff_raw = aware.get("effective_error_pct")
        eff = float(eff_raw if eff_raw is not None else used)
        effective_errs.append(eff)
        contested = is_contested_record(r)
        gate_err = eff if contested else used
        gate_errs.append(gate_err)
        if gate_err > max_gate_err:
            max_gate_err = gate_err
            max_gate_row = r
        if eff > max_effective_any:
            max_effective_any = eff
            max_effective_row = r
        if aware.get("comparison_kind") == "catalog_crosswalk":
            catalog_crosswalk_count += 1
        elif aware.get("within_display_precision") or aware.get("within_literature_band"):
            if ef > MAX_SCALAR_ERROR_PCT:
                rounding_ghost_count += 1

    max_raw_effective = max_err
    if max_row is not None:
        comp = max_row.get("computed")
        meas = max_row.get("measured")
        if comp is not None and meas is not None:
            try:
                aware = literature_aware_error_pct(float(comp), float(meas), max_row)
                max_raw_effective = float(aware.get("effective_error_pct") or max_err)
            except (TypeError, ValueError):
                max_raw_effective = max_err

    med = _median_or_none(errs)
    stored_med = _median_or_none(stored_errs)
    effective_med = _median_or_none(effective_errs)
    gate_med = _median_or_none(gate_errs)
    tier_med = effective_med if effective_med is not None else (gate_med if gate_med is not None else med)
    return {
        "scalar_count": len(errs),
        "scalar_median_error_pct": med,
        "scalar_median_stored_error_pct": stored_med,
        "max_scalar_error_pct": max_err if errs else None,
        "max_stored_scalar_error_pct": max_stored_err if stored_errs else None,
        "stored_error_disagreement_count": disagreement_count,
        "stored_error_crosses_half_pct_count": disagreement_crosses_half_pct,
        "max_scalar_name": (max_row or {}).get("name"),
        "max_scalar_property": (max_row or {}).get("property"),
        "effective_scalar_median_error_pct": effective_med,
        "max_effective_scalar_error_pct": max_raw_effective if effective_errs else None,
        "max_effective_scalar_name": (max_row or {}).get("name"),
        "max_effective_scalar_property": (max_row or {}).get("property"),
        "worst_effective_scalar_error_pct": max_effective_any if effective_errs else None,
        "worst_effective_scalar_name": (max_effective_row or {}).get("name"),
        "worst_effective_scalar_property": (max_effective_row or {}).get("property"),
        "rounding_ghost_scalar_count": rounding_ghost_count,
        "catalog_crosswalk_scalar_count": catalog_crosswalk_count,
        "strict_scalar_pass": not gate_errs or max_gate_err <= MAX_SCALAR_ERROR_PCT,
        "strict_scalar_pass_stored_error": not stored_errs or max_stored_err <= MAX_SCALAR_ERROR_PCT,
        "effective_scalar_pass": not effective_errs or max_raw_effective <= MAX_SCALAR_ERROR_PCT,
        "max_gate_scalar_error_pct": max_gate_err if gate_errs else None,
        "max_gate_scalar_name": (max_gate_row or {}).get("name"),
        "max_gate_scalar_property": (max_gate_row or {}).get("property"),
        "tier_scalar_median_error_pct": tier_med,
        "tier_scalar_pass": not errs
        or (tier_med is not None and tier_med <= TIER_SCALAR_MAX_ERROR_PCT),
        "tier_scalar_max_pass": not errs or max_err <= TIER_SCALAR_MAX_ERROR_PCT,
        "scalar_median_pass": med is None or med <= MAX_MEDIAN_ERROR_PCT,
    }


def prediction_class_counts(records: list[dict], *, file_name: str = "") -> dict[str, int]:
    """Genuine scalar-gate rows versus Ledger B scale-step rows.

    Genuine predictions are records that remain in the scalar gate.
    Structural corrections are the Ledger B step only. Other structural
    kinds (anchors, rollups, preregistration holds) are neither count.
    """
    genuine = 0
    structural_correction = 0
    for r in records:
        if not isinstance(r, dict):
            continue
        if is_ledger_b_scale_step(r):
            structural_correction += 1
            continue
        if classify_record(r, file_name=file_name) != "scalar":
            continue
        e = r.get("error_pct")
        if e is None:
            continue
        try:
            float(e)
        except (TypeError, ValueError):
            continue
        genuine += 1
    return {
        "genuine_prediction_count": genuine,
        "structural_correction_count": structural_correction,
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

    scalar = scalar_metrics(mat, file_name=file_name)
    classifier = classifier_metrics(mat)
    classes = prediction_class_counts(mat, file_name=file_name)

    scalar_pooled = scalar["scalar_median_error_pct"]
    if scalar["scalar_count"] > 0:
        official_pooled = scalar_pooled
    else:
        # Structural / literature-monitor domains — do not inherit headline rollups.
        official_pooled = None

    green_pass = (
        (official_pooled is None or official_pooled <= MAX_MEDIAN_ERROR_PCT)
        and classifier["classifier_pass"]
        and (scalar["scalar_count"] == 0 or scalar["strict_scalar_pass"])
    )
    stored_pooled = scalar.get("scalar_median_stored_error_pct")
    if scalar["scalar_count"] == 0:
        stored_pooled = None
    green_pass_stored = (
        (stored_pooled is None or stored_pooled <= MAX_MEDIAN_ERROR_PCT)
        and classifier["classifier_pass"]
        and (scalar["scalar_count"] == 0 or scalar["strict_scalar_pass_stored_error"])
    )

    return {
        "excluded": False,
        "file": file_name,
        "domain": doc.get("domain") or file_name,
        "records": doc.get("record_count") or doc.get("observable_count") or len(mat),
        "pooled_median_error_pct": float(pooled_headline) if pooled_headline is not None else None,
        "scalar_pooled_median_error_pct": scalar_pooled,
        "official_pooled_median_error_pct": official_pooled,
        "green_gate_pass": green_pass,
        "green_gate_pass_stored_error": green_pass_stored,
        "scalar_gate_applicable": scalar["scalar_count"] > 0,
        "green_gate_pass_pooled_only": green_pass,
        **classes,
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