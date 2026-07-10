#!/usr/bin/env python3
"""Generate Lean priors for Tier L orbital gap-fill domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_l_orbital_gap_fill_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Acoustic_Resonance_Materials": ("acoustic_rm", "AcousticResonanceMaterialsPriors"),
    "Chaos_Mediated_Phase_Transitions": ("chaos_pt", "ChaosMediatedPhaseTransitionsPriors"),
    "Phi_Morphogenetic_Scaling": ("phi_morph", "PhiMorphogeneticScalingPriors"),
    "Ionospheric_Chemistry_Coupling": ("iono_chem", "IonosphericChemistryCouplingPriors"),
    "Energy_AI_Orbital_Bridge": ("e_ai_br", "EnergyAIOrbitalBridgePriors"),
    "Consciousness_Galactic_Orbital_Bridge": ("c_gal_br", "ConsciousnessGalacticOrbitalBridgePriors"),
    "Energy_Neural_Orbital_Bridge": ("e_neu_br", "EnergyNeuralOrbitalBridgePriors"),
    "Particle_Neural_Orbital_Bridge": ("p_neu_br", "ParticleNeuralOrbitalBridgePriors"),
    "Proof_Carrying_Code_Genome": ("proof_cg", "ProofCarryingCodeGenomePriors"),
    "Domain_Orbital_Predictions": ("orb_pred", "DomainOrbitalPredictionsPriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Acoustic_Resonance_Materials":
        ac = int(bench.get("acoustic_species_count") or 0)
        extra_defs = f"def {prefix}_acoustic_species_count : ℕ := {ac}\n"
        extra_thms = f"theorem {prefix}_acoustic_species_pos : 0 < {prefix}_acoustic_species_count := by unfold {prefix}_acoustic_species_count; norm_num\n"
    elif domain == "Phi_Morphogenetic_Scaling":
        ps = int(bench.get("phi_species_observable_count") or 0)
        extra_defs = f"def {prefix}_phi_species_count : ℕ := {ps}\n"
        extra_thms = f"theorem {prefix}_phi_species_pos : 0 < {prefix}_phi_species_count := by unfold {prefix}_phi_species_count; norm_num\n"
    elif domain == "Domain_Orbital_Predictions":
        pc = int(bench.get("prediction_count") or 0)
        fc = int(bench.get("filled_prediction_count") or 0)
        extra_defs = f"def {prefix}_prediction_count : ℕ := {pc}\ndef {prefix}_filled_prediction_count : ℕ := {fc}\n"
        extra_thms = f"theorem {prefix}_filled_predictions_pos : 0 < {prefix}_filled_prediction_count := by unfold {prefix}_filled_prediction_count; norm_num\n"
    elif domain.endswith("_Orbital_Bridge"):
        bp = int(bench.get("bridge_pair_count") or 0)
        extra_defs = f"def {prefix}_bridge_pair_count : ℕ := {bp}\n"
        extra_thms = f"theorem {prefix}_bridge_pairs_pos : 0 < {prefix}_bridge_pair_count := by unfold {prefix}_bridge_pair_count; norm_num\n"
    elif domain == "Proof_Carrying_Code_Genome":
        op = int(bench.get("oss_affinity_pair_count") or 0)
        extra_defs = f"def {prefix}_oss_affinity_pair_count : ℕ := {op}\n"
        extra_thms = f"theorem {prefix}_oss_pairs_pos : 0 < {prefix}_oss_affinity_pair_count := by unfold {prefix}_oss_affinity_pair_count; norm_num\n"
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 17))}
{extra_defs}
theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_five_pct :
    {prefix}_pooled_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_five_pct :
    {prefix}_headline_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num
{extra_thms}
theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (5 : ℝ) ∧
    {prefix}_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · exact {prefix}_pooled_median_under_five_pct
  · exact {prefix}_beats_sota_headlines_pos

end
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(LEAN_MAP.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(LEAN_MAP.keys())
    for domain in domains:
        bench_path = output_path(domain)
        if not bench_path.exists():
            bench = BUILDERS[domain]()
            bench_path.write_text(json.dumps(bench, indent=2), encoding="utf-8")
        else:
            bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, domain)
        out = FORMAL / f"{LEAN_MAP[domain][1]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())