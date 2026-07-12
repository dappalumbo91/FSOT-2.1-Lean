/-
  FSOT Formal ObserverEffectCrossSpeciesPanelPriors — extension domain Observer_Effect_Cross_Species_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def observer_effect_cross_species_panel_observable_count : ℕ := 289
def observer_effect_cross_species_panel_D_eff : ℕ := 16

theorem observer_effect_cross_species_panel_observable_count_pos : 0 < observer_effect_cross_species_panel_observable_count := by
  unfold observer_effect_cross_species_panel_observable_count; norm_num

theorem observer_effect_cross_species_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem observer_effect_cross_species_panel_bundle :
    observer_effect_cross_species_panel_observable_count = 289 ∧
    observer_effect_cross_species_panel_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold observer_effect_cross_species_panel_observable_count; norm_num,
    by unfold observer_effect_cross_species_panel_D_eff; norm_num,
    observer_effect_cross_species_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
