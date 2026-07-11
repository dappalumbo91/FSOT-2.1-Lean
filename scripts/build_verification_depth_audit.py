#!/usr/bin/env python3
"""Honest multi-prover verification depth audit — gaps, precision parity, proof debt."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "verification_depth_audit.json"
CROSS_REPORT = ROOT / "data" / "cross_proof_verification_report.json"
EXTENSION_DEBT = ROOT / "data" / "extension_scalar_precision_debt.json"
PUSHBACK_AUDIT = ROOT / "data" / "scientific_pushback_audit.json"
MARGIN_AUDIT = ROOT / "data" / "benchmark_margin_audit.json"
EXPORT_REGISTRY = ROOT / "data" / "export_exclusion_registry.json"
TRANSCENDENTAL_AUDIT = ROOT / "data" / "transcendental_certificate_audit.json"
HONEST_CLAIMS = ROOT / "data" / "honest_claims_manifest.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import analyze_benchmark  # noqa: E402
from fsot_label_registry_lib import humanize_domain_key  # noqa: E402
from scientific_measurement_lib import domain_precision_summary  # noqa: E402


def _yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _count_lean_theorems() -> int:
    formal = ROOT / "FSOT" / "Formal"
    if not formal.exists():
        return 0
    count = 0
    for path in formal.glob("*.lean"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        count += text.count("theorem ") + text.count("lemma ")
    return count


def _extension_precision_parity() -> list[dict]:
    manifest = _yaml(ROOT / "data" / "extension_domains_manifest.yaml")
    rows: list[dict] = []
    for name, cfg in (manifest.get("extension_domains") or {}).items():
        rel = cfg.get("benchmark_data")
        if not rel:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        recs = doc.get("material_records") or doc.get("records") or []
        margin = analyze_benchmark(doc, file_name=path.name)
        sci = domain_precision_summary(recs)
        rows.append(
            {
                "domain": name,
                "display_name": humanize_domain_key(name),
                "tier": cfg.get("tier"),
                "classifier_accuracy_pct": margin.get("classifier_accuracy_pct"),
                "max_scalar_error_pct": margin.get("max_scalar_error_pct"),
                "max_effective_scalar_error_pct": margin.get("max_effective_scalar_error_pct"),
                "median_error_pct": margin.get("official_pooled_median_error_pct"),
                "green_gate_pass": margin.get("green_gate_pass"),
                "matches_domain_spine": sci.get("matches_domain_spine"),
                "precision_tier_counts": sci.get("precision_tier_counts"),
            }
        )
    return sorted(rows, key=lambda r: (not r.get("green_gate_pass"), -(r.get("max_scalar_error_pct") or 0)))


def build() -> dict:
    cross = json.loads(CROSS_REPORT.read_text(encoding="utf-8")) if CROSS_REPORT.exists() else {}
    debt = json.loads(EXTENSION_DEBT.read_text(encoding="utf-8")) if EXTENSION_DEBT.exists() else {}
    lean_theorems = _count_lean_theorems()
    formal_ob = cross.get("full_formal_spine", {}).get("obligation_count", 0)
    export_pct = round(100.0 * formal_ob / lean_theorems, 2) if lean_theorems else None

    proof_debt = cross.get("proof_debt") or {}
    frameworks = cross.get("frameworks") or {}

    prover_coverage = {
        "lean_4": {
            "role": "primary authority",
            "connective_obligations": cross.get("connective_spine", {}).get("obligation_count", 0),
            "full_formal_obligations": formal_ob,
            "transcendental_lemmas": cross.get("transcendental_bounds", {}).get("obligation_count", 0),
            "lean_theorem_count_estimate": lean_theorems,
            "export_fraction_pct": export_pct,
            "proof_style": "norm_num / decide / linarith certificates",
        },
        "coq": {
            "status": (frameworks.get("coq") or {}).get("status"),
            "chunks_passed": (frameworks.get("coq") or {}).get("chunks_passed"),
            "coverage": "numeric literal replay of exported obligations",
            "axiom_debt": proof_debt.get("transcendental_coq_isabelle"),
        },
        "isabelle": {
            "status": (frameworks.get("isabelle") or {}).get("status"),
            "provable_obligations": (frameworks.get("isabelle") or {}).get("provable_obligations"),
            "coverage": "numeric literal replay of exported obligations",
        },
        "rust_f64_replay": {
            "status": (frameworks.get("rust_replay") or {}).get("status"),
            "obligation_count": (frameworks.get("rust_replay") or {}).get("obligation_count"),
            "note": "Includes connective (24) + formal (1241) + transcendental (68) after Tier 84 update",
        },
        "fstar": {
            "status": (frameworks.get("fstar") or {}).get("status"),
            "scope": "boot scalar kernel only",
            "assume_debt": proof_debt.get("fstar_transcendental_assumes"),
        },
        "esp32_qemu": {
            "status": (frameworks.get("esp32_harness") or {}).get("status"),
            "scope": "single boot scalar UART parity",
        },
    }

    export_reg = json.loads(EXPORT_REGISTRY.read_text(encoding="utf-8")) if EXPORT_REGISTRY.exists() else {}
    transcendental = (
        json.loads(TRANSCENDENTAL_AUDIT.read_text(encoding="utf-8")) if TRANSCENDENTAL_AUDIT.exists() else {}
    )
    transcendental_ok = bool(transcendental.get("overall_ok"))
    bundle_exported = int((cross.get("full_formal_spine") or {}).get("by_kind", {}).get("bundle_conj", 0))
    structural_bundle_left = int((export_reg.get("by_reason") or {}).get("structural_bundle_theorem", 0))
    fstar_report = json.loads(
        (ROOT / "data" / "cross_refinement_fstar_report.json").read_text(encoding="utf-8")
    ) if (ROOT / "data" / "cross_refinement_fstar_report.json").exists() else {}
    fstar_no_assumes = bool((fstar_report.get("checks") or {}).get("fstar_no_transcendental_assumes"))
    native_transcendental = proof_debt.get("transcendental_coq_isabelle") in (
        "native_pi_e_interval_proofs",
        "coq_native_isabelle_certified_intervals",
        "coq_native_isabelle_native_intervals",
    )

    gaps = [
        {
            "id": "export_gap",
            "severity": "medium",
            "description": f"~{100 - (export_pct or 0):.1f}% of Lean theorems not exported as cross-proof obligations",
            "remedy": "See data/export_exclusion_registry.json; extend export or document exclusions",
            "closed": structural_bundle_left <= 6 and bundle_exported >= 300,
        },
        {
            "id": "fstar_assumes",
            "severity": "low",
            "description": "F* boot kernel uses oracle literals at POC transcendental sites; readout aliases canonical",
            "remedy": "Kernel expansion triangulated in cross_refinement_fstar_report.json",
            "closed": fstar_no_assumes,
        },
        {
            "id": "transcendental_axioms",
            "severity": "medium",
            "description": "Coq/Isabelle π/e base intervals",
            "remedy": "Coq TranscendentalBoundsNative.v + Isabelle TranscendentalBoundsNative.thy (approximation)",
            "closed": native_transcendental and transcendental_ok,
        },
        {
            "id": "rust_report_stale",
            "severity": "low",
            "description": "cross_proof_verification_report.json may lag rust_replay_lib until full pipeline re-run",
            "remedy": "Re-run run_cross_proof_verification.py to refresh obligation_count to 1333",
        },
        {
            "id": "hardware_scalar_only",
            "severity": "info",
            "description": "ESP32/QEMU verifies one boot scalar, not 1,241-obligation spine",
            "remedy": "Refinement chain: F* spec → Rust no_std → ESP32 binary hash",
        },
        {
            "id": "norm_num_depth",
            "severity": "medium",
            "description": "Cross-proof replays numeric inequalities, not deep Mathlib proof chains",
            "remedy": "Structural theorem export with independent Coq/Isabelle proof scripts",
        },
    ]

    extension_rows = _extension_precision_parity()
    failing = [r for r in extension_rows if not r.get("green_gate_pass")]
    aspiration_debt = debt.get("aspiration_debt") or debt.get("domains") or []
    aspiration_count = int(debt.get("aspiration_debt_count", len(aspiration_debt)))
    pushback = json.loads(PUSHBACK_AUDIT.read_text(encoding="utf-8")) if PUSHBACK_AUDIT.exists() else {}
    margin = json.loads(MARGIN_AUDIT.read_text(encoding="utf-8")) if MARGIN_AUDIT.exists() else {}
    core_benchmark_failures = margin.get("green_gate_fail_count", 0) or 0
    export_fraction = export_reg.get("export_fraction_pct") or export_pct
    no_proof_cert_count = int((export_reg.get("by_reason") or {}).get("no_proof_certificate_in_module", 0))
    cross_ok = bool(cross.get("overall_ok"))
    extension_green = len(failing) == 0
    aspiration_cleared = aspiration_count == 0
    core_benchmarks_green = core_benchmark_failures == 0
    fixable_export_gaps = int((export_reg.get("by_reason") or {}).get("no_proof_certificate_in_module", 0))
    export_gap_closed = fixable_export_gaps == 0

    undeniable = (
        cross_ok
        and extension_green
        and aspiration_cleared
        and core_benchmarks_green
        and transcendental_ok
        and export_gap_closed
    )

    honest = (
        "Strong numeric literal triangulation across Lean/Coq/Isabelle/Python/Rust "
        "for exported obligations. Literature-aware aspiration debt cleared at "
        f"{aspiration_count} domains. NOT full-depth independent proof of entire "
        "FSOT theory in all four provers. Stumped observables tracked in "
        "scientific_pushback_audit.json."
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "verdict": {
            "cross_proof_overall_ok": cross_ok,
            "extension_domains_all_green": extension_green,
            "aspiration_scalar_debt_cleared": aspiration_cleared,
            "core_benchmarks_all_green": core_benchmarks_green,
            "core_benchmark_fail_count": core_benchmark_failures,
            "transcendental_certificates_ok": transcendental_ok,
            "export_gap_closed": export_gap_closed,
            "export_fraction_pct": export_fraction,
            "no_proof_certificate_module_count": no_proof_cert_count,
            "undeniable_toe_claim": undeniable,
            "honest_assessment": honest,
        },
        "prover_coverage": prover_coverage,
        "proof_debt": proof_debt,
        "gaps": gaps,
        "extension_precision": {
            "domain_count": len(extension_rows),
            "green_count": sum(1 for r in extension_rows if r.get("green_gate_pass")),
            "failing_domains": failing,
            "aspiration_scalar_debt_count": aspiration_count,
        },
        "scientific_pushback_audit": pushback.get("summary") or {},
        "pushback_avenues": pushback.get("pushback_avenues") or [],
        "scientific_measurement_policy": {
            "green_median_gate_pct": 0.5,
            "green_scalar_gate_pct": 2.0,
            "aspiration_scalar_pct": 0.5,
            "fields": ["delta", "delta_pct", "sigma_equivalent", "precision_tier", "reference_uncertainty_pct"],
            "library": "scripts/scientific_measurement_lib.py",
        },
        "label_registry": {
            "path": "data/fsot_label_registry.json",
            "builder": "scripts/build_fsot_label_registry.py",
            "purpose": "Resolve FO-200, PRED-001, tier numbers, obligation ids to human text",
        },
        "roadmap_to_undeniable": [
            "Close remaining Lean export exclusions (extended_formal, non-exportable markers)",
            "Independent deep proofs beyond norm_num/lra replay",
            "Propagate display_label to all benchmark exports and obligation JSON",
            "Attach scientific_measurement envelope (σ, Δ) to every scalar record",
        ],
        "open_gaps": [g for g in gaps if not g.get("closed")],
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  extension green: {doc['extension_precision']['green_count']}/{doc['extension_precision']['domain_count']}")
    print(f"  undeniable ToE: {doc['verdict']['undeniable_toe_claim']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())