#!/usr/bin/env python3
"""Regenerate all FSOT.Formal.* Lean priors from benchmark JSON (clone-and-rebuild)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Core generators first, then extension/tier waves (order matters for dependency logging only).
GENERATOR_ORDER = [
    "gen_brain_priors_lean.py",
    "gen_codon_priors_lean.py",
    "gen_protein_priors_lean.py",
    "gen_protein_formulas_lean.py",
    "gen_extension_domains_lean.py",
    "gen_intelligence_compression_lean.py",
    "gen_cosmology_extended_lean.py",
    "gen_particle_physics_lean.py",
    "gen_cosmology_higher_waves_lean.py",
    "gen_cosmology_wave_lean.py",
    "gen_higgs_branching_lean.py",
    "gen_higgs_mass_lean.py",
    "gen_magnetosphere_extended_lean.py",
    "gen_geochemistry_lean.py",
    "gen_oncology_lean.py",
    "gen_neuroimmunology_lean.py",
    "gen_synthetic_biology_lean.py",
    "gen_quantum_materials_lean.py",
    "gen_multi_hero_lean.py",
    "gen_materials_engineering_lean.py",
    "gen_linguistics_priors_lean.py",
    "gen_math_generator_rules_eval_lean.py",
    "gen_igem_synthetic_biology_lean.py",
    "gen_formula_corpus_closure_lean.py",
    "gen_domain_coupling_simulation_lean.py",
    "gen_tier_f_extension_lean.py",
    "gen_tier_gap_fill_lean.py",
    "gen_tier_d_extension_lean.py",
    "gen_tier_h_cybersecurity_lean.py",
    "gen_tier_i_programming_lean.py",
    "gen_tier_j_toe_completeness_lean.py",
    "gen_tier_k_toe_gap_closure_lean.py",
    "gen_tier_l_orbital_gap_fill_lean.py",
    "gen_tier_m_toe_unity_lean.py",
    "gen_tier_n_compactification_ladder_lean.py",
    "gen_time_emergence_lean.py",
    "gen_anomaly_observables_lean.py",
    "gen_stumped_observables_lean.py",
    "gen_fringe_tier51_lean.py",
    "gen_tier52_astrophysical_lean.py",
    "gen_tiers_53_56_lean.py",
    "gen_tiers_57_58_lean.py",
    "gen_tiers_59_60_lean.py",
    "gen_tiers_61_lean.py",
    "gen_tiers_62_64_lean.py",
    "gen_tiers_65_lean.py",
    "gen_tiers_66_lean.py",
    "gen_tiers_67_lean.py",
    "gen_tiers_68_70_lean.py",
    "gen_tiers_71_lean.py",
    "gen_tiers_72_lean.py",
    "gen_tiers_73_lean.py",
]


def discover_generators() -> list[Path]:
    ordered = []
    seen: set[str] = set()
    for name in GENERATOR_ORDER:
        path = SCRIPTS / name
        if path.exists():
            ordered.append(path)
            seen.add(name)
    for path in sorted(SCRIPTS.glob("gen_*_lean.py")):
        if path.name not in seen:
            ordered.append(path)
    return ordered


def run_generator(path: Path, *, dry_run: bool) -> tuple[bool, str]:
    cmd = [sys.executable, str(path)]
    if dry_run:
        return True, "dry-run"
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out.strip()[-500:] if out else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate all Lean priors from benchmarks")
    parser.add_argument("--dry-run", action="store_true", help="List generators only")
    parser.add_argument("--only", action="append", help="Run matching generator filename(s)")
    args = parser.parse_args()

    generators = discover_generators()
    if args.only:
        only = set(args.only)
        generators = [g for g in generators if g.name in only]

    print(f"Lean rebuild: {len(generators)} generator(s)")
    failed: list[str] = []
    for path in generators:
        ok, tail = run_generator(path, dry_run=args.dry_run)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {path.name}")
        if not ok:
            failed.append(path.name)
            if tail:
                print(f"    {tail}", file=sys.stderr)

    if failed:
        print(f"\nFailed generators: {failed}", file=sys.stderr)
        return 1
    print("\nAll Lean generators completed.")
    print("Next: lake build && python scripts/export_certificate.py --lean-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())