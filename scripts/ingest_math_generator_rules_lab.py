#!/usr/bin/env python3
"""Ingest Math generator RULES corpora benchmark into lab_registry."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "math_generator_rules_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"
BUILDER = ROOT / "scripts" / "build_math_generator_rules_benchmark.py"


def main() -> int:
    if not BENCH.exists() and BUILDER.exists():
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    if not BENCH.exists():
        print(f"Missing {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["math_generator_rules"] = {
        "rule_corpus_count": bench.get("rule_corpus_count"),
        "total_rule_count": bench.get("total_rule_count"),
        "observable_count": bench.get("observable_count"),
        "source_root": bench.get("source_root"),
        "corpus_names": [c.get("corpus") for c in bench.get("corpora") or []],
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    if "math_generator_lab" in registry:
        registry["math_generator_lab"]["rule_corpus_count"] = bench.get("rule_corpus_count")
        registry["math_generator_lab"]["total_rule_count"] = bench.get("total_rule_count")
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(
        f"  corpora: {bench.get('rule_corpus_count')}  "
        f"rules: {bench.get('total_rule_count')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())