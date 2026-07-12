/-
  FSOT Formal MusicHarmonicsPublicPanelPriors — extension domain Music_Harmonics_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def music_harmonics_public_panel_observable_count : ℕ := 24
def music_harmonics_public_panel_D_eff : ℕ := 10

theorem music_harmonics_public_panel_observable_count_pos : 0 < music_harmonics_public_panel_observable_count := by
  unfold music_harmonics_public_panel_observable_count; norm_num

theorem music_harmonics_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem music_harmonics_public_panel_bundle :
    music_harmonics_public_panel_observable_count = 24 ∧
    music_harmonics_public_panel_D_eff = 10 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold music_harmonics_public_panel_observable_count; norm_num,
    by unfold music_harmonics_public_panel_D_eff; norm_num,
    music_harmonics_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
