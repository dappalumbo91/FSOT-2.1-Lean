#!/usr/bin/env python3
"""Ingest Tier 38 public API datasets to Game drive + vendor summaries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier38_public_data_lib import INGESTORS, external_data_root  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Expanded cohort limits (GBIF 300, PubChem 40, etc.)",
    )
    parser.add_argument(
        "--only",
        choices=sorted(INGESTORS.keys()),
        action="append",
        help="Ingest a single source (repeatable)",
    )
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER38_DEEP"] = "1"
    keys = args.only or sorted(INGESTORS.keys())
    print(f"External data root: {external_data_root()}")
    failed: list[str] = []
    for key in keys:
        print(f"\n=== ingest {key} ===")
        try:
            doc = INGESTORS[key]()
            count_key = next((k for k in doc if k.endswith("_count")), "ok")
            print(f"  OK {key}: {count_key}={doc.get(count_key)}")
        except Exception as exc:
            failed.append(key)
            print(f"  FAIL {key}: {exc}")
    if failed:
        print(f"\nFailed: {failed}", file=sys.stderr)
        return 1
    print("\nAll Tier 38 ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())