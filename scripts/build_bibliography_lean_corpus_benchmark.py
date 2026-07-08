#!/usr/bin/env python3
"""FSOT Bibliography Lean corpus benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "bibliography_lean_corpus_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import bibliography_summary_path, rel_repo_path  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    summary = json.loads(bibliography_summary_path().read_text(encoding="utf-8"))
    records: list[dict] = []

    for key, expected in (
        ("constant_count", 9),
        ("theorem_count", 1),
        ("lemma_count", 1),
        ("def_count", 2),
        ("structure_count", 1),
        ("section_count", 3),
    ):
        val = int(summary.get(key) or 0)
        records.append(
            {
                "lab": "bibliography_lean_corpus",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    records.append(
        {
            "lab": "bibliography_lean_corpus",
            "property": "zero_free_parameters",
            "computed": 1 if summary.get("zero_free_parameters") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("zero_free_parameters") else 100.0,
        }
    )
    records.append(
        {
            "lab": "bibliography_lean_corpus",
            "property": "precision_mandate_pct",
            "computed": float(summary.get("precision_mandate_pct") or 0),
            "measured": 0.5,
            "error_pct": _err_pct(float(summary.get("precision_mandate_pct") or 0), 0.5),
        }
    )
    records.append(
        {
            "lab": "bibliography_lean_corpus",
            "property": "workflow_sequence_length",
            "computed": len(summary.get("workflow_sequence") or []),
            "measured": 4,
            "error_pct": 0.0 if len(summary.get("workflow_sequence") or []) == 4 else 100.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(bibliography_summary_path())],
        "maps_to_lean": ["particle", "mathematical"],
        "D_eff": 13,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())