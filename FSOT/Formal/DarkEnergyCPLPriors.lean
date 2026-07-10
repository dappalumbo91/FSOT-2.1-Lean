/-
  FSOT Formal DarkEnergyCPLPriors — Dark_Energy_CPL Tier 51 anomaly observables.
  Generator: scripts/gen_anomaly_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def dark_energy_cpl_observable_count : ℕ := 6
def dark_energy_cpl_pooled_median_error_pct : ℝ := (0.025535 : ℝ)
def dark_energy_cpl_headline_median_error_pct : ℝ := (0.025535 : ℝ)
def dark_energy_cpl_beats_sota_headlines : ℕ := 2
def dark_energy_cpl_D_eff : ℕ := 24
def dark_energy_cpl_fsot_wa : ℝ := (-0.808129 : ℝ)
def dark_energy_cpl_preregistered : Bool := true

theorem dark_energy_cpl_observable_count_pos : 0 < dark_energy_cpl_observable_count := by
  unfold dark_energy_cpl_observable_count; norm_num

theorem dark_energy_cpl_pooled_median_under_half_pct :
    dark_energy_cpl_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold dark_energy_cpl_pooled_median_error_pct; norm_num

theorem dark_energy_cpl_headline_median_under_half_pct :
    dark_energy_cpl_headline_median_error_pct < (0.5 : ℝ) := by
  unfold dark_energy_cpl_headline_median_error_pct; norm_num

theorem dark_energy_cpl_beats_sota_headlines_pos : 0 < dark_energy_cpl_beats_sota_headlines := by
  unfold dark_energy_cpl_beats_sota_headlines; norm_num
theorem dark_energy_cpl_wa_negative : dark_energy_cpl_fsot_wa < (0 : ℝ) := by unfold dark_energy_cpl_fsot_wa; norm_num

theorem dark_energy_cpl_bundle :
    dark_energy_cpl_observable_count = 6 ∧
    dark_energy_cpl_pooled_median_error_pct < (0.5 : ℝ) ∧
    dark_energy_cpl_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold dark_energy_cpl_observable_count; norm_num
  · exact dark_energy_cpl_pooled_median_under_half_pct
  · exact dark_energy_cpl_beats_sota_headlines_pos

end
