#!/usr/bin/env python3
"""Tier 94 — AnAge longevity catalog + extreme species NCBI cross-walk."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier94_longevity_genetics_lib import INGESTORS, cache_root, enrich_genome_crosswalk  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--megadeep", action="store_true")
    parser.add_argument("--enrich-genomes", action="store_true")
    parser.add_argument("--force-genomes", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    parser.add_argument("--external-root", default="")
    args = parser.parse_args()
    if args.deep or args.megadeep:
        os.environ["FSOT_TIER94_DEEP"] = "1"
    if args.megadeep:
        os.environ["FSOT_API_MEGA_DEEP"] = "1"
    if args.external_root:
        os.environ["FSOT_EXTERNAL_DATA_ROOT"] = args.external_root
    elif not os.environ.get("FSOT_EXTERNAL_DATA_ROOT"):
        for candidate in (
            r"I:\FSOT-Physical-Archive\03_FSOT-PublicData",
            r"G:\FSOT-PublicData",
        ):
            if Path(candidate).exists():
                os.environ["FSOT_EXTERNAL_DATA_ROOT"] = candidate
                break
    print(f"Longevity genetics cache: {cache_root()}")
    if args.enrich_genomes and not args.only:
        doc = enrich_genome_crosswalk(force=args.force_genomes)
        print(f"enrich_genome_crosswalk: updated={doc.get('updated_count')} caches={doc.get('caches')}")
        print("\nTier 94 longevity genetics ingests complete.")
        return 0
    keys = args.only or sorted(k for k in INGESTORS if k != "enrich_genome_crosswalk")
    if args.enrich_genomes and "enrich_genome_crosswalk" not in keys:
        keys = ["enrich_genome_crosswalk", *keys]
    for key in keys:
        if key == "enrich_genome_crosswalk":
            doc = enrich_genome_crosswalk(force=args.force_genomes)
            print(f"{key}: updated={doc.get('updated_count')} caches={doc.get('caches')}")
            continue
        doc = INGESTORS[key]()
        print(f"{key}: catalog={doc.get('catalog_count', doc.get('species_count'))}")
    print("\nTier 94 longevity genetics ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())