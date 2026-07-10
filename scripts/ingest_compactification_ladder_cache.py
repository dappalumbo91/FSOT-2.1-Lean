#!/usr/bin/env python3
"""Cache compactification ladder validation data on external drive (G:/FSOT-PublicData)."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXTERNAL = Path(os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "G:/FSOT-PublicData")) / "compactification_ladder"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def build_ladder_index() -> dict:
    manifest = _load_yaml(DATA / "compactification_ladder_manifest.yaml")
    rungs = (manifest.get("ladder") or {}).get("rungs") or []
    rows: list[dict] = []
    for rung in rungs:
        primary = _load_json(ROOT / rung["benchmark_primary"])
        secondary = _load_json(ROOT / rung["benchmark_secondary"])
        rows.append(
            {
                "rung_id": rung["id"],
                "name": rung["name"],
                "rung_index": rung["rung_index"],
                "D_eff_ladder": rung["D_eff_ladder"],
                "anchor_domain": rung["anchor_domain"],
                "formula_branch": rung["formula_branch"],
                "primary_record_count": primary.get("record_count"),
                "primary_median_error_pct": primary.get("pooled_median_error_pct"),
                "secondary_record_count": secondary.get("record_count"),
                "secondary_median_error_pct": secondary.get("pooled_median_error_pct"),
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "external_cache_root": str(EXTERNAL),
        "rung_count": len(rows),
        "rungs": rows,
        "manifest": "compactification_ladder_manifest.yaml",
    }


def build_adjacent_index() -> dict:
    manifest = _load_yaml(DATA / "compactification_ladder_manifest.yaml")
    pairs = (manifest.get("ladder") or {}).get("adjacent_pairs") or []
    bench = _load_json(DATA / "adjacent_rung_coupling_benchmark.json")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "adjacent_pair_count": len(pairs),
        "pairs": pairs,
        "benchmark_pooled_median_error_pct": bench.get("pooled_median_error_pct"),
        "neighbor_only_policy": True,
    }


def main() -> int:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    ladder = build_ladder_index()
    ladder_path = EXTERNAL / "compactification_ladder_index.json"
    ladder_path.write_text(json.dumps(ladder, indent=2), encoding="utf-8")
    print(f"Wrote {ladder_path} rungs={ladder['rung_count']}")

    adjacent = build_adjacent_index()
    adjacent_path = EXTERNAL / "adjacent_rung_coupling_index.json"
    adjacent_path.write_text(json.dumps(adjacent, indent=2), encoding="utf-8")
    print(f"Wrote {adjacent_path} pairs={adjacent['adjacent_pair_count']}")

    fold = _load_json(DATA / "fold_depth_metrics_benchmark.json")
    fold_path = EXTERNAL / "fold_depth_metrics_summary.json"
    fold_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "fold_depth_min": fold.get("fold_depth_min"),
                "fold_depth_max": fold.get("fold_depth_max"),
                "fold_depth_span": fold.get("fold_depth_span"),
                "D_eff_ceiling": fold.get("D_eff_ceiling"),
                "pooled_median_error_pct": fold.get("pooled_median_error_pct"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {fold_path}")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cache_root": str(EXTERNAL),
        "files": [
            "compactification_ladder_index.json",
            "adjacent_rung_coupling_index.json",
            "fold_depth_metrics_summary.json",
        ],
        "note": "Compactification ladder bulk cache — not stored on main system drive.",
    }
    (EXTERNAL / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Compactification ladder cache ready at {EXTERNAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())