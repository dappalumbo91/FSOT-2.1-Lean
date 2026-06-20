#!/usr/bin/env python3
"""Ingest Genetics CAMEO benchmarks into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "cameo_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cameo_benchmarks import load_cameo_results, summarize_cameo  # noqa: E402


def ingest_cameo(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    genetics_root = Path(manifest["genetics_root"])
    csv_path = genetics_root / manifest["artifacts"]["results_csv"]
    rows = load_cameo_results(csv_path)
    symbolic = manifest.get("symbolic_formula", {})
    return {
        "present": csv_path.exists(),
        "genetics_root": str(genetics_root),
        "results_path": str(csv_path),
        "symbolic_formula": symbolic,
        "rows": rows,
        **summarize_cameo(rows, symbolic),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Genetics CAMEO benchmarks")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    cameo = ingest_cameo()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["cameo_lab"] = cameo
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  benchmarks: {cameo['benchmark_count']}")
    print(f"  mean top-L prec: {cameo['mean_top_l_prec']:.2f}%")
    print(f"  symbolic MAE: {cameo.get('mae_angstrom', 'n/a')} Å")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())