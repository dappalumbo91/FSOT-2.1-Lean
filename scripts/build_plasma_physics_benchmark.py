#!/usr/bin/env python3
"""Plasma physics stability classifier vs FSOT energy/plasma scalar (MHD beta proxy)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "plasma_physics_benchmark.json"

# Plasma beta threshold ~0.1 for MHD stability (literature rule-of-thumb)
BETA_STABLE_MAX = 0.1

PLASMA_CASES = [
    {"name": "ionosphere", "beta": 1.0e-6, "observed_stable": True},
    {"name": "solar_wind", "beta": 0.05, "observed_stable": True},
    {"name": "tokamak_H_mode", "beta": 0.03, "observed_stable": True},
    {"name": "tokamak_high_beta", "beta": 0.15, "observed_stable": False},
    {"name": "laboratory_Q_machine", "beta": 0.001, "observed_stable": True},
    {"name": "magnetosphere", "beta": 0.08, "observed_stable": True},
]


def build() -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S = float(mod.domain_scalar("Thermodynamics"))
    records: list[dict] = []
    for case in PLASMA_CASES:
        beta = float(case["beta"])
        observed_stable = bool(case["observed_stable"])
        predicted_stable = S > (0.5 + beta * 2.0)
        match = predicted_stable == observed_stable
        records.append(
            {
                "lab": "plasma_physics_lab",
                "property": "mhd_beta_stability",
                "name": case["name"],
                "computed": 1.0 if predicted_stable else 0.0,
                "measured": 1.0 if observed_stable else 0.0,
                "error_pct": 0.0 if match else 100.0,
                "beta": beta,
                "S": round(S, 6),
            }
        )
    errs = [r["error_pct"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "plasma_scalar_S": S,
        "maps_to_lean": ["energy", "fusion"],
        "D_eff": 14,
        "record_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']} median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())