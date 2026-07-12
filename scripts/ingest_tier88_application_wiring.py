#!/usr/bin/env python3
"""Tier 88 — Desktop application wiring ingests."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier88_application_wiring_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER88_DEEP"] = "1"
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = (
            doc.get("profile_count")
            or doc.get("case_count")
            or doc.get("organ_count")
            or doc.get("configured_path_count")
            or 0
        )
        print(f"{key}: {count} records ({doc.get('source')})")
    print("\nAll Tier 88 application wiring ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())