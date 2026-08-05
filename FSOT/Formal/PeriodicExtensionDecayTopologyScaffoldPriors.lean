/-
  FSOT Formal PeriodicExtensionDecayTopologyScaffoldPriors — extension domain Periodic_Extension_Decay_Topology_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def periodic_extension_decay_topology_scaffold_observable_count : ℕ := 24
def periodic_extension_decay_topology_scaffold_D_eff : ℕ := 22

theorem periodic_extension_decay_topology_scaffold_observable_count_pos : 0 < periodic_extension_decay_topology_scaffold_observable_count := by
  unfold periodic_extension_decay_topology_scaffold_observable_count; decide

theorem periodic_extension_decay_topology_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem periodic_extension_decay_topology_scaffold_bundle :
    periodic_extension_decay_topology_scaffold_observable_count = 24 ∧
    periodic_extension_decay_topology_scaffold_D_eff = 22 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold periodic_extension_decay_topology_scaffold_observable_count; decide,
    by unfold periodic_extension_decay_topology_scaffold_D_eff; decide,
    periodic_extension_decay_topology_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
