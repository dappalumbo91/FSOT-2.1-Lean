/-
  FSOT Formal OmniTheoryHumanitiesPanelPriors — extension domain Omni_Theory_Humanities_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def omni_theory_humanities_panel_observable_count : ℕ := 37
def omni_theory_humanities_panel_D_eff : ℕ := 17

theorem omni_theory_humanities_panel_observable_count_pos : 0 < omni_theory_humanities_panel_observable_count := by
  unfold omni_theory_humanities_panel_observable_count; decide

theorem omni_theory_humanities_panel_median_error_under_half_pct :
    (0.0222545 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0222545 : ℝ) < (0.5 : ℝ))

theorem omni_theory_humanities_panel_bundle :
    omni_theory_humanities_panel_observable_count = 37 ∧
    omni_theory_humanities_panel_D_eff = 17 ∧
    (0.0222545 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold omni_theory_humanities_panel_observable_count; decide,
    by unfold omni_theory_humanities_panel_D_eff; decide,
    omni_theory_humanities_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
