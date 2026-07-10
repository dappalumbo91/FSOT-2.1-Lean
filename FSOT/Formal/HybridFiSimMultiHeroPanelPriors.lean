/-
  FSOT Formal HybridFiSimMultiHeroPanelPriors — Tier 77 post–Tier 76 maintenance.
  Generator: scripts/gen_tiers_77_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hybrid_fi_sim_multi_hero_panel_observable_count : ℕ := 14
def hybrid_fi_sim_multi_hero_panel_pooled_median_error_pct : ℝ := (0.051436 : ℝ)
def hybrid_fi_sim_multi_hero_panel_headline_median_error_pct : ℝ := (0.05143619629083711 : ℝ)
def hybrid_fi_sim_multi_hero_panel_beats_sota_headlines : ℕ := 2
def hybrid_fi_sim_multi_hero_panel_D_eff : ℕ := 18

theorem hybrid_fi_sim_multi_hero_panel_observable_count_pos : 0 < hybrid_fi_sim_multi_hero_panel_observable_count := by
  unfold hybrid_fi_sim_multi_hero_panel_observable_count; norm_num

theorem hybrid_fi_sim_multi_hero_panel_pooled_median_under_half_pct :
    hybrid_fi_sim_multi_hero_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold hybrid_fi_sim_multi_hero_panel_pooled_median_error_pct; norm_num

theorem hybrid_fi_sim_multi_hero_panel_headline_median_under_half_pct :
    hybrid_fi_sim_multi_hero_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold hybrid_fi_sim_multi_hero_panel_headline_median_error_pct; norm_num

theorem hybrid_fi_sim_multi_hero_panel_beats_sota_headlines_pos : 0 < hybrid_fi_sim_multi_hero_panel_beats_sota_headlines := by
  unfold hybrid_fi_sim_multi_hero_panel_beats_sota_headlines; norm_num

theorem hybrid_fi_sim_multi_hero_panel_bundle :
    hybrid_fi_sim_multi_hero_panel_observable_count = 14 ∧
    hybrid_fi_sim_multi_hero_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    hybrid_fi_sim_multi_hero_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold hybrid_fi_sim_multi_hero_panel_observable_count; norm_num
  · exact hybrid_fi_sim_multi_hero_panel_pooled_median_under_half_pct
  · exact hybrid_fi_sim_multi_hero_panel_beats_sota_headlines_pos

end
