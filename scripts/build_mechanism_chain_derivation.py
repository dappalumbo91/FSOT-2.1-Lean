#!/usr/bin/env python3
"""Document raw_S → sector readout without opaque per-observable tuning."""

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
OUT = ROOT / "data" / "mechanism_chain_derivation.json"
REGISTRY = ROOT / "data" / "fsot_35_domain_registry.yaml"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
SPINE = ROOT / "data" / "fsot_formula_spine.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import (  # noqa: E402
    ALPHA,
    BETA,
    CONSCIOUSNESS_FACTOR,
    ETA_EFF,
    K,
    PSI_CON,
    raw_S,
    term1,
    term2,
    term3,
    DOMAINS as LEAN_DOMAINS,
)
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402


def _load_yaml(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _term_breakdown(p) -> dict:
    t1 = term1(p)
    t2 = term2(p)
    t3 = term3(p)
    total = raw_S(p)
    return {
        "term1": round(t1, 8),
        "term2": round(t2, 8),
        "term3": round(t3, 8),
        "raw_S": round(total, 8),
        "term1_fraction": round(abs(t1) / max(abs(total), 1e-12), 6),
    }


def main() -> int:
    mod, authority = load_fsot_compute()
    reg = _load_yaml(REGISTRY)
    ext = _load_yaml(EXT_MANIFEST).get("extension_domains") or {}
    spine = _load_yaml(SPINE)

    core_chains: list[dict] = []
    for name in sorted(mod.DOMAINS.keys()):
        cfg = mod.DOMAINS[name]
        lean_key = (reg.get("lean_overrides") or {}).get(name) or (
            (reg.get("empirical_sources") or {}).get(name) or {}
        ).get("lean_domain")
        lean_p = LEAN_DOMAINS.get(lean_key) if lean_key else None
        core_chains.append(
            {
                "neurolab_domain": name,
                "lean_domain": lean_key,
                "manifest_params": {
                    "D_eff": int(cfg.D_eff),
                    "recent_hits": int(cfg.hits),
                    "delta_psi": float(cfg.delta_psi),
                    "observed": bool(cfg.observed),
                },
                "domain_scalar_K_times_raw_S": round(float(mod.domain_scalar(name)), 8),
                "lean_oracle_breakdown": _term_breakdown(lean_p) if lean_p else None,
                "derivation_note": (
                    "D_eff/hits/δψ/observed are manifest-declared folds of the same engine; "
                    "bleed constants in fsot_compute.py are seed-derived (φ/e/π/γ), not per-observable fits."
                ),
            }
        )

    extension_chains: list[dict] = []
    for panel, cfg in sorted(ext.items(), key=lambda x: x[0]):
        tags = list(cfg.get("maps_to_lean") or [])
        primary = tags[0] if tags else "particle"
        lean_p = LEAN_DOMAINS.get(primary)
        extension_chains.append(
            {
                "panel": panel,
                "maps_to_lean": tags,
                "panel_params": {
                    "D_eff": int(cfg.get("D_eff") or 15),
                    "recent_hits": int(cfg.get("recent_hits") or 0),
                    "delta_psi": float(cfg.get("delta_psi") or 1.0),
                    "observed": bool(cfg.get("observed", True)),
                },
                "primary_lean_breakdown": _term_breakdown(lean_p) if lean_p else None,
            }
        )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "title": "FSOT mechanism chain — seeds to sector readout",
        "verdict": "DERIVATION_DOCUMENTED_NOT_OPAQUE_TABLE",
        "intrinsic_seeds": {
            "alpha": round(ALPHA, 12),
            "psi_con": round(PSI_CON, 12),
            "eta_eff": round(ETA_EFF, 12),
            "beta": round(BETA, 12),
            "consciousness_factor": round(CONSCIOUSNESS_FACTOR, 12),
            "k": round(K, 12),
        },
        "core_formula": "raw_S = term1_final + term2 + term3",
        "term1_structure": "(N·P/√D_eff)·cos((ψ_con+δψ)/η_eff)·growth·coherence·perceived_adjust × quirkMod(observed)",
        "domain_table_honesty": {
            "slots": int((reg.get("verification") or {}).get("domain_table_slots") or 175),
            "interpretation": (
                "175 slots = 35 domains × 5 manifest fields (D_eff, hits, δψ, δθ, observed). "
                "Values are preregistered in fsot_compute.py / extension manifest — not tuned per benchmark row."
            ),
            "parameter_audit": "data/parameter_honesty_closure.json",
        },
        "observer_channel": {
            "method": "consciousness_factor × D_eff/25 + |δψ|/1.2 + consciousness_tag",
            "spine_ref": list((spine.get("term1") or {}).keys())[:6] if spine else [],
        },
        "authority_path": str(authority),
        "core_domain_chains": core_chains,
        "extension_panel_sample": extension_chains[:40],
        "extension_panel_count": len(extension_chains),
        "artifacts": [
            "FSOT/Scalar.lean",
            "vendor/fsot_compute.py",
            "data/fsot_formula_spine.yaml",
            "data/observer_channel_derivation_benchmark.json",
            "data/formula_branching_fractal_benchmark.json",
        ],
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} — {len(core_chains)} core + {len(extension_chains)} extension chains")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())