#!/usr/bin/env python3
"""
FSOT-Living bridge for Kaggle cell-tracking vision.

Canonical Rust source: FSOT-Living fsot-living-rust/src/cell_tracking.rs

Ports two mechanisms from github.com/dappalumbo91/FSOT-Living:

1. accuracy_homeo — when vision organ accuracy sits below healthy band (0.62),
   boost emergence stimuli; when over-detecting, apply damping.
2. vision organ regime — warm/bright → emergence (recall); cool/dark → damping (precision).

Cell tracking maps to Living's **closed-set ranking** strength: U-Net proposes candidates,
FSOT scalar ranks them; weak accuracy regions get homeostatic threshold shifts.

Set FSOT_LIVING_EMERGENCE=1 to enable (v50 competitive default when env set).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np

from fsot_core import FERTILE_HIGH, FERTILE_LOW, compute_scalar_biological

# Mirrors fsot-living-rust/src/accuracy_homeo.rs
VISION_CORE_THR = 0.62
MEDIA_THR = 0.72


@dataclass
class LivingVisionState:
    regime: str
    organ_accuracy_proxy: float
    deficit: float
    boost_strength: float
    det_threshold_delta: float
    nms_um_delta: float
    gate_frac_delta: float
    per_frame_cap_scale: float


def _frame_regime_from_stats(brightness: float, mean_r: float, mean_g: float, mean_b: float, sat: float) -> str:
    """Port of fsot-living-rust/src/vision.rs regime heuristic."""
    if mean_g > mean_r and mean_g > mean_b and brightness > 0.25:
        return "emergence"
    if brightness > 0.45 and (mean_r > mean_b + 0.05):
        return "emergence"
    if brightness < 0.45 and mean_b > mean_r + 0.05:
        return "damping"
    if sat < 0.12:
        return "neutral"
    return "neutral"


def boost_strength(acc: float, thr: float, teach_gain: float = 1.0) -> float:
    """accuracy_homeo.rs boost_str — stimulus from deficit × teach_gain."""
    deficit = max(thr - acc, 0.0)
    return (0.55 + deficit * 1.5) * min(max(teach_gain, 0.4), 1.4)


def fuse_detection_score(
    unet_conf: float,
    fsot_scalar: float,
    *,
    ml_weight: float | None = None,
    fsot_weight: float | None = None,
) -> float:
    """Living closed-set rank: U-Net proposal × FSOT fertile alignment."""
    ml_w = ml_weight if ml_weight is not None else float(os.environ.get("FSOT_LIVING_ML_WEIGHT", "0.72"))
    fsot_w = fsot_weight if fsot_weight is not None else float(os.environ.get("FSOT_LIVING_FSOT_WEIGHT", "0.28"))
    return (max(unet_conf, 1e-6) ** ml_w) * (max(fsot_scalar, 1e-6) ** fsot_w)


def detection_coherence_score(
    t: int,
    z: float,
    y: float,
    x: float,
    *,
    frame_density: float,
    brightness: float = 0.5,
) -> float:
    """
    Closed-set ranking score for one U-Net candidate (Living ranker pattern).

    Higher S in fertile window → prefer keep. Crowded frames raise delta_psi (damping).
    """
    density_norm = min(max(frame_density, 0.0), 1.0)
    delta_psi = 0.06 + 0.18 * density_norm + 0.08 * (1.0 - brightness)
    n_obs = 0.45 + 0.55 * brightness
    s = compute_scalar_biological(N=n_obs, P=1.0, delta_psi=delta_psi, amplitude=1.0)
    mid = 0.5 * (FERTILE_LOW + FERTILE_HIGH)
    fertile_bonus = 1.0 - min(abs(s - mid) / max(mid, 1e-6), 1.0)
    return s * (0.65 + 0.35 * fertile_bonus)


def living_vision_state(
    *,
    proxy_accuracy: float,
    mean_brightness: float = 0.5,
    mean_r: float = 0.33,
    mean_g: float = 0.33,
    mean_b: float = 0.33,
    saturation: float = 0.2,
    nodes_per_frame: float = 0.0,
    target_nodes_per_frame: float = 260.0,
    teach_gain: float = 1.0,
) -> LivingVisionState:
    """
    Diagnose vision organ health and emit homeostatic parameter deltas.

    proxy_accuracy: train-proxy or rolling edge-jaccard estimate (0–1).
    Over-detection (nodes >> target) forces damping even if accuracy is low.
    """
    regime = _frame_regime_from_stats(mean_brightness, mean_r, mean_g, mean_b, saturation)
    deficit = max(VISION_CORE_THR - proxy_accuracy, 0.0)
    boost = boost_strength(proxy_accuracy, VISION_CORE_THR, teach_gain)

    over_density = (
        target_nodes_per_frame > 0
        and nodes_per_frame > target_nodes_per_frame * 1.15
    )
    severe_over = (
        target_nodes_per_frame > 0
        and nodes_per_frame > target_nodes_per_frame * 1.25
    )
    under_density = (
        target_nodes_per_frame > 0
        and nodes_per_frame < target_nodes_per_frame * 0.90
    )

    if severe_over:
        regime = "damping"
    elif over_density and proxy_accuracy < VISION_CORE_THR:
        regime = "damping"
    elif under_density and proxy_accuracy < VISION_CORE_THR:
        regime = "emergence"

    det_delta = 0.0
    nms_delta = 0.0
    gate_delta = 0.0
    cap_scale = 1.0

    if regime == "emergence":
        det_delta = -0.03 * boost
        nms_delta = -0.5
        gate_delta = -0.02
        cap_scale = 1.05
    elif regime == "damping":
        det_delta = 0.03 + 0.02 * min(deficit, 0.5)
        nms_delta = 0.5 if over_density else 0.0
        gate_delta = 0.02
        cap_scale = 0.95 if severe_over else 1.0
    else:
        det_delta = -0.01 * deficit
        gate_delta = -0.005 * deficit

    return LivingVisionState(
        regime=regime,
        organ_accuracy_proxy=proxy_accuracy,
        deficit=deficit,
        boost_strength=boost,
        det_threshold_delta=det_delta,
        nms_um_delta=nms_delta,
        gate_frac_delta=gate_delta,
        per_frame_cap_scale=cap_scale,
    )


def rank_detection_mask(
    coords: np.ndarray,
    *,
    det_conf: np.ndarray | None = None,
    proxy_accuracy: float = 0.54,
    target_per_frame: float | None = None,
    brightness: float = 0.5,
) -> np.ndarray:
    """
    Living closed-set ranker: fuse U-Net confidence + FSOT scalar per detection.
    Only hard-caps when severely over-dense (precision rescue, not recall kill).
    """
    if len(coords) == 0:
        return np.zeros(0, dtype=bool)

    if not living_should_activate(proxy_accuracy):
        return np.ones(len(coords), dtype=bool)

    target_pf = target_per_frame or float(os.environ.get("FSOT_LIVING_TARGET_PER_FRAME", "258"))
    n_frames = max(len(np.unique(coords[:, 0])), 1)
    nodes_pf = len(coords) / n_frames
    state = living_vision_state(
        proxy_accuracy=proxy_accuracy,
        mean_brightness=brightness,
        nodes_per_frame=nodes_pf,
        target_nodes_per_frame=target_pf,
    )

    min_conf = float(os.environ.get("FSOT_LIVING_MIN_UNET_CONF", "0.0"))
    keep = np.ones(len(coords), dtype=bool)
    if det_conf is not None and len(det_conf) == len(coords) and min_conf > 0:
        keep &= det_conf >= min_conf

    severe_over = nodes_pf > target_pf * 1.22
    if severe_over and det_conf is not None and len(det_conf) == len(coords):
        cap = int(max(target_pf * 1.02, 200))
        for t in np.unique(coords[:, 0]):
            frame_idx = np.where(coords[:, 0] == t)[0]
            if len(frame_idx) <= cap:
                continue
            frame = coords[frame_idx]
            confs = det_conf[frame_idx]
            density = len(frame_idx) / max(target_pf, 1.0)
            scores = np.array([
                fuse_detection_score(
                    float(confs[i]),
                    detection_coherence_score(
                        int(c[0]), c[1], c[2], c[3],
                        frame_density=min(density, 2.0),
                        brightness=brightness,
                    ),
                )
                for i, c in enumerate(frame)
            ], dtype=np.float64)
            order = np.argsort(-scores)[:cap]
            local = np.zeros(len(frame_idx), dtype=bool)
            local[order] = True
            keep[frame_idx] = keep[frame_idx] & local

    print(
        f"[FSOT-LIVING] regime={state.regime} proxy_acc={proxy_accuracy:.2f} "
        f"nodes/frame={nodes_pf:.0f} unet_conf={'yes' if det_conf is not None else 'no'} "
        f"kept={keep.sum()}/{len(coords)}"
    )
    return keep


def apply_living_det_adjustments(base_det: float, state: LivingVisionState) -> float:
    lo = float(os.environ.get("FSOT_VISION_THRESHOLD_LO", "0.45"))
    hi = float(os.environ.get("FSOT_VISION_THRESHOLD_HI", "0.68"))
    return min(max(base_det + state.det_threshold_delta, lo), hi)


def living_should_activate(proxy_accuracy: float | None = None) -> bool:
    """accuracy_homeo: only stimulate weak vision organ (proxy < 0.62)."""
    if os.environ.get("FSOT_LIVING_EMERGENCE", "0") != "1":
        return False
    if os.environ.get("FSOT_LIVING_ADAPTIVE", "1") != "1":
        return True
    proxy = proxy_accuracy
    if proxy is None:
        try:
            proxy = float(os.environ.get("FSOT_LIVING_PROXY_ACCURACY", "0.90"))
        except ValueError:
            proxy = 0.90
    return proxy < VISION_CORE_THR


def living_enabled() -> bool:
    return living_should_activate()