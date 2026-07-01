#!/usr/bin/env python3
"""Generate FSOT/Formal/EmergentDomainPriors.lean from emergent domains benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "emergent_domains_manifest.yaml"
DEFAULT_BENCH = ROOT / "data" / "emergent_domains_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "EmergentDomainPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("emergent_domain_count") or bench.get("observable_count") or 0)
    observed = int(bench.get("observed_domain_count") or 0)
    health = bench.get("final_emergence_health")
    health = 0.0 if health is None else float(health)
    meta_s = bench.get("final_meta_S")
    meta_s = 0.0 if meta_s is None else float(meta_s)
    sign = cfg.get("lean", {}).get("sign_theorem", "quantum_raw_S_positive")
    return f"""/-
  FSOT Formal EmergentDomainPriors — Tier 15 MC emergent domain observables.
  Source: data/emergent_domains_benchmark.json (autonomous_monte_carlo_fsot_refiner)
  Generator: scripts/gen_emergent_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def emergent_domain_count : ℕ := {n}
def emergent_observed_domain_count : ℕ := {observed}
def emergent_final_emergence_health : ℝ := ({health} : ℝ)
def emergent_final_meta_S : ℝ := ({meta_s} : ℝ)

theorem emergent_domain_count_pos : 0 < emergent_domain_count := by
  unfold emergent_domain_count; norm_num

theorem emergent_observed_le_total :
    emergent_observed_domain_count ≤ emergent_domain_count := by
  unfold emergent_observed_domain_count emergent_domain_count; norm_num

theorem emergent_final_emergence_health_positive : (0 : ℝ) < emergent_final_emergence_health := by
  unfold emergent_final_emergence_health; norm_num

theorem emergent_final_meta_S_positive : (0 : ℝ) < emergent_final_meta_S := by
  unfold emergent_final_meta_S; norm_num

/-- Bundle: 29 MC-discovered emergent domains with quantum-domain sign proxy. -/
theorem emergent_domain_priors_bundle :
    emergent_domain_count = {n} ∧
    emergent_observed_domain_count = {observed} ∧
    emergent_observed_domain_count ≤ emergent_domain_count ∧
    emergent_final_emergence_health = ({health} : ℝ) ∧
    emergent_final_meta_S = ({meta_s} : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "quantum") := by
  refine ⟨
    by unfold emergent_domain_count; norm_num,
    by unfold emergent_observed_domain_count; norm_num,
    emergent_observed_le_total,
    by unfold emergent_final_emergence_health; norm_num,
    by unfold emergent_final_meta_S; norm_num,
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
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bench = json.loads(args.benchmark.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())