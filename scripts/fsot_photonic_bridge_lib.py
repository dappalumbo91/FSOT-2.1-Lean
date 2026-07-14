"""FSOT photonic bridge — reuse certified solar/galactic/ladder scalars for biology coupling.

Microscope photon fields couple through the same FSOT scalar engine and adjacent-rung
fold steps already solved for airfoil gas-medium, stellar, and galactic panels (~0.02% gate).
Local GPU intensity remains the cellular-rung boundary observation; domain scalars supply
the connective transport (EM → plasma/thermo → stellar → galactic).
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

CELLULAR_TO_GALACTIC_MECHANISMS = (
    "molecular_to_cellular_adjacent_fold",
    "cellular_to_organismic_adjacent_fold",
    "organismic_to_planetary_adjacent_fold",
    "planetary_to_stellar_adjacent_fold",
    "stellar_to_galactic_adjacent_fold",
)

PHI = (1.0 + math.sqrt(5.0)) / 2.0


@dataclass(frozen=True)
class PhotonicBridge:
    biology: float
    thermodynamics: float
    electromagnetism: float
    astronomy: float
    planetary_science: float
    fold_steps: tuple[float, ...]
    log_fold: float
    solar_gate: float
    em_gate: float
    stellar_gate: float
    galactic_gate: float
    authority_path: str


def _smoothstep(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    t = (x - lo) / (hi - lo)
    return t * t * (3.0 - 2.0 * t)


def _load_fold_steps() -> tuple[float, ...]:
    if not ADJACENT_BENCH.exists():
        return tuple()
    doc = json.loads(ADJACENT_BENCH.read_text(encoding="utf-8"))
    by_mech: dict[str, float] = {}
    for row in doc.get("material_records") or []:
        if row.get("property") != "adjacent_fold_step":
            continue
        mech = str(row.get("mechanism") or "")
        if mech:
            by_mech[mech] = float(row.get("computed") or 0.0)
    return tuple(by_mech[m] for m in CELLULAR_TO_GALACTIC_MECHANISMS if m in by_mech)


@lru_cache(maxsize=1)
def load_photonic_bridge() -> PhotonicBridge:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import canonical_domain_scalar, load_fsot_compute  # noqa: WPS433

    _, authority = load_fsot_compute()
    biology = float(canonical_domain_scalar("Biology"))
    thermodynamics = float(canonical_domain_scalar("Thermodynamics"))
    electromagnetism = float(canonical_domain_scalar("Electromagnetism"))
    astronomy = float(canonical_domain_scalar("Astronomy"))
    planetary_science = float(canonical_domain_scalar("Planetary_Science"))

    fold_steps = _load_fold_steps()
    log_fold = sum(math.log1p(step) for step in fold_steps) / PHI if fold_steps else 0.0
    bio_abs = max(abs(biology), 1e-9)

    return PhotonicBridge(
        biology=biology,
        thermodynamics=thermodynamics,
        electromagnetism=electromagnetism,
        astronomy=astronomy,
        planetary_science=planetary_science,
        fold_steps=fold_steps,
        log_fold=log_fold,
        solar_gate=abs(thermodynamics) / bio_abs,
        em_gate=abs(electromagnetism) / bio_abs,
        stellar_gate=abs(astronomy) / bio_abs,
        galactic_gate=abs(planetary_science) / max(abs(astronomy), 1e-9),
        authority_path=str(authority),
    )


def _scalar_coupling_readout(
    local_n: float,
    *,
    bridge: PhotonicBridge,
    dev_psi: float,
    k: float,
    bio_d_eff: float,
    compute_scalar_fast: Any,
) -> tuple[float, float]:
    p_press = bridge.em_gate
    rho = min(bridge.solar_gate * bridge.galactic_gate, 2.5)
    delta_psi = dev_psi + (PHI - 1.0) * bridge.log_fold
    s_photon = float(
        compute_scalar_fast(
            N=max(local_n, 1e-6),
            P=p_press,
            D_eff=bio_d_eff,
            delta_psi=delta_psi,
            delta_theta=1.0,
            rho=rho,
            observed=True,
        )
    )
    coupling = math.log10(1.0 + abs(s_photon) / max(k, 1e-9)) / PHI
    return coupling, s_photon


_CALIBRATION: float | None = None


def _cellular_rung_calibration(
    k: float,
    bio_d_eff: float,
    compute_scalar_fast: Any,
) -> float:
    """Anchor FSOT photonic transport to the cellular-rung intensity reference (PHI*200)."""
    global _CALIBRATION
    if _CALIBRATION is not None:
        return _CALIBRATION
    bridge = load_photonic_bridge()
    ref_intensity = PHI * 200.0
    ref_local_n = math.log10(1.0 + ref_intensity)
    ref_legacy = ref_local_n / PHI
    ref_fsot, _ = _scalar_coupling_readout(
        ref_local_n,
        bridge=bridge,
        dev_psi=0.1,
        k=k,
        bio_d_eff=bio_d_eff,
        compute_scalar_fast=compute_scalar_fast,
    )
    _CALIBRATION = 1.0 if ref_fsot <= 1e-12 else ref_legacy / ref_fsot
    return _CALIBRATION


def fsot_photonic_coupling(
    gpu_intensity: float | None,
    *,
    snr: float = 0.0,
    dev_psi: float = 0.1,
    k: float,
    bio_d_eff: float,
    compute_scalar_fast: Any,
) -> tuple[float, dict[str, float]]:
    """Return (photic_coupling, diagnostics) using pre-solved FSOT transport."""
    bridge = load_photonic_bridge()
    local_n = math.log10(1.0 + gpu_intensity) if gpu_intensity and gpu_intensity > 0 else 0.0

    if local_n <= 0:
        return 0.0, {
            "photic_local_n": 0.0,
            "photic_fsot_scalar": 0.0,
            "photic_solar_gate": bridge.solar_gate,
            "photic_galactic_gate": bridge.galactic_gate,
            "photic_ladder_log_fold": bridge.log_fold,
            "photic_bridge_calibration": 1.0,
        }

    legacy = local_n / PHI
    coupling, s_photon = _scalar_coupling_readout(
        local_n,
        bridge=bridge,
        dev_psi=dev_psi,
        k=k,
        bio_d_eff=bio_d_eff,
        compute_scalar_fast=compute_scalar_fast,
    )
    calibration = _cellular_rung_calibration(k, bio_d_eff, compute_scalar_fast)
    fsot_at_obs = float(coupling * calibration)
    ref_local_n = math.log10(1.0 + PHI * 200.0)
    ref_fsot, _ = _scalar_coupling_readout(
        ref_local_n,
        bridge=bridge,
        dev_psi=dev_psi,
        k=k,
        bio_d_eff=bio_d_eff,
        compute_scalar_fast=compute_scalar_fast,
    )
    fsot_at_ref = float(ref_fsot * calibration)
    if fsot_at_ref > 1e-12 and fsot_at_obs > 0:
        transport_shape = (fsot_at_obs / fsot_at_ref) ** (1.0 / PHI)
        coupling = legacy * transport_shape
    else:
        coupling = legacy

    if snr > 0:
        coupling *= _smoothstep(math.log10(1.0 + snr), 0.05, 1.0)

    return coupling, {
        "photic_local_n": local_n,
        "photic_fsot_scalar": s_photon,
        "photic_solar_gate": bridge.solar_gate,
        "photic_em_gate": bridge.em_gate,
        "photic_stellar_gate": bridge.stellar_gate,
        "photic_galactic_gate": bridge.galactic_gate,
        "photic_ladder_log_fold": bridge.log_fold,
        "photic_bridge_calibration": calibration,
        "photic_legacy_coupling": legacy,
        "photic_fsot_transport": fsot_at_obs,
        "photic_bridge_authority": bridge.authority_path,
    }