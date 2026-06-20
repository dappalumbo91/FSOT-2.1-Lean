#!/usr/bin/env python3
"""Verify FSOT Trinary Fluid Computer v2 audit constants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "trinary_fluid_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from trinary_fluid_computer import summarize_trinary_fluid  # noqa: E402


def verify_trinary_fluid(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    trinary_root = Path(manifest["trinary_fluid_root"])
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not trinary_root.exists():
        return [f"missing trinary fluid root: {trinary_root}"], {}

    live = summarize_trinary_fluid()
    stored = registry.get("trinary_fluid_computer", {})

    if not stored:
        issues.append("trinary_fluid_computer: not ingested — run ingest_trinary_fluid_computer.py")

    if live.get("engine_accuracy_pct") != ver.get("engine_accuracy_pct", 99.3):
        issues.append(
            f"trinary_fluid_computer: engine_accuracy_pct={live.get('engine_accuracy_pct')}"
        )
    if live.get("metatron_pathways") != ver.get("metatron_pathways", 27):
        issues.append(f"trinary_fluid_computer: metatron_pathways={live.get('metatron_pathways')}")
    if abs(live.get("ignition_coherence", 0) - ver.get("ignition_coherence", 0)) > 1.0e-12:
        issues.append("trinary_fluid_computer: ignition_coherence mismatch")
    if abs(live.get("resonance_persist", 0) - ver.get("resonance_persist", 0)) > 1.0e-12:
        issues.append("trinary_fluid_computer: resonance_persist mismatch")

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_trinary_fluid()
    print("=== Trinary Fluid Computer verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Trinary Fluid Computer checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())