#!/usr/bin/env python3
"""
Re-run FSOT unified DB candidates through fsot_numeric_eval_v4 (numeric-only).

Wraps fsot_observable_verification_pipeline.py --mode numeric-only, then exports
updated verification stats into data/numeric_eval_queue_report.json for the Lean runner.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = Path(r"C:\Users\damia\Desktop\fsot code language\audits\fsot_observable_verification_pipeline.py")
DEFAULT_DB = Path(r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\FSOT_UNIFIED.db")
OUT_REPORT = ROOT / "data" / "numeric_eval_queue_report.json"


def summarize_db(db_path: Path) -> dict:
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    total_records = cur.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    numeric_total = cur.execute("SELECT COUNT(*) FROM verification_numeric").fetchone()[0]
    numeric_ok = cur.execute(
        "SELECT COUNT(*) FROM verification_numeric WHERE evaluation_ok = 1"
    ).fetchone()[0]
    numeric_fail = cur.execute(
        "SELECT COUNT(*) FROM verification_numeric WHERE evaluation_ok = 0"
    ).fetchone()[0]
    within_target = cur.execute(
        "SELECT COUNT(*) FROM verification_numeric WHERE error_pct IS NOT NULL AND error_pct <= 2.0"
    ).fetchone()[0]
    within_tolerable = cur.execute(
        "SELECT COUNT(*) FROM verification_numeric WHERE error_pct IS NOT NULL AND error_pct <= 5.0"
    ).fetchone()[0]
    pending = cur.execute(
        """
        SELECT COUNT(*) FROM records r
        LEFT JOIN verification_numeric v ON v.record_id = r.record_id
        WHERE v.record_id IS NULL AND r.strict_empirical = 1
        """
    ).fetchone()[0]
    con.close()
    return {
        "records_total": total_records,
        "verification_numeric_total": numeric_total,
        "evaluation_ok": numeric_ok,
        "evaluation_failed": numeric_fail,
        "within_target_2pct": within_target,
        "within_tolerable_5pct": within_tolerable,
        "strict_empirical_pending_numeric": pending,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run FSOT numeric-only eval queue")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--max-candidates", type=int, default=0, help="0 = all candidates")
    parser.add_argument("--dry-run", action="store_true", help="Summarize only, do not run pipeline")
    args = parser.parse_args()

    before = summarize_db(args.db)
    print("=== Numeric eval queue (before) ===")
    for k, v in before.items():
        print(f"  {k}: {v}")

    if args.dry_run:
        return 0

    if not PIPELINE.exists():
        print(f"FAIL: pipeline not found: {PIPELINE}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable,
        str(PIPELINE),
        "--mode",
        "numeric-only",
        "--db",
        str(args.db),
        "--checkpoint-every",
        "100",
    ]
    if args.max_candidates > 0:
        cmd.extend(["--max-candidates", str(args.max_candidates)])

    print("\n=== Running numeric-only pipeline ===")
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0:
        print(f"FAIL: pipeline exit {proc.returncode}", file=sys.stderr)
        return proc.returncode

    after = summarize_db(args.db)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evaluator_version": "fsot_numeric_eval_v4",
        "db_path": str(args.db),
        "before": before,
        "after": after,
        "delta_numeric_rows": after["verification_numeric_total"] - before["verification_numeric_total"],
    }
    OUT_REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_REPORT}")
    print("=== Numeric eval queue (after) ===")
    for k, v in after.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())