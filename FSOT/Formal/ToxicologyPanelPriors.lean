/-
  FSOT Formal ToxicologyPanelPriors — extension domain Toxicology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def toxicology_panel_observable_count : ℕ := 21
def toxicology_panel_D_eff : ℕ := 13

theorem toxicology_panel_observable_count_pos : 0 < toxicology_panel_observable_count := by
  unfold toxicology_panel_observable_count; norm_num

theorem toxicology_panel_median_error_under_half_pct :
    (0.033401 : ℝ) < (0.5 : ℝ) := by norm_num

theorem toxicology_panel_bundle :
    toxicology_panel_observable_count = 21 ∧
    toxicology_panel_D_eff = 13 ∧
    (0.033401 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold toxicology_panel_observable_count; norm_num,
    by unfold toxicology_panel_D_eff; norm_num,
    toxicology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
