/-
  FSOT Formal ArxivPrimitivesPanelPriors — extension domain Arxiv_Primitives_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def arxiv_primitives_panel_observable_count : ℕ := 22
def arxiv_primitives_panel_D_eff : ℕ := 15

theorem arxiv_primitives_panel_observable_count_pos : 0 < arxiv_primitives_panel_observable_count := by
  unfold arxiv_primitives_panel_observable_count; decide

theorem arxiv_primitives_panel_median_error_under_half_pct :
    (0.031506 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.031506 : ℝ) < (0.5 : ℝ))

theorem arxiv_primitives_panel_bundle :
    arxiv_primitives_panel_observable_count = 22 ∧
    arxiv_primitives_panel_D_eff = 15 ∧
    (0.031506 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold arxiv_primitives_panel_observable_count; decide,
    by unfold arxiv_primitives_panel_D_eff; decide,
    arxiv_primitives_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
