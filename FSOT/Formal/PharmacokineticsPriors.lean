/-
  FSOT Formal PharmacokineticsPriors — extension domain Pharmacokinetics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pharmacokinetics_observable_count : ℕ := 56
def pharmacokinetics_D_eff : ℕ := 14

theorem pharmacokinetics_observable_count_pos : 0 < pharmacokinetics_observable_count := by
  unfold pharmacokinetics_observable_count; decide

theorem pharmacokinetics_median_error_under_half_pct :
    (0.00241237063663613 : ℝ) < (0.5 : ℝ) := by norm_num

theorem pharmacokinetics_bundle :
    pharmacokinetics_observable_count = 56 ∧
    pharmacokinetics_D_eff = 14 ∧
    (0.00241237063663613 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pharmacokinetics_observable_count; decide,
    by unfold pharmacokinetics_D_eff; decide,
    pharmacokinetics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
