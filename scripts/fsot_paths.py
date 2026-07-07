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