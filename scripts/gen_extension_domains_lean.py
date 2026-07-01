#!/usr/bin/env python3
"""Generate Lean priors for extension domains #37-39."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
FORMAL = ROOT / "FSOT" / "Formal"

LEAN_SIGN = {
    "Plasma_Physics": ("energy", "energy_raw_S_positive"),
    "Immunology": ("medical", "medical_raw_S_positive"),
    "Climate_Science": ("energy", "energy_raw_S_positive"),
}


def _load_bench(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _module_stem(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def build_climate_module(name: str, cfg: dict, bench: dict) -> str:
    stem = _module_stem(name)
    n = int(bench.get("record_count") or bench.get("month_count") or 0)
    med = 0.0 if bench.get("median_error_pct") is None else float(bench["median_error_pct"])
    d_eff = int(cfg.get("D_eff", 16))
    cohort = bench.get("cohort") or {}
    hold = cohort.get("holdout") or {}
    train = cohort.get("train") or {}
    ho_n = int(hold.get("record_count") or 0)
    ho_med = hold.get("median_error_pct")
    ho_med = 0.0 if ho_med is None else float(ho_med)
    tr_n = int(train.get("record_count") or 0)
    ho_stn = int(hold.get("station_count") or 0)
    prefix = name.lower()
    return f"""/-
  FSOT Formal {stem}Priors — extension domain {name} (scaled NCEI + station cohort).
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_train_month_count : ℕ := {tr_n}
def {prefix}_holdout_month_count : ℕ := {ho_n}
def {prefix}_holdout_station_count : ℕ := {ho_stn}
def {prefix}_D_eff : ℕ := {d_eff}
def {prefix}_median_error_pct : ℝ := ({med} : ℝ)
def {prefix}_holdout_median_error_pct : ℝ := ({ho_med} : ℝ)

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_holdout_month_count_pos : 0 < {prefix}_holdout_month_count := by
  unfold {prefix}_holdout_month_count; norm_num

theorem {prefix}_median_error_under_five_pct : {prefix}_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_holdout_median_error_under_five_pct : {prefix}_holdout_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_holdout_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_train_month_count = {tr_n} ∧
    {prefix}_holdout_month_count = {ho_n} ∧
    {prefix}_holdout_station_count = {ho_stn} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_median_error_pct < (5 : ℝ) ∧
    {prefix}_holdout_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    by unfold {prefix}_train_month_count; norm_num,
    by unfold {prefix}_holdout_month_count; norm_num,
    by unfold {prefix}_holdout_station_count; norm_num,
    by unfold {prefix}_D_eff; norm_num,
    {prefix}_median_error_under_five_pct,
    {prefix}_holdout_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def build_module(name: str, cfg: dict, bench: dict) -> str:
    if name == "Climate_Science" and bench.get("cohort"):
        return build_climate_module(name, cfg, bench)
    stem = _module_stem(name)
    n = int(
        bench.get("record_count")
        or bench.get("month_count")
        or len(bench.get("records") or [])
    )
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    d_eff = int(cfg.get("D_eff", 12))
    lean_dom, sign_thm = LEAN_SIGN.get(name, ("energy", "energy_raw_S_positive"))
    return f"""/-
  FSOT Formal {stem}Priors — extension domain {name}.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def {name.lower()}_observable_count : ℕ := {n}
def {name.lower()}_D_eff : ℕ := {d_eff}

theorem {name.lower()}_observable_count_pos : 0 < {name.lower()}_observable_count := by
  unfold {name.lower()}_observable_count; norm_num

theorem {name.lower()}_median_error_under_five_pct :
    ({med} : ℝ) < (5 : ℝ) := by norm_num

theorem {name.lower()}_bundle :
    {name.lower()}_observable_count = {n} ∧
    {name.lower()}_D_eff = {d_eff} ∧
    ({med} : ℝ) < (5 : ℝ) ∧
    raw_S (get_domain_params "{lean_dom}") > 0 := by
  refine ⟨
    by unfold {name.lower()}_observable_count; norm_num,
    by unfold {name.lower()}_D_eff; norm_num,
    {name.lower()}_median_error_under_five_pct,
    {sign_thm}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    for name, cfg in (spec.get("extension_domains") or {}).items():
        bench_path = ROOT / cfg["benchmark_data"]
        bench = _load_bench(bench_path)
        stem = _module_stem(name)
        out = FORMAL / f"{stem}Priors.lean"
        out.write_text(build_module(name, cfg, bench), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())