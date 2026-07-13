#!/usr/bin/env python3
"""Top-to-bottom genetics system crosswalk — Tier 94 longevity ↔ Tier 95 developmental."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_canonical_adapter import canonical_domain_scalar, load_fsot_compute  # noqa: E402
from fsot_connective_registry_lib import (  # noqa: E402
    load_connective_registry,
    longevity_genome_pressure,
)
from fsot_developmental_predict_lib import validate_against_mpmath  # noqa: E402
from ingest_zebrafish_reference_anchors import load_zebrafish_reference_anchors  # noqa: E402

OUT = DATA / "tier95_genetics_system_crosswalk_report.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> int:
    issues: list[str] = []
    checks: list[dict] = []

    tier94_spine = _load_json(DATA / "tier_94_longevity_spine_benchmark.json")
    tier95_spine = _load_json(DATA / "tier_95_zebrafish_spine_benchmark.json")
    tier95_bio = _load_json(DATA / "tier95_biological_validation_report.json")
    tier95_coupling = _load_json(DATA / "zebrafish_longevity_genetics_coupling_panel_benchmark.json")
    adjacent = _load_json(DATA / "adjacent_rung_coupling_benchmark.json")
    refs = load_zebrafish_reference_anchors()

    # Species / genome anchor alignment
    t94_zebra = next(
        (r for r in tier94_spine.get("material_records") or [] if r.get("name") == "Danio rerio"),
        None,
    )
    genome_bp = float((refs.get("genome_bp_anchor") or {}).get("measured") or 0)
    if abs(genome_bp - 1.37e9) / 1.37e9 > 0.01:
        issues.append(f"genome_bp_anchor drift: {genome_bp}")
    checks.append(
        {
            "check": "genome_bp_anchor",
            "ok": genome_bp > 0,
            "measured_bp": genome_bp,
            "tier94_present": t94_zebra is not None,
        }
    )

    longevity = refs.get("longevity_anchor") or {}
    pressure = longevity_genome_pressure(
        metabolic_rate_w=float(longevity.get("metabolic_rate_w") or 0.35),
        maximum_longevity_yrs=float(longevity.get("maximum_longevity_yrs") or 5.5),
        longevity_quotient=1.0,
    )
    if pressure <= 0:
        issues.append("longevity_genome_pressure non-positive")
    checks.append(
        {
            "check": "tier94_longevity_spine_coupling",
            "ok": pressure > 0,
            "longevity_genome_pressure": pressure,
            "metabolic_rate_w": longevity.get("metabolic_rate_w"),
            "maximum_longevity_yrs": longevity.get("maximum_longevity_yrs"),
        }
    )

    # Connective registry uses same certified folds as adjacent rung benchmark
    reg = load_connective_registry()
    adj_folds = {
        r.get("mechanism"): float(r.get("computed") or 0)
        for r in adjacent.get("material_records") or []
        if r.get("property") == "adjacent_fold_step"
    }
    for mech, fold in reg.fold_steps.items():
        adj_val = adj_folds.get(mech)
        if adj_val is None:
            continue
        if abs(fold - adj_val) > 1e-9:
            issues.append(f"fold drift {mech}: registry={fold} adjacent={adj_val}")
    checks.append(
        {
            "check": "connective_registry_adjacent_folds",
            "ok": not any("fold drift" in i for i in issues),
            "fold_count": len(reg.fold_steps),
        }
    )

    # Tier 95 spine ↔ biological validation headline
    bio_headline = tier95_bio.get("headline") or {}
    under = bio_headline.get("under_push_target_count")
    total = bio_headline.get("total_mechanistic_count")
    if under != total or total != 20:
        issues.append(f"mechanistic push target incomplete: {under}/{total}")
    checks.append(
        {
            "check": "tier95_mechanistic_push_target",
            "ok": under == total == 20,
            "under_push_target_count": under,
            "total_mechanistic_count": total,
            "median_margin_pct": bio_headline.get("median_margin_of_error_pct"),
            "pearson_r": bio_headline.get("pearson_r"),
        }
    )

    # Longevity genetics coupling panel bridges tier94 ↔ tier95
    coupling_med = float(tier95_coupling.get("pooled_median_error_pct") or 0)
    if coupling_med > 0.5:
        issues.append(f"longevity genetics coupling median {coupling_med}% > 0.5%")
    checks.append(
        {
            "check": "longevity_genetics_coupling_panel",
            "ok": coupling_med <= 0.5,
            "pooled_median_error_pct": coupling_med,
            "record_count": tier95_coupling.get("record_count"),
        }
    )

    # Formal oracle authority matches developmental prediction engine
    _, authority = load_fsot_compute()
    mpmath_check = validate_against_mpmath()
    mpmath_ok = bool(mpmath_check.get("ok"))
    max_rel = float(mpmath_check.get("max_rel_err") or 0.0)
    biology_scalar = float(canonical_domain_scalar("Biology"))
    if not mpmath_ok:
        issues.append(f"mpmath equivalence failed max_rel={max_rel}")
    checks.append(
        {
            "check": "formal_oracle_mpmath_equivalence",
            "ok": mpmath_ok,
            "authority_path": str(authority),
            "biology_domain_scalar": biology_scalar,
            "max_rel": max_rel,
        }
    )

    # Tier 95 spine benchmark green
    spine_med = float(tier95_spine.get("pooled_median_error_pct") or 0)
    checks.append(
        {
            "check": "tier95_spine_benchmark",
            "ok": spine_med <= 0.5,
            "pooled_median_error_pct": spine_med,
            "record_count": tier95_spine.get("record_count"),
        }
    )

    cross_proof = _load_json(DATA / "cross_proof_verification_report.json")
    cp_ok = bool(cross_proof.get("overall_ok"))
    if not cp_ok:
        issues.append("cross_proof_verification overall_ok is False")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tier95_genetics_system_crosswalk",
        "species": "Danio rerio",
        "overall_ok": len(issues) == 0 and cp_ok,
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
        "cross_proof_overall_ok": cp_ok,
        "genetics_application_note": (
            "Tier 95 developmental prediction composes Tier 94 longevity spine, "
            "adjacent-rung certified folds, and fsot_compute formal oracle — "
            "not isolated curve-fit on Zebrahub outcomes."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=== Tier 95 Genetics System Crosswalk ===")
    for chk in checks:
        status = "PASS" if chk.get("ok") else "FAIL"
        print(f"  [{status}] {chk.get('check')}")
    print(f"  cross_proof_overall_ok: {cp_ok}")
    print(f"  overall_ok: {report['overall_ok']}")
    if issues:
        for issue in issues:
            print(f"  ISSUE: {issue}")
    print(f"Wrote {OUT}")
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())