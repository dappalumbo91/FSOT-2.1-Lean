#!/usr/bin/env python3
"""Export canonical FSOT constants from fsot_compute.py into data/canonical_constants.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from fsot_hash_gate import build_hash_gate_payload
from fsot_paths import authority_path_for_export, fsot_compute_path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "canonical_constants.json"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("fsot_compute", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def find_source() -> Path:
    return fsot_compute_path()


def main() -> int:
    source = find_source()
    mod = load_module(source)

    entries = {
        "source": authority_path_for_export(source),
        "seeds": {
            "pi": str(mod.PI),
            "e": str(mod.E),
            "phi": str(mod.PHI),
            "gamma": str(mod.GAMMA),
            "catalan_G": str(mod.G_CAT),
        },
        "layer1": {
            "alpha": str(mod.ALPHA),
            "psi_con": str(mod.PSI_CON),
            "eta_eff": str(mod.ETA_EFF),
            "beta": str(mod.BETA),
            "gamma_c": str(mod.GAMMA_C),
            "omega": str(mod.OMEGA),
            "theta_s": str(mod.THETA_S),
            "poof_factor": str(mod.POOF),
        },
        "layer2": {
            "coherence_efficiency": str(mod.C_EFF),
            "acoustic_bleed": str(mod.A_BLEED),
            "phase_variance": str(mod.P_VAR),
            "bleed_in_factor": str(mod.B_IN),
            "acoustic_inflow": str(mod.A_IN),
            "suction_factor": str(mod.SUCTION),
            "chaos_factor": str(mod.CHAOS),
            "perceived_param_base": str(mod.P_BASE),
            "new_perceived_param": str(mod.P_NEW),
            "consciousness_factor": str(mod.C_FACTOR),
            "k": str(mod.K),
            "c_cosm": str(mod.C_COSM),
        },
        "domain_scalars": {
            "S_cosm": str(mod.S_COSM),
            "S_quant": str(mod.S_QUANT),
        },
        "wave1": {
            name: str(r.computed)
            for name, r in (
                (res.name, res)
                for res in mod.wave1()
            )
        },
        "hash_gate": build_hash_gate_payload(source),
    }

    DATA.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Source: {source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())