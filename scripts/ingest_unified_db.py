#!/usr/bin/env python3
"""Ingest FSOT Unified Database verification report into lab_registry.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "unified_db_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
INDEX_PATH = ROOT / "data" / "unified_db_domain_index.json"
BUILD_INDEX_SCRIPT = ROOT / "scripts" / "build_unified_db_domain_index.py"

sys.path.insert(0, str(ROOT / "scripts"))
from unified_db_meta import (  # noqa: E402
    load_verification_report,
    summarize_unified_db,
    summarize_unified_index,
)


def ingest_unified_db(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["unified_root"])
    report_path = root / manifest["artifacts"]["verification_report"]["path"]
    report = load_verification_report(report_path)

    subprocess.run(
        [sys.executable, str(BUILD_INDEX_SCRIPT), "--output", str(INDEX_PATH)],
        check=True,
        cwd=str(ROOT),
    )
    index_summary = summarize_unified_index(INDEX_PATH)

    return {
        "present": report_path.exists(),
        "report_path": str(report_path),
        **summarize_unified_db(report),
        **index_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest unified DB meta certificate")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    unified = ingest_unified_db()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["unified_db"] = unified
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  strict_empirical: {unified['strict_empirical']}  evaluation_ok: {unified['evaluation_ok']}")
    print(f"  records_total: {unified.get('records_total')}  top_projects: {unified.get('top_project_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())