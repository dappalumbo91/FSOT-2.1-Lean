#!/usr/bin/env python3
"""
Export a portable verification certificate after a green FSOT verification run.

Writes data/certificate.json linking:
  - hash-gate authority digest
  - canonical constants / Wave-1 cache
  - proof ledger entries
  - Lean theorem inventory from FSOT.Formal.*
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LEDGER_PATH = DATA / "proof_ledger.yaml"
CACHE_PATH = DATA / "canonical_constants.json"
CERT_PATH = DATA / "certificate.json"
REGISTRY_PATH = DATA / "lab_registry.json"
TOOLCHAIN_PATH = ROOT / "lean-toolchain"
FORMAL_DIR = ROOT / "FSOT" / "Formal"

LEAN_TARGETS = [
    "FSOT.Formal.Bounds",
    "FSOT.Formal.Scalar",
    "FSOT.Formal.Theorems",
    "FSOT.Formal.Cosmology",
    "FSOT.Formal.Domains",
    "FSOT.Formal.Genomic",
    "FSOT.Formal.BrainPriors",
    "FSOT.Formal.CodonPriors",
    "FSOT.Formal.ProteinPriors",
    "FSOT.Formal.ProteinFormulas",
    "FSOT.Formal.CosmologyLab",
    "FSOT.Formal.FuelPriors",
    "FSOT.Formal.SpeciesPriors",
    "FSOT.Formal.CameoPriors",
    "FSOT.Formal.TrinaryOSPriors",
    "FSOT.Formal.PhotonicForge",
    "FSOT.Formal.VibRegisterPriors",
    "FSOT.Formal.MagneticStringPriors",
    "FSOT.Formal.EvolutionPriors",
    "FSOT.Formal.WeatherPriors",
    "FSOT.Formal.LinguisticsPriors",
    "FSOT.Formal.UnifiedDBPriors",
    "FSOT.Formal.CosmologyWave4",
    "FSOT.Formal.KronosPriors",
    "FSOT.Formal.KnowledgeBasePriors",
    "FSOT.Formal.MathGeneratorPriors",
    "FSOT.Formal.TrinaryFluidPriors",
    "FSOT.Formal.SoulSiblingPriors",
    "FSOT.Formal.LeanProofsBridge",
    "FSOT.Formal.FormulaCorpusPriors",
    "FSOT.Formal.CellularPriors",
    "FSOT.Formal.BlackHoleThesisPriors",
    "FSOT.Formal.NeuronHybridPriors",
    "FSOT.Formal.NeuronCohortPriors",
    "FSOT.Formal.NeuronCohortStrataPriors",
    "FSOT.Formal.AetherPrimePriors",
    "FSOT.Formal.MagicCirclePriors",
    "FSOT.Formal.ExperimentSynthesisPriors",
    "FSOT.Formal.DomainCoveragePriors",
    "FSOT.Formal.DomainPrecisionPriors",
    "FSOT.Formal.IntelligenceCompressionPriors",
    "FSOT.Formal.PlasmaPhysicsPriors",
    "FSOT.Formal.ImmunologyPriors",
    "FSOT.Formal.ClimateSciencePriors",
    "FSOT.Formal.BiologyStrictEmpiricalPriors",
    "FSOT.Formal.NeuronCohortTrainHoldoutPriors",
    "FSOT.Formal.ThesisSimulationPriors",
    "FSOT.Formal.EmergentDomainPriors",
    "FSOT.Formal.Lab",
    "FSOT",
]

THEOREM_RE = re.compile(r"^\s*(theorem|lemma)\s+([A-Za-z0-9_']+)")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_toolchain() -> str:
    if TOOLCHAIN_PATH.exists():
        return TOOLCHAIN_PATH.read_text(encoding="utf-8").strip()
    return "unknown"


def load_ledger() -> dict:
    if not LEDGER_PATH.exists():
        return {"meta": {}, "entries": [], "playbook_patterns": []}
    text = LEDGER_PATH.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    # Minimal fallback: treat as metadata-only if PyYAML missing
    return {"meta": {"note": "PyYAML not installed; ledger not parsed"}, "entries": []}


def scan_formal_theorems() -> dict[str, list[str]]:
    by_module: dict[str, list[str]] = {}
    if not FORMAL_DIR.exists():
        return by_module
    for path in sorted(FORMAL_DIR.glob("*.lean")):
        names: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            m = THEOREM_RE.match(line)
            if m:
                names.append(m.group(2))
        by_module[path.stem] = names
    return by_module


def count_sorry(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(
        1
        for line in path.read_text(encoding="utf-8").splitlines()
        if re.search(r"\bsorry\b", line) and not line.strip().startswith("--")
    )


def domain_theorems_from_ledger(ledger: dict) -> list[dict]:
    out: list[dict] = []
    for entry in ledger.get("entries", []):
        lean = entry.get("lean") or {}
        if lean.get("theorem"):
            out.append(
                {
                    "id": entry.get("id"),
                    "claim": entry.get("claim"),
                    "status": entry.get("status"),
                    "domain": entry.get("domain"),
                    "lean_module": lean.get("module"),
                    "lean_theorem": lean.get("theorem"),
                }
            )
    return out


def build_certificate(*, lean_build_ok: bool, authority_path: str | None = None) -> dict:
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}
    ledger = load_ledger()
    formal = scan_formal_theorems()

    sorry_count = sum(count_sorry(p) for p in FORMAL_DIR.glob("*.lean"))

    source_files = [
        ROOT / "FSOT" / "Formal" / "Scalar.lean",
        ROOT / "FSOT" / "Formal" / "Bounds.lean",
        ROOT / "FSOT" / "Formal" / "Theorems.lean",
        ROOT / "FSOT" / "Formal" / "Cosmology.lean",
        ROOT / "FSOT" / "Formal" / "Domains.lean",
        ROOT / "FSOT" / "Formal" / "Genomic.lean",
        ROOT / "FSOT" / "Formal" / "BrainPriors.lean",
        ROOT / "FSOT" / "Formal" / "CodonPriors.lean",
        ROOT / "FSOT" / "Formal" / "ProteinPriors.lean",
        ROOT / "FSOT" / "Formal" / "ProteinFormulas.lean",
        ROOT / "scripts" / "gen_brain_priors_lean.py",
        ROOT / "scripts" / "gen_codon_priors_lean.py",
        ROOT / "scripts" / "gen_protein_priors_lean.py",
        ROOT / "scripts" / "gen_protein_formulas_lean.py",
        ROOT / "scripts" / "domain_scalar_oracle.py",
        ROOT / "scripts" / "fsot_verification_runner.py",
        LEDGER_PATH,
        CACHE_PATH,
    ]
    source_manifest = {
        str(p.relative_to(ROOT)).replace("\\", "/"): sha256_file(p)
        for p in source_files
        if p.exists()
    }

    hash_gate = cache.get("hash_gate", {})
    authority_sha = hash_gate.get("authority_sha256")

    lab_registry = {}
    if REGISTRY_PATH.exists():
        lab_registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    cert = {
        "certificate_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lean_toolchain": read_toolchain(),
        "mathlib_pin": "v4.31.0",
        "lean_build_ok": lean_build_ok,
        "lean_targets": LEAN_TARGETS,
        "sorry_count_formal": sorry_count,
        "authority": {
            "path": authority_path or hash_gate.get("authority_path"),
            "sha256": authority_sha,
        },
        "wave1": cache.get("wave1", {}),
        "domain_scalars": cache.get("domain_scalars", {}),
        "ledger_meta": ledger.get("meta", {}),
        "proved_claims": domain_theorems_from_ledger(ledger),
        "playbook_patterns": ledger.get("playbook_patterns", []),
        "lab_registry": {
            "present": bool(lab_registry),
            "smiles_records": lab_registry.get("smiles_lab", {}).get("total_records"),
            "smiles_mapped": lab_registry.get("smiles_lab", {}).get("mapped_records"),
            "thalamic_nuclei": lab_registry.get("neurolab", {})
            .get("thalamic_gate", {})
            .get("n_nuclei"),
            "domain_bridge_count": len(
                lab_registry.get("neurolab", {}).get("domain_bridge", [])
            ),
            "brain_component_priors_count": lab_registry.get("neurolab_bio", {})
            .get("brain_component_priors", {})
            .get("count"),
            "brain_component_priors_sha256": lab_registry.get("neurolab_bio", {})
            .get("brain_component_priors", {})
            .get("sha256"),
            "translation_total": lab_registry.get("neurolab_bio", {}).get("translation_total"),
        },
        "formal_theorem_inventory": formal,
        "source_manifest_sha256": source_manifest,
        "reproduce": {
            "sync_constants": "python scripts/sync_canonical_constants.py",
            "verify": "python scripts/fsot_verification_runner.py",
            "lean_build": "lake build " + " ".join(LEAN_TARGETS),
            "export": "python scripts/export_certificate.py",
        },
    }
    return cert


def main() -> int:
    parser = argparse.ArgumentParser(description="Export FSOT verification certificate")
    parser.add_argument(
        "--lean-ok",
        action="store_true",
        help="Mark Lean build as successful (set by runner on green build)",
    )
    parser.add_argument(
        "--authority-path",
        default=None,
        help="Override authority fsot_compute.py path recorded in certificate",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CERT_PATH,
        help="Output JSON path (default: data/certificate.json)",
    )
    args = parser.parse_args()

    cert = build_certificate(lean_build_ok=args.lean_ok, authority_path=args.authority_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  proved_claims: {len(cert['proved_claims'])}")
    print(f"  sorry_count_formal: {cert['sorry_count_formal']}")
    print(f"  lean_build_ok: {cert['lean_build_ok']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())