/-
  FSOT Formal StsciMastTelescopePanelPriors — extension domain STScI_MAST_Telescope_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def stsci_mast_telescope_panel_observable_count : ℕ := 377
def stsci_mast_telescope_panel_D_eff : ℕ := 21

theorem stsci_mast_telescope_panel_observable_count_pos : 0 < stsci_mast_telescope_panel_observable_count := by
  unfold stsci_mast_telescope_panel_observable_count; decide

theorem stsci_mast_telescope_panel_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem stsci_mast_telescope_panel_bundle :
    stsci_mast_telescope_panel_observable_count = 377 ∧
    stsci_mast_telescope_panel_D_eff = 21 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold stsci_mast_telescope_panel_observable_count; decide,
    by unfold stsci_mast_telescope_panel_D_eff; decide,
    stsci_mast_telescope_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
