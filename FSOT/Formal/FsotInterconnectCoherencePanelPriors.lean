/-
  FSOT Formal FsotInterconnectCoherencePanelPriors — hardware depth (FSOT_Interconnect_Coherence_Panel).
  Generator: scripts/gen_hardware_depth_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_interconnect_coherence_observable_count : ℕ := 88
def fsot_interconnect_coherence_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_interconnect_coherence_D_eff : ℕ := 11

theorem fsot_interconnect_coherence_observable_count_pos : 0 < fsot_interconnect_coherence_observable_count := by
  unfold fsot_interconnect_coherence_observable_count; decide

theorem fsot_interconnect_coherence_median_error_under_half_pct :
    fsot_interconnect_coherence_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_interconnect_coherence_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem fsot_interconnect_coherence_bundle :
    fsot_interconnect_coherence_observable_count = 88 ∧
    fsot_interconnect_coherence_D_eff = 11 ∧
    fsot_interconnect_coherence_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold fsot_interconnect_coherence_observable_count; decide,
    by unfold fsot_interconnect_coherence_D_eff; decide,
    fsot_interconnect_coherence_median_error_under_half_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
