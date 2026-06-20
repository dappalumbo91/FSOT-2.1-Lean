#!/usr/bin/env python3
"""Ingest Cosmology Lab Wave-4 observables."""

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
MANIFEST_PATH = ROOT / "data" / "cosmology_wave4_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from cosmology_wave4 import summarize_wave4, wave4_observables  # noqa: E402


def ingest_wave4(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["cosmology_root"])
    compute_path = root / manifest["artifacts"]["fsot_compute"]["path"]
    mod = load_fsot_compute(compute_path)
    rows = wave4_observables(mod)
    return {"present": compute_path.exists(), "compute_path": str(compute_path), "rows": rows, **summarize_wave4(rows)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()
    wave4 = ingest_wave4()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["cosmology_wave4"] = wave4
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  wave4 observables: {wave4['observable_count']}  max err: {wave4['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())