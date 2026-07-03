#!/usr/bin/env python3
"""Planetary structure benchmark — computed density vs JPL published."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "planetary_jpl_cache.json"
OUTPUT = ROOT / "data" / "planetary_structure_benchmark.json"


def build(cache_path: Path = CACHE) -> dict:
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_planetary_jpl.py first: {cache_path}")
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from jpl_horizons_lab import density_from_mass_radius, resolve_body_physical  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_plan = float(mod.domain_scalar("Planetary_Science"))

    records: list[dict] = []
    for body in doc.get("bodies") or []:
        phys = resolve_body_physical(body.get("name") or "", body.get("horizons_text") or "")
        radius = phys.get("radius_km")
        published = phys.get("density_g_cm3")
        mass_kg = phys.get("mass_kg")
        if None in (radius, published, mass_kg):
            continue
        computed = density_from_mass_radius(mass_kg, float(radius))
        tol_pct = 0.5 + abs(S_plan) * 0.3
        err = abs(computed - float(published)) / float(published) * 100.0
        records.append(
            {
                "lab": "planetary_structure_lab",
                "property": "mean_density",
                "name": body.get("name"),
                "computed": round(computed, 4),
                "measured": float(published),
                "error_pct": round(err, 6),
                "within_tol": err <= tol_pct,
            }
        )

    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "JPL_Horizons_physical",
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 16,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  bodies: {doc['record_count']}  median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())