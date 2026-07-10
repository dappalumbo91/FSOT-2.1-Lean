#!/usr/bin/env python3
"""Build Tier 61 music / XR-game / creative arts benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier61_creative_media_lib import BUILDERS, output_path  # noqa: E402

BUILD_ORDER = [
    "Music_Harmonics_Public_Panel",
    "XR_Interactive_Media_Math_Scaffold",
    "Creative_Arts_Math_Spine",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or BUILD_ORDER
    if "Creative_Arts_Math_Spine" in domains:
        for prereq in ("Music_Harmonics_Public_Panel", "XR_Interactive_Media_Math_Scaffold"):
            if prereq not in domains:
                domains = [d for d in BUILD_ORDER if d in set(domains) | {prereq}]
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{domain}: {doc.get('record_count')} records, pooled {doc.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())