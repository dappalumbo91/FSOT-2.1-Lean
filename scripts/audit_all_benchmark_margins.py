#!/usr/bin/env python3
"""Audit error margins across all FSOT benchmark JSON files."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import analyze_benchmark, error_pct_disagrees  # noqa: E402
from fsot_precision_constants import (  # noqa: E402
    AUDIT_EXCLUDED_BENCHMARKS,
    MAX_MEDIAN_ERROR_PCT,
    MAX_SCALAR_ERROR_PCT,
    MIN_CLASSIFIER_ACCURACY_PCT,
    TIER_SCALAR_MAX_ERROR_PCT,
)

DATA = ROOT / "data"
OUT = DATA / "benchmark_margin_audit.json"


def _records(doc: dict) -> list[dict]:
    recs = doc.get("material_records") or doc.get("records") or []
    if not isinstance(recs, list):
        return []
    return [r for r in recs if isinstance(r, dict)]


def main() -> int:
    rows: list[dict] = []
    excluded: list[dict] = []
    disagree_by_file: Counter[str] = Counter()
    cross_by_file: Counter[str] = Counter()
    cross_structural = 0
    cross_gated = 0
    disagree_structural = 0
    disagree_gated = 0
    examples: list[dict] = []
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for rec in _records(doc):
            gap = error_pct_disagrees(rec)
            if gap is None:
                continue
            disagree_by_file[path.name] += 1
            if gap["ledger_b_scale_step"]:
                disagree_structural += 1
            else:
                disagree_gated += 1
            crosses = (
                gap["recomputed_error_pct"] > MAX_SCALAR_ERROR_PCT
                and gap["stored_error_pct"] <= MAX_SCALAR_ERROR_PCT
            )
            if crosses:
                cross_by_file[path.name] += 1
                if gap["ledger_b_scale_step"]:
                    cross_structural += 1
                else:
                    cross_gated += 1
            if crosses and len(examples) < 40:
                examples.append({"file": path.name, **gap})
        row = analyze_benchmark(doc, file_name=path.name)
        if row.get("excluded"):
            excluded.append(row)
            continue
        rows.append(row)

    rows.sort(key=lambda x: -(x.get("max_scalar_error_pct") or 0))
    green_fails = [r for r in rows if not r["green_gate_pass"]]
    pooled_fails = [r for r in rows if not r["green_gate_pass_pooled_only"]]
    strict_fails = [r for r in rows if not r["strict_scalar_pass"] and r["scalar_count"] > 0]
    classifier_fails = [r for r in rows if not r["classifier_pass"] and r["classifier_count"] > 0]
    tier_fails = [r for r in rows if not r["tier_scalar_pass"] and r["scalar_count"] > 0]
    gated = [r for r in rows if r.get("scalar_count", 0) > 0]
    gated_green = [r for r in gated if r["green_gate_pass"]]
    genuine_prediction_count = sum(int(r.get("genuine_prediction_count") or 0) for r in rows)
    structural_correction_count = sum(int(r.get("structural_correction_count") or 0) for r in rows)
    stored_green_fails = [r for r in rows if not r.get("green_gate_pass_stored_error", True)]
    fail_files = {r["file"] for r in green_fails}
    listed_fail_files = {name for name in fail_files if cross_by_file[name] or disagree_by_file[name]}
    unlisted_fail_files = sorted(fail_files - listed_fail_files)

    summary = {
        "benchmark_file_count": len(rows),
        "excluded_file_count": len(excluded),
        "excluded_files": list(AUDIT_EXCLUDED_BENCHMARKS),
        "genuine_prediction_count": genuine_prediction_count,
        "structural_correction_count": structural_correction_count,
        "files_with_gated_scalars_count": len(gated),
        "files_with_gated_scalars_green_count": len(gated_green),
        "files_with_gated_scalars": [r["file"] for r in gated],
        "threshold_official_pooled_median_pct": MAX_MEDIAN_ERROR_PCT,
        "threshold_strict_scalar_max_pct": MAX_SCALAR_ERROR_PCT,
        "threshold_tier_scalar_max_pct": TIER_SCALAR_MAX_ERROR_PCT,
        "threshold_min_classifier_accuracy_pct": MIN_CLASSIFIER_ACCURACY_PCT,
        "green_gate_pass_count": len(rows) - len(green_fails),
        "green_gate_fail_count": len(green_fails),
        "green_gate_pass_count_stored_error": len(rows) - len(stored_green_fails),
        "green_gate_fail_count_stored_error": len(stored_green_fails),
        "error_pct_disagreement_count": int(sum(disagree_by_file.values())),
        "error_pct_disagreement_structural_count": disagree_structural,
        "error_pct_disagreement_other_count": disagree_gated,
        "error_pct_disagreement_file_count": len(disagree_by_file),
        "error_pct_disagreement_by_file": dict(disagree_by_file.most_common()),
        "error_pct_crosses_half_pct_count": int(sum(cross_by_file.values())),
        "error_pct_crosses_half_pct_structural_count": cross_structural,
        "error_pct_crosses_half_pct_other_count": cross_gated,
        "error_pct_crosses_half_pct_file_count": len(cross_by_file),
        "error_pct_crosses_half_pct_by_file": dict(cross_by_file.most_common()),
        "error_pct_disagreement_examples": examples,
        "recomputed_gate_failure_files": sorted(fail_files),
        "unlisted_recomputed_gate_failures": unlisted_fail_files,
        "pooled_only_fail_count": len(pooled_fails),
        "strict_scalar_fail_count": len(strict_fails),
        "classifier_fail_count": len(classifier_fails),
        "tier_scalar_fail_count": len(tier_fails),
        "worst_scalar_max_error_pct": rows[0]["max_scalar_error_pct"] if rows else None,
        "worst_scalar_domain": rows[0]["domain"] if rows else None,
        "green_gate_failures": green_fails,
        "classifier_failures": classifier_fails,
        "strict_scalar_failures_top25": strict_fails[:25],
        "excluded": excluded,
        "all_domains": rows,
    }
    try:
        from ledger_b_null_models import main as _null_main  # noqa: E402

        _null_main()
        null_path = DATA / "ledger_b_null_models.json"
        if null_path.is_file():
            summary["ledger_b_nulls"] = json.loads(null_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        summary["ledger_b_nulls"] = {"error": str(exc), "cite_as_toe_accuracy": False}

    OUT.write_text(json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"  active files={len(rows)} excluded={len(excluded)}")
    print(
        f"  genuine predictions={genuine_prediction_count} "
        f"structural corrections (Ledger B)={structural_correction_count}"
    )
    print(
        f"  files with gated scalars={len(gated)} "
        f"of which green={len(gated_green)}"
    )
    print(
        f"  GREEN stored error_pct: "
        f"{summary['green_gate_pass_count_stored_error']} pass / "
        f"{summary['green_gate_fail_count_stored_error']} fail"
    )
    print(
        f"  GREEN recomputed |c-m|/|m|: "
        f"{summary['green_gate_pass_count']} pass / {summary['green_gate_fail_count']} fail"
    )
    print(
        f"  error_pct disagreements={summary['error_pct_disagreement_count']} "
        f"in {summary['error_pct_disagreement_file_count']} files "
        f"(structural {disagree_structural}, other {disagree_gated})"
    )
    print(
        f"  recomputed crosses 0.5% while stored does not: "
        f"{summary['error_pct_crosses_half_pct_count']} "
        f"in {summary['error_pct_crosses_half_pct_file_count']} files "
        f"(structural {cross_structural}, other {cross_gated})"
    )
    print(f"  pooled-only fails: {summary['pooled_only_fail_count']}")
    print(f"  classifier fails: {summary['classifier_fail_count']}")
    print(
        f"  STRICT scalar max<={MAX_SCALAR_ERROR_PCT}%: "
        f"{len(rows) - len(strict_fails)} pass / {len(strict_fails)} fail"
    )
    if rows and rows[0]["max_scalar_error_pct"] is not None:
        print(f"  worst scalar max: {rows[0]['max_scalar_error_pct']:.4f}% — {rows[0]['domain']}")
    if classifier_fails:
        print("\nClassifier failures (accuracy < 99.5%):")
        for r in classifier_fails[:10]:
            print(
                f"  acc={r['classifier_accuracy_pct']:.2f}% "
                f"mis={r['classifier_misclass_count']}/{r['classifier_count']}  {r['domain'][:45]}"
            )
    if green_fails:
        print("\nGREEN gate failures:")
        for r in green_fails[:10]:
            op = r["official_pooled_median_error_pct"]
            ops = f"{op:.4f}" if op is not None else "n/a"
            print(f"  pooled={ops}  {r['domain'][:45]}")
    if strict_fails:
        print(f"\nSTRICT scalar max failures: {len(strict_fails)}")
        for r in strict_fails[:15]:
            print(
                f"  {r['max_scalar_error_pct']:.4f}% {r.get('max_scalar_property')} "
                f"— {r['domain'][:40]}"
            )
    if unlisted_fail_files:
        print("\nRecomputed-gate failures with no listed disagreement:")
        for name in unlisted_fail_files:
            print(f"  {name}")
        return 1
    if classifier_fails:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())