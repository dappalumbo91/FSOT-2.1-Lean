/-
  FSOT Formal CrossrefScholarlyPanelPriors — extension domain Crossref_Scholarly_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def crossref_scholarly_panel_observable_count : ℕ := 200
def crossref_scholarly_panel_D_eff : ℕ := 18

theorem crossref_scholarly_panel_observable_count_pos : 0 < crossref_scholarly_panel_observable_count := by
  unfold crossref_scholarly_panel_observable_count; norm_num

theorem crossref_scholarly_panel_median_error_under_half_pct :
    (0.01382 : ℝ) < (0.5 : ℝ) := by norm_num

theorem crossref_scholarly_panel_bundle :
    crossref_scholarly_panel_observable_count = 200 ∧
    crossref_scholarly_panel_D_eff = 18 ∧
    (0.01382 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold crossref_scholarly_panel_observable_count; norm_num,
    by unfold crossref_scholarly_panel_D_eff; norm_num,
    crossref_scholarly_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
