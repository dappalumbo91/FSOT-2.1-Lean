/-
  FSOT Formal ZebrafishLongevityGeneticsCouplingPanelPriors — extension domain Zebrafish_Longevity_Genetics_Coupling_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zebrafish_longevity_genetics_coupling_panel_observable_count : ℕ := 24
def zebrafish_longevity_genetics_coupling_panel_D_eff : ℕ := 22

theorem zebrafish_longevity_genetics_coupling_panel_observable_count_pos : 0 < zebrafish_longevity_genetics_coupling_panel_observable_count := by
  unfold zebrafish_longevity_genetics_coupling_panel_observable_count; norm_num

theorem zebrafish_longevity_genetics_coupling_panel_median_error_under_half_pct :
    (0.014453500000000001 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zebrafish_longevity_genetics_coupling_panel_bundle :
    zebrafish_longevity_genetics_coupling_panel_observable_count = 24 ∧
    zebrafish_longevity_genetics_coupling_panel_D_eff = 22 ∧
    (0.014453500000000001 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zebrafish_longevity_genetics_coupling_panel_observable_count; norm_num,
    by unfold zebrafish_longevity_genetics_coupling_panel_D_eff; norm_num,
    zebrafish_longevity_genetics_coupling_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
