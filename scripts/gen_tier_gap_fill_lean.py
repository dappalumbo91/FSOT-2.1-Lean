#!/usr/bin/env python3
"""Generate Lean priors for tier gap-fill neurolab domains."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402
from tier_gap_fill_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Ecology": ("ecology_gap_fill", "biological", "biological_raw_S_positive", "EcologyGapFillPriors"),
    "Economics": ("economics_gap_fill", "consciousness", "consciousness_raw_S_positive", "EconomicsGapFillPriors"),
    "Psychology": ("psychology_gap_fill", "consciousness", "consciousness_raw_S_positive", "PsychologyGapFillPriors"),
    "Sociology": ("sociology_gap_fill", "consciousness", "consciousness_raw_S_positive", "SociologyGapFillPriors"),
    "Oceanography": ("oceanography_gap_fill", "energy", "energy_raw_S_positive", "OceanographyGapFillPriors"),
    "Meteorology": ("meteorology_gap_fill", "energy", "energy_raw_S_positive", "MeteorologyGapFillPriors"),
    "Atmospheric_Physics": ("atmospheric_physics_gap_fill", "energy", "energy_raw_S_positive", "AtmosphericPhysicsGapFillPriors"),
    "Fluid_Dynamics": ("fluid_dynamics_gap_fill", "energy", "energy_raw_S_positive", "FluidDynamicsGapFillPriors"),
    "Atomic_Physics": ("atomic_physics_gap_fill", "particle", "particle_raw_S_positive", "AtomicPhysicsGapFillPriors"),
    "Quantum_Mechanics": ("quantum_mechanics_gap_fill", "quantum", "quantum_raw_S_positive", "QuantumMechanicsGapFillPriors"),
    "Quantum_Optics": ("quantum_optics_gap_fill", "quantum", "quantum_raw_S_positive", "QuantumOpticsGapFillPriors"),
    "Quantum_Computing": ("quantum_computing_gap_fill", "particle", "particle_raw_S_positive", "QuantumComputingGapFillPriors"),
    "Particle_Physics": ("particle_physics_gap_fill", "particle", "particle_raw_S_positive", "ParticlePhysicsGapFillPriors"),
    "Pharmacokinetics": ("pharmacokinetics_gap_fill", "medical", "medical_raw_S_positive", "PharmacokineticsGapFillPriors"),
    "Food_Microbiology": ("food_microbiology_gap_fill", "biological", "biological_raw_S_positive", "FoodMicrobiologyGapFillPriors"),
    "Agriculture_Agroecology": ("agriculture_agroecology_gap_fill", "biological", "biological_raw_S_positive", "AgricultureAgroecologyGapFillPriors"),
    "Maillard_Chemistry": ("maillard_chemistry_gap_fill", "energy", "energy_raw_S_positive", "MaillardChemistryGapFillPriors"),
    "Econometrics": ("econometrics_gap_fill", "consciousness", "consciousness_raw_S_positive", "EconometricsGapFillPriors"),
    "Sports_Biomechanics": ("sports_biomechanics_gap_fill", "biological", "biological_raw_S_positive", "SportsBiomechanicsGapFillPriors"),
    "Architecture_Building_Science": ("architecture_building_science_gap_fill", "energy", "energy_raw_S_positive", "ArchitectureBuildingScienceGapFillPriors"),
}


def _slug(domain: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", domain.lower()).strip("_")


def build_lean(bench: dict, domain: str) -> str:
    prefix, lean_domain, sign, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    return f"""/-
  FSOT Formal {module_stem} — {domain} tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 14))}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) ∧
    {prefix}_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < {prefix}_beats_sota_headlines ∧
    raw_S (get_domain_params "{lean_domain}") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    {prefix}_pooled_median_under_half_pct,
    {prefix}_headline_median_under_half_pct,
    {prefix}_beats_sota_headlines_pos,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(BUILDERS.keys())
    for domain in domains:
        if domain not in LEAN_MAP:
            continue
        bench_path = output_path(domain)
        if not bench_path.exists():
            bench_path.write_text(json.dumps(BUILDERS[domain](), indent=2), encoding="utf-8")
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        module_stem = LEAN_MAP[domain][3]
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(build_lean(bench, domain), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())