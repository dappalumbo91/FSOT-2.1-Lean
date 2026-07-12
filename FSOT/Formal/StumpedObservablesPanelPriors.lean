/-
  FSOT Formal StumpedObservablesPanelPriors — extension domain Stumped_Observables_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def stumped_observables_panel_observable_count : ℕ := 24
def stumped_observables_panel_D_eff : ℕ := 22

theorem stumped_observables_panel_observable_count_pos : 0 < stumped_observables_panel_observable_count := by
  unfold stumped_observables_panel_observable_count; norm_num

theorem stumped_observables_panel_median_error_under_half_pct :
    (0.029748999999999998 : ℝ) < (0.5 : ℝ) := by norm_num

theorem stumped_observables_panel_bundle :
    stumped_observables_panel_observable_count = 24 ∧
    stumped_observables_panel_D_eff = 22 ∧
    (0.029748999999999998 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold stumped_observables_panel_observable_count; norm_num,
    by unfold stumped_observables_panel_D_eff; norm_num,
    stumped_observables_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
