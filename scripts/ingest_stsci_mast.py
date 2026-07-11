#!/usr/bin/env python3
"""Tier 79 — STScI MAST CAOM ingest with bundled fallback."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stsci_mast_lib import ingest_mast  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Use bundled mast_telescope_sample.json only")
    parser.add_argument("--deep", action="store_true", help="Larger CAOM sample pages per target")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER79_DEEP"] = "1"
    doc = ingest_mast(offline=args.offline)
    print(f"MAST ingest: source={doc.get('source')} targets={doc.get('target_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())