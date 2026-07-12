/-
  FSOT Formal MaterialsSpeciesBridgeLivePanelPriors — Tier 86 scientific expansion (Materials_Species_Bridge_Live_Panel).
  Generator: scripts/gen_tier86_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_species_bridge_live_observable_count : ℕ := 150
def materials_species_bridge_live_median_error_pct : ℝ := (0.01341 : ℝ)
def materials_species_bridge_live_D_eff : ℕ := 14

theorem materials_species_bridge_live_observable_count_pos : 0 < materials_species_bridge_live_observable_count := by
  unfold materials_species_bridge_live_observable_count; norm_num

theorem materials_species_bridge_live_median_error_under_five_pct :
    materials_species_bridge_live_median_error_pct < (5 : ℝ) := by
  unfold materials_species_bridge_live_median_error_pct; norm_num

theorem materials_species_bridge_live_bundle :
    materials_species_bridge_live_observable_count = 150 ∧
    materials_species_bridge_live_D_eff = 14 ∧
    materials_species_bridge_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold materials_species_bridge_live_observable_count; norm_num,
    by unfold materials_species_bridge_live_D_eff; norm_num,
    materials_species_bridge_live_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
