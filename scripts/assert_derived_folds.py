#!/usr/bin/env python3
"""Kill-path: leftover assigned D / YAML leak / species knobs / matter-budget object."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import (  # noqa: E402
    DOMAINS,
    MEDIUM_ORIFICES,
    SPECIES,
    S_CHEM,
    S_COSM,
    S_QUANT,
    _fold_observed,
    derived_D_eff,
    domain_scalar,
)
from fsot_canonical_adapter import canonical_domain_scalar  # noqa: E402


def main() -> int:
    issues: list[str] = []

    if derived_D_eff("Quantum_Mechanics") != derived_D_eff("Particle_Physics"):
        issues.append("QM must share Particle nest D")
    if derived_D_eff("Neuroscience") < 5:
        issues.append("Neuroscience D below particle floor")
    if hasattr(SPECIES[0], "D_eff"):
        issues.append("SPECIES still has per-species D_eff")
    if any(sp.name == "Honeybee" and getattr(sp, "D_eff", None) == 4 for sp in SPECIES):
        issues.append("Honeybee D=4 knob still present")

    s_human = None
    for sp in SPECIES:
        if sp.name == "Human":
            s_human = domain_scalar("Neuroscience")
    if s_human is None:
        issues.append("Human missing from SPECIES")

    for name, cfg in DOMAINS.items():
        if bool(cfg.observed) != _fold_observed(name):
            issues.append(f"observed mismatch {name}")
        if (name in MEDIUM_ORIFICES) and cfg.observed:
            issues.append(f"medium orifice marked specimen: {name}")

    # YAML cannot leak into live S
    ext = json.loads((ROOT / "data" / "extension_folds_derived.json").read_text(encoding="utf-8"))
    folds = ext["folds"]
    sample = next(iter(folds))
    yaml_d = folds[sample]["yaml_D_eff_ignored"]
    live_d = folds[sample]["D_eff"]
    s = canonical_domain_scalar(sample)
    if yaml_d != live_d:
        # S must still be computable; KeyError would have raised
        if s == 0:
            issues.append(f"extension {sample} scalar is zero")

    # Matter budget uses chemistry, not QM
    omb_chem = abs(float(S_COSM)) * (1.0 - float(S_CHEM))
    omb_qm = abs(float(S_COSM)) * (1.0 - float(S_QUANT))
    if abs(omb_chem - omb_qm) < 1e-12:
        issues.append("S_chem collapsed onto S_quant — baryon object not relabeled")
    err_chem = abs(omb_chem - 0.02237) / 0.02237 * 100
    err_qm = abs(omb_qm - 0.02237) / 0.02237 * 100
    if err_qm < 5:
        issues.append("QM-class Omega_b no longer shows the nest-collapse miss")
    if err_chem > 0.5:
        issues.append(f"Chemistry-rung Omega_b outside 0.5% ({err_chem:.3f}%)")

    # Overlay: a known extension must not KeyError
    try:
        canonical_domain_scalar("Immunology")
    except KeyError as e:
        issues.append(f"extension overlay KeyError: {e}")

    if issues:
        print("FAIL")
        for i in issues:
            print(" -", i)
        return 1
    print("OK derived folds")
    print(f"  Neuro D={derived_D_eff('Neuroscience')} QM D={derived_D_eff('Quantum_Mechanics')}")
    print(f"  Omega_b chem={omb_chem:.6f} ({err_chem:.3f}%)  qm-class={omb_qm:.6f} ({err_qm:.3f}%)")
    print(f"  medium orifices={len(MEDIUM_ORIFICES)} species={len(SPECIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
