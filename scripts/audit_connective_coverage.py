#!/usr/bin/env python3
"""Audit certified connective pieces vs what prediction engine actually applies."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_connective_registry_lib import interactive_systems_map, load_connective_registry
from fsot_developmental_predict_lib import encode_structural, predict_observables
from tier95_zebrahub_development_lib import _load_json, cache_root

WIRED = {
    "photonic_transport_from_registry",
    "longevity_genome_pressure",
    "connective_photic_observability_floor",
    "connective_early_displacement_transport",
    "connective_displacement_transport",
    "connective_midstage_division_transport",
    "connective_late_body_duration_transport",
    "connective_tail_lineage_transport",
    "connective_stability_transport",
    "connective_diagnostics",
    "genetic_ladder_fold",
    "planetary_to_stellar_adjacent_fold",
    "nuclear_gate",
}

OUT = ROOT / "data" / "tier95_connective_coverage_audit.json"


def _dataset_meta() -> list[dict]:
    tracks = _load_json(cache_root() / "tier95_zebrahub_tracks_cache.json")
    gpu = {
        s["dataset_id"]: s
        for s in _load_json(cache_root() / "tier95_zebrahub_gpu_imaging_cache.json").get("samples") or []
    }
    out = []
    for ds in tracks.get("datasets") or []:
        meta = dict(ds)
        g = gpu.get(ds["dataset_id"], {})
        meta.update(
            {
                "gpu_mean_intensity": g.get("mean_intensity"),
                "gpu_std_intensity": g.get("std_intensity"),
                "gpu_volume_shape": g.get("volume_shape"),
                "gpu_z_index_used": g.get("z_index_used"),
            }
        )
        out.append(meta)
    return out


def main() -> int:
    reg = load_connective_registry()
    systems = interactive_systems_map()
    all_sources = sorted({s for vals in systems.values() for s in vals})
    unwired = [s for s in all_sources if s not in WIRED and not s.startswith("longevity")]

    offenders = []
    for meta in _dataset_meta():
        inp = encode_structural(meta, tier="operational")
        p = predict_observables(inp, tier="operational")
        t_norm = inp.n_timesteps / 791.0
        is_tail = "tail" in inp.dataset_id.lower()
        for prop in (
            "division_rate",
            "mean_track_duration_steps",
            "mean_displacement_um",
            "developmental_stability_proxy",
        ):
            meas = float(meta.get(prop if prop != "mean_track_duration_steps" else "mean_track_duration_steps") or 0)
            if prop == "mean_track_duration_steps":
                meas = float(meta.get("mean_track_duration_steps") or 0)
            comp = float(p.get(prop) or 0)
            margin = abs(comp - meas) / abs(meas) * 100 if meas else 0
            offenders.append(
                {
                    "dataset_id": inp.dataset_id,
                    "property": prop,
                    "margin_of_error_pct": round(margin, 4),
                    "measured": meas,
                    "computed": comp,
                    "t_norm": round(t_norm, 4),
                    "is_tail": is_tail,
                    "photic": p.get("photic_coupling"),
                    "connective_active_ladder_fold": p.get("connective_active_ladder_fold"),
                    "connective_nuclear_gate": p.get("connective_nuclear_gate"),
                    "connective_displacement_transport": p.get("connective_displacement_transport"),
                    "connective_stability_transport": p.get("connective_stability_transport"),
                    "connective_tail_lineage_transport": p.get("connective_tail_lineage_transport"),
                    "habitat_extent": p.get("habitat_extent"),
                    "division_rate_pred": p.get("division_rate"),
                }
            )

    offenders.sort(key=lambda r: -r["margin_of_error_pct"])

    doc = {
        "wired_transports": sorted(WIRED),
        "interactive_systems_map": systems,
        "potentially_unwired_sources": unwired,
        "certified_gates_available": {
            "nuclear_gate": reg.nuclear_gate,
            "evolution_operon_median_err_pct": reg.evolution_operon_median_err_pct,
            "genetic_log_fold": reg.genetic_log_fold,
            "environment_log_fold": reg.environment_log_fold,
            "planetary_to_stellar_fold": reg.fold_steps.get("planetary_to_stellar_adjacent_fold"),
            "molecular_to_cellular_fold": reg.fold_steps.get("molecular_to_cellular_adjacent_fold"),
        },
        "top_offenders": offenders[:8],
        "all_margins": offenders,
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print("Top offenders:")
    for row in doc["top_offenders"]:
        print(f"  {row['margin_of_error_pct']:5.2f}% {row['dataset_id']} {row['property']} t={row['t_norm']}")
    print("Potentially unwired:", unwired)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())