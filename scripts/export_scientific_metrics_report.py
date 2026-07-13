#!/usr/bin/env python3
"""Export repo-wide scientific metrics — Δ, σ, units, % margin for GitHub findings."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import analyze_benchmark, classify_record  # noqa: E402
from fsot_biological_eval_lib import (  # noqa: E402
    MECHANISTIC_PROPERTIES,
    enrich_biological_record,
    mechanistic_biological_summary,
    margin_of_error_scorecard,
)
from ingest_zebrafish_reference_anchors import anchor_for_property  # noqa: E402
from scientific_measurement_lib import (  # noqa: E402
    domain_precision_summary,
    literature_aware_error_pct,
    measurement_envelope,
    relative_error_pct,
)

OUT_JSON = DATA / "scientific_metrics_github_report.json"
TIER95_REPORT = DATA / "tier95_biological_validation_report.json"


def _scalar_records(doc: dict) -> list[dict]:
    rows = doc.get("material_records") or doc.get("records") or []
    return [r for r in rows if classify_record(r) == "scalar"]


def _scientific_row(record: dict) -> dict | None:
    measured = record.get("measured")
    computed = record.get("computed")
    if measured is None or computed is None:
        return None
    try:
        meas_f = float(measured)
        comp_f = float(computed)
    except (TypeError, ValueError):
        return None

    env = record.get("scientific_measurement") or measurement_envelope(record)
    aware = literature_aware_error_pct(comp_f, meas_f, record)
    margin = float(aware.get("raw_error_pct") or relative_error_pct(comp_f, meas_f))
    delta = comp_f - meas_f

    return {
        "name": record.get("name") or record.get("dataset_id"),
        "property": record.get("property"),
        "measured": meas_f,
        "computed": comp_f,
        "unit": env.get("unit") or record.get("unit"),
        "delta": round(delta, 8),
        "abs_delta": round(abs(delta), 8),
        "margin_of_error_pct": round(margin, 4),
        "sigma_equivalent": env.get("sigma_equivalent") or record.get("sigma_equivalent"),
        "reference_uncertainty_pct": env.get("reference_uncertainty_pct")
        or record.get("reference_uncertainty_pct"),
        "within_literature_band": bool(
            env.get("within_literature_band") or aware.get("within_literature_band")
        ),
        "comparison_kind": env.get("comparison_kind") or aware.get("comparison_kind"),
        "precision_tier": env.get("precision_tier"),
        "reference": env.get("reference") or record.get("reference"),
        "reference_source": record.get("source") or record.get("reference_source"),
    }


def _scan_benchmark(path: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    scalars = _scalar_records(doc)
    sci_rows = [r for r in (_scientific_row(s) for s in scalars) if r]
    margin = analyze_benchmark(doc, file_name=path.name)
    summary = domain_precision_summary(scalars)

    return {
        "benchmark_file": path.name,
        "benchmark_stem": path.stem,
        "scalar_count": len(scalars),
        "scientific_record_count": len(sci_rows),
        "median_margin_of_error_pct": margin.get("median_error_pct"),
        "max_margin_of_error_pct": margin.get("max_error_pct"),
        "mean_abs_delta": summary.get("mean_abs_delta"),
        "green_gate_fraction": summary.get("green_gate_fraction"),
        "matches_domain_spine": summary.get("matches_domain_spine"),
        "precision_tier_counts": summary.get("precision_tier_counts"),
        "top_offenders": sorted(
            sci_rows,
            key=lambda r: -float(r.get("margin_of_error_pct") or 0.0),
        )[:5],
    }


def _genetics_panel() -> dict:
    if not TIER95_REPORT.exists():
        return {"available": False}

    doc = json.loads(TIER95_REPORT.read_text(encoding="utf-8"))
    headline = doc.get("headline") or {}
    operational = doc.get("operational_tier") or {}
    bio_records = operational.get("biological_records") or []

    scientific_cards = []
    for rec in bio_records:
        if rec.get("property") not in MECHANISTIC_PROPERTIES:
            continue
        scientific_cards.append(
            {
                "dataset_id": rec.get("dataset_id"),
                "property": rec.get("property"),
                "unit": rec.get("unit"),
                "measured": rec.get("measured"),
                "computed": rec.get("computed"),
                "delta": rec.get("delta"),
                "abs_delta": rec.get("abs_delta"),
                "margin_of_error_pct": rec.get("margin_of_error_pct"),
                "sigma_equivalent": rec.get("sigma_equivalent"),
                "reference_uncertainty_pct": rec.get("reference_uncertainty_pct"),
                "within_literature_band": rec.get("within_literature_band"),
                "comparison_kind": rec.get("comparison_kind"),
                "reference": rec.get("reference"),
                "reference_source": rec.get("reference_source"),
                "scientific_measurement": rec.get("scientific_measurement"),
            }
        )

    return {
        "available": True,
        "panel": "tier95_zebrahub_developmental_genetics",
        "evaluation_standard": doc.get("evaluation_standard"),
        "species": (doc.get("reference_anchors") or {}).get("species"),
        "dataset_count": doc.get("dataset_count"),
        "property_count": len(MECHANISTIC_PROPERTIES),
        "mechanistic_record_count": len(scientific_cards),
        "median_margin_of_error_pct": headline.get("median_margin_of_error_pct"),
        "mean_margin_of_error_pct": headline.get("mean_margin_of_error_pct"),
        "max_margin_of_error_pct": headline.get("max_margin_of_error_pct"),
        "under_push_target_count": headline.get("under_push_target_count"),
        "total_mechanistic_count": headline.get("total_mechanistic_count"),
        "push_target_pct": headline.get("push_target_pct"),
        "pearson_r": headline.get("pearson_r"),
        "r_squared": headline.get("r_squared"),
        "mean_sigma_equivalent": headline.get("mean_sigma_equivalent"),
        "within_literature_band_fraction": headline.get("within_literature_band_fraction"),
        "per_property": headline.get("per_property"),
        "accuracy_scorecard": headline.get("accuracy_scorecard"),
        "scientific_records": sorted(
            scientific_cards,
            key=lambda r: (-float(r.get("margin_of_error_pct") or 0.0), str(r.get("dataset_id"))),
        ),
        "alphafold_analog_note": doc.get("alphafold_analog_note"),
        "margin_of_error_definition": doc.get("margin_of_error_definition"),
    }


def main() -> int:
    benchmarks = sorted(DATA.glob("*_benchmark.json"))
    domains = [_scan_benchmark(p) for p in benchmarks if p.name not in {"tier_95_zebrafish_spine_benchmark.json"}]

    genetics = _genetics_panel()
    all_margins = [
        float(d["median_margin_of_error_pct"])
        for d in domains
        if d.get("median_margin_of_error_pct") is not None
    ]
    if genetics.get("available") and genetics.get("median_margin_of_error_pct") is not None:
        all_margins.append(float(genetics["median_margin_of_error_pct"]))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "fsot_repo_scientific_metrics_export",
        "reporting_standard": {
            "margin_of_error_pct": "|computed - measured| / |measured| * 100",
            "delta": "computed - measured (signed residual, same unit as observable)",
            "sigma_equivalent": "|margin_pct| / literature_reference_uncertainty_pct",
            "within_literature_band": "margin_pct <= reference_uncertainty_pct when σ metadata known",
            "units": "SI or domain-standard (μm, imaging_frames, dimensionless, etc.)",
        },
        "precision_gates_pct": {
            "push_target": 0.5,
            "alphafold_aspiration": 0.02,
            "green_scalar_gate": 0.02,
            "green_median_gate": 0.02,
        },
        "repo_headline": {
            "benchmark_file_count": len(benchmarks),
            "domain_summaries_count": len(domains),
            "pooled_domain_median_margin_pct": sorted(all_margins)[len(all_margins) // 2]
            if all_margins
            else None,
            "genetics_panel_under_push_target": (
                f"{genetics.get('under_push_target_count')}/{genetics.get('total_mechanistic_count')}"
                if genetics.get("available")
                else None
            ),
        },
        "genetics_developmental_panel": genetics,
        "domain_benchmarks": sorted(
            domains,
            key=lambda d: float(d.get("median_margin_of_error_pct") or 0.0),
            reverse=True,
        ),
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=== FSOT Scientific Metrics Export (GitHub-ready) ===")
    print(f"Benchmark files scanned: {len(benchmarks)}")
    print(f"Domain summaries:        {len(domains)}")
    if genetics.get("available"):
        g = genetics
        print("--- Genetics / Tier 95 developmental panel ---")
        print(
            f"  {g.get('under_push_target_count')}/{g.get('total_mechanistic_count')} "
            f"under {g.get('push_target_pct')}% push target"
        )
        print(
            f"  median margin={g.get('median_margin_of_error_pct')}%  "
            f"worst={g.get('max_margin_of_error_pct')}%  "
            f"r={g.get('pearson_r')}  R²={g.get('r_squared')}"
        )
        print("  scientific records (Δ, unit, σ, % margin):")
        for row in g.get("scientific_records") or []:
            print(
                f"    {row.get('margin_of_error_pct'):5.2f}%  σ={row.get('sigma_equivalent')}  "
                f"Δ={row.get('delta')} {row.get('unit')}  "
                f"{row.get('dataset_id')}/{row.get('property')}  "
                f"meas={row.get('measured')} comp={row.get('computed')}"
            )
    print(f"Wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())