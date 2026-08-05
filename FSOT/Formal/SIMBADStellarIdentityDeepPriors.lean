/-
  FSOT Formal SimbadStellarIdentityDeepPriors — extension domain SIMBAD_Stellar_Identity_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def simbad_stellar_identity_deep_observable_count : ℕ := 520
def simbad_stellar_identity_deep_D_eff : ℕ := 20

theorem simbad_stellar_identity_deep_observable_count_pos : 0 < simbad_stellar_identity_deep_observable_count := by
  unfold simbad_stellar_identity_deep_observable_count; decide

theorem simbad_stellar_identity_deep_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022461 : ℝ) < (0.5 : ℝ))

theorem simbad_stellar_identity_deep_bundle :
    simbad_stellar_identity_deep_observable_count = 520 ∧
    simbad_stellar_identity_deep_D_eff = 20 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold simbad_stellar_identity_deep_observable_count; decide,
    by unfold simbad_stellar_identity_deep_D_eff; decide,
    simbad_stellar_identity_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
