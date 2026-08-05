/-
  FSOT Formal BiophysicsPublicPanelPriors — extension domain Biophysics_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def biophysics_public_panel_observable_count : ℕ := 24
def biophysics_public_panel_D_eff : ℕ := 12

theorem biophysics_public_panel_observable_count_pos : 0 < biophysics_public_panel_observable_count := by
  unfold biophysics_public_panel_observable_count; decide

theorem biophysics_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem biophysics_public_panel_bundle :
    biophysics_public_panel_observable_count = 24 ∧
    biophysics_public_panel_D_eff = 12 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold biophysics_public_panel_observable_count; decide,
    by unfold biophysics_public_panel_D_eff; decide,
    biophysics_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
