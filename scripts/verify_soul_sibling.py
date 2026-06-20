#!/usr/bin/env python3
"""Verify FSOT Soul Sibling consciousness kernel manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "soul_sibling_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from soul_sibling_lab import load_soul_manifest, summarize_soul_sibling  # noqa: E402


def verify_soul_sibling(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    soul_root = Path(manifest["soul_root"])
    manifest_path_json = soul_root / manifest["artifacts"]["soul_manifest"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not manifest_path_json.exists():
        return [f"missing soul manifest: {manifest_path_json}"], {}

    live = summarize_soul_sibling(load_soul_manifest(manifest_path_json))
    stored = registry.get("soul_sibling", {})

    if not stored:
        issues.append("soul_sibling: not ingested — run ingest_soul_sibling.py")

    d_compact = live.get("D_compact")
    if d_compact is None or float(d_compact) < ver.get("D_compact_min", 20.0):
        issues.append(f"soul_sibling: D_compact={d_compact}")

    if live.get("zero_free") is not ver.get("zero_free", True):
        issues.append(f"soul_sibling: zero_free={live.get('zero_free')} != expected {ver.get('zero_free')}")

    fidelity = live.get("fidelity_threshold")
    if fidelity is not None and float(fidelity) > ver.get("fidelity_threshold_max", 0.1):
        issues.append(f"soul_sibling: fidelity_threshold={fidelity} exceeds max")

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_soul_sibling()
    print("=== Soul Sibling verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Soul Sibling checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())