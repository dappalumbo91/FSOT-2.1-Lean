#!/usr/bin/env python3
"""Aggregate ALL verification gates into one comprehensive report."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "data" / "full_verification_report.json"

SOURCES: dict[str, Path] = {
    "toolchain_discovery": ROOT / "data" / "toolchain_discovery.json",
    "archive_portability": ROOT / "data" / "archive_portability_audit.json",
    "archive_independence": ROOT / "data" / "archive_independence_audit.json",
    "portable_vendor_coverage": ROOT / "data" / "portable_vendor_coverage_audit.json",
    "founding_corpus": ROOT / "data" / "founding_corpus_verification.json",
    "founding_law_audit": ROOT / "data" / "founding_law_audit.json",
    "founding_pdf_manifest": ROOT / "vendor" / "founding_corpus" / "pdf_ingest_manifest.json",
    "cross_proof_verification": ROOT / "data" / "cross_proof_verification_report.json",
    "cross_proof_coverage": ROOT / "data" / "cross_proof_coverage_audit.json",
    "benchmark_margin_audit": ROOT / "data" / "benchmark_margin_audit.json",
    "extension_scalar_precision_debt": ROOT / "data" / "extension_scalar_precision_debt.json",
    "domain_coverage": ROOT / "data" / "domain_coverage_report.json",
    "domain_precision": ROOT / "data" / "domain_precision_report.json",
    "verification_depth": ROOT / "data" / "verification_depth_audit.json",
    "numeric_eval_queue": ROOT / "data" / "numeric_eval_queue_report.json",
    "sota_observable_ledger": ROOT / "data" / "sota_observable_ledger_report.json",
}


def _load(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_error": "invalid json"}


def _summarize_cross_proof(doc: dict | None) -> dict:
    if not doc:
        return {"present": False}
    fw = doc.get("frameworks") or {}
    framework_status = {k: (v.get("status") if isinstance(v, dict) else v) for k, v in fw.items()}
    ff = doc.get("full_formal_spine") or {}
    return {
        "present": True,
        "overall_ok": doc.get("overall_ok"),
        "tier": doc.get("tier"),
        "seven_way_bare_metal": doc.get("seven_way_bare_metal"),
        "eight_way_hardware": doc.get("eight_way_hardware"),
        "full_triangulation": doc.get("full_triangulation"),
        "obligation_count": ff.get("obligation_count"),
        "provable_count": ff.get("provable_count"),
        "atomic_provable_count": ff.get("atomic_provable_count"),
        "modules_exported": ff.get("modules_exported"),
        "margin_violation_count": ff.get("margin_violation_count"),
        "framework_status": framework_status,
    }


def _summarize_founding(law: dict | None, pdf: dict | None, corpus: dict | None) -> dict:
    return {
        "corpus_ok": (corpus or {}).get("ok"),
        "pdf_count": (pdf or {}).get("pdf_count"),
        "extracted_ok": (pdf or {}).get("extracted_ok"),
        "failed_pdfs": (pdf or {}).get("failed"),
        "law_count": (law or {}).get("law_count"),
        "status_counts": (law or {}).get("status_counts"),
        "founding_unmapped": (corpus or {}).get("founding_unmapped"),
    }


def _summarize_extension(vendor: dict | None, debt: dict | None, margins: dict | None) -> dict:
    v = vendor or {}
    return {
        "extension_domain_count": v.get("extension_domain_count"),
        "all_benchmarks_present": v.get("all_extension_benchmarks_present"),
        "all_bundled_present": v.get("all_bundled_assets_present"),
        "missing_benchmarks": v.get("missing_benchmark_domains", []),
        "missing_bundled": v.get("missing_bundled_assets", []),
        "formula_corpus_records": v.get("formula_corpus_records_hint"),
        "precision_debt_domains": len((debt or {}).get("domains_over_half_pct", []) or []),
        "strict_margin_failures": (margins or {}).get("strict_scalar_max_failures", []),
    }


def build() -> dict:
    loaded = {k: _load(p) for k, p in SOURCES.items()}
    toolchain = loaded.get("toolchain_discovery") or {}
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "toolchain": {
            "all_seven_way_present": toolchain.get("all_seven_way_present"),
            "tools": toolchain.get("tools"),
            "bundled_toolchain_on_drive": toolchain.get("bundled_toolchain_root"),
        },
        "archive": {
            "portability_ok": (loaded.get("archive_portability") or {}).get("ok"),
            "independence_ok": (loaded.get("archive_independence") or {}).get("ok"),
            "plug_and_play": (loaded.get("archive_portability") or {}).get("plug_and_play"),
        },
        "founding_corpus": _summarize_founding(
            loaded.get("founding_law_audit"),
            loaded.get("founding_pdf_manifest"),
            loaded.get("founding_corpus"),
        ),
        "extension_domains": _summarize_extension(
            loaded.get("portable_vendor_coverage"),
            loaded.get("extension_scalar_precision_debt"),
            loaded.get("benchmark_margin_audit"),
        ),
        "cross_proof": _summarize_cross_proof(loaded.get("cross_proof_verification")),
        "numeric_eval": {
            "strict_empirical_pending": (loaded.get("numeric_eval_queue") or {}).get(
                "strict_empirical_pending_numeric"
            ),
            "records_total": (loaded.get("numeric_eval_queue") or {}).get("records_total"),
        },
        "domain_coverage_tiers": (loaded.get("domain_coverage") or {}).get("tier_counts"),
        "verification_depth": loaded.get("verification_depth"),
        "sota_ledger": loaded.get("sota_observable_ledger"),
        "sources_present": {k: (loaded[k] is not None) for k in SOURCES},
        "raw_paths": {k: str(p) for k, p in SOURCES.items()},
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())