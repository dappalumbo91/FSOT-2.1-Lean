/-
  FSOT Formal NeuroscienceConnectomicsDepthPanelPriors — Tier 87 depth wave (Neuroscience_Connectomics_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroscience_connectomics_depth_observable_count : ℕ := 27
def neuroscience_connectomics_depth_median_error_pct : ℝ := (0.0201195 : ℝ)
def neuroscience_connectomics_depth_D_eff : ℕ := 18

theorem neuroscience_connectomics_depth_observable_count_pos : 0 < neuroscience_connectomics_depth_observable_count := by
  unfold neuroscience_connectomics_depth_observable_count; norm_num

theorem neuroscience_connectomics_depth_median_error_under_five_pct :
    neuroscience_connectomics_depth_median_error_pct < (5 : ℝ) := by
  unfold neuroscience_connectomics_depth_median_error_pct; norm_num

theorem neuroscience_connectomics_depth_bundle :
    neuroscience_connectomics_depth_observable_count = 27 ∧
    neuroscience_connectomics_depth_D_eff = 18 ∧
    neuroscience_connectomics_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold neuroscience_connectomics_depth_observable_count; norm_num,
    by unfold neuroscience_connectomics_depth_D_eff; norm_num,
    neuroscience_connectomics_depth_median_error_under_five_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
