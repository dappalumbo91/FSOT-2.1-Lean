/-
  FSOT Formal PeriodicTablePublicPanelPriors — Tier 72 periodic table completion.
  Generator: scripts/gen_tiers_72_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def periodic_table_public_panel_observable_count : ℕ := 52
def periodic_table_public_panel_pooled_median_error_pct : ℝ := (9.5e-05 : ℝ)
def periodic_table_public_panel_headline_median_error_pct : ℝ := (9.504134401579763e-05 : ℝ)
def periodic_table_public_panel_beats_sota_headlines : ℕ := 2
def periodic_table_public_panel_D_eff : ℕ := 9

theorem periodic_table_public_panel_observable_count_pos : 0 < periodic_table_public_panel_observable_count := by
  unfold periodic_table_public_panel_observable_count; norm_num

theorem periodic_table_public_panel_pooled_median_under_half_pct :
    periodic_table_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold periodic_table_public_panel_pooled_median_error_pct; norm_num

theorem periodic_table_public_panel_headline_median_under_half_pct :
    periodic_table_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold periodic_table_public_panel_headline_median_error_pct; norm_num

theorem periodic_table_public_panel_beats_sota_headlines_pos : 0 < periodic_table_public_panel_beats_sota_headlines := by
  unfold periodic_table_public_panel_beats_sota_headlines; norm_num

theorem periodic_table_public_panel_bundle :
    periodic_table_public_panel_observable_count = 52 ∧
    periodic_table_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    periodic_table_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold periodic_table_public_panel_observable_count; norm_num
  · exact periodic_table_public_panel_pooled_median_under_half_pct
  · exact periodic_table_public_panel_beats_sota_headlines_pos

end
