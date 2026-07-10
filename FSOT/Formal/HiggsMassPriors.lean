/-
  FSOT Formal HiggsMassPriors — Higgs boson mass from FO-213 SMILES intrinsic.
  Generator: scripts/gen_higgs_mass_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def higgs_mass_rule_id : String := "FO-213"
def higgs_mass_observable_count : ℕ := 2
def higgs_mass_median_error_pct : ℝ := (0.03990518384182655 : ℝ)
def higgs_mass_computed_gev : ℝ := (125.20001875723811 : ℝ)

theorem higgs_mass_observable_count_pos : 0 < higgs_mass_observable_count := by
  unfold higgs_mass_observable_count; norm_num

theorem higgs_mass_median_error_under_half_pct :
    higgs_mass_median_error_pct < (0.5 : ℝ) := by
  unfold higgs_mass_median_error_pct; norm_num

theorem higgs_mass_computed_positive : 0 < higgs_mass_computed_gev := by
  unfold higgs_mass_computed_gev; norm_num

/-- Bundle: FO-213 Higgs mass with particle-domain sign proxy. -/
theorem higgs_mass_bundle :
    higgs_mass_observable_count = 2 ∧
    higgs_mass_median_error_pct < (0.5 : ℝ) ∧
    0 < higgs_mass_computed_gev ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold higgs_mass_observable_count; norm_num,
    higgs_mass_median_error_under_half_pct,
    higgs_mass_computed_positive,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
