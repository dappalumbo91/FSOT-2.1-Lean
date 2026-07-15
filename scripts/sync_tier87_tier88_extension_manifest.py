#!/usr/bin/env python3
"""Register Tier 87/88 panels in extension_domains_manifest.yaml from tier manifests + benchmarks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required") from None

from tier87_scientific_expansion_lib import BUILDERS as T87_BUILDERS, LEAN_MAP as T87_LEAN, output_path as t87_path  # noqa: E402
from tier88_application_wiring_lib import LEAN_MAP as T88_LEAN, output_path as t88_path  # noqa: E402

T87_NEW = {
    "Biology_Developmental_Structural_Depth_Panel": {
        "routes_to_core": "Biology",
        "formula_branch_override": "term3.chaos_factor",
        "delta_psi": 0.6,
        "note": "Developmental + structural biology literature anchors + genomics relay",
    },
    "Quantum_Mechanics_Entanglement_Depth_Panel": {
        "routes_to_core": "Quantum_Mechanics",
        "formula_branch_override": "term2.amplitude",
        "delta_psi": 0.55,
        "note": "Entanglement, decoherence, and measurement subfield depth anchors",
    },
    "Psychology_Psychometrics_Depth_Panel": {
        "routes_to_core": "Psychology",
        "formula_branch_override": "term1.quirkMod",
        "delta_psi": 0.65,
        "note": "Psychometrics, RCT, and cognition literature anchors",
    },
    "Materials_Creep_Fracture_Depth_Panel": {
        "routes_to_core": "Materials_Science",
        "formula_branch_override": "term2.amplitude",
        "delta_psi": 0.5,
        "note": "Creep + fracture mechanics anchors + Materials Project relay",
    },
}

T88_NEW = {
    "Omni_Theory_Humanities_Panel": {
        "desktop_theme": "omni_theory_humanities",
        "formula_branch_override": "term1.quirkMod",
        "delta_psi": 0.7,
        "note": "Desktop omni-theory genesis per-verse scalar decoder live panel",
    },
    "Intrinsic_LLM_Validators_Panel": {
        "desktop_theme": "validators_intrinsic_llm",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.68,
        "note": "Desktop multi-language intrinsic LLM validator benchmarks",
    },
    "Bibliography_Corpus_Panel": {
        "desktop_theme": "bibliography",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.55,
        "note": "Desktop bibliography axiomatic constants corpus",
    },
    "Binary_Decoder_Panel": {
        "desktop_theme": "binary_decoder",
        "formula_branch_override": "term1.quirkMod",
        "delta_psi": 0.62,
        "note": "Desktop Rendlesham page-14 binary trace decoder",
    },
    "Physarum_Biological_CUDA_Panel": {
        "desktop_theme": "biological_cuda",
        "formula_branch_override": "term3.chaos_factor",
        "delta_psi": 0.72,
        "note": "Desktop Physarum polycephalum CUDA genomics simulation",
    },
    "Arxiv_Brain_Knowledge_Panel": {
        "desktop_theme": "arxiv_brain",
        "formula_branch_override": "term3.chaos_factor",
        "delta_psi": 0.75,
        "note": "Desktop ArXiv integrated knowledge brain portable summary",
    },
    "Scalar_Solver_35_Panel": {
        "desktop_theme": "scalar_solver",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.7,
        "note": "Desktop FSOT 3.5 dual scalar solver catalog metrics",
    },
    "Arxiv_Primitives_Panel": {
        "desktop_theme": "arxiv_primitives",
        "formula_branch_override": "term1.quirkMod",
        "delta_psi": 0.74,
        "note": "Desktop V14 arXiv cognitive primitives loop summary",
    },
    "Rust_Lean_Bridge_Panel": {
        "desktop_theme": "rust_lean_bridge",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.66,
        "note": "Desktop Rust bare-metal observer kernel → Lean bridge POC",
    },
    "Canonical_Oracle_Panel": {
        "desktop_theme": "canonical_oracle",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.8,
        "note": "Desktop fsot_compute.py canonical oracle authority metrics",
    },
    "VL_Agent_Distill_Panel": {
        "desktop_theme": "vl_agent",
        "formula_branch_override": "term1.quirkMod",
        "delta_psi": 0.71,
        "note": "Desktop vision-language agent distillation atlas",
    },
    "Early_Lean_MC_Panel": {
        "desktop_theme": "early_lean_mc",
        "formula_branch_override": "term1.term1_base",
        "delta_psi": 0.58,
        "note": "Desktop FSOTLean Monte Carlo stability portable summary",
    },
}

T88_VERIFIED_DESKTOP = {
    "Machine_And_Molecule_Live_Panel": {
        "desktop_theme": "species_catalog",
        "routes_to_core": "Materials_Science",
        "formula_branch_override": "term2.amplitude",
        "delta_psi": 0.72,
        "note": "Desktop FSOT_Machine_And_Molecule species catalog live verification",
    },
    "Fuel_Lab_Live_Panel": {
        "desktop_theme": "thermodynamics_fuels",
        "routes_to_core": "Thermodynamics",
        "formula_branch_override": "term3.chaos_factor",
        "delta_psi": 0.85,
        "note": "Desktop Fuel Lab engine simulator grounded fuel profiles",
    },
    "BlackHole_WhiteHole_Cycle_Live_Panel": {
        "desktop_theme": "blackhole_cycle",
        "routes_to_core": "Astrophysics",
        "formula_branch_override": "term3.chaos_factor",
        "delta_psi": 0.9,
        "note": "Desktop BH→WH information cycle prototype + warp portal relay",
    },
    "Star_Trek_Transporter_Live_Panel": {
        "desktop_theme": "quantum_transporter",
        "routes_to_core": "Quantum_Mechanics",
        "formula_branch_override": "term2.amplitude",
        "delta_psi": 0.88,
        "note": "Quantum teleportation anchors + Warp BH/WH portal crosswalk",
    },
}


def _bench_maps(domain: str, bench_path: Path) -> tuple[int, list[str]]:
    if not bench_path.exists():
        return 14, ["mathematical"]
    doc = json.loads(bench_path.read_text(encoding="utf-8"))
    d_eff = int(doc.get("D_eff") or 14)
    maps = list(doc.get("maps_to_lean") or ["mathematical"])
    return d_eff, maps


def _lean_module(lean_map: dict, domain: str) -> str:
    row = lean_map.get(domain)
    if not row:
        return f"FSOT.Formal.{domain.replace('_', '')}Priors"
    return f"FSOT.Formal.{row[3]}"


def main() -> int:
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ext = spec.setdefault("extension_domains", {})
    added: list[str] = []

    for domain, meta in T87_NEW.items():
        if domain in ext:
            continue
        bench = t87_path(domain)
        d_eff, maps = _bench_maps(domain, bench)
        ext[domain] = {
            "tier": 87,
            "D_eff": d_eff,
            "delta_psi": meta["delta_psi"],
            "recent_hits": 2,
            "observed": True,
            "maps_to_lean": maps,
            "formula_branch_override": meta["formula_branch_override"],
            "routes_to_core": meta["routes_to_core"],
            "ingest_script": "scripts/ingest_tier87_scientific_expansion.py",
            "build_script": "scripts/build_tier87_scientific_expansion_benchmarks.py",
            "manifest": "data/tier87_scientific_expansion_manifest.yaml",
            "benchmark_data": f"data/{bench.name}",
            "lean_module": _lean_module(T87_LEAN, domain),
            "note": meta["note"],
        }
        added.append(domain)

    for domain, meta in {**T88_NEW, **T88_VERIFIED_DESKTOP}.items():
        if domain in ext:
            continue
        bench = t88_path(domain)
        d_eff, maps = _bench_maps(domain, bench)
        row = {
            "tier": 88,
            "D_eff": d_eff,
            "delta_psi": meta["delta_psi"],
            "recent_hits": 2,
            "observed": True,
            "maps_to_lean": maps,
            "formula_branch_override": meta["formula_branch_override"],
            "desktop_theme": meta["desktop_theme"],
            "ingest_script": "scripts/ingest_tier88_application_wiring.py",
            "build_script": "scripts/build_tier88_application_wiring_benchmarks.py",
            "manifest": "data/tier88_application_wiring_manifest.yaml",
            "benchmark_data": f"data/{bench.name}",
            "lean_module": _lean_module(T88_LEAN, domain),
            "note": meta["note"],
        }
        if meta.get("routes_to_core"):
            row["routes_to_core"] = meta["routes_to_core"]
        ext[domain] = row
        added.append(domain)

    spec["updated"] = "2026-07-15"
    MANIFEST.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {MANIFEST}")
    print(f"  added {len(added)} panels: {added}")
    print(f"  total extension domains: {len(ext)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())