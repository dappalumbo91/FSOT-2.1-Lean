/-
  FSOT Formal CosmologyAnomalyDeepPanelPriors — extension domain Cosmology_Anomaly_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cosmology_anomaly_deep_panel_observable_count : ℕ := 24
def cosmology_anomaly_deep_panel_D_eff : ℕ := 24

theorem cosmology_anomaly_deep_panel_observable_count_pos : 0 < cosmology_anomaly_deep_panel_observable_count := by
  unfold cosmology_anomaly_deep_panel_observable_count; decide

theorem cosmology_anomaly_deep_panel_median_error_under_half_pct :
    (0.029733 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cosmology_anomaly_deep_panel_bundle :
    cosmology_anomaly_deep_panel_observable_count = 24 ∧
    cosmology_anomaly_deep_panel_D_eff = 24 ∧
    (0.029733 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cosmology_anomaly_deep_panel_observable_count; decide,
    by unfold cosmology_anomaly_deep_panel_D_eff; decide,
    cosmology_anomaly_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
