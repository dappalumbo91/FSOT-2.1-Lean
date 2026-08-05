/-
  FSOT Formal MpcorbMinorPlanetCatalogPriors — IAU MPCORB full-catalog residual gates.
  Generator: scripts/gen_mpcorb_minor_planet_catalog_lean.py
  Refinement: docs/MPCORB_REFINEMENT_PROCESS.md
  Prediction law: measured * (1 + |S(domain)| * factor) at D_eff interfaces.
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mpcorb_object_count : ℕ := 1554101
def mpcorb_D_eff : ℕ := 21
def mpcorb_pooled_median_error_pct : ℝ := (0.023015 : ℝ)
def mpcorb_kepler_median_error_pct : ℝ := (1.5875572596619725e-06 : ℝ)
def mpcorb_green_gate_flag : ℕ := 1

theorem mpcorb_object_count_pos : 0 < mpcorb_object_count := by
  unfold mpcorb_object_count; decide

theorem mpcorb_pooled_median_under_half_pct :
    mpcorb_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold mpcorb_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem mpcorb_pooled_median_under_tier_aspiration :
    mpcorb_pooled_median_error_pct < (0.05 : ℝ) := by
  unfold mpcorb_pooled_median_error_pct; norm_num

theorem mpcorb_kepler_integrity_under_ppm :
    mpcorb_kepler_median_error_pct < (0.001 : ℝ) := by
  unfold mpcorb_kepler_median_error_pct; norm_num

theorem mpcorb_green_gate_pass : mpcorb_green_gate_flag = 1 := by
  unfold mpcorb_green_gate_flag; rfl

theorem mpcorb_minor_planet_catalog_bundle :
    mpcorb_object_count = 1554101 ∧
    mpcorb_D_eff = 21 ∧
    mpcorb_pooled_median_error_pct < (0.5 : ℝ) ∧
    mpcorb_pooled_median_error_pct < (0.05 : ℝ) ∧
    mpcorb_kepler_median_error_pct < (0.001 : ℝ) ∧
    mpcorb_green_gate_flag = 1 ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold mpcorb_object_count; decide,
    by unfold mpcorb_D_eff; decide,
    mpcorb_pooled_median_under_half_pct,
    mpcorb_pooled_median_under_tier_aspiration,
    mpcorb_kepler_integrity_under_ppm,
    mpcorb_green_gate_pass,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
