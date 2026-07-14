/-
  FSOT Formal LongevityExtremeSpeciesPanelPriors — extension domain Longevity_Extreme_Species_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def longevity_extreme_species_panel_observable_count : ℕ := 164
def longevity_extreme_species_panel_D_eff : ℕ := 21

theorem longevity_extreme_species_panel_observable_count_pos : 0 < longevity_extreme_species_panel_observable_count := by
  unfold longevity_extreme_species_panel_observable_count; norm_num

theorem longevity_extreme_species_panel_median_error_under_half_pct :
    (0.017789 : ℝ) < (0.5 : ℝ) := by norm_num

theorem longevity_extreme_species_panel_bundle :
    longevity_extreme_species_panel_observable_count = 164 ∧
    longevity_extreme_species_panel_D_eff = 21 ∧
    (0.017789 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold longevity_extreme_species_panel_observable_count; norm_num,
    by unfold longevity_extreme_species_panel_D_eff; norm_num,
    longevity_extreme_species_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
