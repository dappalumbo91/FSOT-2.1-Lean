/-
Copyright (c) 2026 Damian Arthur Palumbo. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Damian Arthur Palumbo

Top-level re-export for the Fluid Spacetime Omni-Theory (FSOT) Lean library.
This allows users to `import FSOT` and get both the executable Float layer
and the heavier Formal/Real layer.
-/

import FSOT.Scalar
import FSOT.Theorems
import FSOT.Formal.Scalar
import FSOT.Formal.Theorems
import FSOT.Formal.Cosmology
import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT

-- Re-export Formal-layer names into the top-level FSOT import path
export FSOT.Formal (
  FSOTParams raw_S scaled_S quirkMod term1 term3
  coherence_efficiency_positive
  get_domain_params compute_for_domain
  cosmological_term1_negative cosmological_term1_dominates_term3 cosmological_term2_eq_one
  raw_S_negative_when_term1_overcomes_defaults term2_default_eq_one
  dark_energy_term1_negative cmb_term1_negative
  cosmological_raw_S_negative dark_energy_raw_S_negative
  ai_raw_S_non_positive neural_raw_S_positive
  quantum_raw_S_positive cmb_raw_S_negative chemical_raw_S_positive
  c_cosm S_cosm_cached S_quant_cached
  alpha_s_MZ alpha_s_MZ_canonical h0_fsot h0_fsot_canonical t_cmb_fsot t_cmb_fsot_canonical
  n_s_fsot n_s_fsot_canonical omega_b_h2_fsot omega_b_h2_fsot_canonical
  alpha_s_MZ_approx_value h0_fsot_cached_approx_value t_cmb_fsot_cached_approx_value
  n_s_fsot_cached_approx_value omega_b_h2_fsot_cached_approx_value omega_b_h2_fsot_cached_pos
  p_base r_star_Mpc delta_lambda_cosm r_d_canonical r_d_approx_value
)

end FSOT
