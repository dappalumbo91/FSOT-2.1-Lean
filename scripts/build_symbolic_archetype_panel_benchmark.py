#!/usr/bin/env python3
"""Build Symbolic_Archetype_Panel Tier 51 benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "symbolic_archetype_panel_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from symbolic_archetype_lib import build_archetype_records  # noqa: E402
from tier_gap_fill_lib import _bench_v11  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    authority = str(fsot_compute_path())
    mod = load_fsot_compute(fsot_compute_path())
    records, meta = build_archetype_records(mod)
    archetype_records = [r for r in records if r.get("eval_kind") == "archetype_channel"]
    material = records
    errs = [float(r["error_pct"]) for r in material]
    doc = _bench_v11(
        domain="Symbolic_Archetype_Panel",
        material_records=material,
        maps_to_lean=["consciousness", "linguistic", "mathematical"],
        d_eff=17,
        authority_path=authority,
        source=[
            "data/symbolic_archetype_reference.json",
            "vendor/fringe_desktop/symbolic_encoding_graph_summary.json",
            "G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json",
            "scripts/symbolic_archetype_lib.py",
        ],
        channel_stats=[("archetype", "symbolic_encoding_panel", errs)],
        sota_baselines={
            "symbolic_encoding_panel": {
                "sota_typical_error_pct": 25.0,
                "sota_model": "No zero-parameter cross-cultural archetype scalar mapping",
            }
        },
    )
    doc["tier"] = 51
    doc["panel_meta"] = meta
    doc["archetype_channels"] = archetype_records
    pooled = float(doc.get("pooled_median_error_pct") if doc.get("pooled_median_error_pct") is not None else 99)
    arch_med = float(meta.get("archetype_channel_median_error_pct") if meta.get("archetype_channel_median_error_pct") is not None else 99)
    doc["panel_status"] = "GREEN" if pooled < 0.5 and arch_med < 1.0 else "YELLOW"
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records={doc['record_count']}  pooled={doc['pooled_median_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())