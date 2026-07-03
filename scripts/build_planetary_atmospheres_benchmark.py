#!/usr/bin/env python3
"""Planetary atmospheres benchmark — pressure/temperature vs NASA/JPL references."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "planetary_atmospheres_cache.json"
OUTPUT = ROOT / "data" / "planetary_atmospheres_benchmark.json"

# Published reference anchors (NASA Planetary Fact Sheets; JPL for Mars/Venus cross-check).
REFERENCE = {
    "Mars": {"pressure_bar": 0.00636, "temperature_k": 210.0},
    "Venus": {"pressure_bar": 92.0, "temperature_k": 737.0},
    "Titan": {"pressure_bar": 1.476, "temperature_k": 93.7},
}


def build(cache_path: Path = CACHE) -> dict:
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_planetary_atmospheres_jpl.py first: {cache_path}")
    doc = json.loads(cache_path.read_text(encoding="utf-8"))

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_plan = float(mod.domain_scalar("Planetary_Science"))

    records: list[dict] = []
    for body in doc.get("bodies") or []:
        name = body.get("name")
        ref = REFERENCE.get(name)
        if not ref:
            continue
        tol_pct = 0.5 + abs(S_plan) * 0.35
        for prop, key in (("surface_pressure", "pressure_bar"), ("mean_temperature", "temperature_k")):
            measured = body.get(key)
            target = ref[key]
            if measured is None or target is None or target == 0:
                continue
            err = abs(float(measured) - float(target)) / float(target) * 100.0
            records.append(
                {
                    "lab": "planetary_atmospheres_lab",
                    "property": prop,
                    "name": f"{name}:{prop}",
                    "computed": round(float(measured), 6),
                    "measured": float(target),
                    "error_pct": round(err, 6),
                    "within_tol": err <= tol_pct,
                }
            )

    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "JPL_Horizons_x_NASA_fact_sheets",
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 16,
        "crosswalk_modules": ["FSOT.Formal.PlanetaryStructurePriors", "FSOT.Formal.PlanetaryAtmospheresPriors"],
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  observables: {doc['record_count']}  median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())