#!/usr/bin/env python3
"""Tier 87 — Core domain depth wave ingests."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier87_scientific_expansion_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER87_DEEP"] = "1"
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = (
            doc.get("rule_count")
            or doc.get("stratum_count")
            or doc.get("superconductor_count")
            or doc.get("interferometer_count")
            or 0
        )
        print(f"{key}: {count} records ({doc.get('source')})")
    print("\nAll Tier 87 scientific expansion ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())