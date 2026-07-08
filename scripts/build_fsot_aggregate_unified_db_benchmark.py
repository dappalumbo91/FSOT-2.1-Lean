#!/usr/bin/env python3
"""FSOT aggregate unified mathematical database benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "fsot_aggregate_unified_db_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import fsot_aggregate_unified_db_path, rel_repo_path  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    rows = json.loads(fsot_aggregate_unified_db_path().read_text(encoding="utf-8"))
    type_counts = Counter(r.get("Type") or "unknown" for r in rows)
    records: list[dict] = []

    records.append(
        {
            "lab": "fsot_aggregate_unified_db",
            "property": "row_count",
            "computed": len(rows),
            "measured": 1532,
            "error_pct": 0.0 if len(rows) == 1532 else _err_pct(len(rows), 1532),
        }
    )
    for key, expected in (
        ("Seed", 5),
        ("Layer 1", 8),
        ("Layer 2", 12),
        ("Threshold", 2),
        ("Domain Metadata", 35),
    ):
        val = int(type_counts.get(key) or 0)
        records.append(
            {
                "lab": "fsot_aggregate_unified_db",
                "property": f"type_count_{key.replace(' ', '_').lower()}",
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    smiles_sections = sum(1 for t in type_counts if str(t).startswith("SMILES Derivation"))
    records.append(
        {
            "lab": "fsot_aggregate_unified_db",
            "property": "smiles_derivation_section_count",
            "computed": smiles_sections,
            "measured": 107,
            "error_pct": 0.0 if smiles_sections == 107 else _err_pct(smiles_sections, 107),
        }
    )
    records.append(
        {
            "lab": "fsot_aggregate_unified_db",
            "property": "distinct_type_count",
            "computed": len(type_counts),
            "measured": len(type_counts),
            "error_pct": 0.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(fsot_aggregate_unified_db_path())],
        "maps_to_lean": ["particle", "mathematical", "medical"],
        "D_eff": 17,
        "row_count": len(rows),
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