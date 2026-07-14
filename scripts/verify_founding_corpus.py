#!/usr/bin/env python3
"""Verification gate: founding PDF ingest + 35-law audit must be present and fresh."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_MANIFEST = ROOT / "vendor" / "founding_corpus" / "pdf_ingest_manifest.json"
LAW_AUDIT = ROOT / "data" / "founding_law_audit.json"
OUT = ROOT / "data" / "founding_corpus_verification.json"


def verify() -> dict:
    issues: list[str] = []
    pdf_ok = False
    law_ok = False
    pdf_stats = {}
    law_stats = {}

    if PDF_MANIFEST.exists():
        pdf_stats = json.loads(PDF_MANIFEST.read_text(encoding="utf-8"))
        if pdf_stats.get("extracted_ok", 0) > 0:
            pdf_ok = True
        else:
            issues.append("pdf_manifest: no successful extractions")
    else:
        issues.append(f"missing {PDF_MANIFEST}")

    if LAW_AUDIT.exists():
        law_stats = json.loads(LAW_AUDIT.read_text(encoding="utf-8"))
        if law_stats.get("law_count", 0) >= 35:
            law_ok = True
        else:
            issues.append(f"law_audit: expected 35 laws, got {law_stats.get('law_count')}")
    else:
        issues.append(f"missing {LAW_AUDIT}")

    report = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "ok": pdf_ok and law_ok and not issues,
        "pdf_ingest_ok": pdf_ok,
        "law_audit_ok": law_ok,
        "pdf_stats": {
            "pdf_count": pdf_stats.get("pdf_count"),
            "extracted_ok": pdf_stats.get("extracted_ok"),
            "accuracy_flagged": pdf_stats.get("accuracy_flagged_pdfs"),
        },
        "law_stats": law_stats.get("status_counts"),
        "issues": issues,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    r = verify()
    print(json.dumps(r, indent=2))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())