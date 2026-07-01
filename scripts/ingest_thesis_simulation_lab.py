#!/usr/bin/env python3
"""Ingest thesis simulation benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "thesis_simulation_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_thesis_simulation_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["thesis_simulation_lab"] = {
        "wave_target_count": bench.get("wave_target_count"),
        "intrinsic_screen_count": bench.get("intrinsic_screen_count"),
        "observable_count": bench.get("observable_count"),
        "wave_file_count": bench.get("wave_file_count"),
        "intrinsic_best_rmse": bench.get("intrinsic_best_rmse"),
        "intrinsic_best_r2": bench.get("intrinsic_best_r2"),
        "source_root": bench.get("source_root"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  observables: {bench.get('observable_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())