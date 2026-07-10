#!/usr/bin/env python3
"""Ingest Tier 51 anomaly public data to G:/FSOT-PublicData/anomaly_observables."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from anomaly_public_data_lib import INGESTORS, cache_root  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    keys = args.only or sorted(INGESTORS.keys())
    print(f"Anomaly cache root: {cache_root()}")
    failed: list[str] = []
    for key in keys:
        print(f"\n=== {key} ===")
        try:
            doc = INGESTORS[key]()
            print(f"  OK: {doc}")
        except Exception as exc:
            failed.append(key)
            print(f"  FAIL: {exc}")
    if failed:
        print(f"\nFailed ingests: {failed}", file=sys.stderr)
        return 1
    print("\nAnomaly public data ingest complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())