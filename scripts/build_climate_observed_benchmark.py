#!/usr/bin/env python3
"""Build climate_observed_benchmark.json from chunked NCEI cache (or Open-Meteo fallback)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from climate_ncei_lab import MANIFEST_PATH, build_benchmark_records, load_all_chunks, load_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build climate observed benchmark")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--min-chunks", type=int, default=1)
    parser.add_argument("--fallback-open-meteo", action="store_true")
    args = parser.parse_args()

    spec = load_manifest(args.manifest)
    cache_root = ROOT / spec["cache"]["root"]
    chunks_dir = cache_root / "chunks"
    output = ROOT / spec["benchmark"]["output"]
    min_months = int(spec["benchmark"].get("min_months_total", 120))

    chunks = load_all_chunks(chunks_dir)
    if len(chunks) >= args.min_chunks:
        doc = build_benchmark_records(
            chunks,
            anomaly_tolerance_c=float(spec["benchmark"].get("anomaly_tolerance_c", 2.5)),
            D_eff=float(spec["benchmark"].get("D_eff", 16)),
        )
        doc["ingest_state"] = str(cache_root / "ingest_state.json")
    elif args.fallback_open_meteo:
        fetch = ROOT / "scripts" / "fetch_climate_observed_benchmark.py"
        proc = subprocess.run([sys.executable, str(fetch), "--output", str(output)], check=False)
        return proc.returncode
    else:
        print(f"FAIL: only {len(chunks)} chunks in {chunks_dir}; run ingest_climate_ncei_chunked.py first")
        return 1

    if doc.get("record_count", 0) < min_months and not args.fallback_open_meteo:
        print(f"WARN: {doc['record_count']} records < min_months_total {min_months}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"  stations: {doc.get('station_count')}  records: {doc.get('record_count')}")
    print(f"  median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())