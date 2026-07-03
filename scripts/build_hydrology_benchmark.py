#!/usr/bin/env python3
"""Build hydrology_benchmark.json from chunked USGS cache."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hydrology_usgs_lab import (  # noqa: E402
    MANIFEST_PATH,
    attach_cohort_metrics,
    build_benchmark_records,
    load_all_chunks,
    load_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--min-chunks", type=int, default=1)
    args = parser.parse_args()

    spec = load_manifest(args.manifest)
    cache_root = ROOT / spec["cache"]["root"]
    chunks_dir = cache_root / "chunks"
    output = ROOT / spec["benchmark"]["output"]
    min_months = int(spec["benchmark"].get("min_months_total", 120))

    chunks = load_all_chunks(chunks_dir)
    if len(chunks) < args.min_chunks:
        print(f"FAIL: only {len(chunks)} chunks; run ingest_hydrology_usgs_chunked.py first")
        return 1

    doc = build_benchmark_records(
        chunks,
        anomaly_tolerance_pct=float(spec["benchmark"].get("anomaly_tolerance_pct", 25.0)),
        D_eff=float(spec["benchmark"].get("D_eff", 15)),
    )
    doc["ingest_state"] = str(cache_root / "ingest_state.json")
    doc = attach_cohort_metrics(doc, spec)

    if doc.get("record_count", 0) < min_months:
        print(f"WARN: {doc['record_count']} records < min_months_total {min_months}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {output}")
    print(
        f"  stations: {doc.get('station_count')}  records: {doc.get('record_count')}  "
        f"match rate: {doc.get('stability_match_rate', 0):.2%}"
    )
    cohort = doc.get("cohort") or {}
    if cohort:
        ho = cohort.get("holdout") or {}
        print(f"  holdout: {ho.get('record_count')} rec median={ho.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())