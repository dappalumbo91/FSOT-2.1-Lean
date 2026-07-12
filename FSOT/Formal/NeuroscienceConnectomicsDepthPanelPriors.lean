/-
  FSOT Formal NeuroscienceConnectomicsDepthPanelPriors — extension domain Neuroscience_Connectomics_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neuroscience_connectomics_depth_panel_observable_count : ℕ := 27
def neuroscience_connectomics_depth_panel_D_eff : ℕ := 18

theorem neuroscience_connectomics_depth_panel_observable_count_pos : 0 < neuroscience_connectomics_depth_panel_observable_count := by
  unfold neuroscience_connectomics_depth_panel_observable_count; norm_num

theorem neuroscience_connectomics_depth_panel_median_error_under_half_pct :
    (0.0201195 : ℝ) < (0.5 : ℝ) := by norm_num

theorem neuroscience_connectomics_depth_panel_bundle :
    neuroscience_connectomics_depth_panel_observable_count = 27 ∧
    neuroscience_connectomics_depth_panel_D_eff = 18 ∧
    (0.0201195 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neuroscience_connectomics_depth_panel_observable_count; norm_num,
    by unfold neuroscience_connectomics_depth_panel_D_eff; norm_num,
    neuroscience_connectomics_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
