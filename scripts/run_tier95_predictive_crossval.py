#!/usr/bin/env python3
"""Tier 95 intrinsic FSOT predictive cross-validation (strict + operational tiers)."""

from __future__ import annotations

import json
import os
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
from ingest_zebrafish_reference_anchors import anchor_for_property, load_zebrafish_reference_anchors  # noqa: E402
from tier95_zebrahub_development_lib import _load_json, _longevity_zebrafish, cache_root  # noqa: E402

OUT = ROOT / "data" / "tier95_predictive_crossval_report.json"


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


def main() -> int:
    tracks = _load_json(cache_root() / "tier95_zebrahub_tracks_cache.json")
    datasets = list(tracks.get("datasets") or [])
    if not datasets:
        print("No Tier 95 track datasets in cache.")
        return 1

    longevity = _longevity_zebrafish()
    lq = float(longevity.get("longevity_quotient") or 1.0)
    longevity_ctx = {
        "maximum_longevity_yrs": float(longevity.get("maximum_longevity_yrs") or 5.5),
        "longevity_quotient": lq,
        "metabolic_rate_w": float(longevity.get("metabolic_rate_w") or 0.35),
    }
    gpu_map, gpu_std_map, gpu_env_map = _gpu_imaging_maps()

    strict = leave_one_out_crossval(
        datasets,
        tier="strict",
        longevity=longevity_ctx,
        gpu_by_id=gpu_map,
        gpu_std_by_id=gpu_std_map,
        gpu_env_by_id=gpu_env_map,
    )
    operational = leave_one_out_crossval(
        datasets,
        tier="operational",
        longevity=longevity_ctx,
        gpu_by_id=gpu_map,
        gpu_std_by_id=gpu_std_map,
        gpu_env_by_id=gpu_env_map,
    )

    mod, authority = load_fsot_compute()
    biology_scalar = float(canonical_domain_scalar("Biology"))
    fast_check = strict.get("mpmath_equivalence") or {}

    mech_props = set(MECHANISTIC_PROPERTIES)

    def _attach_biological_science(tier_doc: dict) -> dict:
        bio_records = [
            enrich_biological_record(row, reference_anchor=anchor_for_property(str(row.get("property") or "")))
            for row in tier_doc.get("records") or []
            if row.get("property") in mech_props
        ]
        return mechanistic_biological_summary(bio_records)

    def _mech_median(tier_doc: dict) -> float:
        errs = [
            float(r["error_pct"])
            for r in tier_doc.get("records") or []
            if r.get("property") in mech_props
        ]
        return sorted(errs)[len(errs) // 2] if errs else 0.0

    report = {
        "source": "tier95_zebrahub_intrinsic_fsot_prediction",
        "dataset_count": len(datasets),
        "longevity_anchor": longevity_ctx,
        "mechanistic_properties": sorted(mech_props),
        "formal_oracle": {
            "authority_path": str(authority),
            "biology_domain_scalar": round(biology_scalar, 8),
            "mpmath_float64_equiv_ok": bool(fast_check.get("ok")),
            "mpmath_max_rel_err": fast_check.get("max_rel_err"),
        },
        "strict_tier": strict,
        "operational_tier": operational,
        "mechanistic_median_error_pct": {
            "strict": round(_mech_median(strict), 6),
            "operational": round(_mech_median(operational), 6),
        },
        "biological_science": {
            "evaluation_standard": "developmental_cell_tracking_literature",
            "primary_metrics": [
                "pearson_r",
                "spearman_rho",
                "r_squared",
                "rmse",
                "mae",
                "sigma_equivalent",
                "within_literature_band_fraction",
            ],
            "reference_anchors": load_zebrafish_reference_anchors(),
            "strict_tier": _attach_biological_science(strict),
            "operational_tier": _attach_biological_science(operational),
        },
        "interpretation": (
            "strict tier uses only n_timesteps + species longevity; "
            "operational tier adds detection census (not lineage outcomes) as population N; "
            "fsot_connective_registry_lib composes certified domain scalars, adjacent-rung "
            "fold steps, longevity spine, and photonic environment stack (~0.02% gate) "
            "across proliferation, motility, stability, and imaging interactive systems."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    op_bio = report["biological_science"]["operational_tier"]
    print("=== Tier 95 FSOT intrinsic prediction (LODO) ===")
    print(f"strict:      median margin off = {report['mechanistic_median_error_pct']['strict']:.4f}%")
    print(f"operational: median margin off = {report['mechanistic_median_error_pct']['operational']:.4f}%")
    print(f"operational: mean margin off   = {op_bio.get('mean_margin_of_error_pct')}%")
    print(f"operational: worst margin off  = {op_bio.get('max_margin_of_error_pct')}%")
    print(f"AlphaFold aspiration gate: 0.02%")
    for row in (op_bio.get("accuracy_scorecard") or [])[:5]:
        print(
            f"  {row.get('margin_of_error_pct'):5.2f}%  {row.get('dataset_id')}  "
            f"{row.get('property')}  meas={row.get('measured')}  comp={row.get('computed')}"
        )
    print(f"biological cross-check: r={op_bio.get('pearson_r')} R²={op_bio.get('r_squared')}")
    print(f"mpmath≡float64: {fast_check.get('ok')} max_rel={fast_check.get('max_rel_err')}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())