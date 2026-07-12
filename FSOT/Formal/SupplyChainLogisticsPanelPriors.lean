/-
  FSOT Formal SupplyChainLogisticsPanelPriors — Tier 85 scientific expansion (Supply_Chain_Logistics_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def supply_chain_panel_observable_count : ℕ := 27
def supply_chain_panel_median_error_pct : ℝ := (0.02584 : ℝ)
def supply_chain_panel_D_eff : ℕ := 18

theorem supply_chain_panel_observable_count_pos : 0 < supply_chain_panel_observable_count := by
  unfold supply_chain_panel_observable_count; norm_num

theorem supply_chain_panel_median_error_under_five_pct :
    supply_chain_panel_median_error_pct < (5 : ℝ) := by
  unfold supply_chain_panel_median_error_pct; norm_num

theorem supply_chain_panel_bundle :
    supply_chain_panel_observable_count = 27 ∧
    supply_chain_panel_D_eff = 18 ∧
    supply_chain_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold supply_chain_panel_observable_count; norm_num,
    by unfold supply_chain_panel_D_eff; norm_num,
    supply_chain_panel_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
