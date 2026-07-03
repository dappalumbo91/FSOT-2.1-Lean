#!/usr/bin/env python3
"""Generate FSOT/Formal/SeismologyDeepPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "seismology_deep_manifest.yaml"
BENCH = ROOT / "data" / "seismology_deep_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "SeismologyDeepPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    ho_n = int(bench.get("holdout_record_count") or 0)
    ho_match = int(bench.get("holdout_match_count") or 0)
    rate = float(bench.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 18)
    sign = cfg.get("lean", {}).get("sign_theorem", "energy_raw_S_positive")
    return f"""/-
  FSOT Formal SeismologyDeepPriors — moment-tensor + plate-margin deep classifier.
  Generator: scripts/gen_seismology_deep_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def seismology_deep_observable_count : ℕ := {n}
def seismology_deep_match_count : ℕ := {match_n}
def seismology_deep_holdout_count : ℕ := {ho_n}
def seismology_deep_holdout_match_count : ℕ := {ho_match}
def seismology_deep_D_eff : ℕ := {d_eff}
def seismology_deep_match_rate : ℝ := ({rate} : ℝ)

theorem seismology_deep_observable_count_pos : 0 < seismology_deep_observable_count := by
  unfold seismology_deep_observable_count; norm_num

theorem seismology_deep_match_le_total : seismology_deep_match_count ≤ seismology_deep_observable_count := by
  unfold seismology_deep_match_count seismology_deep_observable_count; norm_num

theorem seismology_deep_holdout_match_le_total :
    seismology_deep_holdout_match_count ≤ seismology_deep_holdout_count := by
  unfold seismology_deep_holdout_match_count seismology_deep_holdout_count; norm_num

theorem seismology_deep_bundle :
    seismology_deep_observable_count = {n} ∧
    seismology_deep_match_count = {match_n} ∧
    seismology_deep_holdout_count = {ho_n} ∧
    seismology_deep_holdout_match_count = {ho_match} ∧
    seismology_deep_D_eff = {d_eff} ∧
    seismology_deep_match_count ≤ seismology_deep_observable_count ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold seismology_deep_observable_count; norm_num,
    by unfold seismology_deep_match_count; norm_num,
    by unfold seismology_deep_holdout_count; norm_num,
    by unfold seismology_deep_holdout_match_count; norm_num,
    by unfold seismology_deep_D_eff; norm_num,
    seismology_deep_match_le_total,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())