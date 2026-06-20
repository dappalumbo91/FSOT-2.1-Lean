#!/usr/bin/env python3
"""Verify FSOT magnetic string lattice simulation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "magnetic_strings_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from magnetic_strings import load_magnetic_strings, summarize_magnetic_strings  # noqa: E402


def verify_magnetic(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["magnetic_root"])
    json_path = root / manifest["artifacts"]["final_json"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not json_path.exists():
        return [f"missing magnetic strings JSON: {json_path}"], {}

    live = summarize_magnetic_strings(load_magnetic_strings(json_path))
    if not registry.get("magnetic_strings"):
        issues.append("magnetic_strings: not ingested — run ingest_magnetic_strings.py")
    if live["string_count"] < ver.get("string_count_min", 250):
        issues.append(f"magnetic_strings: only {live['string_count']} strings")
    if (live.get("S_em") or 0) < ver.get("S_em_min", 0.4):
        issues.append(f"magnetic_strings: S_em={live.get('S_em')} below minimum")
    if live["top_aligned_count"] < ver.get("top_aligned_min", 50):
        issues.append(f"magnetic_strings: top_aligned={live['top_aligned_count']} below minimum")

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_magnetic()
    print("=== Magnetic strings verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All magnetic string checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())