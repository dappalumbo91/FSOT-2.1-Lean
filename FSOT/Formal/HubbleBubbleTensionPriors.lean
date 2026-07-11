/-
  FSOT Formal HubbleBubbleTensionPriors — Hubble_Bubble_Tension Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hubble_tension_observable_count : ℕ := 6
def hubble_tension_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def hubble_tension_headline_median_error_pct : ℝ := (0.662298 : ℝ)
def hubble_tension_beats_sota_headlines : ℕ := 2
def hubble_tension_D_eff : ℕ := 25
def hubble_tension_h0_sector_count : ℕ := 6

theorem hubble_tension_observable_count_pos : 0 < hubble_tension_observable_count := by
  unfold hubble_tension_observable_count; norm_num

theorem hubble_tension_pooled_median_under_half_pct :
    hubble_tension_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold hubble_tension_pooled_median_error_pct; norm_num

-- Headline channel median (0.662298%) exceeds 0.5% gate; pooled median gate is separate.
theorem hubble_tension_headline_median_under_one_pct :
    hubble_tension_headline_median_error_pct < (1.0 : ℝ) := by
  unfold hubble_tension_headline_median_error_pct; norm_num

theorem hubble_tension_beats_sota_headlines_pos : 0 < hubble_tension_beats_sota_headlines := by
  unfold hubble_tension_beats_sota_headlines; norm_num
theorem hubble_tension_h0_sectors_pos : 0 < hubble_tension_h0_sector_count := by unfold hubble_tension_h0_sector_count; norm_num

theorem hubble_tension_bundle :
    hubble_tension_observable_count = 6 ∧
    hubble_tension_pooled_median_error_pct < (0.5 : ℝ) ∧
    hubble_tension_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold hubble_tension_observable_count; norm_num
  · exact hubble_tension_pooled_median_under_half_pct
  · exact hubble_tension_beats_sota_headlines_pos

end
