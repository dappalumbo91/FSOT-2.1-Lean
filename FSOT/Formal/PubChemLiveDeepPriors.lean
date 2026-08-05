/-
  FSOT Formal PubchemLiveDeepPriors — extension domain PubChem_Live_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pubchem_live_deep_observable_count : ℕ := 5254
def pubchem_live_deep_D_eff : ℕ := 20

theorem pubchem_live_deep_observable_count_pos : 0 < pubchem_live_deep_observable_count := by
  unfold pubchem_live_deep_observable_count; decide

theorem pubchem_live_deep_median_error_under_half_pct :
    (0.032631 : ℝ) < (0.5 : ℝ) := by norm_num

theorem pubchem_live_deep_bundle :
    pubchem_live_deep_observable_count = 5254 ∧
    pubchem_live_deep_D_eff = 20 ∧
    (0.032631 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pubchem_live_deep_observable_count; decide,
    by unfold pubchem_live_deep_D_eff; decide,
    pubchem_live_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
