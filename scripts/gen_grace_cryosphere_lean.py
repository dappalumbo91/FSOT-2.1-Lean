#!/usr/bin/env python3
"""Generate FSOT/Formal/GraceCryospherePriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "grace_cryosphere_manifest.yaml"
BENCH = ROOT / "data" / "grace_cryosphere_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "GraceCryospherePriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    rate = float(bench.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 16)
    sign = cfg.get("lean", {}).get("sign_theorem", "galactic_raw_S_positive")
    return f"""/-
  FSOT Formal GraceCryospherePriors — GRACE Greenland mass-decline classifier.
  Generator: scripts/gen_grace_cryosphere_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def grace_cryosphere_month_count : ℕ := {n}
def grace_cryosphere_match_count : ℕ := {match_n}
def grace_cryosphere_D_eff : ℕ := {d_eff}
def grace_cryosphere_match_rate : ℝ := ({rate} : ℝ)

theorem grace_cryosphere_month_count_pos : 0 < grace_cryosphere_month_count := by
  unfold grace_cryosphere_month_count; norm_num

theorem grace_cryosphere_match_le_total : grace_cryosphere_match_count ≤ grace_cryosphere_month_count := by
  unfold grace_cryosphere_match_count grace_cryosphere_month_count; norm_num

theorem grace_cryosphere_bundle :
    grace_cryosphere_month_count = {n} ∧
    grace_cryosphere_match_count = {match_n} ∧
    grace_cryosphere_D_eff = {d_eff} ∧
    grace_cryosphere_match_count ≤ grace_cryosphere_month_count ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold grace_cryosphere_month_count; norm_num,
    by unfold grace_cryosphere_match_count; norm_num,
    by unfold grace_cryosphere_D_eff; norm_num,
    grace_cryosphere_match_le_total,
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