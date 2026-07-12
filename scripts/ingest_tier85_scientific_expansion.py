#!/usr/bin/env python3
"""Tier 85 — Tier-41 gap domains with live FSOT prediction ingests (credential-free)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier85_scientific_expansion_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER85_DEEP"] = "1"
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = (
            doc.get("metric_count")
            or doc.get("planet_count")
            or doc.get("work_count")
            or doc.get("row_count")
            or doc.get("record_count")
            or doc.get("site_count")
            or 0
        )
        print(f"{key}: {count} records ({doc.get('source')})")
    print("\nAll Tier 85 scientific expansion ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())