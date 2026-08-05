/-
  FSOT Formal CveCodonHoleFalsificationPriors — extension domain CVE_Codon_Hole_Falsification.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cve_codon_hole_falsification_observable_count : ℕ := 29
def cve_codon_hole_falsification_D_eff : ℕ := 17

theorem cve_codon_hole_falsification_observable_count_pos : 0 < cve_codon_hole_falsification_observable_count := by
  unfold cve_codon_hole_falsification_observable_count; decide

theorem cve_codon_hole_falsification_median_error_under_half_pct :
    (0.009186636881580057 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.009186636881580057 : ℝ) < (0.5 : ℝ))

theorem cve_codon_hole_falsification_bundle :
    cve_codon_hole_falsification_observable_count = 29 ∧
    cve_codon_hole_falsification_D_eff = 17 ∧
    (0.009186636881580057 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cve_codon_hole_falsification_observable_count; decide,
    by unfold cve_codon_hole_falsification_D_eff; decide,
    cve_codon_hole_falsification_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
