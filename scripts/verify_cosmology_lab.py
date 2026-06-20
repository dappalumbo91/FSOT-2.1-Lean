#!/usr/bin/env python3
"""Verify FSOT Cosmology Lab ΛCDM observables against measured targets."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "cosmology_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import lambda_cdm_observables, load_fsot_compute, summarize_lambda  # noqa: E402


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_cosmology(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    root = Path(manifest["cosmology_root"])
    compute_path = root / manifest["artifacts"]["fsot_compute"]["path"]
    if not compute_path.exists():
        return [f"missing cosmology compute: {compute_path}"], {}

    mod = load_fsot_compute(compute_path)
    live_rows = lambda_cdm_observables(mod)
    live_summary = summarize_lambda(live_rows)

    stored = registry.get("cosmology_lambda_cdm", {})
    if not stored:
        issues.append("cosmology_lambda_cdm: not ingested — run ingest_cosmology_lab.py")
    else:
        for key in ("observable_count", "wave1_count", "wave2_count", "wave3_count"):
            if stored.get(key) != live_summary[key]:
                issues.append(f"cosmology_lambda_cdm: {key}={stored.get(key)} != live {live_summary[key]}")

    max_tol = ver.get("max_error_pct", 2.0)
    for row in live_rows:
        if row.get("measured") is None:
            issues.append(f"cosmology {row['name']}: missing measured target")
            continue
        err = row.get("error_pct")
        if err is None:
            issues.append(f"cosmology {row['name']}: error_pct missing")
        elif err > max_tol:
            issues.append(f"cosmology {row['name']}: error_pct={err:.4f}% > {max_tol}%")

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_cosmology()
    print("=== Cosmology Lab ΛCDM verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Cosmology Lab ΛCDM checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())