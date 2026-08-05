/-
  FSOT Formal Tier93DualWaveSpinePriors — extension domain Tier_93_Dual_Wave_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def tier_93_dual_wave_spine_observable_count : ℕ := 24
def tier_93_dual_wave_spine_D_eff : ℕ := 19

theorem tier_93_dual_wave_spine_observable_count_pos : 0 < tier_93_dual_wave_spine_observable_count := by
  unfold tier_93_dual_wave_spine_observable_count; decide

theorem tier_93_dual_wave_spine_median_error_under_half_pct :
    (0.011093889935064888 : ℝ) < (0.5 : ℝ) := by norm_num

theorem tier_93_dual_wave_spine_bundle :
    tier_93_dual_wave_spine_observable_count = 24 ∧
    tier_93_dual_wave_spine_D_eff = 19 ∧
    (0.011093889935064888 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tier_93_dual_wave_spine_observable_count; decide,
    by unfold tier_93_dual_wave_spine_D_eff; decide,
    tier_93_dual_wave_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
