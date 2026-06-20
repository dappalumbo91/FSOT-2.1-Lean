#!/usr/bin/env python3
"""Ingest Math Generator FSOT formula comparisons into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "math_generator_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from math_generator_lab import load_comparison_report, summarize_math_generator  # noqa: E402


def ingest_math_generator(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    math_root = Path(manifest["math_generator_root"])
    report_path = math_root / manifest["artifacts"]["comparison_report"]["path"]
    data = load_comparison_report(report_path) if report_path.exists() else {}
    return {
        "present": report_path.exists(),
        "math_generator_root": str(math_root),
        "report_path": str(report_path),
        **summarize_math_generator(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Math Generator comparison report")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    math_gen = ingest_math_generator()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["math_generator_lab"] = math_gen
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(
        f"  comparisons: {math_gen.get('comparison_count')}  "
        f"max err: {math_gen.get('max_error_pct', 0):.4f}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())