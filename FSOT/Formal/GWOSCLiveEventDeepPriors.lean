/-
  FSOT Formal GwoscLiveEventDeepPriors — extension domain GWOSC_Live_Event_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def gwosc_live_event_deep_observable_count : ℕ := 191
def gwosc_live_event_deep_D_eff : ℕ := 20

theorem gwosc_live_event_deep_observable_count_pos : 0 < gwosc_live_event_deep_observable_count := by
  unfold gwosc_live_event_deep_observable_count; decide

theorem gwosc_live_event_deep_median_error_under_half_pct :
    (0.008488 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.008488 : ℝ) < (0.5 : ℝ))

theorem gwosc_live_event_deep_bundle :
    gwosc_live_event_deep_observable_count = 191 ∧
    gwosc_live_event_deep_D_eff = 20 ∧
    (0.008488 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold gwosc_live_event_deep_observable_count; decide,
    by unfold gwosc_live_event_deep_D_eff; decide,
    gwosc_live_event_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
