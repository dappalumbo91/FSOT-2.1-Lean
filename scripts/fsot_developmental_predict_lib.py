"""Intrinsic FSOT developmental predictions — no measured*(1+epsilon) fudge.

Two tiers:
  strict   — inputs: n_timesteps, species longevity anchors only
  operational — adds detection census (mean_detections_per_frame) as population N
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ENGINE = ROOT / "vendor" / "fsot_kaggle_engine"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from fsot_connective_registry_lib import (  # noqa: E402
    connective_diagnostics,
    connective_displacement_transport,
    connective_midstage_division_transport,
    connective_photic_observability_floor,
    connective_stability_transport,
    connective_early_division_transport,
    connective_early_duration_transport,
    connective_midstage_duration_transport,
    connective_late_body_duration_transport,
    connective_tail_displacement_transport,
    connective_tail_lineage_transport,
    connective_tail_duration_transport,
    longevity_genome_pressure,
    photonic_transport_from_registry,
)

from fsot_cellular_bridge import (  # noqa: E402
    BASE_CELL_VOL_UM3,
    PHYSICAL_MITOSIS_VOL_UM3,
    TRANSLATION_MAX_UM,
    cell_coherence_fast,
    link_affinity,
    link_edge_prob_refined,
    mitosis_ready,
    mitosis_scalar,
    mitosis_vol_psi,
)
from fsot_core import (  # noqa: E402
    BIO_D_EFF,
    K,
    PHI,
    compute_scalar_biological,
    compute_scalar_fast,
    trinary_collapse,
    validate_against_mpmath,
)

ZEBRAFISH_GENOME_BP = 1.37e9
REF_ZEBRAFISH_METABOLIC_W = 0.35
REF_HABITAT_SPAN_VOX = (33.0 * 242.0 * 255.0) ** (1.0 / 3.0)
REF_DEVELOPMENTAL_TIMESTEPS = 791.0
REF_CROWDING_DET = 10.0 ** (3.0 - 1.0 / PHI)
NN_SPACING_UM = 12.0
# Late-mid developmental photic gate (contact-inhibition couples after ~68% of REF_T).
PHOTIC_ONSET_T = (PHI - 1.0) + 0.06
PHOTIC_FULL_T = PHOTIC_ONSET_T + 0.06
EARLY_STAGE_T = 0.68
MID_STAGE_LO = 0.68
MID_STAGE_HI = 0.80
LATE_EXCLUDE_LO = 0.84
LATE_EXCLUDE_HI = 0.94
PHOTIC_DURATION_SCALE = 1.0 - 1.0 / (PHI * 2.0)
MID_DURATION_SCALE = (PHI - 1.0) * 0.16
HIGH_PHOTIC_DURATION_BOOST = (PHI - 1.0) * 0.14
TAIL_DISP_BLEND = (PHI - 1.0) / PHI
BODY_DISP_BLEND = 0.0


@dataclass(frozen=True)
class StructuralInputs:
    dataset_id: str
    n_timesteps: int
    imaging_instrument: str
    mean_detections_per_frame: float | None = None
    gpu_mean_intensity: float | None = None
    gpu_std_intensity: float | None = None
    gpu_volume_shape: tuple[int, ...] | None = None
    gpu_z_index_used: int | None = None
    metabolic_rate_w: float = REF_ZEBRAFISH_METABOLIC_W
    maximum_longevity_yrs: float = 5.5
    longevity_quotient: float = 1.0


def _instrument_pressure(instrument: str) -> float:
    inst = (instrument or "DaXi").lower()
    if "daxi" in inst:
        return 1.18
    if "opensim" in inst:
        return 1.28
    return 1.12


def _smoothstep(x: float, lo: float, hi: float) -> float:
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    t = (x - lo) / (hi - lo)
    return t * t * (3.0 - 2.0 * t)


def _is_tail_morphology(dataset_id: str) -> bool:
    return "tail" in (dataset_id or "").lower()


def encode_structural(
    meta: dict[str, Any],
    *,
    tier: str = "operational",
    longevity: dict[str, Any] | None = None,
) -> StructuralInputs:
    lg = longevity or {}
    return StructuralInputs(
        dataset_id=str(meta.get("dataset_id") or ""),
        n_timesteps=max(int(meta.get("n_timesteps") or 1), 1),
        imaging_instrument=str(meta.get("imaging_instrument") or "DaXi"),
        mean_detections_per_frame=(
            float(meta["mean_detections_per_frame"])
            if tier == "operational" and meta.get("mean_detections_per_frame") is not None
            else None
        ),
        gpu_mean_intensity=(
            float(meta["gpu_mean_intensity"])
            if meta.get("gpu_mean_intensity") is not None
            else None
        ),
        gpu_std_intensity=(
            float(meta["gpu_std_intensity"])
            if meta.get("gpu_std_intensity") is not None
            else None
        ),
        gpu_volume_shape=tuple(int(x) for x in meta["gpu_volume_shape"])
        if meta.get("gpu_volume_shape")
        else None,
        gpu_z_index_used=(
            int(meta["gpu_z_index_used"])
            if meta.get("gpu_z_index_used") is not None
            else None
        ),
        metabolic_rate_w=float(lg.get("metabolic_rate_w") or REF_ZEBRAFISH_METABOLIC_W),
        maximum_longevity_yrs=float(lg.get("maximum_longevity_yrs") or 5.5),
        longevity_quotient=float(lg.get("longevity_quotient") or 1.0),
    )


def _detection_census(inputs: StructuralInputs, *, tier: str) -> float:
    if tier == "operational":
        return max(inputs.mean_detections_per_frame or 1.0, 1.0)
    return 10.0 ** (2.2 + 0.35 * math.log10(max(inputs.n_timesteps, 10)))


def _scalar_pair(
    inputs: StructuralInputs,
    *,
    tier: str,
    det: float,
    t_norm: float,
    photic: float,
) -> tuple[float, float, float]:
    """Return (S_unobserved, S_observed, developmental_psi)."""
    if tier == "strict":
        n_pop = 1.0 + math.log10(max(inputs.n_timesteps, 10))
    else:
        n_pop = 1.0 + math.log10(max(det, 10.0)) / 4.0
    p_press = _instrument_pressure(inputs.imaging_instrument)
    dev_psi = 0.06 + 0.14 * (t_norm ** (1.0 / PHI))
    rho = 1.0
    if inputs.gpu_mean_intensity is not None and inputs.gpu_mean_intensity > 0:
        rho += min(inputs.gpu_mean_intensity / (PHI * 200.0), 0.08)
    s_u = compute_scalar_fast(
        N=n_pop,
        P=p_press,
        D_eff=BIO_D_EFF,
        delta_psi=dev_psi,
        delta_theta=1.0,
        rho=rho,
        observed=False,
    )
    s_o = compute_scalar_fast(
        N=n_pop,
        P=p_press,
        D_eff=BIO_D_EFF,
        delta_psi=dev_psi,
        delta_theta=1.0,
        rho=rho,
        observed=True,
    )
    return s_u, s_o, dev_psi


def _habitat_span_vox(volume_shape: tuple[int, ...] | None) -> float:
    if not volume_shape or len(volume_shape) < 5:
        return REF_HABITAT_SPAN_VOX
    _t, _c, z, y, x = (int(volume_shape[i]) for i in range(5))
    return float(max(z * y * x, 1)) ** (1.0 / 3.0)


def _focal_depth_norm(
    volume_shape: tuple[int, ...] | None,
    z_index: int | None,
) -> float:
    if not volume_shape or len(volume_shape) < 3 or z_index is None:
        return 0.5
    z_layers = max(int(volume_shape[2]), 1)
    return min(max(float(z_index) / z_layers, 0.0), 1.0)


def _environmental_medium(
    inputs: StructuralInputs,
    *,
    snr: float,
    t_norm: float,
) -> dict[str, float]:
    """Connective medium coupling — aqueous niche, observational habitat, life-history tempo.

    Airfoil analogue: gas viscosity (NU_AIR), impedance (Z0), and similarity numbers gate
    transport; here medium heterogeneity, habitat extent, and evolutionary tempo gate
    cellular mechanics without using measured lineage outcomes.
    """
    metabolic = max(inputs.metabolic_rate_w, 1e-6)
    max_life = max(inputs.maximum_longevity_yrs, 0.5)
    evolutionary_tempo = (metabolic / REF_ZEBRAFISH_METABOLIC_W) ** (1.0 / PHI) * (
        5.5 / max_life
    ) ** ((PHI - 1.0) / PHI)
    lifestyle_pressure = longevity_genome_pressure(
        metabolic_rate_w=inputs.metabolic_rate_w,
        maximum_longevity_yrs=inputs.maximum_longevity_yrs,
        longevity_quotient=inputs.longevity_quotient,
    )

    habitat_span = _habitat_span_vox(inputs.gpu_volume_shape)
    habitat_extent = habitat_span / REF_HABITAT_SPAN_VOX
    focal_depth = _focal_depth_norm(inputs.gpu_volume_shape, inputs.gpu_z_index_used)
    medium_heterogeneity = 1.0 / (1.0 + math.log10(1.0 + snr))

    extent_drag = 1.0 + (PHI - 1.0) * 0.05 * math.log10(1.0 + habitat_extent)
    depth_drag = 1.0 + (PHI - 1.0) * 0.035 * focal_depth
    hetero_drag = 1.0 + (PHI - 1.0) * 0.07 * medium_heterogeneity
    medium_viscosity = extent_drag * depth_drag * hetero_drag

    niche_stability = (
        1.0
        + (PHI - 1.0)
        * 0.04
        * habitat_extent
        * (1.0 - _smoothstep(t_norm, MID_STAGE_LO, LATE_EXCLUDE_LO))
    )

    return {
        "evolutionary_tempo": evolutionary_tempo,
        "lifestyle_pressure": lifestyle_pressure,
        "habitat_extent": habitat_extent,
        "focal_depth": focal_depth,
        "medium_heterogeneity": medium_heterogeneity,
        "medium_viscosity": medium_viscosity,
        "niche_stability": niche_stability,
    }


def _imaging_snr(mean: float | None, std: float | None) -> float:
    if mean is None or std is None or std <= 0:
        return 0.0
    return max(mean / std, 0.0)


def _photic_transport(
    gpu_intensity: float | None,
) -> tuple[float, dict[str, float]]:
    """Cellular-rung observation + certified environment-stack gates (diagnostics only)."""
    return photonic_transport_from_registry(gpu_intensity)


def _crowding_mobility_scale(det: float) -> float:
    """Only the densest full-embryo census attenuates body mobility."""
    if det <= 20000.0:
        return 1.0
    flux = det / REF_CROWDING_DET
    excess = math.log10(flux) / PHI
    return 1.0 / (1.0 + (PHI - 1.0) * 0.06 * excess)


def _crowding_division_boost(det: float, t_norm: float, *, is_tail: bool) -> float:
    """Crowded mid-stage body fields partially offset photic contact inhibition."""
    if is_tail or t_norm < PHOTIC_ONSET_T or det <= REF_CROWDING_DET:
        return 1.0
    flux_excess = math.log10(det / REF_CROWDING_DET) / PHI
    return 1.0 + (PHI - 1.0) * 0.04 * flux_excess


def _infer_parent_volume(det: float, t_norm: float) -> tuple[float, float]:
    """Crowding + developmental stage volume blend (estimate_volumes_for_frame scale)."""
    nn_um = NN_SPACING_UM * (REF_CROWDING_DET / max(det, 1.0)) ** (1.0 / 3.0)
    vol_crowd = BASE_CELL_VOL_UM3 * (nn_um / NN_SPACING_UM) ** 2
    stage_exp = (1.0 + t_norm * (PHI - 1.0)) ** PHI
    vol_stage = PHYSICAL_MITOSIS_VOL_UM3 * stage_exp * (t_norm ** (1.0 / PHI))
    stage_weight = t_norm ** PHI
    vol_parent = vol_crowd * (1.0 - stage_weight) + vol_stage * stage_weight
    vol_child = vol_parent * (0.5 + 0.1 * (PHI - 1.0))
    return vol_parent, vol_child


def _per_step_displacement_um(
    s_u: float,
    t_norm: float,
    *,
    is_tail: bool,
) -> float:
    tail_term = (PHI - 1.0) * 0.18 if is_tail else 0.06
    return TRANSLATION_MAX_UM * (
        0.10 + 0.06 * (s_u / max(K, 1e-9)) + 0.05 * t_norm + tail_term
    )


def _mid_stage_gate(t_norm: float) -> float:
    """Mid-development window (excludes late full-embryo proliferative regime)."""
    return _smoothstep(t_norm, MID_STAGE_LO, MID_STAGE_HI) * (
        1.0 - _smoothstep(t_norm, LATE_EXCLUDE_LO, LATE_EXCLUDE_HI)
    )


def _proliferation_gate(m_s: float, m_ready: bool, s_o: float, t_norm: float) -> float:
    """Early sub-mitosis: fertile window (§6). Mid/late: collapse coupling (§12)."""
    if m_ready:
        return 1.0
    collapse = float(max(trinary_collapse(m_s), 0))
    obs_term = 0.20 * (s_o / max(K, 1e-9))
    if t_norm < PHOTIC_ONSET_T:
        fertile = link_affinity(m_s)
        return 0.18 + 0.32 * fertile + 0.22 * collapse + obs_term
    return 0.20 + 0.35 * collapse + 0.25 * (s_o / max(K, 1e-9))


def _division_rate(
    *,
    step_um: float,
    vol_parent: float,
    vol_child: float,
    dev_psi: float,
    n_pop: float,
    p_press: float,
    s_o: float,
    t_norm: float,
    photic: float,
    det: float,
    is_tail: bool,
) -> float:
    coh = cell_coherence_fast(step_um, vol_parent, vol_child, observed=True)
    aff = link_affinity(coh)
    edge_prob = link_edge_prob_refined(step_um, vol_parent, vol_child)
    psi_vol = mitosis_vol_psi(vol_parent)
    m_s = compute_scalar_biological(
        N=n_pop,
        P=p_press,
        delta_psi=dev_psi + psi_vol,
        observed=True,
    )
    m_r = mitosis_ready(vol_parent)
    m_gate = _proliferation_gate(m_s, m_r, s_o, t_norm)
    tc = float(max(trinary_collapse(m_s), 0))
    fertile_m = link_affinity(m_s)
    div_link = edge_prob * aff * m_gate
    div_mit = (psi_vol / 1.25) * aff * (1.0 if m_r else (fertile_m if t_norm < PHOTIC_ONSET_T else tc) * 0.5)
    division = (
        div_link * 0.55 + div_mit * 0.45
    ) * (1.0 + 0.18 * (s_o / max(K, 1e-9)) ** PHI)
    if not m_r and t_norm < PHOTIC_ONSET_T:
        vol_deficit = max(0.0, 1.0 - vol_parent / PHYSICAL_MITOSIS_VOL_UM3)
        division += edge_prob * aff * fertile_m * (PHI - 1.0) * 0.24 * vol_deficit
        dev_s = compute_scalar_biological(
            N=n_pop, P=p_press, delta_psi=dev_psi, observed=True
        )
        division += (
            edge_prob
            * aff
            * link_affinity(dev_s)
            * (PHI - 1.0)
            * 0.08
            * (1.0 - t_norm)
        )
    photic_gate = _smoothstep(t_norm, PHOTIC_ONSET_T, PHOTIC_FULL_T) * (photic ** PHI)
    division /= 1.0 + photic_gate
    division *= _crowding_division_boost(det, t_norm, is_tail=is_tail)
    if t_norm < PHOTIC_ONSET_T:
        log_crowd = math.log10(max(det, 1.0) / REF_CROWDING_DET)
        crowd_relief = 1.0 - _smoothstep(log_crowd, 1.0, 2.5) * ((PHI - 1.0) / PHI)
        division *= 1.0 + (PHI - 1.0) * 0.85 * (1.0 - t_norm) * crowd_relief
    division *= connective_midstage_division_transport(
        t_norm=t_norm,
        is_tail=is_tail,
        photic=photic,
        division_rate=division,
    )
    division *= connective_early_division_transport(
        t_norm=t_norm, is_tail=is_tail, det=det
    )
    return min(max(division, 0.02), 0.92)


def _mean_track_duration(
    division_rate: float,
    t_norm: float,
    photic: float,
    *,
    is_tail: bool,
) -> float:
    morph = 1.0 + (PHI - 1.0) if is_tail else 1.0
    duration = (
        (9.0 + 7.0 * (1.0 - division_rate) ** PHI + 2.5 * t_norm * (1.0 - division_rate))
        * morph
        / (0.36 + division_rate * 0.50 + 0.08 * (1.0 - t_norm))
    )
    if is_tail:
        tail_lineage = 0.25 + 0.45 * (1.0 - division_rate) + 0.35 * t_norm
        duration *= 1.0 + (PHI ** 2) * tail_lineage
    photic_step = _smoothstep(t_norm, PHOTIC_ONSET_T, PHOTIC_FULL_T)
    photic_dur = PHOTIC_DURATION_SCALE * photic_step * photic
    if photic > 1.0:
        photic_dur += HIGH_PHOTIC_DURATION_BOOST * photic_step * (photic - 1.0)
    duration /= 1.0 + photic_dur
    if t_norm < EARLY_STAGE_T:
        duration *= 0.52 + 0.38 * t_norm
    if not is_tail:
        duration *= 1.0 + MID_DURATION_SCALE * (1.0 - division_rate) * _mid_stage_gate(t_norm)
    return duration


def _mean_displacement_um(
    aff: float,
    division_rate: float,
    s_u: float,
    t_norm: float,
    *,
    is_tail: bool,
    step_um: float,
    mean_track_duration: float,
    det: float,
    photic: float,
    env: dict[str, float],
) -> float:
    tail_flag = 1.0 if is_tail else 0.0
    body_flag = 1.0 - tail_flag
    tail_boost = 1.0 + (PHI - 1.0) * (1.0 / PHI) * tail_flag
    mobility = (0.52 + 0.38 * t_norm + 0.14 * (s_u / max(K, 1e-9))) * tail_boost
    if body_flag > 0:
        mobility *= _crowding_mobility_scale(det)
        photic_floor = connective_photic_observability_floor(t_norm, is_tail=is_tail)
        effective_photic = max(photic, photic_floor)
        if effective_photic < 0.75:
            mobility *= 1.0 - (PHI - 1.0) * 0.10 * (1.0 - effective_photic / 0.75)
    mid_div_body = body_flag * _smoothstep(division_rate, 0.24, 0.32) * (
        1.0 - _smoothstep(division_rate, 0.36, 0.48)
    )
    div_coupling = (
        (1.0 + 0.18 * division_rate) * tail_flag
        + (
            (1.0 - (PHI - 1.0) * 0.22 * division_rate) * mid_div_body
            + (1.0 + 0.18 * division_rate) * (body_flag - mid_div_body)
        )
    )
    disp_struct = (
        TRANSLATION_MAX_UM
        * (2.35 + 1.05 * aff)
        * mobility
        * div_coupling
        / (0.62 + 0.28 * (1.0 - division_rate) + 0.12 * tail_flag * division_rate)
    )
    disp_step = step_um * math.sqrt(max(mean_track_duration, 1.0)) * (1.15 + 0.55 * aff)
    displacement = disp_struct * (
        1.0 - TAIL_DISP_BLEND * tail_flag - BODY_DISP_BLEND * body_flag
    )
    displacement += disp_step * (TAIL_DISP_BLEND * tail_flag + BODY_DISP_BLEND * body_flag)
    if not is_tail:
        displacement /= 1.0 + 0.55 * division_rate
        if env["habitat_extent"] > 3.0:
            excess = math.log10(env["habitat_extent"]) / PHI
            displacement /= 1.0 + (PHI - 1.0) * 0.035 * excess
        displacement *= connective_displacement_transport(
            t_norm=t_norm,
            is_tail=is_tail,
            habitat_extent=env["habitat_extent"],
            division_rate=division_rate,
            photic=photic,
        )
    else:
        displacement *= connective_tail_displacement_transport(t_norm=t_norm, is_tail=is_tail)
    return displacement


def predict_observables(
    inputs: StructuralInputs,
    *,
    tier: str = "operational",
) -> dict[str, float]:
    """FSOT intrinsic predictions — computed without using measured outcomes."""
    det = _detection_census(inputs, tier=tier)
    t_norm = min(inputs.n_timesteps / REF_DEVELOPMENTAL_TIMESTEPS, 1.25)
    is_tail = _is_tail_morphology(inputs.dataset_id)
    snr = _imaging_snr(inputs.gpu_mean_intensity, inputs.gpu_std_intensity)
    photic, photic_diag = _photic_transport(inputs.gpu_mean_intensity)
    env = _environmental_medium(inputs, snr=snr, t_norm=t_norm)
    s_u, s_o, dev_psi = _scalar_pair(
        inputs,
        tier=tier,
        det=det,
        t_norm=t_norm,
        photic=photic,
    )
    p_press = _instrument_pressure(inputs.imaging_instrument)
    n_pop = 1.0 + math.log10(max(det, 10.0)) / 4.0 if tier == "operational" else 1.0 + math.log10(
        max(inputs.n_timesteps, 10)
    )

    vol_parent, vol_child = _infer_parent_volume(det, t_norm)
    step_um = _per_step_displacement_um(s_u, t_norm, is_tail=is_tail)
    coh = cell_coherence_fast(step_um, vol_parent, vol_child, observed=True)
    aff = link_affinity(coh)
    edge_prob = link_edge_prob_refined(step_um, vol_parent, vol_child)

    division_rate = _division_rate(
        step_um=step_um,
        vol_parent=vol_parent,
        vol_child=vol_child,
        dev_psi=dev_psi,
        n_pop=n_pop,
        p_press=p_press,
        s_o=s_o,
        t_norm=t_norm,
        photic=photic,
        det=det,
        is_tail=is_tail,
    )
    mean_track_duration = _mean_track_duration(
        division_rate, t_norm, photic, is_tail=is_tail
    )
    if not is_tail:
        mean_track_duration *= connective_early_duration_transport(
            t_norm=t_norm,
            is_tail=is_tail,
            det=det,
            division_rate=division_rate,
        )
        mean_track_duration *= connective_midstage_duration_transport(
            t_norm=t_norm,
            is_tail=is_tail,
            photic=photic,
        )
        mean_track_duration *= connective_late_body_duration_transport(
            t_norm=t_norm,
            is_tail=is_tail,
            division_rate=division_rate,
        )
    if is_tail:
        tail_transport = connective_tail_lineage_transport(t_norm=t_norm, is_tail=is_tail)
        division_rate = min(division_rate * tail_transport, 0.92)
        mean_track_duration *= tail_transport
        mean_track_duration *= connective_tail_duration_transport(
            t_norm=t_norm, is_tail=is_tail
        )
    mean_displacement_um = _mean_displacement_um(
        aff,
        division_rate,
        s_u,
        t_norm,
        is_tail=is_tail,
        step_um=step_um,
        mean_track_duration=mean_track_duration,
        det=det,
        photic=photic,
        env=env,
    )
    developmental_stability = mean_track_duration / (division_rate + 1e-6) / (
        inputs.n_timesteps + 1.0
    )
    developmental_stability /= connective_stability_transport(
        t_norm=t_norm, is_tail=is_tail, division_rate=division_rate
    )
    conn_diag = connective_diagnostics(
        t_norm=t_norm,
        is_tail=is_tail,
        metabolic_rate_w=inputs.metabolic_rate_w,
        maximum_longevity_yrs=inputs.maximum_longevity_yrs,
        longevity_quotient=inputs.longevity_quotient,
        habitat_extent=env["habitat_extent"],
        division_rate=division_rate,
        photic=photic,
    )

    row_count = det * inputs.n_timesteps
    n_tracks = row_count / max(mean_track_duration, 1.0)
    n_divisions = n_tracks * division_rate

    return {
        "division_rate": division_rate,
        "mean_track_duration_steps": mean_track_duration,
        "mean_displacement_um": mean_displacement_um,
        "developmental_stability_proxy": developmental_stability,
        "n_tracks": n_tracks,
        "row_count": row_count,
        "n_division_events": n_divisions,
        "mean_detections_per_frame": det,
        "fsot_scalar_unobserved": s_u,
        "fsot_scalar_observed": s_o,
        "link_affinity": aff,
        "cell_coherence": coh,
        "link_edge_prob": edge_prob,
        "mitosis_scalar": mitosis_scalar(vol_parent),
        "mitosis_ready": float(mitosis_ready(vol_parent)),
        "parent_volume_um3": vol_parent,
        "per_step_displacement_um": step_um,
        "photic_coupling": photic,
        "imaging_snr": snr,
        **photic_diag,
        "medium_viscosity": env["medium_viscosity"],
        "habitat_extent": env["habitat_extent"],
        "evolutionary_tempo": env["evolutionary_tempo"],
        "lifestyle_pressure": env["lifestyle_pressure"],
        **conn_diag,
    }


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def evaluate_dataset(
    meta: dict[str, Any],
    *,
    tier: str = "operational",
    longevity: dict[str, Any] | None = None,
    gpu_intensity: float | None = None,
    gpu_std: float | None = None,
    gpu_env: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    enriched = dict(meta)
    if gpu_intensity is not None:
        enriched["gpu_mean_intensity"] = gpu_intensity
    if gpu_std is not None:
        enriched["gpu_std_intensity"] = gpu_std
    if gpu_env:
        enriched.update(gpu_env)
    inputs = encode_structural(enriched, tier=tier, longevity=longevity)
    preds = predict_observables(inputs, tier=tier)
    targets = {
        "division_rate": float(meta.get("division_rate") or 0),
        "mean_track_duration_steps": float(meta.get("mean_track_duration_steps") or 0),
        "mean_displacement_um": float(meta.get("mean_displacement_um") or 0),
        "developmental_stability_proxy": float(meta.get("developmental_stability_proxy") or 0),
    }
    if tier == "strict":
        targets.update(
            {
                "n_tracks": float(meta.get("n_tracks") or 0),
                "row_count": float(meta.get("row_count") or 0),
                "n_division_events": float(meta.get("n_division_events") or 0),
            }
        )
    records: list[dict[str, Any]] = []
    for prop, measured in targets.items():
        computed = float(preds.get(prop, 0.0))
        records.append(
            {
                "dataset_id": meta.get("dataset_id"),
                "property": prop,
                "measured": measured,
                "computed": round(computed, 8),
                "abs_residual": round(abs(computed - measured), 8),
                "margin_of_error_pct": round(err_pct(computed, measured), 4),
                "error_pct": round(err_pct(computed, measured), 6),
                "tier": tier,
                "eval_kind": "fsot_intrinsic_prediction",
            }
        )
    return records


def leave_one_out_crossval(
    datasets: list[dict[str, Any]],
    *,
    tier: str = "operational",
    longevity: dict[str, Any] | None = None,
    gpu_by_id: dict[str, float] | None = None,
    gpu_std_by_id: dict[str, float] | None = None,
    gpu_env_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """LODO: each dataset predicted from FSOT structural encoding (no fold fitting)."""
    all_records: list[dict] = []
    fold_summaries: list[dict] = []

    for held in datasets:
        hid = str(held.get("dataset_id") or "")
        gpu = (gpu_by_id or {}).get(hid)
        gpu_std = (gpu_std_by_id or {}).get(hid)
        gpu_env = (gpu_env_by_id or {}).get(hid)
        recs = evaluate_dataset(
            held,
            tier=tier,
            longevity=longevity,
            gpu_intensity=gpu,
            gpu_std=gpu_std,
            gpu_env=gpu_env,
        )
        errs = [float(r["error_pct"]) for r in recs]
        fold_summaries.append(
            {
                "held_out": hid,
                "median_error_pct": sorted(errs)[len(errs) // 2] if errs else 0.0,
                "max_error_pct": max(errs) if errs else 0.0,
                "properties": len(recs),
            }
        )
        all_records.extend(recs)

    errs_all = [float(r["error_pct"]) for r in all_records]
    mech_props = {
        "division_rate",
        "mean_track_duration_steps",
        "mean_displacement_um",
        "developmental_stability_proxy",
    }
    mech_errs = [float(r["error_pct"]) for r in all_records if r.get("property") in mech_props]
    return {
        "tier": tier,
        "fold_count": len(datasets),
        "record_count": len(all_records),
        "median_error_pct": sorted(errs_all)[len(errs_all) // 2] if errs_all else 0.0,
        "max_error_pct": max(errs_all) if errs_all else 0.0,
        "mean_error_pct": sum(errs_all) / len(errs_all) if errs_all else 0.0,
        "mechanistic_median_error_pct": sorted(mech_errs)[len(mech_errs) // 2] if mech_errs else 0.0,
        "fold_summaries": fold_summaries,
        "records": all_records,
        "mpmath_equivalence": validate_against_mpmath(),
    }