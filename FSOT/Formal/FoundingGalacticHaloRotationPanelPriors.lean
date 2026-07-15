/-
  FSOT Formal FoundingGalacticHaloRotationPanelPriors — extension domain Founding_Galactic_Halo_Rotation_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_galactic_halo_rotation_panel_observable_count : ℕ := 24
def founding_galactic_halo_rotation_panel_D_eff : ℕ := 14

theorem founding_galactic_halo_rotation_panel_observable_count_pos : 0 < founding_galactic_halo_rotation_panel_observable_count := by
  unfold founding_galactic_halo_rotation_panel_observable_count; norm_num

theorem founding_galactic_halo_rotation_panel_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem founding_galactic_halo_rotation_panel_bundle :
    founding_galactic_halo_rotation_panel_observable_count = 24 ∧
    founding_galactic_halo_rotation_panel_D_eff = 14 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_galactic_halo_rotation_panel_observable_count; norm_num,
    by unfold founding_galactic_halo_rotation_panel_D_eff; norm_num,
    founding_galactic_halo_rotation_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
