#!/usr/bin/env python3
"""Generate Tier 7 FSOT Formal priors from experiment_synthesis registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
FORMAL = ROOT / "FSOT" / "Formal"


def _f(x: float) -> str:
    return repr(float(x))


def gen_neuron(registry: dict) -> str:
    n = registry.get("experiment_synthesis", {}).get("neuron_hybrid_lab", {})
    specimen = int(n.get("specimen_id") or 0)
    fi_pts = int(n.get("fi_point_count") or 0)
    mean_err = float(n.get("mean_rel_err") or 1.0)
    conf = float(n.get("verifier_confidence") or 0.0)
    g0 = float(n.get("soma_gain_base") or 0.0)
    g1 = float(n.get("soma_gain_scalar") or 0.0)
    k_cache = float(n.get("neuron_K_cached") or 0.0)
    neuro_s = float(n.get("canonical_neuroscience_S") or 0.0)

    return f"""/-
  FSOT Formal NeuronHybridPriors — Allen hybrid neuron + canonical FSOT bridge.

  Source: nuron/cell data/inconsistency_rerun_report.json
  Generator: scripts/gen_experiment_synthesis_lean.py

  Legacy scalar: micro_scalar_v16 (deprecated projection).
  Canon scalar: raw_S via Neuroscience / neural domain.
  Calibrated somatic gains (g₀, g₁) are empirical Allen-fit layer — not Layer-1 free params.
-/

import FSOT.Formal.Domains
import FSOT.Formal.Lab
import FSOT.Formal.Bounds

namespace FSOT.Formal

noncomputable section

open Real

def neuron_allen_specimen_id : ℕ := {specimen}
def neuron_fi_point_count : ℕ := {fi_pts}
def neuron_mean_rel_err : ℝ := ({_f(mean_err)} : ℝ)
def neuron_verifier_confidence : ℝ := ({_f(conf)} : ℝ)
def neuron_K_cached : ℝ := ({_f(k_cache)} : ℝ)
def neuron_soma_gain_base : ℝ := ({_f(g0)} : ℝ)
def neuron_soma_gain_scalar : ℝ := ({_f(g1)} : ℝ)
def neuron_canonical_neuroscience_S : ℝ := ({_f(neuro_s)} : ℝ)

theorem neuron_fi_point_count_pos : 0 < neuron_fi_point_count := by
  unfold neuron_fi_point_count; norm_num

theorem neuron_mean_rel_err_lt_fifteen_pct : neuron_mean_rel_err < (0.15 : ℝ) := by
  unfold neuron_mean_rel_err; norm_num

theorem neuron_verifier_confidence_gt_ninety_pct : (0.90 : ℝ) < neuron_verifier_confidence := by
  unfold neuron_verifier_confidence; norm_num

theorem neuron_K_matches_thalamic_gate : |k - neuron_K_cached| < (5e-4 : ℝ) := by
  unfold neuron_K_cached
  exact thalamic_K_matches_formal_k

theorem neuron_canonical_neuroscience_S_positive : (0 : ℝ) < neuron_canonical_neuroscience_S := by
  unfold neuron_canonical_neuroscience_S; norm_num

/-- Bundle: Allen hybrid FI fit + K alignment + neural-domain canon S (Python oracle). -/
theorem neuron_hybrid_priors_bundle :
    neuron_allen_specimen_id = {specimen} ∧
    neuron_fi_point_count = {fi_pts} ∧
    neuron_mean_rel_err < (0.15 : ℝ) ∧
    (0.90 : ℝ) < neuron_verifier_confidence ∧
    |k - neuron_K_cached| < (5e-4 : ℝ) ∧
    (0 : ℝ) < neuron_canonical_neuroscience_S ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold neuron_allen_specimen_id; norm_num,
    by unfold neuron_fi_point_count; norm_num,
    neuron_mean_rel_err_lt_fifteen_pct,
    neuron_verifier_confidence_gt_ninety_pct,
    neuron_K_matches_thalamic_gate,
    neuron_canonical_neuroscience_S_positive,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def gen_aether(registry: dict) -> str:
    a = registry.get("experiment_synthesis", {}).get("aether_prime_lab", {})
    rows = int(a.get("distill_row_count") or 0)
    ops = int(a.get("solver_op_count") or 6)
    rejects = int(a.get("verifier_reject_count") or 0)
    psi = float(a.get("psi_con_solver") or 0)
    eta = float(a.get("eta_eff_solver") or 0)
    ga = float(a.get("golden_angle_solver_deg") or 0)

    return f"""/-
  FSOT Formal AetherPrimePriors — deterministic solver + verifier distill certificates.

  Source: Aether Prime/fsot_verifier_distill_small.jsonl
  Generator: scripts/gen_experiment_synthesis_lean.py

  ψ_con and η_eff solver values align with FSOT.Formal.Bounds interval certificates.
  fsot_alpha in solver config is deprecated Layer-1 alias (audit only).
-/

import FSOT.Formal.Bounds

namespace FSOT.Formal

noncomputable section

open Real

def aether_distill_row_count : ℕ := {rows}
def aether_solver_op_count : ℕ := {ops}
def aether_verifier_reject_count : ℕ := {rejects}
def aether_psi_con_solver : ℝ := ({_f(psi)} : ℝ)
def aether_eta_eff_solver : ℝ := ({_f(eta)} : ℝ)
def aether_golden_angle_solver_deg : ℝ := ({_f(ga)} : ℝ)

theorem aether_distill_row_count_pos : 0 < aether_distill_row_count := by
  unfold aether_distill_row_count; norm_num

theorem aether_solver_op_count_eq_six : aether_solver_op_count = 6 := by
  unfold aether_solver_op_count; norm_num

theorem aether_psi_con_solver_in_bounds : (0.632 : ℝ) < aether_psi_con_solver ∧ aether_psi_con_solver < (0.633 : ℝ) := by
  unfold aether_psi_con_solver
  constructor <;> norm_num

theorem aether_eta_eff_solver_in_bounds : (0.466 : ℝ) < aether_eta_eff_solver ∧ aether_eta_eff_solver < (0.467 : ℝ) := by
  unfold aether_eta_eff_solver
  constructor <;> norm_num

theorem aether_golden_angle_gt_137 : (137 : ℝ) < aether_golden_angle_solver_deg := by
  unfold aether_golden_angle_solver_deg; norm_num

/-- Bundle: 6-op solver + distill corpus + ψ_con/η_eff alignment with formal bounds. -/
theorem aether_prime_priors_bundle :
    aether_distill_row_count = {rows} ∧
    aether_solver_op_count = 6 ∧
    (0.632 : ℝ) < aether_psi_con_solver ∧
    aether_psi_con_solver < (0.633 : ℝ) ∧
    (0.466 : ℝ) < aether_eta_eff_solver ∧
    aether_eta_eff_solver < (0.467 : ℝ) ∧
    (137 : ℝ) < aether_golden_angle_solver_deg ∧
    (0 : ℕ) < aether_distill_row_count := by
  refine ⟨
    by unfold aether_distill_row_count; norm_num,
    aether_solver_op_count_eq_six,
    aether_psi_con_solver_in_bounds.1,
    aether_psi_con_solver_in_bounds.2,
    aether_eta_eff_solver_in_bounds.1,
    aether_eta_eff_solver_in_bounds.2,
    aether_golden_angle_gt_137,
    aether_distill_row_count_pos
  ⟩

end

end FSOT.Formal
"""


def gen_magic(registry: dict) -> str:
    m = registry.get("experiment_synthesis", {}).get("magic_circle_lab", {})
    min_res = float(m.get("min_resonance_for_emergence") or 0)
    internal = float(m.get("internalized_threshold") or 0)
    imb = float(m.get("imbalance_penalty_max") or 0)
    backlash = float(m.get("backlash_risk_threshold_high") or 0)

    return f"""/-
  FSOT Formal MagicCirclePriors — glyph emergence boundary certificates.

  Source: fsot magic circle/fsot_glyph_config.json
  Generator: scripts/gen_experiment_synthesis_lean.py

  Resonance layer is FSOT-structured emergence math (not raw_S); bounds certified here.
-/

import FSOT.Formal.TrinaryFluidPriors

namespace FSOT.Formal

noncomputable section

open Real

def magic_min_resonance_for_emergence : ℝ := ({_f(min_res)} : ℝ)
def magic_internalized_threshold : ℝ := ({_f(internal)} : ℝ)
def magic_imbalance_penalty_max : ℝ := ({_f(imb)} : ℝ)
def magic_backlash_risk_threshold_high : ℝ := ({_f(backlash)} : ℝ)

theorem magic_min_resonance_lt_internalized :
    magic_min_resonance_for_emergence < magic_internalized_threshold := by
  unfold magic_min_resonance_for_emergence magic_internalized_threshold; norm_num

theorem magic_imbalance_penalty_in_unit_interval :
    (0 : ℝ) < magic_imbalance_penalty_max ∧ magic_imbalance_penalty_max ≤ (1 : ℝ) := by
  unfold magic_imbalance_penalty_max; constructor <;> norm_num

theorem magic_backlash_threshold_in_unit_interval :
    (0 : ℝ) < magic_backlash_risk_threshold_high ∧ magic_backlash_risk_threshold_high < (1 : ℝ) := by
  unfold magic_backlash_risk_threshold_high; constructor <;> norm_num

/-- Bundle: glyph stabilization thresholds + trinary fluid pathway anchor. -/
theorem magic_circle_priors_bundle :
    magic_min_resonance_for_emergence < magic_internalized_threshold ∧
    (0 : ℝ) < magic_imbalance_penalty_max ∧
    magic_imbalance_penalty_max ≤ (1 : ℝ) ∧
    (0 : ℝ) < magic_backlash_risk_threshold_high ∧
    magic_backlash_risk_threshold_high < (1 : ℝ) ∧
    trinary_metatron_pathways = 27 := by
  refine ⟨
    magic_min_resonance_lt_internalized,
    magic_imbalance_penalty_in_unit_interval.1,
    magic_imbalance_penalty_in_unit_interval.2,
    magic_backlash_threshold_in_unit_interval.1,
    magic_backlash_threshold_in_unit_interval.2,
    by unfold trinary_metatron_pathways; norm_num
  ⟩

end

end FSOT.Formal
"""


def gen_neuron_cohort(registry: dict) -> str:
    cohort = registry.get("neuron_cohort_lab", {})
    proxy = cohort.get("cohort_fi_proxy", {})
    hero = cohort.get("hero_certified_fi", {})
    bridge = cohort.get("neurolab_smiles_bridge", {})
    canon_bridge = cohort.get("canonical_scalar_bridge", {})
    n_cells = int(proxy.get("cell_count") or 0)
    med_err = float(proxy.get("fi_median_rel_err") or 1.0)
    pearson = float(proxy.get("fi_pearson_r") or 0.0)
    hero_err = float(hero.get("mean_rel_err") or 1.0)
    hero_conf = float(hero.get("verifier_confidence") or 0.0)
    s_min = float(proxy.get("canonical_scalar_min") or 0.0)
    canon_err = float(canon_bridge.get("hero_canonical_mean_rel_err") or 1.0)
    canon_delta = float(canon_bridge.get("canonical_vs_certified_delta") or 1.0)
    bridge_scale = float(canon_bridge.get("bridge_scale") or 0.0)
    smiles_n = int(bridge.get("smiles_mapped_records") or 0)
    strict_n = int(bridge.get("strict_empirical_records") or 0)
    brain_n = int(bridge.get("brain_component_priors_count") or 0)

    return f"""/-
  FSOT Formal NeuronCohortPriors — Allen 2333-cell catalog + NeuroLab/SMILES bridge.

  Source: data/neuron_cohort_report.json
  Generator: scripts/gen_experiment_synthesis_lean.py

  Cohort FI proxy: cross-cell slope×stimulus model (no per-cell refit).
  Hero certified FI: calibrated hybrid on specimen 324257146 (Sst interneuron).
  Canonical scalar bridge v2: oracle alpha/psi_con/eta_eff hybrid-structure modulation.
-/

import FSOT.Formal.Lab
import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def allen_cohort_cell_count : ℕ := {n_cells}
def allen_cohort_fi_median_rel_err : ℝ := ({_f(med_err)} : ℝ)
def allen_cohort_fi_pearson_r : ℝ := ({_f(pearson)} : ℝ)
def hero_certified_fi_mean_rel_err : ℝ := ({_f(hero_err)} : ℝ)
def hero_certified_verifier_confidence : ℝ := ({_f(hero_conf)} : ℝ)
def cohort_canonical_scalar_min : ℝ := ({_f(s_min)} : ℝ)
def hero_canonical_bridge_mean_rel_err : ℝ := ({_f(canon_err)} : ℝ)
def hero_canonical_bridge_delta : ℝ := ({_f(canon_delta)} : ℝ)
def canonical_bridge_scale : ℝ := ({_f(bridge_scale)} : ℝ)
def neurolab_smiles_mapped_records : ℕ := {smiles_n}
def neurolab_strict_empirical_records : ℕ := {strict_n}
def neurolab_brain_component_count : ℕ := {brain_n}

theorem allen_cohort_cell_count_pos : 0 < allen_cohort_cell_count := by
  unfold allen_cohort_cell_count; norm_num

theorem allen_cohort_fi_median_rel_err_lt_thirty_pct : allen_cohort_fi_median_rel_err < (0.30 : ℝ) := by
  unfold allen_cohort_fi_median_rel_err; norm_num

theorem allen_cohort_fi_pearson_r_gt_fifty_five : (0.55 : ℝ) < allen_cohort_fi_pearson_r := by
  unfold allen_cohort_fi_pearson_r; norm_num

theorem hero_certified_fi_mean_rel_err_lt_fifteen_pct : hero_certified_fi_mean_rel_err < (0.15 : ℝ) := by
  unfold hero_certified_fi_mean_rel_err; norm_num

theorem hero_certified_verifier_confidence_gt_ninety_pct : (0.90 : ℝ) < hero_certified_verifier_confidence := by
  unfold hero_certified_verifier_confidence; norm_num

theorem cohort_canonical_scalar_min_positive : (0 : ℝ) < cohort_canonical_scalar_min := by
  unfold cohort_canonical_scalar_min; norm_num

theorem hero_canonical_bridge_mean_rel_err_lt_twelve_pct : hero_canonical_bridge_mean_rel_err < (0.12 : ℝ) := by
  unfold hero_canonical_bridge_mean_rel_err; norm_num

theorem hero_canonical_bridge_delta_lt_five_pct : hero_canonical_bridge_delta < (0.05 : ℝ) := by
  unfold hero_canonical_bridge_delta; norm_num

theorem canonical_bridge_scale_gt_one : (1 : ℝ) < canonical_bridge_scale := by
  unfold canonical_bridge_scale; norm_num

theorem neurolab_smiles_mapped_records_pos : 0 < neurolab_smiles_mapped_records := by
  unfold neurolab_smiles_mapped_records; norm_num

theorem neurolab_strict_empirical_records_large : (7900 : ℕ) < neurolab_strict_empirical_records := by
  unfold neurolab_strict_empirical_records; norm_num

/-- Bundle: 2166-cell Allen cohort + hero FI + SMILES/NeuroLab bridge certificates. -/
theorem neuron_cohort_priors_bundle :
    allen_cohort_cell_count = {n_cells} ∧
    allen_cohort_fi_median_rel_err < (0.30 : ℝ) ∧
    (0.55 : ℝ) < allen_cohort_fi_pearson_r ∧
    hero_certified_fi_mean_rel_err < (0.15 : ℝ) ∧
    (0.90 : ℝ) < hero_certified_verifier_confidence ∧
    hero_canonical_bridge_mean_rel_err < (0.12 : ℝ) ∧
    hero_canonical_bridge_delta < (0.05 : ℝ) ∧
    (1 : ℝ) < canonical_bridge_scale ∧
    (0 : ℝ) < cohort_canonical_scalar_min ∧
    neurolab_smiles_mapped_records = {smiles_n} ∧
    (7900 : ℕ) < neurolab_strict_empirical_records ∧
    neurolab_brain_component_count = {brain_n} ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold allen_cohort_cell_count; norm_num,
    allen_cohort_fi_median_rel_err_lt_thirty_pct,
    allen_cohort_fi_pearson_r_gt_fifty_five,
    hero_certified_fi_mean_rel_err_lt_fifteen_pct,
    hero_certified_verifier_confidence_gt_ninety_pct,
    hero_canonical_bridge_mean_rel_err_lt_twelve_pct,
    hero_canonical_bridge_delta_lt_five_pct,
    canonical_bridge_scale_gt_one,
    cohort_canonical_scalar_min_positive,
    by unfold neurolab_smiles_mapped_records; norm_num,
    neurolab_strict_empirical_records_large,
    by unfold neurolab_brain_component_count; norm_num,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def gen_synthesis(registry: dict) -> str:
    syn = registry.get("experiment_synthesis", {})
    llm = syn.get("llm_experiments_lab", {})
    llm_count = int(llm.get("project_folder_count") or 0)
    neuron = syn.get("neuron_hybrid_lab", {})
    aether = syn.get("aether_prime_lab", {})
    magic = syn.get("magic_circle_lab", {})
    cohort = registry.get("neuron_cohort_lab", {})
    approach_count = sum(
        1 for lab in (neuron, aether, magic, cohort) if lab.get("present")
    )

    return f"""/-
  FSOT Formal ExperimentSynthesisPriors — verified math floor from all intelligence experiments.

  Source: data/experiment_synthesis_manifest.yaml
  Generator: scripts/gen_experiment_synthesis_lean.py

  Tier 7 synthesis: correct project math against Lean + fsot_compute canon.
-/

import FSOT.Formal.Domains
import FSOT.Formal.NeuronHybridPriors
import FSOT.Formal.NeuronCohortPriors
import FSOT.Formal.AetherPrimePriors
import FSOT.Formal.MagicCirclePriors

namespace FSOT.Formal

noncomputable section

def experiment_synthesis_approach_count : ℕ := {approach_count}
def experiment_llm_project_folder_count : ℕ := {llm_count}

theorem experiment_synthesis_approach_count_pos : 0 < experiment_synthesis_approach_count := by
  unfold experiment_synthesis_approach_count; norm_num

theorem experiment_llm_project_count_pos : 0 < experiment_llm_project_folder_count := by
  unfold experiment_llm_project_folder_count; norm_num

/-- Bundle: neuron cohort + hybrid + Aether Prime + magic circle synthesis floor. -/
theorem experiment_synthesis_priors_bundle :
    experiment_synthesis_approach_count = {approach_count} ∧
    experiment_llm_project_folder_count = {llm_count} ∧
    allen_cohort_fi_median_rel_err < (0.30 : ℝ) ∧
    hero_certified_fi_mean_rel_err < (0.15 : ℝ) ∧
    aether_distill_row_count = {int(aether.get('distill_row_count') or 0)} ∧
    magic_min_resonance_for_emergence < magic_internalized_threshold ∧
    (7900 : ℕ) < neurolab_strict_empirical_records ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold experiment_synthesis_approach_count; norm_num,
    by unfold experiment_llm_project_folder_count; norm_num,
    allen_cohort_fi_median_rel_err_lt_thirty_pct,
    hero_certified_fi_mean_rel_err_lt_fifteen_pct,
    by unfold aether_distill_row_count; norm_num,
    magic_min_resonance_lt_internalized,
    neurolab_strict_empirical_records_large,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Tier 7 experiment synthesis Lean modules")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))

    outputs = {
        "NeuronHybridPriors.lean": gen_neuron(registry),
        "NeuronCohortPriors.lean": gen_neuron_cohort(registry),
        "AetherPrimePriors.lean": gen_aether(registry),
        "MagicCirclePriors.lean": gen_magic(registry),
        "ExperimentSynthesisPriors.lean": gen_synthesis(registry),
    }
    for name, content in outputs.items():
        path = FORMAL / name
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())