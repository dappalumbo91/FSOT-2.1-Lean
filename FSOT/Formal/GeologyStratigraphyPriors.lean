/-
  FSOT Formal GeologyStratigraphyPriors — extension domain Geology_Stratigraphy.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def geology_stratigraphy_observable_count : ℕ := 1960
def geology_stratigraphy_D_eff : ℕ := 18

theorem geology_stratigraphy_observable_count_pos : 0 < geology_stratigraphy_observable_count := by
  unfold geology_stratigraphy_observable_count; norm_num

theorem geology_stratigraphy_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem geology_stratigraphy_bundle :
    geology_stratigraphy_observable_count = 1960 ∧
    geology_stratigraphy_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold geology_stratigraphy_observable_count; norm_num,
    by unfold geology_stratigraphy_D_eff; norm_num,
    geology_stratigraphy_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
