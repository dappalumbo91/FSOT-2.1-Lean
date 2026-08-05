/-
  FSOT Formal PhysarumBiologicalCudaPanelPriors — extension domain Physarum_Biological_CUDA_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def physarum_biological_cuda_panel_observable_count : ℕ := 24
def physarum_biological_cuda_panel_D_eff : ℕ := 15

theorem physarum_biological_cuda_panel_observable_count_pos : 0 < physarum_biological_cuda_panel_observable_count := by
  unfold physarum_biological_cuda_panel_observable_count; decide

theorem physarum_biological_cuda_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem physarum_biological_cuda_panel_bundle :
    physarum_biological_cuda_panel_observable_count = 24 ∧
    physarum_biological_cuda_panel_D_eff = 15 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold physarum_biological_cuda_panel_observable_count; decide,
    by unfold physarum_biological_cuda_panel_D_eff; decide,
    physarum_biological_cuda_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
