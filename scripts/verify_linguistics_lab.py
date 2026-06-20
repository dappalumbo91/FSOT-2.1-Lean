#!/usr/bin/env python3
"""Verify FSOT linguistics empirical anchor derivations."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "linguistics_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from linguistics_targets import (  # noqa: E402
    load_derivations_db,
    load_targets_csv,
    merge_targets,
    summarize_linguistics,
)


def verify_linguistics(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["linguistics_root"])
    csv_path = root / manifest["artifacts"]["targets_csv"]["path"]
    db_path = root / manifest["artifacts"]["derivations_db"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not csv_path.exists():
        return [f"missing linguistics targets: {csv_path}"], {}

    rows = merge_targets(load_targets_csv(csv_path), load_derivations_db(db_path))
    live = summarize_linguistics(rows)
    if not registry.get("linguistics_lab"):
        issues.append("linguistics_lab: not ingested — run ingest_linguistics_lab.py")
    if live["target_count"] != ver.get("target_count", 10):
        issues.append(f"linguistics_lab: target_count={live['target_count']} != {ver.get('target_count')}")
    if live["derived_count"] < ver.get("target_count", 10):
        issues.append(f"linguistics_lab: only {live['derived_count']} derivations")
    max_tol = ver.get("max_error_pct", 5.0)
    for row in rows:
        err = row.get("error_pct")
        if err is None:
            issues.append(f"linguistics {row['name']}: missing derivation")
        elif abs(err) > max_tol:
            issues.append(f"linguistics {row['name']}: error_pct={err:.4f}% > {max_tol}%")
    if live["max_error_pct"] > max_tol:
        issues.append(f"linguistics_lab: max_error_pct={live['max_error_pct']:.4f}%")

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_linguistics()
    print("=== Linguistics Lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:15]:
            print(f"    - {item}")
        return 1
    print("  All linguistics Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())