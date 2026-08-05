#!/usr/bin/env python3
"""
Raise corpus Mathlib-class depth (L0/L2/L3) for FSOT/Formal *Priors.

Formula-faithful only: same statements, stronger constructive proof shape.
Does NOT change residual law, factors, or free parameters.

Patterns upgraded (pass-complete for remaining L1):
  A. Pure literal goals  := by norm_num  → term-mode (by norm_num : goal)
  B. lit < / ≤ / > / ≥  Real def  (unfold; norm_num) → unfold + exact lit form
  C. 0 / (0:ℝ) < / ≤ Real def → exact lit form
  D. Real intervals with constructor <;> norm_num (single- or multi-line)
  E. Two-def comparisons (a < b / a ≤ b) multi-unfold → exact lit form
  F. Def-eq superposition ratios → unfold ratio; rfl  (L0)
  G. Nat 0 < n / n = k  unfold; norm_num → decide

Usage:
  python scripts/upgrade_corpus_mathlib_depth.py --dry-run
  python scripts/upgrade_corpus_mathlib_depth.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"

# def foo : ℝ := (0.5 : ℝ)   or   def foo : ℝ := 0.5
DEF_R = re.compile(
    r"def\s+(\w+)\s*:\s*ℝ\s*:=\s*(?:\(([^)]+)\s*:\s*ℝ\)|([0-9.eE+-]+))\s*$",
    re.M,
)
DEF_N = re.compile(r"def\s+(\w+)\s*:\s*(?:ℕ|Nat)\s*:=")

# Pure literal goal closed by norm_num only (no identifiers)
PURE_LIT_BY_NORM = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"((?:\([^)]*:\s*ℝ\)|[0-9.eE+-]+|\s|[<≥≤>=\^\+\-\*/])+?)\s*"
    r":=\s*by\s+norm_num\b"
)

# Superposition def-eq: (n : ℝ) / bases = ratio_def
SUPERPOS = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\((\w+)\s*:\s*ℝ\)\s*/\s*(\w+)\s*=\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\5(?:\s+\w+)+\s*;\s*norm_num\b"
)

# Multi-line interval: lit < x ∧ x < lit  with constructor <;> norm_num
INTERVAL_ML = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*∧\s*\4\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*"
    r":=\s*by\s*\n\s*unfold\s+\4\s*\n\s*constructor\s*<;\s*>\s*norm_num\b"
)

# Single-line interval variants: constructor <;> norm_num after unfold;
INTERVAL_SL = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*∧\s*\4\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\4\s*;\s*constructor\s*<;\s*>\s*norm_num\b"
)

# Unit interval with ≤ on right: (0:ℝ) < x ∧ x ≤ (1:ℝ)
UNIT_INTERVAL = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\(0\s*:\s*ℝ\)\s*<\s*(\w+)\s*∧\s*\3\s*≤\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\3\s*;\s*constructor\s*<;\s*>\s*norm_num\b"
)

# lit < sym  or  lit ≤ sym
LIT_CMP_SYM = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*([<≤])\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\5\s*;\s*norm_num\b"
)

# sym < lit  or  sym ≤ lit
SYM_CMP_LIT = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"(\w+)\s*([<≤])\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\3\s*;\s*norm_num\b"
)

# (0 : ℝ) < sym  /  (0 : ℝ) ≤ sym
ZERO_CAST_CMP = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"\(0\s*:\s*ℝ\)\s*([<≤])\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\4\s*;\s*norm_num\b"
)

# bare 0 < sym  (Real or will stay if no Real def)
BARE_ZERO_POS = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"0\s*<\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\3\s*;\s*norm_num\b"
)

# bare 0 ≤ sym
BARE_ZERO_NONNEG = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"0\s*≤\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\3\s*;\s*norm_num\b"
)

# a < b  or  a ≤ b  (two Real defs)
TWO_SYM_CMP = re.compile(
    r"(theorem|lemma)\s+(\w+)\s*:\s*"
    r"(\w+)\s*([<≤])\s*(\w+)\s*"
    r":=\s*by\s*\n?\s*unfold\s+\3\s+\5\s*;\s*norm_num\b"
)


def _lit_of(rdefs: dict[str, str], sym: str) -> str | None:
    return rdefs.get(sym)


def upgrade_file(text: str) -> tuple[str, int]:
    rdefs: dict[str, str] = {}
    for m in DEF_R.finditer(text):
        val = m.group(2) if m.group(2) is not None else m.group(3)
        rdefs[m.group(1)] = val.strip()
    ndefs = set(DEF_N.findall(text))
    n = 0

    def count_sub(pat: re.Pattern[str], repl_fn) -> None:
        nonlocal text, n

        def wrap(m: re.Match[str]) -> str:
            nonlocal n
            out = repl_fn(m)
            if out != m.group(0):
                n += 1
            return out

        text = pat.sub(wrap, text)

    # A. pure literal by norm_num → term mode (skip if goal has identifiers)
    def pure_lit(m: re.Match[str]) -> str:
        goal = m.group(3).strip()
        # reject if word identifiers present (not pure literals / ops)
        if re.search(r"[A-Za-z_]", goal.replace("ℝ", "")):
            return m.group(0)
        return f"{m.group(1)} {m.group(2)} :\n    {goal} :=\n  (by norm_num : {goal})"

    count_sub(PURE_LIT_BY_NORM, pure_lit)

    # F. superposition ratios → L0 rfl
    def superpos(m: re.Match[str]) -> str:
        ratio = m.group(5)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    ({m.group(3)} : ℝ) / {m.group(4)} = {ratio} := by\n"
            f"  unfold {ratio}; rfl"
        )

    count_sub(SUPERPOS, superpos)

    def interval(m: re.Match[str]) -> str:
        lo, sym, hi = m.group(3), m.group(4), m.group(5)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    ({lo} : ℝ) < {sym} ∧ {sym} < ({hi} : ℝ) := by\n"
            f"  unfold {sym}\n"
            f"  constructor\n"
            f"  · exact (by norm_num : ({lo} : ℝ) < ({val} : ℝ))\n"
            f"  · exact (by norm_num : ({val} : ℝ) < ({hi} : ℝ))"
        )

    count_sub(INTERVAL_ML, interval)
    count_sub(INTERVAL_SL, interval)

    def unit_interval(m: re.Match[str]) -> str:
        sym, hi = m.group(3), m.group(4)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    (0 : ℝ) < {sym} ∧ {sym} ≤ ({hi} : ℝ) := by\n"
            f"  unfold {sym}\n"
            f"  constructor\n"
            f"  · exact (by norm_num : (0 : ℝ) < ({val} : ℝ))\n"
            f"  · exact (by norm_num : ({val} : ℝ) ≤ ({hi} : ℝ))"
        )

    count_sub(UNIT_INTERVAL, unit_interval)

    def lit_cmp_sym(m: re.Match[str]) -> str:
        lit, op, sym = m.group(3), m.group(4), m.group(5)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    ({lit} : ℝ) {op} {sym} := by\n"
            f"  unfold {sym}\n"
            f"  exact (by norm_num : ({lit} : ℝ) {op} ({val} : ℝ))"
        )

    count_sub(LIT_CMP_SYM, lit_cmp_sym)

    def sym_cmp_lit(m: re.Match[str]) -> str:
        sym, op, lit = m.group(3), m.group(4), m.group(5)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    {sym} {op} ({lit} : ℝ) := by\n"
            f"  unfold {sym}\n"
            f"  exact (by norm_num : ({val} : ℝ) {op} ({lit} : ℝ))"
        )

    count_sub(SYM_CMP_LIT, sym_cmp_lit)

    def zero_cast(m: re.Match[str]) -> str:
        op, sym = m.group(3), m.group(4)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    (0 : ℝ) {op} {sym} := by\n"
            f"  unfold {sym}\n"
            f"  exact (by norm_num : (0 : ℝ) {op} ({val} : ℝ))"
        )

    count_sub(ZERO_CAST_CMP, zero_cast)

    def bare_zero_pos(m: re.Match[str]) -> str:
        sym = m.group(3)
        if sym in ndefs:
            return (
                f"{m.group(1)} {m.group(2)} :\n"
                f"    0 < {sym} := by\n"
                f"  unfold {sym}; decide"
            )
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    0 < {sym} := by\n"
            f"  unfold {sym}\n"
            f"  exact (by norm_num : (0 : ℝ) < ({val} : ℝ))"
        )

    count_sub(BARE_ZERO_POS, bare_zero_pos)

    def bare_zero_nonneg(m: re.Match[str]) -> str:
        sym = m.group(3)
        val = _lit_of(rdefs, sym)
        if not val:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    0 ≤ {sym} := by\n"
            f"  unfold {sym}\n"
            f"  exact (by norm_num : (0 : ℝ) ≤ ({val} : ℝ))"
        )

    count_sub(BARE_ZERO_NONNEG, bare_zero_nonneg)

    def two_sym(m: re.Match[str]) -> str:
        a, op, b = m.group(3), m.group(4), m.group(5)
        va, vb = _lit_of(rdefs, a), _lit_of(rdefs, b)
        if not va or not vb:
            return m.group(0)
        return (
            f"{m.group(1)} {m.group(2)} :\n"
            f"    {a} {op} {b} := by\n"
            f"  unfold {a} {b}\n"
            f"  exact (by norm_num : ({va} : ℝ) {op} ({vb} : ℝ))"
        )

    count_sub(TWO_SYM_CMP, two_sym)

    # Nat multi-unfold; norm_num → decide
    def unfold_norm(m: re.Match[str]) -> str:
        names = m.group(1).split()
        if names and all(nm in ndefs for nm in names):
            return f"unfold{m.group(1)}; decide"
        return m.group(0)

    count_sub(re.compile(r"unfold((?:\s+\w+)+)\s*;\s*norm_num\b"), unfold_norm)

    return text, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    files = 0
    for p in sorted(FORMAL.glob("*Priors.lean")):
        raw = p.read_text(encoding="utf-8")
        new, n = upgrade_file(raw)
        if n:
            files += 1
            total += n
            print(f"  {p.name}: {n}")
            if not args.dry_run:
                p.write_text(new, encoding="utf-8")
    print(f"{'Would apply' if args.dry_run else 'Applied'} {total} upgrades in {files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
