#!/usr/bin/env python3
"""Ingest strict-empirical formula corpus into lab_registry."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "formula_corpus_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from formula_corpus import load_strict_empirical_jsonl, summarize_formula_corpus  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    corpus_path = Path(manifest["corpus_root"]) / manifest["artifacts"]["strict_empirical_jsonl"]["path"]
    rows = load_strict_empirical_jsonl(corpus_path)
    summary = summarize_formula_corpus(rows)

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else {}
    registry["formula_corpus"] = {
        **summary,
        "corpus_path": str(corpus_path),
        "verification_tier": "numeric_formula",
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY_PATH}")
    print(f"  records: {summary['records_total']}  matched: {summary['matched_count']}")
    print(f"  within 2%: {summary['within_target_2pct']}  within 5%: {summary['within_tolerable_5pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())