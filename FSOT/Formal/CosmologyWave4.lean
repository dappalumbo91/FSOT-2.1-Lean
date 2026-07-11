/-
  DEPRECATED — use FSOT.Formal.CosmologyWave4Priors (per-wave Priors path).
  This module re-exports the Priors bundle for backward-compatible imports only.
  Generator: scripts/gen_cosmology_wave4_lean.py (deprecation shim)
-/

import FSOT.Formal.CosmologyWave4Priors

namespace FSOT.Formal

noncomputable section

open Real

/-- Legacy alias: Wave-4 observable count (see `cosmology_wave4_observable_count`). -/
def wave4_observable_count : ℕ := cosmology_wave4_observable_count

theorem wave4_observable_count_pos : 0 < wave4_observable_count := by
  unfold wave4_observable_count cosmology_wave4_observable_count; norm_num

end

end FSOT.Formal