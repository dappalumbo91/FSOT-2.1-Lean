#!/usr/bin/env python3
"""Build data/fsot_verification_progress.yaml — where we are in the verification arc."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "fsot_verification_progress.yaml"
FORMAL = ROOT / "FSOT" / "Formal"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _median_error(doc: dict, *keys: str, default: float = 99.0) -> float:
    for key in keys:
        if key in doc and doc[key] is not None:
            return float(doc[key])
    return default


def build_progress() -> dict:
    cert = _load_json(ROOT / "data" / "certificate.json")
    registry = _load_json(ROOT / "data" / "lab_registry.json")
    cohort = _load_json(ROOT / "data" / "neuron_cohort_report.json")
    allen_verify = _load_json(ROOT / "data" / "allen_sdk_verification.json")
    domain_cov = _load_json(ROOT / "data" / "domain_coverage_report.json")
    domain_prec = _load_json(ROOT / "data" / "domain_precision_report.json")
    fic_report = _load_json(ROOT / "data" / "fic_sensitivity_report.json")
    bio_report = _load_json(ROOT / "data" / "biology_numeric_report.json")
    bio_strict = _load_json(ROOT / "data" / "biology_strict_empirical.json")
    plasma_bench = _load_json(ROOT / "data" / "plasma_physics_benchmark.json")
    immuno_bench = _load_json(ROOT / "data" / "immunology_benchmark.json")
    climate_bench = _load_json(ROOT / "data" / "climate_observed_benchmark.json")
    neuron_th = _load_json(ROOT / "data" / "neuron_cohort_train_holdout.json")
    sci_map = _load_json(ROOT / "data" / "scientific_domain_expansion_map.json")
    thesis_bench = _load_json(ROOT / "data" / "thesis_simulation_benchmark.json")
    emergent_bench = _load_json(ROOT / "data" / "emergent_domains_benchmark.json")
    mg_rules_bench = _load_json(ROOT / "data" / "math_generator_rules_benchmark.json")
    cosmo_ext_bench = _load_json(ROOT / "data" / "cosmology_extended_benchmark.json")
    particle_bench = _load_json(ROOT / "data" / "particle_physics_benchmark.json")
    higgs_bench = _load_json(ROOT / "data" / "higgs_branching_benchmark.json")
    registry_full = _load_json(ROOT / "data" / "lab_registry.json")
    higher_waves = registry_full.get("cosmology_higher_waves_lab", {})
    space_weather_bench = _load_json(ROOT / "data" / "space_weather_benchmark.json")
    pharmacology_bench = _load_json(ROOT / "data" / "pharmacology_benchmark.json")
    cryosphere_bench = _load_json(ROOT / "data" / "cryosphere_benchmark.json")
    seismology_bench = _load_json(ROOT / "data" / "seismology_benchmark.json")
    tectonics_bench = _load_json(ROOT / "data" / "tectonics_benchmark.json")
    geomagnetism_bench = _load_json(ROOT / "data" / "geomagnetism_benchmark.json")
    planetary_bench = _load_json(ROOT / "data" / "planetary_structure_benchmark.json")
    orbital_bench = _load_json(ROOT / "data" / "orbital_mechanics_benchmark.json")
    small_body_bench = _load_json(ROOT / "data" / "small_body_orbits_benchmark.json")
    magnetosphere_bench = _load_json(ROOT / "data" / "magnetosphere_benchmark.json")
    grace_cryosphere_bench = _load_json(ROOT / "data" / "grace_cryosphere_benchmark.json")
    seismology_deep_bench = _load_json(ROOT / "data" / "seismology_deep_benchmark.json")
    planetary_atmospheres_bench = _load_json(ROOT / "data" / "planetary_atmospheres_benchmark.json")
    magnetosphere_ext_bench = _load_json(ROOT / "data" / "magnetosphere_extended_benchmark.json")
    geochemistry_bench = _load_json(ROOT / "data" / "geochemistry_benchmark.json")
    oncology_bench = _load_json(ROOT / "data" / "oncology_benchmark.json")
    neuroimmunology_bench = _load_json(ROOT / "data" / "neuroimmunology_benchmark.json")
    synthetic_bio_bench = _load_json(ROOT / "data" / "synthetic_biology_benchmark.json")
    quantum_materials_bench = _load_json(ROOT / "data" / "quantum_materials_benchmark.json")
    multi_hero_bench = _load_json(ROOT / "data" / "multi_hero_benchmark.json")
    linguistics_formal_bench = _load_json(ROOT / "data" / "linguistics_formal_benchmark.json")
    mathematics_bench = _load_json(ROOT / "data" / "mathematics_computational_benchmark.json")
    materials_eng_bench = _load_json(ROOT / "data" / "materials_engineering_benchmark.json")
    computational_reasoning_bench = _load_json(ROOT / "data" / "computational_reasoning_benchmark.json")
    mg_rules_eval_bench = _load_json(ROOT / "data" / "math_generator_rules_eval_benchmark.json")
    trinary_portable_bench = _load_json(ROOT / "data" / "trinary_os_portable_benchmark.json")
    materials_species_bench = _load_json(ROOT / "data" / "materials_species_bridge_benchmark.json")
    igem_syn_bio_bench = _load_json(ROOT / "data" / "igem_synthetic_biology_benchmark.json")
    mg_bench_formula_bench = _load_json(ROOT / "data" / "math_generator_benchmark_formula_eval_benchmark.json")
    trinary_isa_bench = _load_json(ROOT / "data" / "trinary_os_isa_rebuild_benchmark.json")
    igem_live_fasta_bench = _load_json(ROOT / "data" / "igem_live_fasta_benchmark.json")
    mg_airfoil_rmse_bench = _load_json(ROOT / "data" / "math_generator_airfoil_rmse_benchmark.json")
    trinary_round_trip_bench = _load_json(ROOT / "data" / "trinary_os_round_trip_benchmark.json")
    tokenization_smoke_bench = _load_json(ROOT / "data" / "tokenization_smoke_benchmark.json")
    trinary_hw_motif_bench = _load_json(ROOT / "data" / "trinary_hardware_motif_benchmark.json")
    intrinsic_llm_bench = _load_json(ROOT / "data" / "intrinsic_llm_validators_benchmark.json")
    biological_cuda_physarum_bench = _load_json(ROOT / "data" / "biological_cuda_physarum_benchmark.json")
    arxiv_primitives_v14_bench = _load_json(ROOT / "data" / "arxiv_primitives_v14_benchmark.json")
    formula_corpus_cnc_bench = _load_json(ROOT / "data" / "formula_corpus_cnc_benchmark.json")
    binary_decoder_rendlesham_bench = _load_json(ROOT / "data" / "binary_decoder_rendlesham_benchmark.json")
    certified_agent_qwen_bench = _load_json(ROOT / "data" / "certified_agent_qwen_benchmark.json")
    omni_theory_genesis_bench = _load_json(ROOT / "data" / "omni_theory_genesis_benchmark.json")
    fsot_aggregate_unified_db_bench = _load_json(ROOT / "data" / "fsot_aggregate_unified_db_benchmark.json")
    prediction_rederivation_bench = _load_json(ROOT / "data" / "prediction_rederivation_benchmark.json")
    vl_distill_atlas_bench = _load_json(ROOT / "data" / "vl_distill_atlas_benchmark.json")
    rust_lean_bridge_bench = _load_json(ROOT / "data" / "rust_lean_bridge_benchmark.json")
    bibliography_lean_corpus_bench = _load_json(ROOT / "data" / "bibliography_lean_corpus_benchmark.json")
    vendor_audit = _load_json(ROOT / "data" / "portable_vendor_coverage_audit.json")

    proved = cert.get("proved_claims")
    proved_n = len(proved) if isinstance(proved, list) else proved

    lean_modules = sorted(p.stem for p in FORMAL.glob("*.lean"))
    syn = registry.get("experiment_synthesis", {})
    strata = cohort.get("cohort_strata", {})

    tiers = [
        {
            "tier": 1,
            "name": "Core scalar + domains",
            "status": "complete",
            "artifacts": ["FSOT.Formal.Domains", "FSOT.Formal.Bounds", "FSOT.Formal.Theorems"],
        },
        {
            "tier": 2,
            "name": "Lab ingest (SMILES, NeuroLab, cosmology, …)",
            "status": "complete",
            "artifacts": [m for m in lean_modules if m.endswith("Priors") or m in ("CosmologyLab", "PhotonicForge")],
        },
        {
            "tier": 7,
            "name": "Experiment synthesis (neuron, Aether, magic circle, LLM inventory)",
            "status": "complete",
            "metrics": {
                "hero_fi_mean_rel_err": syn.get("neuron_hybrid_lab", {}).get("mean_rel_err"),
                "aether_distill_rows": syn.get("aether_prime_lab", {}).get("distill_row_count"),
                "llm_folders": syn.get("llm_experiments_lab", {}).get("project_folder_count"),
            },
        },
        {
            "tier": "7b",
            "name": "Neuron cohort + canonical scalar bridge",
            "status": "complete",
            "metrics": {
                "cohort_cells": cohort.get("cohort_fi_proxy", {}).get("cell_count"),
                "canonical_bridge_delta": (cohort.get("canonical_scalar_bridge") or {}).get(
                    "canonical_vs_certified_delta"
                ),
                "allensdk_verified": allen_verify.get("allensdk_installed"),
            },
        },
        {
            "tier": 8,
            "name": "Allen per-class strata + held-out cohort",
            "status": "complete" if strata.get("strata") else "pending",
            "metrics": {
                "held_out_cells": (strata.get("held_out_fi_proxy") or {}).get("cell_count"),
                "strata_count": len(strata.get("strata") or {}),
            },
        },
        {
            "tier": 9,
            "name": "35-domain NeuroLab coverage (Lean + empirical labs)",
            "status": "complete"
            if domain_cov.get("domain_count") == 35
            and domain_cov.get("domains_with_empirical_data") == 35
            else "pending",
            "metrics": {
                "domain_count": domain_cov.get("domain_count"),
                "empirical_domains": domain_cov.get("domains_with_empirical_data"),
                "total_empirical_records": domain_cov.get("total_empirical_records"),
                "lean_override_aligned": f"{domain_cov.get('lean_param_aligned_count')}/{domain_cov.get('lean_mapped_count')}",
                "negative_scalar_domains": len(domain_cov.get("negative_scalar_domains") or []),
            },
            "artifacts": ["FSOT.Formal.DomainCoveragePriors", "data/fsot_35_domain_registry.yaml"],
        },
        {
            "tier": 10,
            "name": "Per-record numeric precision (2%/5% bands + gap diagnostics)",
            "status": "complete"
            if domain_prec.get("domains_with_numeric_precision", 0) >= 25
            else "pending",
            "metrics": {
                "numeric_precision_domains": domain_prec.get("domains_with_numeric_precision"),
                "target_band_2pct": domain_prec.get("domains_target_band_2pct"),
                "tolerable_band_5pct": domain_prec.get("domains_tolerable_band_5pct"),
                "huge_gap_domains": domain_prec.get("domains_huge_gap"),
                "sign_mismatch_domains": domain_prec.get("domains_sign_mismatch"),
            },
            "artifacts": ["FSOT.Formal.DomainPrecisionPriors", "data/domain_precision_report.json"],
        },
        {
            "tier": 11,
            "name": "Intelligence_Compression (FIC sweep + fertile window)",
            "status": "complete"
            if fic_report.get("sweep_row_count", 0) >= 100
            and fic_report.get("fertile_count", 0) >= 5
            else "pending",
            "metrics": {
                "sweep_rows": fic_report.get("sweep_row_count"),
                "fertile_rows": fic_report.get("fertile_count"),
                "optimal_S_final": fic_report.get("optimal_S_final"),
                "best_intelligence_score": fic_report.get("best_intelligence_score"),
            },
            "artifacts": [
                "FSOT.Formal.IntelligenceCompressionPriors",
                "data/fic_sensitivity_sweep.csv",
                "data/intelligence_compression_manifest.yaml",
            ],
        },
        {
            "tier": "11b",
            "name": "Biology numeric depth (Soul 234k + DB bio subset)",
            "status": "complete"
            if bio_report.get("soul_manifest", {}).get("records_processed", 0) >= 200000
            else "pending",
            "metrics": {
                "soul_records": bio_report.get("soul_manifest", {}).get("records_processed"),
                "biology_corpus_estimated": bio_report.get("soul_biology_sample", {}).get(
                    "biology_records_estimated"
                ),
                "db_bio_numeric": bio_report.get("unified_db_biology", {}).get(
                    "verification_numeric"
                ),
            },
            "artifacts": ["data/biology_numeric_report.json", "data/cellular_manifest.yaml"],
        },
        {
            "tier": 12,
            "name": "Extension domains #37-39 (Plasma, Immunology, Climate)",
            "status": "complete"
            if plasma_bench.get("record_count", 0) >= 5
            and immuno_bench.get("record_count", 0) >= 5
            and climate_bench.get("month_count", 0) >= 5
            else "pending",
            "metrics": {
                "plasma_records": plasma_bench.get("record_count"),
                "immunology_records": immuno_bench.get("record_count"),
                "climate_months": climate_bench.get("month_count"),
                "biology_strict_records": bio_strict.get("record_count"),
            },
            "artifacts": [
                "FSOT.Formal.PlasmaPhysicsPriors",
                "FSOT.Formal.ImmunologyPriors",
                "FSOT.Formal.ClimateSciencePriors",
                "data/extension_domains_manifest.yaml",
            ],
        },
        {
            "tier": 13,
            "name": "Biology strict-empirical NCBI bridge (mt operons → Lean)",
            "status": "complete"
            if bio_strict.get("strict_record_count", 0) >= 10
            and _median_error(bio_strict, "strict_median_error_pct", "median_error_pct") <= 2.0
            else "pending",
            "metrics": {
                "strict_records": bio_strict.get("strict_record_count"),
                "operon_records": bio_strict.get("operon_records"),
                "strict_median_error_pct": _median_error(
                    bio_strict, "strict_median_error_pct", "median_error_pct", default=0.0
                )
                if "strict_median_error_pct" in bio_strict or "median_error_pct" in bio_strict
                else None,
                "ncbi_reference": bio_strict.get("ncbi_reference"),
                "soul_biology_rows": bio_strict.get("soul_biology_rows"),
            },
            "artifacts": [
                "FSOT.Formal.BiologyStrictEmpiricalPriors",
                "data/biology_strict_manifest.yaml",
                "data/biology_strict_empirical.json",
            ],
        },
        {
            "tier": 14,
            "name": "Climate scale cohort + neuron train/holdout + scientific domain map",
            "status": "complete"
            if (neuron_th.get("gates") or {}).get("all_pass")
            and (climate_bench.get("cohort") or {}).get("holdout", {}).get("record_count", 0) >= 1
            and sci_map.get("summary", {}).get("total_scientific_domains_covered", 0) >= 39
            else "pending",
            "metrics": {
                "climate_total_months": climate_bench.get("record_count"),
                "climate_holdout_months": (climate_bench.get("cohort") or {})
                .get("holdout", {})
                .get("record_count"),
                "climate_holdout_median_err": (climate_bench.get("cohort") or {})
                .get("holdout", {})
                .get("median_error_pct"),
                "neuron_train_cells": (neuron_th.get("train") or {}).get("cell_count"),
                "neuron_holdout_cells": (neuron_th.get("holdout") or {}).get("cell_count"),
                "neuron_holdout_gates_pass": (neuron_th.get("gates") or {}).get("all_pass"),
                "scientific_domains_covered": sci_map.get("summary", {}).get(
                    "total_scientific_domains_covered"
                ),
                "expansion_candidates": len(sci_map.get("expansion_candidates") or []),
            },
            "artifacts": [
                "data/climate_ncei_manifest.yaml",
                "data/neuron_cohort_train_holdout.json",
                "data/scientific_domain_expansion_map.json",
                "FSOT.Formal.NeuronCohortTrainHoldoutPriors",
            ],
        },
        {
            "tier": 15,
            "name": "Wave A core theory grounding (thesis sim + emergent MC + math rules)",
            "status": "complete"
            if thesis_bench.get("wave_target_count", 0) >= 90
            and thesis_bench.get("intrinsic_screen_count", 0) >= 50
            and emergent_bench.get("emergent_domain_count", 0) >= 29
            and emergent_bench.get("observed_domain_count", 0) >= 25
            and mg_rules_bench.get("rule_corpus_count", 0) >= 55
            and mg_rules_bench.get("total_rule_count", 0) >= 1000
            else "pending",
            "metrics": {
                "thesis_wave_targets": thesis_bench.get("wave_target_count"),
                "thesis_intrinsic_screens": thesis_bench.get("intrinsic_screen_count"),
                "thesis_observables": thesis_bench.get("observable_count"),
                "emergent_domains": emergent_bench.get("emergent_domain_count"),
                "emergent_observed": emergent_bench.get("observed_domain_count"),
                "emergence_health": emergent_bench.get("final_emergence_health"),
                "math_rule_corpora": mg_rules_bench.get("rule_corpus_count"),
                "math_rule_observables": mg_rules_bench.get("total_rule_count"),
            },
            "artifacts": [
                "data/thesis_simulation_manifest.yaml",
                "data/emergent_domains_manifest.yaml",
                "data/math_generator_rules_manifest.yaml",
                "FSOT.Formal.ThesisSimulationPriors",
                "FSOT.Formal.EmergentDomainPriors",
                "FSOT.Formal.MathGeneratorPriors",
            ],
        },
        {
            "tier": 16,
            "name": "Wave B cosmology + particle physics extended domains",
            "status": "complete"
            if cosmo_ext_bench.get("observable_count", 0) >= 50
            and cosmo_ext_bench.get("skeleton_derivation_count", 0) >= 20
            and particle_bench.get("observable_count", 0) >= 70
            and particle_bench.get("wave4_count", 0) >= 16
            and _median_error(particle_bench, "median_error_pct", default=99.0) <= 5.0
            else "pending",
            "metrics": {
                "cosmology_skeleton_derivations": cosmo_ext_bench.get("skeleton_derivation_count"),
                "cosmology_lambda_cdm_bundle": cosmo_ext_bench.get("lambda_cdm_count"),
                "cosmology_extended_observables": cosmo_ext_bench.get("observable_count"),
                "particle_smiles_records": particle_bench.get("smiles_particle_count"),
                "particle_wave4_observables": particle_bench.get("wave4_count"),
                "particle_math_physics_rules": particle_bench.get("math_physics_rule_count"),
                "particle_extended_observables": particle_bench.get("observable_count"),
                "particle_median_error_pct": _median_error(particle_bench, "median_error_pct", default=0.0),
            },
            "artifacts": [
                "data/cosmology_extended_manifest.yaml",
                "data/particle_physics_manifest.yaml",
                "FSOT.Formal.CosmologyExtendedPriors",
                "FSOT.Formal.ParticlePhysicsPriors",
            ],
        },
        {
            "tier": 17,
            "name": "Cosmo/particle deepen (astro thicken + Higgs + SWPC + waves 5–10)",
            "status": "complete"
            if higher_waves.get("observable_count", 0) >= 140
            and higgs_bench.get("observable_count", 0) >= 8
            and space_weather_bench.get("kp_record_count", 0) >= 30
            and next(
                (
                    d.get("empirical_records", 0)
                    for d in (domain_cov.get("domains") or [])
                    if d.get("neurolab_domain") == "Astrophysics"
                ),
                0,
            )
            >= 50
            and next(
                (
                    d.get("empirical_records", 0)
                    for d in (domain_cov.get("domains") or [])
                    if d.get("neurolab_domain") == "Particle_Astrophysics"
                ),
                0,
            )
            >= 50
            else "pending",
            "metrics": {
                "cosmology_higher_waves": higher_waves.get("observable_count"),
                "higgs_branching_observables": higgs_bench.get("observable_count"),
                "space_weather_kp_records": space_weather_bench.get("kp_record_count"),
                "astrophysics_empirical_records": next(
                    (
                        d.get("empirical_records")
                        for d in (domain_cov.get("domains") or [])
                        if d.get("neurolab_domain") == "Astrophysics"
                    ),
                    None,
                ),
                "particle_astrophysics_empirical_records": next(
                    (
                        d.get("empirical_records")
                        for d in (domain_cov.get("domains") or [])
                        if d.get("neurolab_domain") == "Particle_Astrophysics"
                    ),
                    None,
                ),
            },
            "artifacts": [
                "data/cosmology_higher_waves_manifest.yaml",
                "data/higgs_branching_manifest.yaml",
                "data/space_weather_manifest.yaml",
                "FSOT.Formal.CosmologyHigherWavesPriors",
                "FSOT.Formal.HiggsBranchingPriors",
                "FSOT.Formal.SpaceWeatherPriors",
            ],
        },
        {
            "tier": 18,
            "name": "Per-wave cosmology + historical SWPC + plasma crosswalk",
            "status": "complete"
            if all(
                (registry_full.get(f"cosmology_wave{n}_lab") or {}).get("observable_count", 0) >= 5
                for n in (5, 6, 7, 8, 9, 10)
            )
            and space_weather_bench.get("kp_record_count", 0) >= 500
            else "pending",
            "metrics": {
                "cosmology_wave5_observables": (registry_full.get("cosmology_wave5_lab") or {}).get("observable_count"),
                "cosmology_wave8_observables": (registry_full.get("cosmology_wave8_lab") or {}).get("observable_count"),
                "space_weather_kp_records": space_weather_bench.get("kp_record_count"),
                "plasma_crosswalk_labs": ["plasma_physics_lab", "space_weather_lab"],
            },
            "artifacts": [
                "data/cosmology_per_wave_manifest.yaml",
                "data/space_weather_manifest.yaml",
                "FSOT.Formal.CosmologyWave5Priors",
                "FSOT.Formal.CosmologyWave10Priors",
                "FSOT.Formal.SpaceWeatherPriors",
            ],
        },
        {
            "tier": 19,
            "name": "GFZ 2010–2024 + Wave4 Priors + USGS hydrology",
            "status": "complete"
            if (registry_full.get("cosmology_wave4_lab") or {}).get("observable_count", 0) >= 16
            and space_weather_bench.get("kp_record_count", 0) >= 35000
            and _load_json(ROOT / "data" / "hydrology_benchmark.json").get("record_count", 0) >= 120
            else "pending",
            "metrics": {
                "cosmology_wave4_observables": (registry_full.get("cosmology_wave4_lab") or {}).get("observable_count"),
                "space_weather_kp_records": space_weather_bench.get("kp_record_count"),
                "hydrology_month_records": _load_json(ROOT / "data" / "hydrology_benchmark.json").get("record_count"),
                "gfz_year_range": [2010, 2024],
            },
            "artifacts": [
                "data/space_weather_manifest.yaml",
                "data/hydrology_usgs_manifest.yaml",
                "FSOT.Formal.CosmologyWave4Priors",
                "FSOT.Formal.HydrologyPriors",
            ],
        },
        {
            "tier": 20,
            "name": "GFZ 1932 arc + Priors-only Wave4 + ChEMBL + Cryosphere + ToE crosswalk",
            "status": "complete"
            if space_weather_bench.get("kp_record_count", 0) >= 250000
            and pharmacology_bench.get("observable_count", 0) >= 40
            and cryosphere_bench.get("observable_count", 0) >= 48
            and (ROOT / "data" / "fsot_theory_crosswalk.yaml").exists()
            and (ROOT / "data" / "FSOT_VERIFIED_SCOPE.yaml").exists()
            else "pending",
            "metrics": {
                "space_weather_kp_records": space_weather_bench.get("kp_record_count"),
                "pharmacology_observables": pharmacology_bench.get("observable_count"),
                "cryosphere_month_records": cryosphere_bench.get("observable_count"),
                "cryosphere_match_rate": cryosphere_bench.get("stability_match_rate"),
                "gfz_year_range": [1932, 2024],
                "theory_crosswalk_domains": [
                    "Aerospace_Engineering",
                    "Computer_Science",
                    "Hearing_Science",
                    "Pharmacology",
                    "Cryosphere",
                ],
            },
            "artifacts": [
                "data/space_weather_manifest.yaml",
                "data/pharmacology_chembl_manifest.yaml",
                "data/cryosphere_manifest.yaml",
                "data/fsot_theory_crosswalk.yaml",
                "data/FSOT_VERIFIED_SCOPE.yaml",
                "FSOT.Formal.CosmologyWave4Priors",
                "FSOT.Formal.PharmacologyPriors",
                "FSOT.Formal.CryospherePriors",
            ],
        },
        {
            "tier": 21,
            "name": "Geophysics & planetary mechanics (seismology, tectonics, EM, orbits)",
            "status": "complete"
            if seismology_bench.get("observable_count", 0) >= 80
            and tectonics_bench.get("observable_count", 0) >= 80
            and geomagnetism_bench.get("observable_count", 0) >= 40
            and planetary_bench.get("observable_count", 0) >= 6
            and orbital_bench.get("observable_count", 0) >= 6
            else "pending",
            "metrics": {
                "seismology_events": seismology_bench.get("observable_count"),
                "seismology_match_rate": seismology_bench.get("stability_match_rate"),
                "tectonics_events": tectonics_bench.get("observable_count"),
                "tectonics_boundary_features": tectonics_bench.get("plate_boundary_features"),
                "geomagnetism_observables": geomagnetism_bench.get("observable_count"),
                "planetary_structure_bodies": planetary_bench.get("observable_count"),
                "orbital_mechanics_bodies": orbital_bench.get("observable_count"),
                "orbital_median_error_pct": orbital_bench.get("median_error_pct"),
            },
            "artifacts": [
                "data/seismology_usgs_manifest.yaml",
                "data/tectonics_manifest.yaml",
                "data/geomagnetism_manifest.yaml",
                "data/planetary_structure_manifest.yaml",
                "data/orbital_mechanics_manifest.yaml",
                "FSOT.Formal.SeismologyPriors",
                "FSOT.Formal.TectonicsPriors",
                "FSOT.Formal.GeomagnetismPriors",
                "FSOT.Formal.PlanetaryStructurePriors",
                "FSOT.Formal.OrbitalMechanicsPriors",
            ],
        },
        {
            "tier": 22,
            "name": "Small-body orbits + magnetosphere coupling (Dst×Kp×magnetic-string)",
            "status": "complete"
            if small_body_bench.get("observable_count", 0) >= 4
            and magnetosphere_bench.get("observable_count", 0) >= 40
            and magnetosphere_bench.get("stability_match_rate", 0) >= 0.5
            else "pending",
            "metrics": {
                "small_body_orbit_count": small_body_bench.get("observable_count"),
                "small_body_median_error_pct": small_body_bench.get("median_error_pct"),
                "magnetosphere_observables": magnetosphere_bench.get("observable_count"),
                "magnetosphere_match_rate": magnetosphere_bench.get("stability_match_rate"),
                "magnetosphere_kp_resolution": magnetosphere_bench.get("kp_primary_resolution"),
                "magnetosphere_resolution_comparison": magnetosphere_bench.get("resolution_comparison"),
                "magnetosphere_channel_decomposition": magnetosphere_bench.get("channel_decomposition"),
            },
            "artifacts": [
                "data/small_body_orbits_manifest.yaml",
                "data/magnetosphere_manifest.yaml",
                "FSOT.Formal.SmallBodyOrbitsPriors",
                "FSOT.Formal.MagnetospherePriors",
            ],
        },
        {
            "tier": 23,
            "name": "GRACE cryosphere + seismology deep + planetary atmospheres",
            "status": "complete"
            if grace_cryosphere_bench.get("observable_count", 0) >= 120
            and grace_cryosphere_bench.get("stability_match_rate", 0) >= 0.5
            and seismology_deep_bench.get("observable_count", 0) >= 80
            and seismology_deep_bench.get("stability_match_rate", 0) >= 0.5
            and planetary_atmospheres_bench.get("observable_count", 0) >= 4
            and _median_error(planetary_atmospheres_bench, "median_error_pct") <= 5.0
            else "pending",
            "metrics": {
                "grace_cryosphere_months": grace_cryosphere_bench.get("observable_count"),
                "grace_cryosphere_match_rate": grace_cryosphere_bench.get("stability_match_rate"),
                "seismology_deep_observables": seismology_deep_bench.get("observable_count"),
                "seismology_deep_match_rate": seismology_deep_bench.get("stability_match_rate"),
                "seismology_deep_holdout_match_rate": seismology_deep_bench.get("holdout_match_rate"),
                "planetary_atmospheres_observables": planetary_atmospheres_bench.get("observable_count"),
                "planetary_atmospheres_median_error_pct": planetary_atmospheres_bench.get("median_error_pct"),
            },
            "artifacts": [
                "data/grace_cryosphere_manifest.yaml",
                "data/seismology_deep_manifest.yaml",
                "data/planetary_atmospheres_manifest.yaml",
                "FSOT.Formal.GraceCryospherePriors",
                "FSOT.Formal.SeismologyDeepPriors",
                "FSOT.Formal.PlanetaryAtmospheresPriors",
            ],
        },
        {
            "tier": 24,
            "name": "Magnetosphere timeline resolution (hourly Kp + channel decomposition)",
            "status": "complete"
            if magnetosphere_bench.get("benchmark_version") == "1.1"
            and magnetosphere_bench.get("kp_primary_resolution") == "interpolated_1h"
            and magnetosphere_bench.get("stability_match_rate", 0) >= 0.98
            and magnetosphere_bench.get("channel_decomposition", {}).get("coupled_physical", {}).get(
                "match_rate", 0
            )
            >= 0.99
            else "pending",
            "metrics": {
                "magnetosphere_primary_resolution": magnetosphere_bench.get("kp_primary_resolution"),
                "magnetosphere_match_rate": magnetosphere_bench.get("stability_match_rate"),
                "resolution_comparison": magnetosphere_bench.get("resolution_comparison"),
                "channel_decomposition": magnetosphere_bench.get("channel_decomposition"),
                "overlap_dst_hours": (magnetosphere_bench.get("overlap_window") or {}).get("dst_hour_count"),
            },
            "artifacts": [
                "data/magnetosphere_manifest.yaml",
                "scripts/magnetosphere_timeline.py",
                "FSOT.Formal.MagnetospherePriors",
            ],
        },
        {
            "tier": 25,
            "name": "Magnetosphere extended (historical Dst 120k+ hrs, RTSW Bz, G-scale holdout)",
            "status": "complete"
            if (magnetosphere_ext_bench.get("historical_coupled") or {}).get("observable_count", 0) >= 10000
            and (magnetosphere_ext_bench.get("historical_coupled") or {}).get("stability_match_rate", 0) >= 0.95
            and (magnetosphere_ext_bench.get("storm_holdout") or {}).get("observable_count", 0) >= 50
            and (magnetosphere_ext_bench.get("storm_holdout") or {}).get("stability_match_rate", 0) >= 0.5
            and (magnetosphere_ext_bench.get("solar_wind_bz") or {}).get("observable_count", 0) >= 100
            else "pending",
            "metrics": {
                "historical_coupled_hours": (magnetosphere_ext_bench.get("historical_coupled") or {}).get(
                    "observable_count"
                ),
                "historical_coupled_match_rate": (magnetosphere_ext_bench.get("historical_coupled") or {}).get(
                    "stability_match_rate"
                ),
                "storm_holdout_hours": (magnetosphere_ext_bench.get("storm_holdout") or {}).get("observable_count"),
                "storm_holdout_match_rate": (magnetosphere_ext_bench.get("storm_holdout") or {}).get(
                    "stability_match_rate"
                ),
                "quiet_baseline_match_rate": (magnetosphere_ext_bench.get("storm_holdout") or {}).get(
                    "quiet_baseline_match_rate"
                ),
                "solar_wind_bz_records": (magnetosphere_ext_bench.get("solar_wind_bz") or {}).get("observable_count"),
                "solar_wind_bz_match_rate": (magnetosphere_ext_bench.get("solar_wind_bz") or {}).get(
                    "stability_match_rate"
                ),
            },
            "artifacts": [
                "data/kyoto_dst_manifest.yaml",
                "data/magnetosphere_extended_manifest.yaml",
                "data/solar_wind_rtsw_manifest.yaml",
                "FSOT.Formal.MagnetosphereExtendedPriors",
            ],
        },
        {
            "tier": 26,
            "name": "Thin-domain thicken + Geochemistry/Oncology/Neuroimmunology",
            "status": "complete"
            if planetary_bench.get("observable_count", 0) >= 12
            and small_body_bench.get("observable_count", 0) >= 10
            and plasma_bench.get("record_count", 0) >= 15
            and geochemistry_bench.get("record_count", 0) >= 50
            and oncology_bench.get("record_count", 0) >= 20
            and neuroimmunology_bench.get("record_count", 0) >= 20
            else "pending",
            "metrics": {
                "planetary_structure_bodies": planetary_bench.get("observable_count"),
                "orbital_mechanics_bodies": orbital_bench.get("observable_count"),
                "small_body_orbits_bodies": small_body_bench.get("observable_count"),
                "plasma_physics_cases": plasma_bench.get("record_count"),
                "geochemistry_records": geochemistry_bench.get("record_count"),
                "geochemistry_median_error_pct": geochemistry_bench.get("median_error_pct"),
                "oncology_records": oncology_bench.get("record_count"),
                "oncology_median_error_pct": oncology_bench.get("median_error_pct"),
                "neuroimmunology_records": neuroimmunology_bench.get("record_count"),
                "neuroimmunology_median_error_pct": neuroimmunology_bench.get("median_error_pct"),
            },
            "artifacts": [
                "data/geochemistry_manifest.yaml",
                "data/oncology_manifest.yaml",
                "data/neuroimmunology_manifest.yaml",
                "FSOT.Formal.GeochemistryPriors",
                "FSOT.Formal.OncologyPriors",
                "FSOT.Formal.NeuroimmunologyPriors",
            ],
        },
        {
            "tier": 27,
            "name": "Synthetic Biology/Quantum Materials + multi-hero + climate scale-up",
            "status": "complete"
            if synthetic_bio_bench.get("record_count", 0) >= 20
            and quantum_materials_bench.get("record_count", 0) >= 50
            and multi_hero_bench.get("record_count", 0) >= 12
            and climate_bench.get("station_count", 0) >= 30
            and (climate_bench.get("cohort") or {}).get("holdout", {}).get("record_count", 0) >= 200
            else "pending",
            "metrics": {
                "synthetic_biology_records": synthetic_bio_bench.get("record_count"),
                "quantum_materials_records": quantum_materials_bench.get("record_count"),
                "multi_hero_records": multi_hero_bench.get("record_count"),
                "multi_hero_median_fi_proxy_pct": multi_hero_bench.get("median_fi_proxy_rel_err_pct"),
                "climate_station_count": climate_bench.get("station_count"),
                "climate_record_count": climate_bench.get("record_count"),
                "climate_holdout_records": (climate_bench.get("cohort") or {}).get("holdout", {}).get("record_count"),
                "climate_holdout_median_error_pct": (climate_bench.get("cohort") or {})
                .get("holdout", {})
                .get("median_error_pct"),
            },
            "artifacts": [
                "data/synthetic_biology_manifest.yaml",
                "data/quantum_materials_manifest.yaml",
                "data/multi_hero_manifest.yaml",
                "data/climate_ncei_manifest.yaml",
                "FSOT.Formal.SyntheticBiologyPriors",
                "FSOT.Formal.QuantumMaterialsPriors",
                "FSOT.Formal.NeuronMultiHeroPriors",
            ],
        },
        {
            "tier": 28,
            "name": "Portable verification — vendor bundle + clone-and-verify",
            "status": "complete",
            "artifacts": [
                "vendor/fsot_compute.py",
                "CONTRIBUTING.md",
                "data/external_data_manifest.yaml",
                "scripts/fsot_paths.py",
            ],
        },
        {
            "tier": 29,
            "name": "Practical application wave — linguistics, math, materials engineering, reasoning",
            "status": "complete"
            if linguistics_formal_bench.get("record_count", 0) >= 10
            and mathematics_bench.get("record_count", 0) >= 15
            and materials_eng_bench.get("record_count", 0) >= 50
            and computational_reasoning_bench.get("record_count", 0) >= 100
            else "pending",
            "metrics": {
                "linguistics_formal_records": linguistics_formal_bench.get("record_count"),
                "mathematics_computational_records": mathematics_bench.get("record_count"),
                "materials_engineering_records": materials_eng_bench.get("record_count"),
                "computational_reasoning_records": computational_reasoning_bench.get("record_count"),
                "computational_reasoning_median_error_pct": computational_reasoning_bench.get(
                    "median_error_pct"
                ),
            },
            "artifacts": [
                "data/linguistics_formal_manifest.yaml",
                "data/mathematics_computational_manifest.yaml",
                "data/materials_engineering_manifest.yaml",
                "data/computational_reasoning_manifest.yaml",
                "FSOT.Formal.LinguisticsFormalPriors",
                "FSOT.Formal.MathematicsComputationalPriors",
                "FSOT.Formal.MaterialsEngineeringPriors",
                "FSOT.Formal.ComputationalReasoningPriors",
            ],
        },
        {
            "tier": 30,
            "name": "Portable bridges — math rules eval, trinary OS, materials↔species",
            "status": "complete"
            if mg_rules_eval_bench.get("record_count", 0) >= 1500
            and mg_rules_eval_bench.get("schema_fail_count", 99) == 0
            and trinary_portable_bench.get("oracle_count", 0) >= 3
            and trinary_portable_bench.get("median_error_pct", 99) == 0
            and materials_species_bench.get("record_count", 0) >= 20
            else "pending",
            "metrics": {
                "math_generator_rules_eval_records": mg_rules_eval_bench.get("record_count"),
                "math_generator_rules_eval_median_error_pct": mg_rules_eval_bench.get("median_error_pct"),
                "math_generator_rules_schema_fail_count": mg_rules_eval_bench.get("schema_fail_count"),
                "trinary_os_portable_records": trinary_portable_bench.get("record_count"),
                "trinary_os_portable_oracle_count": trinary_portable_bench.get("oracle_count"),
                "materials_species_bridge_records": materials_species_bench.get("record_count"),
                "materials_species_bridge_metals": materials_species_bench.get("overlap_metal_count"),
                "materials_species_bridge_median_error_pct": materials_species_bench.get("median_error_pct"),
            },
            "artifacts": [
                "data/math_generator_rules_eval_manifest.yaml",
                "data/trinary_os_portable_manifest.yaml",
                "data/materials_species_bridge_manifest.yaml",
                "vendor/trinary_os/target",
                "vendor/species/fsot_species_catalog.json",
                "FSOT.Formal.MathGeneratorRulesEvalPriors",
                "FSOT.Formal.TrinaryOSPortablePriors",
                "FSOT.Formal.MaterialsSpeciesBridgePriors",
            ],
        },
        {
            "tier": 31,
            "name": "Strict bridges — iGEM synbio, benchmark_formula eval, trinary ISA rebuild",
            "status": "complete"
            if igem_syn_bio_bench.get("record_count", 0) >= 50
            and mg_bench_formula_bench.get("record_count", 0) >= 3
            and mg_bench_formula_bench.get("median_error_pct", 99) <= 1.0
            and trinary_isa_bench.get("opcode_count", 0) >= 27
            and trinary_isa_bench.get("median_error_pct", 99) == 0
            else "pending",
            "metrics": {
                "igem_synthetic_biology_records": igem_syn_bio_bench.get("record_count"),
                "igem_synthetic_biology_parts": igem_syn_bio_bench.get("part_count"),
                "math_generator_benchmark_formula_records": mg_bench_formula_bench.get("record_count"),
                "math_generator_benchmark_formula_median_error_pct": mg_bench_formula_bench.get("median_error_pct"),
                "trinary_os_isa_rebuild_records": trinary_isa_bench.get("record_count"),
                "trinary_os_isa_opcode_count": trinary_isa_bench.get("opcode_count"),
            },
            "artifacts": [
                "data/igem_synthetic_biology_manifest.yaml",
                "data/math_generator_benchmark_formula_eval_manifest.yaml",
                "data/trinary_os_isa_rebuild_manifest.yaml",
                "vendor/igem/igem_parts_registry.json",
                "vendor/math_generator/benchmark_reports",
                "vendor/trinary_os/isa/fsotb_opcode_registry.json",
                "FSOT.Formal.IGEMSyntheticBiologyPriors",
                "FSOT.Formal.MathGeneratorBenchmarkFormulaEvalPriors",
                "FSOT.Formal.TrinaryOSISARebuildPriors",
            ],
        },
        {
            "tier": 32,
            "name": "Live ingest — iGEM FASTA, airfoil RMSE, trinary round-trip",
            "status": "complete"
            if igem_live_fasta_bench.get("record_count", 0) >= 40
            and igem_live_fasta_bench.get("median_error_pct", 99) <= 1.0
            and mg_airfoil_rmse_bench.get("record_count", 0) >= 5
            and mg_airfoil_rmse_bench.get("median_error_pct", 99) <= 1.0
            and trinary_round_trip_bench.get("record_count", 0) >= 20
            and trinary_round_trip_bench.get("median_error_pct", 99) == 0
            else "pending",
            "metrics": {
                "igem_live_fasta_records": igem_live_fasta_bench.get("record_count"),
                "igem_live_fasta_parts": igem_live_fasta_bench.get("part_count"),
                "math_generator_airfoil_rmse_records": mg_airfoil_rmse_bench.get("record_count"),
                "math_generator_airfoil_rmse_median_error_pct": mg_airfoil_rmse_bench.get("median_error_pct"),
                "trinary_os_round_trip_records": trinary_round_trip_bench.get("record_count"),
                "trinary_os_round_trip_program_count": trinary_round_trip_bench.get("program_count"),
            },
            "artifacts": [
                "data/igem_live_fasta_manifest.yaml",
                "data/math_generator_airfoil_rmse_manifest.yaml",
                "data/trinary_os_round_trip_manifest.yaml",
                "vendor/igem/fastas",
                "vendor/math_generator/datasets/airfoil_self_noise.csv",
                "vendor/trinary_os/fixtures",
                "vendor/trinary_os/round_trip",
                "FSOT.Formal.IGEMLiveFastaPriors",
                "FSOT.Formal.MathGeneratorAirfoilRmsePriors",
                "FSOT.Formal.TrinaryOSRoundTripPriors",
            ],
        },
        {
            "tier": 33,
            "name": "Consolidation — Tier 9 coverage, linguistics portable, crosswalk wave",
            "status": "complete"
            if domain_cov.get("domains_with_empirical_data") == 35
            and tokenization_smoke_bench.get("record_count", 0) >= 5
            and trinary_hw_motif_bench.get("record_count", 0) >= 5
            and intrinsic_llm_bench.get("record_count", 0) >= 5
            and tokenization_smoke_bench.get("median_error_pct", 99) <= 1.0
            and trinary_hw_motif_bench.get("median_error_pct", 99) <= 1.0
            and intrinsic_llm_bench.get("median_error_pct", 99) <= 1.0
            else "pending",
            "metrics": {
                "domain_coverage_empirical_domains": domain_cov.get("domains_with_empirical_data"),
                "tokenization_smoke_records": tokenization_smoke_bench.get("record_count"),
                "trinary_hardware_motif_records": trinary_hw_motif_bench.get("record_count"),
                "intrinsic_llm_validators_records": intrinsic_llm_bench.get("record_count"),
            },
            "artifacts": [
                "scripts/ingest_geophysical_labs.py",
                "vendor/linguistics/linguistics_derivations.json",
                "data/tokenization_smoke_manifest.yaml",
                "data/trinary_hardware_motif_manifest.yaml",
                "data/intrinsic_llm_validators_manifest.yaml",
                "FSOT.Formal.TokenizationSmokePriors",
                "FSOT.Formal.TrinaryHardwareMotifPriors",
                "FSOT.Formal.IntrinsicLLMValidatorsPriors",
            ],
        },
        {
            "tier": 34,
            "name": "Crosswalk wave — Physarum CUDA, arXiv V14 primitives, formula corpus CNC",
            "status": "complete"
            if biological_cuda_physarum_bench.get("record_count", 0) >= 5
            and arxiv_primitives_v14_bench.get("record_count", 0) >= 5
            and formula_corpus_cnc_bench.get("record_count", 0) >= 5
            and biological_cuda_physarum_bench.get("median_error_pct", 99) <= 5.0
            and arxiv_primitives_v14_bench.get("median_error_pct", 99) <= 1.0
            and formula_corpus_cnc_bench.get("median_error_pct", 99) <= 5.0
            else "pending",
            "metrics": {
                "biological_cuda_physarum_records": biological_cuda_physarum_bench.get("record_count"),
                "arxiv_primitives_v14_records": arxiv_primitives_v14_bench.get("record_count"),
                "formula_corpus_cnc_records": formula_corpus_cnc_bench.get("record_count"),
            },
            "artifacts": [
                "data/biological_cuda_physarum_manifest.yaml",
                "data/arxiv_primitives_v14_manifest.yaml",
                "data/formula_corpus_cnc_manifest.yaml",
                "vendor/physarum",
                "vendor/arxiv_primitives",
                "vendor/formula_corpus_cnc",
                "FSOT.Formal.BiologicalCudaPhysarumPriors",
                "FSOT.Formal.ArxivPrimitivesV14Priors",
                "FSOT.Formal.FormulaCorpusCncPriors",
            ],
        },
        {
            "tier": 35,
            "name": "Crosswalk wave — Rendlesham decoder, Qwen certified agent, Genesis omni-theory",
            "status": "complete"
            if binary_decoder_rendlesham_bench.get("record_count", 0) >= 5
            and certified_agent_qwen_bench.get("record_count", 0) >= 5
            and omni_theory_genesis_bench.get("record_count", 0) >= 5
            and binary_decoder_rendlesham_bench.get("median_error_pct", 99) <= 1.0
            and certified_agent_qwen_bench.get("median_error_pct", 99) <= 1.0
            and omni_theory_genesis_bench.get("median_error_pct", 99) <= 5.0
            else "pending",
            "metrics": {
                "binary_decoder_rendlesham_records": binary_decoder_rendlesham_bench.get("record_count"),
                "certified_agent_qwen_records": certified_agent_qwen_bench.get("record_count"),
                "omni_theory_genesis_records": omni_theory_genesis_bench.get("record_count"),
            },
            "artifacts": [
                "data/binary_decoder_rendlesham_manifest.yaml",
                "data/certified_agent_qwen_manifest.yaml",
                "data/omni_theory_genesis_manifest.yaml",
                "vendor/binary_decoder",
                "vendor/certified_agent",
                "vendor/omni_theory",
                "FSOT.Formal.BinaryDecoderRendleshamPriors",
                "FSOT.Formal.CertifiedAgentQwenPriors",
                "FSOT.Formal.OmniTheoryGenesisPriors",
            ],
        },
        {
            "tier": 36,
            "name": "Self-contained unit — portable formula corpus, aggregate DB, vendor audit",
            "status": "complete"
            if fsot_aggregate_unified_db_bench.get("record_count", 0) >= 5
            and prediction_rederivation_bench.get("record_count", 0) >= 5
            and vendor_audit.get("formula_corpus_portable")
            and vendor_audit.get("all_extension_benchmarks_present")
            and fsot_aggregate_unified_db_bench.get("median_error_pct", 99) <= 5.0
            and prediction_rederivation_bench.get("median_error_pct", 99) <= 5.0
            else "pending",
            "metrics": {
                "formula_corpus_portable": vendor_audit.get("formula_corpus_portable"),
                "formula_corpus_records_hint": vendor_audit.get("formula_corpus_records_hint"),
                "extension_domain_count": vendor_audit.get("extension_domain_count"),
                "fsot_aggregate_unified_db_records": fsot_aggregate_unified_db_bench.get("record_count"),
                "prediction_rederivation_records": prediction_rederivation_bench.get("record_count"),
                "precision_candidates_over_1pct": len(vendor_audit.get("precision_tightening_candidates") or []),
            },
            "artifacts": [
                "vendor/formula_corpus/by_domain/strict_empirical.jsonl",
                "vendor/fsot_aggregate",
                "data/fsot_aggregate_unified_db_manifest.yaml",
                "data/prediction_rederivation_manifest.yaml",
                "data/portable_vendor_coverage_audit.json",
                "FSOT.Formal.FsotAggregateUnifiedDbPriors",
                "FSOT.Formal.PredictionRederivationPriors",
            ],
        },
        {
            "tier": 37,
            "name": "Desktop crosswalk — VL distill atlas, Rust Lean bridge, Bibliography corpus",
            "status": "complete"
            if vl_distill_atlas_bench.get("record_count", 0) >= 5
            and rust_lean_bridge_bench.get("record_count", 0) >= 5
            and bibliography_lean_corpus_bench.get("record_count", 0) >= 5
            and vl_distill_atlas_bench.get("median_error_pct", 99) <= 1.0
            and rust_lean_bridge_bench.get("median_error_pct", 99) <= 1.0
            and bibliography_lean_corpus_bench.get("median_error_pct", 99) <= 1.0
            else "pending",
            "metrics": {
                "vl_distill_atlas_records": vl_distill_atlas_bench.get("record_count"),
                "rust_lean_bridge_records": rust_lean_bridge_bench.get("record_count"),
                "bibliography_lean_corpus_records": bibliography_lean_corpus_bench.get("record_count"),
                "extension_domain_count": vendor_audit.get("extension_domain_count"),
            },
            "artifacts": [
                "data/vl_distill_atlas_manifest.yaml",
                "data/rust_lean_bridge_manifest.yaml",
                "data/bibliography_lean_corpus_manifest.yaml",
                "vendor/vl_distill",
                "vendor/rust_lean_bridge",
                "vendor/bibliography_corpus",
                "FSOT.Formal.VlDistillAtlasPriors",
                "FSOT.Formal.RustLeanBridgePriors",
                "FSOT.Formal.BibliographyLeanCorpusPriors",
            ],
        },
    ]

    next_steps = [
        "Extension domain precision tightening (median error < 1% wave)",
        "Knowledge-base per-formula portable bundle",
        "Public API extension domains (NIST CODATA, GBIF, NOAA, Exoplanet Archive, OpenAlex)",
    ]

    completed = [t for t in tiers if t.get("status") == "complete"]
    pending = [t for t in tiers if t.get("status") != "complete"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "remote": "https://github.com/dappalumbo91/FSOT-2.1-Lean.git",
        "summary": {
            "lean_formal_modules": len(lean_modules),
            "proved_claims": proved_n,
            "sorry_count_formal": cert.get("sorry_count_formal", 0),
            "lean_build_ok": cert.get("lean_build_ok"),
            "tiers_complete": len(completed),
            "tiers_total": len(tiers),
            "percent_complete": round(100.0 * len(completed) / max(1, len(tiers)), 1),
        },
        "current_position": "Tier 37 Desktop crosswalk — VL distill atlas, Rust Lean bridge, Bibliography corpus",
        "tiers": tiers,
        "next_steps": next_steps,
        "key_metrics": {
            "strict_empirical_records": registry.get("formula_corpus", {}).get("records_total")
            or registry.get("knowledge_base", {}).get("strict_empirical"),
            "smiles_mapped": registry.get("smiles_lab", {}).get("mapped_records"),
            "allen_catalog_cells": cohort.get("total_cells_in_catalog"),
            "allen_eval_cells": cohort.get("cohort_fi_proxy", {}).get("cell_count"),
            "hero_fi_pct": round(100 * float((cohort.get("hero_certified_fi") or {}).get("mean_rel_err", 1)), 2),
            "canonical_bridge_fi_pct": round(
                100 * float((cohort.get("canonical_scalar_bridge") or {}).get("hero_canonical_mean_rel_err", 1)), 2
            ),
            "neurolab_domain_count": domain_cov.get("domain_count"),
            "domains_with_empirical_data": domain_cov.get("domains_with_empirical_data"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT verification progress tracker")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if yaml is None:
        raise RuntimeError("PyYAML required")
    doc = build_progress()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {args.output}")
    print(f"  progress: {s['percent_complete']}% ({s['tiers_complete']}/{s['tiers_total']} tiers)")
    print(f"  proved claims: {s['proved_claims']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())