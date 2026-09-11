#!/usr/bin/env python3
"""Compare a Ledger A emit to a frozen literature anchor. Separate from predict.

  python scripts/compare_to_anchor.py --observable T_CMB --source nist
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_ledger_a_lib import compare_anchor  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="Ledger A compare (anchor not in formula)")
    p.add_argument("--observable", required=True)
    p.add_argument("--source", default="literature", help="label only; anchor is frozen in ledger_a_lib")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rec = compare_anchor(args.observable)
    rec["requested_source"] = args.source
    if args.json:
        print(json.dumps(rec, indent=2))
    else:
        print(f"{rec['observable_id']}  hat={rec['value']}  anchor={rec['anchor']} {rec['units']}")
        print(f"  error_pct   {rec['error_pct']:.6f}%")
        print(f"  kind        {rec['kind']}")
        print(f"  source      {rec['anchor_source']}")
        print(f"  kill_band   {rec['kill_band']}")
        print("  formula did not see the anchor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
