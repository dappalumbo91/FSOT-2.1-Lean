#!/usr/bin/env python3
"""Ingest Soul Simulator + evolution cellular proxy."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cellular_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cellular_lab import load_soul_manifest, summarize_cellular  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    soul_path = Path(manifest["artifacts"]["soul_simulator_manifest"]["path"])
    operons_path = Path(manifest["artifacts"]["evolution_operons"]["path"])
    soul = load_soul_manifest(soul_path)
    summary = summarize_cellular(soul, operons_path)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["cellular_lab"] = {
        **summary,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  soul_records: {summary['soul_records_processed']}  operons: {summary['evolution_operon_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())