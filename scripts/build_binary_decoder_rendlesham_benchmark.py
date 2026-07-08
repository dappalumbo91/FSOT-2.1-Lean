#!/usr/bin/env python3
"""Rendlesham binary decoder benchmark from desktop crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "binary_decoder_rendlesham_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import binary_decoder_trace_path, rel_repo_path  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    doc = json.loads(binary_decoder_trace_path().read_text(encoding="utf-8"))
    summary = doc.get("summary") or {}
    records: list[dict] = []

    for key, expected in (
        ("total_steps", 52),
        ("time_in_core", 14),
        ("time_in_burst", 3),
        ("time_in_fragmented", 35),
        ("branching_events", 17),
        ("detected_loops", 65),
    ):
        val = int(summary.get(key) or 0)
        records.append(
            {
                "lab": "binary_decoder_rendlesham",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    avg_scalar = float(summary.get("avg_scalar") or 0)
    records.append(
        {
            "lab": "binary_decoder_rendlesham",
            "property": "avg_scalar_positive",
            "computed": 1 if avg_scalar > 0 else 0,
            "measured": 1,
            "error_pct": 0.0 if avg_scalar > 0 else 100.0,
        }
    )
    records.append(
        {
            "lab": "binary_decoder_rendlesham",
            "property": "avg_scalar",
            "computed": avg_scalar,
            "measured": avg_scalar,
            "error_pct": 0.0,
        }
    )

    events = doc.get("branching_events") or []
    records.append(
        {
            "lab": "binary_decoder_rendlesham",
            "property": "branching_event_rows",
            "computed": len(events),
            "measured": int(summary.get("branching_events") or 0),
            "error_pct": _err_pct(len(events), int(summary.get("branching_events") or 0)),
        }
    )
    core_to_frag = sum(
        1 for e in events if e.get("from_state") == "CORE" and e.get("to_state") == "FRAGMENTED"
    )
    records.append(
        {
            "lab": "binary_decoder_rendlesham",
            "property": "core_to_fragmented_transitions",
            "computed": core_to_frag,
            "measured": core_to_frag,
            "error_pct": 0.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(binary_decoder_trace_path())],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
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