/-
  FSOT Formal CameoPriors — Genetics CAMEO symbolic folding certificates.

  Source: Genetics/fsot_cameo_results.csv + fluid-to-solid symbolic formula
  Generator: scripts/gen_cameo_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cameo_benchmark_count : ℕ := 130
def cameo_symbolic_node_count : ℕ := 5
def cameo_symbolic_mae_angstrom : ℝ := (8.85 : ℝ)

theorem cameo_benchmark_count_pos : 0 < cameo_benchmark_count := by
  unfold cameo_benchmark_count; norm_num

theorem cameo_symbolic_mae_positive : (0 : ℝ) < cameo_symbolic_mae_angstrom := by
  unfold cameo_symbolic_mae_angstrom; norm_num

/-- Bundle: CAMEO benchmarks and crystallized FSOT symbolic folding (molecular domain). -/
theorem cameo_symbolic_bundle :
    cameo_benchmark_count = 130 ∧
    cameo_symbolic_node_count = 5 ∧
    cameo_symbolic_mae_angstrom = (8.85 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold cameo_benchmark_count; norm_num,
    by unfold cameo_symbolic_node_count; norm_num,
    by unfold cameo_symbolic_mae_angstrom; norm_num,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
