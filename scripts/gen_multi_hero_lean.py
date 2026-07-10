#!/usr/bin/env python3
"""Generate FSOT/Formal/NeuronMultiHeroPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "multi_hero_manifest.yaml"
BENCH = ROOT / "data" / "multi_hero_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "NeuronMultiHeroPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    med_fi = bench.get("median_fi_proxy_rel_err_pct")
    med_fi = 0.0 if med_fi is None else float(med_fi)
    strata_n = int(bench.get("stratum_count") or 0)
    d_eff = int(cfg.get("D_eff", 14))
    sign = cfg.get("lean", {}).get("sign_theorem", "neural_raw_S_positive")
    return f"""/-
  FSOT Formal NeuronMultiHeroPriors — multi-hero FI-proxy certification per Allen class.
  Generator: scripts/gen_multi_hero_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuron_multi_hero_count : ℕ := {n}
def neuron_multi_hero_stratum_count : ℕ := {strata_n}
def neuron_multi_hero_median_error_pct : ℝ := ({med} : ℝ)
def neuron_multi_hero_median_fi_proxy_rel_err_pct : ℝ := ({med_fi} : ℝ)
def neuron_multi_hero_D_eff : ℕ := {d_eff}

theorem neuron_multi_hero_count_pos : 0 < neuron_multi_hero_count := by
  unfold neuron_multi_hero_count; norm_num

theorem neuron_multi_hero_median_error_under_half_pct :
    neuron_multi_hero_median_error_pct < (0.5 : ℝ) := by
  unfold neuron_multi_hero_median_error_pct; norm_num

theorem neuron_multi_hero_median_fi_under_thirty_pct :
    neuron_multi_hero_median_fi_proxy_rel_err_pct < (30 : ℝ) := by
  unfold neuron_multi_hero_median_fi_proxy_rel_err_pct; norm_num

theorem neuron_multi_hero_bundle :
    neuron_multi_hero_count = {n} ∧
    neuron_multi_hero_stratum_count = {strata_n} ∧
    neuron_multi_hero_D_eff = {d_eff} ∧
    neuron_multi_hero_median_error_pct < (0.5 : ℝ) ∧
    neuron_multi_hero_median_fi_proxy_rel_err_pct < (30 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold neuron_multi_hero_count; norm_num,
    by unfold neuron_multi_hero_stratum_count; norm_num,
    by unfold neuron_multi_hero_D_eff; norm_num,
    neuron_multi_hero_median_error_under_half_pct,
    neuron_multi_hero_median_fi_under_thirty_pct,
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