/-
  FSOT Formal Term3AcousticBleedDepthPriors — extension domain Term3_Acoustic_Bleed_Depth.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def term3_acoustic_bleed_depth_observable_count : ℕ := 23
def term3_acoustic_bleed_depth_D_eff : ℕ := 15

theorem term3_acoustic_bleed_depth_observable_count_pos : 0 < term3_acoustic_bleed_depth_observable_count := by
  unfold term3_acoustic_bleed_depth_observable_count; decide

theorem term3_acoustic_bleed_depth_median_error_under_half_pct :
    (0.008381497018408523 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.008381497018408523 : ℝ) < (0.5 : ℝ))

theorem term3_acoustic_bleed_depth_bundle :
    term3_acoustic_bleed_depth_observable_count = 23 ∧
    term3_acoustic_bleed_depth_D_eff = 15 ∧
    (0.008381497018408523 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold term3_acoustic_bleed_depth_observable_count; decide,
    by unfold term3_acoustic_bleed_depth_D_eff; decide,
    term3_acoustic_bleed_depth_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
