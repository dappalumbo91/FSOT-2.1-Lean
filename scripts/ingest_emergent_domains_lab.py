#!/usr/bin/env python3
"""Ingest emergent domains benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "emergent_domains_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_emergent_domains_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["emergent_domains_lab"] = {
        "emergent_domain_count": bench.get("emergent_domain_count"),
        "observed_domain_count": bench.get("observed_domain_count"),
        "final_emergence_health": bench.get("final_emergence_health"),
        "final_meta_S": bench.get("final_meta_S"),
        "refined_robust_count": bench.get("refined_robust_count"),
        "source_root": bench.get("source_root"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  emergent domains: {bench.get('emergent_domain_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())