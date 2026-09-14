#!/usr/bin/env python3
"""Derive extension D_eff from the parent core nest. YAML integers are not authority."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_compute import DOMAINS, derived_D_eff, _fold_hits, _fold_look  # noqa: E402

MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
OUT = ROOT / "data" / "extension_folds_derived.json"

LEAN_TO_CORE = {
    "cosmological": "Cosmology",
    "astronomical": "Astronomy",
    "blackhole": "Astrophysics",
    "cmb": "Cosmology",
    "energy": "Thermodynamics",
    "fusion": "Nuclear_Physics",
    "plasma": "Condensed_Matter",
    "medical": "Biochemistry",
    "biological": "Biology",
    "galactic": "Astronomy",
    "particle": "Particle_Physics",
    "quantum": "Quantum_Mechanics",
    "atomic": "Atomic_Physics",
    "chemical": "Chemistry",
    "ocean": "Oceanography",
    "climate": "Meteorology",
    "seismic": "Seismology",
    "neural": "Neuroscience",
    "economic": "Economics",
    "planetary": "Planetary_Science",
    "nuclear": "Nuclear_Physics",
    "fluid": "Fluid_Dynamics",
    "optical": "Optics",
    "acoustic": "Acoustics",
}


def _parent(name: str, tags: list[str]) -> str:
    if name in DOMAINS:
        return name
    for t in tags:
        core = LEAN_TO_CORE.get(str(t).lower())
        if core in DOMAINS:
            return core
    lower = name.lower()
    for token, core in LEAN_TO_CORE.items():
        if token in lower and core in DOMAINS:
            return core
    for core in DOMAINS:
        if core.lower().replace("_", "") in lower.replace("_", ""):
            return core
    return "Cosmology"


def main() -> int:
    if yaml is None:
        print("PyYAML required", file=sys.stderr)
        return 1
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    rows = {}
    for name, cfg in (spec.get("extension_domains") or {}).items():
        tags = list(cfg.get("maps_to_lean") or [])
        parent = _parent(name, tags)
        yaml_d = cfg.get("D_eff")
        d = derived_D_eff(parent)
        rows[name] = {
            "parent_core": parent,
            "D_eff": d,
            "yaml_D_eff_ignored": yaml_d,
            "look": float(_fold_look(parent)),
            "hits": _fold_hits(parent),
            "observed": bool(DOMAINS[parent].observed),
        }
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Extension D_eff is the parent core's derived nest value. YAML integers are ignored.",
        "n": len(rows),
        "folds": rows,
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    n_diff = sum(1 for r in rows.values() if r["yaml_D_eff_ignored"] != r["D_eff"])
    print(f"wrote {OUT} n={len(rows)} yaml_D_differs={n_diff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
