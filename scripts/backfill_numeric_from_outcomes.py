#!/usr/bin/env python3
"""
Backfill verification_numeric from records.outcome_json (strict-empirical fsot_numeric_eval outcomes).

The observable pipeline only writes rows when select_observable() matches; strict-empirical
records already carry target/computed/error in outcome_json from prior fsot_numeric_eval runs.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = Path(
    r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\FSOT_UNIFIED.db"
)
EVALUATOR_VERSION = "fsot_numeric_eval_v4"
NUMERIC_TABLE = "verification_numeric"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def error_band(error_pct: float) -> str:
    if error_pct <= 2.0:
        return "target"
    if error_pct < 5.0:
        return "tolerable_refine"
    return "unacceptable"


def fetch_backfill_candidates(con: sqlite3.Connection, only_missing: bool) -> list[sqlite3.Row]:
    con.row_factory = sqlite3.Row
    if only_missing:
        query = """
            SELECT r.record_id, r.concept_name, r.target_quantity, r.formula_canonical,
                   r.strict_empirical, r.outcome_json
            FROM records r
            LEFT JOIN verification_numeric v ON v.record_id = r.record_id
            WHERE v.record_id IS NULL
              AND r.outcome_json IS NOT NULL AND r.outcome_json != ''
              AND json_extract(r.outcome_json, '$.error_pct') IS NOT NULL
        """
    else:
        query = """
            SELECT record_id, concept_name, target_quantity, formula_canonical,
                   strict_empirical, outcome_json
            FROM records
            WHERE outcome_json IS NOT NULL AND outcome_json != ''
              AND json_extract(outcome_json, '$.error_pct') IS NOT NULL
        """
    return list(con.execute(query).fetchall())


def outcome_to_numeric_row(row: sqlite3.Row) -> dict | None:
    try:
        outcome = json.loads(row["outcome_json"] or "{}")
    except json.JSONDecodeError:
        return None
    if outcome.get("error_pct") in (None, ""):
        return None
    try:
        target = float(outcome["target_value"])
        computed = float(outcome["computed_value"])
        error_pct = float(outcome["error_pct"])
    except (KeyError, TypeError, ValueError):
        return None

    abs_error = abs(computed - target)
    concept = (row["concept_name"] or "").strip()
    observable_id = concept if concept else f"strict_empirical_target_{row['record_id'][:8]}"
    matched = str(outcome.get("matched", "")).lower() == "true"
    band = error_band(error_pct)

    return {
        "record_id": row["record_id"],
        "observable_id": observable_id,
        "measured_value": target,
        "computed_value": computed,
        "abs_error": abs_error,
        "error_pct": error_pct,
        "error_band": band,
        "unit": "mixed",
        "eval_expression": (row["formula_canonical"] or "")[:160],
        "measured_unit_raw": "mixed",
        "measured_unit_canonical": "mixed",
        "computed_unit_raw": "mixed",
        "computed_unit_canonical": "mixed",
        "unit_conversion": "identity",
        "unit_handling_status": "outcome_json_backfill",
        "measured_source_name": "strict_empirical_corpus",
        "measured_source_title": row["target_quantity"] or concept,
        "measured_source_url": "",
        "measured_source_doi": "",
        "measured_source_accessed_utc": "",
        "measured_uncertainty": None,
        "measured_uncertainty_rel": None,
        "uncertainty_source": "",
        "uncertainty_kind": "empirical_target",
        "fsot_abs_error_in_sigma": None,
        "within_measured_1sigma": None,
        "within_measured_2sigma": None,
        "uncertainty_benchmark_note": "outcome_json_backfill",
        "baseline_competitor_pct": None,
        "baseline_source": "",
        "falsification_threshold_pct": 2.0,
        "eval_platform": "backfill_numeric_from_outcomes.py",
        "codata_symbol": concept,
        "nist_observable_id": "",
        "observable_domain": "strict_empirical",
        "evaluation_ok": 1 if matched and band in ("target", "tolerable_refine") else 0,
        "evaluation_error": "" if matched else "unmatched_outcome",
        "evaluator_version": EVALUATOR_VERSION,
        "updated_utc": iso_now(),
    }


def write_rows(db_path: Path, rows: list[dict]) -> int:
    if not rows:
        return 0
    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        cur.executemany(
            f"""
            INSERT INTO {NUMERIC_TABLE} (
                record_id, observable_id, measured_value, computed_value,
                abs_error, error_pct, error_band, unit, eval_expression,
                measured_unit_raw, measured_unit_canonical,
                computed_unit_raw, computed_unit_canonical,
                unit_conversion, unit_handling_status,
                measured_source_name, measured_source_title,
                measured_source_url, measured_source_doi,
                measured_source_accessed_utc,
                measured_uncertainty, measured_uncertainty_rel, uncertainty_source,
                uncertainty_kind,
                fsot_abs_error_in_sigma, within_measured_1sigma, within_measured_2sigma,
                uncertainty_benchmark_note,
                baseline_competitor_pct, baseline_source, falsification_threshold_pct,
                eval_platform, codata_symbol, nist_observable_id, observable_domain,
                evaluation_ok, evaluation_error, evaluator_version, updated_utc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(record_id) DO UPDATE SET
                observable_id=excluded.observable_id,
                measured_value=excluded.measured_value,
                computed_value=excluded.computed_value,
                abs_error=excluded.abs_error,
                error_pct=excluded.error_pct,
                error_band=excluded.error_band,
                unit=excluded.unit,
                eval_expression=excluded.eval_expression,
                unit_handling_status=excluded.unit_handling_status,
                evaluation_ok=excluded.evaluation_ok,
                evaluation_error=excluded.evaluation_error,
                evaluator_version=excluded.evaluator_version,
                updated_utc=excluded.updated_utc
            """,
            [
                (
                    r["record_id"],
                    r["observable_id"],
                    r["measured_value"],
                    r["computed_value"],
                    r["abs_error"],
                    r["error_pct"],
                    r["error_band"],
                    r["unit"],
                    r["eval_expression"],
                    r["measured_unit_raw"],
                    r["measured_unit_canonical"],
                    r["computed_unit_raw"],
                    r["computed_unit_canonical"],
                    r["unit_conversion"],
                    r["unit_handling_status"],
                    r["measured_source_name"],
                    r["measured_source_title"],
                    r["measured_source_url"],
                    r["measured_source_doi"],
                    r["measured_source_accessed_utc"],
                    r["measured_uncertainty"],
                    r["measured_uncertainty_rel"],
                    r["uncertainty_source"],
                    r["uncertainty_kind"],
                    r["fsot_abs_error_in_sigma"],
                    r["within_measured_1sigma"],
                    r["within_measured_2sigma"],
                    r["uncertainty_benchmark_note"],
                    r["baseline_competitor_pct"],
                    r["baseline_source"],
                    r["falsification_threshold_pct"],
                    r["eval_platform"],
                    r["codata_symbol"],
                    r["nist_observable_id"],
                    r["observable_domain"],
                    r["evaluation_ok"],
                    r["evaluation_error"],
                    r["evaluator_version"],
                    r["updated_utc"],
                )
                for r in rows
            ],
        )
        con.commit()
    finally:
        con.close()
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill verification_numeric from outcome_json")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--all", action="store_true", help="Upsert all outcome_json rows, not only missing")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"FAIL: db not found: {args.db}", file=sys.stderr)
        return 1

    con = sqlite3.connect(str(args.db))
    candidates = fetch_backfill_candidates(con, only_missing=not args.all)
    con.close()

    rows: list[dict] = []
    skipped = 0
    for cand in candidates:
        nrow = outcome_to_numeric_row(cand)
        if nrow:
            rows.append(nrow)
        else:
            skipped += 1

    print(f"Candidates: {len(candidates)}  rows built: {len(rows)}  skipped: {skipped}")
    if args.dry_run:
        return 0

    written = write_rows(args.db, rows)
    print(f"Wrote {written} rows to {NUMERIC_TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())