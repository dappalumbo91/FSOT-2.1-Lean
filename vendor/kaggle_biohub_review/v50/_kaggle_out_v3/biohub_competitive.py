#!/usr/bin/env python3
"""
Biohub competitive cell-tracking engine.

Detection + linking stack aligned with the official competition repo
(royerlab/kaggle-cell-tracking-competition): quantile normalization, 3D NMS,
Hungarian assignment at metric-scale distances, gap recovery, and division handling.

FSOT scalar costs refine link selection on top of this base (fsot_cellular_bridge).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy.ndimage import center_of_mass, label, maximum_filter
from scipy.optimize import linear_sum_assignment

from fsot_cellular_bridge import (
    GAP_DISTANCE_SCALE,
    GAP_MAX_FRAMES,
    MITOSIS_DAUGHTER_MAX_UM,
    PHYSICAL_MITOSIS_VOL_UM3,
    SCALE_VEC,
    TRANSLATION_MAX_UM,
    DetectionStats,
    OpenTrack,
    SequenceTracker,
    link_cost,
    mitosis_ready,
    phys_coords,
)

try:
    from tracking_cellmot.img_proc import nms_3d, quantile_normalize
except ImportError:
    nms_3d = None
    quantile_normalize = None

# Physical scale (z, y, x) microns / voxel — competition default.
SCALE = (1.625, 0.40625, 0.40625)
Z_SCALE, Y_SCALE, X_SCALE = SCALE
VOXEL_VOL_UM3 = Z_SCALE * Y_SCALE * X_SCALE
MIN_CELL_VOL_UM3 = float(os.environ.get("BIOHUB_MIN_VOL_UM3", "150"))
MATCH_MAX_UM = float(os.environ.get("BIOHUB_MATCH_MAX_UM", "7.0"))
LINK_MAX_UM = float(os.environ.get("BIOHUB_LINK_MAX_UM", str(TRANSLATION_MAX_UM)))
FSOT_LINK_WEIGHT = float(os.environ.get("FSOT_LINK_WEIGHT", "1.0"))
NMS_MIN_UM = float(os.environ.get("BIOHUB_NMS_UM", "6.0"))
PEAK_THRESH = float(os.environ.get("BIOHUB_PEAK_THRESH", "0.55"))
PEAK_TOPK = int(os.environ.get("BIOHUB_PEAK_TOPK", "0"))  # 0 = disabled

CELLPOSE_DIAMETER = float(os.environ.get("CELLPOSE_DIAMETER", "30.0"))
CELLPOSE_STITCH = float(os.environ.get("CELLPOSE_STITCH", "0.5"))


@dataclass
class DatasetContext:
    quantiles: dict[str, float] = field(default_factory=dict)

    def normalize_frame(self, frame: np.ndarray) -> np.ndarray:
        if self.quantiles and "0.001" in self.quantiles and "0.999" in self.quantiles:
            q1 = float(self.quantiles["0.001"])
            q2 = float(self.quantiles["0.999"])
            out = (frame.astype(np.float32) - q1) / (q2 - q1 + 1e-6)
            return np.clip(out, 0.0, 4.0)
        if quantile_normalize is not None:
            return quantile_normalize(frame)
        img = frame.astype(np.float32)
        return (img - img.min()) / (img.max() - img.min() + 1e-6)


def _cells_from_labels(frame_3d: np.ndarray, labels: np.ndarray) -> list[dict]:
    num = int(labels.max())
    if num == 0:
        return []
    centers = center_of_mass(frame_3d, labels, range(1, num + 1))
    counts = np.bincount(labels.ravel())[1:]
    cells = []
    for i in range(num):
        coords = centers[i]
        if coords is None or np.isnan(coords).any():
            continue
        z, y, x = coords
        vol = float(counts[i] * VOXEL_VOL_UM3)
        if vol >= MIN_CELL_VOL_UM3:
            cells.append({
                "z": float(z), "y": float(y), "x": float(x),
                "physical_volume": vol, "vol": vol, "score": float(vol),
            })
    return cells


def _nms_cells(cells: list[dict]) -> list[dict]:
    if not cells or nms_3d is None or len(cells) == 1:
        return cells
    coords = np.array([[c["z"], c["y"], c["x"]] for c in cells])
    scores = np.array([c.get("score", c["physical_volume"]) for c in cells], dtype=np.float64)
    keep = nms_3d(coords, scores, NMS_MIN_UM, SCALE)
    return [cells[i] for i in keep]


def detect_peaks(frame_3d: np.ndarray, ctx: DatasetContext | None = None) -> list[dict]:
    """Quantile-normalized 3D local-max peaks (competition-style fallback)."""
    ctx = ctx or DatasetContext()
    fn = ctx.normalize_frame(frame_3d)
    kz = max(1, int(round(4.0 / Z_SCALE)))
    ky = max(1, int(round(3.0 / Y_SCALE)))
    kx = max(1, int(round(3.0 / X_SCALE)))
    if kz % 2 == 0:
        kz += 1
    if ky % 2 == 0:
        ky += 1
    if kx % 2 == 0:
        kx += 1
    mx = maximum_filter(fn, size=(kz, ky, kx))
    peaks = np.argwhere((fn == mx) & (fn > PEAK_THRESH))
    if len(peaks) == 0:
        return []
    scores = fn[peaks[:, 0], peaks[:, 1], peaks[:, 2]]
    if nms_3d is not None:
        keep = nms_3d(peaks, scores, NMS_MIN_UM, SCALE)
        peaks, scores = peaks[keep], scores[keep]
    if PEAK_TOPK > 0 and len(scores) > PEAK_TOPK:
        order = np.argsort(scores)[::-1][:PEAK_TOPK]
        peaks, scores = peaks[order], scores[order]
    return [
        {"z": float(z), "y": float(y), "x": float(x),
         "physical_volume": 500.0, "vol": 500.0, "score": float(s)}
        for (z, y, x), s in zip(peaks, scores)
    ]


def detect_threshold(frame_3d: np.ndarray) -> list[dict]:
    """Legacy threshold detector — kept for diagnostics only."""
    threshold = np.mean(frame_3d) + 1.2 * np.std(frame_3d)
    labeled, _ = label(frame_3d > threshold)
    return _nms_cells(_cells_from_labels(frame_3d, labeled))


_CELLPOSE_MODEL = None


def _get_cellpose(pretrained: str | None = None):
    global _CELLPOSE_MODEL
    if _CELLPOSE_MODEL is None:
        import torch
        from cellpose import models
        gpu = torch.cuda.is_available()
        path = pretrained or os.environ.get("CELLPOSE_WEIGHTS", r"C:\Users\damia\.cellpose\models\cpsam_v2")
        if os.path.exists(path):
            _CELLPOSE_MODEL = models.CellposeModel(gpu=gpu, pretrained_model=path)
        else:
            _CELLPOSE_MODEL = models.CellposeModel(gpu=gpu)
    return _CELLPOSE_MODEL


def detect_cellpose(frame_3d: np.ndarray, ctx: DatasetContext | None = None) -> list[dict]:
    model = _get_cellpose()
    out = model.eval(
        frame_3d, z_axis=0, stitch_threshold=CELLPOSE_STITCH,
        diameter=CELLPOSE_DIAMETER, normalize=True,
    )
    cells = _cells_from_labels(frame_3d, np.asarray(out[0]))
    return _nms_cells(cells)


@dataclass
class CompetitiveDetector:
    mode: str = os.environ.get("BIOHUB_DETECTOR", "cellpose")
    ctx: DatasetContext = field(default_factory=DatasetContext)
    stats: DetectionStats = field(default_factory=DetectionStats)

    def __call__(self, frame_3d: np.ndarray) -> list[dict]:
        used_cellpose = False
        cells: list[dict] = []
        if self.mode == "cellpose":
            try:
                cells = detect_cellpose(frame_3d, self.ctx)
                used_cellpose = True
            except Exception as exc:  # noqa: BLE001
                print(f"[DETECT] cellpose failed ({type(exc).__name__}: {exc}); using peaks.")
                cells = detect_peaks(frame_3d, self.ctx)
        elif self.mode == "peaks":
            cells = detect_peaks(frame_3d, self.ctx)
        else:
            cells = detect_threshold(frame_3d)
        self.stats.record(used_cellpose)
        return cells


class CompetitiveTracker(SequenceTracker):
    """Gap-recovery tracker with FSOT-weighted Hungarian costs."""

    def _assign(self, parents: list[OpenTrack], child_indices: list[int],
                children: list[dict], child_global_ids: list[int], gap: int
                ) -> tuple[set[int], set[int]]:
        if not parents or not child_indices:
            return set(), set()

        p_phys = np.array([phys_coords([p.cell])[0] for p in parents])
        c_phys = phys_coords([children[j] for j in child_indices])
        max_um = LINK_MAX_UM * (1.0 + (max(1, gap) - 1) * GAP_DISTANCE_SCALE)

        n_p, n_c = len(parents), len(child_indices)
        cost = np.full((n_p, n_c), 1e6, dtype=np.float64)
        for i, parent in enumerate(parents):
            pv = parent.cell.get("physical_volume", parent.cell.get("vol", 1.0))
            for j_local, j in enumerate(child_indices):
                cv = children[j]["physical_volume"]
                d_um = float(np.linalg.norm(c_phys[j_local] - p_phys[i]))
                if d_um <= max_um:
                    dist_cost = d_um / max(LINK_MAX_UM, 1e-6)
                    fsot_cost = link_cost(d_um, pv, cv) if FSOT_LINK_WEIGHT > 0 else 0.0
                    cost[i, j_local] = dist_cost + FSOT_LINK_WEIGHT * fsot_cost

        matched_children: set[int] = set()
        linked_parents: set[int] = set()
        row_ind, col_ind = linear_sum_assignment(cost)
        for i, j_local in zip(row_ind, col_ind):
            if cost[i, j_local] >= 1e5:
                continue
            j = child_indices[j_local]
            self.edges.append((parents[i].global_id, child_global_ids[j]))
            matched_children.add(j)
            linked_parents.add(parents[i].global_id)
        return matched_children, linked_parents

    def _mitosis_links(self, parent: OpenTrack, child_indices: list[int],
                       children: list[dict], child_global_ids: list[int]) -> list[int]:
        if not mitosis_ready(parent.cell.get("physical_volume", parent.cell.get("vol", 0.0))):
            return []
        return super()._mitosis_links(parent, child_indices, children, child_global_ids)


def run_tracking(
    frames: list[list[dict]],
    global_ids_per_frame: list[list[int]],
) -> list[tuple[int, int]]:
    tracker = CompetitiveTracker()
    for t, (cells, gids) in enumerate(zip(frames, global_ids_per_frame)):
        tracker.advance(t, cells, gids)
    return list(tracker.edges)


def make_benchmark_tracker():
    """Return a tracksdata-compatible tracker function."""
    def _track(frames):
        import polars as pl
        import tracksdata as td
        from fsot_cellular_bridge import track_sequence

        g, per_t = frames["graph"], frames["per_t"]
        norm_per_t = []
        for cells, ids in per_t:
            norm_cells = []
            for c in cells:
                nc = dict(c)
                nc["physical_volume"] = c.get("vol", c.get("physical_volume", 0.0))
                norm_cells.append(nc)
            norm_per_t.append((norm_cells, ids))

        # Use CompetitiveTracker via patched sequence — reuse bridge track_sequence
        # but swap in competitive assignment through run_tracking on index ids.
        tracker = CompetitiveTracker()
        id_to_loc: dict[int, tuple[int, int]] = {}
        edge_quads = []
        prev = 0
        for t, (cells, ids) in enumerate(norm_per_t):
            for j, nid in enumerate(ids):
                id_to_loc[nid] = (t, j)
            tracker.advance(t, cells, ids)
            for src_gid, tgt_gid in tracker.edges[prev:]:
                if src_gid in id_to_loc and tgt_gid in id_to_loc:
                    ts, isrc = id_to_loc[src_gid]
                    tt, jtgt = id_to_loc[tgt_gid]
                    edge_quads.append((ts, isrc, tt, jtgt))
            prev = len(tracker.edges)

        for ts, isrc, tt, jtgt in edge_quads:
            g.add_edge(norm_per_t[ts][1][isrc], norm_per_t[tt][1][jtgt], {})
        return g

    return _track