#!/usr/bin/env python3
"""Generate FSOT/Formal/IntelligenceCompressionPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "intelligence_compression_manifest.yaml"
BENCH = ROOT / "data" / "intelligence_compression_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "IntelligenceCompressionPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("sweep_row_count") or bench.get("record_count") or 0)
    fertile = int(bench.get("fertile_count") or 0)
    best = float(bench.get("best_intelligence_score") or 0.0)
    d_eff = int(bench.get("D_eff") or 12)
    replay_rate = float(bench.get("stability_match_rate") or 0.0)
    headline_med = float(bench.get("headline_median_error_pct") or bench.get("median_error_pct") or 0.0)
    optimal_s = float(bench.get("optimal_S_final") or 0.0)
    source = cfg.get("source_repo", "vendor/intelligence_compression")
    return f"""/-
  FSOT Formal IntelligenceCompressionPriors — FIC sensitivity sweep certificates.
  Generator: scripts/gen_intelligence_compression_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fic_sweep_row_count : ℕ := {n}
def fic_fertile_row_count : ℕ := {fertile}
def fic_D_eff_optimal : ℕ := {d_eff}
def fic_fertile_replay_match_count : ℕ := {int(bench.get("stability_match_count") or 0)}
def fic_headline_median_error_pct : ℝ := ({headline_med} : ℝ)
def fic_optimal_S_final : ℝ := ({optimal_s} : ℝ)
def fic_best_intelligence_score : ℝ := ({best} : ℝ)
def fic_fertile_replay_match_rate : ℝ := ({replay_rate} : ℝ)

theorem fic_sweep_row_count_pos : 0 < fic_sweep_row_count := by
  unfold fic_sweep_row_count; norm_num

theorem fic_fertile_rows_present : 0 < fic_fertile_row_count := by
  unfold fic_fertile_row_count; norm_num

theorem fic_fertile_replay_match_le_total :
    fic_fertile_replay_match_count ≤ fic_sweep_row_count := by
  unfold fic_fertile_replay_match_count fic_sweep_row_count; norm_num

theorem fic_best_intelligence_score_positive :
    (0 : ℝ) < fic_best_intelligence_score := by
  unfold fic_best_intelligence_score; norm_num

theorem fic_fertile_replay_match_rate_le_one :
    fic_fertile_replay_match_rate ≤ (1 : ℝ) := by
  unfold fic_fertile_replay_match_rate; norm_num

/-- Bundle: Intelligence Compression fertile-window sweep with neural/consciousness/ai maps. -/
theorem intelligence_compression_priors_bundle :
    fic_sweep_row_count = {n} ∧
    fic_fertile_row_count = {fertile} ∧
    fic_D_eff_optimal = {d_eff} ∧
    fic_fertile_replay_match_count = {int(bench.get("stability_match_count") or 0)} ∧
    (0 : ℝ) < fic_best_intelligence_score ∧
    fic_fertile_replay_match_count ≤ fic_sweep_row_count ∧
    raw_S (get_domain_params "neural") > 0 ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold fic_sweep_row_count; norm_num,
    by unfold fic_fertile_row_count; norm_num,
    by unfold fic_D_eff_optimal; norm_num,
    by unfold fic_fertile_replay_match_count; norm_num,
    fic_best_intelligence_score_positive,
    fic_fertile_replay_match_le_total,
    neural_raw_S_positive,
    consciousness_raw_S_positive
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
    if not args.bench.exists():
        raise FileNotFoundError(f"Run build_intelligence_compression_benchmark.py first: {args.bench}")
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())