#!/usr/bin/env python3
"""Verify FSOT Fuel Lab compound lookup profiles."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "fuel_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fuel_compounds import load_profiles, summarize_fuel  # noqa: E402


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_fuel(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    fuel_root = Path(manifest["fuel_root"])
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not fuel_root.exists():
        return [f"missing fuel lab root: {fuel_root}"], {}

    live_profiles = load_profiles(fuel_root)
    live_summary = summarize_fuel(live_profiles)
    stored = registry.get("fuel_lab", {})

    if not stored:
        issues.append("fuel_lab: not ingested — run ingest_fuel_lab.py")
    elif live_summary["profile_count"] != stored.get("profile_count"):
        issues.append(
            f"fuel_lab: profile_count={stored.get('profile_count')} != live {live_summary['profile_count']}"
        )

    if live_summary["profile_count"] < ver.get("profile_count_min", 30):
        issues.append(f"fuel_lab: only {live_summary['profile_count']} profiles")

    frac_tol = ver.get("composition_fraction_tolerance", 0.05)
    required = ver.get("resolved_entry_requires", ["molecular_formula", "inchi_key"])

    for profile in live_profiles:
        pid = profile["profile_id"]
        comp_sum = profile.get("composition_fraction_sum", 0.0)
        if comp_sum > 1.0 + frac_tol:
            issues.append(f"fuel_lab {pid}: composition fractions sum {comp_sum:.3f} > 1 + {frac_tol}")
        for row in profile.get("rows", []):
            if not row.get("resolved"):
                continue
            for field in required:
                if not row.get(field):
                    issues.append(f"fuel_lab {pid} {row['key']}: resolved entry missing {field}")

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_fuel()
    print("=== Fuel Lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:15]:
            print(f"    - {item}")
        return 1
    print("  All Fuel Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())