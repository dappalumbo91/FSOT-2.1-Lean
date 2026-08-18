#!/usr/bin/env python3
"""Copy headline ledgers from FSOT-Genetics and FSOT-Quantum into this hub.

Does not rewrite predictions. Writes results/siblings/ only.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "siblings"

CANDIDATES = {
    "genetics": [
        Path(r"C:\Users\damia\Desktop\FSOT-Genetics"),
        ROOT.parent / "FSOT-Genetics",
        ROOT / "_ref" / "FSOT-Genetics",
    ],
    "quantum": [
        Path(r"C:\Users\damia\Desktop\fsot quantum"),
        Path(r"C:\Users\damia\Desktop\FSOT-Quantum"),
        ROOT.parent / "FSOT-Quantum",
        ROOT / "_ref" / "FSOT-Quantum",
    ],
}

GENETICS_FILES = [
    ("data/product_vs_alphafold.json", "product_vs_alphafold.json"),
    ("docs/PRODUCT_FREEZE.md", "PRODUCT_FREEZE.md"),
    ("data/af_coverage.json", "af_coverage.json"),
]

QUANTUM_FILES = [
    ("docs/STATUS.md", "STATUS.md"),
    ("docs/H0_TENSION.md", "H0_TENSION.md"),
    ("docs/CONCEPTS.md", "CONCEPTS.md"),
    ("results/h0_tension.json", "h0_tension.json"),
    ("results/contested_sectors.json", "contested_sectors.json"),
    ("results/FOLD_NOT_HILBERT.md", "FOLD_NOT_HILBERT.md"),
]


def _first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.is_dir():
            return p
    return None


def _copy(src_root: Path, rel_src: str, dest_dir: Path, dest_name: str) -> dict:
    src = src_root / rel_src
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / dest_name
    if not src.is_file():
        return {"src": rel_src, "ok": False, "error": "missing"}
    shutil.copy2(src, dest)
    return {"src": rel_src, "dest": str(dest.relative_to(ROOT)), "ok": True, "bytes": dest.stat().st_size}


def main() -> int:
    report: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_pin_prefix": "D1D38A",
        "hub": "FSOT-2.1-Lean",
        "siblings": {},
    }
    g = _first_existing(CANDIDATES["genetics"])
    q = _first_existing(CANDIDATES["quantum"])
    report["siblings"]["genetics"] = {
        "root": str(g) if g else None,
        "url": "https://github.com/dappalumbo91/FSOT-Genetics",
        "files": [_copy(g, a, OUT / "genetics", b) for a, b in GENETICS_FILES] if g else [],
    }
    report["siblings"]["quantum"] = {
        "root": str(q) if q else None,
        "url": "https://github.com/dappalumbo91/FSOT-Quantum",
        "files": [_copy(q, a, OUT / "quantum", b) for a, b in QUANTUM_FILES] if q else [],
    }

    # Compact machine headlines for the hub scoreboard
    headlines: dict = {"pin": "D1D38A"}
    prod = OUT / "genetics" / "product_vs_alphafold.json"
    if prod.is_file():
        p = json.loads(prod.read_text(encoding="utf-8"))
        s = p.get("summary") or {}
        headlines["genetics_product"] = {
            "n": s.get("n"),
            "fsot_product_median_A": s.get("fsot_product_median_A"),
            "alphafold_median_A": s.get("alphafold_median_A"),
            "fsot_bulk_median_A": s.get("fsot_bulk_median_A"),
            "product_sub2A": s.get("product_sub2A"),
            "free_parameters": s.get("free_parameters"),
            "freeze": "2026-08-13",
        }
    h0 = OUT / "quantum" / "h0_tension.json"
    if h0.is_file():
        h = json.loads(h0.read_text(encoding="utf-8"))
        headlines["quantum_h0_bubble"] = {
            "overall_ok": h.get("overall_ok"),
            "h0_global": h.get("h0_global"),
            "bubble_bleed_fraction": h.get("bubble_bleed_fraction"),
            "policy": h.get("policy"),
        }
    cs = OUT / "quantum" / "contested_sectors.json"
    if cs.is_file():
        c = json.loads(cs.read_text(encoding="utf-8"))
        headlines["quantum_contested"] = {
            "n_ok": c.get("n_ok"),
            "n": c.get("n"),
            "overall_ok": c.get("overall_ok"),
        }
    report["headlines"] = headlines
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sync_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT / 'sync_report.json'}")
    for name, block in report["siblings"].items():
        ok = sum(1 for f in block["files"] if f.get("ok"))
        print(f"  {name}: {ok}/{len(block['files'])} from {block['root']}")
    return 0 if (g or q) else 1


if __name__ == "__main__":
    raise SystemExit(main())
