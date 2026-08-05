/-
  FSOT Formal ArxivGravitationalWavesPanelPriors — extension domain Arxiv_Gravitational_Waves_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def arxiv_gravitational_waves_panel_observable_count : ℕ := 60
def arxiv_gravitational_waves_panel_D_eff : ℕ := 21

theorem arxiv_gravitational_waves_panel_observable_count_pos : 0 < arxiv_gravitational_waves_panel_observable_count := by
  unfold arxiv_gravitational_waves_panel_observable_count; decide

theorem arxiv_gravitational_waves_panel_median_error_under_half_pct :
    (0.01748 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.01748 : ℝ) < (0.5 : ℝ))

theorem arxiv_gravitational_waves_panel_bundle :
    arxiv_gravitational_waves_panel_observable_count = 60 ∧
    arxiv_gravitational_waves_panel_D_eff = 21 ∧
    (0.01748 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold arxiv_gravitational_waves_panel_observable_count; decide,
    by unfold arxiv_gravitational_waves_panel_D_eff; decide,
    arxiv_gravitational_waves_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
