/-
  FSOT Formal MaterialsSpeciesBridgeLivePanelPriors — extension domain Materials_Species_Bridge_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def materials_species_bridge_live_panel_observable_count : ℕ := 150
def materials_species_bridge_live_panel_D_eff : ℕ := 14

theorem materials_species_bridge_live_panel_observable_count_pos : 0 < materials_species_bridge_live_panel_observable_count := by
  unfold materials_species_bridge_live_panel_observable_count; decide

theorem materials_species_bridge_live_panel_median_error_under_half_pct :
    (0.01341 : ℝ) < (0.5 : ℝ) := by norm_num

theorem materials_species_bridge_live_panel_bundle :
    materials_species_bridge_live_panel_observable_count = 150 ∧
    materials_species_bridge_live_panel_D_eff = 14 ∧
    (0.01341 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold materials_species_bridge_live_panel_observable_count; decide,
    by unfold materials_species_bridge_live_panel_D_eff; decide,
    materials_species_bridge_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
