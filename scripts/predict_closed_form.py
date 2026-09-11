#!/usr/bin/env python3
"""Emit a Ledger A closed form. No measured input.

  python scripts/predict_closed_form.py --observable T_CMB
  python scripts/predict_closed_form.py --observable T_CMB --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_ledger_a_lib import LEDGER_A, fsot_predict  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="Ledger A predict (no measured value)")
    p.add_argument("--observable", required=True, help="Ledger A id, e.g. T_CMB")
    p.add_argument("--json", action="store_true")
    p.add_argument("--list", action="store_true")
    args = p.parse_args()
    if args.list:
        print("\n".join(sorted(LEDGER_A)))
        return 0
    rec = fsot_predict(args.observable)
    if args.json:
        print(json.dumps(rec, indent=2))
    else:
        print(f"{rec['observable_id']}  {rec['value']} {rec['units']}")
        print(f"  expression  {rec['expression']}")
        print(f"  pin         {rec['pin']}")
        print(f"  kind        {rec['kind']}  (FORECAST may appear in a ToE paragraph; CONSTANT_IDENTITY is inventory)")
        print("  measured    not used")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
