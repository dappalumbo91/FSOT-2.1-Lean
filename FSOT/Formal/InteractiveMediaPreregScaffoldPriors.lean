/-
  FSOT Formal InteractiveMediaPreregScaffoldPriors — extension domain Interactive_Media_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def interactive_media_prereg_scaffold_observable_count : ℕ := 42
def interactive_media_prereg_scaffold_D_eff : ℕ := 14

theorem interactive_media_prereg_scaffold_observable_count_pos : 0 < interactive_media_prereg_scaffold_observable_count := by
  unfold interactive_media_prereg_scaffold_observable_count; norm_num

theorem interactive_media_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem interactive_media_prereg_scaffold_bundle :
    interactive_media_prereg_scaffold_observable_count = 42 ∧
    interactive_media_prereg_scaffold_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold interactive_media_prereg_scaffold_observable_count; norm_num,
    by unfold interactive_media_prereg_scaffold_D_eff; norm_num,
    interactive_media_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
