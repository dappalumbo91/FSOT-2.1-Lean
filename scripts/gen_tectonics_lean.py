#!/usr/bin/env python3
"""Generate FSOT/Formal/TectonicsPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "tectonics_manifest.yaml"
BENCH = ROOT / "data" / "tectonics_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "TectonicsPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    boundaries = int(bench.get("plate_boundary_features") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    rate = float(bench.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 17)
    sign = cfg.get("lean", {}).get("sign_theorem", "energy_raw_S_positive")
    return f"""/-
  FSOT Formal TectonicsPriors — plate-boundary crustal earthquake coupling.
  Generator: scripts/gen_tectonics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tectonics_event_count : ℕ := {n}
def tectonics_boundary_count : ℕ := {boundaries}
def tectonics_match_count : ℕ := {match_n}
def tectonics_D_eff : ℕ := {d_eff}
def tectonics_match_rate : ℝ := ({rate} : ℝ)

theorem tectonics_event_count_pos : 0 < tectonics_event_count := by
  unfold tectonics_event_count; norm_num

theorem tectonics_boundary_count_pos : 0 < tectonics_boundary_count := by
  unfold tectonics_boundary_count; norm_num

theorem tectonics_match_le_total : tectonics_match_count ≤ tectonics_event_count := by
  unfold tectonics_match_count tectonics_event_count; norm_num

theorem tectonics_bundle :
    tectonics_event_count = {n} ∧
    tectonics_boundary_count = {boundaries} ∧
    tectonics_match_count = {match_n} ∧
    tectonics_D_eff = {d_eff} ∧
    tectonics_match_count ≤ tectonics_event_count ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tectonics_event_count; norm_num,
    by unfold tectonics_boundary_count; norm_num,
    by unfold tectonics_match_count; norm_num,
    by unfold tectonics_D_eff; norm_num,
    tectonics_match_le_total,
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