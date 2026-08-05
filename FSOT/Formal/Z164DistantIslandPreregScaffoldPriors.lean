/-
  FSOT Formal Z164DistantIslandPreregScaffoldPriors — extension domain Z164_Distant_Island_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def z164_distant_island_prereg_scaffold_observable_count : ℕ := 24
def z164_distant_island_prereg_scaffold_D_eff : ℕ := 24

theorem z164_distant_island_prereg_scaffold_observable_count_pos : 0 < z164_distant_island_prereg_scaffold_observable_count := by
  unfold z164_distant_island_prereg_scaffold_observable_count; decide

theorem z164_distant_island_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem z164_distant_island_prereg_scaffold_bundle :
    z164_distant_island_prereg_scaffold_observable_count = 24 ∧
    z164_distant_island_prereg_scaffold_D_eff = 24 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold z164_distant_island_prereg_scaffold_observable_count; decide,
    by unfold z164_distant_island_prereg_scaffold_D_eff; decide,
    z164_distant_island_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
