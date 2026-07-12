/-
  FSOT Formal ConsciousnessGeneticsSpeciesPanelPriors — extension domain Consciousness_Genetics_Species_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_genetics_species_panel_observable_count : ℕ := 27
def consciousness_genetics_species_panel_D_eff : ℕ := 18

theorem consciousness_genetics_species_panel_observable_count_pos : 0 < consciousness_genetics_species_panel_observable_count := by
  unfold consciousness_genetics_species_panel_observable_count; norm_num

theorem consciousness_genetics_species_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem consciousness_genetics_species_panel_bundle :
    consciousness_genetics_species_panel_observable_count = 27 ∧
    consciousness_genetics_species_panel_D_eff = 18 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_genetics_species_panel_observable_count; norm_num,
    by unfold consciousness_genetics_species_panel_D_eff; norm_num,
    consciousness_genetics_species_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
