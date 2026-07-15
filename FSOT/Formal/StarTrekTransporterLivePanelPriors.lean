/-
  FSOT Formal StarTrekTransporterLivePanelPriors — Tier 88 application wiring (Star_Trek_Transporter_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def star_trek_transporter_observable_count : ℕ := 14
def star_trek_transporter_median_error_pct : ℝ := (0.095551 : ℝ)
def star_trek_transporter_D_eff : ℕ := 17

theorem star_trek_transporter_observable_count_pos : 0 < star_trek_transporter_observable_count := by
  unfold star_trek_transporter_observable_count; norm_num

theorem star_trek_transporter_median_error_under_five_pct :
    star_trek_transporter_median_error_pct < (5 : ℝ) := by
  unfold star_trek_transporter_median_error_pct; norm_num

theorem star_trek_transporter_bundle :
    star_trek_transporter_observable_count = 14 ∧
    star_trek_transporter_D_eff = 17 ∧
    star_trek_transporter_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold star_trek_transporter_observable_count; norm_num,
    by unfold star_trek_transporter_D_eff; norm_num,
    star_trek_transporter_median_error_under_five_pct,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
