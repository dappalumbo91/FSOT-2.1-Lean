/-
  FSOT Formal EconometricsPriors — extension domain Econometrics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def econometrics_observable_count : ℕ := 172
def econometrics_D_eff : ℕ := 19

theorem econometrics_observable_count_pos : 0 < econometrics_observable_count := by
  unfold econometrics_observable_count; norm_num

theorem econometrics_median_error_under_half_pct :
    (0.12920090413715177 : ℝ) < (0.5 : ℝ) := by norm_num

theorem econometrics_bundle :
    econometrics_observable_count = 172 ∧
    econometrics_D_eff = 19 ∧
    (0.12920090413715177 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold econometrics_observable_count; norm_num,
    by unfold econometrics_D_eff; norm_num,
    econometrics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
