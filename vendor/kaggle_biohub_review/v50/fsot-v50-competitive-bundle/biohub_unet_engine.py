#!/usr/bin/env python3
"""
FSOT-first competitive engine (royerlab/kaggle-cell-tracking-competition U-Net detector).

Architecture (matches FSOT-2.1-Lean cellular lab + kaggle_prototype_fsot_tracker):
  1. U-Net local-max detection  — ML vision gateway (coords only)
  2. FSOT SequenceTracker       — phase-scalar link_cost + mitosis gates (edges)

Set FSOT_LINK_MODE=fsot (default) | fsot_union | fsot_gate | hybrid | transformer
"""

from __future__ import annotations

import contextlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
import tracksdata as td


def _wire_cellmot_import_paths() -> None:
    """Prefer patched predict_unet_transformer (local repo or Kaggle cellmot_bundle)."""
    root = Path(__file__).resolve().parent
    for repo in (
        Path("/kaggle/working/cellmot_bundle"),
        root / "kaggle-cell-tracking-competition",
        root / "cellmot_bundle",
    ):
        scripts = repo / "scripts"
        src = repo / "src"
        if not (scripts / "predict_unet_transformer.py").exists():
            continue
        for p in (src, scripts):
            sp = str(p)
            if sp not in sys.path:
                sys.path.insert(0, sp)
        return


_wire_cellmot_import_paths()

from predict_unet_transformer import (  # noqa: E402
    PredictConfig,
    _detect_cells_pooled,
    _load_frame,
    build_graph,
    load_model,
    pool_kernel_from_um,
    predict_video,
)

try:
    from predict_unet_transformer import _detect_cells_pooled_scored  # noqa: E402
except ImportError:
    def _detect_cells_pooled_scored(
        det_logits: torch.Tensor,
        t: int,
        det_threshold: float = 0.5,
        pool_kernel: tuple[int, ...] = (3, 3, 3),
    ) -> tuple[np.ndarray, np.ndarray]:
        """Fallback when bundled cellmot script predates conf-ranked NMS."""
        logits = det_logits.unsqueeze(0)
        pad = tuple(k // 2 for k in pool_kernel)
        pooled = F.max_pool3d(logits, pool_kernel, stride=1, padding=pad)
        probs = torch.sigmoid(logits)
        is_peak = (logits == pooled) & (probs > det_threshold)
        peak_idx = torch.nonzero(is_peak[0, 0])
        if peak_idx.shape[0] == 0:
            return np.empty((0, 4), dtype=np.int16), np.empty(0, dtype=np.float32)
        conf = probs[0, 0, peak_idx[:, 0], peak_idx[:, 1], peak_idx[:, 2]].float().cpu().numpy()
        coords = peak_idx.float().cpu().numpy()
        t_col = np.full((len(coords), 1), t, dtype=np.float32)
        return np.concatenate([t_col, coords], axis=1).astype(np.int16), conf.astype(np.float32)
from tracking_cellmot.io import open_dataset  # noqa: E402
from tracking_cellmot.metrics import evaluate, per_sample_metrics, node_recall, summarise  # noqa: E402

try:
    from tracking_cellmot.img_proc import nms_3d
except ImportError:
    nms_3d = None

ROOT = Path(__file__).resolve().parent
BASELINE_WEIGHTS = ROOT / (
    "cellmot_weights/cellmot-baseline-artifacts/weights/unet_transformer/split_0/edge_predictor_best.pth"
)
FT_WEIGHTS = ROOT / "cellmot_weights/cellmot-ft-detector-biohub/edge_predictor_best.pth"

SCALE = (1.625, 0.40625, 0.40625)
def _nms_min_um() -> float:
    return float(os.environ.get("CELLMOT_NMS_UM", os.environ.get("BIOHUB_NMS_UM", "8.0")))


def _det_topk() -> int:
    return int(os.environ.get("CELLMOT_DET_TOPK", "0"))


def _living_proxy_accuracy() -> float:
    raw = os.environ.get("FSOT_LIVING_PROXY_ACCURACY", "0.90")
    try:
        return float(raw)
    except ValueError:
        return 0.90


def _want_det_conf() -> bool:
    """U-Net sigmoid confidences for NMS ranking (Living dormant at high proxy)."""
    try:
        from fsot_living_emergence import living_should_activate

        if living_should_activate(_living_proxy_accuracy()):
            return True
    except Exception:
        pass
    return os.environ.get("FSOT_DET_CONF_RANK", "1") == "1"


def _nms_scores_for_frame(
    frame: np.ndarray,
    frame_idx: np.ndarray,
    det_conf: np.ndarray | None,
) -> np.ndarray:
    """Per-detection NMS ranking scores: fuse U-Net conf + FSOT when available."""
    try:
        from fsot_living_emergence import living_should_activate

        living_on = living_should_activate(_living_proxy_accuracy())
    except Exception:
        living_on = os.environ.get("FSOT_LIVING_EMERGENCE", "0") == "1"
    if not living_on:
        conf_rank = os.environ.get("FSOT_DET_CONF_RANK", "1") == "1"
        if conf_rank and det_conf is not None and len(det_conf) == len(frame_idx):
            return det_conf.astype(np.float64)
        return np.ones(len(frame), dtype=np.float64)
    target_pf = float(os.environ.get("FSOT_LIVING_TARGET_PER_FRAME", "258"))
    density = len(frame_idx) / max(target_pf, 1.0)
    try:
        from fsot_living_emergence import detection_coherence_score, fuse_detection_score

        if det_conf is not None and len(det_conf) == len(frame_idx):
            return np.array([
                fuse_detection_score(
                    float(det_conf[i]),
                    detection_coherence_score(
                        int(c[0]), c[1], c[2], c[3], frame_density=min(density, 2.0),
                    ),
                )
                for i, c in enumerate(frame)
            ], dtype=np.float64)
        return np.array([
            detection_coherence_score(
                int(c[0]), c[1], c[2], c[3], frame_density=min(density, 2.0),
            )
            for c in frame
        ], dtype=np.float64)
    except Exception:
        return np.ones(len(frame), dtype=np.float64)


def _prune_keep_mask(
    coords: np.ndarray,
    scale: tuple[float, ...] = SCALE,
    det_conf: np.ndarray | None = None,
) -> np.ndarray:
    """Boolean mask of detections to keep after per-frame NMS + optional top-k cap."""
    if len(coords) == 0:
        return np.zeros(0, dtype=bool)
    keep = np.zeros(len(coords), dtype=bool)
    nms_um = _nms_min_um()
    living_on = False
    try:
        from fsot_living_emergence import living_should_activate

        living_on = living_should_activate(_living_proxy_accuracy())
    except Exception:
        living_on = os.environ.get("FSOT_LIVING_EMERGENCE", "0") == "1"
    if living_on:
        try:
            from fsot_living_emergence import living_vision_state

            proxy = _living_proxy_accuracy()
            n_frames = max(len(np.unique(coords[:, 0])), 1)
            state = living_vision_state(
                proxy_accuracy=proxy,
                nodes_per_frame=len(coords) / n_frames,
            )
            nms_um = max(nms_um + state.nms_um_delta, 4.0)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] FSOT-Living NMS adjust skipped: {exc}")
    topk = _det_topk()
    if nms_3d is not None and nms_um > 0:
        for t in np.unique(coords[:, 0]):
            frame_idx = np.where(coords[:, 0] == t)[0]
            frame = coords[frame_idx]
            spatial = frame[:, 1:4].astype(np.float64)
            conf_slice = det_conf[frame_idx] if det_conf is not None and len(det_conf) == len(coords) else None
            scores = _nms_scores_for_frame(frame, frame_idx, conf_slice)
            local = nms_3d(spatial, scores, nms_um, scale)
            keep[frame_idx[local]] = True
    else:
        keep[:] = True
    if living_on:
        try:
            from fsot_living_emergence import rank_detection_mask

            living_keep = rank_detection_mask(
                coords,
                det_conf=det_conf,
                proxy_accuracy=_living_proxy_accuracy(),
            )
            keep &= living_keep
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] FSOT-Living rank prune skipped: {exc}")
    if topk > 0:
        capped = np.zeros(len(coords), dtype=bool)
        for t in np.unique(coords[:, 0]):
            frame_idx = np.where((coords[:, 0] == t) & keep)[0]
            if len(frame_idx) <= topk:
                capped[frame_idx] = True
            else:
                frame = coords[frame_idx]
                center = frame[:, 1:4].mean(axis=0)
                dist = np.linalg.norm(frame[:, 1:4].astype(np.float64) - center, axis=1)
                capped[frame_idx[np.argsort(dist)[:topk]]] = True
        keep = capped
    return keep


def _postprocess_coords(
    coords: np.ndarray,
    det_conf: np.ndarray | None = None,
) -> np.ndarray:
    if len(coords) == 0:
        return coords
    keep = _prune_keep_mask(coords, det_conf=det_conf)
    return coords[keep]


def _postprocess_coords_edges(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
    det_conf: np.ndarray | None = None,
) -> tuple[np.ndarray, list[tuple[int, int, float, float]]]:
    if len(coords) == 0:
        return coords, []
    keep = _prune_keep_mask(coords, det_conf=det_conf)
    if keep.all():
        return coords, edges
    old_to_new = {}
    new_coords = []
    for old_i, k in enumerate(keep):
        if k:
            old_to_new[old_i] = len(new_coords)
            new_coords.append(coords[old_i])
    new_edges = [
        (old_to_new[s], old_to_new[t], p, d)
        for s, t, p, d in edges
        if s in old_to_new and t in old_to_new
    ]
    return np.asarray(new_coords, dtype=coords.dtype), new_edges


def _inject_fsot_mitosis_edges(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
    fsot_edges: list[tuple[int, int, float, float]],
) -> list[tuple[int, int, float, float]]:
    """Preserve FSOT mitosis forks (2 daughters) through the ML gate + ILP path."""
    from collections import defaultdict

    from fsot_cellular_bridge import _vol_key, estimate_volumes_for_frame, mitosis_ready

    if not fsot_edges:
        return edges

    cells_by_idx: dict[int, dict] = {}
    by_t: dict[int, list[int]] = {}
    for idx, row in enumerate(coords):
        cells_by_idx[idx] = {
            "z": float(row[1]), "y": float(row[2]), "x": float(row[3]),
            "physical_volume": float(os.environ.get("FSOT_DEFAULT_VOL_UM3", "500")),
            "vol": float(os.environ.get("FSOT_DEFAULT_VOL_UM3", "500")),
        }
        by_t.setdefault(int(row[0]), []).append(idx)
    for indices in by_t.values():
        estimate_volumes_for_frame([cells_by_idx[i] for i in indices])

    by_src: dict[int, list[tuple[int, int, float, float]]] = defaultdict(list)
    for s, t, p, d in fsot_edges:
        by_src[s].append((s, t, p, d))

    existing = {(s, t) for s, t, _, _ in edges}
    injected = 0
    out = list(edges)
    for src, outs in by_src.items():
        if src not in cells_by_idx or not mitosis_ready(_vol_key(cells_by_idx[src])):
            continue
        outs = sorted(outs, key=lambda e: -e[2])[:2]
        if len(outs) < 2:
            continue
        for e in outs:
            key = (e[0], e[1])
            if key not in existing:
                out.append(e)
                existing.add(key)
                injected += 1
    if injected:
        print(f"[FSOT-MITOSIS] injected {injected} division edges")
    return out


def _fsot_fuse_edges(
    coords: np.ndarray,
    ml_edges: list[tuple[int, int, float, float]],
    mode: str,
) -> list[tuple[int, int, float, float]]:
    from fsot_cellular_bridge import (
        BASE_CELL_VOL_UM3,
        _edge_threshold,
        estimate_volumes_for_frame,
        link_coords_fsot,
        link_edge_prob_refined,
        phys_coords,
    )

    default_vol = float(os.environ.get("FSOT_DEFAULT_VOL_UM3", str(BASE_CELL_VOL_UM3)))
    fsot_edges = link_coords_fsot(coords, default_vol=default_vol)

    cells_by_idx: dict[int, dict] = {}
    by_t: dict[int, list[int]] = {}
    for idx, row in enumerate(coords):
        cells_by_idx[idx] = {
            "z": float(row[1]), "y": float(row[2]), "x": float(row[3]),
            "physical_volume": default_vol, "vol": default_vol,
        }
        by_t.setdefault(int(row[0]), []).append(idx)
    for indices in by_t.values():
        estimate_volumes_for_frame([cells_by_idx[i] for i in indices], base_vol=default_vol)

    refined: dict[tuple[int, int], float] = {}
    for s, t, _p, _d in ml_edges:
        if s not in cells_by_idx or t not in cells_by_idx:
            continue
        p = cells_by_idx[s]
        c = cells_by_idx[t]
        d_um = float(np.linalg.norm(phys_coords([c])[0] - phys_coords([p])[0]))
        refined[(s, t)] = link_edge_prob_refined(
            d_um, p.get("vol", default_vol), c.get("vol", default_vol)
        )

    fsot_prob = {(s, t): p for s, t, p, _ in fsot_edges}
    thr = _edge_threshold()
    gate_frac = float(os.environ.get("FSOT_GATE_FRAC", "0.48"))
    gate_base = thr * gate_frac
    adaptive = os.environ.get("FSOT_GATE_ADAPTIVE", "0") == "1"
    rescue_fsot = os.environ.get("FSOT_GATE_RESCUE", "0") == "1"
    ml_w = float(os.environ.get("FSOT_GATE_ML_WEIGHT", "0.55"))
    fsot_w = float(os.environ.get("FSOT_GATE_FSOT_WEIGHT", "0.45"))

    if mode == "fsot_gate":
        soft_gate = os.environ.get("FSOT_GATE_SOFT", "0") == "1"
        soft_frac = float(os.environ.get("FSOT_GATE_SOFT_FRAC", "0.55"))
        ml_keep_min = float(os.environ.get("FSOT_GATE_ML_KEEP", "0.32"))
        edges: list[tuple[int, int, float, float]] = []
        kept_ml = 0
        for s, t, p, d in ml_edges:
            fp = refined.get((s, t), fsot_prob.get((s, t), 0.0))
            gate = gate_base * (1.0 - 0.45 * min(max(p, 0.0), 1.0)) if adaptive else gate_base
            soft_thr = gate_base * soft_frac
            keep = fp >= gate or (adaptive and p >= 0.65 and fp >= gate_base * 0.55)
            if soft_gate and not keep:
                keep = fp >= soft_thr or p >= ml_keep_min
            if keep:
                fsot_factor = max(fp, 1e-6) ** fsot_w
                if soft_gate and fp < gate:
                    fsot_factor = (max(fp, 1e-6) / max(gate, 1e-6)) ** fsot_w * 0.85
                score = (p ** ml_w) * fsot_factor
                edges.append((s, t, score, d))
                kept_ml += 1

        if rescue_fsot:
            rescue_min = thr * float(os.environ.get("FSOT_RESCUE_MIN_FRAC", "1.15"))
            ml_pairs = {(s, t) for s, t, _, _ in ml_edges}
            rescued = 0
            for s, t, fp, d in fsot_edges:
                if (s, t) in ml_pairs or fp < rescue_min:
                    continue
                edges.append((s, t, fp * 0.9, d))
                rescued += 1
        else:
            rescued = 0

        edges = _inject_fsot_mitosis_edges(coords, edges, fsot_edges)

        print(
            f"[FSOT-GATE] fsot={len(fsot_edges)} ml={len(ml_edges)} "
            f"kept_ml={kept_ml} rescued={rescued} gate_base={gate_base:.3f}"
        )
        return edges

    fused: dict[tuple[int, int], tuple[int, int, float, float]] = {}
    for s, t, p, d in fsot_edges:
        fused[(s, t)] = (s, t, p, d)
    for s, t, p, d in ml_edges:
        fp = refined.get((s, t), fsot_prob.get((s, t), 0.0))
        if fp < gate_base:
            continue
        score = (p ** 0.55) * (max(fp, 1e-6) ** 0.45)
        if (s, t) not in fused or score > fused[(s, t)][2]:
            fused[(s, t)] = (s, t, score, d)
    edges = list(fused.values())
    print(f"[HYBRID] fsot={len(fsot_edges)} ml={len(ml_edges)} fused={len(edges)} gate={gate_base:.3f}")
    return edges


def _link_mode() -> str:
    return os.environ.get("FSOT_LINK_MODE", "fsot_gate").lower()


def link_coords_with_fsot(
    coords: np.ndarray,
) -> list[tuple[int, int, float, float]]:
    """Build temporal edges with FSOT scalar costs (fsot_cellular_bridge.SequenceTracker)."""
    from fsot_cellular_bridge import BASE_CELL_VOL_UM3, link_coords_fsot

    default_vol = float(os.environ.get("FSOT_DEFAULT_VOL_UM3", str(BASE_CELL_VOL_UM3)))
    return link_coords_fsot(coords, default_vol=default_vol)


def _merge_edge_lists(
    primary: list[tuple[int, int, float, float]],
    secondary: list[tuple[int, int, float, float]],
) -> list[tuple[int, int, float, float]]:
    """Union edge lists; keep higher-probability edge on duplicate (src, tgt) pairs."""
    best: dict[tuple[int, int], tuple[int, int, float, float]] = {}
    for s, t, prob, dist in primary:
        best[(s, t)] = (s, t, prob, dist)
    for s, t, prob, dist in secondary:
        key = (s, t)
        if key not in best or prob > best[key][2]:
            best[key] = (s, t, prob, dist)
    return list(best.values())


@torch.no_grad()
def predict_coords_only(
    model,
    ds_path: Path,
    device: torch.device,
    cfg: PredictConfig,
    window_size: int = 2,
    max_frames: int | None = None,
    downsample: tuple[int, ...] = (1, 4, 4),
) -> np.ndarray:
    """U-Net detection only — skips transformer edge inference (faster fsot link path)."""
    import torch.nn.functional as F
    import zarr
    from tqdm import tqdm

    from dataspec import INTERACTIVE  # noqa: E402

    ds = open_dataset(ds_path, normalize=False, load_image=False, downsample=downsample)
    if "0.001" not in ds.quantiles or "0.999" not in ds.quantiles:
        raise ValueError(f"Zarr attrs missing image_statistics.quantiles for {ds_path}")
    zarr_arr = zarr.open_group(str(ds.zarr_path), mode="r")["0"]
    q_low = float(ds.quantiles["0.001"])
    q_high = float(ds.quantiles["0.999"])

    T = ds.image_shape[0] if max_frames is None else min(ds.image_shape[0], max_frames)
    target_shape = list(ds.image_shape[1:])
    ds_arr = np.array(downsample, dtype=np.float32)
    W = window_size
    voxel_size = tuple(s * d for s, d in zip(ds.scale, downsample))
    pool_k = pool_kernel_from_um(cfg.pool_kernel_um, voxel_size)

    collect_conf = _want_det_conf()
    seen_frames: set[int] = set()
    coord_lists: list[np.ndarray] = []
    conf_lists: list[np.ndarray] = []
    stride = max(W - 1, 1)
    window_starts = list(range(0, T - W + 1, stride))
    if not window_starts or window_starts[-1] + W < T:
        last = max(T - W, 0)
        if not window_starts or last != window_starts[-1]:
            window_starts.append(last)

    for ws in tqdm(window_starts, desc="  detect", leave=False, disable=not INTERACTIVE):
        frame_indices = list(range(ws, ws + W))
        imgs = torch.stack([
            _load_frame(zarr_arr, t, target_shape, downsample) for t in frame_indices
        ])
        imgs = ((imgs - q_low) / (q_high - q_low + 1e-6)).clamp(0.0)
        imgs = imgs.unsqueeze(0).to(device)

        _unet_out, det_logits = model.encode(imgs)
        if cfg.det_tta:
            for dims in [(-1,), (-2,), (-2, -1)]:
                imgs_flip = imgs.flip(dims)
                _, det_flip = model.encode(imgs_flip)
                for f in range(W):
                    det_logits[f] = det_logits[f] + det_flip[f].flip(dims)
            for f in range(W):
                det_logits[f] = det_logits[f] / 4

        for f_idx, t in enumerate(frame_indices):
            if t not in seen_frames:
                if collect_conf:
                    arr, conf = _detect_cells_pooled_scored(
                        det_logits[f_idx][0], t, cfg.det_threshold, pool_k,
                    )
                    conf_lists.append(conf)
                else:
                    arr = _detect_cells_pooled(
                        det_logits[f_idx][0], t, cfg.det_threshold, pool_k,
                    )
                coord_lists.append(arr)
                seen_frames.add(t)
        del imgs, _unet_out, det_logits

    coords = np.concatenate(coord_lists) if coord_lists else np.empty((0, 4), dtype=np.int16)
    det_conf = np.concatenate(conf_lists) if conf_lists else None
    coords = coords.astype(np.float32)
    coords[:, 1:] *= ds_arr
    coords = coords.astype(np.int16)
    if det_conf is not None and len(det_conf) > 0:
        print(
            f"[DET-CONF] mean={det_conf.mean():.3f} "
            f"p50={np.median(det_conf):.3f} max={det_conf.max():.3f}"
        )
    before = len(coords)
    coords = _postprocess_coords(coords, det_conf=det_conf)
    if before != len(coords):
        print(f"[DETECT] NMS/topk: {before} -> {len(coords)} nodes (nms_um={_nms_min_um()})")
    return coords


def _pool_kernel_um(weights: Path) -> float:
    env = os.environ.get("CELLMOT_POOL_UM")
    if env:
        return float(env)
    cfg_path = weights.parent / "config.json"
    if cfg_path.exists():
        return float(json.loads(cfg_path.read_text()).get("pool_kernel_um", 8.0))
    return float(os.environ.get("CELLMOT_POOL_UM", "8.0"))


def _resolve_weights(path: str | Path | None = None) -> Path:
    if path:
        p = Path(path)
        if p.exists():
            return p
    env = os.environ.get("CELLMOT_UNET_WEIGHTS")
    if env and Path(env).exists():
        return Path(env)
    if os.environ.get("CELLMOT_USE_FT", "1") != "0" and FT_WEIGHTS.exists():
        return FT_WEIGHTS
    if BASELINE_WEIGHTS.exists():
        return BASELINE_WEIGHTS
    hits = list(ROOT.glob("**/edge_predictor_best.pth"))
    if hits:
        return hits[0]
    raise FileNotFoundError(
        "U-Net weights not found. Download aashishnegi23/cellmot-ft-detector-biohub or "
        "thibautgoldsborough/cellmot-baseline-artifacts, or set CELLMOT_UNET_WEIGHTS."
    )


def _build_config(weights: Path, ds_path: Path | None = None) -> PredictConfig:
    det_thr = float(os.environ.get("CELLMOT_DET_THRESHOLD", "0.55"))
    if ds_path is not None and os.environ.get("FSOT_VISION_CALIBRATE", "1") == "1":
        try:
            from fsot_vision_calibrate import apply_fsot_vision_calibrate

            det_thr = apply_fsot_vision_calibrate(ds_path)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] FSOT vision calibrate skipped: {exc}")
    return PredictConfig(
        det_threshold=det_thr,
        det_tta=os.environ.get("CELLMOT_DET_TTA", "1") == "1",
        pool_kernel_um=_pool_kernel_um(weights),
        edge_activation=os.environ.get("CELLMOT_EDGE_ACTIVATION", "softmax"),
        threshold=float(os.environ.get("CELLMOT_EDGE_THRESHOLD", "0.3")),
        use_ilp=os.environ.get("CELLMOT_USE_ILP", "1") == "1",
        ilp_edge_weight=float(os.environ.get("CELLMOT_ILP_EDGE_WEIGHT", "-1.0")),
        ilp_appearance_weight=float(os.environ.get("CELLMOT_ILP_APPEARANCE", "0.1")),
        ilp_disappearance_weight=float(os.environ.get("CELLMOT_ILP_DISAPPEARANCE", "0.1")),
        ilp_division_weight=float(os.environ.get("CELLMOT_ILP_DIVISION", "1.0")),
    )


@contextlib.contextmanager
def _suppress_output():
    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            yield


def _ilp_edge_cap() -> int:
    """Skip full ILP above this edge count — use CPU lite consistency instead."""
    return int(os.environ.get("CELLMOT_ILP_MAX_EDGES", "35000"))


def _lite_consistency_enabled() -> bool:
    mode = os.environ.get("CELLMOT_GRAPH_CONSISTENCY", "auto").lower()
    if mode in ("0", "off", "none"):
        return False
    if mode in ("lite", "greedy", "1", "on"):
        return True
    # auto: lite fallback whenever ILP is off or skipped (Kaggle CPU default path)
    return True


def _greedy_track_consistency(graph: td.graph.InMemoryGraph) -> td.graph.InMemoryGraph:
    """
    CPU-fast track consistency: one parent per child, max two daughters per parent.
    Mimics the main benefit of tracksdata ILP without SCIP solve time.
    """
    from collections import defaultdict

    if graph.num_edges() == 0:
        return graph

    k = td.DEFAULT_ATTR_KEYS
    attr_keys = [k.EDGE_SOURCE, k.EDGE_TARGET]
    has_prob = "edge_prob" in graph.edge_attr_keys()
    has_dist = "edge_dist" in graph.edge_attr_keys()
    if has_prob:
        attr_keys.append("edge_prob")
    if has_dist:
        attr_keys.append("edge_dist")
    edges_tbl = graph.edge_attrs(attr_keys=attr_keys)
    srcs = edges_tbl[k.EDGE_SOURCE].to_list()
    tgts = edges_tbl[k.EDGE_TARGET].to_list()
    probs = (
        edges_tbl["edge_prob"].to_list()
        if has_prob
        else [1.0] * len(srcs)
    )
    dists = (
        edges_tbl["edge_dist"].to_list()
        if has_dist
        else [0.0] * len(srcs)
    )

    ranked = sorted(
        zip(srcs, tgts, probs, dists, strict=True),
        key=lambda row: -float(row[2]),
    )
    parent_of: dict[int, int] = {}
    child_count: dict[int, int] = defaultdict(int)
    kept: list[tuple[int, int, float, float]] = []
    for src, tgt, prob, dist in ranked:
        src_i, tgt_i = int(src), int(tgt)
        if tgt_i in parent_of or child_count[src_i] >= 2:
            continue
        parent_of[tgt_i] = src_i
        child_count[src_i] += 1
        kept.append((src_i, tgt_i, float(prob), float(dist)))

    if not kept:
        return graph

    used_nodes = {nid for edge in kept for nid in edge[:2]}
    nodes_tbl = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"]).sort(
        [k.T, "z", "y", "x", k.NODE_ID],
    )
    import polars as pl

    node_rows = nodes_tbl.filter(pl.col(k.NODE_ID).is_in(list(used_nodes)))
    old_to_new = {
        int(nid): idx
        for idx, nid in enumerate(node_rows[k.NODE_ID].to_list())
    }
    coords = np.array(
        [
            [int(row[k.T]), int(round(row["z"])), int(round(row["y"])), int(round(row["x"]))]
            for row in node_rows.iter_rows(named=True)
        ],
        dtype=np.int16,
    )
    remapped = [
        (old_to_new[s], old_to_new[t], p, d)
        for s, t, p, d in kept
        if s in old_to_new and t in old_to_new
    ]
    before_n, before_e = graph.num_nodes(), graph.num_edges()
    out = build_graph(coords, remapped)
    print(
        f"[LITE-CONSISTENCY] {before_n} nodes/{before_e} edges -> "
        f"{out.num_nodes()} nodes/{out.num_edges()} edges"
    )
    return out


def _apply_ilp(graph: td.graph.InMemoryGraph, cfg: PredictConfig) -> td.graph.InMemoryGraph:
    if not cfg.use_ilp or graph.num_edges() == 0:
        return graph
    cap = _ilp_edge_cap()
    if graph.num_edges() > cap:
        print(
            f"[ILP] skipped: {graph.num_edges()} edges > cap {cap} "
            "(set CELLMOT_ILP_MAX_EDGES to override)"
        )
        return graph
    try:
        solver = td.solvers.ILPSolver(
            edge_weight=cfg.ilp_edge_weight * td.EdgeAttr("edge_prob"),
            appearance_weight=cfg.ilp_appearance_weight,
            disappearance_weight=cfg.ilp_disappearance_weight,
            division_weight=cfg.ilp_division_weight,
        )
        with _suppress_output():
            solved = solver.solve(graph)
        return solved.detach() if hasattr(solved, "detach") else solved
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] ILP post-processing skipped: {exc}")
        return graph


def _patch_ml_division_post_ilp(
    graph: td.graph.InMemoryGraph,
    coords: np.ndarray,
    model,
    device: torch.device,
    cfg: PredictConfig,
    ds_path: Path,
    downsample: tuple[int, ...],
) -> td.graph.InMemoryGraph:
    """Fix mislinked parents on ML-refine frames using transformer argmax after ILP."""
    if os.environ.get("FSOT_ML_POST_ILP_CORRECT", "1") != "1":
        return graph
    from fsot_cellular_bridge import MITOSIS_DAUGHTER_MAX_UM, phys_coords
    from fsot_division_ml_refine import (
        _idx_by_time,
        _ml_edge_probs,
        _parse_frame_list,
        _refine_edge_threshold,
    )

    refine_frames = _parse_frame_list("FSOT_ML_REFINE_FRAMES")
    if not refine_frames:
        return graph

    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"])
    pos_to_gid: dict[tuple[int, int, int, int], int] = {}
    gid_to_t: dict[int, int] = {}
    for row in nodes.iter_rows(named=True):
        gid = int(row[k.NODE_ID])
        gid_to_t[gid] = int(row[k.T])
        key = (
            int(row[k.T]),
            int(round(row["z"])),
            int(round(row["y"])),
            int(round(row["x"])),
        )
        pos_to_gid[key] = gid

    coord_to_gid = {
        i: pos_to_gid.get((
            int(coords[i, 0]), int(coords[i, 1]),
            int(coords[i, 2]), int(coords[i, 3]),
        ))
        for i in range(len(coords))
    }
    gid_to_coord = {gid: i for i, gid in coord_to_gid.items() if gid is not None}

    edge_keys = [k.EDGE_ID, k.EDGE_SOURCE, k.EDGE_TARGET]
    if "edge_prob" in graph.edge_attr_keys():
        edge_keys.append("edge_prob")
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    by_t = _idx_by_time(coords)
    min_prob = float(os.environ.get("FSOT_ML_CORRECT_MIN_PROB", "0.25"))
    margin = float(os.environ.get("FSOT_ML_CORRECT_MARGIN", "0.06"))
    removed = 0
    to_add: list[dict] = []

    for t_src in sorted(refine_frames):
        t_tgt = t_src + 1
        idx_src = by_t.get(t_src, [])
        idx_tgt = by_t.get(t_tgt, [])
        if not idx_src or not idx_tgt:
            continue
        probs = _ml_edge_probs(
            model, device, cfg, Path(ds_path), coords,
            idx_src, idx_tgt, t_src, t_tgt, downsample,
        )
        if probs is None:
            continue
        gid_to_i = {coord_to_gid[idx_src[i]]: i for i in range(len(idx_src))
                    if coord_to_gid.get(idx_src[i]) is not None}
        c_src = coords[idx_src]
        c_tgt = coords[idx_tgt]
        pc_src = phys_coords([
            {"z": float(c[1]), "y": float(c[2]), "x": float(c[3])} for c in c_src
        ])
        pc_tgt = phys_coords([
            {"z": float(c[1]), "y": float(c[2]), "x": float(c[3])} for c in c_tgt
        ])

        for src_gid, i in gid_to_i.items():
            row = probs[i]
            j_best = int(np.argmax(row))
            best_prob = float(row[j_best])
            lowconf_thr = float(os.environ.get("FSOT_ML_CORRECT_LOWCONF", "0.0"))
            if best_prob < max(min_prob, _refine_edge_threshold(cfg)) and lowconf_thr <= 0:
                continue
            best_gid = coord_to_gid.get(idx_tgt[j_best])
            if best_gid is None:
                continue
            if float(np.linalg.norm(pc_src[i] - pc_tgt[j_best])) > MITOSIS_DAUGHTER_MAX_UM * 1.2:
                continue

            out_rows = edge_tbl.filter(edge_tbl[k.EDGE_SOURCE] == src_gid)
            cur_tgts: list[tuple[int, int]] = []
            for row in out_rows.iter_rows(named=True):
                tgt_gid = int(row[k.EDGE_TARGET])
                if gid_to_t.get(tgt_gid, -9) != t_tgt:
                    continue
                cur_tgts.append((int(row[k.EDGE_ID]), tgt_gid))

            if not cur_tgts:
                continue

            if any(tgt == best_gid for _, tgt in cur_tgts):
                continue

            cur_prob = 0.0
            for _, tgt in cur_tgts:
                ci = gid_to_coord.get(tgt)
                if ci is not None and ci in idx_tgt:
                    jj = idx_tgt.index(ci)
                    cur_prob = max(cur_prob, float(probs[i, jj]))
            if best_prob < lowconf_thr and lowconf_thr > 0:
                dists = [float(np.linalg.norm(pc_src[i] - pc_tgt[j])) for j in range(len(idx_tgt))]
                j_near = int(np.argmin(dists))
                if float(np.min(dists)) <= MITOSIS_DAUGHTER_MAX_UM:
                    j_best = j_near
                    best_prob = float(row[j_best])
                    best_gid = coord_to_gid.get(idx_tgt[j_best])
                    if best_gid is None or any(tgt == best_gid for _, tgt in cur_tgts):
                        continue
            elif best_prob < cur_prob + margin:
                continue

            for eid, _ in cur_tgts:
                graph.remove_edge(edge_id=eid)
                removed += 1
            dist = float(np.linalg.norm(
                c_src[i, 1:].astype(np.float32) - c_tgt[j_best, 1:].astype(np.float32)
            ))
            to_add.append({
                "source_id": src_gid,
                "target_id": best_gid,
                "edge_prob": best_prob,
                "edge_dist": dist,
            })

    if not to_add and removed == 0:
        return graph
    import polars as pl

    if to_add:
        if "edge_prob" not in graph.edge_attr_keys():
            graph.add_edge_attr_key("edge_prob", pl.Float64, 0.0)
            graph.add_edge_attr_key("edge_dist", pl.Float64, 0.0)
        graph.bulk_add_edges(to_add)
    print(
        f"[ML-REFINE] post-ILP correct removed={removed} added={len(to_add)}"
    )
    return graph


def _patch_preserved_fsot_edges(
    graph: td.graph.InMemoryGraph,
    coords: np.ndarray,
    preserve_edges: list[tuple[int, int, float, float]],
) -> td.graph.InMemoryGraph:
    """Re-attach pre-ILP FSOT edges on frames that ML replace must not disturb."""
    if not preserve_edges:
        return graph
    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"])
    pos_to_id: dict[tuple[int, int, int, int], int] = {}
    for row in nodes.iter_rows(named=True):
        key = (
            int(row[k.T]),
            int(round(row["z"])),
            int(round(row["y"])),
            int(round(row["x"])),
        )
        pos_to_id[key] = int(row[k.NODE_ID])

    edge_tbl = graph.edge_attrs(attr_keys=[k.EDGE_SOURCE, k.EDGE_TARGET])
    existing = {
        (int(row[k.EDGE_SOURCE]), int(row[k.EDGE_TARGET]))
        for row in edge_tbl.iter_rows(named=True)
    }
    node_t = {
        int(row[k.NODE_ID]): int(row[k.T])
        for row in nodes.iter_rows(named=True)
    }
    to_add: list[dict] = []
    for src_i, tgt_i, prob, dist in preserve_edges:
        if src_i >= len(coords) or tgt_i >= len(coords):
            continue
        s_key = (
            int(coords[src_i, 0]),
            int(coords[src_i, 1]),
            int(coords[src_i, 2]),
            int(coords[src_i, 3]),
        )
        t_key = (
            int(coords[tgt_i, 0]),
            int(coords[tgt_i, 1]),
            int(coords[tgt_i, 2]),
            int(coords[tgt_i, 3]),
        )
        src_id = pos_to_id.get(s_key)
        tgt_id = pos_to_id.get(t_key)
        if src_id is None or tgt_id is None:
            continue
        if (src_id, tgt_id) in existing:
            continue
        to_add.append({
            "source_id": src_id,
            "target_id": tgt_id,
            "edge_prob": float(prob),
            "edge_dist": float(dist),
        })
        existing.add((src_id, tgt_id))

    if not to_add:
        return graph
    import polars as pl

    if "edge_prob" not in graph.edge_attr_keys():
        graph.add_edge_attr_key("edge_prob", pl.Float64, 0.0)
        graph.add_edge_attr_key("edge_dist", pl.Float64, 0.0)
    graph.bulk_add_edges(to_add)
    print(f"[ML-REFINE] post-ILP restored {len(to_add)} preserved FSOT edges")
    return graph


def _reconcile_preserve_daughters(
    graph: td.graph.InMemoryGraph,
    coords: np.ndarray,
    preserve_edges: list[tuple[int, int, float, float]],
    frames: set[int],
) -> td.graph.InMemoryGraph:
    """On preserved frames, drop extra daughters; keep best FSOT-prob daughter per parent."""
    if not preserve_edges or not frames:
        return graph
    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"])
    pos_to_gid: dict[tuple[int, int, int, int], int] = {}
    gid_t: dict[int, int] = {}
    for row in nodes.iter_rows(named=True):
        gid = int(row[k.NODE_ID])
        gid_t[gid] = int(row[k.T])
        pos_to_gid[(int(row[k.T]), int(round(row["z"])), int(round(row["y"])), int(round(row["x"])))] = gid

    fsot_best: dict[int, tuple[int, float]] = {}
    for src_i, tgt_i, prob, _ in preserve_edges:
        if int(coords[src_i, 0]) not in frames:
            continue
        cur = fsot_best.get(src_i)
        if cur is None or prob > cur[1]:
            fsot_best[src_i] = (tgt_i, float(prob))

    coord_to_gid = {
        i: pos_to_gid.get((
            int(coords[i, 0]), int(coords[i, 1]), int(coords[i, 2]), int(coords[i, 3]),
        ))
        for i in range(len(coords))
    }
    prefer_gid: dict[int, int] = {}
    for src_i, (tgt_i, _) in fsot_best.items():
        g_src = coord_to_gid.get(src_i)
        g_tgt = coord_to_gid.get(tgt_i)
        if g_src is not None and g_tgt is not None:
            prefer_gid[g_src] = g_tgt

    edge_keys = [k.EDGE_ID, k.EDGE_SOURCE, k.EDGE_TARGET]
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    by_parent: dict[int, list[tuple[int, int]]] = {}
    for row in edge_tbl.iter_rows(named=True):
        src = int(row[k.EDGE_SOURCE])
        tgt = int(row[k.EDGE_TARGET])
        if gid_t.get(src, -9) not in frames or gid_t.get(tgt, -9) != gid_t.get(src, -9) + 1:
            continue
        by_parent.setdefault(src, []).append((int(row[k.EDGE_ID]), tgt))

    removed = 0
    for src, outs in by_parent.items():
        if len(outs) <= 1:
            continue
        keep_tgt = prefer_gid.get(src)
        if keep_tgt is None:
            continue
        for eid, tgt in outs:
            if tgt != keep_tgt:
                graph.remove_edge(edge_id=eid)
                removed += 1
    if removed:
        print(f"[ML-REFINE] reconcile dropped {removed} extra daughters on frames {sorted(frames)}")
    return graph


def _patch_nearest_daughter_post_ilp(
    graph: td.graph.InMemoryGraph,
    coords: np.ndarray,
    frames: set[int],
) -> td.graph.InMemoryGraph:
    """Swap mislinked daughters when a nearer cell exists (division frames only)."""
    if os.environ.get("FSOT_ML_NEAREST_DAUGHTER", "1") != "1" or not frames:
        return graph
    from fsot_cellular_bridge import MITOSIS_DAUGHTER_MAX_UM, phys_coords

    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"])
    gid_pos: dict[int, np.ndarray] = {}
    gid_t: dict[int, int] = {}
    pos_to_gid: dict[tuple[int, int, int, int], int] = {}
    for row in nodes.iter_rows(named=True):
        gid = int(row[k.NODE_ID])
        gid_t[gid] = int(row[k.T])
        pos = np.array([float(row["z"]), float(row["y"]), float(row["x"])], dtype=np.float32)
        gid_pos[gid] = pos
        pos_to_gid[(int(row[k.T]), int(round(row["z"])), int(round(row["y"])), int(round(row["x"])))] = gid

    coord_gid = {
        i: pos_to_gid.get((
            int(coords[i, 0]), int(coords[i, 1]), int(coords[i, 2]), int(coords[i, 3]),
        ))
        for i in range(len(coords))
    }
    by_t: dict[int, list[int]] = {}
    for i, gid in coord_gid.items():
        if gid is None:
            continue
        by_t.setdefault(int(coords[i, 0]), []).append(i)

    edge_keys = [k.EDGE_ID, k.EDGE_SOURCE, k.EDGE_TARGET]
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    swapped = 0
    to_add: list[dict] = []

    for t_src in sorted(frames):
        t_tgt = t_src + 1
        tgt_gids = [
            coord_gid[i] for i in by_t.get(t_tgt, [])
            if coord_gid.get(i) is not None
        ]
        if not tgt_gids:
            continue
        tgt_phys = {
            g: phys_coords([{"z": gid_pos[g][0], "y": gid_pos[g][1], "x": gid_pos[g][2]}])[0]
            for g in tgt_gids
        }

        by_parent: dict[int, list[tuple[int, int]]] = {}
        for row in edge_tbl.iter_rows(named=True):
            src = int(row[k.EDGE_SOURCE])
            tgt = int(row[k.EDGE_TARGET])
            if gid_t.get(src) != t_src or gid_t.get(tgt) != t_tgt:
                continue
            by_parent.setdefault(src, []).append((int(row[k.EDGE_ID]), tgt))

        for src, outs in by_parent.items():
            if len(outs) != 1 or src not in gid_pos:
                continue
            eid, cur_tgt = outs[0]
            p_phys = phys_coords([{
                "z": gid_pos[src][0], "y": gid_pos[src][1], "x": gid_pos[src][2],
            }])[0]
            nearest_gid = min(
                tgt_gids,
                key=lambda g: float(np.linalg.norm(p_phys - tgt_phys[g])),
            )
            if nearest_gid == cur_tgt:
                continue
            cur_d = float(np.linalg.norm(p_phys - tgt_phys[cur_tgt]))
            near_d = float(np.linalg.norm(p_phys - tgt_phys[nearest_gid]))
            if near_d > MITOSIS_DAUGHTER_MAX_UM or near_d >= cur_d - 2.0:
                continue
            graph.remove_edge(edge_id=eid)
            dist = float(np.linalg.norm(gid_pos[src] - gid_pos[nearest_gid]))
            to_add.append({
                "source_id": src,
                "target_id": nearest_gid,
                "edge_prob": 0.95,
                "edge_dist": dist,
            })
            swapped += 1

    if not to_add:
        return graph
    import polars as pl

    if "edge_prob" not in graph.edge_attr_keys():
        graph.add_edge_attr_key("edge_prob", pl.Float64, 0.0)
        graph.add_edge_attr_key("edge_dist", pl.Float64, 0.0)
    graph.bulk_add_edges(to_add)
    print(f"[ML-REFINE] nearest-daughter swapped {swapped} edges on frames {sorted(frames)}")
    return graph


def _prune_multi_daughter_edges(
    graph: td.graph.InMemoryGraph,
    frames: set[int],
) -> td.graph.InMemoryGraph:
    """Drop weaker second daughters on preserved frames (reduces spurious FP links)."""
    if not frames:
        return graph
    k = td.DEFAULT_ATTR_KEYS
    edge_keys = [k.EDGE_ID, k.EDGE_SOURCE, k.EDGE_TARGET]
    if "edge_prob" in graph.edge_attr_keys():
        edge_keys.append("edge_prob")
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T])
    node_t = {int(row[k.NODE_ID]): int(row[k.T]) for row in nodes.iter_rows(named=True)}

    by_parent: dict[int, list[tuple[int, int, float]]] = {}
    for row in edge_tbl.iter_rows(named=True):
        src = int(row[k.EDGE_SOURCE])
        tgt = int(row[k.EDGE_TARGET])
        t_src = node_t.get(src, -9)
        t_tgt = node_t.get(tgt, -9)
        if t_src not in frames or t_tgt != t_src + 1:
            continue
        prob = float(row["edge_prob"]) if "edge_prob" in row else 1.0
        by_parent.setdefault(src, []).append((int(row[k.EDGE_ID]), tgt, prob))

    removed = 0
    for src, outs in by_parent.items():
        if len(outs) <= 1:
            continue
        outs.sort(key=lambda x: -x[2])
        for eid, _, _ in outs[1:]:
            graph.remove_edge(edge_id=eid)
            removed += 1
    if removed:
        print(f"[ML-REFINE] pruned {removed} secondary daughter edges on frames {sorted(frames)}")
    return graph


def _snapshot_pre_ilp_parents(
    graph: td.graph.InMemoryGraph,
    frames: set[int],
) -> set[int]:
    """Parents on ``frames`` with a t->t+1 edge in the pre-ILP graph."""
    if not frames:
        return set()
    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T])
    gid_t = {int(row[k.NODE_ID]): int(row[k.T]) for row in nodes.iter_rows(named=True)}
    parents: set[int] = set()
    edge_tbl = graph.edge_attrs(attr_keys=[k.EDGE_SOURCE, k.EDGE_TARGET])
    for row in edge_tbl.iter_rows(named=True):
        src = int(row[k.EDGE_SOURCE])
        tgt = int(row[k.EDGE_TARGET])
        t_src = gid_t.get(src, -9)
        t_tgt = gid_t.get(tgt, -9)
        if t_src in frames and t_tgt == t_src + 1:
            parents.add(src)
    return parents


def _patch_division_gap_post_ilp(
    graph: td.graph.InMemoryGraph,
    preserve_frames: set[int],
    refine_frames: set[int],
    *,
    pre_ilp_parents: set[int] | None = None,
) -> td.graph.InMemoryGraph:
    """Surgical division fixes after ILP: 2nd-daughter prune + pre-ILP orphan relink."""
    if os.environ.get("FSOT_ML_DIVISION_GAP_PATCH", "1") != "1":
        return graph
    from fsot_cellular_bridge import MITOSIS_DAUGHTER_MAX_UM, phys_coords

    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"])
    gid_t: dict[int, int] = {}
    gid_pos: dict[int, np.ndarray] = {}
    for row in nodes.iter_rows(named=True):
        gid = int(row[k.NODE_ID])
        gid_t[gid] = int(row[k.T])
        gid_pos[gid] = np.array([float(row["z"]), float(row["y"]), float(row["x"])])

    edge_keys = [k.EDGE_ID, k.EDGE_SOURCE, k.EDGE_TARGET]
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    by_parent: dict[int, list[tuple[int, int]]] = {}
    for row in edge_tbl.iter_rows(named=True):
        src = int(row[k.EDGE_SOURCE])
        tgt = int(row[k.EDGE_TARGET])
        t_src = gid_t.get(src, -9)
        t_tgt = gid_t.get(tgt, -9)
        if t_tgt != t_src + 1:
            continue
        by_parent.setdefault(src, []).append((int(row[k.EDGE_ID]), tgt))

    removed = 0
    for src, outs in by_parent.items():
        if len(outs) != 2 or gid_t.get(src, -9) not in preserve_frames:
            continue
        if src not in gid_pos:
            continue
        p_pos = gid_pos[src]

        def _dy(tgt_gid: int) -> float:
            return float(gid_pos[tgt_gid][1] - p_pos[1])

        keep_tgt = max((tgt for _, tgt in outs), key=_dy)
        for eid, tgt in outs:
            if tgt != keep_tgt:
                graph.remove_edge(edge_id=eid)
                removed += 1

    # Refresh after removals
    edge_tbl = graph.edge_attrs(attr_keys=edge_keys)
    by_parent = {}
    for row in edge_tbl.iter_rows(named=True):
        src = int(row[k.EDGE_SOURCE])
        tgt = int(row[k.EDGE_TARGET])
        t_src = gid_t.get(src, -9)
        t_tgt = gid_t.get(tgt, -9)
        if t_tgt != t_src + 1:
            continue
        by_parent.setdefault(src, []).append((int(row[k.EDGE_ID]), tgt))

    tgt_by_frame: dict[int, list[int]] = {}
    for gid, t in gid_t.items():
        tgt_by_frame.setdefault(t, []).append(gid)

    relink_parents = pre_ilp_parents or set()
    to_add: list[dict] = []
    linked = 0
    for t_src in sorted(refine_frames):
        t_tgt = t_src + 1
        for src in sorted(relink_parents):
            if gid_t.get(src, -9) != t_src:
                continue
            if src in by_parent and by_parent[src]:
                continue
            if src not in gid_pos:
                continue
            p_phys = phys_coords([{
                "z": gid_pos[src][0], "y": gid_pos[src][1], "x": gid_pos[src][2],
            }])[0]
            best_gid = None
            best_d = float("inf")
            for cand in tgt_by_frame.get(t_tgt, []):
                if cand not in gid_pos:
                    continue
                c_phys = phys_coords([{
                    "z": gid_pos[cand][0], "y": gid_pos[cand][1], "x": gid_pos[cand][2],
                }])[0]
                d_um = float(np.linalg.norm(p_phys - c_phys))
                if d_um <= MITOSIS_DAUGHTER_MAX_UM and d_um < best_d:
                    best_d = d_um
                    best_gid = cand
            if best_gid is None:
                continue
            dist = float(np.linalg.norm(gid_pos[src] - gid_pos[best_gid]))
            to_add.append({
                "source_id": src,
                "target_id": best_gid,
                "edge_prob": 0.92,
                "edge_dist": dist,
            })
            linked += 1

    if to_add:
        import polars as pl

        if "edge_prob" not in graph.edge_attr_keys():
            graph.add_edge_attr_key("edge_prob", pl.Float64, 0.0)
            graph.add_edge_attr_key("edge_dist", pl.Float64, 0.0)
        graph.bulk_add_edges(to_add)
    if removed or linked:
        print(
            f"[ML-REFINE] division-gap removed={removed} orphan-linked={linked} "
            f"frames preserve={sorted(preserve_frames)} refine={sorted(refine_frames)}"
        )
    return graph


def _apply_graph_postprocess(
    graph: td.graph.InMemoryGraph,
    cfg: PredictConfig,
    *,
    coords: np.ndarray | None = None,
    preserve_fsot_edges: list[tuple[int, int, float, float]] | None = None,
    ml_patch_ctx: tuple | None = None,
) -> td.graph.InMemoryGraph:
    """ILP when affordable; otherwise CPU lite greedy consistency (Kaggle-safe)."""
    before_n, before_e = graph.num_nodes(), graph.num_edges()
    pre_ilp_parents: set[int] | None = None
    if coords is not None:
        from fsot_division_ml_refine import _parse_frame_list

        refine_frames_for_snap = _parse_frame_list("FSOT_ML_REFINE_FRAMES")
        if refine_frames_for_snap:
            pre_ilp_parents = _snapshot_pre_ilp_parents(graph, refine_frames_for_snap)
    if cfg.use_ilp and graph.num_edges() <= _ilp_edge_cap():
        graph = _apply_ilp(graph, cfg)
        if graph.num_nodes() < before_n or graph.num_edges() < before_e:
            print(
                f"[ILP] {before_n} nodes/{before_e} edges -> "
                f"{graph.num_nodes()} nodes/{graph.num_edges()} edges"
            )
        if coords is not None:
            from fsot_division_ml_refine import _parse_frame_list
            preserve_frames = _parse_frame_list("FSOT_ML_PRESERVE_FSOT_FRAMES")
            refine_frames = _parse_frame_list("FSOT_ML_REFINE_FRAMES")
            if preserve_fsot_edges:
                graph = _patch_preserved_fsot_edges(graph, coords, preserve_fsot_edges)
            if preserve_frames or refine_frames:
                graph = _patch_division_gap_post_ilp(
                    graph,
                    preserve_frames,
                    refine_frames,
                    pre_ilp_parents=pre_ilp_parents,
                )
            if (
                preserve_fsot_edges
                and os.environ.get("FSOT_ML_RECONCILE_DAUGHTERS", "0") == "1"
                and preserve_frames
            ):
                graph = _reconcile_preserve_daughters(
                    graph, coords, preserve_fsot_edges, preserve_frames,
                )
        if coords is not None and ml_patch_ctx is not None:
            if os.environ.get("FSOT_ML_POST_ILP_CORRECT", "0") == "1":
                model, device, ds_path, downsample = ml_patch_ctx
                graph = _patch_ml_division_post_ilp(
                    graph, coords, model, device, cfg, ds_path, downsample,
                )
        return graph
    if cfg.use_ilp and graph.num_edges() > _ilp_edge_cap():
        print(
            f"[ILP] skipped: {graph.num_edges()} edges > cap {_ilp_edge_cap()} "
            "— using lite consistency"
        )
    if _lite_consistency_enabled():
        return _greedy_track_consistency(graph)
    return graph


def _configure_cpu_threads() -> None:
    """Respect Kaggle CPU thread caps (set OMP_NUM_THREADS in notebook)."""
    n = os.environ.get("OMP_NUM_THREADS") or os.environ.get("TORCH_NUM_THREADS")
    if n:
        try:
            torch.set_num_threads(int(n))
        except Exception:
            pass


def _pick_device(requested: str | None = None) -> torch.device:
    _configure_cpu_threads()
    if requested:
        return torch.device(requested)
    env = os.environ.get("CELLMOT_DEVICE")
    if env:
        return torch.device(env)
    if os.environ.get("KAGGLE_CPU_ONLY", "0") == "1" or os.path.exists("/kaggle/input"):
        return torch.device("cpu")
    if not torch.cuda.is_available():
        return torch.device("cpu")
    try:
        torch.relu(torch.randn(8, device="cuda"))
        return torch.device("cuda")
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] CUDA probe failed ({exc}); falling back to CPU")
        return torch.device("cpu")


_ENGINE_CACHE: tuple | None = None


def _load_engine(weights: Path | None = None, device: str | None = None):
    global _ENGINE_CACHE
    if _ENGINE_CACHE is not None and weights is None:
        return _ENGINE_CACHE
    weights = _resolve_weights(weights)
    dev = _pick_device(device)
    print(f"[UNET] device={dev}")
    model, window_size, downsample = load_model(weights, dev)
    cfg = _build_config(weights, ds_path=None)
    _ENGINE_CACHE = (model, cfg, window_size, downsample, dev, weights)
    return _ENGINE_CACHE


def predict_dataset(
    ds_path: str | Path,
    max_frames: int | None = None,
    weights: Path | None = None,
    return_graph: bool = False,
    link_mode: str | None = None,
) -> tuple[np.ndarray, list[tuple[int, int, float, float]]] | td.graph.InMemoryGraph:
    """Run U-Net detection + FSOT (or transformer) linking on one dataset."""
    model, cfg, window_size, downsample, device, wpath = _load_engine(weights)
    ds_path = Path(ds_path)
    if ds_path.suffix in (".zarr", ".geff"):
        ds_path = ds_path.parent / ds_path.stem

    cfg = _build_config(wpath, ds_path=ds_path)

    use_conf = _want_det_conf()
    conf_parts: list[np.ndarray] = [] if use_conf else []
    preserve_fsot_edges: list[tuple[int, int, float, float]] = []

    mode = (link_mode or _link_mode()).lower()
    if mode == "transformer":
        coords, edges = predict_video(
            model, ds_path, device, cfg,
            window_size=window_size, max_frames=max_frames, downsample=downsample,
            det_conf_parts=conf_parts if use_conf else None,
        )
        det_conf = np.concatenate(conf_parts) if conf_parts else None
        before = len(coords)
        coords, edges = _postprocess_coords_edges(coords, edges, det_conf=det_conf)
        if before != len(coords):
            print(f"[DETECT] NMS/topk: {before} -> {len(coords)} nodes (nms_um={_nms_min_um()})")
        print(f"[ML-EDGE] {len(edges)} transformer edges from {len(coords)} nodes")
    elif mode == "fsot_union":
        coords, ml_edges = predict_video(
            model, ds_path, device, cfg,
            window_size=window_size, max_frames=max_frames, downsample=downsample,
            det_conf_parts=conf_parts if use_conf else None,
        )
        det_conf = np.concatenate(conf_parts) if conf_parts else None
        before = len(coords)
        coords, ml_edges = _postprocess_coords_edges(coords, ml_edges, det_conf=det_conf)
        if before != len(coords):
            print(f"[DETECT] NMS/topk: {before} -> {len(coords)} nodes (nms_um={_nms_min_um()})")
        fsot_edges = link_coords_with_fsot(coords)
        edges = _merge_edge_lists(fsot_edges, ml_edges)
        print(
            f"[FSOT-UNION] fsot={len(fsot_edges)} ml={len(ml_edges)} "
            f"union={len(edges)} nodes={len(coords)}"
        )
    elif mode in ("hybrid", "fsot_gate"):
        coords, ml_edges = predict_video(
            model, ds_path, device, cfg,
            window_size=window_size, max_frames=max_frames, downsample=downsample,
            det_conf_parts=conf_parts if use_conf else None,
        )
        det_conf = np.concatenate(conf_parts) if conf_parts else None
        if det_conf is not None and len(det_conf) == len(coords):
            print(
                f"[DET-CONF] mean={det_conf.mean():.3f} "
                f"p50={np.median(det_conf):.3f} max={det_conf.max():.3f}"
            )
        before = len(coords)
        coords, ml_edges = _postprocess_coords_edges(coords, ml_edges, det_conf=det_conf)
        if before != len(coords):
            print(f"[DETECT] NMS/topk: {before} -> {len(coords)} nodes (nms_um={_nms_min_um()})")
        edges = _fsot_fuse_edges(coords, ml_edges, mode)
    else:
        coords = predict_coords_only(
            model, ds_path, device, cfg,
            window_size=window_size, max_frames=max_frames, downsample=downsample,
        )
        edges = link_coords_with_fsot(coords)
        if os.environ.get("FSOT_DIVISION_ML_REFINE", "0") == "1":
            from fsot_division_ml_refine import (
                _edges_on_frames,
                _parse_frame_list,
                refine_fsot_edges_ml,
            )

            preserve_frames = _parse_frame_list("FSOT_ML_PRESERVE_FSOT_FRAMES")
            if preserve_frames:
                preserve_fsot_edges = _edges_on_frames(coords, edges, preserve_frames)
            edges = refine_fsot_edges_ml(
                coords, edges, model, device, cfg, Path(ds_path),
                downsample=downsample, window_size=window_size,
            )
        print(f"[FSOT] {len(edges)} edges from {len(coords)} U-Net detections")

    if return_graph:
        return _apply_graph_postprocess(
            build_graph(coords, edges),
            cfg,
            coords=coords,
            preserve_fsot_edges=preserve_fsot_edges or None,
            ml_patch_ctx=(model, device, Path(ds_path), downsample),
        )
    return coords, edges


def predict_graph(
    ds_path: str | Path,
    max_frames: int | None = None,
    weights: Path | None = None,
) -> td.graph.InMemoryGraph:
    """Run U-Net inference and return a tracksdata graph (with optional ILP)."""
    return predict_dataset(ds_path, max_frames=max_frames, weights=weights, return_graph=True)


def graph_to_submission_rows_from_graph(
    graph: td.graph.InMemoryGraph,
    dataset_name: str,
    row_start: int = 0,
    node_id_start: int = 1,
) -> tuple[list[dict], int, int]:
    """Convert a tracksdata graph to Kaggle submission rows (matches geffs_to_csv)."""
    import polars as pl

    k = td.DEFAULT_ATTR_KEYS
    nodes = graph.node_attrs(attr_keys=[k.NODE_ID, k.T, "z", "y", "x"]).sort(
        [k.T, "z", "y", "x", k.NODE_ID],
    )
    graph_to_sub: dict[int, int] = {}
    rows: list[dict] = []
    row_idx = row_start
    sub_id = node_id_start
    for i in range(nodes.height):
        gid = int(nodes[k.NODE_ID][i])
        graph_to_sub[gid] = sub_id
        rows.append({
            "id": row_idx, "dataset": dataset_name, "row_type": "node",
            "node_id": sub_id, "t": int(nodes[k.T][i]),
            "z": int(round(nodes["z"][i])), "y": int(round(nodes["y"][i])),
            "x": int(round(nodes["x"][i])),
            "source_id": -1, "target_id": -1,
        })
        row_idx += 1
        sub_id += 1
    edges = graph.edge_attrs(attr_keys=[k.EDGE_SOURCE, k.EDGE_TARGET])
    edge_pairs = list(zip(
        edges[k.EDGE_SOURCE].to_list(), edges[k.EDGE_TARGET].to_list(), strict=True,
    ))
    seen_edges: set[tuple[int, int]] = set()
    for src, tgt in edge_pairs:
        sid, tid = graph_to_sub[int(src)], graph_to_sub[int(tgt)]
        if (sid, tid) in seen_edges:
            continue
        seen_edges.add((sid, tid))
        rows.append({
            "id": row_idx, "dataset": dataset_name, "row_type": "edge",
            "node_id": -1, "t": -1, "z": -1, "y": -1, "x": -1,
            "source_id": sid, "target_id": tid,
        })
        row_idx += 1
    return rows, row_idx, sub_id


def write_submission_csv(rows: list[dict], out_path: str | Path) -> Path:
    """Write submission CSV in official column order (polars, integer dtypes)."""
    import polars as pl

    out = Path(out_path)
    cols = [
        "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
    ]
    table = pl.DataFrame(rows).select(cols).with_row_index("id")
    table = table.select(
        "id", "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
    )
    table.write_csv(out)
    return out


def graph_to_submission_rows(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
    dataset_name: str,
    row_start: int = 0,
    node_id_start: int = 1,
) -> tuple[list[dict], int, int]:
    """Convert U-Net coords/edges to Kaggle submission rows."""
    rows: list[dict] = []
    row_idx = row_start
    node_ids = list(range(node_id_start, node_id_start + len(coords)))
    for i, (t, z, y, x) in enumerate(coords):
        rows.append({
            "id": row_idx, "dataset": dataset_name, "row_type": "node",
            "node_id": node_ids[i], "t": int(t),
            "z": int(round(z)), "y": int(round(y)), "x": int(round(x)),
            "source_id": -1, "target_id": -1,
        })
        row_idx += 1
    for src, tgt, _prob, _dist in edges:
        rows.append({
            "id": row_idx, "dataset": dataset_name, "row_type": "edge",
            "node_id": -1, "t": -1, "z": -1, "y": -1, "x": -1,
            "source_id": node_ids[src], "target_id": node_ids[tgt],
        })
        row_idx += 1
    return rows, row_idx, node_id_start + len(coords)


def benchmark_dataset(ds_path: str | Path, max_frames: int | None = 20) -> dict:
    """Score one train dataset against GT using official metrics."""
    ds_path = Path(ds_path)
    if ds_path.suffix in (".zarr", ".geff"):
        ds_path = ds_path.parent / ds_path.stem
    graph = predict_graph(ds_path, max_frames=max_frames)
    ds = open_dataset(ds_path, normalize=False, device="cpu", require_tracks=True)
    from geff import GeffMetadata

    geff = ds_path.parent / f"{ds_path.stem}.geff"
    n_total = float("nan")
    if geff.exists():
        try:
            val = (GeffMetadata.read(geff).extra or {}).get("estimated_number_of_nodes")
            n_total = float(val) if val is not None else float("nan")
        except Exception:
            pass
    er = evaluate(graph, ds.tracks, scale=SCALE)
    recall = node_recall(graph, ds.tracks) if graph.num_nodes() > 0 and graph.num_edges() > 0 else 0.0
    row = per_sample_metrics(er, n_total, recall)
    summary = summarise([row])
    return {
        "nodes": graph.num_nodes(),
        "edges": graph.num_edges(),
        "edge_jaccard": summary["edge_jaccard"],
        "adj_edge_jaccard": summary["adj_edge_jaccard"],
        "division_jaccard": summary["division_jaccard"],
        "node_recall": summary["node_recall"],
        "score": summary["score"],
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Benchmark U-Net engine on train data")
    ap.add_argument("--data-dir", default=r"D:\Kaggle_Biohub_Data\train")
    ap.add_argument("--name", default=None, help="dataset id (default: first .zarr)")
    ap.add_argument("--max-t", type=int, default=20)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    name = args.name or sorted(p.stem for p in data_dir.glob("*.zarr"))[0]
    print(f"Benchmarking U-Net on {name} (max_t={args.max_t})...")
    out = benchmark_dataset(data_dir / name, max_frames=args.max_t)
    print(f"  nodes={out['nodes']} edges={out['edges']}")
    print(f"  edge_jaccard={out['edge_jaccard']:.4f}")
    print(f"  division_jaccard={out['division_jaccard']}")
    print(f"  FINAL SCORE={out['score']:.4f}")