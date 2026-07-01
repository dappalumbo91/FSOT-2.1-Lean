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
    ]

    next_steps = [
        "Per-stratum hybrid FI sim (not just slope proxy) for top specimens per class",
        "Multi-hero held-out: certify 3–5 specimens per Sst/PV/VIP/L2/3",
        "Tighten canonical bridge per-class using psi_con/eta_eff only",
        "Wire remaining LLM experiment folders into Lean namespaces",
        "Cohort train/holdout split with Lean regression gates",
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
        "current_position": "Tier 15 Wave A core theory grounding (thesis sim + emergent MC + math rules)",
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