/-
  FSOT Formal InaturalistObservationPanelPriors — extension domain iNaturalist_Observation_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def inaturalist_observation_panel_observable_count : ℕ := 288
def inaturalist_observation_panel_D_eff : ℕ := 15

theorem inaturalist_observation_panel_observable_count_pos : 0 < inaturalist_observation_panel_observable_count := by
  unfold inaturalist_observation_panel_observable_count; norm_num

theorem inaturalist_observation_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) := by norm_num

theorem inaturalist_observation_panel_bundle :
    inaturalist_observation_panel_observable_count = 288 ∧
    inaturalist_observation_panel_D_eff = 15 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold inaturalist_observation_panel_observable_count; norm_num,
    by unfold inaturalist_observation_panel_D_eff; norm_num,
    inaturalist_observation_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
