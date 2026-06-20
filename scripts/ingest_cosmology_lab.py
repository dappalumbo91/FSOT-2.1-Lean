#!/usr/bin/env python3
"""Ingest FSOT Cosmology Lab ΛCDM observables into lab_registry.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "cosmology_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import lambda_cdm_observables, load_fsot_compute, summarize_lambda  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def ingest_cosmology(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["cosmology_root"])
    compute_path = root / manifest["artifacts"]["fsot_compute"]["path"]
    mod = load_fsot_compute(compute_path)
    rows = lambda_cdm_observables(mod)
    summary = summarize_lambda(rows)
    return {
        "present": compute_path.exists(),
        "compute_path": str(compute_path),
        "compute_sha256": sha256_file(compute_path) if compute_path.exists() else None,
        "rows": rows,
        **summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Cosmology Lab ΛCDM observables")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    cosmology = ingest_cosmology()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["cosmology_lambda_cdm"] = cosmology
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  observables: {cosmology['observable_count']} (w1={cosmology['wave1_count']}, w2={cosmology['wave2_count']}, w3={cosmology['wave3_cosmology_count']})")
    print(f"  max error: {cosmology['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())