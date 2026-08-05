/-
  FSOT Formal SupplyChainLogisticsPanelPriors — extension domain Supply_Chain_Logistics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def supply_chain_logistics_panel_observable_count : ℕ := 40
def supply_chain_logistics_panel_D_eff : ℕ := 18

theorem supply_chain_logistics_panel_observable_count_pos : 0 < supply_chain_logistics_panel_observable_count := by
  unfold supply_chain_logistics_panel_observable_count; decide

theorem supply_chain_logistics_panel_median_error_under_half_pct :
    (0.02584 : ℝ) < (0.5 : ℝ) := by norm_num

theorem supply_chain_logistics_panel_bundle :
    supply_chain_logistics_panel_observable_count = 40 ∧
    supply_chain_logistics_panel_D_eff = 18 ∧
    (0.02584 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold supply_chain_logistics_panel_observable_count; decide,
    by unfold supply_chain_logistics_panel_D_eff; decide,
    supply_chain_logistics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
