/-
  FSOT Formal ExperimentSynthesisPriors — verified math floor from all intelligence experiments.

  Source: data/experiment_synthesis_manifest.yaml
  Generator: scripts/gen_experiment_synthesis_lean.py

  Tier 7–8 synthesis: corrected project math + Allen strata against Lean + fsot_compute canon.
-/

import FSOT.Formal.Domains
import FSOT.Formal.NeuronHybridPriors
import FSOT.Formal.NeuronCohortPriors
import FSOT.Formal.NeuronCohortStrataPriors
import FSOT.Formal.AetherPrimePriors
import FSOT.Formal.MagicCirclePriors

namespace FSOT.Formal

noncomputable section

def experiment_synthesis_approach_count : ℕ := 5
def experiment_llm_project_folder_count : ℕ := 21

theorem experiment_synthesis_approach_count_pos : 0 < experiment_synthesis_approach_count := by
  unfold experiment_synthesis_approach_count; norm_num

theorem experiment_llm_project_count_pos : 0 < experiment_llm_project_folder_count := by
  unfold experiment_llm_project_folder_count; norm_num

/-- Bundle: neuron cohort + hybrid + Aether Prime + magic circle synthesis floor. -/
theorem experiment_synthesis_priors_bundle :
    experiment_synthesis_approach_count = 5 ∧
    experiment_llm_project_folder_count = 21 ∧
    allen_cohort_fi_median_rel_err < (0.30 : ℝ) ∧
    hero_certified_fi_mean_rel_err < (0.15 : ℝ) ∧
    (2100 : ℕ) < held_out_cell_count ∧
    aether_distill_row_count = 120 ∧
    magic_min_resonance_for_emergence < magic_internalized_threshold ∧
    (7900 : ℕ) < neurolab_strict_empirical_records ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold experiment_synthesis_approach_count; norm_num,
    by unfold experiment_llm_project_folder_count; norm_num,
    allen_cohort_fi_median_rel_err_lt_thirty_pct,
    hero_certified_fi_mean_rel_err_lt_fifteen_pct,
    held_out_cell_count_large,
    by unfold aether_distill_row_count; norm_num,
    magic_min_resonance_lt_internalized,
    neurolab_strict_empirical_records_large,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
