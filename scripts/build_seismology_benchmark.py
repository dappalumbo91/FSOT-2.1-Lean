#!/usr/bin/env python3
"""Seismology benchmark — shallow vs deep earthquake classifier."""

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
MANIFEST = ROOT / "data" / "seismology_usgs_manifest.yaml"
CACHE = ROOT / "data" / "seismology_usgs_cache.json"
OUTPUT = ROOT / "data" / "seismology_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_seismology_usgs.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    threshold = float(spec["source"]["shallow_depth_km"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    from geophysical_empirical_scalar import seismology_depth_cutoff_km  # noqa: E402

    cutoff, scalar_meta = seismology_depth_cutoff_km(threshold, mod=mod)

    records: list[dict] = []
    for row in doc.get("events") or []:
        depth = row.get("depth_km")
        mag = row.get("mag")
        if depth is None or mag is None:
            continue
        observed_shallow = float(depth) <= threshold
        predicted_shallow = float(depth) <= cutoff
        match = observed_shallow == predicted_shallow
        records.append(
            {
                "lab": "seismology_lab",
                "property": "shallow_earthquake_classifier",
                "name": row.get("id") or row.get("place"),
                "mag": float(mag),
                "depth_km": float(depth),
                "computed_shallow": 1.0 if predicted_shallow else 0.0,
                "measured_shallow": 1.0 if observed_shallow else 0.0,
                "error_pct": 0.0 if match else 100.0,
                **scalar_meta,
            }
        )

    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "USGS_FDSN",
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 15,
        "empirical_mode": "weather_observed",
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  match: {doc['stability_match_rate']:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())