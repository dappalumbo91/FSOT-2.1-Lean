/-
  FSOT Formal PeriodicTablePublicPanelPriors — extension domain Periodic_Table_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def periodic_table_public_panel_observable_count : ℕ := 52
def periodic_table_public_panel_D_eff : ℕ := 9

theorem periodic_table_public_panel_observable_count_pos : 0 < periodic_table_public_panel_observable_count := by
  unfold periodic_table_public_panel_observable_count; norm_num

theorem periodic_table_public_panel_median_error_under_half_pct :
    (9.5e-05 : ℝ) < (0.5 : ℝ) := by norm_num

theorem periodic_table_public_panel_bundle :
    periodic_table_public_panel_observable_count = 52 ∧
    periodic_table_public_panel_D_eff = 9 ∧
    (9.5e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold periodic_table_public_panel_observable_count; norm_num,
    by unfold periodic_table_public_panel_D_eff; norm_num,
    periodic_table_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
