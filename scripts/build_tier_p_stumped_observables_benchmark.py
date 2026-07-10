#!/usr/bin/env python3
"""Build Tier 51 (P) stumped observables / open-problem benchmarks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tier_p_stumped_observables_lib import BUILDERS, TIER_P, output_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=TIER_P)
    args = ap.parse_args()
    targets = [args.only] if args.only else TIER_P
    for name in targets:
        doc = BUILDERS[name]()
        path = output_path(name)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        status = (
            doc.get("stumped_spine_status")
            or doc.get("panel_status")
            or doc.get("tension_status")
            or doc.get("dark_sector_status")
            or "GREEN"
        )
        print(
            f"Wrote {path} — records={doc.get('record_count')} "
            f"pooled={doc.get('pooled_median_error_pct')} status={status}"
        )
    print("Tier 51 stumped observables benchmarks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())