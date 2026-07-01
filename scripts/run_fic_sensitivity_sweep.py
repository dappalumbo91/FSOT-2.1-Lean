#!/usr/bin/env python3
"""Generate full FIC sensitivity sweep CSV (replaces truncated FSOT-2.0 stub)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "fic_sensitivity_sweep.csv"
DEFAULT_REPORT = ROOT / "data" / "fic_sensitivity_report.json"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from fic_lab import run_sensitivity_sweep, summarize_sweep, write_sweep_csv  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run FIC sensitivity sweep")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = run_sensitivity_sweep()
    write_sweep_csv(rows, args.csv)
    summary = summarize_sweep(rows)
    summary["csv_path"] = str(args.csv)
    args.report.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {args.csv} ({len(rows)} rows)")
    print(f"Wrote {args.report}")
    print(f"  fertile: {summary['fertile_count']}/{summary['sweep_row_count']}")
    print(f"  optimal_S: {summary.get('optimal_S_final')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())