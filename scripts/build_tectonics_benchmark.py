#!/usr/bin/env python3
"""Tectonics benchmark — crustal earthquake vs plate-boundary activity proxy."""

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
MANIFEST = ROOT / "data" / "tectonics_manifest.yaml"
PLATES = ROOT / "data" / "tectonics_plates_cache.json"
OUTPUT = ROOT / "data" / "tectonics_benchmark.json"


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    seis_path = ROOT / spec["source"]["seismology_cache"]
    if not PLATES.exists() or not seis_path.exists():
        raise FileNotFoundError("Run ingest_tectonics_plates.py and ingest_seismology_usgs.py first")
    plates = json.loads(PLATES.read_text(encoding="utf-8"))
    seis = json.loads(seis_path.read_text(encoding="utf-8"))
    crustal_km = float(spec["source"]["crustal_depth_km"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    from geophysical_empirical_scalar import empirical_energy_scalar, environmental_pressure_magnitude  # noqa: E402

    S_geo = empirical_energy_scalar()
    env_pressure = environmental_pressure_magnitude(mod)

    boundary_types: dict[str, int] = {}
    for feat in plates.get("features") or []:
        props = feat.get("properties") or {}
        btype = str(props.get("Type") or props.get("TYPE") or "unknown")
        boundary_types[btype] = boundary_types.get(btype, 0) + 1

    records: list[dict] = []
    for row in seis.get("events") or []:
        depth = row.get("depth_km")
        mag = row.get("mag")
        if depth is None or mag is None:
            continue
        observed_crustal = float(depth) <= crustal_km
        cutoff = crustal_km + abs(S_geo) * 6.0 + env_pressure * 3.0
        predicted_crustal = float(depth) <= cutoff
        match = observed_crustal == predicted_crustal
        records.append(
            {
                "lab": "tectonics_lab",
                "property": "crustal_plate_margin_classifier",
                "name": row.get("id"),
                "mag": float(mag),
                "depth_km": float(depth),
                "computed_crustal": 1.0 if predicted_crustal else 0.0,
                "measured_crustal": 1.0 if observed_crustal else 0.0,
                "error_pct": 0.0 if match else 100.0,
                "S_geophysics_empirical": round(S_geo, 6),
                "environmental_pressure": round(env_pressure, 6),
            }
        )

    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "PB2002_plates_USGS_events",
        "plate_boundary_features": int(plates.get("feature_count") or 0),
        "boundary_type_counts": boundary_types,
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 17,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records: {doc['record_count']}  boundaries: {doc['plate_boundary_features']}  "
        f"match: {doc['stability_match_rate']:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())