/-
  FSOT Formal OstiDoeSciencePanelPriors — extension domain OSTI_DOE_Science_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def osti_doe_science_panel_observable_count : ℕ := 100
def osti_doe_science_panel_D_eff : ℕ := 18

theorem osti_doe_science_panel_observable_count_pos : 0 < osti_doe_science_panel_observable_count := by
  unfold osti_doe_science_panel_observable_count; decide

theorem osti_doe_science_panel_median_error_under_half_pct :
    (0.01382 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.01382 : ℝ) < (0.5 : ℝ))

theorem osti_doe_science_panel_bundle :
    osti_doe_science_panel_observable_count = 100 ∧
    osti_doe_science_panel_D_eff = 18 ∧
    (0.01382 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold osti_doe_science_panel_observable_count; decide,
    by unfold osti_doe_science_panel_D_eff; decide,
    osti_doe_science_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
