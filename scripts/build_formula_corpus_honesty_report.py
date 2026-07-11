#!/usr/bin/env python3
"""Publish formula corpus row vs unique-observable honesty report."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "formula_corpus_honesty_report.json"

sys.path.insert(0, str(ROOT / "scripts"))
from verify_formula_corpus import verify_formula_corpus  # noqa: E402


def build() -> dict:
    issues, summary = verify_formula_corpus()
    total = int(summary.get("records_total") or 0)
    unique = int(summary.get("unique_observables") or 0)
    factor = round(total / unique, 3) if unique else 1.0
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "verdict": "ROW_COUNT_WITH_DEDUPED_UNIQUE" if factor > 1.1 else "UNIQUE_OBSERVABLE_COUNT",
        "headline_row_count": total,
        "unique_observable_count": unique,
        "project_triplication_factor": factor,
        "live_recompute": {
            "enabled": summary.get("live_recompute_deduped"),
            "sample_size": summary.get("live_recompute_sample_size"),
            "checked": summary.get("live_recompute_checked"),
            "ok": summary.get("live_recompute_ok"),
            "ok_ratio": summary.get("live_recompute_ok_ratio"),
            "drift_debt_count": summary.get("live_recompute_drift_debt_count"),
        },
        "honest_statement": (
            f"strict_empirical.jsonl contains {total:,} rows representing "
            f"{unique:,} unique observables (concept+formula+target); "
            f"~{factor}× project triplication. Live recompute runs on deduped "
            f"unique observables ({summary.get('live_recompute_ok', 0)}/"
            f"{summary.get('live_recompute_checked', 0)} OK)."
        ),
        "verification_issues": issues,
        "verification_passed": len(issues) == 0,
        "full_summary": summary,
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  rows={doc['headline_row_count']} unique={doc['unique_observable_count']} factor={doc['project_triplication_factor']}")
    return 0 if doc["verification_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())