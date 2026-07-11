#!/usr/bin/env python3
"""Build PDG, CRC handbook, and NIST DLMF first-class reference anchor benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reference_anchors_lib import BUILDERS, REFERENCE_ANCHOR_DOMAINS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=REFERENCE_ANCHOR_DOMAINS, action="append")
    args = parser.parse_args()
    domains = args.only or REFERENCE_ANCHOR_DOMAINS
    failed: list[str] = []
    for domain in domains:
        out_name, builder = BUILDERS[domain]
        out_path = ROOT / "data" / out_name
        try:
            doc = builder()
            out_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
            print(f"Wrote {out_path}")
            print(
                f"  {domain}: records={doc['record_count']} "
                f"median={doc.get('median_error_pct')}% max={doc.get('max_error_pct')}%"
            )
        except Exception as exc:
            failed.append(domain)
            print(f"FAIL {domain}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())