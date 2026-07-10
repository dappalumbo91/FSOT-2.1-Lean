#!/usr/bin/env python3
"""Build Tier A/B/C neurolab gap-fill v1.1 benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier_gap_fill_lib import BUILDERS, TIER_A, TIER_C, output_path, rebuild_tier38_benchmarks  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["A", "C", "all"], default="all")
    parser.add_argument("--only", action="append", choices=sorted(BUILDERS.keys()))
    parser.add_argument("--refresh-tier38", action="store_true")
    args = parser.parse_args()

    if args.refresh_tier38:
        print("Refreshing Tier 38 public API benchmarks...")
        rebuild_tier38_benchmarks()

    if args.only:
        domains = args.only
    elif args.tier == "A":
        domains = TIER_A
    elif args.tier == "C":
        domains = TIER_C
    else:
        domains = TIER_A + TIER_C

    for domain in domains:
        builder = BUILDERS[domain]
        doc = builder()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"  {domain}: records={doc['record_count']} "
            f"pooled_median={doc.get('median_error_pct'):.4f}% -> {out.name}"
        )
    print(f"Built {len(domains)} gap-fill benchmarks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())