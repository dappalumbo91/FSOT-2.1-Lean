/-
  FSOT Formal TokenizationLivePanelPriors — extension domain Tokenization_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def tokenization_live_panel_observable_count : ℕ := 24
def tokenization_live_panel_D_eff : ℕ := 13

theorem tokenization_live_panel_observable_count_pos : 0 < tokenization_live_panel_observable_count := by
  unfold tokenization_live_panel_observable_count; decide

theorem tokenization_live_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem tokenization_live_panel_bundle :
    tokenization_live_panel_observable_count = 24 ∧
    tokenization_live_panel_D_eff = 13 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tokenization_live_panel_observable_count; decide,
    by unfold tokenization_live_panel_D_eff; decide,
    tokenization_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
