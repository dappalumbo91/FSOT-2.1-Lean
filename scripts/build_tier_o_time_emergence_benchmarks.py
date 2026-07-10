#!/usr/bin/env python3
"""Build Tier 50 (O) time emergence / FPC benchmarks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_o_time_emergence_lib import BUILDERS, TIER_O, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_O)
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_O
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        status = (
            doc.get("fpc_spine_status")
            or doc.get("time_status")
            or doc.get("crosswalk_status")
            or doc.get("coupling_status")
            or "GREEN"
        )
        print(
            f"Wrote {path} — records={doc.get('record_count')} "
            f"pooled={doc.get('pooled_median_error_pct')} status={status}"
        )
    print("Tier 50 time emergence / FPC benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())