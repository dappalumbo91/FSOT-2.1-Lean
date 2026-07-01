#!/usr/bin/env python3
"""Generate FSOT/Formal/NeuronCohortTrainHoldoutPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "neuron_cohort_train_holdout.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "NeuronCohortTrainHoldoutPriors.lean"


def build_lean(doc: dict) -> str:
    tr = doc.get("train") or {}
    ho = doc.get("holdout") or {}
    tr_n = int(tr.get("cell_count") or 0)
    ho_n = int(ho.get("cell_count") or 0)
    tr_med = float(tr.get("fi_median_rel_err") or 1.0)
    ho_med = float(ho.get("fi_median_rel_err") or 1.0)
    ho_r = float(ho.get("fi_pearson_r") or 0.0)
    tr_gate = max(0, tr_n - 1)
    ho_gate = max(0, ho_n - 1)
    return f"""/-
  FSOT Formal NeuronCohortTrainHoldoutPriors — Tier 14 train/holdout regression gates.
  Source: data/neuron_cohort_train_holdout.json
  Generator: scripts/gen_neuron_cohort_train_holdout_lean.py
-/

import FSOT.Formal.NeuronCohortPriors

namespace FSOT.Formal

noncomputable section

open Real

def neuron_train_cell_count : ℕ := {tr_n}
def neuron_holdout_cell_count : ℕ := {ho_n}
def neuron_train_fi_median_rel_err : ℝ := ({tr_med} : ℝ)
def neuron_holdout_fi_median_rel_err : ℝ := ({ho_med} : ℝ)
def neuron_holdout_fi_pearson_r : ℝ := ({ho_r} : ℝ)

theorem neuron_train_cell_count_pos : 0 < neuron_train_cell_count := by
  unfold neuron_train_cell_count; norm_num

theorem neuron_holdout_cell_count_pos : 0 < neuron_holdout_cell_count := by
  unfold neuron_holdout_cell_count; norm_num

theorem neuron_train_cell_count_ge_gate : ({tr_gate} : ℕ) < neuron_train_cell_count := by
  unfold neuron_train_cell_count; norm_num

theorem neuron_holdout_cell_count_ge_gate : ({ho_gate} : ℕ) < neuron_holdout_cell_count := by
  unfold neuron_holdout_cell_count; norm_num

theorem neuron_train_fi_median_lt_thirty_pct : neuron_train_fi_median_rel_err < (0.30 : ℝ) := by
  unfold neuron_train_fi_median_rel_err; norm_num

theorem neuron_holdout_fi_median_lt_thirty_pct : neuron_holdout_fi_median_rel_err < (0.30 : ℝ) := by
  unfold neuron_holdout_fi_median_rel_err; norm_num

theorem neuron_holdout_fi_pearson_gt_fifty_five : (0.55 : ℝ) < neuron_holdout_fi_pearson_r := by
  unfold neuron_holdout_fi_pearson_r; norm_num

theorem neuron_cohort_train_holdout_bundle :
    neuron_train_cell_count = {tr_n} ∧
    neuron_holdout_cell_count = {ho_n} ∧
    ({tr_gate} : ℕ) < neuron_train_cell_count ∧
    ({ho_gate} : ℕ) < neuron_holdout_cell_count ∧
    neuron_train_fi_median_rel_err < (0.30 : ℝ) ∧
    neuron_holdout_fi_median_rel_err < (0.30 : ℝ) ∧
    (0.55 : ℝ) < neuron_holdout_fi_pearson_r := by
  refine ⟨
    by unfold neuron_train_cell_count; norm_num,
    by unfold neuron_holdout_cell_count; norm_num,
    neuron_train_cell_count_ge_gate,
    neuron_holdout_cell_count_ge_gate,
    neuron_train_fi_median_lt_thirty_pct,
    neuron_holdout_fi_median_lt_thirty_pct,
    neuron_holdout_fi_pearson_gt_fifty_five
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = json.loads(args.bench.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(doc), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())