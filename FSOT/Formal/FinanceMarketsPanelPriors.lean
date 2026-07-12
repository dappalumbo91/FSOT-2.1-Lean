/-
  FSOT Formal FinanceMarketsPanelPriors — Tier 85 scientific expansion (Finance_Markets_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def finance_markets_panel_observable_count : ℕ := 25
def finance_markets_panel_median_error_pct : ℝ := (0.02584 : ℝ)
def finance_markets_panel_D_eff : ℕ := 19

theorem finance_markets_panel_observable_count_pos : 0 < finance_markets_panel_observable_count := by
  unfold finance_markets_panel_observable_count; norm_num

theorem finance_markets_panel_median_error_under_five_pct :
    finance_markets_panel_median_error_pct < (5 : ℝ) := by
  unfold finance_markets_panel_median_error_pct; norm_num

theorem finance_markets_panel_bundle :
    finance_markets_panel_observable_count = 25 ∧
    finance_markets_panel_D_eff = 19 ∧
    finance_markets_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold finance_markets_panel_observable_count; norm_num,
    by unfold finance_markets_panel_D_eff; norm_num,
    finance_markets_panel_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
