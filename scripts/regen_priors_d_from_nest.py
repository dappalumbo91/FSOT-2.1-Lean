#!/usr/bin/env python3
"""Rewrite *Priors.lean D_eff integers from the parent nest. YAML is not authority."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_compute import DOMAINS, derived_D_eff  # noqa: E402
from derive_extension_folds import _earliest_core, _parent  # noqa: E402

FOLDS = json.loads((ROOT / "data" / "extension_folds_derived.json").read_text(encoding="utf-8"))["folds"]
FORMAL = ROOT / "FSOT" / "Formal"

HEADER_RE = re.compile(r"extension domain ([A-Za-z0-9_]+)")
PAREN_RE = re.compile(r"\(([A-Za-z][A-Za-z0-9_]{3,})\)")
DEF_RE = re.compile(r"^(def (\w+)_D_eff : ℕ := )(\d+)\s*$", re.M)
STRIP = (
    "gapfill",
    "panel",
    "extension",
    "depth",
    "spine",
    "open",
    "live",
    "priors",
    "benchmark",
    "bundle",
)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _strip_suffixes(n: str) -> list[str]:
    out = [n]
    cur = n
    changed = True
    while changed:
        changed = False
        for suf in STRIP:
            if cur.endswith(suf) and len(cur) > len(suf) + 3:
                cur = cur[: -len(suf)]
                out.append(cur)
                changed = True
    return out


def _lookup_d(names: list[str]) -> int | None:
    fold_norm = {_norm(k): int(v["D_eff"]) for k, v in FOLDS.items()}
    core_norm = {_norm(k): derived_D_eff(k) for k in DOMAINS}
    cands: list[str] = []
    for raw in names:
        n = _norm(raw)
        if not n:
            continue
        cands.extend(_strip_suffixes(n))
        cands.append(n)
    seen: set[str] = set()
    ordered: list[str] = []
    for c in cands:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    for n in ordered:
        if n in fold_norm:
            return fold_norm[n]
        if n in core_norm:
            return core_norm[n]
    # longest fold key containing / contained in the candidate
    for n in ordered:
        hits = [(k, d) for k, d in fold_norm.items() if n in k or k in n]
        if len(hits) == 1:
            return hits[0][1]
        if hits:
            hits.sort(key=lambda kv: len(kv[0]), reverse=True)
            return hits[0][1]
        chits = [(k, d) for k, d in core_norm.items() if n in k or k in n]
        if chits:
            chits.sort(key=lambda kv: len(kv[0]), reverse=True)
            return chits[0][1]
    return None


def _names_from(path: Path, text: str) -> list[str]:
    names: list[str] = []
    m = HEADER_RE.search(text)
    if m:
        names.append(m.group(1))
    names.extend(PAREN_RE.findall(text.split("Generator:")[0] if "Generator:" in text else text[:800]))
    stem = path.stem
    if stem.endswith("Priors"):
        stem = stem[: -len("Priors")]
    names.append(stem)
    snake = re.sub(r"(?<!^)([A-Z])", r"_\1", stem)
    names.append(snake)
    return names


def main() -> int:
    n_files = n_changed = n_skip = n_miss = 0
    missed: list[str] = []
    for path in sorted(FORMAL.glob("*Priors.lean")):
        n_files += 1
        text = path.read_text(encoding="utf-8")
        def_m = DEF_RE.search(text)
        if not def_m:
            n_skip += 1
            continue
        names = _names_from(path, text)
        new_d = _lookup_d(names)
        if new_d is None:
            named = None
            for n in names + [path.stem.replace("Priors", "")]:
                named = _earliest_core(n)
                if named:
                    break
            if named:
                new_d = derived_D_eff(named)
            else:
                parent = _parent(path.stem.replace("Priors", ""), [])
                if parent:
                    new_d = derived_D_eff(parent)
        if new_d is None:
            n_miss += 1
            missed.append(path.name)
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
    print(f"priors files={n_files} changed={n_changed} no_D_def={n_skip} unmatched={n_miss}")
    for name in missed[:20]:
        print("  miss", name)
    if len(missed) > 20:
        print(f"  ... {len(missed) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
