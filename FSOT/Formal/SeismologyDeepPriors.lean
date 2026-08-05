/-
  FSOT Formal SeismologyDeepPriors — moment-tensor + plate-margin deep classifier.
  Generator: scripts/gen_seismology_deep_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def seismology_deep_observable_count : ℕ := 1000
def seismology_deep_match_count : ℕ := 1000
def seismology_deep_holdout_count : ℕ := 189
def seismology_deep_holdout_match_count : ℕ := 189
def seismology_deep_D_eff : ℕ := 18
def seismology_deep_match_rate : ℝ := (1.0 : ℝ)

theorem seismology_deep_observable_count_pos : 0 < seismology_deep_observable_count := by
  unfold seismology_deep_observable_count; decide

theorem seismology_deep_match_le_total : seismology_deep_match_count ≤ seismology_deep_observable_count := by
  unfold seismology_deep_match_count seismology_deep_observable_count; norm_num

theorem seismology_deep_holdout_match_le_total :
    seismology_deep_holdout_match_count ≤ seismology_deep_holdout_count := by
  unfold seismology_deep_holdout_match_count seismology_deep_holdout_count; norm_num

theorem seismology_deep_bundle :
    seismology_deep_observable_count = 1000 ∧
    seismology_deep_match_count = 1000 ∧
    seismology_deep_holdout_count = 189 ∧
    seismology_deep_holdout_match_count = 189 ∧
    seismology_deep_D_eff = 18 ∧
    seismology_deep_match_count ≤ seismology_deep_observable_count ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold seismology_deep_observable_count; decide,
    by unfold seismology_deep_match_count; decide,
    by unfold seismology_deep_holdout_count; decide,
    by unfold seismology_deep_holdout_match_count; decide,
    by unfold seismology_deep_D_eff; decide,
    seismology_deep_match_le_total,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
