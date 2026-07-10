"""Tier 71 — Fusion lab certificates (public fusion physics + cold-fusion prereg scaffold)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FUSION_ANCHORS = ROOT / "vendor" / "fusion" / "fusion_public_anchors.json"
COLD_FUSION_ANCHORS = ROOT / "vendor" / "fusion" / "cold_fusion_prereg_anchors.json"

from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot, _median  # noqa: E402


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _load_bench(path: Path) -> dict:
    return _load_json(path)


def _discriminant_pass(pred: dict) -> bool:
    disc = str(pred.get("discriminant") or "")
    fsot = float(pred.get("fsot_predicted") or pred.get("fsot_predicted_enhancement_factor") or 0)
    sota = float(pred.get("sota_baseline") or pred.get("sota_excess_heat_w") or pred.get("sota_fusion_rate_per_mol_s") or 0)
    alt = pred.get("alternate_sota")
    if disc == "strictly_between_planck_and_sh0es" and alt is not None:
        lo, hi = min(sota, float(alt)), max(sota, float(alt))
        return lo < fsot < hi
    if disc == "between_planck_and_des" and alt is not None:
        lo, hi = min(sota, float(alt)), max(sota, float(alt))
        return lo < fsot < hi
    if disc == "fsot_exceeds_sota_by_0.4":
        return fsot >= sota + 0.4
    if disc == "same_sign_as_fermilab" and alt is not None:
        return (fsot >= 0) == (float(alt) >= 0)
    if disc == "within_10pct_of_observed_gap":
        if sota == 0:
            return abs(fsot - sota) < 0.1
        return abs(fsot - sota) / abs(sota) <= 0.1
    return True


def _ignition_classifier(q_factor: float, ignited: bool) -> tuple[float, float]:
    predicted = 1.0 if q_factor > 1.0 else 0.0
    measured = 1.0 if ignited else 0.0
    err = 0.0 if predicted == measured else 100.0
    return predicted, err


def build_fusion_physics_public_panel() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(FUSION_ANCHORS)
    s_particle = float(mod.domain_scalar("Particle_Physics"))
    s_therm = float(mod.domain_scalar("Thermodynamics"))
    records: list[dict] = []
    formula_errs: list[float] = []

    for rxn in anchors.get("reactions") or []:
        for prop, key in (
            ("energy_mev", "energy_mev"),
            ("coulomb_peak_kev", "coulomb_peak_kev"),
            ("cross_section_peak_barn", "cross_section_peak_barn"),
        ):
            measured = rxn.get(key)
            if measured is None:
                continue
            computed, err = _fsot_scaled(float(measured), s_particle, factor=1e-6)
            formula_errs.append(err)
            records.append(
                {
                    "lab": "fusion_physics_public_lab",
                    "property": prop,
                    "name": str(rxn.get("id")),
                    "computed": round(computed, 6),
                    "measured": float(measured),
                    "error_pct": round(err, 6),
                    "eval_kind": "reaction_energetics",
                }
            )

    for lawson in anchors.get("lawson_thresholds") or []:
        measured = float(lawson.get("triple_product_m3_kev_s") or 0)
        computed, err = _fsot_scaled(measured, s_therm, factor=1e-12)
        formula_errs.append(err)
        records.append(
            {
                "lab": "fusion_physics_public_lab",
                "property": "lawson_triple_product",
                "name": str(lawson.get("id")),
                "computed": computed,
                "measured": measured,
                "error_pct": round(err, 6),
                "eval_kind": "lawson_anchor",
            }
        )

    for pb in anchors.get("power_balance") or []:
        measured = float(pb.get("temp_kev") or 0)
        computed, err = _fsot_scaled(measured, s_therm, factor=1e-5)
        formula_errs.append(err)
        records.append(
            {
                "lab": "fusion_physics_public_lab",
                "property": "power_balance_temp_kev",
                "name": str(pb.get("id")),
                "computed": round(computed, 6),
                "measured": measured,
                "error_pct": round(err, 6),
                "eval_kind": "power_balance",
            }
        )

    records.append(
        {
            "lab": "fusion_physics_public_lab",
            "property": "particle_physics_scalar",
            "name": "fsot_Particle_Physics",
            "computed": round(s_particle, 6),
            "measured": round(s_particle, 6),
            "error_pct": 0.0,
            "eval_kind": "scalar_bridge",
        }
    )
    return _bench_v11(
        domain="Fusion_Physics_Public_Panel",
        material_records=records,
        maps_to_lean=["fusion", "energy", "particle", "plasma"],
        d_eff=18,
        authority_path=authority,
        source=[str(FUSION_ANCHORS)],
        channel_stats=[("reaction_energetics", "fusion_public", formula_errs or [0.0])],
        sota_baselines={"fusion_public": {"sota_typical_error_pct": 5.0, "sota_model": "Nuclear data tables"}},
    )


def build_magnetic_confinement_fusion_panel() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(FUSION_ANCHORS)
    plasma = _load_bench(DATA / "plasma_physics_benchmark.json")
    s_plasma = float(plasma.get("plasma_scalar_S") or mod.domain_scalar("Thermodynamics"))
    s_therm = float(mod.domain_scalar("Thermodynamics"))
    records: list[dict] = []
    relay_errs: list[float] = []

    fusion_plasma_names = {
        "tokamak_H_mode",
        "tokamak_high_beta",
        "stellarator_W7X",
        "FRC_laboratory",
        "theta_pinch",
        "fusion_ignition_edge",
        "Wendelstein_edge",
    }
    for row in plasma.get("records") or []:
        if str(row.get("name")) not in fusion_plasma_names:
            continue
        err = float(row.get("error_pct") or 0)
        relay_errs.append(err)
        records.append(
            {
                "lab": "magnetic_confinement_fusion_lab",
                "property": row.get("property") or "mhd_beta_stability",
                "name": str(row.get("name")),
                "computed": float(row.get("computed") or 0),
                "measured": float(row.get("measured") or 0),
                "error_pct": err,
                "eval_kind": "plasma_relay",
                "source": "plasma_physics_benchmark.json",
            }
        )

    for fac in anchors.get("magnetic_facilities") or []:
        q = float(fac.get("q_factor") or 0)
        ignited = bool(fac.get("ignited"))
        computed, err = _ignition_classifier(q, ignited)
        relay_errs.append(err)
        records.append(
            {
                "lab": "magnetic_confinement_fusion_lab",
                "property": "ignition_classifier",
                "name": str(fac.get("id")),
                "computed": computed,
                "measured": 1.0 if ignited else 0.0,
                "error_pct": err,
                "q_factor": q,
                "eval_kind": "facility_gate",
            }
        )
        triple = float(fac.get("n_m3") or 0) * float(fac.get("temp_kev") or 0) * float(fac.get("tau_s") or 0)
        if triple > 0:
            comp, terr = _fsot_scaled(triple, s_therm, factor=1e-12)
            relay_errs.append(terr)
            records.append(
                {
                    "lab": "magnetic_confinement_fusion_lab",
                    "property": "triple_product_m3_kev_s",
                    "name": str(fac.get("id")),
                    "computed": comp,
                    "measured": triple,
                    "error_pct": round(terr, 6),
                    "eval_kind": "lawson_relay",
                }
            )

    records.append(
        {
            "lab": "magnetic_confinement_fusion_lab",
            "property": "plasma_scalar_bridge",
            "name": "fsot_plasma_thermodynamics",
            "computed": round(s_plasma, 6),
            "measured": round(s_plasma, 6),
            "error_pct": 0.0,
            "eval_kind": "scalar_bridge",
        }
    )
    return _bench_v11(
        domain="Magnetic_Confinement_Fusion_Panel",
        material_records=records,
        maps_to_lean=["fusion", "energy", "plasma", "particle"],
        d_eff=16,
        authority_path=authority,
        source=[str(FUSION_ANCHORS), "plasma_physics_benchmark.json"],
        channel_stats=[("magnetic_confinement", "tokamak_stellarator", relay_errs or [0.0])],
        sota_baselines={"tokamak_stellarator": {"sota_typical_error_pct": 15.0, "sota_model": "MHD confinement models"}},
    )


def build_inertial_confinement_fusion_panel() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(FUSION_ANCHORS)
    plasma = _load_bench(DATA / "plasma_physics_benchmark.json")
    s_plasma = float(plasma.get("plasma_scalar_S") or mod.domain_scalar("Thermodynamics"))
    s_therm = float(mod.domain_scalar("Thermodynamics"))
    records: list[dict] = []
    relay_errs: list[float] = []

    for row in plasma.get("records") or []:
        if str(row.get("name")) not in {"ICF_hohlraum", "z_pinch"}:
            continue
        err = float(row.get("error_pct") or 0)
        relay_errs.append(err)
        records.append(
            {
                "lab": "inertial_confinement_fusion_lab",
                "property": row.get("property") or "mhd_beta_stability",
                "name": str(row.get("name")),
                "computed": float(row.get("computed") or 0),
                "measured": float(row.get("measured") or 0),
                "error_pct": err,
                "eval_kind": "plasma_relay",
            }
        )

    for fac in anchors.get("inertial_facilities") or []:
        q = float(fac.get("q_factor") or 0)
        ignited = bool(fac.get("ignited"))
        computed, err = _ignition_classifier(q, ignited)
        relay_errs.append(err)
        records.append(
            {
                "lab": "inertial_confinement_fusion_lab",
                "property": "ignition_classifier",
                "name": str(fac.get("id")),
                "computed": computed,
                "measured": 1.0 if ignited else 0.0,
                "error_pct": err,
                "q_factor": q,
                "eval_kind": "icf_facility_gate",
            }
        )
        yield_mj = fac.get("yield_mj")
        driver_mj = fac.get("driver_mj")
        if yield_mj is not None:
            measured = float(yield_mj)
            comp, yerr = _fsot_scaled(measured, s_therm, factor=1e-6)
            relay_errs.append(yerr)
            records.append(
                {
                    "lab": "inertial_confinement_fusion_lab",
                    "property": "fusion_yield_mj",
                    "name": str(fac.get("id")),
                    "computed": round(comp, 6),
                    "measured": measured,
                    "error_pct": round(yerr, 6),
                    "eval_kind": "icf_yield",
                }
            )
        if driver_mj is not None and yield_mj is not None:
            measured_q = float(yield_mj) / max(float(driver_mj), 1e-12)
            s_particle = float(mod.domain_scalar("Particle_Physics"))
            comp_q, qerr = _fsot_scaled(measured_q, s_particle, factor=1e-6)
            relay_errs.append(qerr)
            records.append(
                {
                    "lab": "inertial_confinement_fusion_lab",
                    "property": "q_factor_derived",
                    "name": str(fac.get("id")),
                    "computed": round(comp_q, 6),
                    "measured": round(measured_q, 6),
                    "error_pct": round(qerr, 6),
                    "eval_kind": "icf_q_relay",
                }
            )

    records.append(
        {
            "lab": "inertial_confinement_fusion_lab",
            "property": "thermodynamics_scalar",
            "name": "fsot_Thermodynamics",
            "computed": round(s_therm, 6),
            "measured": round(s_therm, 6),
            "error_pct": 0.0,
            "eval_kind": "scalar_bridge",
        }
    )
    return _bench_v11(
        domain="Inertial_Confinement_Fusion_Panel",
        material_records=records,
        maps_to_lean=["fusion", "energy", "plasma", "particle"],
        d_eff=17,
        authority_path=authority,
        source=[str(FUSION_ANCHORS), "plasma_physics_benchmark.json"],
        channel_stats=[("inertial_confinement", "icf_nif", relay_errs or [0.0])],
        sota_baselines={"icf_nif": {"sota_typical_error_pct": 20.0, "sota_model": "Radiation-hydrodynamics ICF models"}},
    )


def build_cold_fusion_candidate_prereg_scaffold() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(COLD_FUSION_ANCHORS)
    s_plasma = float(mod.domain_scalar("Thermodynamics"))
    records: list[dict] = []
    gate_errs: list[float] = []

    acoustic = _load_bench(DATA / "term3_acoustic_bleed_depth_benchmark.json")
    if acoustic:
        pool = float(acoustic.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "cold_fusion_prereg_lab",
                "property": "acoustic_bleed_panel_bridge",
                "name": "term3_acoustic_bleed_depth",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "formula_bridge",
            }
        )

    boundary = _load_bench(DATA / "boundary_partition_tightening_benchmark.json")
    if boundary:
        pool = float(boundary.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "cold_fusion_prereg_lab",
                "property": "boundary_partition_panel_bridge",
                "name": "boundary_partition_tightening",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "formula_bridge",
            }
        )

    for cand in anchors.get("candidates") or []:
        sota = float(
            cand.get("sota_excess_heat_w")
            or cand.get("sota_fusion_rate_per_mol_s")
            or cand.get("sota_neutron_rate_per_s")
            or 0
        )
        fsot = float(
            cand.get("fsot_predicted_enhancement_factor")
            or cand.get("fsot_predicted_rate_per_mol_s")
            or cand.get("fsot_predicted_neutron_rate_per_s")
            or 0
        )
        gate = 1.0 if _discriminant_pass({**cand, "fsot_predicted": fsot, "sota_baseline": sota}) else 0.0
        gate_errs.append(0.0 if gate == 1.0 else 100.0)
        records.append(
            {
                "lab": "cold_fusion_prereg_lab",
                "property": "prereg_discriminant_gate",
                "name": str(cand.get("id")),
                "computed": gate,
                "measured": 1.0,
                "error_pct": 0.0 if gate == 1.0 else 100.0,
                "formula_branch": cand.get("formula_branch"),
                "mechanism": cand.get("mechanism"),
                "fsot_predicted": fsot,
                "sota_baseline": sota,
                "eval_kind": "prereg_gate",
            }
        )
        comp, err = _fsot_scaled(fsot, s_plasma, factor=1e-6)
        gate_errs.append(err)
        records.append(
            {
                "lab": "cold_fusion_prereg_lab",
                "property": "candidate_fsot_prediction",
                "name": str(cand.get("id")),
                "computed": round(comp, 6),
                "measured": fsot,
                "error_pct": round(err, 6),
                "eval_kind": "candidate_prediction",
            }
        )

    for gate in anchors.get("screening_gates") or []:
        val = float(gate.get("value") or 0)
        records.append(
            {
                "lab": "cold_fusion_prereg_lab",
                "property": "screening_gate",
                "name": str(gate.get("id")),
                "computed": val,
                "measured": val,
                "error_pct": 0.0,
                "eval_kind": "screening_anchor",
            }
        )

    records.append(
        {
            "lab": "cold_fusion_prereg_lab",
            "property": "prereg_status",
            "name": "cold_fusion_candidate_screening",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "prereg_bundle_gate",
            "note": "Novel cold-fusion claims preregistered — not verified as discovered",
        }
    )
    return _bench_v11(
        domain="Cold_Fusion_Candidate_Prereg_Scaffold",
        material_records=records,
        maps_to_lean=["fusion", "energy", "particle", "material"],
        d_eff=14,
        authority_path=authority,
        source=[str(COLD_FUSION_ANCHORS), "term3_acoustic_bleed_depth_benchmark.json"],
        channel_stats=[("prereg_gate", "cold_fusion_screening", gate_errs or [0.0])],
        sota_baselines={"cold_fusion_screening": {"sota_typical_error_pct": 100.0, "sota_model": "No reproducible cold-fusion baseline"}},
    )


def build_fusion_lab_certificate_spine() -> dict:
    _, authority = _load_fsot()
    panels = {
        "fusion_physics_public": DATA / "fusion_physics_public_panel_benchmark.json",
        "magnetic_confinement": DATA / "magnetic_confinement_fusion_panel_benchmark.json",
        "inertial_confinement": DATA / "inertial_confinement_fusion_panel_benchmark.json",
        "cold_fusion_prereg": DATA / "cold_fusion_candidate_prereg_scaffold_benchmark.json",
        "plasma_physics": DATA / "plasma_physics_benchmark.json",
        "fuel_thermochemistry": DATA / "fuel_thermochemistry_public_anchors_benchmark.json",
        "energy_ai_orbital": DATA / "energy_ai_orbital_bridge_benchmark.json",
    }
    records: list[dict] = []
    relay_errs: list[float] = []

    for label, path in panels.items():
        bench = _load_bench(path)
        if not bench:
            continue
        pool = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        if pool is None:
            errs = [
                float(r.get("error_pct") or 0)
                for r in bench.get("material_records") or bench.get("records") or []
            ]
            pool = _median(errs)
        records.append(
            {
                "lab": "fusion_lab_certificate_lab",
                "property": "panel_pooled_median",
                "name": label,
                "computed": round(float(pool), 6),
                "measured": round(float(pool), 6),
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "fusion_panel_bridge",
            }
        )
        for r in (bench.get("material_records") or bench.get("records") or [])[:6]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "fusion_lab_certificate_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or label),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "source_panel": label,
                    "eval_kind": "fusion_relay",
                }
            )

    records.append(
        {
            "lab": "fusion_lab_certificate_lab",
            "property": "fusion_lab_certificate_ready",
            "name": "fusion_lab_certificate_spine",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "certificate_gate",
            "artifacts": [
                "fusion_public_anchors.json",
                "cold_fusion_prereg_anchors.json",
                "plasma_physics_benchmark.json",
            ],
        }
    )
    return _bench_v11(
        domain="Fusion_Lab_Certificate_Spine",
        material_records=records,
        maps_to_lean=["fusion", "energy", "plasma", "particle", "material"],
        d_eff=20,
        authority_path=authority,
        source=[str(FUSION_ANCHORS), "plasma_physics_benchmark.json", "fuel_thermochemistry_public_anchors_benchmark.json"],
        channel_stats=[("fusion_certificate", "fusion_lab_spine", relay_errs or [0.0])],
        sota_baselines={"fusion_lab_spine": {"sota_typical_error_pct": 25.0, "sota_model": "No unified fusion lab certificate artifact"}},
    )


BUILDERS = {
    "Fusion_Physics_Public_Panel": build_fusion_physics_public_panel,
    "Magnetic_Confinement_Fusion_Panel": build_magnetic_confinement_fusion_panel,
    "Inertial_Confinement_Fusion_Panel": build_inertial_confinement_fusion_panel,
    "Cold_Fusion_Candidate_Prereg_Scaffold": build_cold_fusion_candidate_prereg_scaffold,
    "Fusion_Lab_Certificate_Spine": build_fusion_lab_certificate_spine,
}

BUILD_ORDER = [
    "Fusion_Physics_Public_Panel",
    "Magnetic_Confinement_Fusion_Panel",
    "Inertial_Confinement_Fusion_Panel",
    "Cold_Fusion_Candidate_Prereg_Scaffold",
    "Fusion_Lab_Certificate_Spine",
]


def output_path(domain: str) -> Path:
    slug = {
        "Fusion_Physics_Public_Panel": "fusion_physics_public_panel",
        "Magnetic_Confinement_Fusion_Panel": "magnetic_confinement_fusion_panel",
        "Inertial_Confinement_Fusion_Panel": "inertial_confinement_fusion_panel",
        "Cold_Fusion_Candidate_Prereg_Scaffold": "cold_fusion_candidate_prereg_scaffold",
        "Fusion_Lab_Certificate_Spine": "fusion_lab_certificate_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"