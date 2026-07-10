#!/usr/bin/env python3
"""Ingest Higgs mass benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "higgs_mass_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_higgs_mass_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    gev = next((r for r in bench.get("records") or [] if r.get("property") == "m_H_GeV"), {})
    registry["higgs_mass_lab"] = {
        "rule_id": bench.get("rule_id"),
        "observable_count": bench.get("observable_count"),
        "median_error_pct": bench.get("median_error_pct"),
        "computed_gev": gev.get("computed"),
        "measured_gev": gev.get("measured"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  higgs mass observables: {bench.get('observable_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())