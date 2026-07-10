#!/usr/bin/env python3
"""Build Tier N (49) compactification/folding ladder benchmarks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_n_compactification_ladder_lib import BUILDERS, TIER_N, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_N)
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_N
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"Wrote {path} — records={doc.get('record_count')} "
            f"pooled={doc.get('pooled_median_error_pct')} status={doc.get('ladder_status') or doc.get('coupling_status') or doc.get('metrics_status') or doc.get('folding_status')}"
        )
    print("Tier N compactification ladder benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())