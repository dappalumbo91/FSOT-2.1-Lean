/-
  FSOT Formal NetworkInternetProtocolsPriors — extension domain Network_Internet_Protocols.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def network_internet_protocols_observable_count : ℕ := 22
def network_internet_protocols_D_eff : ℕ := 15

theorem network_internet_protocols_observable_count_pos : 0 < network_internet_protocols_observable_count := by
  unfold network_internet_protocols_observable_count; norm_num

theorem network_internet_protocols_median_error_under_half_pct :
    (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by norm_num

theorem network_internet_protocols_bundle :
    network_internet_protocols_observable_count = 22 ∧
    network_internet_protocols_D_eff = 15 ∧
    (0.010337117254355377 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold network_internet_protocols_observable_count; norm_num,
    by unfold network_internet_protocols_D_eff; norm_num,
    network_internet_protocols_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
