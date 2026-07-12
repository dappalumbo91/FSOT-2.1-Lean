#!/usr/bin/env python3
"""Build Tier 92 alternate base mathematics explorer benchmarks."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier92_alternate_base_mathematics_lib import BUILDERS, BUILD_ORDER, output_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-ingest", action="store_true")
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    if not args.skip_ingest:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "ingest_tier92_alternate_base_mathematics.py"), "--deep"],
            check=False,
        )
    domains = args.only or BUILD_ORDER
    if "Alternate_Base_Mathematics_Spine" in domains:
        prereqs = [d for d in BUILD_ORDER if d != "Alternate_Base_Mathematics_Spine"]
        domains = [d for d in BUILD_ORDER if d in set(domains) | set(prereqs)]
    for domain in domains:
        doc = BUILDERS[domain]()
        out = output_path(domain)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{domain}: {doc.get('record_count')} records, pooled {doc.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())