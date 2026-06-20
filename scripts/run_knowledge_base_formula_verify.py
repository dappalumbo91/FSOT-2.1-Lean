#!/usr/bin/env python3
"""Run per-formula KB validation (same methodology as strict_empirical) and ingest summary."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB_WORKSPACE = Path(r"C:\Users\damia\Desktop\Knowledge base")
KB_VALIDATOR = KB_WORKSPACE / "scripts" / "run_fsot_full_corpus_validation.py"
KB_VALIDATION_JSON = KB_WORKSPACE / "export" / "full_corpus_math_validation.json"
OUT_JSONL = ROOT / "data" / "knowledge_base_formula_verification.jsonl"
OUT_SUMMARY = ROOT / "data" / "knowledge_base_formula_verification_summary.json"

sys.path.insert(0, str(ROOT / "scripts"))
from formula_corpus import load_strict_empirical_jsonl, summarize_formula_corpus  # noqa: E402


def summarize_kb_validation(data: dict) -> dict:
    summary = data.get("summary") or {}
    rows = data.get("rows") or []
    verified = sum(1 for r in rows if r.get("status") == "verified")
    tolerable = sum(1 for r in rows if r.get("status") == "tolerable")
    unacceptable = sum(1 for r in rows if r.get("status") == "unacceptable")
    with_target = sum(1 for r in rows if r.get("target_value") is not None)
    within_2 = sum(
        1
        for r in rows
        if r.get("error_pct") is not None and float(r["error_pct"]) <= 2.0
    )
    within_5 = sum(
        1
        for r in rows
        if r.get("error_pct") is not None and float(r["error_pct"]) <= 5.0
    )
    return {
        "catalog_formulas_total": summary.get("total_formulas", len(rows)),
        "with_target": summary.get("with_target", with_target),
        "evaluated": summary.get("evaluated", 0),
        "verified_status_count": verified,
        "tolerable_status_count": tolerable,
        "unacceptable_status_count": unacceptable,
        "within_target_2pct": within_2,
        "within_tolerable_5pct": within_5,
        "unparseable": summary.get("unparseable", 0),
        "skipped_non_math": summary.get("skipped_non_math", 0),
        "computed_no_target": summary.get("computed_no_target", 0),
        "symbolic_math_no_target": summary.get("symbolic_math_no_target", 0),
    }


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="KB per-formula verification pass")
    parser.add_argument("--skip-validator", action="store_true", help="Use existing full_corpus_math_validation.json")
    args = parser.parse_args()

    if not args.skip_validator:
        if not KB_VALIDATOR.exists():
            print(f"FAIL: validator not found: {KB_VALIDATOR}", file=sys.stderr)
            return 1
        print("=== Running KB full corpus validation ===")
        proc = subprocess.run([sys.executable, str(KB_VALIDATOR)], check=False)
        if proc.returncode != 0:
            print(f"FAIL: validator exit {proc.returncode}", file=sys.stderr)
            return proc.returncode

    if not KB_VALIDATION_JSON.exists():
        print(f"FAIL: missing {KB_VALIDATION_JSON}", file=sys.stderr)
        return 1

    data = json.loads(KB_VALIDATION_JSON.read_text(encoding="utf-8"))
    kb_summary = summarize_kb_validation(data)
    rows = data.get("rows") or []
    write_jsonl(rows, OUT_JSONL)

    strict_path = Path(
        r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\by_domain\strict_empirical.jsonl"
    )
    strict_summary = (
        summarize_formula_corpus(load_strict_empirical_jsonl(strict_path))
        if strict_path.exists()
        else {}
    )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verification_tier": "numeric_formula",
        "kb_corpus_validation_path": str(KB_VALIDATION_JSON),
        "strict_empirical_corpus_path": str(strict_path),
        "per_formula_jsonl": str(OUT_JSONL),
        "kb_catalog": kb_summary,
        "strict_empirical_bridge": strict_summary,
        "observable_verified_formulas": strict_summary.get("records_total", 0),
        "observable_verified_matched": strict_summary.get("matched_count", 0),
        "within_target_2pct": strict_summary.get("within_target_2pct", 0),
        "within_tolerable_5pct": strict_summary.get("within_tolerable_5pct", 0),
    }
    OUT_SUMMARY.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSONL} ({len(rows)} rows)")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"  KB catalog formulas: {kb_summary.get('catalog_formulas_total')}")
    print(f"  KB verified (status): {kb_summary.get('verified_status_count')}")
    print(f"  strict_empirical bridge: {strict_summary.get('records_total')} matched {strict_summary.get('matched_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())