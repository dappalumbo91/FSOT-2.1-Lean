#!/usr/bin/env python3
"""Verify FSOT_Lean_Proofs formal constant bridge output."""

from __future__ import annotations

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


def verify_lean_proofs(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    lean_root = Path(manifest["lean_proofs_root"])
    output_path = lean_root / manifest["artifacts"]["formal_output"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not output_path.exists():
        return [f"missing Lean proofs output: {output_path}"], {}

    live = summarize_lean_proofs(load_formal_output(output_path))
    stored = registry.get("lean_proofs_bridge", {})

    if not stored:
        issues.append("lean_proofs_bridge: not ingested — run ingest_lean_proofs_bridge.py")

    if (live.get("formal_constant_count") or 0) < ver.get("formal_constant_count_min", 25):
        issues.append(f"lean_proofs_bridge: formal_constant_count={live.get('formal_constant_count')}")
    if (live.get("domain_proven_count") or 0) < ver.get("domain_proven_min", 25):
        issues.append(f"lean_proofs_bridge: domain_proven_count={live.get('domain_proven_count')}")

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_lean_proofs()
    print("=== Lean Proofs Bridge verification ===")
    for k, v in summary.items():
        if k != "issues" and k != "formal_names":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Lean Proofs Bridge checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())