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
    "chemistry": "Chemistry",
    "ocean": "Oceanography",
    "climate": "Meteorology",
    "seismic": "Seismology",
    "seismology": "Seismology",
    "neural": "Neuroscience",
    "neuro": "Neuroscience",
    "economic": "Economics",
    "economics": "Economics",
    "planetary": "Planetary_Science",
    "nuclear": "Nuclear_Physics",
    "fluid": "Fluid_Dynamics",
    "optical": "Optics",
    "optics": "Optics",
    "acoustic": "Acoustics",
    "acoustical": "Acoustics",
    "materials": "Materials_Science",
    "material": "Materials_Science",
    "psychology": "Psychology",
    "psychometric": "Psychology",
    "computing": "Quantum_Computing",
    "interferometry": "Optics",
    "meteorology": "Meteorology",
    "ecology": "Ecology",
    "geophysics": "Geophysics",
    "sociology": "Sociology",
    "engineering": "Thermodynamics",
    "hardware": "Quantum_Computing",
    "gpu": "Quantum_Computing",
    "cuda": "Quantum_Computing",
    "esp32": "Quantum_Computing",
    "desi": "Cosmology",
    "chembl": "Chemistry",
    "alphafold": "Biochemistry",
    "circuit": "Electromagnetism",
    "cache": "Quantum_Computing",
    "interconnect": "Quantum_Computing",
    "endf": "Nuclear_Physics",
    "iaea": "Nuclear_Physics",
    "dzhanibekov": "Fluid_Dynamics",
    "optimade": "Condensed_Matter",
    "coding": "Quantum_Computing",
    "codata": "Particle_Physics",
    "gaia": "Astronomy",
    "gbif": "Ecology",
    "gwas": "Biology",
    "gwosc": "Particle_Astrophysics",
    "gwtc": "Particle_Astrophysics",
    "nist": "Atomic_Physics",
    "noaa": "Oceanography",
    "tides": "Oceanography",
    "nufit": "Particle_Physics",
    "neutrino": "Particle_Physics",
    "lmfdb": "Particle_Physics",
    "oeis": "Particle_Physics",
    "dft": "Condensed_Matter",
    "antimatter": "Particle_Physics",
    "processor": "Quantum_Computing",
    "cpack": "Quantum_Computing",
}

# First-tag dumps. Only used if the name and other tags say nothing.
WEAK_TAGS = frozenset({"particle", "energy", "quantum", "galactic"})


def _compact(s: str) -> str:
    return s.lower().replace("_", "")


def _earliest_core(text: str) -> str | None:
    """Leading orifice in the name: earliest start, then longest token."""
    compact = _compact(text)
    lower = text.lower()
    hits: list[tuple[int, int, str]] = []
    for core in DOMAINS:
        cc = _compact(core)
        i = compact.find(cc)
        if i >= 0:
            hits.append((i, -len(cc), core))
    for token, core in LEAN_TO_CORE.items():
        if core not in DOMAINS:
            continue
        i = lower.find(token)
        if i >= 0:
            hits.append((i, -len(token), core))
    if not hits:
        return None
    hits.sort()
    return hits[0][2]


def _parent(name: str, tags: list[str]) -> str:
    """Parent is the orifice of the name. Tags are fallback, not a particle dump."""
    if name in DOMAINS:
        return name
    named = _earliest_core(name)
    if named:
        return named
    strong: list[tuple[int, str]] = []
    weak: list[tuple[int, str]] = []
    for t in tags:
        mapped = _earliest_core(str(t)) or LEAN_TO_CORE.get(str(t).lower())
        if mapped not in DOMAINS:
            continue
        tl = str(t).lower()
        bucket = weak if tl in WEAK_TAGS else strong
        bucket.append((len(tl), mapped))
    strong.sort(reverse=True)
    if strong:
        return strong[0][1]
    weak.sort(reverse=True)
    if weak:
        return weak[0][1]
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
