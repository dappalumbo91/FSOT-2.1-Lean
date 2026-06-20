#!/usr/bin/env python3
"""Ingest Kronos FSOT metrology thesis runs into lab_registry.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "kronos_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from kronos_lab import load_kronos_summary, summarize_kronos  # noqa: E402


def ingest_kronos(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    kronos_root = Path(manifest["kronos_root"])
    csv_path = kronos_root / manifest["artifacts"]["run_summary"]["path"]
    rows = load_kronos_summary(csv_path) if csv_path.exists() else []
    return {
        "present": csv_path.exists(),
        "kronos_root": str(kronos_root),
        "summary_path": str(csv_path),
        "rows": rows,
        **summarize_kronos(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Kronos metrology thesis runs")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    kronos = ingest_kronos()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["kronos_lab"] = kronos
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  runs: {kronos['run_count']}")
    if kronos.get("best_fractional_error") is not None:
        print(f"  best fractional error: {kronos['best_fractional_error']:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())