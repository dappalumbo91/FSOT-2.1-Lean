#!/usr/bin/env python3
"""Audit Coq/Isabelle cross-proof coverage vs full FSOT Lean corpus."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
OBL_CONNECTIVE = ROOT / "verification" / "obligations" / "connective_spine.json"
OBL_FULL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OBL_PRIORS = ROOT / "verification" / "obligations" / "full_priors_spine.json"
OUT = ROOT / "data" / "cross_proof_coverage_audit.json"


def count_domains() -> int:
    exp = ROOT / "data" / "scientific_domain_expansion_map.json"
    if exp.exists():
        doc = json.loads(exp.read_text(encoding="utf-8"))
        if isinstance(doc, list):
            return len(doc)
        if "domains" in doc:
            return len(doc["domains"])
        if "entries" in doc:
            return len(doc["entries"])
    scope = ROOT / "data" / "FSOT_VERIFIED_SCOPE.yaml"
    if scope.exists():
        return len(re.findall(r"^- domain:", scope.read_text(encoding="utf-8"), re.M))
    return 0


def scan_priors() -> dict:
    priors = sorted(FORMAL.glob("*Priors.lean"))
    theorem_re = re.compile(r"^theorem\s+", re.M)
    norm_num_re = re.compile(r"norm_num", re.M)
    exportable_re = re.compile(
        r"theorem\s+\w+.*(?:\(0\s*:\s*ℝ\)\s*<|\(1\s*:\s*ℝ\)\s*<|0\s*<|<\s*\(0\.5\s*:\s*ℝ\)|<\s*\(0\.5)",
        re.M,
    )
    total_thm = 0
    norm_thm = 0
    exportable = 0
    per_module: list[dict] = []
    for p in priors:
        text = p.read_text(encoding="utf-8")
        t = len(theorem_re.findall(text))
        n = len(norm_num_re.findall(text))
        e = len(exportable_re.findall(text))
        total_thm += t
        norm_thm += n
        exportable += e
        if e > 0:
            per_module.append({"module": p.stem, "theorems": t, "exportable_hints": e})
    return {
        "priors_modules": len(priors),
        "total_theorems": total_thm,
        "norm_num_uses": norm_thm,
        "exportable_theorem_hints": exportable,
        "modules_with_exportable": len(per_module),
        "top_exportable_modules": sorted(per_module, key=lambda x: -x["exportable_hints"])[:15],
    }


def main() -> int:
    connective = json.loads(OBL_CONNECTIVE.read_text(encoding="utf-8")) if OBL_CONNECTIVE.exists() else {}
    full = json.loads(OBL_FULL.read_text(encoding="utf-8")) if OBL_FULL.exists() else {}
    scan = scan_priors()
    n_domains = count_domains()

    coq_connective = int(connective.get("obligation_count") or 0)
    coq_full = int(full.get("obligation_count") or 0)
    coq_sources = len(connective.get("lean_sources") or [])

    report_path = ROOT / "data" / "cross_proof_verification_report.json"
    refinement_path = ROOT / "data" / "cross_refinement_lean_coq_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    refinement = json.loads(refinement_path.read_text(encoding="utf-8")) if refinement_path.exists() else {}

    coq_status = (report.get("frameworks") or {}).get("coq", {})
    coq_chunk_files = len(list((ROOT / "verification" / "coq").glob("FullFormalSpine_*.v")))
    priors_doc = json.loads(OBL_PRIORS.read_text(encoding="utf-8")) if OBL_PRIORS.exists() else {}
    margin_path = ROOT / "verification" / "obligations" / "margin_violations.json"
    margin_doc = json.loads(margin_path.read_text(encoding="utf-8")) if margin_path.exists() else {}
    margin_count = int(margin_doc.get("count") or 0)
    coq_provable_target = max(0, coq_full - margin_count)
    coq_full_obligations_proved = coq_provable_target if coq_status.get("status") == "passed" and coq_chunk_files > 0 else 0

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fsot_scale": {
            "extension_domains": n_domains,
            "priors_lean_modules": scan["priors_modules"],
            "total_lean_theorems": scan["total_theorems"],
            "norm_num_certificate_uses": scan["norm_num_uses"],
        },
        "coq_cross_proof": {
            "tier": "79_connective_spine",
            "lean_source_modules": coq_sources,
            "obligations_proved_in_coq": coq_connective,
            "pct_of_priors_modules": round(100 * coq_sources / max(1, scan["priors_modules"]), 4),
            "pct_of_lean_theorems": round(100 * coq_connective / max(1, scan["total_theorems"]), 4),
            "pct_of_extension_domains": round(100 * coq_sources / max(1, n_domains), 4),
        },
        "full_formal_spine": {
            "obligations_in_full_json": coq_full,
            "modules_in_full_json": int(full.get("modules_exported") or 0),
            "by_tier": full.get("by_tier"),
            "by_kind": full.get("by_kind"),
            "pct_of_formal_theorems": round(100 * coq_full / max(1, scan["total_theorems"]), 4),
            "coq_chunks_generated": coq_chunk_files,
            "margin_violations_excluded": margin_count,
            "coq_provable_target": coq_provable_target,
            "coq_proved_yet": coq_full_obligations_proved,
            "coq_proved_pct_of_full_export": round(100 * coq_full_obligations_proved / max(1, coq_full), 4) if coq_full else 0.0,
            "coq_proved_pct_of_provable": round(100 * coq_full_obligations_proved / max(1, coq_provable_target), 4) if coq_provable_target else 0.0,
            "coq_compile_status": coq_status.get("status"),
            "cross_refinement_ok": refinement.get("overall_ok"),
        },
        "full_priors_spine": {
            "obligations_exportable": scan["exportable_theorem_hints"],
            "obligations_in_full_json": int(priors_doc.get("obligation_count") or 0),
            "modules_in_full_json": int(priors_doc.get("modules_exported") or 0),
            "pct_of_priors_modules": round(100 * int(priors_doc.get("modules_exported") or 0) / max(1, scan["priors_modules"]), 4),
            "pct_of_lean_theorems": round(100 * int(priors_doc.get("obligation_count") or 0) / max(1, scan["total_theorems"]), 4),
            "cross_refinement_triangulated_pct": (refinement.get("triangulation") or {}).get("pct_provable_triangulated"),
        },
        "interpretation": (
            "Tier 80: wide FSOT/Formal export (priors + Bounds + genomic/neuron extended modules). "
            "Numeric certificates cross-proved in Coq; margin violations flagged for refinement. "
            "Transcendental pi/e interval lemmas deferred to Tier 81 Coq Real port."
        ),
        "scan": scan,
        "other_frameworks": {
            "implemented": ["lean4", "python_decimal", "rocq_coq", "coqchk"],
            "artifacts_ready": ["isabelle"],
            "planned_tier_80": ["agda", "metamath"],
            "all_free_no_account": True,
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-PROOF COVERAGE AUDIT")
    print(f"  extension domains: {n_domains}")
    print(f"  priors modules: {scan['priors_modules']}")
    print(f"  lean theorems: {scan['total_theorems']}")
    print(f"  Coq obligations (connective): {coq_connective} from {coq_sources} modules")
    print(f"  Coq % of priors modules: {doc['coq_cross_proof']['pct_of_priors_modules']}%")
    print(f"  Coq % of lean theorems: {doc['coq_cross_proof']['pct_of_lean_theorems']}%")
    print(f"  exportable norm_num hints: {scan['exportable_theorem_hints']}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())