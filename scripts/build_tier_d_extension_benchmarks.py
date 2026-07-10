#!/usr/bin/env python3
"""Build Tier D extension domain v1.1 benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier_d_extension_lib import BUILDERS, TIER_D, ingest_tier_d_data, output_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()

    if args.ingest:
        summary = ingest_tier_d_data()
        print(json.dumps(summary, indent=2))

    domains = args.only or TIER_D
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        med = doc.get("pooled_median_error_pct") or doc.get("median_error_pct")
        print(f"{domain}: {doc.get('record_count')} records, pooled median {med}% -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())