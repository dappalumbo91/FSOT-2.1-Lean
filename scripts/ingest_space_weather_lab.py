#!/usr/bin/env python3
"""Ingest space weather benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "space_weather_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
INGEST = ROOT / "scripts" / "ingest_space_weather_swpc.py"
BUILDER = ROOT / "scripts" / "build_space_weather_benchmark.py"


def main() -> int:
    if INGEST.exists():
        subprocess.run([sys.executable, str(INGEST)], cwd=ROOT, check=False)
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["space_weather_lab"] = {
        "kp_record_count": bench.get("kp_record_count"),
        "ap_record_count": bench.get("ap_record_count"),
        "observable_count": bench.get("observable_count"),
        "stability_match_rate": bench.get("stability_match_rate"),
        "fusion_scalar_S": bench.get("fusion_scalar_S"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  space weather Kp records: {bench.get('kp_record_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())