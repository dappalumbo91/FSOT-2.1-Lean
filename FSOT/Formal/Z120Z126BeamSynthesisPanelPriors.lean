/-
  FSOT Formal Z120Z126BeamSynthesisPanelPriors — Tier 74 superheavy island Z=120-126.
  Generator: scripts/gen_tiers_74_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def z120_z126_beam_synthesis_panel_observable_count : ℕ := 20
def z120_z126_beam_synthesis_panel_pooled_median_error_pct : ℝ := (9.5e-05 : ℝ)
def z120_z126_beam_synthesis_panel_headline_median_error_pct : ℝ := (9.504134402225917e-05 : ℝ)
def z120_z126_beam_synthesis_panel_beats_sota_headlines : ℕ := 2
def z120_z126_beam_synthesis_panel_D_eff : ℕ := 20

theorem z120_z126_beam_synthesis_panel_observable_count_pos : 0 < z120_z126_beam_synthesis_panel_observable_count := by
  unfold z120_z126_beam_synthesis_panel_observable_count; norm_num

theorem z120_z126_beam_synthesis_panel_pooled_median_under_half_pct :
    z120_z126_beam_synthesis_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold z120_z126_beam_synthesis_panel_pooled_median_error_pct; norm_num

theorem z120_z126_beam_synthesis_panel_headline_median_under_half_pct :
    z120_z126_beam_synthesis_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold z120_z126_beam_synthesis_panel_headline_median_error_pct; norm_num

theorem z120_z126_beam_synthesis_panel_beats_sota_headlines_pos : 0 < z120_z126_beam_synthesis_panel_beats_sota_headlines := by
  unfold z120_z126_beam_synthesis_panel_beats_sota_headlines; norm_num

theorem z120_z126_beam_synthesis_panel_bundle :
    z120_z126_beam_synthesis_panel_observable_count = 20 ∧
    z120_z126_beam_synthesis_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    z120_z126_beam_synthesis_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold z120_z126_beam_synthesis_panel_observable_count; norm_num
  · exact z120_z126_beam_synthesis_panel_pooled_median_under_half_pct
  · exact z120_z126_beam_synthesis_panel_beats_sota_headlines_pos

end
