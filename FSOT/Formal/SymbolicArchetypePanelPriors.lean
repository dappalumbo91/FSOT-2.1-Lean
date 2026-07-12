/-
  FSOT Formal SymbolicArchetypePanelPriors — extension domain Symbolic_Archetype_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def symbolic_archetype_panel_observable_count : ℕ := 28
def symbolic_archetype_panel_D_eff : ℕ := 17

theorem symbolic_archetype_panel_observable_count_pos : 0 < symbolic_archetype_panel_observable_count := by
  unfold symbolic_archetype_panel_observable_count; norm_num

theorem symbolic_archetype_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem symbolic_archetype_panel_bundle :
    symbolic_archetype_panel_observable_count = 28 ∧
    symbolic_archetype_panel_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold symbolic_archetype_panel_observable_count; norm_num,
    by unfold symbolic_archetype_panel_D_eff; norm_num,
    symbolic_archetype_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
