#!/usr/bin/env python3
"""Verify FSOT Unified Database meta-oracle certificate."""

from __future__ import annotations

import json
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

sys.path.insert(0, str(ROOT / "scripts"))
from unified_db_meta import (  # noqa: E402
    load_verification_report,
    summarize_unified_db,
    summarize_unified_index,
)


def verify_unified_db(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["unified_root"])
    report_path = root / manifest["artifacts"]["verification_report"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not report_path.exists():
        return [f"missing unified DB report: {report_path}"], {}

    live = summarize_unified_db(load_verification_report(report_path))
    if not registry.get("unified_db"):
        issues.append("unified_db: not ingested — run ingest_unified_db.py")
    if (live.get("total_candidates") or 0) < ver.get("total_candidates_min", 13000):
        issues.append(f"unified_db: total_candidates={live.get('total_candidates')}")
    if (live.get("strict_empirical") or 0) < ver.get("strict_empirical_min", 9000):
        issues.append(f"unified_db: strict_empirical={live.get('strict_empirical')}")
    if (live.get("evaluation_ok") or 0) < ver.get("evaluation_ok_min", 140):
        issues.append(f"unified_db: evaluation_ok={live.get('evaluation_ok')}")

    if not INDEX_PATH.exists():
        issues.append(f"unified_db: missing domain index — run ingest_unified_db.py ({INDEX_PATH})")
    else:
        index_live = summarize_unified_index(INDEX_PATH)
        records_total = index_live.get("records_total") or 0
        if records_total < ver.get("records_total_min", 30000):
            issues.append(f"unified_db: records_total={records_total} < 30000")
        live = {**live, **index_live}

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_unified_db()
    print("=== Unified DB verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All unified DB checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())