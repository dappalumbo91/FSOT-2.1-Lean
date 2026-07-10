#!/usr/bin/env python3
"""Generate Lean priors for full scientific-domain coupling simulation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
BENCH = ROOT / "data" / "domain_coupling_simulation_benchmark.json"


def main() -> int:
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    n_nodes = int(bench["node_count"])
    n_edges = int(bench["edge_count"])
    pooled = float(bench["pooled_median_error_pct"])
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in (bench.get("sota_comparison") or {}).get("beats_sota_summary", {}).values() if v)
    out = FORMAL / "DomainCouplingSimulationPriors.lean"
    out.write_text(
        f"""/-
  FSOT Formal DomainCouplingSimulationPriors — {n_nodes}-domain cross-domain coupling graph.
  Generator: scripts/gen_domain_coupling_simulation_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def domain_coupling_node_count : ℕ := {n_nodes}
def domain_coupling_edge_count : ℕ := {n_edges}
def domain_coupling_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def domain_coupling_headline_median_error_pct : ℝ := ({headline} : ℝ)
def domain_coupling_beats_sota_headlines : ℕ := {beats}
def domain_coupling_D_eff : ℕ := 17

theorem domain_coupling_node_count_pos : 0 < domain_coupling_node_count := by
  unfold domain_coupling_node_count; norm_num

theorem domain_coupling_edge_count_pos : 0 < domain_coupling_edge_count := by
  unfold domain_coupling_edge_count; norm_num

theorem domain_coupling_pooled_median_under_half_pct :
    domain_coupling_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold domain_coupling_pooled_median_error_pct; norm_num

theorem domain_coupling_headline_median_under_half_pct :
    domain_coupling_headline_median_error_pct < (0.5 : ℝ) := by
  unfold domain_coupling_headline_median_error_pct; norm_num

theorem domain_coupling_beats_sota_headlines_pos : 0 < domain_coupling_beats_sota_headlines := by
  unfold domain_coupling_beats_sota_headlines; norm_num

theorem domain_coupling_bundle :
    domain_coupling_node_count = {n_nodes} ∧
    domain_coupling_edge_count = {n_edges} ∧
    domain_coupling_pooled_median_error_pct < (0.5 : ℝ) ∧
    domain_coupling_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < domain_coupling_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold domain_coupling_node_count; norm_num,
    by unfold domain_coupling_edge_count; norm_num,
    domain_coupling_pooled_median_under_half_pct,
    domain_coupling_headline_median_under_half_pct,
    domain_coupling_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
""",
        encoding="utf-8",
    )
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())