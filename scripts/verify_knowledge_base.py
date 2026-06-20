#!/usr/bin/env python3
"""Verify FSOT Knowledge Base unified transfer corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "knowledge_base_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from knowledge_base_corpus import load_unified_transfer, summarize_knowledge_base  # noqa: E402


def verify_knowledge_base(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    knowledge_root = Path(manifest["knowledge_root"])
    transfer_path = knowledge_root / manifest["artifacts"]["unified_transfer"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not transfer_path.exists():
        return [f"missing knowledge transfer: {transfer_path}"], {}

    live = summarize_knowledge_base(load_unified_transfer(transfer_path))
    stored = registry.get("knowledge_base", {})

    if not stored:
        issues.append("knowledge_base: not ingested — run ingest_knowledge_base.py")

    if (live.get("source_count") or 0) < ver.get("source_count_min", 30):
        issues.append(f"knowledge_base: source_count={live.get('source_count')}")
    if (live.get("catalog_formulas") or 0) < ver.get("catalog_formulas_min", 19000):
        issues.append(f"knowledge_base: catalog_formulas={live.get('catalog_formulas')}")
    if (live.get("observable_citations") or 0) < ver.get("observable_citations_min", 1800):
        issues.append(f"knowledge_base: observable_citations={live.get('observable_citations')}")
    if (stored.get("observable_verified_formulas") or 0) < ver.get("observable_verified_min", 7900):
        issues.append(
            f"knowledge_base: observable_verified_formulas={stored.get('observable_verified_formulas')}"
        )

    summary = {**live, **{k: stored.get(k) for k in (
        "observable_verified_formulas", "observable_verified_matched",
        "within_target_2pct", "within_tolerable_5pct",
    )}, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_knowledge_base()
    print("=== Knowledge Base verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Knowledge Base checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())