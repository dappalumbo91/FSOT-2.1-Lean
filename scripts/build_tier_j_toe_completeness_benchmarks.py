#!/usr/bin/env python3
"""Build Tier J (45) ToE completeness benchmarks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_j_toe_completeness_lib import BUILDERS, TIER_J, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_J)
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_J
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"Wrote {path} — records={doc.get('record_count')} pooled={doc.get('pooled_median_error_pct')}")
    print("Tier J ToE completeness benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())