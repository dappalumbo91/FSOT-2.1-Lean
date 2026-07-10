#!/usr/bin/env python3
"""Build Tier M (48) ToE unity benchmarks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_m_toe_unity_lib import BUILDERS, TIER_M, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_M)
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_M
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"Wrote {path} — records={doc.get('record_count')} pooled={doc.get('pooled_median_error_pct')}")
    print("Tier M ToE unity benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())