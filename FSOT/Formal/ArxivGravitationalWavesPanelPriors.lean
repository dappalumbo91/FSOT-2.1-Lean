/-
  FSOT Formal ArxivGravitationalWavesPanelPriors — Tier 84 scientific expansion (Arxiv_Gravitational_Waves_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def arxiv_gw_panel_observable_count : ℕ := 36
def arxiv_gw_panel_median_error_pct : ℝ := (0.01748 : ℝ)
def arxiv_gw_panel_D_eff : ℕ := 21

theorem arxiv_gw_panel_observable_count_pos : 0 < arxiv_gw_panel_observable_count := by
  unfold arxiv_gw_panel_observable_count; norm_num

theorem arxiv_gw_panel_median_error_under_five_pct :
    arxiv_gw_panel_median_error_pct < (5 : ℝ) := by
  unfold arxiv_gw_panel_median_error_pct; norm_num

theorem arxiv_gw_panel_bundle :
    arxiv_gw_panel_observable_count = 36 ∧
    arxiv_gw_panel_D_eff = 21 ∧
    arxiv_gw_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold arxiv_gw_panel_observable_count; norm_num,
    by unfold arxiv_gw_panel_D_eff; norm_num,
    arxiv_gw_panel_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
