#!/usr/bin/env python3
"""Ingest FSOT_Lean_Proofs formal constant bridge into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "lean_proofs_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from lean_proofs_bridge import load_formal_output, summarize_lean_proofs  # noqa: E402


def ingest_lean_proofs(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    lean_root = Path(manifest["lean_proofs_root"])
    output_path = lean_root / manifest["artifacts"]["formal_output"]["path"]
    data = load_formal_output(output_path) if output_path.exists() else {}
    return {
        "present": output_path.exists(),
        "lean_proofs_root": str(lean_root),
        "formal_output_path": str(output_path),
        **summarize_lean_proofs(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Lean Proofs formal constant bridge")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    bridge = ingest_lean_proofs()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["lean_proofs_bridge"] = bridge
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(
        f"  formal_constants: {bridge.get('formal_constant_count')}  "
        f"domain_proven: {bridge.get('domain_proven_count')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())