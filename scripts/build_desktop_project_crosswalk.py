#!/usr/bin/env python3
"""Map Desktop FSOT project folders → Lean lab wiring → scientific themes."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path(r"C:\Users\damia\Desktop")
OUTPUT_JSON = ROOT / "data" / "desktop_project_crosswalk.json"
OUTPUT_YAML = ROOT / "data" / "desktop_project_crosswalk.yaml"

# User-supplied Desktop roots (2026-07-01 audit)
DESKTOP_FOLDERS: list[dict] = [
    {"name": "FSOT, Cube Block Trinary Design", "theme": "trinary_hardware", "lean_lab": None},
    {"name": "New folder", "theme": "thesis_simulation", "lean_lab": None},
    {"name": "Fluid spacetime omni-theory, FSOT, and the Holy Bible", "theme": "omni_theory_humanities", "lean_lab": None},
    {"name": "New folder (2)", "theme": "validators_intrinsic_llm", "lean_lab": None},
    {"name": "Kronos", "theme": "spacetime_precision", "lean_lab": "kronos_lab"},
    {"name": "llm modles", "theme": "model_weights", "lean_lab": None},
    {"name": "VibraFSOT", "theme": "vibration_register", "lean_lab": "vibra_register"},
    {"name": "Math generator", "theme": "math_generator", "lean_lab": "math_generator_lab"},
    {"name": "FSOTLean", "theme": "early_lean_mc", "lean_lab": None},
    {"name": "New folder (6)", "theme": "bibliography", "lean_lab": None},
    {"name": "Fsot trinary", "theme": "trinary_os", "lean_lab": "trinary_os"},
    {"name": "FSOT linguistics", "theme": "linguistics", "lean_lab": "linguistics_lab"},
    {"name": "Dictionary", "theme": "tokenization", "lean_lab": None},
    {"name": "fsot QWEN 3VL_Formal_Env", "theme": "certified_agent", "lean_lab": None},
    {"name": "New folder (4)", "theme": "fsot_20_code_vl_distill", "lean_lab": "lean_proofs_bridge"},
    {"name": "FSOT NeuroLab", "theme": "neurolab_35_domains", "lean_lab": "neurolab"},
    {"name": "Genetics", "theme": "protein_codon", "lean_lab": "protein_formulas"},
    {"name": "FSOT_Trinary_Codon_Project", "theme": "codon_trinary", "lean_lab": "codon_trinary_map"},
    {"name": "fsot_evolution_", "theme": "evolution", "lean_lab": "evolution_lab"},
    {"name": "fsot qwen 3vl", "theme": "vl_agent", "lean_lab": None},
    {"name": "gemma-4-", "theme": "model_weights", "lean_lab": None},
    {"name": "FSOT SMILES Lab", "theme": "physical_constants", "lean_lab": "smiles_lab"},
    {"name": "fsot_rendlesham_page_decoder ailen code", "theme": "binary_decoder", "lean_lab": None},
    {"name": "FSOT Cosmology Lab", "theme": "cosmology", "lean_lab": "cosmology_lambda_cdm"},
    {"name": "fsot code language", "theme": "formula_corpus", "lean_lab": "formula_corpus"},
    {"name": "Physarum polycephalum,", "theme": "biological_cuda", "lean_lab": None},
    {"name": "Law global research, non-FSOT", "theme": "non_fsot", "lean_lab": None},
    {"name": "FSOT_Trinary_Fluid_Computer_v2 (1)", "theme": "fluid_computer", "lean_lab": "trinary_fluid_computer"},
    {"name": "Fsot3.0 code", "theme": "fsot_30_aggregate", "lean_lab": "formula_corpus"},
    {"name": "Brain", "theme": "arxiv_brain", "lean_lab": None},
    {"name": "FSOT_3_5", "theme": "scalar_solver", "lean_lab": None},
    {"name": "loop", "theme": "arxiv_primitives", "lean_lab": None},
    {"name": "fsot flow chart", "theme": "documentation", "lean_lab": None},
    {"name": "autonomous_monte_carlo_fsot_refiner", "theme": "emergent_domains_mc", "lean_lab": None},
    {"name": "New folder (8)", "theme": "lean_duplicate", "lean_lab": None},
    {"name": "fsot llm expariments", "theme": "llm_experiments", "lean_lab": "experiment_synthesis"},
    {"name": "nuron", "theme": "neuron_allen", "lean_lab": "neuron_cohort_lab"},
    {"name": "weather", "theme": "atmospheric", "lean_lab": "weather_lab"},
    {"name": "fsot magic circle", "theme": "glyph_resonance", "lean_lab": "experiment_synthesis"},
    {"name": "FSOT-2.1-Lean", "theme": "formal_verification_hub", "lean_lab": None},
    {"name": "New folder (7)", "theme": "rust_lean_bridge", "lean_lab": None},
    {"name": "nuron lean", "theme": "empty", "lean_lab": None},
    {"name": "FSOT-2.1-Lean-main", "theme": "formal_verification_hub", "lean_lab": None},
    {"name": "FSOT Photonic V2 Experiments", "theme": "photonics", "lean_lab": "photonic_forge"},
    {"name": "FSOT document update", "theme": "canonical_oracle", "lean_lab": None},
    {"name": "FSOT_Machine_And_Molecule", "theme": "species_catalog", "lean_lab": "species_catalog"},
    {"name": "Fuel Lab", "theme": "thermodynamics_fuels", "lean_lab": "fuel_lab"},
    {"name": "FSOT_BlackHole_WhiteHole", "theme": "blackhole_cycle", "lean_lab": "blackhole_thesis"},
    {"name": "FSOT, Star Trek Transporter", "theme": "empty", "lean_lab": None},
    {"name": "FSOT Photonic Forge", "theme": "photonics", "lean_lab": "photonic_forge"},
    {"name": "fsot_magnetic_string_sim", "theme": "magnetic_strings", "lean_lab": "magnetic_strings"},
    {"name": "New folder (5)", "theme": "empty", "lean_lab": None},
    {"name": "New folder (3)", "theme": "formula_corpus_cnc", "lean_lab": "formula_corpus"},
]

THEME_LABELS = {
    "trinary_hardware": "Trinary hardware / ESP32 cube",
    "thesis_simulation": "Core thesis simulation (fsot_simulation.py)",
    "omni_theory_humanities": "Omni-theory / religious decoder",
    "validators_intrinsic_llm": "Multi-language validators + intrinsic LLM",
    "spacetime_precision": "Kronos spacetime ticker",
    "model_weights": "LLM weight assets",
    "vibration_register": "Vibra register MC",
    "math_generator": "Math generator rule corpora",
    "early_lean_mc": "Early Lean + Monte Carlo",
    "bibliography": "Bibliography archive",
    "trinary_os": "Trinary OS oracles",
    "linguistics": "Linguistic observables",
    "tokenization": "FSOT numeric tokenization",
    "certified_agent": "Qwen formal certified agent",
    "fsot_20_code_vl_distill": "FSOT 2.0 + VL distillation",
    "neurolab_35_domains": "NeuroLab 35-domain table (ONE slice)",
    "protein_codon": "Protein / genetics",
    "codon_trinary": "64-codon trinary map",
    "evolution": "Mitochondrial evolution",
    "vl_agent": "Vision-language agent",
    "physical_constants": "SMILES physical constants",
    "binary_decoder": "Rendlesham binary decoder",
    "cosmology": "Cosmology ΛCDM + wave4",
    "formula_corpus": "Strict empirical formula corpus",
    "biological_cuda": "Physarum CUDA biology",
    "non_fsot": "Non-FSOT research",
    "fluid_computer": "Trinary fluid computer",
    "fsot_30_aggregate": "FSOT 3.0 code aggregate",
    "arxiv_brain": "ArXiv integrated brain",
    "scalar_solver": "FSOT 3.5 dual solver",
    "arxiv_primitives": "V14 arXiv cognitive primitives",
    "documentation": "Architecture docs",
    "emergent_domains_mc": "MC emergent domain discovery",
    "lean_duplicate": "Lean workspace duplicate",
    "llm_experiments": "21 LLM experiment folders (D: drive)",
    "neuron_allen": "Allen neuron hybrid",
    "atmospheric": "Weather / atmospheric",
    "glyph_resonance": "Magic circle glyph sim",
    "formal_verification_hub": "Lean verification hub",
    "rust_lean_bridge": "Rust→Lean bridge",
    "empty": "Empty / stub",
    "photonics": "Photonic forge experiments",
    "canonical_oracle": "fsot_compute.py authority",
    "species_catalog": "Machine & molecule catalog",
    "thermodynamics_fuels": "Fuel lab",
    "blackhole_cycle": "Black hole / white hole thesis",
    "magnetic_strings": "Magnetic string coherence",
    "formula_corpus_cnc": "Formula corpus + CNC controller",
}


def _safe_count(path: Path, pattern: str, limit: int = 5000) -> int:
    n = 0
    try:
        for p in path.rglob(pattern):
            if p.is_file():
                n += 1
                if n >= limit:
                    break
    except OSError:
        pass
    return n


def _scan_folder(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "item_count": 0, "has_py": False, "has_json": False, "has_lean": False}
    try:
        items = list(path.iterdir()) if path.is_dir() else []
    except OSError:
        items = []
    py = _safe_count(path, "*.py")
    js = _safe_count(path, "*.json")
    lean = _safe_count(path, "*.lean")
    return {
        "exists": True,
        "item_count": len(items),
        "python_files": py,
        "json_files": js,
        "lean_files": lean,
        "empty": len(items) == 0,
    }


def build_crosswalk() -> dict:
    registry = {}
    lab_path = ROOT / "data" / "lab_registry.json"
    if lab_path.exists():
        registry = json.loads(lab_path.read_text(encoding="utf-8"))

    projects = []
    wired = 0
    unwired = 0
    by_theme: dict[str, list] = {}

    for entry in DESKTOP_FOLDERS:
        path = DESKTOP / entry["name"]
        scan = _scan_folder(path)
        theme = entry["theme"]
        lean_lab = entry.get("lean_lab")
        is_wired = bool(lean_lab and registry.get(lean_lab, {}).get("present", lean_lab in registry))
        if entry["theme"] in ("empty", "non_fsot", "formal_verification_hub", "lean_duplicate"):
            wire_status = "hub_or_skip"
        elif is_wired:
            wire_status = "wired"
            wired += 1
        elif scan.get("exists") and not scan.get("empty"):
            wire_status = "unwired"
            unwired += 1
        else:
            wire_status = "missing_or_empty"

        row = {
            "folder": entry["name"],
            "path": str(path),
            "theme": theme,
            "theme_label": THEME_LABELS.get(theme, theme),
            "lean_lab": lean_lab,
            "wire_status": wire_status,
            **scan,
        }
        projects.append(row)
        by_theme.setdefault(theme, []).append(entry["name"])

    mc_path = DESKTOP / "autonomous_monte_carlo_fsot_refiner" / "fsot_autonomous_run_summary.json"
    mc_domains = 0
    if mc_path.exists():
        mc_domains = int(json.loads(mc_path.read_text(encoding="utf-8")).get("emergent_domains_discovered") or 0)

    mg_rules = len(list((DESKTOP / "Math generator").glob("*_RULES.json"))) if (DESKTOP / "Math generator").exists() else 0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "desktop_folders_listed": len(DESKTOP_FOLDERS),
            "projects_existing": sum(1 for p in projects if p.get("exists")),
            "wired_to_lean": wired,
            "unwired_with_content": unwired,
            "neurolab_domain_slots": 35,
            "extension_domain_slots": 4,
            "math_generator_rule_corpora": mg_rules,
            "mc_emergent_domains": mc_domains,
            "estimated_theory_ceiling_domains": 35 + 4 + mc_domains + mg_rules,
            "note": "NeuroLab 35 is ONE indexing table; Desktop portfolio is the true coverage surface.",
        },
        "layer_model": {
            "L1_desktop_projects": "~48 active folders across ~20 scientific themes",
            "L2_lab_registry": "30 lab keys in lab_registry.json",
            "L3_neurolab_table": "35 domain slots (physics/chemistry/biology taxonomy)",
            "L4_lean_formal": "47 Formal modules, 65 proved claims",
            "L5_emergent_mc": f"{mc_domains} auto-discovered domain parameterizations",
            "L6_math_rules": f"{mg_rules} math-generator rule corpora (not in NeuroLab table)",
        },
        "projects": projects,
        "by_theme": {k: v for k, v in sorted(by_theme.items())},
        "priority_unwired": [
            "New folder (thesis_simulation)",
            "autonomous_monte_carlo_fsot_refiner (emergent_domains_mc)",
            "New folder (2) (validators_intrinsic_llm)",
            "Math generator depth (math_generator_lab exists but 50+ rule corpora under-counted)",
            "FSOT, Cube Block Trinary Design (trinary_hardware)",
            "Physarum polycephalum (biological_cuda)",
            "loop (arxiv_primitives)",
            "fsot QWEN 3VL_Formal_Env (certified_agent)",
            "Dictionary (tokenization)",
            "New folder (3) (formula_corpus_cnc)",
            "fsot_rendlesham_page_decoder (binary_decoder)",
            "Fluid spacetime omni-theory (omni_theory_humanities)",
        ],
    }


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-yaml", type=Path, default=OUTPUT_YAML)
    args = parser.parse_args()
    doc = build_crosswalk()
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    args.output_yaml.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {args.output_json}")
    print(f"  wired: {s['wired_to_lean']}  unwired: {s['unwired_with_content']}")
    print(f"  theory ceiling estimate: {s['estimated_theory_ceiling_domains']} domain surfaces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())