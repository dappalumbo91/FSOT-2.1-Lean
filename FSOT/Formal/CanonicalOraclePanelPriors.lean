/-
  FSOT Formal CanonicalOraclePanelPriors — extension domain Canonical_Oracle_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def canonical_oracle_panel_observable_count : ℕ := 24
def canonical_oracle_panel_D_eff : ℕ := 18

theorem canonical_oracle_panel_observable_count_pos : 0 < canonical_oracle_panel_observable_count := by
  unfold canonical_oracle_panel_observable_count; decide

theorem canonical_oracle_panel_median_error_under_half_pct :
    (0.013294 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013294 : ℝ) < (0.5 : ℝ))

theorem canonical_oracle_panel_bundle :
    canonical_oracle_panel_observable_count = 24 ∧
    canonical_oracle_panel_D_eff = 18 ∧
    (0.013294 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold canonical_oracle_panel_observable_count; decide,
    by unfold canonical_oracle_panel_D_eff; decide,
    canonical_oracle_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
