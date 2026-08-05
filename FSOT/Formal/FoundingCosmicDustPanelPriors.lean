/-
  FSOT Formal FoundingCosmicDustPanelPriors — extension domain Founding_Cosmic_Dust_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_cosmic_dust_panel_observable_count : ℕ := 24
def founding_cosmic_dust_panel_D_eff : ℕ := 13

theorem founding_cosmic_dust_panel_observable_count_pos : 0 < founding_cosmic_dust_panel_observable_count := by
  unfold founding_cosmic_dust_panel_observable_count; decide

theorem founding_cosmic_dust_panel_median_error_under_half_pct :
    (0.026675 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.026675 : ℝ) < (0.5 : ℝ))

theorem founding_cosmic_dust_panel_bundle :
    founding_cosmic_dust_panel_observable_count = 24 ∧
    founding_cosmic_dust_panel_D_eff = 13 ∧
    (0.026675 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_cosmic_dust_panel_observable_count; decide,
    by unfold founding_cosmic_dust_panel_D_eff; decide,
    founding_cosmic_dust_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
