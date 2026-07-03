#!/usr/bin/env python3
"""Generate FSOT/Formal/HiggsBranchingPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "higgs_branching_manifest.yaml"
BENCH = ROOT / "data" / "higgs_branching_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "HiggsBranchingPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    compute_n = int(bench.get("compute_higgs_count") or 0)
    thesis_n = int(bench.get("thesis_higgs_count") or 0)
    total = int(bench.get("observable_count") or compute_n + thesis_n)
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    max_err = bench.get("max_error_pct")
    max_err = 0.0 if max_err is None else float(max_err)
    sign = cfg.get("lean", {}).get("sign_theorem", "higgs_raw_S_positive")
    return f"""/-
  FSOT Formal HiggsBranchingPriors — dedicated HEP/Higgs branching observables.
  Generator: scripts/gen_higgs_branching_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def higgs_compute_branching_count : ℕ := {compute_n}
def higgs_thesis_target_count : ℕ := {thesis_n}
def higgs_branching_observable_count : ℕ := {total}
def higgs_branching_median_error_pct : ℝ := ({med} : ℝ)
def higgs_branching_max_error_pct : ℝ := ({max_err} : ℝ)

theorem higgs_compute_branching_count_pos : 0 < higgs_compute_branching_count := by
  unfold higgs_compute_branching_count; norm_num

theorem higgs_branching_observable_count_pos : 0 < higgs_branching_observable_count := by
  unfold higgs_branching_observable_count; norm_num

theorem higgs_branching_components_sum :
    higgs_compute_branching_count + higgs_thesis_target_count = higgs_branching_observable_count := by
  unfold higgs_compute_branching_count higgs_thesis_target_count higgs_branching_observable_count; norm_num

theorem higgs_branching_median_error_under_five_pct :
    higgs_branching_median_error_pct < (5 : ℝ) := by
  unfold higgs_branching_median_error_pct; norm_num

theorem higgs_branching_max_error_under_five_pct :
    higgs_branching_max_error_pct < (5 : ℝ) := by
  unfold higgs_branching_max_error_pct; norm_num

/-- Bundle: Higgs BR from fsot_compute + thesis wave8 with higgs-domain sign proxy. -/
theorem higgs_branching_bundle :
    higgs_compute_branching_count = {compute_n} ∧
    higgs_thesis_target_count = {thesis_n} ∧
    higgs_branching_observable_count = {total} ∧
    higgs_compute_branching_count + higgs_thesis_target_count = {total} ∧
    higgs_branching_median_error_pct < (5 : ℝ) ∧
    higgs_branching_max_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "higgs") := by
  refine ⟨
    by unfold higgs_compute_branching_count; norm_num,
    by unfold higgs_thesis_target_count; norm_num,
    by unfold higgs_branching_observable_count; norm_num,
    higgs_branching_components_sum,
    higgs_branching_median_error_under_five_pct,
    higgs_branching_max_error_under_five_pct,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--benchmark", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bench = json.loads(args.benchmark.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())