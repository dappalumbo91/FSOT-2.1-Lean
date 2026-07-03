#!/usr/bin/env python3
"""Ingest particle physics extended benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "particle_physics_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_particle_physics_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["particle_physics_lab"] = {
        "smiles_particle_count": bench.get("smiles_particle_count"),
        "thesis_particle_wave_count": bench.get("thesis_particle_wave_count"),
        "wave4_count": bench.get("wave4_count"),
        "math_physics_rule_count": bench.get("math_physics_rule_count"),
        "observable_count": bench.get("observable_count"),
        "median_error_pct": bench.get("median_error_pct"),
        "max_error_pct": bench.get("max_error_pct"),
        "within_two_pct_count": bench.get("within_two_pct_count"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  particle observables: {bench.get('observable_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())