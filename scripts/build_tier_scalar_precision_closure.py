#!/usr/bin/env python3
"""Tier-scalar precision closure report — pooled median ≤0.05% gate."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "tier_scalar_precision_closure.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"

sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import analyze_benchmark  # noqa: E402
from fsot_precision_constants import TIER_SCALAR_MAX_ERROR_PCT  # noqa: E402


def build() -> dict:
    margin = json.loads(MARGIN.read_text(encoding="utf-8")) if MARGIN.exists() else {}
    rows = margin.get("all_domains") or []
    fails = [
        r
        for r in rows
        if not r.get("excluded") and r.get("scalar_count", 0) > 0 and not r.get("tier_scalar_pass")
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "gate": f"pooled_scalar_median_or_effective_median <= {TIER_SCALAR_MAX_ERROR_PCT}%",
        "tier_scalar_max_record_gate_pct": TIER_SCALAR_MAX_ERROR_PCT,
        "benchmark_file_count": margin.get("benchmark_file_count"),
        "tier_scalar_pass_count": (margin.get("benchmark_file_count") or 0)
        - int(margin.get("tier_scalar_fail_count") or 0),
        "tier_scalar_fail_count": len(fails),
        "closed": len(fails) == 0,
        "failing_domains": [
            {
                "domain": r.get("domain"),
                "file": r.get("file"),
                "scalar_pooled_median_error_pct": r.get("scalar_pooled_median_error_pct"),
                "effective_scalar_median_error_pct": r.get("effective_scalar_median_error_pct"),
                "max_scalar_error_pct": r.get("max_scalar_error_pct"),
            }
            for r in fails
        ],
        "honest_statement": (
            "tier_scalar_pass uses pooled scalar median (or literature-aware effective median) "
            f"≤ {TIER_SCALAR_MAX_ERROR_PCT}%, aligned with fsot_precision_constants tier aspiration. "
            "Per-record max up to 0.5% remains the green_gate strict_scalar bound."
        ),
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  tier_scalar closed={doc['closed']} fails={doc['tier_scalar_fail_count']}")
    return 0 if doc["closed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())