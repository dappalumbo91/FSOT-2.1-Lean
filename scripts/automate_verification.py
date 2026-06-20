#!/usr/bin/env python3
"""
Staged FSOT verification automation.

Lean proves structural certificates (signs, K intervals, bundles).
Python automates numeric lab checks, ingest, hash gate, and lake build.

Usage:
  python scripts/automate_verification.py              # full pipeline
  python scripts/automate_verification.py --stage bio  # NeuroLab bio only
  python scripts/automate_verification.py --list-stages
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

STAGES: dict[str, tuple[str, list[str]]] = {
    "gaps": ("Fill SMILES catalog gaps", ["fill_smiles_catalog_gaps.py"]),
    "align": ("Align NeuroLab domains to Lean ledger", ["align_neurolab_domains.py", "--skip-sync"]),
    "mirrors": ("Sync lab fsot_compute mirrors", ["sync_lab_compute_mirrors.py"]),
    "parse_bio": ("Parse NeuroLab biological translations", ["parse_neurolab_translations.py"]),
    "genomic": ("Validate genomic exact identities + sync Lean brackets", ["gen_genomic_bounds.py", "--write-lean"]),
    "ingest": ("Ingest SMILES + NeuroLab registry", ["ingest_lab_data.py"]),
    "brain_priors_lean": ("Generate BrainPriors.lean from registry", ["gen_brain_priors_lean.py"]),
    "codon_ingest": ("Ingest 64-codon dual-axis trinary map", ["ingest_codon_map.py"]),
    "codon_priors_lean": ("Generate CodonPriors.lean from registry", ["gen_codon_priors_lean.py"]),
    "protein_ingest": ("Ingest protein trinary phases into registry", ["ingest_protein_formulas.py"]),
    "protein_priors_lean": ("Generate ProteinPriors.lean from registry", ["gen_protein_priors_lean.py"]),
    "protein_formulas_lean": ("Generate ProteinFormulas.lean closed forms", ["gen_protein_formulas_lean.py"]),
    "verify_lab": ("Verify lab registry", ["verify_lab_registry.py"]),
    "verify_bio": ("Verify NeuroLab biological data", ["verify_neurolab_bio.py"]),
    "verify_codon": ("Verify 64-codon trinary map", ["verify_codon_map.py"]),
    "verify_protein": ("Verify protein amino-acid trinary phases", ["verify_protein_formulas.py"]),
    "cosmology_ingest": ("Ingest Cosmology Lab ΛCDM observables", ["ingest_cosmology_lab.py"]),
    "cosmology_priors_lean": ("Generate CosmologyLab.lean", ["gen_cosmology_lab_lean.py"]),
    "fuel_ingest": ("Ingest Fuel Lab compound profiles", ["ingest_fuel_lab.py"]),
    "fuel_priors_lean": ("Generate FuelPriors.lean", ["gen_fuel_priors_lean.py"]),
    "species_ingest": ("Ingest Machine & Molecule species catalog", ["ingest_species_catalog.py"]),
    "species_priors_lean": ("Generate SpeciesPriors.lean", ["gen_species_priors_lean.py"]),
    "verify_cosmology": ("Verify Cosmology Lab ΛCDM observables", ["verify_cosmology_lab.py"]),
    "verify_fuel": ("Verify Fuel Lab compound lookups", ["verify_fuel_lab.py"]),
    "verify_species": ("Verify species catalog tolerances", ["verify_species_catalog.py"]),
    "cameo_ingest": ("Ingest Genetics CAMEO benchmarks", ["ingest_cameo_lab.py"]),
    "cameo_priors_lean": ("Generate CameoPriors.lean", ["gen_cameo_priors_lean.py"]),
    "trinary_os_ingest": ("Ingest Fsot trinary OS oracles", ["ingest_trinary_os.py"]),
    "trinary_os_lean": ("Generate TrinaryOSPriors.lean", ["gen_trinary_os_lean.py"]),
    "photonic_ingest": ("Ingest FSOT Photonic V2 payload", ["ingest_photonic_forge.py"]),
    "photonic_lean": ("Generate PhotonicForge.lean", ["gen_photonic_forge_lean.py"]),
    "verify_cameo": ("Verify CAMEO symbolic benchmarks", ["verify_cameo_lab.py"]),
    "verify_trinary_os": ("Verify trinary OS FSOTB oracles", ["verify_trinary_os.py"]),
    "verify_photonic": ("Verify photonic VRAM payload", ["verify_photonic_forge.py"]),
    "vibra_ingest": ("Ingest VibraFSOT register + MC report", ["ingest_vibra_register.py"]),
    "vibra_lean": ("Generate VibRegisterPriors.lean", ["gen_vibra_register_lean.py"]),
    "magnetic_ingest": ("Ingest magnetic string lattice", ["ingest_magnetic_strings.py"]),
    "magnetic_lean": ("Generate MagneticStringPriors.lean", ["gen_magnetic_strings_lean.py"]),
    "evolution_ingest": ("Ingest evolution sim operons", ["ingest_evolution_lab.py"]),
    "evolution_lean": ("Generate EvolutionPriors.lean", ["gen_evolution_priors_lean.py"]),
    "weather_ingest": ("Ingest weather simulation log", ["ingest_weather_lab.py"]),
    "weather_lean": ("Generate WeatherPriors.lean", ["gen_weather_priors_lean.py"]),
    "linguistics_ingest": ("Ingest linguistics empirical targets", ["ingest_linguistics_lab.py"]),
    "linguistics_lean": ("Generate LinguisticsPriors.lean", ["gen_linguistics_priors_lean.py"]),
    "unified_db_ingest": ("Ingest unified DB verification report", ["ingest_unified_db.py"]),
    "unified_db_lean": ("Generate UnifiedDBPriors.lean", ["gen_unified_db_lean.py"]),
    "verify_vibra": ("Verify VibraFSOT register + MC alignment", ["verify_vibra_register.py"]),
    "verify_magnetic": ("Verify magnetic string lattice", ["verify_magnetic_strings.py"]),
    "verify_evolution": ("Verify evolution sim metrics", ["verify_evolution_lab.py"]),
    "verify_weather": ("Verify weather scalar simulation", ["verify_weather_lab.py"]),
    "verify_linguistics": ("Verify linguistics anchor derivations", ["verify_linguistics_lab.py"]),
    "verify_unified_db": ("Verify unified DB meta-oracle", ["verify_unified_db.py"]),
    "wave4_ingest": ("Ingest Cosmology Lab Wave-4 observables", ["ingest_cosmology_wave4.py"]),
    "wave4_lean": ("Generate CosmologyWave4.lean", ["gen_cosmology_wave4_lean.py"]),
    "kronos_ingest": ("Ingest Kronos metrology thesis runs", ["ingest_kronos_lab.py"]),
    "kronos_lean": ("Generate KronosPriors.lean", ["gen_kronos_priors_lean.py"]),
    "knowledge_ingest": ("Ingest Knowledge base unified transfer corpus", ["ingest_knowledge_base.py"]),
    "knowledge_lean": ("Generate KnowledgeBasePriors.lean", ["gen_knowledge_base_lean.py"]),
    "math_gen_ingest": ("Ingest Math generator comparison report", ["ingest_math_generator_lab.py"]),
    "math_gen_lean": ("Generate MathGeneratorPriors.lean", ["gen_math_generator_lean.py"]),
    "trinary_fluid_ingest": ("Ingest Trinary Fluid Computer v2 audit", ["ingest_trinary_fluid_computer.py"]),
    "trinary_fluid_lean": ("Generate TrinaryFluidPriors.lean", ["gen_trinary_fluid_lean.py"]),
    "soul_sibling_ingest": ("Ingest Soul Sibling kernel manifest", ["ingest_soul_sibling.py"]),
    "soul_sibling_lean": ("Generate SoulSiblingPriors.lean", ["gen_soul_sibling_lean.py"]),
    "lean_proofs_ingest": ("Ingest FSOT_Lean_Proofs formal output", ["ingest_lean_proofs_bridge.py"]),
    "lean_proofs_lean": ("Generate LeanProofsBridge.lean", ["gen_lean_proofs_bridge_lean.py"]),
    "verify_wave4": ("Verify Cosmology Wave-4 observables", ["verify_cosmology_wave4.py"]),
    "verify_kronos": ("Verify Kronos metrology runs", ["verify_kronos_lab.py"]),
    "verify_knowledge": ("Verify Knowledge base corpus", ["verify_knowledge_base.py"]),
    "verify_math_gen": ("Verify Math generator comparisons", ["verify_math_generator_lab.py"]),
    "verify_trinary_fluid": ("Verify Trinary Fluid Computer v2", ["verify_trinary_fluid_computer.py"]),
    "verify_soul_sibling": ("Verify Soul Sibling kernel", ["verify_soul_sibling.py"]),
    "verify_lean_proofs": ("Verify Lean proofs constant bridge", ["verify_lean_proofs_bridge.py"]),
    "synthesis_ingest": ("Ingest Tier 7 experiment synthesis labs", ["ingest_experiment_synthesis.py"]),
    "synthesis_lean": ("Generate experiment synthesis Lean priors", ["gen_experiment_synthesis_lean.py"]),
    "verify_synthesis": ("Verify experiment synthesis vs fsot_compute", ["verify_experiment_synthesis.py"]),
    "runner": ("Full hash gate + Lean build + certificate", ["fsot_verification_runner.py"]),
}


def run_stage(name: str, extra_args: list[str] | None = None) -> int:
    label, argv = STAGES[name]
    cmd = [sys.executable, str(SCRIPTS / argv[0]), *argv[1:], *(extra_args or [])]
    print(f"\n── Stage: {name} — {label}")
    proc = subprocess.run(cmd, cwd=ROOT, check=False)
    if proc.returncode != 0:
        print(f"  FAILED (exit {proc.returncode})")
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Staged FSOT verification automation")
    parser.add_argument("--stage", action="append", help="Run only these stage(s)")
    parser.add_argument("--list-stages", action="store_true")
    parser.add_argument("--skip-lean", action="store_true", help="Pass --skip-lean to runner stage")
    args = parser.parse_args()

    if args.list_stages:
        for key, (label, _) in STAGES.items():
            print(f"  {key:12s}  {label}")
        return 0

    if args.stage:
        selected = args.stage
    else:
        selected = list(STAGES.keys())

    failures = 0
    for name in selected:
        extra = ["--skip-lean"] if name == "runner" and args.skip_lean else None
        if run_stage(name, extra) != 0:
            failures += 1
            if name in (
                "verify_lab", "verify_bio", "verify_codon", "verify_protein",
                "verify_cosmology", "verify_fuel", "verify_species",
                "verify_vibra", "verify_magnetic", "verify_evolution",
                "verify_weather", "verify_linguistics", "verify_unified_db",
                "verify_wave4", "verify_kronos", "verify_knowledge", "verify_math_gen",
                "verify_trinary_fluid", "verify_soul_sibling", "verify_lean_proofs", "runner",
            ):
                break

    print(f"\n=== Automation summary: {len(selected) - failures}/{len(selected)} stages OK ===")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())