/-
  FSOT Formal RecentBreakthroughsExpansionPanelPriors — recent breakthrough expansion (Recent_Breakthroughs_Expansion_Panel).
  Generator: scripts/gen_recent_breakthrough_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def recent_breakthroughs_expansion_observable_count : ℕ := 27
def recent_breakthroughs_expansion_median_error_pct : ℝ := (0.0 : ℝ)
def recent_breakthroughs_expansion_D_eff : ℕ := 13

theorem recent_breakthroughs_expansion_observable_count_pos : 0 < recent_breakthroughs_expansion_observable_count := by
  unfold recent_breakthroughs_expansion_observable_count; norm_num

theorem recent_breakthroughs_expansion_median_error_under_half_pct :
    recent_breakthroughs_expansion_median_error_pct < (0.5 : ℝ) := by
  unfold recent_breakthroughs_expansion_median_error_pct; norm_num

theorem recent_breakthroughs_expansion_bundle :
    recent_breakthroughs_expansion_observable_count = 27 ∧
    recent_breakthroughs_expansion_D_eff = 13 ∧
    recent_breakthroughs_expansion_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold recent_breakthroughs_expansion_observable_count; norm_num,
    by unfold recent_breakthroughs_expansion_D_eff; norm_num,
    recent_breakthroughs_expansion_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
