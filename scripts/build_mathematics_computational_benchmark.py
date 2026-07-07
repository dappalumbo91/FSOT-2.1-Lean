#!/usr/bin/env python3
"""Mathematics computational — math-generator formula comparisons + constant alignment."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "mathematics_computational_manifest.yaml"
OUTPUT = ROOT / "data" / "mathematics_computational_benchmark.json"
CACHE = ROOT / "data" / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import math_generator_comparison_path  # noqa: E402

CONST_MAP = {
    "phi": ("seeds", "phi"),
    "alpha": ("layer1", "alpha"),
    "psi_con": ("layer1", "psi_con"),
    "eta_eff": ("layer1", "eta_eff"),
    "theta_s": ("layer1", "theta_s"),
    "poof": ("layer1", "poof_factor"),
    "c_eff": ("layer2", "coherence_efficiency"),
    "a_bleed": ("layer2", "acoustic_bleed"),
    "a_in": ("layer2", "acoustic_inflow"),
    "p_base": ("layer2", "perceived_param_base"),
    "p_new": ("layer2", "new_perceived_param"),
    "c_cosm": ("layer2", "c_cosm"),
    "b_in": ("layer2", "bleed_in_factor"),
    "c_factor": ("layer2", "consciousness_factor"),
}


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    report_path = math_generator_comparison_path()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    records: list[dict] = []

    for row in report.get("comparisons") or []:
        err = row.get("relative_error_percent")
        if err is None:
            continue
        records.append(
            {
                "lab": "math_generator_lab",
                "case_id": row.get("case_id"),
                "property": row.get("observed_value_kind") or row.get("case_id"),
                "computed": row.get("derived_value") or row.get("fsot_scalar"),
                "measured": row.get("observed_value"),
                "error_pct": float(err),
                "unit": row.get("unit"),
                "formula": row.get("formula_expression"),
            }
        )

    for sym, live in (report.get("constants") or {}).items():
        section, key = CONST_MAP.get(sym, (None, None))
        if section is None:
            continue
        cached = float(cache.get(section, {}).get(key, 0))
        if cached == 0:
            continue
        err = abs(float(live) - cached) / abs(cached) * 100.0
        records.append(
            {
                "lab": "math_generator_constants",
                "case_id": f"constant_{sym}",
                "property": sym,
                "computed": live,
                "measured": cached,
                "error_pct": err,
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(report_path),
        "maps_to_lean": ["particle", "mathematical"],
        "D_eff": 17,
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