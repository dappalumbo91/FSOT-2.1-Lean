#!/usr/bin/env python3
"""Build Tier 66 NeuroLab residual panels + spine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier66_neurolab_residual_lib import BUILDERS, BUILD_ORDER, output_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or BUILD_ORDER
    if "Neurolab_Residual_Math_Spine" in domains:
        prereqs = [d for d in BUILD_ORDER if d != "Neurolab_Residual_Math_Spine"]
        domains = list(dict.fromkeys([*domains, *prereqs]))
        domains = [d for d in BUILD_ORDER if d in domains]
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{domain}: {doc.get('record_count')} records, pooled {doc.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())