/-
  FSOT Formal NeuroimmunologyPriors — immunology SMILES + neuron cohort strata.
  Generator: scripts/gen_neuroimmunology_lean.py
  Source: vendor/neuroimmunology
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroimmunology_observable_count : ℕ := 92
def neuroimmunology_section_count : ℕ := 7
def neuroimmunology_D_eff : ℕ := 14
def neuroimmunology_pooled_median_error_pct : ℝ := (0.05041956982053305 : ℝ)
def neuroimmunology_headline_median_error_pct : ℝ := (0.060502 : ℝ)
def neuroimmunology_beats_sota_headlines : ℕ := 6

theorem neuroimmunology_observable_count_pos : 0 < neuroimmunology_observable_count := by
  unfold neuroimmunology_observable_count; decide

theorem neuroimmunology_section_count_pos : 0 < neuroimmunology_section_count := by
  unfold neuroimmunology_section_count; decide

theorem neuroimmunology_pooled_median_under_half_pct :
    neuroimmunology_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold neuroimmunology_pooled_median_error_pct
  exact (by norm_num : (0.05041956982053305  : ℝ) < 0.5)

theorem neuroimmunology_headline_median_under_half_pct :
    neuroimmunology_headline_median_error_pct < (0.5 : ℝ) := by
  unfold neuroimmunology_headline_median_error_pct
  exact (by norm_num : (0.060502  : ℝ) < 0.5)

theorem neuroimmunology_beats_sota_headlines_pos : 0 < neuroimmunology_beats_sota_headlines := by
  unfold neuroimmunology_beats_sota_headlines; decide

theorem neuroimmunology_bundle :
    neuroimmunology_observable_count = 92 ∧
    neuroimmunology_section_count = 7 ∧
    neuroimmunology_D_eff = 14 ∧
    neuroimmunology_pooled_median_error_pct < (0.5 : ℝ) ∧
    neuroimmunology_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < neuroimmunology_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold neuroimmunology_observable_count; decide,
    by unfold neuroimmunology_section_count; decide,
    by unfold neuroimmunology_D_eff; decide,
    neuroimmunology_pooled_median_under_half_pct,
    neuroimmunology_headline_median_under_half_pct,
    neuroimmunology_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
