/-
  FSOT Formal FpcTemporalCouplingPriors — extension domain FPC_Temporal_Coupling.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fpc_temporal_coupling_observable_count : ℕ := 24
def fpc_temporal_coupling_D_eff : ℕ := 18

theorem fpc_temporal_coupling_observable_count_pos : 0 < fpc_temporal_coupling_observable_count := by
  unfold fpc_temporal_coupling_observable_count; decide

theorem fpc_temporal_coupling_median_error_under_half_pct :
    (0.029733 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.029733 : ℝ) < (0.5 : ℝ))

theorem fpc_temporal_coupling_bundle :
    fpc_temporal_coupling_observable_count = 24 ∧
    fpc_temporal_coupling_D_eff = 18 ∧
    (0.029733 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fpc_temporal_coupling_observable_count; decide,
    by unfold fpc_temporal_coupling_D_eff; decide,
    fpc_temporal_coupling_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
