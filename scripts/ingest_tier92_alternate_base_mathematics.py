#!/usr/bin/env python3
"""Tier 92 — alternate base mathematics explorer ingests."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier92_alternate_base_mathematics_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER92_DEEP"] = "1"
    for key in args.only or sorted(INGESTORS.keys()):
        doc = INGESTORS[key]()
        print(f"{key}: bases={doc.get('bases_analyzed')} best={doc.get('best_fsot_alignment_base')}")
    print("\nTier 92 alternate base mathematics ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())