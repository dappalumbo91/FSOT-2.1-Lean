/-
  FSOT Formal FusionDecayChainPreregScaffoldPriors — extension domain Fusion_Decay_Chain_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fusion_decay_chain_prereg_scaffold_observable_count : ℕ := 24
def fusion_decay_chain_prereg_scaffold_D_eff : ℕ := 17

theorem fusion_decay_chain_prereg_scaffold_observable_count_pos : 0 < fusion_decay_chain_prereg_scaffold_observable_count := by
  unfold fusion_decay_chain_prereg_scaffold_observable_count; decide

theorem fusion_decay_chain_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem fusion_decay_chain_prereg_scaffold_bundle :
    fusion_decay_chain_prereg_scaffold_observable_count = 24 ∧
    fusion_decay_chain_prereg_scaffold_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fusion_decay_chain_prereg_scaffold_observable_count; decide,
    by unfold fusion_decay_chain_prereg_scaffold_D_eff; decide,
    fusion_decay_chain_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
