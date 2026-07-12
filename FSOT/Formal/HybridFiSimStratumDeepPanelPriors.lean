/-
  FSOT Formal HybridFiSimStratumDeepPanelPriors — Tier 86 scientific expansion (Hybrid_FI_Sim_Stratum_Deep_Panel).
  Generator: scripts/gen_tier86_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hybrid_fi_stratum_deep_observable_count : ℕ := 19
def hybrid_fi_stratum_deep_median_error_pct : ℝ := (0.018003 : ℝ)
def hybrid_fi_stratum_deep_D_eff : ℕ := 18

theorem hybrid_fi_stratum_deep_observable_count_pos : 0 < hybrid_fi_stratum_deep_observable_count := by
  unfold hybrid_fi_stratum_deep_observable_count; norm_num

theorem hybrid_fi_stratum_deep_median_error_under_five_pct :
    hybrid_fi_stratum_deep_median_error_pct < (5 : ℝ) := by
  unfold hybrid_fi_stratum_deep_median_error_pct; norm_num

theorem hybrid_fi_stratum_deep_bundle :
    hybrid_fi_stratum_deep_observable_count = 19 ∧
    hybrid_fi_stratum_deep_D_eff = 18 ∧
    hybrid_fi_stratum_deep_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold hybrid_fi_stratum_deep_observable_count; norm_num,
    by unfold hybrid_fi_stratum_deep_D_eff; norm_num,
    hybrid_fi_stratum_deep_median_error_under_five_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
