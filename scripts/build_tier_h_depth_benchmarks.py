#!/usr/bin/env python3
"""Run Tier H depth pass on Malware + Code Genome domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier_h_cybersecurity_lib import output_path  # noqa: E402
from tier_h_depth_lib import BUILDERS, TIER_H_DEPTH  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=TIER_H_DEPTH, action="append")
    args = parser.parse_args()
    domains = args.only or TIER_H_DEPTH
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        med = doc.get("pooled_median_error_pct")
        print(f"{domain}: {doc.get('record_count')} records, pooled median {med}% -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())