#!/usr/bin/env python3
"""Generate Lean *Priors.lean for Matter/Antimatter + Quantum/Trinary syntax panels.

Same pattern as gen_open_frontier_priors_lean.py. Feeds:
  export_full_priors_obligations.py
  export_scientific_catalog_obligations.py  (via green margin audit)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

# (benchmark_file, lean_prefix, d_eff)
PANELS: list[tuple[str, str, int]] = [
    ("matter_antimatter_benchmark.json", "matter_antimatter", 5),
    ("quantum_trinary_syntax_benchmark.json", "quantum_trinary_syntax", 11),
]


def _to_module_stem(prefix: str) -> str:
    parts = prefix.split("_")
    return "".join(p[:1].upper() + p[1:] for p in parts if p) + "Priors"


def build_lean(
    prefix: str,
    module_stem: str,
    n: int,
    pooled: float,
    headline: float,
    d_eff: int,
    *,
    domain_label: str,
) -> str:
    pooled_s = f"{pooled:.12g}"
    headline_s = f"{headline:.12g}"
    return f"""/-
  FSOT Formal {module_stem} — {domain_label} residual panel.
  Residual law: make_fsot_record / fsot_scaled / seed identities (FSOT mathematics).
  Generator: scripts/gen_matter_quantum_trinary_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled_s} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline_s} : ℝ)
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · unfold {prefix}_D_eff; norm_num
  · exact {prefix}_pooled_median_under_half_pct

end

end FSOT.Formal
"""


def main() -> int:
    FORMAL.mkdir(parents=True, exist_ok=True)
    wrote = 0
    for bench_name, prefix, d_eff in PANELS:
        path = DATA / bench_name
        if not path.exists():
            print(f"MISSING {bench_name}", file=sys.stderr)
            continue
        bench = json.loads(path.read_text(encoding="utf-8"))
        n = int(bench.get("observable_count") or bench.get("record_count") or 0)
        # Note: pooled can be 0.0 — do not use `or 99` (0.0 is falsy)
        raw_p = bench.get("pooled_median_error_pct")
        if raw_p is None:
            raw_p = bench.get("median_error_pct")
        pooled = float(raw_p) if raw_p is not None else 99.0
        raw_h = bench.get("headline_median_error_pct")
        headline = float(raw_h) if raw_h is not None else pooled
        domain_label = str(bench.get("domain") or prefix)
        if pooled >= 0.5 or n <= 0:
            print(f"SKIP (not green): {bench_name} n={n} pooled={pooled}", file=sys.stderr)
            continue
        module_stem = _to_module_stem(prefix)
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(
            build_lean(prefix, module_stem, n, pooled, headline, d_eff, domain_label=domain_label),
            encoding="utf-8",
        )
        wrote += 1
        print(f"Wrote {out.relative_to(ROOT)} n={n} pooled={pooled:.6g}% D_eff={d_eff}")
    print(f"Generated {wrote} Lean prior modules (matter + quantum/trinary)")
    return 0 if wrote == len(PANELS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
