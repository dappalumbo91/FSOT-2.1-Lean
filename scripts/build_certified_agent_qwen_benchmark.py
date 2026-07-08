#!/usr/bin/env python3
"""Qwen certified formal agent benchmark from desktop crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "certified_agent_qwen_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import (  # noqa: E402
    certified_agent_summary_path,
    certified_agent_workspace_path,
    rel_repo_path,
)


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    summary = json.loads(certified_agent_summary_path().read_text(encoding="utf-8"))
    workspace = json.loads(certified_agent_workspace_path().read_text(encoding="utf-8"))
    records: list[dict] = []

    for key, expected in (
        ("promotion_threshold_percent", 2.0),
        ("max_tool_iterations", 10),
        ("max_rag_results", 8),
    ):
        val = float(summary.get(key) or workspace.get(key) or 0)
        records.append(
            {
                "lab": "certified_agent_qwen",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": _err_pct(val, expected),
            }
        )

    paths = workspace.get("paths") or {}
    records.append(
        {
            "lab": "certified_agent_qwen",
            "property": "configured_path_count",
            "computed": len(paths),
            "measured": int(summary.get("configured_path_count") or len(paths)),
            "error_pct": _err_pct(len(paths), int(summary.get("configured_path_count") or len(paths))),
        }
    )
    records.append(
        {
            "lab": "certified_agent_qwen",
            "property": "protocol_version_match",
            "computed": 1 if str(summary.get("protocol_version")) == "1.1" else 0,
            "measured": 1,
            "error_pct": 0.0 if str(summary.get("protocol_version")) == "1.1" else 100.0,
        }
    )
    records.append(
        {
            "lab": "certified_agent_qwen",
            "property": "requires_lean_bridge",
            "computed": 1 if summary.get("requires_lean_bridge") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("requires_lean_bridge") else 100.0,
        }
    )
    records.append(
        {
            "lab": "certified_agent_qwen",
            "property": "no_probabilistic_math",
            "computed": 1 if summary.get("no_probabilistic_math") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("no_probabilistic_math") else 100.0,
        }
    )
    records.append(
        {
            "lab": "certified_agent_qwen",
            "property": "certification_requires_compiler_verified",
            "computed": 1 if summary.get("certification_requires_compiler_verified") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("certification_requires_compiler_verified") else 100.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [
            rel_repo_path(certified_agent_summary_path()),
            rel_repo_path(certified_agent_workspace_path()),
        ],
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