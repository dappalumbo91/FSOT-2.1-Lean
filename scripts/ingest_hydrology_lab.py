#!/usr/bin/env python3
"""Ingest hydrology benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "hydrology_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
CHUNKED = ROOT / "scripts" / "ingest_hydrology_usgs_chunked.py"
BUILDER = ROOT / "scripts" / "build_hydrology_benchmark.py"


def main() -> int:
    if CHUNKED.exists():
        subprocess.run([sys.executable, str(CHUNKED)], cwd=ROOT, check=False)
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["hydrology_lab"] = {
        "station_count": bench.get("station_count"),
        "month_count": bench.get("month_count"),
        "observable_count": bench.get("observable_count"),
        "stability_match_rate": bench.get("stability_match_rate"),
        "median_error_pct": bench.get("median_error_pct"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  hydrology months: {bench.get('record_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())