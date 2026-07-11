#!/usr/bin/env python3
"""Bundle portable knowledge-base summary + optional transfer symlink for GitHub clones."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "knowledge_base_manifest.yaml"
VENDOR_KB = ROOT / "vendor" / "knowledge_base"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import (  # noqa: E402
    knowledge_base_transfer_path,
    knowledge_base_validation_path,
    rel_repo_path,
    strict_empirical_jsonl_path,
)
from knowledge_base_corpus import load_unified_transfer, summarize_knowledge_base  # noqa: E402
from knowledge_base_formula_verify import summarize_knowledge_base_formulas  # noqa: E402


def bundle(*, copy_transfer: bool = False) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    VENDOR_KB.mkdir(parents=True, exist_ok=True)
    (VENDOR_KB / "transfer").mkdir(parents=True, exist_ok=True)
    (VENDOR_KB / "export").mkdir(parents=True, exist_ok=True)

    transfer_src = knowledge_base_transfer_path(require=False)
    validation_src = knowledge_base_validation_path(require=False)
    strict_path = strict_empirical_jsonl_path(require=False)

    transfer_dest = VENDOR_KB / manifest["artifacts"]["unified_transfer"]["path"]
    validation_dest = VENDOR_KB / manifest["artifacts"]["validation_export"]["path"]
    summary_dest = VENDOR_KB / manifest["artifacts"]["portable_summary"]["path"]

    if copy_transfer and transfer_src and transfer_src.exists():
        shutil.copy2(transfer_src, transfer_dest)

    if validation_src and validation_src.exists() and validation_src.resolve() != validation_dest.resolve():
        shutil.copy2(validation_src, validation_dest)

    transfer_live = transfer_src if transfer_src and transfer_src.exists() else transfer_dest
    transfer_data = load_unified_transfer(transfer_live) if transfer_live.exists() else {}
    formula_stats = (
        summarize_knowledge_base_formulas(transfer_data, strict_path)
        if transfer_live.exists()
        else {}
    )
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "transfer_present": transfer_live.exists(),
        "validation_present": validation_dest.exists(),
        "transfer_path": rel_repo_path(transfer_live) if transfer_live.exists() else None,
        "validation_path": rel_repo_path(validation_dest) if validation_dest.exists() else None,
        "strict_empirical_path": rel_repo_path(strict_path) if strict_path else None,
        **summarize_knowledge_base(transfer_data),
        **formula_stats,
    }
    summary_dest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--copy-transfer",
        action="store_true",
        help="Copy full Desktop transfer JSON into vendor/knowledge_base (large ~35MB)",
    )
    args = parser.parse_args()
    summary = bundle(copy_transfer=args.copy_transfer)
    print(f"Wrote {VENDOR_KB / 'kb_portable_summary.json'}")
    print(
        f"  sources={summary.get('source_count')} catalog={summary.get('catalog_formulas')} "
        f"transfer_present={summary.get('transfer_present')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())