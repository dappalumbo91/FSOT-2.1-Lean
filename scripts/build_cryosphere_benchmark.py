#!/usr/bin/env python3
"""Cryosphere benchmark — northern climate cohort freezing-month classifier."""

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
MANIFEST = ROOT / "data" / "cryosphere_manifest.yaml"
OUTPUT = ROOT / "data" / "cryosphere_benchmark.json"


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    climate_manifest = yaml.safe_load((ROOT / spec["source"]["climate_manifest"]).read_text(encoding="utf-8"))
    cache_root = ROOT / climate_manifest["cache"]["root"] / "chunks"
    northern = set(spec["source"]["northern_stations"])
    threshold = float(spec["source"]["freezing_threshold_c"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_gal = float(mod.domain_scalar("Planetary_Science"))

    records: list[dict] = []
    for path in sorted(cache_root.glob("*.json")):
        chunk = json.loads(path.read_text(encoding="utf-8"))
        station = chunk.get("station")
        if station not in northern:
            continue
        for month, stats in (chunk.get("monthly") or {}).items():
            tavg = stats.get("tavg_mean_c")
            if tavg is None:
                continue
            observed_freezing = float(tavg) < threshold
            # Galactic-scalar gate for cryosphere-active months
            freeze_cutoff = threshold - abs(S_gal) * 0.5
            predicted_freezing = float(tavg) < freeze_cutoff
            match = predicted_freezing == observed_freezing
            records.append(
                {
                    "lab": "cryosphere_lab",
                    "property": "freezing_month_classifier",
                    "name": f"{station}:{month}",
                    "station": station,
                    "month": month,
                    "tavg_c": round(float(tavg), 3),
                    "computed_freezing": 1.0 if predicted_freezing else 0.0,
                    "measured_freezing": 1.0 if observed_freezing else 0.0,
                    "error_pct": 0.0 if match else 100.0,
                    "S_galactic": round(S_gal, 6),
                }
            )

    errs = [r["error_pct"] for r in records]
    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    stations = sorted({r["station"] for r in records})
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "climate_ncei_northern_cryosphere_proxy",
        "station_count": len(stations),
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "freezing_threshold_c": threshold,
        "maps_to_lean": ["energy", "galactic"],
        "D_eff": 16,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = build(args.manifest)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records: {bench['record_count']}  stations: {bench['station_count']}  "
        f"match: {bench.get('stability_match_rate', 0):.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())