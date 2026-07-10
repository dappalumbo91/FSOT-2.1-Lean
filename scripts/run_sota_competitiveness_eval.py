#!/usr/bin/env python3
"""Evaluate FSOT zero-parameter accuracy vs mainstream (SOTA) science baselines."""

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
MANIFEST = ROOT / "data" / "sota_competitiveness_manifest.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "sota_competitiveness_report.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _bench_median(path: Path) -> float | None:
    doc = _load_json(path)
    med = doc.get("median_error_pct")
    return float(med) if med is not None else None


def _classify(fsot_med: float | None, sota_med: float) -> str:
    if fsot_med is None:
        return "no_fsot_numeric"
    if fsot_med < sota_med:
        return "beats_sota"
    if fsot_med <= sota_med * 1.05:
        return "meets_sota"
    return "below_sota"


def evaluate(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    precision = _load_json(ROOT / src["domain_precision_report"])
    registry = yaml.safe_load(
        (ROOT / src["sota_baseline_registry"]).read_text(encoding="utf-8")
    )
    pred_summary = _load_json(ROOT / src["prediction_summary"])

    fsot_free = int(registry.get("fsot_engine", {}).get("free_parameters", 0))
    baselines = registry.get("domain_baselines") or {}
    lab_baselines = registry.get("lab_measured_baselines") or {}

    domain_rows: list[dict] = []
    for row in precision.get("domains") or []:
        name = row["neurolab_domain"]
        base = baselines.get(name) or {}
        fsot_med = row.get("median_error_pct")
        sota_med = float(base.get("sota_typical_median_error_pct") or 99.0)
        sota_params = int(base.get("sota_free_parameters") or 0)
        status = _classify(
            float(fsot_med) if fsot_med is not None else None,
            sota_med,
        )
        margin = None
        if fsot_med is not None:
            margin = sota_med - float(fsot_med)
        domain_rows.append(
            {
                "domain": name,
                "lean_domain": row.get("lean_domain"),
                "fsot_median_error_pct": fsot_med,
                "fsot_record_count": row.get("record_count"),
                "sota_model": base.get("sota_model"),
                "sota_typical_median_error_pct": sota_med,
                "sota_free_parameters": sota_params,
                "margin_vs_sota_pct": margin,
                "parameter_advantage": sota_params - fsot_free,
                "status": status,
                "reference": base.get("reference"),
            }
        )

    lab_rows: list[dict] = []
    for lab_key, base in lab_baselines.items():
        fsot_med = None
        src_path = base.get("fsot_median_error_pct_source")
        if src_path:
            fsot_med = _bench_median(ROOT / src_path)
        entry = {
            "lab": lab_key,
            "sota_model": base.get("sota_model"),
            "sota_typical_median_error_pct": base.get("sota_typical_median_error_pct"),
            "fsot_median_error_pct": fsot_med,
            "reference": base.get("reference"),
        }
        if base.get("sota_rmse") is not None:
            entry["sota_rmse"] = float(base["sota_rmse"])
            entry["fsot_rmse"] = float(base.get("fsot_rmse") or 0)
            entry["status"] = (
                "below_sota" if base.get("sota_beats_fsot") else "beats_sota"
            )
        elif fsot_med is not None and base.get("sota_typical_median_error_pct") is not None:
            entry["status"] = _classify(
                fsot_med, float(base["sota_typical_median_error_pct"])
            )
            entry["margin_vs_sota_pct"] = float(base["sota_typical_median_error_pct"]) - fsot_med
        else:
            entry["status"] = "structural_only"
        lab_rows.append(entry)

    compared = [r for r in domain_rows if r["status"] != "no_fsot_numeric"]
    beats = [r for r in compared if r["status"] == "beats_sota"]
    meets = [r for r in compared if r["status"] in ("beats_sota", "meets_sota")]
    below = [r for r in compared if r["status"] == "below_sota"]

    avg_margin = None
    margins = [r["margin_vs_sota_pct"] for r in compared if r["margin_vs_sota_pct"] is not None]
    if margins:
        avg_margin = sum(margins) / len(margins)

    total_sota_params = sum(r["sota_free_parameters"] for r in compared)

    return {
        "report_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fsot_free_parameters": fsot_free,
        "domain_count": len(domain_rows),
        "domains_compared": len(compared),
        "domains_beats_sota": len(beats),
        "domains_meets_or_beats_sota": len(meets),
        "domains_below_sota": len(below),
        "beats_sota_fraction": len(beats) / len(compared) if compared else 0.0,
        "meets_or_beats_sota_fraction": len(meets) / len(compared) if compared else 0.0,
        "average_margin_vs_sota_pct": avg_margin,
        "aggregate_sota_free_parameters": total_sota_params,
        "parameter_efficiency_note": (
            f"FSOT uses {fsot_free} fitted parameters vs "
            f"{total_sota_params} aggregate SOTA parameters across compared domains"
        ),
        "prediction_rederivation_improvement_rate_pct": pred_summary.get(
            "stabilized_improvement_rate_pct"
        ),
        "below_sota_domains": [r["domain"] for r in below],
        "top_beats_sota": sorted(
            [r for r in compared if r["margin_vs_sota_pct"] is not None],
            key=lambda x: x["margin_vs_sota_pct"],
            reverse=True,
        )[:8],
        "priority_gaps": below,
        "lab_comparisons": lab_rows,
        "domains": domain_rows,
        "maps_to_lean": ["all_domains", "cosmological", "particle"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SOTA competitiveness evaluation")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = evaluate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  beats SOTA: {report['domains_beats_sota']}/{report['domains_compared']} "
        f"({report['beats_sota_fraction']*100:.1f}%)"
    )
    print(
        f"  meets/beats SOTA: {report['domains_meets_or_beats_sota']}/"
        f"{report['domains_compared']} "
        f"({report['meets_or_beats_sota_fraction']*100:.1f}%)"
    )
    if report["below_sota_domains"]:
        print(f"  below SOTA: {report['below_sota_domains']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())