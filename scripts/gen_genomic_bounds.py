#!/usr/bin/env python3
"""
Validate FSOT genomic exact identities and emit certified Lean interval lemmas.

Run before committing FSOT/Formal/Genomic.lean changes:
  python scripts/gen_genomic_bounds.py
  python scripts/gen_genomic_bounds.py --write-lean
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENOMIC_LEAN = ROOT / "FSOT" / "Formal" / "Genomic.lean"
SNIPPET_PATH = ROOT / "scripts" / "_genomic_bounds_snippet.lean"

PHI = (1 + math.sqrt(5)) / 2
PHI_LO = 1.618
PHI_HI = 1.6181
AUTOSOME_TOL = 0.01
TARGET_AUTOSOME = 22.0


def check_exact_identities() -> list[str]:
    issues: list[str] = []
    if 4**3 != 64:
        issues.append("4^3 != 64")
    if 3**3 != 27:
        issues.append("3^3 != 27")
    if abs(3 / 64 - 0.046875) > 1e-15:
        issues.append("3/64 != 0.046875")
    if abs((4 / 3) ** 3 - 64 / 27) > 1e-12:
        issues.append("(4/3)^3 != 64/27")
    aa = 4 * PHI**3 + 8 * PHI ** (-2)
    if abs(aa - 20) > 1e-9:
        issues.append(f"4*phi^3+8*phi^-2 = {aa}, not 20")
    autosome = 2 * (PHI**5 - PHI ** (-5))
    if abs(autosome - TARGET_AUTOSOME) > 1e-9:
        issues.append(f"2*(phi^5-phi^-5) = {autosome}, not 22")
    return issues


def phi_pow_interval(n: int) -> tuple[float, float]:
    if n > 0:
        return PHI_LO**n, PHI_HI**n
    return PHI_HI ** n, PHI_LO ** n


def autosome_interval(p5_lo: float, p5_hi: float, pm5_lo: float, pm5_hi: float) -> tuple[float, float]:
    diff_lo = p5_lo - pm5_hi
    diff_hi = p5_hi - pm5_lo
    return 2 * diff_lo, 2 * diff_hi


def certify_decimal(value: float, *, direction: str, places: int = 5) -> float:
    """Pick a conservative decimal bracket constant provable with norm_num."""
    step = 10 ** (-places)
    if direction == "lower":
        v = math.floor(value * (10**places)) / (10**places)
        while v >= value:
            v -= step
        return round(v, places)
    v = math.ceil(value * (10**places)) / (10**places)
    while v <= value:
        v += step
    return round(v, places)


def certified_brackets() -> dict[str, float]:
    p5_lo, p5_hi = phi_pow_interval(5)
    pm5_lo, pm5_hi = phi_pow_interval(-5)
    brackets = {
        "phi_pow5_lo": certify_decimal(p5_lo, direction="lower"),
        "phi_pow5_hi": certify_decimal(p5_hi, direction="upper"),
        "phi_pow_neg5_lo": certify_decimal(pm5_lo, direction="lower"),
        "phi_pow_neg5_hi": certify_decimal(pm5_hi, direction="upper"),
    }
    a_lo, a_hi = autosome_interval(
        brackets["phi_pow5_lo"],
        brackets["phi_pow5_hi"],
        brackets["phi_pow_neg5_lo"],
        brackets["phi_pow_neg5_hi"],
    )
    if a_lo <= TARGET_AUTOSOME - AUTOSOME_TOL or a_hi >= TARGET_AUTOSOME + AUTOSOME_TOL:
        raise RuntimeError(
            f"Certified brackets fail autosome tolerance: [{a_lo:.6f}, {a_hi:.6f}] "
            f"not inside ({TARGET_AUTOSOME - AUTOSOME_TOL}, {TARGET_AUTOSOME + AUTOSOME_TOL})"
        )
    brackets["autosome_lo"] = a_lo
    brackets["autosome_hi"] = a_hi
    return brackets


def lean_bound_name(prefix: str, value: float) -> str:
    return prefix + str(value).replace(".", "_").replace("-", "neg")


def emit_lean_snippet(brackets: dict[str, float]) -> str:
    lines = [
        "-- Auto-validated genomic interval lemmas (scripts/gen_genomic_bounds.py)",
        "-- Reference only; FSOT/Formal/Genomic.lean uses certified bracket lemmas.",
        (
            f"lemma {lean_bound_name('phi_pow5_gt_', brackets['phi_pow5_lo'])} "
            f": ({brackets['phi_pow5_lo']} : ℝ) < phi ^ 5 := by sorry"
        ),
        (
            f"lemma {lean_bound_name('phi_pow5_lt_', brackets['phi_pow5_hi'])} "
            f": phi ^ 5 < ({brackets['phi_pow5_hi']} : ℝ) := by sorry"
        ),
        (
            f"lemma {lean_bound_name('phi_pow_neg5_gt_', brackets['phi_pow_neg5_lo'])} "
            f": ({brackets['phi_pow_neg5_lo']} : ℝ) < phi ^ (-5 : ℤ) := by sorry"
        ),
        (
            f"lemma {lean_bound_name('phi_pow_neg5_lt_', brackets['phi_pow_neg5_hi'])} "
            f": phi ^ (-5 : ℤ) < ({brackets['phi_pow_neg5_hi']} : ℝ) := by sorry"
        ),
        (
            f"-- autosome 2*(phi^5 - phi^-5) in "
            f"({brackets['autosome_lo']:.6f}, {brackets['autosome_hi']:.6f}); target 22"
        ),
    ]
    return "\n".join(lines) + "\n"


def patch_genomic_lean(brackets: dict[str, float]) -> tuple[bool, str]:
    """Sync certified bracket constants; keep stable lemma names for cross-references."""
    text = GENOMIC_LEAN.read_text(encoding="utf-8")
    p5_lo = brackets["phi_pow5_lo"]
    p5_hi = brackets["phi_pow5_hi"]
    pm5_lo = brackets["phi_pow_neg5_lo"]
    pm5_hi = brackets["phi_pow_neg5_hi"]
    replacements = [
        (
            r"(lemma phi_pow5_gt_11089 : )\([\d.]+ : ℝ\) < phi \^ 5",
            rf"\g<1>({p5_lo} : ℝ) < phi ^ 5",
        ),
        (
            r"(lemma phi_pow5_lt_11094 : phi \^ 5 < )\([\d.]+ : ℝ\)",
            rf"\g<1>({p5_hi} : ℝ)",
        ),
        (
            r"(lemma phi_pow_neg5_gt_09013 : )\([\d.]+ : ℝ\) < phi \^ \(-5 : ℤ\)",
            rf"\g<1>({pm5_lo} : ℝ) < phi ^ (-5 : ℤ)",
        ),
        (
            r"(lemma phi_pow_neg5_lt_09018 : phi \^ \(-5 : ℤ\) < )\([\d.]+ : ℝ\)",
            rf"\g<1>({pm5_hi} : ℝ)",
        ),
        (
            r"/-- φ⁵ lower bracket \(gen_genomic_bounds\.py: PHI_LO\^5 ≈ [\d.]+\)\. -/",
            f"/-- φ⁵ lower bracket (gen_genomic_bounds.py: PHI_LO^5 ≈ {p5_lo}). -/",
        ),
        (
            r"/-- φ⁵ upper bracket \(gen_genomic_bounds\.py: PHI_HI\^5 ≈ [\d.]+\)\. -/",
            f"/-- φ⁵ upper bracket (gen_genomic_bounds.py: PHI_HI^5 ≈ {p5_hi}). -/",
        ),
        (
            r"have h_inv : 1 / \(11\.[\d]+ : ℝ\) < 1 / phi \^ 5 :=",
            f"have h_inv : 1 / ({p5_hi} : ℝ) < 1 / phi ^ 5 :=",
        ),
        (
            r"have h_base : \([\d.]+ : ℝ\) < 1 / \(11\.[\d]+ : ℝ\) := by norm_num",
            f"have h_base : ({pm5_lo} : ℝ) < 1 / ({p5_hi} : ℝ) := by norm_num",
        ),
        (
            r"have h_inv : 1 / phi \^ 5 < 1 / \(11\.[\d]+ : ℝ\) :=",
            f"have h_inv : 1 / phi ^ 5 < 1 / ({p5_lo} : ℝ) :=",
        ),
        (
            r"have h_base : 1 / \(11\.[\d]+ : ℝ\) < \([\d.]+ : ℝ\) := by norm_num",
            f"have h_base : 1 / ({p5_lo} : ℝ) < ({pm5_hi} : ℝ) := by norm_num",
        ),
        (
            r"one_div_lt_one_div_of_lt \(by norm_num : \(0 : ℝ\) < 11\.[\d]+\) phi_pow5_gt_11089",
            f"one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < {p5_lo}) phi_pow5_gt_11089",
        ),
        (
            r"have h5lo : \(11\.[\d]+ : ℝ\) < phi \^ 5 := phi_pow5_gt_11089",
            f"have h5lo : ({p5_lo} : ℝ) < phi ^ 5 := phi_pow5_gt_11089",
        ),
        (
            r"have h5hi : phi \^ 5 < \(11\.[\d]+ : ℝ\) := phi_pow5_lt_11094",
            f"have h5hi : phi ^ 5 < ({p5_hi} : ℝ) := phi_pow5_lt_11094",
        ),
        (
            r"have hmlo : \(0\.[\d]+ : ℝ\) < 1 / phi \^ 5 :=",
            f"have hmlo : ({pm5_lo} : ℝ) < 1 / phi ^ 5 :=",
        ),
        (
            r"have hmhi : 1 / phi \^ 5 < \(0\.[\d]+ : ℝ\) :=",
            f"have hmhi : 1 / phi ^ 5 < ({pm5_hi} : ℝ) :=",
        ),
    ]
    updated = text
    changed = 0
    for pattern, repl in replacements:
        new_text, n = re.subn(pattern, repl, updated, count=1)
        if n:
            changed += 1
        updated = new_text
    if changed == 0:
        return False, "no bracket constants changed"
    GENOMIC_LEAN.write_text(updated, encoding="utf-8")
    return True, f"patched {changed} bracket site(s)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate genomic identities and emit Lean brackets")
    parser.add_argument("--write-lean", action="store_true", help="Sync certified brackets into Genomic.lean")
    args = parser.parse_args()

    issues = check_exact_identities()
    brackets = certified_brackets()
    print("=== Genomic exact identity checks ===")
    print("  4^3 = 64")
    print("  3^3 = 27")
    print("  4*phi^3 + 8*phi^-2 = 20")
    print(
        f"  2*(phi^5 - phi^-5) in [{brackets['autosome_lo']:.6f}, {brackets['autosome_hi']:.6f}] "
        f"(target {TARGET_AUTOSOME} ± {AUTOSOME_TOL})"
    )
    print(f"  Certified φ⁵ brackets: ({brackets['phi_pow5_lo']}, {brackets['phi_pow5_hi']})")
    print(
        f"  Certified φ⁻⁵ brackets: ({brackets['phi_pow_neg5_lo']}, {brackets['phi_pow_neg5_hi']})"
    )
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All exact identities OK.")
    SNIPPET_PATH.write_text(emit_lean_snippet(brackets), encoding="utf-8")
    print(f"  Wrote reference snippet: {SNIPPET_PATH}")
    if args.write_lean:
        ok, detail = patch_genomic_lean(brackets)
        if ok:
            print(f"  Synced certified brackets into {GENOMIC_LEAN} ({detail})")
        else:
            print(f"  WARN: Genomic.lean bracket sync skipped ({detail})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())