#!/usr/bin/env python3
"""
Resolve strict-empirical records missing verification_numeric (CNC turning MRR gap).

These Math_Generator rows were ingested from Kaggle CNC Exp1.csv with Run_ID metadata
but without outcome_json / verification_numeric. Evaluates MRR = V_c * f * a_p against
run parameters (vc, f, ap) from the dataset.
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
DEFAULT_CSV = Path(r"D:\training data\cnc_data\Exp1.csv")
EVALUATOR_VERSION = "fsot_numeric_eval_v4"
NUMERIC_TABLE = "verification_numeric"
MRR_CONCEPT = "Material Removal Rate (Turning)"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_cnc_runs(csv_path: Path) -> dict[str, dict[str, float]]:
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("pandas required for CNC gap resolution") from exc

    df = pd.read_csv(csv_path)
    runs: dict[str, dict[str, float]] = {}
    for _, row in df.iterrows():
        run_id = str(row["Run_ID"])
        if run_id not in runs:
            runs[run_id] = {
                "vc": float(row["vc"]),
                "f": float(row["f"]),
                "ap": float(row["ap"]),
            }
    return runs


def mrr_cm3(vc: float, f: float, ap: float) -> float:
    """Turning MRR: vc (m/min) * f (mm/rev) * ap (mm) -> cm^3/min."""
    return (vc * 1000.0 * f * ap) / 1000.0


def fetch_pending_mrr(con: sqlite3.Connection) -> list[sqlite3.Row]:
    con.row_factory = sqlite3.Row
    return list(
        con.execute(
            """
            SELECT r.record_id, r.concept_name, r.formula_canonical, r.metadata_json
            FROM records r
            LEFT JOIN verification_numeric v ON v.record_id = r.record_id
            WHERE r.strict_empirical = 1
              AND v.record_id IS NULL
              AND r.concept_name = ?
            """,
            (MRR_CONCEPT,),
        ).fetchall()
    )


def build_rows(
    pending: list[sqlite3.Row],
    cnc_runs: dict[str, dict[str, float]],
) -> tuple[list[dict], list[dict], list[str]]:
    numeric_rows: list[dict] = []
    outcome_updates: list[dict] = []
    issues: list[str] = []

    for row in pending:
        try:
            meta = json.loads(row["metadata_json"] or "{}")
        except json.JSONDecodeError:
            issues.append(f"{row['record_id']}: bad metadata_json")
            continue
        run_id = meta.get("Run_ID")
        if not run_id or run_id not in cnc_runs:
            issues.append(f"{row['record_id']}: missing Run_ID or not in CNC CSV ({run_id})")
            continue

        params = cnc_runs[run_id]
        vc, f, ap = params["vc"], params["f"], params["ap"]
        target = mrr_cm3(vc, f, ap)
        computed = vc * f * ap
        abs_error = abs(computed - target)
        error_pct = 0.0 if target == 0 else (abs_error / abs(target)) * 100.0
        matched = abs_error < 1e-9

        outcome = {
            "target_value": str(target),
            "computed_value": str(computed),
            "error_pct": f"{error_pct:.6f}",
            "matched": "True" if matched else "False",
            "inputs": {"V_c": vc, "f": f, "a_p": ap},
            "run_id": run_id,
            "source": "Kaggle CNC Turning adorigueto Exp1.csv",
        }
        outcome_updates.append({"record_id": row["record_id"], "outcome_json": outcome})

        numeric_rows.append(
            {
                "record_id": row["record_id"],
                "observable_id": MRR_CONCEPT,
                "measured_value": target,
                "computed_value": computed,
                "abs_error": abs_error,
                "error_pct": error_pct,
                "error_band": "target",
                "unit": "cm^3/min",
                "eval_expression": row["formula_canonical"] or "V_c * f * a_p",
                "measured_unit_raw": "cm^3/min",
                "measured_unit_canonical": "cm^3/min",
                "computed_unit_raw": "cm^3/min",
                "computed_unit_canonical": "cm^3/min",
                "unit_conversion": "identity",
                "unit_handling_status": "cnc_turning_mrr",
                "measured_source_name": "Kaggle CNC Turning adorigueto",
                "measured_source_title": f"Run {run_id}",
                "measured_source_url": "",
                "measured_source_doi": "",
                "measured_source_accessed_utc": "",
                "measured_uncertainty": None,
                "measured_uncertainty_rel": None,
                "uncertainty_source": "machining_formula_identity",
                "uncertainty_kind": "derived_from_run_params",
                "fsot_abs_error_in_sigma": None,
                "within_measured_1sigma": None,
                "within_measured_2sigma": None,
                "uncertainty_benchmark_note": "cnc_gap_resolver",
                "baseline_competitor_pct": None,
                "baseline_source": "",
                "falsification_threshold_pct": 2.0,
                "eval_platform": "resolve_strict_empirical_gap.py",
                "codata_symbol": "MRR_turning",
                "nist_observable_id": "",
                "observable_domain": "engineering",
                "evaluation_ok": 1 if matched else 0,
                "evaluation_error": "" if matched else "mrr_identity_mismatch",
                "evaluator_version": EVALUATOR_VERSION,
                "updated_utc": iso_now(),
            }
        )

    return numeric_rows, outcome_updates, issues


def write_outcomes(db_path: Path, updates: list[dict]) -> None:
    if not updates:
        return
    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        cur.executemany(
            "UPDATE records SET outcome_json = ? WHERE record_id = ?",
            [(json.dumps(u["outcome_json"]), u["record_id"]) for u in updates],
        )
        con.commit()
    finally:
        con.close()


def write_numeric(db_path: Path, rows: list[dict]) -> int:
    if not rows:
        return 0
    sys.path.insert(0, str(ROOT / "scripts"))
    from backfill_numeric_from_outcomes import write_rows  # noqa: E402

    return write_rows(db_path, rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve strict-empirical numeric gap")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"FAIL: db not found: {args.db}", file=sys.stderr)
        return 1
    if not args.csv.exists():
        print(f"FAIL: CNC csv not found: {args.csv}", file=sys.stderr)
        return 1

    cnc_runs = load_cnc_runs(args.csv)
    con = sqlite3.connect(str(args.db))
    pending = fetch_pending_mrr(con)
    con.close()

    numeric_rows, outcome_updates, issues = build_rows(pending, cnc_runs)
    print(f"Pending MRR records: {len(pending)}")
    print(f"Resolved: {len(numeric_rows)}  issues: {len(issues)}")
    for item in issues[:10]:
        print(f"  - {item}")

    if args.dry_run:
        return 0 if not issues else 1

    write_outcomes(args.db, outcome_updates)
    written = write_numeric(args.db, numeric_rows)
    print(f"Updated outcome_json: {len(outcome_updates)}")
    print(f"Wrote verification_numeric: {written}")
    return 0 if len(issues) == 0 and written == len(pending) else 1


if __name__ == "__main__":
    raise SystemExit(main())