#!/usr/bin/env python3
"""Sync seismology/tectonics/geomagnetism benchmarks into lab_registry.json."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"

BENCH_MAP = {
    "seismology_lab": {
        "bench": ROOT / "data" / "seismology_benchmark.json",
        "build": ROOT / "scripts" / "build_seismology_benchmark.py",
        "ingest": ROOT / "scripts" / "ingest_seismology_usgs.py",
    },
    "tectonics_lab": {
        "bench": ROOT / "data" / "tectonics_benchmark.json",
        "build": ROOT / "scripts" / "build_tectonics_benchmark.py",
        "ingest": ROOT / "scripts" / "ingest_tectonics_plates.py",
    },
    "geomagnetism_lab": {
        "bench": ROOT / "data" / "geomagnetism_benchmark.json",
        "build": ROOT / "scripts" / "build_geomagnetism_benchmark.py",
        "ingest": ROOT / "scripts" / "ingest_geomagnetism_swpc.py",
    },
}


def _ensure_benchmark(lab_key: str, spec: dict) -> dict:
    bench_path = spec["bench"]
    if not bench_path.exists():
        if spec["ingest"].exists():
            subprocess.run([sys.executable, str(spec["ingest"])], cwd=ROOT, check=False)
        if spec["build"].exists():
            subprocess.run([sys.executable, str(spec["build"])], cwd=ROOT, check=True)
    if not bench_path.exists():
        raise FileNotFoundError(f"Missing benchmark for {lab_key}: {bench_path}")
    return json.loads(bench_path.read_text(encoding="utf-8"))


def ingest() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    summary: dict[str, dict] = {}
    for lab_key, spec in BENCH_MAP.items():
        bench = _ensure_benchmark(lab_key, spec)
        entry = {
            "present": True,
            "record_count": int(bench.get("record_count") or bench.get("observable_count") or 0),
            "observable_count": int(bench.get("observable_count") or bench.get("record_count") or 0),
            "median_error_pct": bench.get("median_error_pct"),
            "stability_match_rate": bench.get("stability_match_rate"),
            "D_eff": bench.get("D_eff"),
            "source": bench.get("source"),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        }
        registry[lab_key] = entry
        summary[lab_key] = entry
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    summary = ingest()
    print(f"Updated {REGISTRY}")
    for lab_key, entry in summary.items():
        print(f"  {lab_key}: records={entry['record_count']} median_err={entry['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())