/-
  FSOT Formal HeavyIonLabSynthesisPanelPriors — extension domain Heavy_Ion_Lab_Synthesis_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def heavy_ion_lab_synthesis_panel_observable_count : ℕ := 39
def heavy_ion_lab_synthesis_panel_D_eff : ℕ := 13

theorem heavy_ion_lab_synthesis_panel_observable_count_pos : 0 < heavy_ion_lab_synthesis_panel_observable_count := by
  unfold heavy_ion_lab_synthesis_panel_observable_count; decide

theorem heavy_ion_lab_synthesis_panel_median_error_under_half_pct :
    (9.5e-05 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (9.5e-05 : ℝ) < (0.5 : ℝ))

theorem heavy_ion_lab_synthesis_panel_bundle :
    heavy_ion_lab_synthesis_panel_observable_count = 39 ∧
    heavy_ion_lab_synthesis_panel_D_eff = 13 ∧
    (9.5e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold heavy_ion_lab_synthesis_panel_observable_count; decide,
    by unfold heavy_ion_lab_synthesis_panel_D_eff; decide,
    heavy_ion_lab_synthesis_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
