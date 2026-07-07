"""Shared Lean prior generator template for Tier 29 extension domains."""

from __future__ import annotations


def extension_priors_lean(
    *,
    module_title: str,
    generator: str,
    prefix: str,
    sign_theorem: str,
    lean_domain: str,
    n: int,
    med: float,
    d_eff: int,
) -> str:
    return f"""/-
  {module_title}
  Generator: {generator}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_median_error_pct : ℝ := ({med} : ℝ)
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_median_error_under_five_pct :
    {prefix}_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "{lean_domain}") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    by unfold {prefix}_D_eff; norm_num,
    {prefix}_median_error_under_five_pct,
    {sign_theorem}
  ⟩

end

end FSOT.Formal
"""