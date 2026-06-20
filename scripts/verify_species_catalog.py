#!/usr/bin/env python3
"""Verify FSOT Machine & Molecule species catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "species_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from species_catalog import flatten_catalog, load_catalog, summarize_species  # noqa: E402


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_species(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    root = Path(manifest["machine_molecule_root"])
    catalog_path = root / manifest["artifacts"]["catalog_json"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not catalog_path.exists():
        return [f"missing species catalog: {catalog_path}"], {}

    catalog = load_catalog(catalog_path)
    live_rows = flatten_catalog(catalog)
    live_summary = summarize_species(catalog, live_rows)
    stored = registry.get("species_catalog", {})

    if not stored:
        issues.append("species_catalog: not ingested — run ingest_species_catalog.py")
    elif live_summary["species_count"] != stored.get("species_count"):
        issues.append("species_catalog: species_count mismatch vs live catalog")

    if live_summary["species_count"] < ver.get("species_count_min", 140):
        issues.append(f"species_catalog: species_count={live_summary['species_count']} below minimum")
    if live_summary["property_count"] < ver.get("property_count_min", 900):
        issues.append(f"species_catalog: property_count={live_summary['property_count']} below minimum")

    max_tol = ver.get("max_error_pct", 5.0)
    if live_summary["max_error_pct"] > max_tol:
        issues.append(
            f"species_catalog: max_error_pct={live_summary['max_error_pct']:.4f}% > {max_tol}%"
        )

    for row in live_rows:
        err = row.get("error_pct")
        if err is None:
            issues.append(f"species {row['species_id']} {row['property']}: missing error_pct")
        elif err > max_tol:
            issues.append(
                f"species {row['species_id']} {row['property']}: error_pct={err:.4f}% > {max_tol}%"
            )

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_species()
    print("=== Species catalog verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:10]:
            print(f"    - {item}")
        if len(issues) > 10:
            print(f"    ... and {len(issues) - 10} more")
        return 1
    print("  All species catalog checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())