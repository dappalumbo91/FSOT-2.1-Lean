#!/usr/bin/env python3
"""Generate FSOT/Formal/MagnetosphereExtendedPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "magnetosphere_extended_manifest.yaml"
BENCH = ROOT / "data" / "magnetosphere_extended_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "MagnetosphereExtendedPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    hc = bench.get("historical_coupled") or {}
    sh = bench.get("storm_holdout") or {}
    bz = bench.get("solar_wind_bz") or {}
    hist_n = int(hc.get("observable_count") or 0)
    hist_m = int(hc.get("stability_match_count") or 0)
    storm_n = int(sh.get("observable_count") or 0)
    storm_m = int(sh.get("stability_match_count") or 0)
    bz_n = int(bz.get("observable_count") or 0)
    bz_m = int(bz.get("stability_match_count") or 0)
    hist_rate = float(hc.get("stability_match_rate") or 0.0)
    storm_rate = float(sh.get("stability_match_rate") or 0.0)
    bz_rate = float(bz.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 14)
    sign = cfg.get("lean", {}).get("sign_theorem", "electron_raw_S_positive")
    return f"""/-
  FSOT Formal MagnetosphereExtendedPriors — historical Dst×Kp + RTSW Bz + G-scale holdout.
  Generator: scripts/gen_magnetosphere_extended_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def magnetosphere_extended_historical_hours : ℕ := {hist_n}
def magnetosphere_extended_historical_match_count : ℕ := {hist_m}
def magnetosphere_extended_storm_holdout_hours : ℕ := {storm_n}
def magnetosphere_extended_storm_holdout_match_count : ℕ := {storm_m}
def magnetosphere_extended_bz_record_count : ℕ := {bz_n}
def magnetosphere_extended_bz_match_count : ℕ := {bz_m}
def magnetosphere_extended_D_eff : ℕ := {d_eff}
def magnetosphere_extended_historical_match_rate : ℝ := ({hist_rate} : ℝ)
def magnetosphere_extended_storm_holdout_match_rate : ℝ := ({storm_rate} : ℝ)
def magnetosphere_extended_bz_match_rate : ℝ := ({bz_rate} : ℝ)

theorem magnetosphere_extended_historical_hours_pos : 0 < magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_hours; norm_num

theorem magnetosphere_extended_historical_match_le_total :
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_match_count magnetosphere_extended_historical_hours; norm_num

theorem magnetosphere_extended_storm_holdout_match_le_total :
    magnetosphere_extended_storm_holdout_match_count ≤ magnetosphere_extended_storm_holdout_hours := by
  unfold magnetosphere_extended_storm_holdout_match_count magnetosphere_extended_storm_holdout_hours; norm_num

theorem magnetosphere_extended_bz_match_le_total :
    magnetosphere_extended_bz_match_count ≤ magnetosphere_extended_bz_record_count := by
  unfold magnetosphere_extended_bz_match_count magnetosphere_extended_bz_record_count; norm_num

theorem magnetosphere_extended_bundle :
    magnetosphere_extended_historical_hours = {hist_n} ∧
    magnetosphere_extended_historical_match_count = {hist_m} ∧
    magnetosphere_extended_storm_holdout_hours = {storm_n} ∧
    magnetosphere_extended_storm_holdout_match_count = {storm_m} ∧
    magnetosphere_extended_bz_record_count = {bz_n} ∧
    magnetosphere_extended_bz_match_count = {bz_m} ∧
    magnetosphere_extended_D_eff = {d_eff} ∧
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold magnetosphere_extended_historical_hours; norm_num,
    by unfold magnetosphere_extended_historical_match_count; norm_num,
    by unfold magnetosphere_extended_storm_holdout_hours; norm_num,
    by unfold magnetosphere_extended_storm_holdout_match_count; norm_num,
    by unfold magnetosphere_extended_bz_record_count; norm_num,
    by unfold magnetosphere_extended_bz_match_count; norm_num,
    by unfold magnetosphere_extended_D_eff; norm_num,
    magnetosphere_extended_historical_match_le_total,
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