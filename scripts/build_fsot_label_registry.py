#!/usr/bin/env python3
"""Build data/fsot_label_registry.json from manifests, rules, and roadmaps."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fsot_label_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_label_registry_lib import (  # noqa: E402
    EXPANSION_ROADMAP,
    EXTENSION_MANIFEST,
    OVERLAY_RULES,
    PREREG_MANIFEST,
    humanize_domain_key,
    resolve_tier_label,
)


def _yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _tier_labels() -> dict[str, str]:
    labels: dict[str, str] = {
        "6": "Core scalar spine (NeuroLab alignment)",
        "12": "Extension plasma / immunology / climate cohort",
        "18": "Geophysical depth (seismology / tectonics / stratigraphy)",
        "25": "Cosmology bubble-bleed / SH0ES / fluid spacetime",
        "31": "Math generator benchmark formula eval (FO-200/210/220)",
        "32": "Airfoil RMSE gas-medium readout (FO-212)",
        "39": "Propulsion / electrical / HVAC thermal systems",
        "43": "Cybersecurity engineering (Tier H)",
        "51": "Consciousness soul bridge + symbolic archetype",
        "79": "Multi-framework cross-proof export (Lean → Coq/Isabelle/Python)",
        "80": "Full formal spine (1,241 numeric obligations)",
        "83": "Transcendental bounds (π/e interval certificates)",
        "84": "Rust f64 obligation replay",
        "91": "Seven-way bare-metal runtime (QEMU + ESP32 serial)",
    }
    roadmap = _yaml(EXPANSION_ROADMAP)
    for tier_key, domains in (roadmap.get("completed_tiers") or {}).items():
        num = tier_key.replace("tier_", "")
        if num not in labels and domains:
            labels[num] = f"Tier {num} — {humanize_domain_key(str(domains[0]))} + cluster"
    return labels


def _extension_domains() -> dict[str, dict]:
    manifest = _yaml(EXTENSION_MANIFEST)
    out: dict[str, dict] = {}
    for key, cfg in (manifest.get("extension_domains") or {}).items():
        tier = cfg.get("tier", "?")
        out[key] = {
            "display_name": humanize_domain_key(key),
            "tier": tier,
            "tier_label": resolve_tier_label(tier),
            "lean_module": cfg.get("lean_module"),
            "D_eff": cfg.get("D_eff"),
        }
    return out


def _fo_rules() -> dict[str, str]:
    out: dict[str, str] = {}
    if OVERLAY_RULES.exists():
        doc = json.loads(OVERLAY_RULES.read_text(encoding="utf-8"))
        for rule in doc.get("rules") or []:
            rid = str(rule.get("id") or "")
            if rid:
                out[rid] = str(rule.get("name") or rid)
    return out


def _math_rule_codes() -> dict[str, str]:
    out: dict[str, str] = {}
    rules_root = ROOT / "vendor" / "math_generator" / "rules"
    for path in sorted(rules_root.glob("*_RULES.json")) if rules_root.exists() else []:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for rule in doc.get("rules") or []:
            rid = str(rule.get("id") or "")
            if rid:
                out[rid] = str(rule.get("name") or rid)
    return out


def _prereg() -> dict[str, str]:
    out: dict[str, str] = {}
    manifest = _yaml(PREREG_MANIFEST)
    for row in manifest.get("predictions") or []:
        pid = str(row.get("id") or "")
        if pid:
            out[pid] = str(row.get("name") or pid)
    return out


def _smiles_sections() -> dict[str, str]:
    return {
        "§21 Protein ΔG": "SMILES Lab §21 — protein folding free energy (ΔG)",
        "§22 Amino Acid pKa": "SMILES Lab §22 — amino acid acid dissociation (pKa)",
        "§23 Drug pKd": "SMILES Lab §23 — drug binding affinity (pKd)",
        "§24 Enzyme kcat": "SMILES Lab §24 — enzyme turnover (kcat)",
        "§35 Michaelis Km": "SMILES Lab §35 — Michaelis constant (Km)",
        "§65 Enzyme pKi": "SMILES Lab §65 — enzyme inhibition (pKi)",
        "§71 DNA Stacking ΔG": "SMILES Lab §71 — DNA stacking free energy (ΔG)",
        "§92 Protein Fold Rate": "SMILES Lab §92 — protein folding rate log(kf)",
    }


def build() -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "purpose": "Human-readable labels for opaque FSOT codes (tiers, FO/PRED/rules, obligations)",
        "tiers": _tier_labels(),
        "extension_domains": _extension_domains(),
        "math_generator_rules": _fo_rules(),
        "math_generator_rule_codes": _math_rule_codes(),
        "prereg_predictions": _prereg(),
        "smiles_sections": _smiles_sections(),
        "obligation_kind_glossary": {
            "lt_half": "Empirical pooled median error below 0.5% gate",
            "nat_pos": "Observable / record count is positive",
            "pos": "Scalar constant is strictly positive",
        },
        "connective_symbols": {
            "warp_psi_friction": "Warp ψ friction coupling (Tier 79 actuation connective)",
            "warp_psi_node": "Warp ψ node coupling (Tier 79 actuation connective)",
        },
        "code_patterns": {
            "FO-NNN": "FSOT overlay benchmark promotion rule — see math_generator_rules",
            "PRED-NNN": "Preregistered prediction — see prereg_predictions",
            "AA/MS/PL-NNN": "Math generator domain rule — see math_generator_rule_codes",
            "tier_N": "Expansion roadmap tier — see tiers",
        },
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  extension_domains: {len(doc['extension_domains'])}")
    print(f"  FO rules: {len(doc['math_generator_rules'])}")
    print(f"  math rule codes: {len(doc['math_generator_rule_codes'])}")
    print(f"  prereg: {len(doc['prereg_predictions'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())