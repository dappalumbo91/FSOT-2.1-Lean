#!/usr/bin/env python3
"""Ingest FSOT linguistics empirical anchors into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "linguistics_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from linguistics_targets import (  # noqa: E402
    load_derivations_db,
    load_targets_csv,
    merge_targets,
    summarize_linguistics,
)


def ingest_linguistics(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["linguistics_root"])
    csv_path = root / manifest["artifacts"]["targets_csv"]["path"]
    db_path = root / manifest["artifacts"]["derivations_db"]["path"]
    targets = load_targets_csv(csv_path)
    derivations = load_derivations_db(db_path)
    rows = merge_targets(targets, derivations)
    return {
        "present": csv_path.exists(),
        "targets_path": str(csv_path),
        "db_path": str(db_path),
        "rows": rows,
        **summarize_linguistics(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest linguistics targets")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    linguistics = ingest_linguistics()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["linguistics_lab"] = linguistics
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  targets: {linguistics['target_count']}  max_err: {linguistics['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())