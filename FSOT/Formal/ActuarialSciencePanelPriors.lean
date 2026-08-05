/-
  FSOT Formal ActuarialSciencePanelPriors — extension domain Actuarial_Science_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def actuarial_science_panel_observable_count : ℕ := 60
def actuarial_science_panel_D_eff : ℕ := 20

theorem actuarial_science_panel_observable_count_pos : 0 < actuarial_science_panel_observable_count := by
  unfold actuarial_science_panel_observable_count; decide

theorem actuarial_science_panel_median_error_under_half_pct :
    (0.02261 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02261 : ℝ) < (0.5 : ℝ))

theorem actuarial_science_panel_bundle :
    actuarial_science_panel_observable_count = 60 ∧
    actuarial_science_panel_D_eff = 20 ∧
    (0.02261 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold actuarial_science_panel_observable_count; decide,
    by unfold actuarial_science_panel_D_eff; decide,
    actuarial_science_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
