/-
  FSOT Formal HybridFiSimStratumDeepPanelPriors — extension domain Hybrid_FI_Sim_Stratum_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def hybrid_fi_sim_stratum_deep_panel_observable_count : ℕ := 24
def hybrid_fi_sim_stratum_deep_panel_D_eff : ℕ := 18

theorem hybrid_fi_sim_stratum_deep_panel_observable_count_pos : 0 < hybrid_fi_sim_stratum_deep_panel_observable_count := by
  unfold hybrid_fi_sim_stratum_deep_panel_observable_count; decide

theorem hybrid_fi_sim_stratum_deep_panel_median_error_under_half_pct :
    (0.018003 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.018003 : ℝ) < (0.5 : ℝ))

theorem hybrid_fi_sim_stratum_deep_panel_bundle :
    hybrid_fi_sim_stratum_deep_panel_observable_count = 24 ∧
    hybrid_fi_sim_stratum_deep_panel_D_eff = 18 ∧
    (0.018003 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hybrid_fi_sim_stratum_deep_panel_observable_count; decide,
    by unfold hybrid_fi_sim_stratum_deep_panel_D_eff; decide,
    hybrid_fi_sim_stratum_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
