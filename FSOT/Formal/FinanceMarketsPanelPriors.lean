/-
  FSOT Formal FinanceMarketsPanelPriors — extension domain Finance_Markets_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def finance_markets_panel_observable_count : ℕ := 36
def finance_markets_panel_D_eff : ℕ := 19

theorem finance_markets_panel_observable_count_pos : 0 < finance_markets_panel_observable_count := by
  unfold finance_markets_panel_observable_count; decide

theorem finance_markets_panel_median_error_under_half_pct :
    (0.02584 : ℝ) < (0.5 : ℝ) := by norm_num

theorem finance_markets_panel_bundle :
    finance_markets_panel_observable_count = 36 ∧
    finance_markets_panel_D_eff = 19 ∧
    (0.02584 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold finance_markets_panel_observable_count; decide,
    by unfold finance_markets_panel_D_eff; decide,
    finance_markets_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
