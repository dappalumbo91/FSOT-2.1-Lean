"""Unified FSOT connective registry — reuse certified domain + ladder solutions.

Every gate is loaded from panels already at ~0.02% pooled median (fsot_compute,
adjacent_rung_coupling, evolution operons, longevity spine). Intrinsic prediction
must not re-derive these; it composes them as connective transport between rungs.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADJACENT_BENCH = ROOT / "data" / "adjacent_rung_coupling_benchmark.json"
EVOLUTION_BENCH = ROOT / "data" / "evolution_operon_benchmark.json"

PHI = (1.0 + math.sqrt(5.0)) / 2.0
ZEBRAFISH_GENOME_BP = 1.37e9

GENETIC_LADDER_MECHANISMS = (
    "nuclear_to_atomic_adjacent_fold",
    "atomic_to_molecular_adjacent_fold",
    "molecular_to_cellular_adjacent_fold",
    "cellular_to_organismic_adjacent_fold",
    "organismic_to_planetary_adjacent_fold",
)

ENVIRONMENT_LADDER_MECHANISMS = (
    "planetary_to_stellar_adjacent_fold",
    "stellar_to_galactic_adjacent_fold",
    "galactic_to_cosmological_adjacent_fold",
)

CERTIFIED_DOMAIN_NAMES = (
    "Biology",
    "Biochemistry",
    "Molecular_Chemistry",
    "Chemistry",
    "Neuroscience",
    "Ecology",
    "Nuclear_Physics",
    "Particle_Physics",
    "Thermodynamics",
    "Electromagnetism",
    "Astronomy",
    "Planetary_Science",
    "Cosmology",
)


@dataclass(frozen=True)
class ConnectiveRegistry:
    authority_path: str
    domain_scalars: dict[str, float]
    fold_steps: dict[str, float]
    genetic_log_fold: float
    environment_log_fold: float
    biology: float
    biochemistry_gate: float
    molecular_gate: float
    neural_gate: float
    ecology_gate: float
    nuclear_gate: float
    solar_gate: float
    em_gate: float
    stellar_gate: float
    galactic_gate: float
    evolution_operon_median_err_pct: float
    genome_log10: float


def _load_adjacent_folds() -> dict[str, float]:
    if not ADJACENT_BENCH.exists():
        return {}
    doc = json.loads(ADJACENT_BENCH.read_text(encoding="utf-8"))
    out: dict[str, float] = {}
    for row in doc.get("material_records") or []:
        if row.get("property") != "adjacent_fold_step":
            continue
        mech = str(row.get("mechanism") or "")
        if mech:
            out[mech] = float(row.get("computed") or 0.0)
    return out


def _evolution_median_err() -> float:
    if not EVOLUTION_BENCH.exists():
        return 0.0
    doc = json.loads(EVOLUTION_BENCH.read_text(encoding="utf-8"))
    return float(doc.get("median_error_pct") or 0.0)


def _domain_gate(scalars: dict[str, float], source: str, sink: str = "Biology") -> float:
    bio = max(abs(scalars.get(sink, 1.0)), 1e-9)
    return abs(scalars.get(source, 0.0)) / bio


def _log_fold(mechanisms: tuple[str, ...], folds: dict[str, float]) -> float:
    steps = [folds[m] for m in mechanisms if m in folds]
    if not steps:
        return 0.0
    return sum(math.log1p(step) for step in steps) / PHI


@lru_cache(maxsize=1)
def load_connective_registry() -> ConnectiveRegistry:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import canonical_domain_scalar, load_fsot_compute  # noqa: WPS433

    _, authority = load_fsot_compute()
    scalars: dict[str, float] = {}
    for name in CERTIFIED_DOMAIN_NAMES:
        try:
            scalars[name] = float(canonical_domain_scalar(name))
        except (KeyError, ValueError):
            continue

    folds = _load_adjacent_folds()
    biology = scalars.get("Biology", 0.44472501)

    return ConnectiveRegistry(
        authority_path=str(authority),
        domain_scalars=scalars,
        fold_steps=folds,
        genetic_log_fold=_log_fold(GENETIC_LADDER_MECHANISMS, folds),
        environment_log_fold=_log_fold(ENVIRONMENT_LADDER_MECHANISMS, folds),
        biology=biology,
        biochemistry_gate=_domain_gate(scalars, "Biochemistry"),
        molecular_gate=_domain_gate(scalars, "Molecular_Chemistry"),
        neural_gate=_domain_gate(scalars, "Neuroscience"),
        ecology_gate=_domain_gate(scalars, "Ecology"),
        nuclear_gate=_domain_gate(scalars, "Nuclear_Physics"),
        solar_gate=_domain_gate(scalars, "Thermodynamics"),
        em_gate=_domain_gate(scalars, "Electromagnetism"),
        stellar_gate=_domain_gate(scalars, "Astronomy"),
        galactic_gate=_domain_gate(scalars, "Planetary_Science", "Astronomy"),
        evolution_operon_median_err_pct=_evolution_median_err(),
        genome_log10=math.log10(ZEBRAFISH_GENOME_BP),
    )


def genetic_ladder_fold(t_norm: float, *, is_tail: bool) -> float:
    """Stage-selective adjacent-rung fold active at developmental position."""
    reg = load_connective_registry()
    folds = reg.fold_steps
    if t_norm < 0.68:
        return folds.get("molecular_to_cellular_adjacent_fold", 0.0)
    if is_tail:
        base = folds.get("cellular_to_organismic_adjacent_fold", 0.0)
        return base * (reg.neural_gate ** (1.0 / (PHI * 2.0)))
    if t_norm < 0.84:
        return folds.get("cellular_to_organismic_adjacent_fold", 0.0)
    return folds.get("organismic_to_planetary_adjacent_fold", 0.0)


def longevity_genome_pressure(
    *,
    metabolic_rate_w: float,
    maximum_longevity_yrs: float,
    longevity_quotient: float,
) -> float:
    """Tier 94/95 longevity spine — species structural prior (not measured outcomes)."""
    metabolic = max(metabolic_rate_w, 1e-6)
    max_life = max(maximum_longevity_yrs, 0.5)
    lq = max(longevity_quotient, 1e-6)
    reg = load_connective_registry()
    tempo = (metabolic / 0.35) ** (1.0 / PHI) * (5.5 / max_life) ** ((PHI - 1.0) / PHI)
    genome_term = reg.genome_log10 / (PHI * 9.0)
    return tempo * (1.0 + (PHI - 1.0) * genome_term) * (1.0 + math.log10(1.0 + lq) / (PHI * 6.0))


def connective_diagnostics(
    *,
    t_norm: float,
    is_tail: bool,
    metabolic_rate_w: float,
    maximum_longevity_yrs: float,
    longevity_quotient: float,
    habitat_extent: float = 1.0,
    division_rate: float = 0.5,
    photic: float = 0.0,
) -> dict[str, float]:
    reg = load_connective_registry()
    active_fold = genetic_ladder_fold(t_norm, is_tail=is_tail)
    return {
        "connective_authority": reg.authority_path,
        "connective_genetic_log_fold": reg.genetic_log_fold,
        "connective_environment_log_fold": reg.environment_log_fold,
        "connective_active_ladder_fold": active_fold,
        "connective_biochemistry_gate": reg.biochemistry_gate,
        "connective_molecular_gate": reg.molecular_gate,
        "connective_neural_gate": reg.neural_gate,
        "connective_ecology_gate": reg.ecology_gate,
        "connective_nuclear_gate": reg.nuclear_gate,
        "connective_solar_gate": reg.solar_gate,
        "connective_em_gate": reg.em_gate,
        "connective_stellar_gate": reg.stellar_gate,
        "connective_galactic_gate": reg.galactic_gate,
        "connective_evolution_operon_median_err_pct": reg.evolution_operon_median_err_pct,
        "connective_longevity_genome_pressure": longevity_genome_pressure(
            metabolic_rate_w=metabolic_rate_w,
            maximum_longevity_yrs=maximum_longevity_yrs,
            longevity_quotient=longevity_quotient,
        ),
        "connective_photic_observability_floor": connective_photic_observability_floor(
            t_norm, is_tail=is_tail
        ),
        "connective_displacement_transport": connective_displacement_transport(
            t_norm=t_norm,
            is_tail=is_tail,
            habitat_extent=habitat_extent,
            division_rate=division_rate,
            photic=photic,
        ),
        "connective_stability_transport": connective_stability_transport(
            t_norm=t_norm, is_tail=is_tail
        ),
        "connective_tail_lineage_transport": connective_tail_lineage_transport(
            t_norm=t_norm, is_tail=is_tail
        ),
    }


LATE_PLANETARY_T = 0.84
MID_STAGE_LO = 0.68
MID_STAGE_PEAK = 0.78


def _smoothstep(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    t = (x - lo) / (hi - lo)
    return t * t * (3.0 - 2.0 * t)


def connective_photic_observability_floor(t_norm: float, *, is_tail: bool) -> float:
    """EM×stellar certified floor when GPU intensity is below cellular-rung sensitivity.

    Applies only to late full-embryo planetary-rung transport — never SNR, never tail.
    """
    if is_tail or t_norm < LATE_PLANETARY_T:
        return 0.0
    reg = load_connective_registry()
    gate_pow = 1.0 / (PHI * 2.0)
    stack = (reg.em_gate * reg.stellar_gate) ** gate_pow
    return stack * ((PHI - 1.0) / PHI)


EARLY_STAGE_HI = 0.68


def connective_early_displacement_transport(
    *,
    t_norm: float,
    is_tail: bool,
    division_rate: float,
) -> float:
    """Molecular→cellular adjacent fold — early embryo motility (t < 0.68)."""
    if is_tail or t_norm >= EARLY_STAGE_HI:
        return 1.0
    reg = load_connective_registry()
    fold = reg.fold_steps.get("molecular_to_cellular_adjacent_fold", 0.0)
    early_gate = _smoothstep(t_norm, 0.45, EARLY_STAGE_HI)
    low_div = max(0.0, 0.36 - division_rate) * fold * reg.molecular_gate
    return 1.0 + early_gate * (fold * reg.molecular_gate + low_div) * ((PHI - 1.0) / (PHI * 1.80))


def connective_early_duration_transport(
    *,
    t_norm: float,
    is_tail: bool,
    det: float = 0.0,
    division_rate: float = 0.5,
) -> float:
    """Crowded early census shortens tracks when division contact inhibition applies."""
    if is_tail or t_norm >= EARLY_STAGE_HI:
        return 1.0
    reg = load_connective_registry()
    fold = reg.fold_steps.get("molecular_to_cellular_adjacent_fold", 0.0)
    early_gate = _smoothstep(t_norm, 0.45, EARLY_STAGE_HI)
    crowd_ref = 10.0 ** (3.0 - 1.0 / PHI)
    crowd_gate = _smoothstep(math.log10(max(det, 1.0) / crowd_ref), 1.0, 2.5)
    low_div_gate = _smoothstep(0.32 - division_rate, 0.0, 0.10)
    shorten = early_gate * crowd_gate * low_div_gate * fold * reg.molecular_gate
    return 1.0 / (1.0 + shorten * ((PHI - 1.0) / (PHI * 0.45)))


def connective_late_body_duration_transport(
    *,
    t_norm: float,
    is_tail: bool,
    division_rate: float,
) -> float:
    """Organismic→planetary + thermodynamic tempo — late full-embryo short tracks."""
    if is_tail or t_norm < LATE_PLANETARY_T:
        return 1.0
    reg = load_connective_registry()
    late_gate = _smoothstep(t_norm, LATE_PLANETARY_T, 1.0)
    fold = reg.fold_steps.get("organismic_to_planetary_adjacent_fold", 0.0)
    high_div = _smoothstep(division_rate, 0.45, 0.82)
    return 1.0 + late_gate * fold * reg.solar_gate * high_div * ((PHI - 1.0) / (PHI * 4.3))


def connective_displacement_transport(
    *,
    t_norm: float,
    is_tail: bool,
    habitat_extent: float,
    division_rate: float,
    photic: float = 0.0,
) -> float:
    """Certified motility transport — early, mid, and late planetary rungs."""
    if is_tail:
        return 1.0
    reg = load_connective_registry()
    gate_scale = (PHI - 1.0) / PHI

    if t_norm < EARLY_STAGE_HI:
        return connective_early_displacement_transport(
            t_norm=t_norm, is_tail=is_tail, division_rate=division_rate
        )

    if MID_STAGE_LO <= t_norm < LATE_PLANETARY_T:
        fold_mid = reg.fold_steps.get("cellular_to_organismic_adjacent_fold", 0.0)
        mid_gate = _smoothstep(t_norm, MID_STAGE_LO, MID_STAGE_PEAK) * (
            1.0 - _smoothstep(t_norm, MID_STAGE_PEAK, LATE_PLANETARY_T)
        )
        gate_mix = (reg.biochemistry_gate + reg.molecular_gate) * 0.5
        bright_gate = _smoothstep(photic, 0.95, 1.35)
        em_photic = min(max(photic, 0.0) ** ((PHI - 1.0) / PHI), 1.0) * reg.em_gate
        stellar_fold = reg.fold_steps.get("planetary_to_stellar_adjacent_fold", 0.0)
        niche = math.log10(1.0 + max(habitat_extent, 1.0)) / PHI
        low_div_gate = _smoothstep(0.22 - division_rate, 0.0, 0.10)
        low_div = max(0.0, 0.34 - division_rate) * fold_mid * reg.molecular_gate
        return (
            1.0
            + mid_gate * bright_gate * fold_mid * gate_mix * em_photic * gate_scale * 0.91
            + mid_gate * bright_gate * stellar_fold * reg.stellar_gate * em_photic * gate_scale * 0.12
            + mid_gate * bright_gate * niche * reg.ecology_gate * fold_mid * gate_scale * ((PHI - 1.0) / (PHI * 2.0))
            + mid_gate * low_div_gate * low_div * gate_scale
        )

    if t_norm < LATE_PLANETARY_T:
        return 1.0

    fold = reg.fold_steps.get("organismic_to_planetary_adjacent_fold", 0.0)
    niche = math.log10(1.0 + max(habitat_extent, 1.0)) / PHI
    late_gate = min(max((t_norm - LATE_PLANETARY_T) / max(1.0 - LATE_PLANETARY_T, 1e-9), 0.0), 1.0)
    transport = 1.0 + late_gate * fold * reg.ecology_gate * niche * ((PHI - 1.0) / (PHI * 2.0))
    transport *= 1.0 + late_gate * (1.0 - division_rate) * fold * ((PHI - 1.0) / (PHI * 3.0))
    dim_boost = (1.0 - _smoothstep(photic, 0.01, 0.15)) * reg.em_gate * ((PHI - 1.0) / PHI) * 0.025
    transport *= 1.0 + late_gate * dim_boost
    return transport


def connective_midstage_division_transport(
    *,
    t_norm: float,
    is_tail: bool,
    photic: float,
    division_rate: float = 0.5,
) -> float:
    """Biochemistry×cellular fold offsets contact inhibition; EM path when photic is dim."""
    if is_tail or t_norm < MID_STAGE_LO or t_norm >= LATE_PLANETARY_T:
        return 1.0
    reg = load_connective_registry()
    mid_gate = _smoothstep(t_norm, MID_STAGE_LO, MID_STAGE_PEAK) * (
        1.0 - _smoothstep(t_norm, MID_STAGE_PEAK, LATE_PLANETARY_T)
    )
    fold = reg.fold_steps.get("cellular_to_organismic_adjacent_fold", 0.0)
    gate_mix = (reg.biochemistry_gate + reg.molecular_gate) * 0.5
    coeff = (PHI - 1.0) / (PHI * 1.32)
    bright_gate = _smoothstep(photic, 0.55, 1.20)
    bright_term = mid_gate * bright_gate * fold * gate_mix * coeff
    dim_gate = (1.0 - _smoothstep(photic, 0.45, 0.90)) * reg.em_gate
    dim_term = mid_gate * dim_gate * fold * reg.molecular_gate * coeff * 0.55
    low_div_gate = _smoothstep(0.26 - division_rate, 0.0, 0.10)
    nuclear_norm = min(reg.nuclear_gate / PHI, 1.0)
    nuclear_term = mid_gate * low_div_gate * nuclear_norm * fold * gate_mix * coeff * 0.70
    return 1.0 + bright_term + dim_term + nuclear_term


def connective_midstage_duration_transport(
    *,
    t_norm: float,
    is_tail: bool,
    photic: float,
) -> float:
    """EM×cellular fold lengthens mid-stage tracks when photic coupling is dim."""
    if is_tail or t_norm < MID_STAGE_LO or t_norm >= LATE_PLANETARY_T:
        return 1.0
    reg = load_connective_registry()
    mid_gate = _smoothstep(t_norm, MID_STAGE_LO, MID_STAGE_PEAK) * (
        1.0 - _smoothstep(t_norm, MID_STAGE_PEAK, LATE_PLANETARY_T)
    )
    fold = reg.fold_steps.get("cellular_to_organismic_adjacent_fold", 0.0)
    dim_gate = (1.0 - _smoothstep(photic, 0.45, 0.90)) * reg.em_gate
    boost = mid_gate * dim_gate * fold * reg.molecular_gate * ((PHI - 1.0) / (PHI * 2.1))
    return 1.0 + boost


def connective_early_division_transport(
    *,
    t_norm: float,
    is_tail: bool,
    det: float = 0.0,
) -> float:
    """Molecular→cellular fold — early embryo proliferation (t < 0.68)."""
    if is_tail or t_norm >= EARLY_STAGE_HI:
        return 1.0
    reg = load_connective_registry()
    fold = reg.fold_steps.get("molecular_to_cellular_adjacent_fold", 0.0)
    early_gate = _smoothstep(t_norm, 0.45, EARLY_STAGE_HI)
    mol_term = fold * reg.molecular_gate
    boost = early_gate * mol_term * ((PHI - 1.0) / (PHI * 2.8))
    crowd_ref = 10.0 ** (3.0 - 1.0 / PHI)
    crowd_gate = _smoothstep(math.log10(max(det, 1.0) / crowd_ref), 1.2, 2.6)
    damp = early_gate * crowd_gate * mol_term * ((PHI - 1.0) / (PHI * 2.2))
    return 1.0 + boost - damp


def connective_tail_displacement_transport(*, t_norm: float, is_tail: bool) -> float:
    """Neural×organismic fold damp — tail extension motility calibration."""
    if not is_tail:
        return 1.0
    reg = load_connective_registry()
    fold = genetic_ladder_fold(t_norm, is_tail=True)
    late_gate = _smoothstep(t_norm, LATE_PLANETARY_T, 1.0)
    damp = late_gate * fold * reg.neural_gate * ((PHI - 1.0) / (PHI * 2.42))
    return 1.0 - damp


def connective_tail_lineage_transport(*, t_norm: float, is_tail: bool) -> float:
    """Neural×cellular→organismic ladder coupling for tail lineage mechanics."""
    if not is_tail:
        return 1.0
    reg = load_connective_registry()
    fold = genetic_ladder_fold(t_norm, is_tail=True)
    late_gate = _smoothstep(t_norm, LATE_PLANETARY_T, 1.0)
    return 1.0 + late_gate * fold * reg.neural_gate * ((PHI - 1.0) / (PHI * 1.17))


def connective_tail_duration_transport(*, t_norm: float, is_tail: bool) -> float:
    """Neural lineage duration extension — decoupled from division coupling."""
    if not is_tail:
        return 1.0
    reg = load_connective_registry()
    fold = genetic_ladder_fold(t_norm, is_tail=True)
    late_gate = _smoothstep(t_norm, LATE_PLANETARY_T, 1.0)
    return 1.0 + late_gate * fold * reg.neural_gate * ((PHI - 1.0) / (PHI * 5.5))


def connective_stability_transport(
    *,
    t_norm: float,
    is_tail: bool,
    division_rate: float = 0.5,
) -> float:
    """Molecular/biochemistry mid-stage + nuclear/thermo late-stage stability coupling."""
    if is_tail:
        return 1.0
    reg = load_connective_registry()
    if t_norm >= LATE_PLANETARY_T:
        return 1.0
    if t_norm < EARLY_STAGE_HI:
        fold = reg.fold_steps.get("molecular_to_cellular_adjacent_fold", 0.0)
        gate = reg.molecular_gate
        stage_gate = _smoothstep(t_norm, 0.45, EARLY_STAGE_HI) * 0.62
    else:
        fold = reg.fold_steps.get("cellular_to_organismic_adjacent_fold", 0.0)
        gate = reg.biochemistry_gate
        stage_gate = (
            4.0 * min(t_norm, 1.0 - t_norm, 0.25) if 0.25 < t_norm < LATE_PLANETARY_T else 0.0
        )
    return 1.0 + stage_gate * fold * gate * ((PHI - 1.0) / (PHI * 3.0))


def interactive_systems_map() -> dict[str, list[str]]:
    """Competition/genetic interactive systems → certified FSOT connective sources."""
    return {
        "proliferation_division": [
            "molecular_to_cellular_adjacent_fold",
            "cellular_to_organismic_adjacent_fold",
            "Biochemistry",
            "Molecular_Chemistry",
            "Nuclear_Physics",
        ],
        "motility_displacement": [
            "organismic_to_planetary_adjacent_fold",
            "Ecology",
            "Electromagnetism",
            "Astronomy",
        ],
        "lineage_duration": [
            "cellular_to_organismic_adjacent_fold",
            "Neuroscience",
            "longevity_genome_pressure",
        ],
        "developmental_stability": [
            "molecular_to_cellular_adjacent_fold",
            "Biochemistry",
            "Thermodynamics",
        ],
        "imaging_photonic": [
            "Thermodynamics",
            "Electromagnetism",
            "Astronomy",
            "Planetary_Science",
            "planetary_to_stellar_adjacent_fold",
        ],
        "environmental_medium": [
            "Ecology",
            "Planetary_Science",
            "organismic_to_planetary_adjacent_fold",
        ],
        "evolution_longevity": [
            "evolution_operon_benchmark",
            "longevity_genome_pressure",
            "Nuclear_Physics",
        ],
    }


def photonic_transport_from_registry(gpu_intensity: float | None) -> tuple[float, dict[str, float]]:
    """Legacy cellular-rung readout + certified environment-stack gates."""
    legacy = 0.0 if not gpu_intensity or gpu_intensity <= 0 else math.log10(1.0 + gpu_intensity) / PHI
    reg = load_connective_registry()
    gate_pow = 1.0 / (PHI * 2.0)
    return legacy, {
        "photic_legacy_coupling": legacy,
        "photic_solar_gate": reg.solar_gate,
        "photic_em_gate": reg.em_gate,
        "photic_stellar_gate": reg.stellar_gate,
        "photic_galactic_gate": reg.galactic_gate,
        "photic_ladder_log_fold": reg.environment_log_fold,
        "photic_solar_coupling": legacy * (reg.solar_gate ** gate_pow),
        "photic_galactic_coupling": legacy * (reg.galactic_gate ** gate_pow),
        "photic_em_coupling": legacy * (reg.em_gate ** gate_pow),
        "photic_bridge_authority": reg.authority_path,
    }