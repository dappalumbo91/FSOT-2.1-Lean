#!/usr/bin/env python3
"""Tier 81 — credential-free public API ingest (no API keys)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier81_public_verifiable_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        import os

        os.environ["FSOT_TIER81_DEEP"] = "1"
    keys = args.only or sorted(INGESTORS.keys())
    failed: list[str] = []
    for key in keys:
        print(f"\n=== ingest {key} ===")
        try:
            doc = INGESTORS[key]()
            count_key = next((k for k in doc if k.endswith("_count")), "row_count")
            print(f"  OK {key}: {count_key}={doc.get(count_key)} source={doc.get('source')}")
        except Exception as exc:
            failed.append(key)
            print(f"  FAIL {key}: {exc}")
    if failed:
        print(f"\nFailed: {failed}", file=sys.stderr)
        return 1
    print("\nAll Tier 81 credential-free ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())