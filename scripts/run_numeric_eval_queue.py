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
sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import observable_verification_pipeline_path, unified_db_path  # noqa: E402

BACKFILL = ROOT / "scripts" / "backfill_numeric_from_outcomes.py"
GAP_RESOLVER = ROOT / "scripts" / "resolve_strict_empirical_gap.py"
OUT_REPORT = ROOT / "data" / "numeric_eval_queue_report.json"


def _resolve_db(cli_db: Path | None) -> Path:
    path = cli_db or unified_db_path(require=False)
    if path is None:
        raise FileNotFoundError(
            "FSOT_UNIFIED.db not found in vendor/fsot_aggregate. Set FSOT_UNIFIED_DB."
        )
    return path


BIOLOGY_FILTER = (
    "domain_type LIKE '%bio%' OR concept_name LIKE '%bio%'"
    " OR concept_name LIKE '%cell%' OR concept_name LIKE '%gene%'"
    " OR concept_name LIKE '%DNA%' OR concept_name LIKE '%evolution%'"
    " OR concept_name LIKE '%mitochond%' OR concept_name LIKE '%operon%'"
)
BIOLOGY_JOIN_FILTER = BIOLOGY_FILTER.replace("domain_type", "r.domain_type").replace(
    "concept_name", "r.concept_name"
)


def summarize_db(db_path: Path, *, biology_only: bool = False) -> dict:
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    where = f"WHERE ({BIOLOGY_FILTER})" if biology_only else ""
    join_where = f"AND ({BIOLOGY_JOIN_FILTER})" if biology_only else ""
    total_records = cur.execute(f"SELECT COUNT(*) FROM records {where}").fetchone()[0]
    numeric_total = cur.execute(
        f"""
        SELECT COUNT(*) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        {'WHERE ' + BIOLOGY_JOIN_FILTER if biology_only else ''}
        """
    ).fetchone()[0]
    numeric_ok = cur.execute(
        f"""
        SELECT COUNT(*) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE v.evaluation_ok = 1 {join_where}
        """
    ).fetchone()[0]
    numeric_fail = cur.execute(
        f"""
        SELECT COUNT(*) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE v.evaluation_ok = 0 {join_where}
        """
    ).fetchone()[0]
    within_target = cur.execute(
        f"""
        SELECT COUNT(*) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE v.error_pct IS NOT NULL AND v.error_pct <= 2.0 {join_where}
        """
    ).fetchone()[0]
    within_tolerable = cur.execute(
        f"""
        SELECT COUNT(*) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE v.error_pct IS NOT NULL AND v.error_pct <= 5.0 {join_where}
        """
    ).fetchone()[0]
    pending = cur.execute(
        f"""
        SELECT COUNT(*) FROM records r
        LEFT JOIN verification_numeric v ON v.record_id = r.record_id
        WHERE v.record_id IS NULL AND r.strict_empirical = 1
        {join_where}
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
    parser.add_argument("--db", type=Path, default=None, help="Unified DB (default: vendor/fsot_aggregate via fsot_paths)")
    parser.add_argument("--max-candidates", type=int, default=0, help="0 = all candidates")
    parser.add_argument(
        "--biology-subset",
        action="store_true",
        help="Summarize and report biology-related records only",
    )
    parser.add_argument("--dry-run", action="store_true", help="Summarize only, do not run pipeline")
    parser.add_argument("--skip-pipeline", action="store_true", help="Only backfill from outcome_json")
    parser.add_argument("--skip-backfill", action="store_true", help="Only run observable pipeline")
    args = parser.parse_args()

    try:
        db_path = _resolve_db(args.db)
    except FileNotFoundError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    before = summarize_db(db_path, biology_only=args.biology_subset)
    label = "biology subset" if args.biology_subset else "all"
    print(f"=== Numeric eval queue ({label}, before) ===")
    for k, v in before.items():
        print(f"  {k}: {v}")

    if args.dry_run:
        return 0

    if not args.skip_pipeline:
        pipeline = observable_verification_pipeline_path(require=False)
        if pipeline is None or not pipeline.exists():
            print(
                "SKIP: observable pipeline not bundled (use --skip-pipeline or set FSOT_OBSERVABLE_PIPELINE_PATH).",
                file=sys.stderr,
            )
            args.skip_pipeline = True
        else:
            cmd = [
                sys.executable,
                str(pipeline),
                "--mode",
                "numeric-only",
                "--db",
                str(db_path),
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

    if not args.skip_backfill and GAP_RESOLVER.exists():
        print("\n=== Resolving strict-empirical CNC gap ===")
        proc_gap = subprocess.run(
            [sys.executable, str(GAP_RESOLVER), "--db", str(db_path)],
            check=False,
        )
        if proc_gap.returncode != 0:
            print(f"FAIL: gap resolver exit {proc_gap.returncode}", file=sys.stderr)
            return proc_gap.returncode

    if not args.skip_backfill and BACKFILL.exists():
        print("\n=== Backfilling verification_numeric from outcome_json ===")
        proc_bf = subprocess.run(
            [sys.executable, str(BACKFILL), "--db", str(db_path)],
            check=False,
        )
        if proc_bf.returncode != 0:
            print(f"FAIL: backfill exit {proc_bf.returncode}", file=sys.stderr)
            return proc_bf.returncode

    after = summarize_db(db_path, biology_only=args.biology_subset)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evaluator_version": "fsot_numeric_eval_v4",
        "db_path": str(db_path),
        "biology_subset": args.biology_subset,
        "before": before,
        "after": after,
        "delta_numeric_rows": after["verification_numeric_total"] - before["verification_numeric_total"],
        "backfill_ran": not args.skip_backfill,
        "pipeline_ran": not args.skip_pipeline,
    }
    OUT_REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_REPORT}")
    print(f"=== Numeric eval queue ({label}, after) ===")
    for k, v in after.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())