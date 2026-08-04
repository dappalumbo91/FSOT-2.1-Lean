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
    gate_pct: float = 5.0,
) -> str:
    """Generate extension *Priors.lean.

    gate_pct: residual bound in theorems (default 5 for legacy tiers;
    use 0.5 for official green-gate engineering/GPU panels).
    """
    gate_lit = f"({gate_pct} : ℝ)" if gate_pct != int(gate_pct) else f"({int(gate_pct)} : ℝ)"
    # theorem name must be a valid Lean identifier fragment
    if abs(gate_pct - 0.5) < 1e-12:
        under_name = f"{prefix}_median_error_under_half_pct"
        under_stmt = f"{prefix}_median_error_pct < (0.5 : ℝ)"
    elif abs(gate_pct - 5.0) < 1e-12:
        under_name = f"{prefix}_median_error_under_five_pct"
        under_stmt = f"{prefix}_median_error_pct < (5 : ℝ)"
    else:
        under_name = f"{prefix}_median_error_under_gate_pct"
        under_stmt = f"{prefix}_median_error_pct < {gate_lit}"
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

theorem {under_name} :
    {under_stmt} := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_D_eff = {d_eff} ∧
    {under_stmt} ∧
    raw_S (get_domain_params "{lean_domain}") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    by unfold {prefix}_D_eff; norm_num,
    {under_name},
    {sign_theorem}
  ⟩

end

end FSOT.Formal
"""