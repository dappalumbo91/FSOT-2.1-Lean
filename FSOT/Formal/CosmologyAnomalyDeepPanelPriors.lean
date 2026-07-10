/-
  FSOT Formal CosmologyAnomalyDeepPanelPriors — Tier 76 fluid spacetime + cosmology.
  Generator: scripts/gen_tiers_76_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_anomaly_deep_panel_observable_count : ℕ := 14
def cosmology_anomaly_deep_panel_pooled_median_error_pct : ℝ := (0.000502 : ℝ)
def cosmology_anomaly_deep_panel_headline_median_error_pct : ℝ := (0.0005024559462039755 : ℝ)
def cosmology_anomaly_deep_panel_beats_sota_headlines : ℕ := 2
def cosmology_anomaly_deep_panel_D_eff : ℕ := 24

theorem cosmology_anomaly_deep_panel_observable_count_pos : 0 < cosmology_anomaly_deep_panel_observable_count := by
  unfold cosmology_anomaly_deep_panel_observable_count; norm_num

theorem cosmology_anomaly_deep_panel_pooled_median_under_half_pct :
    cosmology_anomaly_deep_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_anomaly_deep_panel_pooled_median_error_pct; norm_num

theorem cosmology_anomaly_deep_panel_headline_median_under_half_pct :
    cosmology_anomaly_deep_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_anomaly_deep_panel_headline_median_error_pct; norm_num

theorem cosmology_anomaly_deep_panel_beats_sota_headlines_pos : 0 < cosmology_anomaly_deep_panel_beats_sota_headlines := by
  unfold cosmology_anomaly_deep_panel_beats_sota_headlines; norm_num

theorem cosmology_anomaly_deep_panel_bundle :
    cosmology_anomaly_deep_panel_observable_count = 14 ∧
    cosmology_anomaly_deep_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    cosmology_anomaly_deep_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold cosmology_anomaly_deep_panel_observable_count; norm_num
  · exact cosmology_anomaly_deep_panel_pooled_median_under_half_pct
  · exact cosmology_anomaly_deep_panel_beats_sota_headlines_pos

end
