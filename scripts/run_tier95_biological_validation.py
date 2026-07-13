#!/usr/bin/env python3
"""Tier 95 biological-science validation — Pearson/RMSE/σ vs literature anchors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_biological_eval_lib import (  # noqa: E402
    MECHANISTIC_PROPERTIES,
    enrich_biological_record,
    mechanistic_biological_summary,
)
from fsot_canonical_adapter import canonical_domain_scalar, load_fsot_compute  # noqa: E402
from fsot_developmental_predict_lib import leave_one_out_crossval  # noqa: E402
from ingest_zebrafish_reference_anchors import (  # noqa: E402
    anchor_for_property,
    ingest_zebrafish_reference_anchors,
    load_zebrafish_reference_anchors,
)
from tier95_zebrahub_development_lib import _load_json, _longevity_zebrafish, cache_root  # noqa: E402

OUT = ROOT / "data" / "tier95_biological_validation_report.json"


def _gpu_imaging_maps() -> tuple[dict[str, float], dict[str, float], dict[str, dict]]:
    gpu = _load_json(cache_root() / "tier95_zebrahub_gpu_imaging_cache.json")
    mean_out: dict[str, float] = {}
    std_out: dict[str, float] = {}
    env_out: dict[str, dict] = {}
    for sample in gpu.get("samples") or []:
        ds_id = str(sample.get("dataset_id") or "")
        if not ds_id:
            continue
        mean_val = float(sample.get("mean_intensity") or 0)
        std_val = float(sample.get("std_intensity") or 0)
        if mean_val > 0:
            mean_out[ds_id] = mean_val
        if std_val > 0:
            std_out[ds_id] = std_val
        shape = sample.get("volume_shape")
        if shape:
            env_out[ds_id] = {
                "gpu_volume_shape": shape,
                "gpu_z_index_used": sample.get("z_index_used"),
            }
    return mean_out, std_out, env_out


def _enrich_tier(tier_doc: dict) -> dict:
    records = []
    for row in tier_doc.get("records") or []:
        prop = str(row.get("property") or "")
        if prop not in MECHANISTIC_PROPERTIES:
            continue
        records.append(enrich_biological_record(row, reference_anchor=anchor_for_property(prop)))
    summary = mechanistic_biological_summary(records)
    return {**tier_doc, "biological_records": records, "biological_science": summary}


def main() -> int:
    tracks = _load_json(cache_root() / "tier95_zebrahub_tracks_cache.json")
    datasets = list(tracks.get("datasets") or [])
    if not datasets:
        print("No Tier 95 track datasets in cache.")
        return 1

    refs = ingest_zebrafish_reference_anchors(live=True)
    longevity = _longevity_zebrafish()
    longevity_ctx = {
        "maximum_longevity_yrs": float(longevity.get("maximum_longevity_yrs") or 5.5),
        "longevity_quotient": float(longevity.get("longevity_quotient") or 1.0),
        "metabolic_rate_w": float(longevity.get("metabolic_rate_w") or 0.35),
    }
    gpu_map, gpu_std_map, gpu_env_map = _gpu_imaging_maps()

    operational = leave_one_out_crossval(
        datasets,
        tier="operational",
        longevity=longevity_ctx,
        gpu_by_id=gpu_map,
        gpu_std_by_id=gpu_std_map,
        gpu_env_by_id=gpu_env_map,
    )
    operational_bio = _enrich_tier(operational)

    _, authority = load_fsot_compute()
    biology_scalar = float(canonical_domain_scalar("Biology"))
    fast_check = operational.get("mpmath_equivalence") or {}
    bio = operational_bio.get("biological_science") or {}

    report = {
        "source": "tier95_zebrahub_biological_science_validation",
        "evaluation_standard": "developmental_cell_tracking_literature",
        "primary_metrics": [
            "margin_of_error_pct",
            "median_margin_of_error_pct",
            "pearson_r",
            "spearman_rho",
            "r_squared",
            "rmse",
            "mae",
            "sigma_equivalent",
            "within_literature_band_fraction",
        ],
        "margin_of_error_definition": (
            "|computed - measured| / |measured| * 100 — same grading-style % accuracy "
            "used in high-school/college; how far off the observable we are."
        ),
        "alphafold_analog_note": (
            "AlphaFold reports structural metrics (lDDT, GDT, TM-score, RMSD in Å), not % off "
            "a tabulated answer. Our % margin is the direct 'how wrong am I' readout."
        ),
        "precision_gates_pct": {
            "push_target": 0.5,
            "alphafold_aspiration": 0.02,
            "description": "Beat AlphaFold credibility in genetics: all mechanistic margins under 0.5%; "
            "0.02% is world-class scalar precision.",
        },
        "dataset_count": len(datasets),
        "reference_anchors": load_zebrafish_reference_anchors(),
        "longevity_anchor": longevity_ctx,
        "formal_oracle": {
            "authority_path": str(authority),
            "biology_domain_scalar": round(biology_scalar, 8),
            "mpmath_float64_equiv_ok": bool(fast_check.get("ok")),
        },
        "operational_tier": operational_bio,
        "headline": {
            "median_margin_of_error_pct": bio.get("median_margin_of_error_pct"),
            "mean_margin_of_error_pct": bio.get("mean_margin_of_error_pct"),
            "max_margin_of_error_pct": bio.get("max_margin_of_error_pct"),
            "push_target_pct": 0.5,
            "alphafold_aspiration_pct": 0.02,
            "under_push_target_count": sum(
                1
                for row in (bio.get("accuracy_scorecard") or [])
                if float(row.get("margin_of_error_pct") or 0) <= 0.5
            ),
            "total_mechanistic_count": len(bio.get("accuracy_scorecard") or []),
            "accuracy_scorecard": bio.get("accuracy_scorecard") or [],
            "per_property": (bio.get("per_property") or {}),
            "pearson_r": bio.get("pearson_r"),
            "spearman_rho": bio.get("spearman_rho"),
            "r_squared": bio.get("r_squared"),
            "mean_sigma_equivalent": bio.get("mean_sigma_equivalent"),
            "within_literature_band_fraction": bio.get("within_literature_band_fraction"),
        },
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=== Tier 95 Accuracy (margin of error %) ===")
    h = report["headline"]
    print(f"Median margin off:  {h.get('median_margin_of_error_pct')}%")
    print(f"Mean margin off:    {h.get('mean_margin_of_error_pct')}%")
    print(f"Worst margin off:   {h.get('max_margin_of_error_pct')}%")
    print(f"Push target:        {h.get('push_target_pct')}%  "
          f"({h.get('under_push_target_count')}/{h.get('total_mechanistic_count')} under)")
    print(f"AlphaFold class:    {h.get('alphafold_aspiration_pct')}%")
    print("--- scorecard (measured -> computed, % off) ---")
    for row in h.get("accuracy_scorecard") or []:
        print(
            f"  {row.get('margin_of_error_pct'):6.2f}%  {row.get('dataset_id'):14s}  "
            f"{row.get('property'):35s}  "
            f"meas={row.get('measured')}  comp={row.get('computed')}  ({row.get('unit')})"
        )
    print("--- scientific measurement (Δ, σ_equiv, literature band) ---")
    bio_records = (operational_bio.get("biological_records") or [])
    by_key = {
        (r.get("dataset_id"), r.get("property")): r
        for r in bio_records
    }
    for row in h.get("accuracy_scorecard") or []:
        full = by_key.get((row.get("dataset_id"), row.get("property"))) or {}
        print(
            f"  {row.get('dataset_id'):14s}  {row.get('property'):35s}  "
            f"Δ={full.get('delta')} {row.get('unit')}  "
            f"σ={full.get('sigma_equivalent')}  "
            f"ref_unc={full.get('reference_uncertainty_pct')}%  "
            f"in_band={full.get('within_literature_band')}"
        )
    print("--- per-property median % off ---")
    for prop, stats in sorted((h.get("per_property") or {}).items()):
        print(
            f"  {prop}: median={stats.get('median_margin_of_error_pct')}%  "
            f"max={stats.get('max_margin_of_error_pct')}%  "
            f"(RMSE={stats.get('rmse')} {stats.get('unit')})"
        )
    print("--- biological cross-checks ---")
    print(f"Pearson r: {h.get('pearson_r')}  R²: {h.get('r_squared')}  within_lit_band: {h.get('within_literature_band_fraction')}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())