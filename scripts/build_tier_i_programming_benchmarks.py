#!/usr/bin/env python3
"""Build Tier I (44) programming benchmarks: external OSS code genome + language laws."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_i_programming_lib import BUILDERS, TIER_I, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_I, help="Build single domain")
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_I
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"Wrote {path} — records={doc.get('record_count')} "
            f"pooled={doc.get('pooled_median_error_pct')}"
        )
    print("Tier I programming benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())