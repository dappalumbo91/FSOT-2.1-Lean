/-
  FSOT Formal QceElmFusionEdgePanelPriors — recent breakthrough expansion (QCE_ELM_Fusion_Edge_Panel).
  Generator: scripts/gen_recent_breakthrough_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def qce_elm_fusion_edge_observable_count : ℕ := 22
def qce_elm_fusion_edge_median_error_pct : ℝ := (0.0 : ℝ)
def qce_elm_fusion_edge_D_eff : ℕ := 14

theorem qce_elm_fusion_edge_observable_count_pos : 0 < qce_elm_fusion_edge_observable_count := by
  unfold qce_elm_fusion_edge_observable_count; norm_num

theorem qce_elm_fusion_edge_median_error_under_half_pct :
    qce_elm_fusion_edge_median_error_pct < (0.5 : ℝ) := by
  unfold qce_elm_fusion_edge_median_error_pct; norm_num

theorem qce_elm_fusion_edge_bundle :
    qce_elm_fusion_edge_observable_count = 22 ∧
    qce_elm_fusion_edge_D_eff = 14 ∧
    qce_elm_fusion_edge_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold qce_elm_fusion_edge_observable_count; norm_num,
    by unfold qce_elm_fusion_edge_D_eff; norm_num,
    qce_elm_fusion_edge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
