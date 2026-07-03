#!/usr/bin/env python3
"""Generate FSOT/Formal/MagnetospherePriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "magnetosphere_manifest.yaml"
BENCH = ROOT / "data" / "magnetosphere_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "MagnetospherePriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    rate = float(bench.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 14)
    sign = cfg.get("lean", {}).get("sign_theorem", "electron_raw_S_positive")
    return f"""/-
  FSOT Formal MagnetospherePriors — Dst+Kp+magnetic-string coupled storm classifier.
  Generator: scripts/gen_magnetosphere_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def magnetosphere_observable_count : ℕ := {n}
def magnetosphere_match_count : ℕ := {match_n}
def magnetosphere_D_eff : ℕ := {d_eff}
def magnetosphere_match_rate : ℝ := ({rate} : ℝ)

theorem magnetosphere_observable_count_pos : 0 < magnetosphere_observable_count := by
  unfold magnetosphere_observable_count; norm_num

theorem magnetosphere_match_le_total : magnetosphere_match_count ≤ magnetosphere_observable_count := by
  unfold magnetosphere_match_count magnetosphere_observable_count; norm_num

theorem magnetosphere_bundle :
    magnetosphere_observable_count = {n} ∧
    magnetosphere_match_count = {match_n} ∧
    magnetosphere_D_eff = {d_eff} ∧
    magnetosphere_match_count ≤ magnetosphere_observable_count ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold magnetosphere_observable_count; norm_num,
    by unfold magnetosphere_match_count; norm_num,
    by unfold magnetosphere_D_eff; norm_num,
    magnetosphere_match_le_total,
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