#!/usr/bin/env python3
"""Build organized unified-DB domain/project index for Lean repo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "unified_db_manifest.yaml"
OUTPUT_PATH = ROOT / "data" / "unified_db_domain_index.json"


def build_index(index_path: Path, report_path: Path) -> dict:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    counts = index.get("counts", {})
    return {
        "generated_from": str(index_path),
        "records_total": counts.get("records_total"),
        "records_science": counts.get("records_science"),
        "records_mathematics": counts.get("records_mathematics"),
        "records_strict_empirical": counts.get("records_strict_empirical"),
        "projects": counts.get("projects"),
        "formula_lineages": counts.get("formula_lineages"),
        "top_projects": index.get("top_projects", [])[:15],
        "verification_candidates": report.get("candidate_counts", {}),
        "numeric_evaluation": report.get("numeric_evaluation", {}),
        "outputs": {
            "by_domain_dir": index.get("outputs", {}).get("by_domain_dir"),
            "by_project_dir": index.get("outputs", {}).get("by_project_dir"),
            "strict_empirical_jsonl": index.get("outputs", {}).get("strict_empirical"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build unified DB domain index")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required")
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    unified_root = Path(manifest["unified_root"])
    index_path = unified_root / "database" / "FSOT_UNIFIED_INDEX.json"
    report_path = unified_root / manifest["artifacts"]["verification_report"]["path"]

    if not index_path.exists():
        raise SystemExit(f"missing index: {index_path}")

    payload = build_index(index_path, report_path)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records_total: {payload['records_total']}")
    print(f"  strict_empirical: {payload['records_strict_empirical']}")
    print(f"  top_projects: {len(payload['top_projects'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())