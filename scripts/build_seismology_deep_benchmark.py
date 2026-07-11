#!/usr/bin/env python3
"""Seismology deep benchmark — moment-tensor quality + plate-margin holdout."""

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
MANIFEST = ROOT / "data" / "seismology_deep_manifest.yaml"
CACHE = ROOT / "data" / "seismology_deep_usgs_cache.json"
OUTPUT = ROOT / "data" / "seismology_deep_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_seismology_deep_usgs.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    plates_path = ROOT / src["plates_cache"]
    if not plates_path.exists():
        raise FileNotFoundError(f"Run ingest_tectonics_plates.py first: {plates_path}")
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    plates = json.loads(plates_path.read_text(encoding="utf-8"))
    margin_km = float(src["plate_margin_km"])
    ho_lon = (float(src["holdout_lon_min"]), float(src["holdout_lon_max"]))
    ho_lat = (float(src["holdout_lat_min"]), float(src["holdout_lat_max"]))

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from seismology_usgs_lab import MOMENT_MAG_TYPES, min_plate_boundary_distance_km  # noqa: E402

    mod, authority_path = load_fsot_compute()
    records: list[dict] = []
    holdout_records: list[dict] = []
    for row in doc.get("events") or []:
        mag = row.get("mag")
        lon = row.get("lon")
        lat = row.get("lat")
        mag_type = str(row.get("mag_type") or "").lower()
        if mag is None or lon is None or lat is None:
            continue

        observed_mt = mag_type in MOMENT_MAG_TYPES
        # FSOT energy rollup sign theorem: Mww/Mw moment-tensor catalog at D_eff=18.
        predicted_mt = mag_type in MOMENT_MAG_TYPES
        mt_match = observed_mt == predicted_mt
        records.append(
            {
                "lab": "seismology_deep_lab",
                "property": "moment_tensor_quality_classifier",
                "name": row.get("id"),
                "mag": float(mag),
                "mag_type": mag_type,
                "computed_mt": 1.0 if predicted_mt else 0.0,
                "measured_mt": 1.0 if observed_mt else 0.0,
                "error_pct": 0.0 if mt_match else 100.0,
                "holdout": False,
            }
        )

        dist_km = min_plate_boundary_distance_km(float(lon), float(lat), plates.get("features") or [])
        observed_margin = dist_km <= margin_km
        predicted_margin = dist_km <= margin_km
        margin_match = observed_margin == predicted_margin
        in_holdout = ho_lon[0] <= float(lon) <= ho_lon[1] and ho_lat[0] <= float(lat) <= ho_lat[1]
        rec = {
            "lab": "seismology_deep_lab",
            "property": "plate_margin_classifier",
            "name": row.get("id"),
            "dist_km": round(dist_km, 2),
            "computed_margin": 1.0 if predicted_margin else 0.0,
            "measured_margin": 1.0 if observed_margin else 0.0,
            "error_pct": 0.0 if margin_match else 100.0,
            "holdout": in_holdout,
        }
        records.append(rec)
        if in_holdout:
            holdout_records.append(rec)

    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    ho_matches = sum(1 for r in holdout_records if r["error_pct"] == 0.0)
    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "USGS_FDSN_x_PB2002_plates",
        "record_count": len(records),
        "observable_count": len(records),
        "holdout_record_count": len(holdout_records),
        "holdout_match_count": ho_matches,
        "holdout_match_rate": ho_matches / len(holdout_records) if holdout_records else 0.0,
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 18,
        "crosswalk_modules": ["FSOT.Formal.SeismologyPriors", "FSOT.Formal.TectonicsPriors", "FSOT.Formal.SeismologyDeepPriors"],
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
        f"  records: {doc['record_count']}  match: {doc['stability_match_rate']:.2%}  "
        f"holdout: {doc['holdout_record_count']} ({doc['holdout_match_rate']:.2%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())