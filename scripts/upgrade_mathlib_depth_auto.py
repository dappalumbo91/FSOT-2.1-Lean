#!/usr/bin/env python3
"""
Auto-upgrade Lean proofs toward constructive Mathlib depth.

Only transforms *safe* Nat/decidable patterns — never rewrites Real residual
certificates that need norm_num.

Safe patterns:
  - `unfold <natDef>; norm_num` → `unfold <natDef>; decide` when def is `ℕ`/`Nat`
  - `:= by norm_num` on theorems whose type is a Nat equality / 0 < Nat

Usage:
  python scripts/upgrade_mathlib_depth_auto.py --dry-run --all
  python scripts/upgrade_mathlib_depth_auto.py --all
  python scripts/upgrade_mathlib_depth_auto.py --engine
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from mathlib_rederivation_lib import ENGINE_WAVES  # noqa: E402

NAT_DEF_RE = re.compile(
    r"def\s+(\w+)\s*:\s*(?:ℕ|Nat)\s*:=\s*",
    re.MULTILINE,
)
# theorem ... : 0 < foo := by unfold foo; norm_num
THM_NAT_POS = re.compile(
    r"((?:theorem|lemma)\s+\w+[\s\S]*?:\s*0\s*<\s*(\w+)\s*:=\s*by\s*\n"
    r"(?:\s*)unfold\s+\2\s*;\s*)norm_num\b",
    re.MULTILINE,
)
# theorem ... : foo = N := by unfold foo; norm_num
THM_NAT_EQ = re.compile(
    r"((?:theorem|lemma)\s+\w+[\s\S]*?:\s*(\w+)\s*=\s*\(?\d+\)?(?:\s*:\s*ℕ)?\s*:=\s*by\s*\n"
    r"(?:\s*)unfold\s+\2\s*;\s*)norm_num\b",
    re.MULTILINE,
)
# generic unfold natDef; norm_num when natDef known
UNFOLD_ANY = re.compile(r"(\bunfold\s+(\w+)\s*;\s*)norm_num\b")


def nat_defs_in(text: str) -> set[str]:
    return set(NAT_DEF_RE.findall(text))


def upgrade_text(text: str) -> tuple[str, int]:
    nats = nat_defs_in(text)
    n = 0

    def repl_unfold(m: re.Match[str]) -> str:
        nonlocal n
        name = m.group(2)
        if name in nats:
            n += 1
            return f"{m.group(1)}decide"
        return m.group(0)

    text = UNFOLD_ANY.sub(repl_unfold, text)

    # Explicit Nat pos/eq patterns even if def form differs slightly
    text2, c = THM_NAT_POS.subn(r"\1decide", text)
    n += c
    text = text2
    text2, c = THM_NAT_EQ.subn(r"\1decide", text)
    n += c
    text = text2
    return text, n


def process_file(path: Path, *, dry_run: bool) -> int:
    raw = path.read_text(encoding="utf-8")
    new, n = upgrade_text(raw)
    if n and not dry_run and new != raw:
        path.write_text(new, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--engine", action="store_true")
    ap.add_argument("--priors", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if args.all or (not args.engine and not args.priors):
        args.engine = True
        args.priors = True

    engine_mods = {m for w in ENGINE_WAVES for m in w["modules"]}
    total = 0
    files = 0
    for path in sorted(FORMAL.glob("*.lean")):
        stem = path.stem
        if args.engine and stem in engine_mods:
            pass
        elif args.priors and "Priors" in stem:
            pass
        else:
            continue
        n = process_file(path, dry_run=args.dry_run)
        if n:
            files += 1
            total += n
            print(f"  {path.name}: {n}")
    print(f"{'Would apply' if args.dry_run else 'Applied'} {total} upgrades in {files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
