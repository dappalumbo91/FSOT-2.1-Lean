#!/usr/bin/env python3
"""Rust no_std bare-metal → Lean bridge benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "rust_lean_bridge_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import (  # noqa: E402
    rel_repo_path,
    rust_lean_bridge_summary_path,
    vl_distill_atlas_summary_path,
)


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    summary = json.loads(rust_lean_bridge_summary_path().read_text(encoding="utf-8"))
    atlas = json.loads(vl_distill_atlas_summary_path().read_text(encoding="utf-8"))
    records: list[dict] = []

    for key, expected in (
        ("boot_d_eff", 8),
        ("constant_count", 16),
    ):
        val = float(summary.get(key) or 0) if key == "boot_d_eff" else int(summary.get(key) or 0)
        records.append(
            {
                "lab": "rust_lean_bridge",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    k_rust = float(summary.get("K") or 0)
    k_atlas = float(atlas.get("K_FSOT") or summary.get("atlas_K_FSOT") or 0)
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "K_matches_atlas",
            "computed": 1 if abs(k_rust - k_atlas) < 1e-12 else 0,
            "measured": 1,
            "error_pct": 0.0 if abs(k_rust - k_atlas) < 1e-12 else 100.0,
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "boot_scalar_positive",
            "computed": 1 if summary.get("boot_scalar_positive") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("boot_scalar_positive") else 100.0,
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "boot_scalar",
            "computed": float(summary.get("boot_scalar") or 0),
            "measured": 0.09928895626861721,
            "error_pct": _err_pct(float(summary.get("boot_scalar") or 0), 0.09928895626861721),
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "no_std",
            "computed": 1 if summary.get("no_std") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("no_std") else 100.0,
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "requires_lean_bridge",
            "computed": 1 if summary.get("requires_lean_bridge") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("requires_lean_bridge") else 100.0,
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "boot_observed",
            "computed": 1 if summary.get("boot_observed") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("boot_observed") else 100.0,
        }
    )
    records.append(
        {
            "lab": "rust_lean_bridge",
            "property": "boot_delta_psi",
            "computed": float(summary.get("boot_delta_psi") or 0),
            "measured": 0.7,
            "error_pct": _err_pct(float(summary.get("boot_delta_psi") or 0), 0.7),
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(rust_lean_bridge_summary_path())],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 8,
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