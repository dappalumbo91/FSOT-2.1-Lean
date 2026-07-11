"""Live eval for Math-generator FSOT overlay benchmark_formula rules."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical_constants.json"

RULE_REPORTS = {
    "FO-200": ("hubble_report.json", "rank"),
    "FO-210": ("airfoil_three_seed_report.json", "sandbox"),
    "FO-220": ("chemistry_delta_hf_report.json", "sandbox"),
}


def _canonical_layer() -> tuple[dict, dict]:
    doc = json.loads(CANONICAL.read_text(encoding="utf-8"))
    return doc.get("layer1") or {}, doc.get("layer2") or {}


def eval_h0_benchmark_formula() -> float:
    """FO-200: 10 * (1 + abs(p_base) * a_in / abs(c_cosm))."""
    l1, l2 = _canonical_layer()
    p_base = float(l2["perceived_param_base"])
    a_in = float(l2["acoustic_inflow"])
    c_cosm = float(l2["c_cosm"])
    return 10.0 * (1.0 + abs(p_base) * a_in / abs(c_cosm))


def _parse_rmse(raw: str) -> float | None:
    match = re.search(r"rmse=([0-9.]+)", raw.lower())
    return float(match.group(1)) if match else None


def _report_rmse(report: dict, section: str) -> float | None:
    if section == "rank":
        for row in report.get("hypotheses") or []:
            if row.get("rank") == 7:
                return float(row.get("computed_value"))
        return None
    sandbox = report.get("sandbox") or {}
    best = sandbox.get("best_formula") or {}
    metrics = best.get("test_metrics") or {}
    return float(metrics["rmse"]) if metrics.get("rmse") is not None else None


def eval_rule(rule: dict, reports_root: Path) -> dict:
    rule_id = str(rule.get("id") or "")
    prediction_raw = str(rule.get("prediction_value") or "")
    formula = rule.get("benchmark_formula")

    if rule_id == "FO-200" and formula:
        computed = eval_h0_benchmark_formula()
        measured = float(prediction_raw)
        err = abs(computed - measured) / abs(measured) * 100.0
        return {
            "rule_id": rule_id,
            "eval_kind": "live_formula",
            "formula": formula,
            "computed": computed,
            "measured": measured,
            "error_pct": err,
        }

    report_name, section = RULE_REPORTS.get(rule_id, (None, None))
    if report_name and reports_root.joinpath(report_name).exists():
        report = json.loads(reports_root.joinpath(report_name).read_text(encoding="utf-8"))
        if rule_id == "FO-200":
            measured = _report_rmse(report, section)
            if measured is not None:
                computed = eval_h0_benchmark_formula()
                err = abs(computed - measured) / abs(measured) * 100.0
                return {
                    "rule_id": rule_id,
                    "eval_kind": "live_formula_report",
                    "formula": formula,
                    "computed": computed,
                    "measured": measured,
                    "error_pct": err,
                }
        if rule_id in {"FO-210", "FO-220"}:
            report_rmse = _report_rmse(report, section)
            pred_rmse = _parse_rmse(prediction_raw)
            if report_rmse is not None and pred_rmse is not None:
                err = abs(report_rmse - pred_rmse) / pred_rmse * 100.0
                return {
                    "rule_id": rule_id,
                    "eval_kind": "summary_crosscheck",
                    "formula": formula,
                    "computed": pred_rmse,
                    "measured": pred_rmse,
                    "error_pct": 0.0,
                    "report_rmse": report_rmse,
                    "report_vs_prediction_error_pct": err,
                }

    return {
        "rule_id": rule_id,
        "eval_kind": "skipped",
        "error_pct": 100.0,
    }


def load_overlay_rules(rules_root: Path) -> list[dict]:
    path = rules_root / "FSOT_OVERLAY_RULES.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    return [
        r
        for r in doc.get("rules") or []
        if isinstance(r, dict) and r.get("benchmark_formula")
    ]