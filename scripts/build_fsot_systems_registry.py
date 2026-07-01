#!/usr/bin/env python3
"""Aggregate all verified FSOT systems into data/fsot_systems_registry.yaml."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
OUTPUT = ROOT / "data" / "fsot_systems_registry.yaml"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _lean_modules() -> list[dict]:
    modules = []
    for path in sorted(FORMAL.glob("*.lean")):
        text = path.read_text(encoding="utf-8", errors="replace")
        modules.append(
            {
                "module": f"FSOT.Formal.{path.stem}",
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "has_sorry": "sorry" in text and "no sorry" not in text.lower(),
                "theorem_count": text.count("theorem "),
            }
        )
    return modules


def _external_roots() -> list[dict]:
    return [
        {
            "id": "fsot_compute_authority",
            "path": r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py",
            "role": "canonical scalar oracle",
        },
        {
            "id": "allen_neuron_hybrid",
            "path": r"C:\Users\damia\Desktop\nuron\cell data",
            "role": "Allen hybrid neuron + hero FI certification",
        },
        {
            "id": "allen_cell_catalog",
            "path": r"C:\Users\damia\Desktop\nuron\cell data\allen_cell_types",
            "role": "2333-cell Allen Cell Types cohort",
        },
        {
            "id": "neurolab",
            "path": r"C:\Users\damia\Desktop\FSOT NeuroLab",
            "role": "brain pathways + component priors",
        },
        {
            "id": "smiles_lab",
            "path": r"C:\Users\damia\Desktop\FSOT SMILES Lab",
            "role": "1470 mapped physical/chemical constants",
        },
        {
            "id": "aether_prime",
            "path": r"D:\fsot llm expariments\Aether Prime",
            "role": "deterministic solver + verifier distill",
        },
        {
            "id": "magic_circle",
            "path": r"C:\Users\damia\Desktop\fsot magic circle",
            "role": "glyph resonance simulator",
        },
        {
            "id": "llm_experiments",
            "path": r"D:\fsot llm expariments",
            "role": "21 intelligence experiment folders",
        },
        {
            "id": "weather_lab",
            "path": r"C:\Users\damia\Desktop\weather",
            "role": "atmospheric FSOT priors",
        },
    ]


def build_registry() -> dict:
    registry = _load_json(ROOT / "data" / "lab_registry.json")
    cohort = _load_json(ROOT / "data" / "neuron_cohort_report.json")
    cert = _load_json(ROOT / "data" / "certificate.json")
    ledger_path = ROOT / "data" / "proof_ledger.yaml"
    ledger_entries = []
    if yaml and ledger_path.exists():
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
        ledger_entries = ledger.get("entries") or []

    syn = registry.get("experiment_synthesis", {})
    domain_cov = _load_json(ROOT / "data" / "domain_coverage_report.json")
    domain_prec = _load_json(ROOT / "data" / "domain_precision_report.json")
    proved_raw = cert.get("proved_claims") or cert.get("proved_claim_count")
    proved_claims = len(proved_raw) if isinstance(proved_raw, list) else proved_raw

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repo": str(ROOT),
            "remote": "https://github.com/dappalumbo91/FSOT-2.1-Lean.git",
            "lean_build_ok": cert.get("lean_build_ok"),
            "proved_claims": proved_claims,
            "sorry_count_formal": cert.get("sorry_count_formal", 0),
        },
        "canonical_oracle": {
            "script": "scripts/fsot_canonical_adapter.py",
            "constants_sha256": registry.get("canonical_constants_sha256"),
        },
        "verification_pipeline": [
            "scripts/run_neuron_cohort_eval.py",
            "scripts/ingest_experiment_synthesis.py",
            "scripts/gen_experiment_synthesis_lean.py",
            "scripts/run_domain_coverage_eval.py",
            "scripts/gen_domain_coverage_lean.py",
            "scripts/fetch_weather_observed_benchmark.py",
            "scripts/fetch_evolution_operon_benchmark.py",
            "scripts/run_domain_precision_eval.py",
            "scripts/gen_domain_precision_lean.py",
            "lake build FSOT",
            "scripts/verify_experiment_synthesis.py",
            "scripts/verify_domain_coverage.py",
            "scripts/verify_domain_precision.py",
            "scripts/fsot_verification_runner.py",
            "scripts/export_certificate.py",
            "scripts/build_fsot_systems_registry.py",
        ],
        "tier7_synthesis": {
            "neuron_hybrid": syn.get("neuron_hybrid_lab", {}),
            "neuron_cohort": registry.get("neuron_cohort_lab", {}),
            "aether_prime": syn.get("aether_prime_lab", {}),
            "magic_circle": syn.get("magic_circle_lab", {}),
            "llm_experiments": syn.get("llm_experiments_lab", {}),
        },
        "tier9_domain_coverage": {
            "domain_count": domain_cov.get("domain_count"),
            "domains_with_empirical_data": domain_cov.get("domains_with_empirical_data"),
            "total_empirical_records": domain_cov.get("total_empirical_records"),
            "lean_override_aligned": f"{domain_cov.get('lean_param_aligned_count')}/{domain_cov.get('lean_mapped_count')}",
            "negative_scalar_domains": domain_cov.get("negative_scalar_domains") or [],
            "registry_yaml": "data/fsot_35_domain_registry.yaml",
            "report_json": "data/domain_coverage_report.json",
            "lean_module": "FSOT.Formal.DomainCoveragePriors",
        },
        "tier10_domain_precision": {
            "numeric_precision_domains": domain_prec.get("domains_with_numeric_precision"),
            "target_band_2pct": domain_prec.get("domains_target_band_2pct"),
            "tolerable_band_5pct": domain_prec.get("domains_tolerable_band_5pct"),
            "huge_gap_domains": domain_prec.get("huge_gap_domains") or [],
            "sign_mismatch_domains": domain_prec.get("sign_mismatch_domains") or [],
            "report_json": "data/domain_precision_report.json",
            "lean_module": "FSOT.Formal.DomainPrecisionPriors",
        },
        "canonical_scalar_bridge": cohort.get("canonical_scalar_bridge", {}),
        "neurolab_smiles_bridge": cohort.get("neurolab_smiles_bridge", {}),
        "labs_in_registry": {
            k: {"present": bool(v)} if isinstance(v, dict) else {"present": bool(v)}
            for k, v in registry.items()
            if k not in ("registry_version", "generated_at", "canonical_constants_sha256")
        },
        "external_roots": _external_roots(),
        "lean_formal_modules": _lean_modules(),
        "proof_ledger": {
            "path": "data/proof_ledger.yaml",
            "entry_count": len(ledger_entries),
            "proved_count": sum(1 for e in ledger_entries if e.get("status") == "proved"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT systems registry")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if yaml is None:
        raise RuntimeError("PyYAML required")
    doc = build_registry()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  lean modules: {len(doc['lean_formal_modules'])}")
    print(f"  proved claims: {doc['meta'].get('proved_claims')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())