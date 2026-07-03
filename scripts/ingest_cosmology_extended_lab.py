#!/usr/bin/env python3
"""Ingest cosmology extended benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "cosmology_extended_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_cosmology_extended_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["cosmology_extended_lab"] = {
        "skeleton_derivation_count": bench.get("skeleton_derivation_count"),
        "lambda_cdm_count": bench.get("lambda_cdm_count"),
        "thesis_cosmology_wave_count": bench.get("thesis_cosmology_wave_count"),
        "observable_count": bench.get("observable_count"),
        "median_error_pct": bench.get("median_error_pct"),
        "within_five_pct_count": bench.get("within_five_pct_count"),
        "source_root": bench.get("source_root"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  cosmology observables: {bench.get('observable_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())