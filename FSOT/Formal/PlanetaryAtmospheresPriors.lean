/-
  FSOT Formal PlanetaryAtmospheresPriors — Mars/Venus/Titan atmosphere observables.
  Generator: scripts/gen_planetary_atmospheres_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_atmospheres_observable_count : ℕ := 6
def planetary_atmospheres_D_eff : ℕ := 16
def planetary_atmospheres_median_error_pct : ℝ := (0.27137 : ℝ)

theorem planetary_atmospheres_observable_count_pos : 0 < planetary_atmospheres_observable_count := by
  unfold planetary_atmospheres_observable_count; norm_num

theorem planetary_atmospheres_median_error_under_five_pct :
    planetary_atmospheres_median_error_pct < (5 : ℝ) := by
  unfold planetary_atmospheres_median_error_pct; norm_num

theorem planetary_atmospheres_bundle :
    planetary_atmospheres_observable_count = 6 ∧
    planetary_atmospheres_D_eff = 16 ∧
    planetary_atmospheres_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_atmospheres_observable_count; norm_num,
    by unfold planetary_atmospheres_D_eff; norm_num,
    planetary_atmospheres_median_error_under_five_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
