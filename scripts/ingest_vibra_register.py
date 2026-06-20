#!/usr/bin/env python3
"""Ingest VibraFSOT + FSOTLean MC alignment into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "vibra_register_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from vibra_register import load_mc_report, load_vibra_progress, summarize_vibra  # noqa: E402


def ingest_vibra(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    vibra_root = Path(manifest["vibra_root"])
    lean_root = Path(manifest["fsotlean_root"])
    vibra_path = vibra_root / manifest["artifacts"]["vibra_progress"]["path"]
    mc_path = lean_root / manifest["artifacts"]["mc_report"]["path"]
    vibra = load_vibra_progress(vibra_path)
    mc = load_mc_report(mc_path)
    return {
        "present": vibra_path.exists() and mc_path.exists(),
        "vibra_path": str(vibra_path),
        "mc_report_path": str(mc_path),
        **summarize_vibra(vibra, mc),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest VibraFSOT register + MC report")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    vibra = ingest_vibra()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["vibra_register"] = vibra
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  d_eff={vibra['d_eff']}  pattern_stability={vibra['pattern_stability']:.4f}")
    print(f"  mc_prob_non_decrease@cp{vibra['mc_checkpoint']}={vibra['mc_prob_non_decrease']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())