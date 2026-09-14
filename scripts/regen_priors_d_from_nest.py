#!/usr/bin/env python3
"""Rewrite *Priors.lean D_eff integers from the parent nest. YAML is not authority."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDS = json.loads((ROOT / "data" / "extension_folds_derived.json").read_text(encoding="utf-8"))["folds"]
FORMAL = ROOT / "FSOT" / "Formal"

HEADER_RE = re.compile(r"extension domain ([A-Za-z0-9_]+)")
DEF_RE = re.compile(r"^(def (\w+)_D_eff : ℕ := )(\d+)\s*$", re.M)
EQ_RE = re.compile(r"(\w+_D_eff) = (\d+)")


def _norm(s: str) -> str:
    return s.lower().replace("_", "")


def main() -> int:
    lookup = {_norm(k): v for k, v in FOLDS.items()}
    n_files = n_changed = n_miss = 0
    for path in sorted(FORMAL.glob("*Priors.lean")):
        n_files += 1
        text = path.read_text(encoding="utf-8")
        m = HEADER_RE.search(text)
        key = None
        if m:
            key = lookup.get(_norm(m.group(1)))
        if key is None:
            # try filename AcousticResonanceMaterialsPriors → acoustic_resonance_materials
            stem = path.stem
            if stem.endswith("Priors"):
                stem = stem[: -len("Priors")]
            # insert underscores before caps
            snake = re.sub(r"(?<!^)([A-Z])", r"_\1", stem).lower()
            key = lookup.get(_norm(snake))
        if key is None:
            n_miss += 1
            continue
        new_d = int(key["D_eff"])
        def_m = DEF_RE.search(text)
        if not def_m:
            n_miss += 1
            continue
        old_d = int(def_m.group(3))
        if old_d == new_d:
            continue
        prefix = def_m.group(2)
        text2 = DEF_RE.sub(rf"\g<1>{new_d}", text, count=1)
        text2 = re.sub(
            rf"({re.escape(prefix)}_D_eff) = {old_d}\b",
            rf"\1 = {new_d}",
            text2,
        )
        if text2 != text:
            path.write_text(text2, encoding="utf-8")
            n_changed += 1
    print(f"priors files={n_files} changed={n_changed} unmatched_or_skipped={n_miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
