#!/usr/bin/env python3
"""Consolidated deep verification audit — cross-proof, refinement, export, precision."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "deep_verification_audit.json"

REPORTS = {
    "cross_proof": ROOT / "data" / "cross_proof_verification_report.json",
    "depth": ROOT / "data" / "verification_depth_audit.json",
    "export": ROOT / "data" / "export_exclusion_registry.json",
    "transcendental": ROOT / "data" / "transcendental_certificate_audit.json",
    "transcendental_gap": ROOT / "data" / "transcendental_bounds_gap_report.json",
    "transcendental_obligations": ROOT / "verification" / "obligations" / "transcendental_bounds.json",
    "pushback": ROOT / "data" / "scientific_pushback_audit.json",
    "margins": ROOT / "data" / "benchmark_margin_audit.json",
    "coq_refinement": ROOT / "data" / "cross_refinement_lean_coq_report.json",
    "isabelle_refinement": ROOT / "data" / "cross_refinement_lean_isabelle_report.json",
    "rust_refinement": ROOT / "data" / "cross_refinement_rust_report.json",
    "fstar_refinement": ROOT / "data" / "cross_refinement_fstar_report.json",
    "coverage": ROOT / "data" / "cross_proof_coverage_audit.json",
    "structural": ROOT / "data" / "structural_proof_depth_audit.json",
    "living_hardware": ROOT / "data" / "living_fsot_hardware_verification_report.json",
    "bundle_ledger": ROOT / "data" / "structural_bundle_ledger.json",
    "oracle_ledger": ROOT / "data" / "oracle_debt_ledger.json",
    "formula_honesty": ROOT / "data" / "formula_corpus_honesty_report.json",
    "runtime_scope": ROOT / "data" / "runtime_verification_scope_audit.json",
    "parameter_closure": ROOT / "data" / "parameter_honesty_closure.json",
}


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_rust_count(cross: dict, coq_ref: dict) -> int:
    conn = int((cross.get("connective_spine") or {}).get("obligation_count", 0))
    trans = int((cross.get("transcendental_bounds") or {}).get("obligation_count", 0))
    atomic = int(coq_ref.get("obligation_count_atomic_provable", 0))
    if not atomic:
        formal = cross.get("full_formal_spine") or {}
        provable = int(formal.get("provable_count", 0))
        bundle_prov = int(coq_ref.get("obligation_count_bundle_conj", 0))
        atomic = provable - bundle_prov
    return conn + atomic + trans


def _margin_bundle_analysis(cross: dict, coq_ref: dict, bundle_ledger: dict) -> dict:
    formal = cross.get("full_formal_spine") or {}
    tri = coq_ref.get("triangulation") or {}
    bl = bundle_ledger.get("summary") or {}
    return {
        "total_obligations": formal.get("obligation_count"),
        "provable_atomic": coq_ref.get("obligation_count_atomic_provable"),
        "provable_bundle_conj": coq_ref.get("obligation_count_bundle_conj"),
        "structural_bundle_excluded": formal.get("structural_bundle_excluded_count")
        or bl.get("structural_bundle_excluded"),
        "false_margin_violations": formal.get("margin_violation_count"),
        "conjunct_atomic_coverage_pct": bl.get("conjunct_atomic_coverage_pct"),
        "margin_violation_design": (
            "False margin violations are atomic inequalities that fail Python verify. "
            "Structural bundle_conj rows are excluded from Coq/Isabelle/Rust by design — "
            "see data/structural_bundle_ledger.json."
        ),
        "lt_half_pooled_median_margin": coq_ref.get("lt_half_pooled_median_margin_to_bound"),
        "atomic_triangulated": f"{tri.get('atomic_triangulated_ok', 0)}/{coq_ref.get('obligation_count_atomic_provable', 0)}",
        "bundle_conj_triangulated": f"{tri.get('bundle_conj_triangulated_ok', 0)}/{coq_ref.get('obligation_count_bundle_conj', 0)}",
        "margin_violations_confirmed_in_lean": tri.get("margin_violations_confirmed_ok", 0),
        "margin_violations_unconfirmed": tri.get("margin_violations_confirmed_fail", 0),
    }


def _transcendental_gaps(trans_ob: dict) -> dict:
    obligations = trans_ob.get("obligations") or []
    missing_py = [
        o["id"]
        for o in obligations
        if o.get("python_decimal_verified") is not True
    ]
    native_pi_e = [o["id"] for o in obligations if o.get("proof_template") in ("e_interval", "pi_interval")]
    return {
        "obligation_count": trans_ob.get("obligation_count"),
        "python_decimal_verified_count": trans_ob.get("python_decimal_verified_count"),
        "missing_python_decimal": missing_py,
        "native_pi_e_intervals": native_pi_e,
        "structural_symbolic": [
            o["id"]
            for o in obligations
            if "consciousness_factor" in str(o.get("lean_type") or "")
        ],
    }


def _raw_eff_divergence_summary(pushback: dict) -> list[dict]:
    return list(pushback.get("raw_eff_divergence_domains") or [])


def build() -> dict:
    cross = _load(REPORTS["cross_proof"])
    depth = _load(REPORTS["depth"])
    export_reg = _load(REPORTS["export"])
    trans_cert = _load(REPORTS["transcendental"])
    trans_gap = _load(REPORTS["transcendental_gap"])
    trans_ob = _load(REPORTS["transcendental_obligations"])
    pushback = _load(REPORTS["pushback"])
    margins = _load(REPORTS["margins"])
    coq_ref = _load(REPORTS["coq_refinement"])
    isa_ref = _load(REPORTS["isabelle_refinement"])
    rust_ref = _load(REPORTS["rust_refinement"])
    fstar_ref = _load(REPORTS["fstar_refinement"])
    coverage = _load(REPORTS["coverage"])
    living_hw = _load(REPORTS["living_hardware"])
    bundle_ledger = _load(REPORTS["bundle_ledger"])
    oracle_ledger = _load(REPORTS["oracle_ledger"])
    formula_honesty = _load(REPORTS["formula_honesty"])
    runtime_scope = _load(REPORTS["runtime_scope"])
    parameter_closure = _load(REPORTS["parameter_closure"])

    rust_expected = _expected_rust_count(cross, coq_ref)
    rust_actual = int((cross.get("frameworks") or {}).get("rust_replay", {}).get("obligation_count", 0))
    rust_meta = rust_ref.get("rust_meta") or {}

    open_gaps = depth.get("open_gaps") or []
    stale_rust = rust_actual != rust_expected and rust_meta.get("total_count") != rust_expected

    findings: list[dict] = []
    if stale_rust:
        findings.append(
            {
                "id": "rust_count_mismatch",
                "severity": "low",
                "detail": f"report={rust_actual} expected={rust_expected} rust_meta={rust_meta.get('total_count')}",
                "remedy": "Re-run run_cross_proof_verification.py",
            }
        )

    trans_gaps = _transcendental_gaps(trans_ob)
    if trans_gaps["missing_python_decimal"]:
        symbolic = set(trans_gaps["structural_symbolic"])
        native = set(trans_gaps["native_pi_e_intervals"])
        unexpected = [x for x in trans_gaps["missing_python_decimal"] if x not in symbolic and x not in native]
        if unexpected:
            findings.append(
                {
                    "id": "transcendental_decimal_gaps",
                    "severity": "medium",
                    "detail": unexpected,
                    "remedy": "Re-export transcendental_bounds.json or add decimal verify fallback",
                }
            )

    push_summary = pushback.get("summary") or {}
    if push_summary.get("domains_missing_uncertainty_metadata"):
        findings.append(
            {
                "id": "missing_literature_uncertainty",
                "severity": "low",
                "detail": pushback.get("missing_uncertainty_domains", [])[:5],
                "remedy": "Propagate literature_uncertainty_anchors via enrich_benchmark_scientific_metadata.py",
                "monitored": True,
            }
        )

    raw_eff_domains = push_summary.get("domains_raw_eff_divergence", 0)
    if raw_eff_domains:
        findings.append(
            {
                "id": "raw_vs_effective_error_divergence",
                "severity": "info",
                "detail": f"{raw_eff_domains} domains with literature-aware effective error diverging from raw %",
                "remedy": "Run enrich_benchmark_scientific_metadata.py; see scientific_pushback_audit.json",
                "monitored": True,
            }
        )
    structural = _load(REPORTS["structural"])
    if not structural.get("overall_ok"):
        findings.append(
            {
                "id": "norm_num_depth",
                "severity": "medium",
                "detail": structural.get("breakdown") or "structural proof spine not verified",
                "remedy": "Run generate_structural_proof_artifacts.py and audit_structural_proof_depth.py",
            }
        )

    verdict = depth.get("verdict") or {}
    undeniable = bool(verdict.get("undeniable_toe_claim")) and not any(
        f.get("severity") in ("high", "medium") and not f.get("monitored") for f in findings
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "tier": "deep_verification_audit_v1",
        "verdict": {
            "overall_ok": bool(cross.get("overall_ok")),
            "undeniable_toe_claim": undeniable,
            "cross_proof_overall_ok": bool(cross.get("overall_ok")),
            "extension_domains_all_green": verdict.get("extension_domains_all_green"),
            "transcendental_certificates_ok": verdict.get("transcendental_certificates_ok"),
            "export_gap_closed": verdict.get("export_gap_closed"),
            "honest_assessment": verdict.get("honest_assessment"),
        },
        "obligation_spine": {
            "connective": (cross.get("connective_spine") or {}).get("obligation_count"),
            "full_formal_total": (cross.get("full_formal_spine") or {}).get("obligation_count"),
            "full_formal_provable": (cross.get("full_formal_spine") or {}).get("provable_count"),
            "transcendental": (cross.get("transcendental_bounds") or {}).get("obligation_count"),
            "rust_replay_total": rust_actual,
            "rust_replay_expected": rust_expected,
            "rust_replay_formula": "connective + atomic_provable + transcendental (bundles/margins excluded)",
            "by_kind": (cross.get("full_formal_spine") or {}).get("by_kind"),
        },
        "triangulation": {
            "coq_atomic": coq_ref.get("triangulation"),
            "isabelle_atomic": isa_ref.get("triangulation"),
            "rust": {
                "connective_ok": rust_ref.get("connective_python_f64_ok"),
                "formal_ok": rust_ref.get("formal_python_f64_ok"),
                "transcendental_ok": rust_ref.get("transcendental_python_f64_ok"),
                "total": rust_meta.get("total_count"),
            },
            "fstar_checks": fstar_ref.get("checks"),
        },
        "margin_bundle_analysis": _margin_bundle_analysis(cross, coq_ref, bundle_ledger),
        "structural_bundle_ledger": bundle_ledger.get("summary") or {},
        "oracle_debt_ledger": oracle_ledger.get("summary") or {},
        "formula_corpus_honesty": formula_honesty.get("summary") or formula_honesty,
        "runtime_verification_scope": runtime_scope,
        "parameter_honesty_closure": parameter_closure.get("summary") or parameter_closure,
        "export_coverage": {
            "lean_theorem_count": export_reg.get("lean_theorem_count"),
            "exported_obligation_count": export_reg.get("exported_obligation_count"),
            "export_fraction_pct": export_reg.get("export_fraction_pct"),
            "by_reason": export_reg.get("by_reason"),
            "structural_bundle_excluded": (export_reg.get("by_reason") or {}).get("structural_bundle_theorem"),
        },
        "transcendental": {
            "certificate_audit_ok": trans_cert.get("overall_ok"),
            "gap_report_status": trans_gap.get("tier_83_status"),
            "native_coq_isabelle": (depth.get("proof_debt") or {}).get("transcendental_coq_isabelle"),
            **trans_gaps,
        },
        "extension_precision": {
            "domain_count": push_summary.get("extension_domain_count"),
            "green_gate_pass_count": push_summary.get("green_gate_pass_count"),
            "core_benchmark_green": margins.get("green_gate_pass_count"),
            "worst_scalar_max_pct": margins.get("worst_scalar_max_error_pct"),
        },
        "scientific_pushback": {
            "summary": push_summary,
            "stumped_observable_count": push_summary.get("stumped_observable_count"),
            "pushback_avenues_monitored": len(pushback.get("pushback_avenues") or []),
            "missing_uncertainty_domains": pushback.get("missing_uncertainty_domains", [])[:10],
            "raw_eff_divergence_domains": _raw_eff_divergence_summary(pushback),
        },
        "coverage_audit": {
            "full_formal_spine": coverage.get("full_formal_spine"),
            "export_exclusions": coverage.get("export_exclusions"),
            "triangulation_summary": coverage.get("triangulation_summary"),
        } if coverage else {},
        "structural_proof_depth": structural,
        "living_fsot_hardware": {
            "overall_ok": living_hw.get("overall_ok"),
            "checks_passed": living_hw.get("checks_passed"),
            "live_operational": living_hw.get("live_operational"),
            "scope": living_hw.get("scope"),
            "living_root": living_hw.get("living_root"),
        },
        "proof_debt": depth.get("proof_debt"),
        "open_gaps_from_depth_audit": open_gaps,
        "findings": findings,
        "source_reports": {k: str(v.relative_to(ROOT)) for k, v in REPORTS.items()},
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  overall_ok: {doc['verdict']['overall_ok']}")
    print(f"  undeniable ToE: {doc['verdict']['undeniable_toe_claim']}")
    print(f"  findings: {len(doc['findings'])}")
    print(f"  rust replay: {doc['obligation_spine']['rust_replay_total']} (expected {doc['obligation_spine']['rust_replay_expected']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())