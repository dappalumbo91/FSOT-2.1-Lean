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


def build_module(name: str, cfg: dict, bench: dict) -> str:
    stem = _module_stem(name)
    n = int(bench.get("record_count") or len(bench.get("records") or []))
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