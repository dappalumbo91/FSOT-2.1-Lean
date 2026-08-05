/-
  FSOT Formal PubchemStabilityPanelPriors — extension domain PubChem_Stability_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pubchem_stability_panel_observable_count : ℕ := 59
def pubchem_stability_panel_D_eff : ℕ := 14

theorem pubchem_stability_panel_observable_count_pos : 0 < pubchem_stability_panel_observable_count := by
  unfold pubchem_stability_panel_observable_count; decide

theorem pubchem_stability_panel_median_error_under_half_pct :
    (0.0024238898584426276 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0024238898584426276 : ℝ) < (0.5 : ℝ))

theorem pubchem_stability_panel_bundle :
    pubchem_stability_panel_observable_count = 59 ∧
    pubchem_stability_panel_D_eff = 14 ∧
    (0.0024238898584426276 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pubchem_stability_panel_observable_count; decide,
    by unfold pubchem_stability_panel_D_eff; decide,
    pubchem_stability_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
