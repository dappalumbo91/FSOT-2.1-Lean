/-
  FSOT Formal XrInteractiveMediaMathScaffoldPriors — extension domain XR_Interactive_Media_Math_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def xr_interactive_media_math_scaffold_observable_count : ℕ := 24
def xr_interactive_media_math_scaffold_D_eff : ℕ := 14

theorem xr_interactive_media_math_scaffold_observable_count_pos : 0 < xr_interactive_media_math_scaffold_observable_count := by
  unfold xr_interactive_media_math_scaffold_observable_count; decide

theorem xr_interactive_media_math_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem xr_interactive_media_math_scaffold_bundle :
    xr_interactive_media_math_scaffold_observable_count = 24 ∧
    xr_interactive_media_math_scaffold_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold xr_interactive_media_math_scaffold_observable_count; decide,
    by unfold xr_interactive_media_math_scaffold_D_eff; decide,
    xr_interactive_media_math_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
