#!/usr/bin/env python3
"""Repository-relative path resolution for portable FSOT verification."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = REPO_ROOT / "vendor"
DATA_ROOT = REPO_ROOT / "data"
CANONICAL_HUB_MARKER = ".fsot-canonical-hub"
CANONICAL_LEAN_HUB_NAME = "02_FSOT-2.1-Lean-Full"
# Legacy default when this repo was always mounted as I: (fallback only).
CANONICAL_ARCHIVE_ROOT = Path(r"I:\FSOT-Physical-Archive")
CANONICAL_LEAN_HUB = CANONICAL_ARCHIVE_ROOT / CANONICAL_LEAN_HUB_NAME


def archive_root() -> Path | None:
    """Physical archive root (parent of Lean hub), any drive letter."""
    override = os.environ.get("FSOT_ARCHIVE_ROOT", "").strip()
    if override:
        path = Path(override).expanduser()
        if path.is_dir():
            return path.resolve()
    if (REPO_ROOT / CANONICAL_HUB_MARKER).is_file():
        return REPO_ROOT.parent.resolve()
    legacy_hub = CANONICAL_ARCHIVE_ROOT / CANONICAL_LEAN_HUB_NAME
    try:
        REPO_ROOT.resolve().relative_to(legacy_hub.resolve())
        return CANONICAL_ARCHIVE_ROOT.resolve()
    except ValueError:
        return None


def founding_archive_roots() -> list[Path]:
    """Founding PDF/markdown roots — prefer archive-bundled 06_Founding-Archives."""
    override = os.environ.get("FSOT_FOUNDING_ROOT", "").strip()
    if override:
        path = Path(override).expanduser()
        if path.is_dir():
            return [path.resolve()]
    candidates: list[Path] = []
    ar = archive_root()
    if ar is not None:
        candidates.extend(
            [
                ar / "06_Founding-Archives" / "fsuft_aasb",
                ar / "06_Founding-Archives" / "fsot_tech",
            ]
        )
    drive = REPO_ROOT.drive or "I:"
    candidates.extend(
        [
            Path(f"{drive}/fsuft aasb"),
            Path(f"{drive}/fsot tech"),
            Path(r"I:\fsuft aasb"),
            Path(r"I:\fsot tech"),
        ]
    )
    seen: set[str] = set()
    out: list[Path] = []
    for candidate in candidates:
        key = str(candidate).lower()
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_dir():
            out.append(candidate.resolve())
    return out

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


def canonical_archive_mode() -> bool:
    """True when running from the physical archive Lean hub (any drive letter)."""
    if _truthy_env("FSOT_CANONICAL_ARCHIVE"):
        return True
    if (REPO_ROOT / CANONICAL_HUB_MARKER).is_file():
        return True
    ar = archive_root()
    if ar is not None and (ar / CANONICAL_LEAN_HUB_NAME).resolve() == REPO_ROOT.resolve():
        return True
    try:
        REPO_ROOT.resolve().relative_to(CANONICAL_LEAN_HUB.resolve())
        return True
    except ValueError:
        return False


def archive_independent_mode() -> bool:
    """Canonical archive or explicit portable — never fall back to C: Desktop."""
    return portable_mode() or canonical_archive_mode()


def _is_legacy_desktop_path(path: Path) -> bool:
    lowered = str(path).replace("/", "\\").lower()
    if "c:\\users\\damia\\desktop" in lowered:
        return True
    parts = {p.lower() for p in path.parts}
    return "desktop" in parts and path.drive.lower() == "c:"


def _resolve(env_var: str, *candidates: Path) -> Path | None:
    override = os.environ.get(env_var, "").strip()
    if override:
        path = Path(override).expanduser()
        if path.exists():
            return path.resolve()
    for candidate in candidates:
        if archive_independent_mode() and _is_legacy_desktop_path(candidate):
            continue
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
        VENDOR_ROOT / "neuron_cohort",
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


def intelligence_compression_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_INTELLIGENCE_COMPRESSION_ROOT",
        VENDOR_ROOT / "intelligence_compression",
        _DESKTOP / "FSOT-2.0-code" / "IntelligenceCompressor",
    )
    if path is None and require:
        raise FileNotFoundError(
            "Intelligence compression root not found. Set FSOT_INTELLIGENCE_COMPRESSION_ROOT."
        )
    return path


def quantum_materials_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_QUANTUM_MATERIALS_ROOT",
        VENDOR_ROOT / "quantum_materials",
        smiles_lab_root(require=False),
    )
    if path is None and require:
        raise FileNotFoundError(
            "Quantum materials root not found. Set FSOT_QUANTUM_MATERIALS_ROOT."
        )
    return path


def neuroimmunology_root(*, require: bool = False) -> Path | None:
    path = _resolve("FSOT_NEUROIMMUNOLOGY_ROOT", VENDOR_ROOT / "neuroimmunology")
    if path is None and require:
        raise FileNotFoundError("Neuroimmunology root not found.")
    return path


def oncology_root(*, require: bool = False) -> Path | None:
    path = _resolve("FSOT_ONCOLOGY_ROOT", VENDOR_ROOT / "oncology")
    if path is None and require:
        raise FileNotFoundError("Oncology root not found.")
    return path


def planetary_atmospheres_root(*, require: bool = False) -> Path | None:
    path = _resolve("FSOT_PLANETARY_ATMOSPHERES_ROOT", VENDOR_ROOT / "planetary_atmospheres")
    if path is None and require:
        raise FileNotFoundError("Planetary atmospheres root not found.")
    return path


def materials_engineering_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_MATERIALS_ENGINEERING_ROOT",
        VENDOR_ROOT / "materials_engineering",
        smiles_lab_root(require=False),
    )
    if path is None and require:
        raise FileNotFoundError(
            "Materials engineering root not found. Set FSOT_MATERIALS_ENGINEERING_ROOT."
        )
    return path


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


def knowledge_base_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_KNOWLEDGE_BASE_ROOT",
        VENDOR_ROOT / "knowledge_base",
        _DESKTOP / "Knowledge base",
    )
    if path is None and require:
        raise FileNotFoundError("Knowledge base root not found. Set FSOT_KNOWLEDGE_BASE_ROOT.")
    return path


def knowledge_base_transfer_path(*, require: bool = False) -> Path | None:
    candidates: list[Path] = [
        _DESKTOP / "Knowledge base" / "transfer" / "FSOT_KNOWLEDGE_UNIFIED_TRANSFER.json",
        VENDOR_ROOT / "knowledge_base" / "transfer" / "FSOT_KNOWLEDGE_UNIFIED_TRANSFER.json",
    ]
    root = knowledge_base_root(require=False)
    if root is not None:
        candidates.insert(0, root / "transfer" / "FSOT_KNOWLEDGE_UNIFIED_TRANSFER.json")
    path = _resolve("FSOT_KNOWLEDGE_BASE_TRANSFER", *candidates)
    if path is None and require:
        raise FileNotFoundError("Knowledge base transfer JSON not found.")
    return path


def knowledge_base_validation_path(*, require: bool = False) -> Path | None:
    candidates: list[Path] = [
        _DESKTOP / "Knowledge base" / "export" / "full_corpus_math_validation.json",
        VENDOR_ROOT / "knowledge_base" / "export" / "full_corpus_math_validation.json",
    ]
    root = knowledge_base_root(require=False)
    if root is not None:
        candidates.insert(0, root / "export" / "full_corpus_math_validation.json")
        candidates.insert(1, root / "full_corpus_math_validation.json")
    path = _resolve("FSOT_KNOWLEDGE_BASE_VALIDATION", *candidates)
    if path is None and require:
        raise FileNotFoundError("Knowledge base validation JSON not found.")
    return path


def unified_db_path(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_UNIFIED_DB",
        VENDOR_ROOT / "fsot_aggregate" / "FSOT_UNIFIED.db",
        _DESKTOP
        / "fsot code language"
        / "audits"
        / "reports"
        / "FSOT_UNIFIED_DATABASE"
        / "FSOT_UNIFIED.db",
    )
    if path is None and require:
        raise FileNotFoundError("FSOT_UNIFIED.db not found. Set FSOT_UNIFIED_DB.")
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


def vl_distill_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_VL_DISTILL_ROOT",
        VENDOR_ROOT / "vl_distill",
        _DESKTOP / "New folder (4)" / "data",
    )
    if path is None and require:
        raise FileNotFoundError("VL distill root not found.")
    assert path is not None
    return path


def vl_distill_atlas_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_VL_DISTILL_ATLAS_SUMMARY",
        VENDOR_ROOT / "vl_distill" / "fsot_atlas_summary.json",
        _DESKTOP / "New folder (4)" / "data" / "fsot_atlas_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("VL distill atlas summary not found.")
    assert path is not None
    return path


def vl_distill_domain_registry_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_VL_DISTILL_DOMAIN_REGISTRY",
        VENDOR_ROOT / "vl_distill" / "fsot_domain_registry.json",
        _DESKTOP / "New folder (4)" / "data" / "fsot_domain_registry.json",
    )
    if path is None and require:
        raise FileNotFoundError("VL distill domain registry not found.")
    assert path is not None
    return path


def vl_distill_dataset_meta_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_VL_DISTILL_DATASET_META",
        VENDOR_ROOT / "vl_distill" / "distill_dataset.meta.json",
        _DESKTOP / "New folder (4)" / "data" / "distill_dataset.meta.json",
    )
    if path is None and require:
        raise FileNotFoundError("VL distill dataset meta not found.")
    assert path is not None
    return path


def vl_distill_competitive_report_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_VL_DISTILL_COMPETITIVE_REPORT",
        VENDOR_ROOT / "vl_distill" / "fsot_competitive_report.json",
        _DESKTOP / "New folder (4)" / "data" / "fsot_competitive_report.json",
    )
    if path is None and require:
        raise FileNotFoundError("VL distill competitive report not found.")
    assert path is not None
    return path


def rust_lean_bridge_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_RUST_LEAN_BRIDGE_ROOT",
        VENDOR_ROOT / "rust_lean_bridge",
        _DESKTOP / "New folder (7)",
    )
    if path is None and require:
        raise FileNotFoundError("Rust Lean bridge root not found.")
    assert path is not None
    return path


def rust_lean_bridge_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_RUST_LEAN_BRIDGE_SUMMARY",
        VENDOR_ROOT / "rust_lean_bridge" / "rust_lean_bridge_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Rust Lean bridge summary not found.")
    assert path is not None
    return path


def bibliography_corpus_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_BIBLIOGRAPHY_CORPUS_ROOT",
        VENDOR_ROOT / "bibliography_corpus",
        _DESKTOP / "New folder (6)",
    )
    if path is None and require:
        raise FileNotFoundError("Bibliography corpus root not found.")
    assert path is not None
    return path


def external_data_root(*, require: bool = False) -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() if raw else Path(r"G:\FSOT-PublicData")
    if require and not root.exists():
        raise FileNotFoundError(
            f"External data root not found: {root}. Set FSOT_EXTERNAL_DATA_ROOT."
        )
    return root


def public_data_vendor_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_PUBLIC_DATA_VENDOR_ROOT",
        VENDOR_ROOT / "public_data",
    )
    if path is None and require:
        raise FileNotFoundError("Public data vendor root not found.")
    assert path is not None
    return path


def bibliography_summary_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_BIBLIOGRAPHY_SUMMARY",
        VENDOR_ROOT / "bibliography_corpus" / "bibliography_summary.json",
    )
    if path is None and require:
        raise FileNotFoundError("Bibliography summary not found.")
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


def the_well_cache_root(*, require: bool = False) -> Path | None:
    path = _resolve(
        "FSOT_THE_WELL_CACHE",
        Path(os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "G:/FSOT-PublicData")).expanduser() / "the_well",
        VENDOR_ROOT / "the_well",
    )
    if path is None and require:
        raise FileNotFoundError("The Well cache root not found. Set FSOT_EXTERNAL_DATA_ROOT.")
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


def manifest_path(raw: str | Path) -> Path:
    """Resolve manifest path strings (repo-relative or absolute)."""
    p = Path(raw)
    if p.is_absolute():
        return p.resolve()
    return (REPO_ROOT / p).resolve()


def thesis_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_THESIS_ROOT",
        VENDOR_ROOT / "thesis",
        _DESKTOP / "New folder",
    )
    if path is None and require:
        raise FileNotFoundError("Thesis wave root not found. Bundle vendor/thesis or set FSOT_THESIS_ROOT.")
    assert path is not None
    return path


def cosmology_skeleton_database_path(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_COSMOLOGY_SKELETON_DB",
        VENDOR_ROOT / "cosmology" / "database" / "FSOT_Mathematical_Database_Unified.json",
        VENDOR_ROOT / "fsot_aggregate" / "FSOT_Mathematical_Database_Unified.json",
        _DESKTOP / "FSOT Cosmology Lab" / "database" / "FSOT_Mathematical_Database_Unified.json",
        _DESKTOP / "New folder" / "database" / "FSOT_Mathematical_Database_Unified.json",
    )
    if path is None and require:
        raise FileNotFoundError("Cosmology skeleton database not found.")
    assert path is not None
    return path


def math_generator_root(*, require: bool = True) -> Path:
    path = _resolve(
        "FSOT_MATH_GENERATOR_ROOT",
        VENDOR_ROOT / "math_generator",
        _DESKTOP / "Math generator",
    )
    if path is None and require:
        raise FileNotFoundError("Math generator root not found.")
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


def observable_verification_pipeline_path(*, require: bool = False) -> Path | None:
    """Author-only numeric pipeline; optional for portable clone-and-verify."""
    candidates: list[Path] = [
        VENDOR_ROOT / "formula_corpus" / "fsot_observable_verification_pipeline.py",
    ]
    if not portable_mode():
        candidates.append(
            _DESKTOP / "fsot code language" / "audits" / "fsot_observable_verification_pipeline.py"
        )
    path = _resolve("FSOT_OBSERVABLE_PIPELINE_PATH", *candidates)
    if path is None and require:
        raise FileNotFoundError(
            "fsot_observable_verification_pipeline.py not found. Set FSOT_OBSERVABLE_PIPELINE_PATH."
        )
    return path


def lab_compute_sync_targets() -> list[Path]:
    """Optional lab mirrors for fsot_compute sync (author dev only)."""
    raw = os.environ.get("FSOT_LAB_COMPUTE_TARGETS", "").strip()
    if raw:
        return [Path(p.strip()).expanduser() for p in raw.split(os.pathsep) if p.strip()]
    targets: list[Path] = []
    for root in (smiles_lab_root(require=False), neurolab_root(require=False)):
        if root is None:
            continue
        candidate = root / "fsot_compute.py"
        if candidate.exists():
            targets.append(candidate)
    return targets


def isabelle_install_roots() -> list[Path]:
    """Discover Isabelle installations without hardcoded author paths."""
    home = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", "")))
    roots: list[Path] = [
        Path(r"C:\Isabelle"),
        Path(r"C:\Program Files\Isabelle"),
        home / "Isabelle",
    ]
    isa_home = os.environ.get("ISABELLE_HOME", "").strip()
    if isa_home:
        roots.insert(0, Path(isa_home).expanduser())
    for pattern in ("Isabelle*", "Isabelle202*"):
        for base in (home / "Desktop", Path(r"C:\Program Files")):
            if base.exists():
                roots.extend(sorted(base.glob(pattern), reverse=True))
    seen: set[str] = set()
    out: list[Path] = []
    for root in roots:
        key = str(root)
        if key in seen or not root.exists():
            continue
        seen.add(key)
        out.append(root)
    return out


def fstar_install_root(*, require: bool = False) -> Path | None:
    """Resolve F* install root from FSTAR_HOME or common install locations."""
    raw = os.environ.get("FSTAR_HOME", "").strip()
    if raw:
        root = Path(raw).expanduser()
        if root.exists():
            return root.resolve()
    home = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", "")))
    candidates: list[Path] = [
        Path(r"C:\Program Files\fstar"),
        Path(r"C:\fstar"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "fstar",
    ]
    tools = home / "tools"
    if tools.exists():
        candidates.extend(sorted(tools.glob("fstar*"), reverse=True))
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    if require:
        raise FileNotFoundError("F* install not found. Set FSTAR_HOME.")
    return None