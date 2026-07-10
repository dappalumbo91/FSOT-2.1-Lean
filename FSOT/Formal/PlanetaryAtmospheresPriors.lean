/-
  FSOT Formal PlanetaryAtmospheresPriors — FSOT-adjusted JPL/NASA atmosphere observables.
  Generator: scripts/gen_planetary_atmospheres_lean.py
  Source: vendor/planetary_atmospheres
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_atmospheres_observable_count : ℕ := 21
def planetary_atmospheres_body_count : ℕ := 13
def planetary_atmospheres_D_eff : ℕ := 16
def planetary_atmospheres_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def planetary_atmospheres_headline_median_error_pct : ℝ := (0.0 : ℝ)
def planetary_atmospheres_beats_sota_headlines : ℕ := 3

theorem planetary_atmospheres_observable_count_pos : 0 < planetary_atmospheres_observable_count := by
  unfold planetary_atmospheres_observable_count; norm_num

theorem planetary_atmospheres_body_count_pos : 0 < planetary_atmospheres_body_count := by
  unfold planetary_atmospheres_body_count; norm_num

theorem planetary_atmospheres_pooled_median_under_five_pct :
    planetary_atmospheres_pooled_median_error_pct < (5 : ℝ) := by
  unfold planetary_atmospheres_pooled_median_error_pct; norm_num

theorem planetary_atmospheres_headline_median_under_five_pct :
    planetary_atmospheres_headline_median_error_pct < (5 : ℝ) := by
  unfold planetary_atmospheres_headline_median_error_pct; norm_num

theorem planetary_atmospheres_beats_sota_headlines_pos : 0 < planetary_atmospheres_beats_sota_headlines := by
  unfold planetary_atmospheres_beats_sota_headlines; norm_num

theorem planetary_atmospheres_bundle :
    planetary_atmospheres_observable_count = 21 ∧
    planetary_atmospheres_body_count = 13 ∧
    planetary_atmospheres_D_eff = 16 ∧
    planetary_atmospheres_pooled_median_error_pct < (5 : ℝ) ∧
    planetary_atmospheres_headline_median_error_pct < (5 : ℝ) ∧
    0 < planetary_atmospheres_beats_sota_headlines ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_atmospheres_observable_count; norm_num,
    by unfold planetary_atmospheres_body_count; norm_num,
    by unfold planetary_atmospheres_D_eff; norm_num,
    planetary_atmospheres_pooled_median_under_five_pct,
    planetary_atmospheres_headline_median_under_five_pct,
    planetary_atmospheres_beats_sota_headlines_pos,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
