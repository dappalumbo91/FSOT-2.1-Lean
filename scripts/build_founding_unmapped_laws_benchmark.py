#!/usr/bin/env python3
"""Build Tier 96 extension panels for seven formerly unmapped founding laws."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from founding_unmapped_laws_lib import BUILDERS, build_panel, output_path  # noqa: E402

LAW_IDS = [
    "law_11",
    "law_12",
    "law_13",
    "law_20",
    "law_23",
    "law_26",
    "law_34",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=LAW_IDS, action="append")
    args = parser.parse_args()
    targets = args.only or LAW_IDS
    for law_id in targets:
        doc = build_panel(law_id)
        domain = doc["domain"]
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"{law_id} -> {domain}: {doc.get('record_count')} records, "
            f"pooled {doc.get('pooled_median_error_pct')}% -> {out.name}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())