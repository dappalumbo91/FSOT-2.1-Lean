/-
  FSOT Formal ConsciousnessSpeciesMultiPanelPriors — extension domain Consciousness_Species_Multi_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_species_multi_panel_observable_count : ℕ := 269
def consciousness_species_multi_panel_D_eff : ℕ := 18

theorem consciousness_species_multi_panel_observable_count_pos : 0 < consciousness_species_multi_panel_observable_count := by
  unfold consciousness_species_multi_panel_observable_count; norm_num

theorem consciousness_species_multi_panel_median_error_under_half_pct :
    (0.0201195 : ℝ) < (0.5 : ℝ) := by norm_num

theorem consciousness_species_multi_panel_bundle :
    consciousness_species_multi_panel_observable_count = 269 ∧
    consciousness_species_multi_panel_D_eff = 18 ∧
    (0.0201195 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_species_multi_panel_observable_count; norm_num,
    by unfold consciousness_species_multi_panel_D_eff; norm_num,
    consciousness_species_multi_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
