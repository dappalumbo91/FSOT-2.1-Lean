#!/usr/bin/env python3
"""Trinary cube-block hardware motif profile benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "trinary_hardware_motif_benchmark.json"
CANONICAL = ROOT / "data" / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import rel_repo_path, trinary_hardware_motif_path  # noqa: E402
from trinary_os_invariants import derived_os_constants  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    motif_path = trinary_hardware_motif_path()
    motif = json.loads(motif_path.read_text(encoding="utf-8"))
    constants = derived_os_constants()
    cache = json.loads(CANONICAL.read_text(encoding="utf-8"))
    l2 = cache.get("layer2") or {}
    c_eff = float(l2.get("coherence_efficiency") or 0)
    p_var = float(l2.get("phase_variance") or 0)
    collapse = c_eff * p_var
    records: list[dict] = []

    tier_checks = [
        ("tier_mild_intensity", 1.05),
        ("tier_moderate_intensity", 1.15),
        ("tier_severe_intensity", 1.30),
    ]
    for key, expected in tier_checks:
        live = float(motif.get(key) or 0)
        records.append(
            {
                "lab": "trinary_hardware_motif",
                "property": key,
                "computed": live,
                "measured": expected,
                "error_pct": _err_pct(live, expected),
            }
        )

    ordering_ok = (
        float(motif.get("tier_mild_intensity", 0))
        < float(motif.get("tier_moderate_intensity", 0))
        < float(motif.get("tier_severe_intensity", 0))
    )
    records.append(
        {
            "lab": "trinary_hardware_motif",
            "property": "tier_intensity_ordering",
            "computed": 1 if ordering_ok else 0,
            "measured": 1,
            "error_pct": 0.0 if ordering_ok else 100.0,
        }
    )

    weight_sum = float(motif.get("interaction_pressure_weight", 0)) + float(
        motif.get("interaction_migration_weight", 0)
    )
    records.append(
        {
            "lab": "trinary_hardware_motif",
            "property": "interaction_weight_sum",
            "computed": weight_sum,
            "measured": 1.0,
            "error_pct": _err_pct(weight_sum, 1.0),
        }
    )

    hysteresis = float(motif.get("abstraction_min_enter", 0)) - float(
        motif.get("abstraction_min_exit", 0)
    )
    records.append(
        {
            "lab": "trinary_hardware_motif",
            "property": "abstraction_hysteresis_gap",
            "computed": hysteresis,
            "measured": float(motif.get("abstraction_hysteresis_gap", 0.05)),
            "error_pct": _err_pct(hysteresis, float(motif.get("abstraction_hysteresis_gap", 0.05))),
        }
    )

    records.append(
        {
            "lab": "trinary_hardware_motif",
            "property": "collapse_threshold_bridge",
            "computed": collapse,
            "measured": float(constants.get("collapse_threshold") or collapse),
            "error_pct": _err_pct(collapse, float(constants.get("collapse_threshold") or collapse)),
        }
    )

    records.append(
        {
            "lab": "trinary_hardware_motif",
            "property": "conversion_gate_min_threshold",
            "computed": float(motif.get("conversion_gate_min_threshold", 0)),
            "measured": 0.30,
            "error_pct": _err_pct(float(motif.get("conversion_gate_min_threshold", 0)), 0.30),
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(motif_path)],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
        "motif_version": motif.get("version"),
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