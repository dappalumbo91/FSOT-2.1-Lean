#!/usr/bin/env python3
"""Build per-observable SOTA ledger with live FSOT errors from benchmarks."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sota_observable_ledger.yaml"
OUTPUT = ROOT / "data" / "sota_observable_ledger_report.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _bench_value(doc: dict, prop: str) -> tuple[float | None, float | None]:
    for row in doc.get("records") or []:
        name = row.get("name") or row.get("property")
        if name == prop or row.get("property") == prop:
            return float(row.get("computed", 0)), float(row.get("error_pct", 0))
    if prop in doc and isinstance(doc[prop], (int, float)):
        return float(doc[prop]), float(doc[prop])
    if "." in prop:
        cur: object = doc
        for part in prop.split("."):
            if isinstance(cur, dict):
                cur = cur.get(part)
            else:
                cur = None
                break
        if isinstance(cur, (int, float)):
            return float(cur), float(cur)
    return None, None


def _comparison_class(row: dict) -> str:
    explicit = row.get("comparison_class")
    if explicit:
        return str(explicit)
    oid = str(row.get("id") or "")
    name = str(row.get("name") or "").lower()
    unit = str(row.get("unit") or "")
    if oid.startswith("mgr_") or "formula_corpus_closure" in oid:
        return "internal_pipeline_metric"
    if any(
        tok in oid
        for tok in (
            "_pooled",
            "_section",
            "_gap_fill_pooled",
            "_tier_g_pooled",
            "_tier_e_pooled",
            "_bridge",
        )
    ):
        return "internal_pipeline_metric"
    if "pooled_median" in name or "section_median" in name:
        return "internal_pipeline_metric"
    if unit == "misclassification_pct":
        return "classifier_pipeline_metric"
    return "external_observable"


def _compare_observable(row: dict, computed: float | None, fsot_err: float | None) -> tuple[str, float | None]:
    metric = row.get("comparison_metric") or "error_pct"
    if metric == "rmse":
        sota_val = float(row.get("measured") or row.get("sota_rmse") or 99.0)
        fsot_val = computed if computed is not None else fsot_err
        if fsot_val is None:
            return "structural_only", None
        margin = sota_val - float(fsot_val)
        if float(fsot_val) < sota_val:
            return "beats_sota", margin
        if float(fsot_val) <= sota_val * 1.05:
            return "meets_sota", margin
        return "below_sota", margin

    sota_err = float(row.get("sota_typical_error_pct") or 99.0)
    if fsot_err is None:
        return "structural_only", None
    margin = sota_err - float(fsot_err)
    if float(fsot_err) < sota_err:
        return "beats_sota", margin
    if float(fsot_err) <= sota_err * 1.05:
        return "meets_sota", margin
    return "below_sota", margin


def build(ledger_path: Path = LEDGER) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    records: list[dict] = []
    beats = 0
    headline_beats = 0
    for row in spec.get("observables") or []:
        fsot_err = row.get("fsot_error_pct")
        computed = row.get("fsot_computed")
        if row.get("fsot_source"):
            src = _load_json(ROOT / row["fsot_source"])
            prop = row.get("fsot_property") or row["id"]
            comp, err = _bench_value(src, prop)
            if comp is not None:
                computed = comp
            if err is not None:
                fsot_err = err
        status, margin = _compare_observable(row, computed, fsot_err)
        comp_class = _comparison_class(row)
        exclude_headline = bool(
            row.get("exclude_from_headline_beats")
            or comp_class != "external_observable"
        )
        if status in ("beats_sota", "meets_sota"):
            beats += 1
            if not exclude_headline:
                headline_beats += 1
        entry = {
            **row,
            "comparison_class": comp_class,
            "exclude_from_headline_beats": exclude_headline,
            "fsot_computed": computed,
            "fsot_error_pct": fsot_err,
            "margin_vs_sota_pct": margin,
            "status": status,
            "parameter_advantage": int(row.get("sota_free_parameters") or 0),
        }
        if row.get("comparison_metric") == "rmse" and computed is not None:
            entry["fsot_rmse"] = computed
            entry["sota_rmse"] = float(row.get("sota_rmse") or row.get("measured") or 0.0)
            entry["fsot_error_pct"] = computed
            entry["sota_typical_error_pct"] = entry["sota_rmse"]
        records.append(entry)
    compared = [r for r in records if r.get("fsot_error_pct") is not None]
    below = [r["id"] for r in records if r.get("status") == "below_sota"]
    headline_records = [r for r in records if not r.get("exclude_from_headline_beats")]
    headline_below = [r["id"] for r in headline_records if r.get("status") == "below_sota"]
    internal_count = sum(
        1 for r in records if r.get("comparison_class") == "internal_pipeline_metric"
    )
    return {
        "report_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "observable_count": len(records),
        "headline_eligible_count": len(headline_records),
        "internal_pipeline_metric_count": internal_count,
        "compared_count": len(compared),
        "beats_or_meets_sota_count": beats,
        "headline_beats_or_meets_count": headline_beats,
        "below_sota_ids": below,
        "headline_below_sota_ids": headline_below,
        "fsot_free_parameters": int(spec.get("fsot_engine", {}).get("free_parameters", 0)),
        "parameter_audit_note": (
            "See data/parameter_count_audit.json — engine uses intrinsic constants "
            "plus per-domain D_eff/δψ assignments, not a zero-knob claim."
        ),
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SOTA observable ledger report")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    report = build()
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  observables: {report['observable_count']}  beats/meets: {report['beats_or_meets_sota_count']}")
    if report["below_sota_ids"]:
        print(f"  below SOTA: {report['below_sota_ids']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())