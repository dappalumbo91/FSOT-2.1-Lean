/-
  FSOT Formal StsciMastTelescopePriors — Tier 79 STScI MAST (STScI_MAST_Telescope_Panel).
  Generator: scripts/gen_tier79_telescope_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def stsci_mast_telescope_observable_count : ℕ := 377
def stsci_mast_telescope_median_error_pct : ℝ := (0.022461 : ℝ)
def stsci_mast_telescope_D_eff : ℕ := 21

theorem stsci_mast_telescope_observable_count_pos : 0 < stsci_mast_telescope_observable_count := by
  unfold stsci_mast_telescope_observable_count; decide

theorem stsci_mast_telescope_median_error_under_five_pct :
    stsci_mast_telescope_median_error_pct < (5 : ℝ) := by
  unfold stsci_mast_telescope_median_error_pct; norm_num

theorem stsci_mast_telescope_bundle :
    stsci_mast_telescope_observable_count = 377 ∧
    stsci_mast_telescope_D_eff = 21 ∧
    stsci_mast_telescope_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold stsci_mast_telescope_observable_count; decide,
    by unfold stsci_mast_telescope_D_eff; decide,
    stsci_mast_telescope_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
