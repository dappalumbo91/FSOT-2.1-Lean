#!/usr/bin/env python3
"""Ingest cosmology bubble-bleed benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "cosmology_bubble_bleed_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
MANIFEST = ROOT / "data" / "cosmology_bubble_bleed_manifest.yaml"
BUILDER = ROOT / "scripts" / "build_cosmology_bubble_bleed_benchmark.py"
INGEST_NEB = ROOT / "scripts" / "ingest_nebula_lensing.py"
INGEST_FRB = ROOT / "scripts" / "ingest_frb_repeaters.py"


def main() -> int:
    if not BENCH.exists():
        for script in (INGEST_NEB, INGEST_FRB, BUILDER):
            if script.exists():
                subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["cosmology_bubble_bleed_lab"] = {
        "mechanism": bench.get("mechanism"),
        "h0_global_fsot": bench.get("h0_global_fsot"),
        "bubble_bleed_fraction": bench.get("bubble_bleed_fraction"),
        "blackhole_observable_count": bench.get("blackhole_observable_count"),
        "nebula_count": bench.get("nebula_count"),
        "frb_count": bench.get("frb_count"),
        "h0_sector_count": bench.get("h0_sector_count"),
        "observable_count": bench.get("observable_count"),
        "nebula_coupling_match_rate": bench.get("nebula_match_rate"),
        "frb_classifier_match_rate": bench.get("frb_classifier_match_rate"),
        "median_error_pct": bench.get("median_error_pct"),
        "max_error_pct": bench.get("max_error_pct"),
        "D_eff": bench.get("D_eff"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  bubble bleed observables: {bench.get('observable_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())