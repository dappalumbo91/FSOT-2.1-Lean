#!/usr/bin/env python3
"""Tier 91 — foundational ontology ingests."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier91_foundational_ontology_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER91_DEEP"] = "1"
    for key in args.only or sorted(INGESTORS.keys()):
        doc = INGESTORS[key]()
        print(f"{key}: axiom_count={doc.get('axiom_count')} friction={doc.get('phase_bleed_friction')}")
    print("\nTier 91 foundational ontology ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())