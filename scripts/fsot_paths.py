#!/usr/bin/env python3
"""Repository-relative path resolution for portable FSOT verification."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = REPO_ROOT / "vendor"
DATA_ROOT = REPO_ROOT / "data"

# Author-only desktop fallbacks (optional when developing on the original machine).
_DESKTOP = Path.home() / "Desktop"
_DESKTOP_COMPUTE = _DESKTOP / "FSOT document update" / "fsot_compute.py"
_DESKTOP_SMILES = _DESKTOP / "FSOT SMILES Lab" / "FSOT_SMILES_Lab_Dataset.json"
_DESKTOP_EVOLUTION_OPERONS = (
    _DESKTOP
    / "fsot_evolution_"
    / "files-b7d9d6b8"
    / "fsot_evolution_sim"
    / "results"
    / "biological_mt_operons.json"
)
_DESKTOP_NEURON_COHORT = _DESKTOP / "nuron" / "cell data" / "allen_cell_types"
_DESKTOP_NEUROLAB = _DESKTOP / "FSOT NeuroLab"
_DESKTOP_SMILES_LAB = _DESKTOP / "FSOT SMILES Lab"


def _truthy_env(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def portable_mode() -> bool:
    """True when verification should not depend on author desktop layout."""
    return _truthy_env("FSOT_PORTABLE")


def _resolve(env_var: str, *candidates: Path) -> Path | None:
    override = os.environ.get(env_var, "").strip()
    if override:
        path = Path(override).expanduser()
        if path.exists():
            return path.resolve()
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def fsot_compute_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_COMPUTE_PATH",
        VENDOR_ROOT / "fsot_compute.py",
        REPO_ROOT / "_research" / "FSOT-2.0-code" / "fsot-2.0" / "fsot_2_0.py",
        _DESKTOP_COMPUTE,
        _DESKTOP / "FSOT Cosmology Lab" / "fsot_compute.py",
    )
    if path is None and require:
        raise FileNotFoundError(
            "fsot_compute.py not found. Bundle missing or set FSOT_COMPUTE_PATH."
        )
    assert path is not None
    return path


def fsot_compute_candidates() -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for candidate in (
        VENDOR_ROOT / "fsot_compute.py",
        REPO_ROOT / "_research" / "FSOT-2.0-code" / "fsot-2.0" / "fsot_2_0.py",
        _DESKTOP_COMPUTE,
        _DESKTOP / "FSOT Cosmology Lab" / "fsot_compute.py",
        _DESKTOP / "Fsot3.0 code" / "fsot_compute.py",
    ):
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            out.append(candidate.resolve())
    return out


def smiles_dataset_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_SMILES_DATASET",
        VENDOR_ROOT / "smiles" / "FSOT_SMILES_Lab_Dataset.json",
        _DESKTOP_SMILES,
    )
    if path is None and require:
        raise FileNotFoundError(
            "FSOT_SMILES_Lab_Dataset.json not found. Bundle missing or set FSOT_SMILES_DATASET."
        )
    assert path is not None
    return path


def smiles_lab_root(*, require: bool = False) -> Path | None:
    dataset = smiles_dataset_path(require=False)
    if dataset is not None:
        return dataset.parent
    path = _resolve("FSOT_SMILES_LAB_ROOT", _DESKTOP_SMILES_LAB)
    if path is None and require:
        raise FileNotFoundError("SMILES lab root not found.")
    return path


def evolution_operons_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_EVOLUTION_OPERONS",
        VENDOR_ROOT / "evolution" / "biological_mt_operons.json",
        _DESKTOP_EVOLUTION_OPERONS,
    )
    if path is None and require:
        raise FileNotFoundError(
            "biological_mt_operons.json not found. Bundle missing or set FSOT_EVOLUTION_OPERONS."
        )
    assert path is not None
    return path


def neuron_cohort_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_NEURON_COHORT_ROOT",
        DATA_ROOT / "vendor" / "neuron_cohort",
        _DESKTOP_NEURON_COHORT,
    )
    if path is None and require:
        raise FileNotFoundError(
            "Allen neuron cohort root not found. Set FSOT_NEURON_COHORT_ROOT or use --portable."
        )
    return path


def neurolab_root(*, require: bool = False) -> Path | None:
    path = _resolve("FSOT_NEUROLAB_ROOT", _DESKTOP_NEUROLAB)
    if path is None and require:
        raise FileNotFoundError("NeuroLab root not found. Set FSOT_NEUROLAB_ROOT or use --portable.")
    return path


def rel_repo_path(path: Path) -> str:
    """Stable repo-relative path string for manifests and certificates."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def linguistics_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_LINGUISTICS_ROOT",
        VENDOR_ROOT / "linguistics",
        _DESKTOP / "FSOT linguistics",
    )
    if path is None and require:
        raise FileNotFoundError("Linguistics root not found.")
    return path


def math_generator_rules_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_MATH_GENERATOR_RULES_ROOT",
        VENDOR_ROOT / "math_generator" / "rules",
        _DESKTOP / "Math generator",
    )
    if path is None and require:
        raise FileNotFoundError("Math generator rules root not found.")
    assert path is not None
    return path


def trinary_os_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_TRINARY_OS_ROOT",
        VENDOR_ROOT / "trinary_os",
        _DESKTOP / "Fsot trinary" / "fsot_os",
    )
    if path is None and require:
        raise FileNotFoundError("Trinary OS root not found.")
    assert path is not None
    return path


def igem_parts_registry_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_IGEM_PARTS_REGISTRY",
        VENDOR_ROOT / "igem" / "igem_parts_registry.json",
    )
    if path is None and require:
        raise FileNotFoundError("iGEM parts registry not found.")
    assert path is not None
    return path


def igem_fastas_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_IGEM_FASTAS_ROOT",
        VENDOR_ROOT / "igem" / "fastas",
    )
    if path is None and require:
        raise FileNotFoundError("iGEM FASTA cache not found.")
    assert path is not None
    return path


def airfoil_dataset_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_AIRFOIL_DATASET",
        VENDOR_ROOT / "math_generator" / "datasets" / "airfoil_self_noise.csv",
        _DESKTOP / "New folder" / "fsot-read-write" / "examples" / "airfoil_self_noise.csv",
    )
    if path is None and require:
        raise FileNotFoundError("airfoil_self_noise.csv not found.")
    assert path is not None
    return path


def tokenization_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_TOKENIZATION_ROOT",
        VENDOR_ROOT / "tokenization",
        _DESKTOP / "Dictionary" / "english_tokens",
    )
    if path is None and require:
        raise FileNotFoundError("Tokenization root not found.")
    assert path is not None
    return path


def trinary_hardware_motif_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_TRINARY_HARDWARE_MOTIF",
        VENDOR_ROOT / "trinary_hardware" / "motif_influence_profile_stable.json",
        _DESKTOP / "FSOT, Cube Block Trinary Design" / "motif_influence_profile_stable.json",
    )
    if path is None and require:
        raise FileNotFoundError("Trinary hardware motif profile not found.")
    assert path is not None
    return path


def intrinsic_llm_benchmark_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_INTRINSIC_LLM_BENCHMARK",
        VENDOR_ROOT / "intrinsic_llm" / "benchmark_results_final.json",
        _DESKTOP / "New folder (2)" / "benchmark_results_final.json",
    )
    if path is None and require:
        raise FileNotFoundError("Intrinsic LLM benchmark not found.")
    assert path is not None
    return path


def physarum_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PHYSARUM_ROOT",
        VENDOR_ROOT / "physarum",
        _DESKTOP / "Physarum polycephalum,",
    )
    if path is None and require:
        raise FileNotFoundError("Physarum root not found.")
    assert path is not None
    return path


def physarum_cuda_benchmark_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PHYSARUM_CUDA_BENCHMARK",
        VENDOR_ROOT / "physarum" / "genome_data" / "cuda_benchmark_results.json",
        _DESKTOP / "Physarum polycephalum," / "genome_data" / "cuda_benchmark_results.json",
    )
    if path is None and require:
        raise FileNotFoundError("Physarum CUDA benchmark not found.")
    assert path is not None
    return path


def physarum_genomics_refined_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PHYSARUM_GENOMICS_REFINED",
        VENDOR_ROOT / "physarum" / "genome_data" / "genomics_slime_mold_refined.json",
        _DESKTOP / "Physarum polycephalum," / "genome_data" / "genomics_slime_mold_refined.json",
    )
    if path is None and require:
        raise FileNotFoundError("Physarum genomics refined JSON not found.")
    assert path is not None
    return path


def physarum_codon_weights_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PHYSARUM_CODON_WEIGHTS",
        VENDOR_ROOT / "physarum" / "genome_data" / "physarum_codon_weights.json",
        _DESKTOP / "Physarum polycephalum," / "genome_data" / "physarum_codon_weights.json",
    )
    if path is None and require:
        raise FileNotFoundError("Physarum codon weights not found.")
    assert path is not None
    return path


def arxiv_primitives_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_ARXIV_PRIMITIVES_ROOT",
        VENDOR_ROOT / "arxiv_primitives",
        _DESKTOP / "loop",
    )
    if path is None and require:
        raise FileNotFoundError("arXiv primitives root not found.")
    assert path is not None
    return path


def arxiv_v14_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_ARXIV_V14_SUMMARY",
        VENDOR_ROOT / "arxiv_primitives" / "v14_run_summary.json",
        _DESKTOP / "loop" / "v14_run_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("arXiv V14 run summary not found.")
    assert path is not None
    return path


def formula_corpus_cnc_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_FORMULA_CORPUS_CNC_ROOT",
        VENDOR_ROOT / "formula_corpus_cnc",
        _DESKTOP / "New folder (3)",
    )
    if path is None and require:
        raise FileNotFoundError("Formula corpus CNC root not found.")
    assert path is not None
    return path


def formula_corpus_cnc_formula_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_FORMULA_CORPUS_CNC_SUMMARY",
        VENDOR_ROOT / "formula_corpus_cnc" / "compiled_formulas" / "formula_summary.json",
        _DESKTOP / "New folder (3)" / "compiled_formulas" / "formula_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Formula corpus CNC summary not found.")
    assert path is not None
    return path


def formula_corpus_cnc_validator_delta_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_FORMULA_CORPUS_CNC_VALIDATOR_DELTA",
        VENDOR_ROOT / "formula_corpus_cnc" / "compiled_formulas" / "validator_vs_corpus_delta.json",
        _DESKTOP / "New folder (3)" / "compiled_formulas" / "validator_vs_corpus_delta.json",
    )
    if path is None and require:
        raise FileNotFoundError("Formula corpus CNC validator delta not found.")
    assert path is not None
    return path


def formula_corpus_cnc_gauntlet_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_FORMULA_CORPUS_CNC_GAUNTLET",
        VENDOR_ROOT / "formula_corpus_cnc" / "real_world_gauntlet_report.json",
        _DESKTOP / "New folder (3)" / "real_world_gauntlet_report.json",
    )
    if path is None and require:
        raise FileNotFoundError("Formula corpus CNC gauntlet report not found.")
    assert path is not None
    return path


def binary_decoder_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_BINARY_DECODER_ROOT",
        VENDOR_ROOT / "binary_decoder",
        _DESKTOP / "fsot_rendlesham_page_decoder ailen code",
    )
    if path is None and require:
        raise FileNotFoundError("Binary decoder root not found.")
    assert path is not None
    return path


def binary_decoder_trace_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_BINARY_DECODER_TRACE",
        VENDOR_ROOT / "binary_decoder" / "rendlesham_page14_trace.json",
        _DESKTOP
        / "fsot_rendlesham_page_decoder ailen code"
        / "files-c593e77d"
        / "page14_test.json",
    )
    if path is None and require:
        raise FileNotFoundError("Rendlesham hidden state trace not found.")
    assert path is not None
    return path


def certified_agent_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_CERTIFIED_AGENT_ROOT",
        VENDOR_ROOT / "certified_agent",
        _DESKTOP / "fsot QWEN 3VL_Formal_Env",
    )
    if path is None and require:
        raise FileNotFoundError("Certified agent root not found.")
    assert path is not None
    return path


def certified_agent_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_CERTIFIED_AGENT_SUMMARY",
        VENDOR_ROOT / "certified_agent" / "certified_agent_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Certified agent summary not found.")
    assert path is not None
    return path


def certified_agent_workspace_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_CERTIFIED_AGENT_WORKSPACE",
        VENDOR_ROOT / "certified_agent" / "fsot_workspace.json",
        _DESKTOP / "fsot QWEN 3VL_Formal_Env" / "fsot_workspace.json",
    )
    if path is None and require:
        raise FileNotFoundError("Certified agent workspace not found.")
    assert path is not None
    return path


def omni_theory_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_OMNI_THEORY_ROOT",
        VENDOR_ROOT / "omni_theory",
        _DESKTOP / "Fluid spacetime omni-theory, FSOT, and the Holy Bible",
    )
    if path is None and require:
        raise FileNotFoundError("Omni-theory root not found.")
    assert path is not None
    return path


def formula_corpus_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_FORMULA_CORPUS_ROOT",
        VENDOR_ROOT / "formula_corpus",
        _DESKTOP
        / "fsot code language"
        / "audits"
        / "reports"
        / "FSOT_UNIFIED_DATABASE",
    )
    if path is None and require:
        raise FileNotFoundError("Formula corpus root not found.")
    assert path is not None
    return path


def strict_empirical_jsonl_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_STRICT_EMPIRICAL_JSONL",
        VENDOR_ROOT / "formula_corpus" / "by_domain" / "strict_empirical.jsonl",
        _DESKTOP
        / "fsot code language"
        / "audits"
        / "reports"
        / "FSOT_UNIFIED_DATABASE"
        / "by_domain"
        / "strict_empirical.jsonl",
    )
    if path is None and require:
        raise FileNotFoundError("strict_empirical.jsonl not found.")
    assert path is not None
    return path


def fsot_aggregate_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_AGGREGATE_ROOT",
        VENDOR_ROOT / "fsot_aggregate",
        _DESKTOP / "Fsot3.0 code" / "database",
    )
    if path is None and require:
        raise FileNotFoundError("FSOT aggregate root not found.")
    assert path is not None
    return path


def fsot_aggregate_unified_db_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_AGGREGATE_UNIFIED_DB",
        VENDOR_ROOT / "fsot_aggregate" / "FSOT_Mathematical_Database_Unified.json",
        _DESKTOP / "Fsot3.0 code" / "database" / "FSOT_Mathematical_Database_Unified.json",
    )
    if path is None and require:
        raise FileNotFoundError("FSOT aggregate unified DB not found.")
    assert path is not None
    return path


def prediction_rederivation_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PREDICTION_REDERIVATION_SUMMARY",
        VENDOR_ROOT / "fsot_aggregate" / "prediction_rederivation_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Prediction rederivation summary not found.")
    assert path is not None
    return path


def omni_theory_genesis_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_OMNI_THEORY_GENESIS_SUMMARY",
        VENDOR_ROOT / "omni_theory" / "analysis" / "genesis" / "genesis_per_verse_summary.json",
        _DESKTOP
        / "Fluid spacetime omni-theory, FSOT, and the Holy Bible"
        / "analysis"
        / "genesis"
        / "genesis_per_verse_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Omni-theory Genesis summary not found.")
    assert path is not None
    return path


def fsot_read_path(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_READ_PATH",
        _DESKTOP / "New folder" / "fsot-read-write" / "target" / "release" / "fsot-read.exe",
        _DESKTOP / "New folder" / "fsot-read-write" / "target" / "debug" / "fsot-read.exe",
    )
    if path is None and require:
        raise FileNotFoundError("fsot-read not found. Set FSOT_READ_PATH.")
    return path


def math_generator_benchmark_reports_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_MATH_GENERATOR_BENCHMARK_REPORTS",
        VENDOR_ROOT / "math_generator" / "benchmark_reports",
        _DESKTOP / "New folder" / "fsot-read-write",
    )
    if path is None and require:
        raise FileNotFoundError("Math generator benchmark reports not found.")
    assert path is not None
    return path


def trinary_os_isa_registry_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_TRINARY_OS_ISA_REGISTRY",
        VENDOR_ROOT / "trinary_os" / "isa" / "fsotb_opcode_registry.json",
        _DESKTOP / "Fsot trinary" / "fsot_os" / "kernel" / "docs",
    )
    if path is None and require:
        raise FileNotFoundError("Trinary OS ISA registry not found.")
    assert path is not None
    return path


def species_catalog_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_SPECIES_CATALOG",
        VENDOR_ROOT / "species" / "fsot_species_catalog.json",
        _DESKTOP / "FSOT_Machine_And_Molecule" / "fsot_species_catalog.json",
    )
    if path is None and require:
        raise FileNotFoundError("Species catalog not found.")
    assert path is not None
    return path


def math_generator_comparison_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_MATH_GENERATOR_COMPARISON",
        VENDOR_ROOT / "math_generator" / "generated_formula_comparison_report.json",
        _DESKTOP
        / "Math generator"
        / "Unified"
        / "ada_spark_formula_generator"
        / "generated_formula_comparison_report.json",
    )
    if path is None and require:
        raise FileNotFoundError("Math generator comparison report not found.")
    assert path is not None
    return path


def authority_path_for_export(path: Path) -> str:
    """Prefer repo-relative authority paths in generated artifacts."""
    rel = rel_repo_path(path)
    if rel.startswith("vendor/") or rel.startswith("data/"):
        return rel
    return rel_repo_path(path) if path.is_relative_to(REPO_ROOT) else str(path)