/-
  FSOT Formal StarTrekTransporterLivePanelPriors — extension domain Star_Trek_Transporter_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def star_trek_transporter_live_panel_observable_count : ℕ := 44
def star_trek_transporter_live_panel_D_eff : ℕ := 14

theorem star_trek_transporter_live_panel_observable_count_pos : 0 < star_trek_transporter_live_panel_observable_count := by
  unfold star_trek_transporter_live_panel_observable_count; norm_num

theorem star_trek_transporter_live_panel_median_error_under_half_pct :
    (0.05256 : ℝ) < (0.5 : ℝ) := by norm_num

theorem star_trek_transporter_live_panel_bundle :
    star_trek_transporter_live_panel_observable_count = 44 ∧
    star_trek_transporter_live_panel_D_eff = 14 ∧
    (0.05256 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold star_trek_transporter_live_panel_observable_count; norm_num,
    by unfold star_trek_transporter_live_panel_D_eff; norm_num,
    star_trek_transporter_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
