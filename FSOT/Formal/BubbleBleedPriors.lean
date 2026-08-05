/-
  FSOT Formal BubbleBleedPriors — BH→WH outgassing bubble bleed lab.
  Nebula framework fit, WH closure/suction, BH spin, FRB classifier, sector H₀.
  Generator: scripts/gen_bubble_bleed_priors_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def bubble_bleed_nebula_count : ℕ := 20
def bubble_bleed_frb_count : ℕ := 38
def bubble_bleed_h0_sector_count : ℕ := 6
def bubble_bleed_framework_count : ℕ := 20
def bubble_bleed_wh_closure_count : ℕ := 20
def bubble_bleed_bh_spin_count : ℕ := 5
def bubble_bleed_frb_p34_count : ℕ := 4
def bubble_bleed_observable_count : ℕ := 113
def bubble_bleed_nebula_match_count : ℕ := 20
def bubble_bleed_framework_fit_count : ℕ := 20
def bubble_bleed_wh_closure_match_count : ℕ := 20
def bubble_bleed_bh_spin_match_count : ℕ := 5
def bubble_bleed_frb_match_count : ℕ := 38
def bubble_bleed_fraction : ℝ := (0.015431 : ℝ)
def bubble_bleed_observability_ratio : ℝ := (0.7142857142857143 : ℝ)
def bubble_bleed_nebula_match_rate : ℝ := (1.0 : ℝ)
def bubble_bleed_framework_fit_rate : ℝ := (1.0 : ℝ)
def bubble_bleed_wh_closure_match_rate : ℝ := (1.0 : ℝ)
def bubble_bleed_bh_spin_match_rate : ℝ := (1.0 : ℝ)
def bubble_bleed_frb_match_rate : ℝ := (1.0 : ℝ)
def bubble_bleed_frb_fp_rate : ℝ := (0.0 : ℝ)

theorem bubble_bleed_nebula_count_pos : 0 < bubble_bleed_nebula_count := by
  unfold bubble_bleed_nebula_count; decide

theorem bubble_bleed_frb_count_pos : 0 < bubble_bleed_frb_count := by
  unfold bubble_bleed_frb_count; decide

theorem bubble_bleed_observable_count_pos : 0 < bubble_bleed_observable_count := by
  unfold bubble_bleed_observable_count; decide

theorem bubble_bleed_framework_fit_le_total :
    bubble_bleed_framework_fit_count ≤ bubble_bleed_framework_count := by
  unfold bubble_bleed_framework_fit_count bubble_bleed_framework_count; decide

theorem bubble_bleed_wh_closure_match_le_total :
    bubble_bleed_wh_closure_match_count ≤ bubble_bleed_wh_closure_count := by
  unfold bubble_bleed_wh_closure_match_count bubble_bleed_wh_closure_count; decide

theorem bubble_bleed_bh_spin_match_le_total :
    bubble_bleed_bh_spin_match_count ≤ bubble_bleed_bh_spin_count := by
  unfold bubble_bleed_bh_spin_match_count bubble_bleed_bh_spin_count; decide

theorem bubble_bleed_nebula_match_le_total :
    bubble_bleed_nebula_match_count ≤ bubble_bleed_nebula_count := by
  unfold bubble_bleed_nebula_match_count bubble_bleed_nebula_count; decide

theorem bubble_bleed_frb_match_le_total :
    bubble_bleed_frb_match_count ≤ bubble_bleed_frb_count := by
  unfold bubble_bleed_frb_match_count bubble_bleed_frb_count; decide

theorem bubble_bleed_observability_ratio_nonneg :
    0 ≤ bubble_bleed_observability_ratio := by
  unfold bubble_bleed_observability_ratio
  exact (by norm_num : (0 : ℝ) ≤ (0.7142857142857143  : ℝ))

/-- Bundle: BH→WH mechanics — framework fit, WH closure, spin, FRB, sector H₀ bleed. -/
theorem bubble_bleed_bundle :
    bubble_bleed_nebula_count = 20 ∧
    bubble_bleed_frb_count = 38 ∧
    bubble_bleed_h0_sector_count = 6 ∧
    bubble_bleed_framework_count = 20 ∧
    bubble_bleed_wh_closure_count = 20 ∧
    bubble_bleed_bh_spin_count = 5 ∧
    bubble_bleed_observable_count = 113 ∧
    bubble_bleed_framework_fit_count ≤ bubble_bleed_framework_count ∧
    bubble_bleed_wh_closure_match_count ≤ bubble_bleed_wh_closure_count ∧
    bubble_bleed_bh_spin_match_count ≤ bubble_bleed_bh_spin_count ∧
    bubble_bleed_nebula_match_count ≤ bubble_bleed_nebula_count ∧
    bubble_bleed_frb_match_count ≤ bubble_bleed_frb_count ∧
    0 ≤ bubble_bleed_observability_ratio ∧
    |h0_fsot S_cosm_cached - h0_fsot_canonical| < (0.11 : ℝ) := by
  refine ⟨
    by unfold bubble_bleed_nebula_count; decide,
    by unfold bubble_bleed_frb_count; decide,
    by unfold bubble_bleed_h0_sector_count; decide,
    by unfold bubble_bleed_framework_count; decide,
    by unfold bubble_bleed_wh_closure_count; decide,
    by unfold bubble_bleed_bh_spin_count; decide,
    by unfold bubble_bleed_observable_count; decide,
    bubble_bleed_framework_fit_le_total,
    bubble_bleed_wh_closure_match_le_total,
    bubble_bleed_bh_spin_match_le_total,
    bubble_bleed_nebula_match_le_total,
    bubble_bleed_frb_match_le_total,
    bubble_bleed_observability_ratio_nonneg,
    h0_fsot_cached_approx_value
  ⟩

end

end FSOT.Formal
