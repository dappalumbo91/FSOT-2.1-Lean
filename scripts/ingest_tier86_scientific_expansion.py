#!/usr/bin/env python3
"""Tier 86 — Pure Mathematics closure + audit depth wave ingests."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier86_scientific_expansion_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER86_DEEP"] = "1"
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = (
            doc.get("constant_count")
            or doc.get("stratum_count")
            or doc.get("compound_count")
            or doc.get("bridge_count")
            or doc.get("metric_count")
            or 0
        )
        print(f"{key}: {count} records ({doc.get('source')})")
    print("\nAll Tier 86 scientific expansion ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())