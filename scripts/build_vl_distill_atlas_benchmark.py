#!/usr/bin/env python3
"""VL distill atlas + domain registry benchmark from desktop crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "vl_distill_atlas_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import (  # noqa: E402
    rel_repo_path,
    vl_distill_atlas_summary_path,
    vl_distill_competitive_report_path,
    vl_distill_dataset_meta_path,
    vl_distill_domain_registry_path,
)


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    atlas = json.loads(vl_distill_atlas_summary_path().read_text(encoding="utf-8"))
    registry = json.loads(vl_distill_domain_registry_path().read_text(encoding="utf-8"))
    meta = json.loads(vl_distill_dataset_meta_path().read_text(encoding="utf-8"))
    competitive = json.loads(vl_distill_competitive_report_path().read_text(encoding="utf-8"))
    records: list[dict] = []

    for key, expected in (
        ("anchor_count", 10),
        ("unit_families", 9),
    ):
        val = atlas.get(key)
        if key == "unit_families":
            val = len(val or [])
        else:
            val = int(val or 0)
        records.append(
            {
                "lab": "vl_distill_atlas",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    k_fsot = float(atlas.get("K_FSOT") or 0)
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "K_FSOT",
            "computed": k_fsot,
            "measured": 0.4202216641606967,
            "error_pct": _err_pct(k_fsot, 0.4202216641606967),
        }
    )

    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "domain_registry_count",
            "computed": int(registry.get("domain_count") or len(registry.get("domains") or [])),
            "measured": 35,
            "error_pct": 0.0
            if int(registry.get("domain_count") or 0) == 35
            else _err_pct(int(registry.get("domain_count") or 0), 35),
        }
    )
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "distill_golden_rows",
            "computed": int(meta.get("golden_rows") or 0),
            "measured": 1500,
            "error_pct": _err_pct(int(meta.get("golden_rows") or 0), 1500),
        }
    )
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "distill_theorem_count",
            "computed": int(meta.get("theorem_count") or 0),
            "measured": 37,
            "error_pct": _err_pct(int(meta.get("theorem_count") or 0), 37),
        }
    )
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "harness_aligned",
            "computed": 1 if meta.get("harness_aligned") else 0,
            "measured": 1,
            "error_pct": 0.0 if meta.get("harness_aligned") else 100.0,
        }
    )

    stats = competitive.get("stats") or {}
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "competitive_targets",
            "computed": int(stats.get("targets") or 0),
            "measured": 22,
            "error_pct": _err_pct(int(stats.get("targets") or 0), 22),
        }
    )
    records.append(
        {
            "lab": "vl_distill_atlas",
            "property": "competitive_promoted_verified",
            "computed": int(stats.get("promoted_verified") or 0),
            "measured": 3,
            "error_pct": _err_pct(int(stats.get("promoted_verified") or 0), 3),
        }
    )

    sample_maps = atlas.get("sample_fractal_maps") or []
    if sample_maps:
        ratio = float(sample_maps[0].get("ratio") or 0)
        records.append(
            {
                "lab": "vl_distill_atlas",
                "property": "alpha_em_inverse_ratio",
                "computed": ratio,
                "measured": 0.9999985583402328,
                "error_pct": _err_pct(ratio, 0.9999985583402328),
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [
            rel_repo_path(vl_distill_atlas_summary_path()),
            rel_repo_path(vl_distill_domain_registry_path()),
            rel_repo_path(vl_distill_dataset_meta_path()),
            rel_repo_path(vl_distill_competitive_report_path()),
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