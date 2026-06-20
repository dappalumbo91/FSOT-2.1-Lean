#!/usr/bin/env python3
"""Ingest FSOT Knowledge Base unified transfer corpus into lab_registry.json."""

from __future__ import annotations

import argparse
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
from knowledge_base_formula_verify import summarize_knowledge_base_formulas  # noqa: E402


def ingest_knowledge_base(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    knowledge_root = Path(manifest["knowledge_root"])
    transfer_path = knowledge_root / manifest["artifacts"]["unified_transfer"]["path"]
    data = load_unified_transfer(transfer_path) if transfer_path.exists() else {}
    strict_path = Path(
        r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\by_domain\strict_empirical.jsonl"
    )
    formula_stats = (
        summarize_knowledge_base_formulas(data, strict_path)
        if transfer_path.exists() and strict_path.exists()
        else {}
    )
    return {
        "present": transfer_path.exists(),
        "knowledge_root": str(knowledge_root),
        "transfer_path": str(transfer_path),
        **summarize_knowledge_base(data),
        **formula_stats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Knowledge Base unified transfer")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    kb = ingest_knowledge_base()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["knowledge_base"] = kb
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  sources: {kb.get('source_count')}  catalog_formulas: {kb.get('catalog_formulas')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())