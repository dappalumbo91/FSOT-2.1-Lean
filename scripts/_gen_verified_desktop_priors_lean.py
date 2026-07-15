"""Lean prior generator for Tier 88 verified desktop panels (cross-proof exportable)."""

from __future__ import annotations


def verified_desktop_priors_lean(
    *,
    module_title: str,
    generator: str,
    prefix: str,
    sign_theorem: str,
    lean_domain: str,
    n: int,
    med: float,
    d_eff: int,
    anchor_scalars: dict[str, float] | None = None,
) -> str:
    anchor_scalars = anchor_scalars or {}
    scalar_defs: list[str] = []
    scalar_thms: list[str] = []
    for key, val in sorted(anchor_scalars.items()):
        sym = f"{prefix}_{key}"
        scalar_defs.append(f"def {sym} : ℝ := ({val} : ℝ)")
        scalar_thms.append(
            f"theorem {sym}_pos : 0 < {sym} := by\n  unfold {sym}; norm_num"
        )
        if val < 0.5:
            scalar_thms.append(
                f"theorem {sym}_under_half_pct : {sym} < (0.5 : ℝ) := by\n  unfold {sym}; norm_num"
            )
    scalar_block = ""
    if scalar_defs:
        scalar_block = "\n".join(scalar_defs) + "\n\n" + "\n\n".join(scalar_thms) + "\n\n"

    return f"""/-
  {module_title}
  Generator: {generator}
  Cross-proof: exported via export_full_formal_obligations.py → Coq / Isabelle / F* / Rust replay
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_median_error_pct : ℝ := ({med} : ℝ)
def {prefix}_D_eff : ℕ := {d_eff}

{scalar_block}theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_median_error_under_five_pct :
    {prefix}_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_median_error_under_half_pct :
    {prefix}_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "{lean_domain}") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    by unfold {prefix}_D_eff; norm_num,
    {prefix}_median_error_under_half_pct,
    {sign_theorem}
  ⟩

end

end FSOT.Formal
"""