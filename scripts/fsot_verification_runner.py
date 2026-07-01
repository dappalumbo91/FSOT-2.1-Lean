#!/usr/bin/env python3
"""
FSOT verification runner — numeric oracle for Lean formalization.

Compares canonical constants, domain scalars, and Wave-1 ΛCDM observables
against the authoritative fsot_compute.py engine.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from fsot_hash_gate import check_authority, check_cache_gate, scan_mirrors

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "canonical_constants.json"
RUN_LOG_PATH = ROOT / "data" / "verification_runs.jsonl"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
CERT_PATH = ROOT / "data" / "certificate.json"


def append_run_log(
    *,
    ok: bool,
    issues: list[str],
    authority_sha256: str | None,
    authority_path: str,
    lean_ok: bool,
) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else {}
    bio = registry.get("neurolab_bio", {})
    priors = bio.get("brain_component_priors", {})
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ok": ok,
        "issue_count": len(issues),
        "issues": issues[:20],
        "authority_path": authority_path,
        "authority_sha256": authority_sha256,
        "lean_build_ok": lean_ok,
        "smiles_records": registry.get("smiles_lab", {}).get("total_records"),
        "smiles_mapped": registry.get("smiles_lab", {}).get("mapped_records"),
        "brain_component_priors": priors.get("count", 0),
        "brain_component_priors_sha256": priors.get("sha256"),
        "translation_total": bio.get("translation_total"),
        "certificate_path": str(CERT_PATH),
    }
    RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RUN_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

CANONICAL_PATHS = [
    Path(r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py"),
    ROOT / "_research" / "FSOT-2.0-code" / "fsot-2.0" / "fsot_2_0.py",
    Path(r"C:\Users\damia\Desktop\FSOT Cosmology Lab\fsot_compute.py"),
]


def load_fsot_compute():
    for path in CANONICAL_PATHS:
        if not path.exists():
            continue
        spec = importlib.util.spec_from_file_location("fsot_compute", path)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod, path
    raise FileNotFoundError("fsot_compute.py not found in expected locations")


def rel_err(a: float, b: float) -> float:
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def check_constants(mod, cache: dict) -> list[str]:
    issues: list[str] = []
    pairs = [
        ("layer2.k", float(mod.K), float(cache["layer2"]["k"])),
        ("layer2.acoustic_bleed", float(mod.A_BLEED), float(cache["layer2"]["acoustic_bleed"])),
        ("layer2.acoustic_inflow", float(mod.A_IN), float(cache["layer2"]["acoustic_inflow"])),
        ("domain_scalars.S_cosm", float(mod.S_COSM), float(cache["domain_scalars"]["S_cosm"])),
        ("domain_scalars.S_quant", float(mod.S_QUANT), float(cache["domain_scalars"]["S_quant"])),
    ]
    for name, live, cached in pairs:
        err = rel_err(live, cached)
        if err > 1e-12:
            issues.append(f"{name}: cache mismatch ({err:.3e})")
    return issues


def check_wave1(mod, cache: dict, tol: float = 1e-9) -> list[str]:
    issues: list[str] = []
    for result in mod.wave1():
        cached = cache["wave1"].get(result.name)
        if cached is None:
            issues.append(f"wave1 missing in cache: {result.name}")
            continue
        err = rel_err(float(result.computed), float(cached))
        if err > tol:
            issues.append(f"wave1 {result.name}: drift ({err:.3e})")
    return issues


def check_dominance_heuristics(mod) -> list[str]:
    """Sanity checks aligned with FSOT.Formal.Theorems cosmological bounds."""
    issues: list[str] = []
    beta = float(mod.BETA)
    if not (0 < beta < 0.01):
        issues.append(f"beta expected tiny positive, got {beta}")
    if float(mod.A_BLEED) >= float(mod.PHI):
        issues.append("acoustic_bleed should be < phi for bleed bounds")
    return issues


def run_lean_build() -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            [
                "lake",
                "build",
                "FSOT.Formal.Bounds",
                "FSOT.Formal.Theorems",
                "FSOT.Formal.Cosmology",
                "FSOT.Formal.Domains",
                "FSOT.Formal.Genomic",
                "FSOT.Formal.BrainPriors",
                "FSOT.Formal.CodonPriors",
                "FSOT.Formal.ProteinPriors",
                "FSOT.Formal.ProteinFormulas",
                "FSOT.Formal.CosmologyLab",
                "FSOT.Formal.FuelPriors",
                "FSOT.Formal.SpeciesPriors",
                "FSOT.Formal.CameoPriors",
                "FSOT.Formal.TrinaryOSPriors",
                "FSOT.Formal.PhotonicForge",
                "FSOT.Formal.VibRegisterPriors",
                "FSOT.Formal.MagneticStringPriors",
                "FSOT.Formal.EvolutionPriors",
                "FSOT.Formal.WeatherPriors",
                "FSOT.Formal.LinguisticsPriors",
                "FSOT.Formal.UnifiedDBPriors",
                "FSOT.Formal.CosmologyWave4",
                "FSOT.Formal.KronosPriors",
                "FSOT.Formal.KnowledgeBasePriors",
                "FSOT.Formal.MathGeneratorPriors",
                "FSOT.Formal.TrinaryFluidPriors",
                "FSOT.Formal.SoulSiblingPriors",
                "FSOT.Formal.LeanProofsBridge",
                "FSOT.Formal.FormulaCorpusPriors",
                "FSOT.Formal.CellularPriors",
                "FSOT.Formal.BlackHoleThesisPriors",
                "FSOT.Formal.NeuronHybridPriors",
                "FSOT.Formal.NeuronCohortPriors",
                "FSOT.Formal.NeuronCohortStrataPriors",
                "FSOT.Formal.AetherPrimePriors",
                "FSOT.Formal.MagicCirclePriors",
                "FSOT.Formal.ExperimentSynthesisPriors",
                "FSOT.Formal.Lab",
                "FSOT",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        ok = proc.returncode == 0
        return ok, proc.stdout + proc.stderr
    except FileNotFoundError:
        return False, "lake not found on PATH"


def print_mirror_scan() -> None:
    print("\n=== Hash-gate mirrors (Desktop fsot_compute.py) ===")
    for row in scan_mirrors():
        if not row["present"]:
            print(f"  {row['label']:14s}  MISSING")
            continue
        status = "OK" if row["matches_expected"] else "MISMATCH"
        digest = row["sha256"][:16]
        print(
            f"  {row['label']:14s}  {status:8s}  "
            f"{row['class']:13s}  {digest}..."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT verification runner")
    parser.add_argument("--skip-lean", action="store_true", help="Skip lake build step")
    parser.add_argument("--sync", action="store_true", help="Regenerate canonical_constants.json first")
    parser.add_argument(
        "--no-hash-gate",
        action="store_true",
        help="Skip SHA-256 authority gate checks",
    )
    parser.add_argument(
        "--scan-mirrors",
        action="store_true",
        help="Print Desktop mirror digest table and exit",
    )
    args = parser.parse_args()

    if args.scan_mirrors:
        print_mirror_scan()
        return 0

    if args.sync:
        sync = ROOT / "scripts" / "sync_canonical_constants.py"
        subprocess.run([sys.executable, str(sync)], check=True)

    fill_gaps = ROOT / "scripts" / "fill_smiles_catalog_gaps.py"
    if fill_gaps.exists():
        subprocess.run([sys.executable, str(fill_gaps)], cwd=ROOT, check=False)

    align_nb = ROOT / "scripts" / "align_neurolab_domains.py"
    if align_nb.exists():
        subprocess.run([sys.executable, str(align_nb), "--skip-sync"], cwd=ROOT, check=False)
        sync_mirrors = ROOT / "scripts" / "sync_lab_compute_mirrors.py"
        if sync_mirrors.exists():
            subprocess.run([sys.executable, str(sync_mirrors)], cwd=ROOT, check=False)

    mod, source = load_fsot_compute()
    print(f"Using compute engine: {source}")

    if not DATA.exists():
        print("canonical_constants.json missing; run with --sync first", file=sys.stderr)
        return 2

    cache = json.loads(DATA.read_text(encoding="utf-8"))
    issues: list[str] = []

    gate_ok, live_digest, gate_issues = check_authority(source)
    if not args.no_hash_gate:
        issues.extend(gate_issues)
        issues.extend(check_cache_gate(cache, live_digest))
        print(f"\n=== Hash gate ===")
        print(f"  authority_sha256 = {live_digest}")
        print(f"  gate             {'OK' if gate_ok else 'FAIL'}")
        print_mirror_scan()

    issues.extend(check_constants(mod, cache))
    issues.extend(check_wave1(mod, cache))
    issues.extend(check_dominance_heuristics(mod))

    section_map = ROOT / "scripts" / "build_section_domain_map.py"
    if section_map.exists():
        subprocess.run([sys.executable, str(section_map)], cwd=ROOT, check=False)
    ingest = ROOT / "scripts" / "ingest_lab_data.py"
    verify_lab = ROOT / "scripts" / "verify_lab_registry.py"
    if ingest.exists():
        print("\n=== Lab data ingest (SMILES + NeuroLab) ===")
        proc = subprocess.run(
            [sys.executable, str(ingest)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        print(proc.stdout.strip() or proc.stderr.strip())
        if proc.returncode != 0:
            issues.append("lab data ingest failed")
        elif verify_lab.exists():
            proc2 = subprocess.run(
                [sys.executable, str(verify_lab)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc2.stdout.strip())
            if proc2.returncode != 0:
                issues.append("lab registry verification failed")
                if proc2.stdout:
                    for line in proc2.stdout.splitlines():
                        if line.strip().startswith("- "):
                            issues.append(line.strip()[2:])
        gen_brain_priors = ROOT / "scripts" / "gen_brain_priors_lean.py"
        if gen_brain_priors.exists() and proc.returncode == 0:
            proc_bp = subprocess.run(
                [sys.executable, str(gen_brain_priors)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_bp.stdout.strip() or proc_bp.stderr.strip())
            if proc_bp.returncode != 0:
                issues.append("BrainPriors.lean generation failed")
        ingest_codon = ROOT / "scripts" / "ingest_codon_map.py"
        gen_codon_priors = ROOT / "scripts" / "gen_codon_priors_lean.py"
        if ingest_codon.exists() and proc.returncode == 0:
            proc_ci = subprocess.run(
                [sys.executable, str(ingest_codon)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_ci.stdout.strip() or proc_ci.stderr.strip())
            if proc_ci.returncode != 0:
                issues.append("codon map ingest failed")
            elif gen_codon_priors.exists():
                proc_cp = subprocess.run(
                    [sys.executable, str(gen_codon_priors)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_cp.stdout.strip() or proc_cp.stderr.strip())
                if proc_cp.returncode != 0:
                    issues.append("CodonPriors.lean generation failed")
        verify_codon = ROOT / "scripts" / "verify_codon_map.py"
        if verify_codon.exists():
            proc_codon = subprocess.run(
                [sys.executable, str(verify_codon)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_codon.stdout.strip())
            if proc_codon.returncode != 0:
                issues.append("codon trinary map verification failed")
        ingest_protein = ROOT / "scripts" / "ingest_protein_formulas.py"
        gen_protein_priors = ROOT / "scripts" / "gen_protein_priors_lean.py"
        if ingest_protein.exists() and proc.returncode == 0:
            proc_pi = subprocess.run(
                [sys.executable, str(ingest_protein)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_pi.stdout.strip() or proc_pi.stderr.strip())
            if proc_pi.returncode != 0:
                issues.append("protein formula ingest failed")
            elif gen_protein_priors.exists():
                proc_pp = subprocess.run(
                    [sys.executable, str(gen_protein_priors)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_pp.stdout.strip() or proc_pp.stderr.strip())
                if proc_pp.returncode != 0:
                    issues.append("ProteinPriors.lean generation failed")
                gen_protein_formulas = ROOT / "scripts" / "gen_protein_formulas_lean.py"
                if gen_protein_formulas.exists():
                    proc_pf = subprocess.run(
                        [sys.executable, str(gen_protein_formulas)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    print(proc_pf.stdout.strip() or proc_pf.stderr.strip())
                    if proc_pf.returncode != 0:
                        issues.append("ProteinFormulas.lean generation failed")
        verify_protein = ROOT / "scripts" / "verify_protein_formulas.py"
        if verify_protein.exists():
            proc4 = subprocess.run(
                [sys.executable, str(verify_protein)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc4.stdout.strip())
            if proc4.returncode != 0:
                issues.append("protein formula verification failed")

        tier2_ingests = [
            ("ingest_cosmology_lab.py", "gen_cosmology_lab_lean.py", "CosmologyLab.lean generation failed", "cosmology lab ingest failed"),
            ("ingest_fuel_lab.py", "gen_fuel_priors_lean.py", "FuelPriors.lean generation failed", "fuel lab ingest failed"),
            ("ingest_species_catalog.py", "gen_species_priors_lean.py", "SpeciesPriors.lean generation failed", "species catalog ingest failed"),
        ]
        for ingest_name, gen_name, gen_fail, ingest_fail in tier2_ingests:
            ingest_script = ROOT / "scripts" / ingest_name
            gen_script = ROOT / "scripts" / gen_name
            if ingest_script.exists() and proc.returncode == 0:
                proc_ing = subprocess.run(
                    [sys.executable, str(ingest_script)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_ing.stdout.strip() or proc_ing.stderr.strip())
                if proc_ing.returncode != 0:
                    issues.append(ingest_fail)
                elif gen_script.exists():
                    proc_gen = subprocess.run(
                        [sys.executable, str(gen_script)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    print(proc_gen.stdout.strip() or proc_gen.stderr.strip())
                    if proc_gen.returncode != 0:
                        issues.append(gen_fail)
        tier3_ingests = [
            ("ingest_cameo_lab.py", "gen_cameo_priors_lean.py", "CameoPriors.lean generation failed", "CAMEO lab ingest failed"),
            ("ingest_trinary_os.py", "gen_trinary_os_lean.py", "TrinaryOSPriors.lean generation failed", "trinary OS ingest failed"),
            ("ingest_photonic_forge.py", "gen_photonic_forge_lean.py", "PhotonicForge.lean generation failed", "photonic forge ingest failed"),
        ]
        for ingest_name, gen_name, gen_fail, ingest_fail in tier3_ingests:
            ingest_script = ROOT / "scripts" / ingest_name
            gen_script = ROOT / "scripts" / gen_name
            if ingest_script.exists() and proc.returncode == 0:
                proc_ing = subprocess.run(
                    [sys.executable, str(ingest_script)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_ing.stdout.strip() or proc_ing.stderr.strip())
                if proc_ing.returncode != 0:
                    issues.append(ingest_fail)
                elif gen_script.exists():
                    proc_gen = subprocess.run(
                        [sys.executable, str(gen_script)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    print(proc_gen.stdout.strip() or proc_gen.stderr.strip())
                    if proc_gen.returncode != 0:
                        issues.append(gen_fail)
        tier4_ingests = [
            ("ingest_vibra_register.py", "gen_vibra_register_lean.py", "VibRegisterPriors.lean generation failed", "VibraFSOT register ingest failed"),
            ("ingest_magnetic_strings.py", "gen_magnetic_strings_lean.py", "MagneticStringPriors.lean generation failed", "magnetic strings ingest failed"),
            ("ingest_evolution_lab.py", "gen_evolution_priors_lean.py", "EvolutionPriors.lean generation failed", "evolution lab ingest failed"),
            ("ingest_weather_lab.py", "gen_weather_priors_lean.py", "WeatherPriors.lean generation failed", "weather lab ingest failed"),
            ("ingest_linguistics_lab.py", "gen_linguistics_priors_lean.py", "LinguisticsPriors.lean generation failed", "linguistics lab ingest failed"),
            ("ingest_unified_db.py", "gen_unified_db_lean.py", "UnifiedDBPriors.lean generation failed", "unified DB ingest failed"),
        ]
        for ingest_name, gen_name, gen_fail, ingest_fail in tier4_ingests:
            ingest_script = ROOT / "scripts" / ingest_name
            gen_script = ROOT / "scripts" / gen_name
            if ingest_script.exists() and proc.returncode == 0:
                proc_ing = subprocess.run(
                    [sys.executable, str(ingest_script)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_ing.stdout.strip() or proc_ing.stderr.strip())
                if proc_ing.returncode != 0:
                    issues.append(ingest_fail)
                elif gen_script.exists():
                    proc_gen = subprocess.run(
                        [sys.executable, str(gen_script)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    print(proc_gen.stdout.strip() or proc_gen.stderr.strip())
                    if proc_gen.returncode != 0:
                        issues.append(gen_fail)
        gap_resolver = ROOT / "scripts" / "resolve_strict_empirical_gap.py"
        if gap_resolver.exists():
            proc_gap = subprocess.run(
                [sys.executable, str(gap_resolver)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_gap.stdout.strip() or proc_gap.stderr.strip())
            if proc_gap.returncode != 0:
                issues.append("strict-empirical CNC gap resolution failed")

        numeric_eval = ROOT / "scripts" / "run_numeric_eval_queue.py"
        if numeric_eval.exists():
            proc_ne = subprocess.run(
                [sys.executable, str(numeric_eval), "--skip-pipeline"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_ne.stdout.strip() or proc_ne.stderr.strip())
            if proc_ne.returncode != 0:
                issues.append("numeric eval queue backfill failed")

        kb_verify = ROOT / "scripts" / "run_knowledge_base_formula_verify.py"
        if kb_verify.exists():
            proc_kb = subprocess.run(
                [sys.executable, str(kb_verify), "--skip-validator"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc_kb.stdout.strip() or proc_kb.stderr.strip())
            if proc_kb.returncode != 0:
                issues.append("knowledge base per-formula verification failed")

        tier5_ingests = [
            ("ingest_cosmology_wave4.py", "gen_cosmology_wave4_lean.py", "CosmologyWave4.lean generation failed", "cosmology wave4 ingest failed"),
            ("ingest_kronos_lab.py", "gen_kronos_priors_lean.py", "KronosPriors.lean generation failed", "Kronos lab ingest failed"),
            ("ingest_knowledge_base.py", "gen_knowledge_base_lean.py", "KnowledgeBasePriors.lean generation failed", "knowledge base ingest failed"),
            ("ingest_math_generator_lab.py", "gen_math_generator_lean.py", "MathGeneratorPriors.lean generation failed", "math generator ingest failed"),
            ("ingest_trinary_fluid_computer.py", "gen_trinary_fluid_lean.py", "TrinaryFluidPriors.lean generation failed", "trinary fluid ingest failed"),
            ("ingest_soul_sibling.py", "gen_soul_sibling_lean.py", "SoulSiblingPriors.lean generation failed", "soul sibling ingest failed"),
            ("ingest_lean_proofs_bridge.py", "gen_lean_proofs_bridge_lean.py", "LeanProofsBridge.lean generation failed", "lean proofs bridge ingest failed"),
            ("ingest_formula_corpus.py", "gen_formula_corpus_lean.py", "FormulaCorpusPriors.lean generation failed", "formula corpus ingest failed"),
            ("ingest_cellular_lab.py", "gen_cellular_priors_lean.py", "CellularPriors.lean generation failed", "cellular lab ingest failed"),
            ("ingest_blackhole_thesis.py", "gen_blackhole_thesis_lean.py", "BlackHoleThesisPriors.lean generation failed", "blackhole thesis ingest failed"),
            ("ingest_experiment_synthesis.py", "gen_experiment_synthesis_lean.py", "ExperimentSynthesisPriors.lean generation failed", "experiment synthesis ingest failed"),
        ]
        for ingest_name, gen_name, gen_fail, ingest_fail in tier5_ingests:
            ingest_script = ROOT / "scripts" / ingest_name
            gen_script = ROOT / "scripts" / gen_name
            if ingest_script.exists() and proc.returncode == 0:
                proc_ing = subprocess.run(
                    [sys.executable, str(ingest_script)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_ing.stdout.strip() or proc_ing.stderr.strip())
                if proc_ing.returncode != 0:
                    issues.append(ingest_fail)
                elif gen_script.exists():
                    proc_gen = subprocess.run(
                        [sys.executable, str(gen_script)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    print(proc_gen.stdout.strip() or proc_gen.stderr.strip())
                    if proc_gen.returncode != 0:
                        issues.append(gen_fail)
        for verify_name, fail_msg in (
            ("verify_cosmology_lab.py", "Cosmology Lab ΛCDM verification failed"),
            ("verify_fuel_lab.py", "Fuel Lab verification failed"),
            ("verify_species_catalog.py", "species catalog verification failed"),
            ("verify_cameo_lab.py", "CAMEO Lab verification failed"),
            ("verify_trinary_os.py", "Trinary OS verification failed"),
            ("verify_photonic_forge.py", "Photonic Forge verification failed"),
            ("verify_vibra_register.py", "VibraFSOT register verification failed"),
            ("verify_magnetic_strings.py", "Magnetic strings verification failed"),
            ("verify_evolution_lab.py", "Evolution Lab verification failed"),
            ("verify_weather_lab.py", "Weather Lab verification failed"),
            ("verify_linguistics_lab.py", "Linguistics Lab verification failed"),
            ("verify_unified_db.py", "Unified DB verification failed"),
            ("verify_cosmology_wave4.py", "Cosmology Wave-4 verification failed"),
            ("verify_kronos_lab.py", "Kronos Lab verification failed"),
            ("verify_knowledge_base.py", "Knowledge Base verification failed"),
            ("verify_math_generator_lab.py", "Math Generator verification failed"),
            ("verify_trinary_fluid_computer.py", "Trinary Fluid Computer verification failed"),
            ("verify_soul_sibling.py", "Soul Sibling verification failed"),
            ("verify_lean_proofs_bridge.py", "Lean Proofs bridge verification failed"),
            ("verify_formula_corpus.py", "Formula corpus strict-empirical verification failed"),
            ("verify_cellular_lab.py", "Cellular lab verification failed"),
            ("verify_blackhole_thesis.py", "BlackHole thesis verification failed"),
            ("verify_experiment_synthesis.py", "Experiment synthesis verification failed"),
        ):
            verify_script = ROOT / "scripts" / verify_name
            if verify_script.exists():
                proc_v = subprocess.run(
                    [sys.executable, str(verify_script)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                print(proc_v.stdout.strip())
                if proc_v.returncode != 0:
                    issues.append(fail_msg)

        parse_bio = ROOT / "scripts" / "parse_neurolab_translations.py"
        verify_bio = ROOT / "scripts" / "verify_neurolab_bio.py"
        if parse_bio.exists():
            subprocess.run([sys.executable, str(parse_bio)], cwd=ROOT, check=False)
        if verify_bio.exists():
            proc3 = subprocess.run(
                [sys.executable, str(verify_bio)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc3.stdout.strip())
            if proc3.returncode != 0:
                issues.append("NeuroLab biological verification failed")

    print("\n=== Wave 1 (ΛCDM core) ===")
    for r in mod.wave1():
        print(f"  {r.name:20s}  {float(r.computed):.8f}")

    print("\n=== Domain scalars ===")
    print(f"  S_cosm = {float(mod.S_COSM):.8f}")
    print(f"  S_quant = {float(mod.S_QUANT):.8f}")

    gen_bounds = ROOT / "scripts" / "gen_genomic_bounds.py"
    if gen_bounds.exists():
        print("\n=== Genomic exact identity checks ===")
        proc_g = subprocess.run(
            [sys.executable, str(gen_bounds), "--write-lean"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        print(proc_g.stdout.strip() or proc_g.stderr.strip())
        if proc_g.returncode != 0:
            issues.append("genomic exact identity validation failed")

    if not args.skip_lean:
        print("\n=== Lean build ===")
        ok, log = run_lean_build()
        print("  OK" if ok else "  FAILED")
        if not ok:
            issues.append("Lean build failed")
            print(log[-4000:])

    print("\n=== Summary ===")
    lean_ok = not args.skip_lean and "Lean build failed" not in issues
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        append_run_log(
            ok=False,
            issues=issues,
            authority_sha256=live_digest if not args.no_hash_gate else None,
            authority_path=str(source),
            lean_ok=lean_ok,
        )
        return 1

    print("  All checks passed.")

    export = ROOT / "scripts" / "export_certificate.py"
    if export.exists():
        print("\n=== Certificate export ===")
        cmd = [
            sys.executable,
            str(export),
            "--authority-path",
            str(source),
        ]
        if lean_ok:
            cmd.append("--lean-ok")
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        print(proc.stdout.strip() or proc.stderr.strip())
        if proc.returncode != 0:
            issues.append("certificate export failed")
            append_run_log(
                ok=False,
                issues=issues,
                authority_sha256=live_digest if not args.no_hash_gate else None,
                authority_path=str(source),
                lean_ok=lean_ok,
            )
            return 1

    append_run_log(
        ok=True,
        issues=[],
        authority_sha256=live_digest if not args.no_hash_gate else None,
        authority_path=str(source),
        lean_ok=lean_ok,
    )
    if RUN_LOG_PATH.exists():
        print(f"  Run logged: {RUN_LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())