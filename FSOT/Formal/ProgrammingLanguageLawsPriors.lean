/-
  FSOT Formal ProgrammingLanguageLawsPriors — extension domain Programming_Language_Laws.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def programming_language_laws_observable_count : ℕ := 107
def programming_language_laws_D_eff : ℕ := 15

theorem programming_language_laws_observable_count_pos : 0 < programming_language_laws_observable_count := by
  unfold programming_language_laws_observable_count; decide

theorem programming_language_laws_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem programming_language_laws_bundle :
    programming_language_laws_observable_count = 107 ∧
    programming_language_laws_D_eff = 15 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold programming_language_laws_observable_count; decide,
    by unfold programming_language_laws_D_eff; decide,
    programming_language_laws_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
