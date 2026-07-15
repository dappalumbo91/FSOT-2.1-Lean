#!/usr/bin/env python3
"""Build Tier 95 Zebrahub developmental genetics benchmarks."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier95_zebrahub_development_lib import BUILDERS, BUILD_ORDER, output_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-ingest", action="store_true")
    parser.add_argument("--deep", action="store_true", help="Ingest all Zebrahub track CSVs and imaging volumes")
    parser.add_argument("--gpu", action="store_true")
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER95_DEEP"] = "1"
    if not args.skip_ingest:
        cmd = [sys.executable, str(ROOT / "scripts" / "ingest_tier95_zebrahub_development.py")]
        if args.deep or os.environ.get("FSOT_TIER95_DEEP", "").strip().lower() in {"1", "true", "yes"}:
            cmd.append("--deep")
        if args.gpu:
            cmd.append("--gpu")
        subprocess.run(cmd, check=False)
    domains = args.only or BUILD_ORDER
    if "Tier_95_Zebrafish_Spine" in domains:
        prereqs = [d for d in BUILD_ORDER if d != "Tier_95_Zebrafish_Spine"]
        domains = [d for d in BUILD_ORDER if d in set(domains) | set(prereqs)]
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{domain}: {doc.get('record_count')} records, pooled {doc.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())