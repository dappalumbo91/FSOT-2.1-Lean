#!/usr/bin/env python3
"""Write FSOT/Formal/DerivedNest.lean from the live Python nest."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_compute import (  # noqa: E402
    MEDIUM_ORIFICES,
    NEST_GENERATIONS,
    _fold_hits,
    derived_D_eff,
)

OUT = ROOT / "FSOT" / "Formal" / "DerivedNest.lean"


def _ident(name: str) -> str:
    return name.lower()


def main() -> int:
    lines = [
        "/-",
        "  Derived nest D_eff. Authority is vendor/fsot_compute.py NEST_GENERATIONS.",
        "  D_eff(g) = round(5 * 5^(g/(G-1))).",
        "  Hits/observed from named fold laws. Look is 1 except Atomic e/π and HEP 1-POOF/π.",
        "  FSOT.Formal.Scalar.get_domain_params still holds older assigned looks",
        "  for existing positivity proofs — do not quote it as live ToE D_eff.",
        "-/",
        "",
        "namespace FSOT.Formal.DerivedNest",
        "",
    ]
    for group in NEST_GENERATIONS:
        d = derived_D_eff(group[0])
        for name in group:
            ident = _ident(name)
            hits = _fold_hits(name)
            obs = "false" if name in MEDIUM_ORIFICES else "true"
            lines.append(f"def {ident} : Nat := {d}")
            lines.append(f"def {ident}_hits : Nat := {hits}")
            lines.append(f"def {ident}_observed : Bool := {obs}")
        lines.append("")
    q = derived_D_eff("Quantum_Mechanics")
    p = derived_D_eff("Particle_Physics")
    c = derived_D_eff("Cosmology")
    n = derived_D_eff("Neuroscience")
    chem = derived_D_eff("Chemistry")
    lines += [
        "theorem quantum_shares_particle : quantum_mechanics = particle_physics := by",
        "  unfold quantum_mechanics particle_physics; rfl",
        "",
        "theorem cosmology_ceiling : cosmology = 25 := by",
        "  unfold cosmology; rfl",
        "",
        "theorem neuroscience_is_eleven : neuroscience = 11 := by",
        "  unfold neuroscience; rfl",
        "",
        "theorem chemistry_is_first_default_look_above_floor : chemistry = 6 := by",
        "  unfold chemistry; rfl",
        "",
        "theorem hep_collision_is_one_hit : high_energy_physics_hits = 1 := by",
        "  unfold high_energy_physics_hits; rfl",
        "",
        "theorem cosmology_is_medium : cosmology_observed = false := by",
        "  unfold cosmology_observed; rfl",
        "",
        "theorem neuroscience_is_specimen : neuroscience_observed = true := by",
        "  unfold neuroscience_observed; rfl",
        "",
        "end FSOT.Formal.DerivedNest",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} particle={p} quantum={q} chemistry={chem} neuro={n} cosm={c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
