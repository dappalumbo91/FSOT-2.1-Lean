#!/usr/bin/env python3
"""Tier 90 — consciousness expansion ingests (AnAge, microtubule anchors, OpenNeuro)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier90_consciousness_expansion_lib import INGESTORS, cache_root  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    parser.add_argument(
        "--external-root",
        default="",
        help="Override FSOT_EXTERNAL_DATA_ROOT / FSOT_ANOMALY_CACHE_ROOT",
    )
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER90_DEEP"] = "1"
    if args.external_root:
        os.environ["FSOT_EXTERNAL_DATA_ROOT"] = args.external_root
        os.environ["FSOT_ANOMALY_CACHE_ROOT"] = args.external_root
    elif not os.environ.get("FSOT_EXTERNAL_DATA_ROOT"):
        for candidate in ("G:/FSOT-PublicData", "D:/FSOT-2.1-Lean-PublicData"):
            if Path(candidate).exists():
                os.environ["FSOT_EXTERNAL_DATA_ROOT"] = candidate
                os.environ["FSOT_ANOMALY_CACHE_ROOT"] = candidate
                break
    print(f"Consciousness cache: {cache_root()}")
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = (
            doc.get("merged_species_count")
            or doc.get("dataset_count")
            or doc.get("resonance_meta", {}).get("practice_count")
            or 0
        )
        print(f"{key}: {count} ({doc.get('source')})")
    print("\nAll Tier 90 consciousness expansion ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())