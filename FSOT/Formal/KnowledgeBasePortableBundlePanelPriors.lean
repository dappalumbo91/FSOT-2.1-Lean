/-
  FSOT Formal KnowledgeBasePortableBundlePanelPriors — Tier 77 post–Tier 76 maintenance.
  Generator: scripts/gen_tiers_77_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def knowledge_base_portable_bundle_panel_observable_count : ℕ := 13
def knowledge_base_portable_bundle_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def knowledge_base_portable_bundle_panel_headline_median_error_pct : ℝ := (0.018019024892929635 : ℝ)
def knowledge_base_portable_bundle_panel_beats_sota_headlines : ℕ := 2
def knowledge_base_portable_bundle_panel_D_eff : ℕ := 19

theorem knowledge_base_portable_bundle_panel_observable_count_pos : 0 < knowledge_base_portable_bundle_panel_observable_count := by
  unfold knowledge_base_portable_bundle_panel_observable_count; norm_num

theorem knowledge_base_portable_bundle_panel_pooled_median_under_half_pct :
    knowledge_base_portable_bundle_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold knowledge_base_portable_bundle_panel_pooled_median_error_pct; norm_num

theorem knowledge_base_portable_bundle_panel_headline_median_under_half_pct :
    knowledge_base_portable_bundle_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold knowledge_base_portable_bundle_panel_headline_median_error_pct; norm_num

theorem knowledge_base_portable_bundle_panel_beats_sota_headlines_pos : 0 < knowledge_base_portable_bundle_panel_beats_sota_headlines := by
  unfold knowledge_base_portable_bundle_panel_beats_sota_headlines; norm_num

theorem knowledge_base_portable_bundle_panel_bundle :
    knowledge_base_portable_bundle_panel_observable_count = 13 ∧
    knowledge_base_portable_bundle_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    knowledge_base_portable_bundle_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold knowledge_base_portable_bundle_panel_observable_count; norm_num
  · exact knowledge_base_portable_bundle_panel_pooled_median_under_half_pct
  · exact knowledge_base_portable_bundle_panel_beats_sota_headlines_pos

end
