#!/usr/bin/env python3
"""Verify Cosmology Lab Wave-4 observables."""

from __future__ import annotations

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


def verify_wave4(manifest_path: Path = MANIFEST_PATH, registry_path: Path = REGISTRY_PATH) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["cosmology_root"])
    compute_path = root / manifest["artifacts"]["fsot_compute"]["path"]
    issues: list[str] = []
    if not compute_path.exists():
        return [f"missing compute: {compute_path}"], {}
    mod = load_fsot_compute(compute_path)
    live = summarize_wave4(wave4_observables(mod))
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    if not registry.get("cosmology_wave4"):
        issues.append("cosmology_wave4: not ingested")
    max_tol = ver.get("max_error_pct", 2.0)
    for row in wave4_observables(mod):
        err = row.get("error_pct")
        if err is not None and err > max_tol:
            issues.append(f"wave4 {row['name']}: {err:.4f}% > {max_tol}%")
    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_wave4()
    print("=== Cosmology Wave-4 verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Wave-4 checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())