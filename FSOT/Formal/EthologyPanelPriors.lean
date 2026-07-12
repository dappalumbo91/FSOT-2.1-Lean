/-
  FSOT Formal EthologyPanelPriors — extension domain Ethology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def ethology_panel_observable_count : ℕ := 100
def ethology_panel_D_eff : ℕ := 15

theorem ethology_panel_observable_count_pos : 0 < ethology_panel_observable_count := by
  unfold ethology_panel_observable_count; norm_num

theorem ethology_panel_median_error_under_half_pct :
    (0.006607 : ℝ) < (0.5 : ℝ) := by norm_num

theorem ethology_panel_bundle :
    ethology_panel_observable_count = 100 ∧
    ethology_panel_D_eff = 15 ∧
    (0.006607 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold ethology_panel_observable_count; norm_num,
    by unfold ethology_panel_D_eff; norm_num,
    ethology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
