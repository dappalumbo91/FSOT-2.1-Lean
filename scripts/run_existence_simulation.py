#!/usr/bin/env python3
"""Run existence simulation — synthetic gap fill + independent prediction ledger."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from existence_simulation_lib import build_gap_fill_records, persist_simulation  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT existence simulation gap fill")
    parser.add_argument("--max-corpus", type=int, default=80, help="Max strict_empirical gaps")
    parser.add_argument("--max-stumped", type=int, default=12, help="Max stumped open-science gaps")
    args = parser.parse_args()

    sim = build_gap_fill_records(max_corpus=args.max_corpus, max_stumped=args.max_stumped)
    cache, ledger = persist_simulation(sim)
    print(f"Gap-fill records: {sim['gap_fill_count']}")
    print(f"  strict_empirical: {sim['strict_empirical_gaps']}")
    print(f"  stumped: {sim['stumped_gaps']}")
    print(f"  orbital: {sim['orbital_frontiers']}")
    print(f"Simulation pooled median error: {sim['simulation_pooled_median_error_pct']}%")
    if sim.get("verification_pooled_median_error_pct") is not None:
        print(f"Verification anchor median (locked, not used in sim): {sim['verification_pooled_median_error_pct']}%")
    print(f"Wrote {cache}")
    print(f"Wrote {ledger}")
    return 0 if sim["gap_fill_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())