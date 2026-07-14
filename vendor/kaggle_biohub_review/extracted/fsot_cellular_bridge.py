#!/usr/bin/env python3
"""
FSOT Cellular Bridge — calibrated mapping from 3D cell observables to FSOT delta_psi,
plus Hungarian assignment and gap-recovery tracking shared by the Kaggle master pipeline
and the local benchmark harness.

Calibration mirrors the burial-bridge pattern in Desktop/New folder: Lean certifies the
scalar math (fsot_core.py); this module maps *physical* cell-tracking features into the
dual-axis trinary encoding used by codon_coherence_fast (64_codon_trinary_map.txt §5–6).

Linking  → coherence scalar (mode C): S in fertile window 0.15–0.45, centered near K.
Mitosis  → coherence-collapse (mode B): compute_scalar_biological(vol_psi) >= threshold.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np
from scipy.spatial import cKDTree

from fsot_core import (
    COLLAPSE_THRESHOLD,
    FERTILE_HIGH,
    FERTILE_LOW,
    K,
    compute_scalar_biological,
    trinary_collapse,
)

# ---------------------------------------------------------------------------
# Physical calibration (keep in sync with fsot_kaggle_submission_master.py)
# ---------------------------------------------------------------------------
Z_SCALE = 1.625
Y_SCALE = 0.40625
X_SCALE = 0.40625
SCALE_VEC = np.array([Z_SCALE, Y_SCALE, X_SCALE])

PHYSICAL_MITOSIS_VOL_UM3 = float(os.environ.get("FSOT_MITOSIS_VOL_UM3", "2500"))
TRANSLATION_MAX_UM = float(os.environ.get("FSOT_TRANSLATION_MAX_UM", "25"))
MITOSIS_DAUGHTER_MAX_UM = float(os.environ.get("FSOT_MITOSIS_DAUGHTER_UM", "35"))
GAP_MAX_FRAMES = int(os.environ.get("FSOT_GAP_MAX", "3"))
GAP_DISTANCE_SCALE = float(os.environ.get("FSOT_GAP_DISTANCE_SCALE", "1.35"))
BASE_CELL_VOL_UM3 = float(os.environ.get("FSOT_BASE_VOL_UM3", "500"))
def _edge_threshold() -> float:
    return float(os.environ.get("FSOT_EDGE_THRESHOLD", "0.42"))


def _use_softmax_assign() -> bool:
    # Softmax only when explicitly enabled — crowded U-Net graphs dilute per-child mass.
    return os.environ.get("FSOT_SOFTMAX_ASSIGN", "0") == "1"


def _max_parents() -> int:
    return int(os.environ.get("FSOT_MAX_PARENTS", "1"))


def _max_children() -> int:
    return int(os.environ.get("FSOT_MAX_CHILDREN", "2"))


def _vol_key(cell: dict) -> float:
    return float(cell.get("physical_volume", cell.get("vol", 0.0)))


def phys_coords(cells: list[dict]) -> np.ndarray:
    return np.array([[c["z"], c["y"], c["x"]] for c in cells], dtype=np.float64) * SCALE_VEC


def _trit_from_norm(x: float, low: float = 0.33, high: float = 0.66) -> int:
    if x < low:
        return -1
    if x > high:
        return 1
    return 0


def codon_coherence_fast(
    primary: Sequence[int],
    secondary: Sequence[int],
    observed: bool = True,
) -> float:
    """Dual-axis trinary → biological-domain scalar (slime mold / fsot gene verified)."""
    p_norm = sum(abs(x) for x in primary) / 3.0
    s_norm = sum(abs(x) for x in secondary) / 3.0
    return compute_scalar_biological(
        N=1.0,
        P=(p_norm + s_norm) / 2,
        delta_psi=p_norm * 0.1,
        observed=observed,
    )


def cell_dual_axis(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
) -> tuple[list[int], list[int]]:
    """Map cell-pair observables to PRIMARY/SECONDARY trinary vectors (§12 bridge)."""
    disp_norm = min(displacement_um / max(translation_max, 1e-6), 1.0)
    dvol_norm = min(abs(child_vol - parent_vol) / max(parent_vol, 1.0), 1.0)
    vol_norm = min(parent_vol / max(PHYSICAL_MITOSIS_VOL_UM3, 1.0), 1.0)

    primary = [
        _trit_from_norm(vol_norm),
        _trit_from_norm(disp_norm, 0.25, 0.75),
        _trit_from_norm(dvol_norm, 0.15, 0.45),
    ]
    secondary = [
        _trit_from_norm(1.0 - disp_norm),
        _trit_from_norm(1.0 - dvol_norm),
        0 if 0.3 < disp_norm < 0.7 else _trit_from_norm(dvol_norm),
    ]
    return primary, secondary


def cell_coherence_fast(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
    observed: bool = True,
) -> float:
    primary, secondary = cell_dual_axis(
        displacement_um, parent_vol, child_vol, translation_max
    )
    return codon_coherence_fast(primary, secondary, observed=observed)


def link_affinity(S: float) -> float:
    """Fertile-window intelligence score centered on K (fic_lab / §6 pattern)."""
    if not (FERTILE_LOW < S < FERTILE_HIGH):
        return 0.0
    half_band = (FERTILE_HIGH - FERTILE_LOW) / 2.0
    return max(0.0, 1.0 - abs(S - K) / half_band)


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def cell_pair_directed_delta(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
) -> float:
    """Asymmetric parent→child coupling (fsot_structure_math.directed_codon_pair_delta)."""
    primary_p, secondary_p = cell_dual_axis(
        displacement_um, parent_vol, child_vol, translation_max
    )
    primary_c, secondary_c = cell_dual_axis(
        displacement_um, child_vol, parent_vol, translation_max
    )
    coh_p = codon_coherence_fast(primary_p, secondary_p, observed=True)
    coh_c = codon_coherence_fast(primary_c, secondary_c, observed=True)
    coh_p_u = codon_coherence_fast(primary_p, secondary_p, observed=False)
    coh_c_u = codon_coherence_fast(primary_c, secondary_c, observed=False)
    p_pole = sum(primary_p) / 3.0
    c_pole = sum(primary_c) / 3.0
    yin_p = float(trinary_collapse(coh_p)) - float(trinary_collapse(coh_p_u))
    yin_c = float(trinary_collapse(coh_c)) - float(trinary_collapse(coh_c_u))
    obs_p = coh_p - coh_p_u
    obs_c = coh_c - coh_c_u
    yin_prod_p = float(primary_p[0] * secondary_p[1])
    yin_prod_c = float(primary_c[0] * secondary_c[1])
    return (
        p_pole * coh_c - c_pole * coh_p
        + 0.45 * (yin_p * yin_prod_c - yin_c * yin_prod_p)
        + 0.30 * (obs_p * c_pole - obs_c * p_pole)
    )


def link_edge_prob(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
) -> float:
    """FSOT link logit: fertile coherence × spatial coupling × directed pair gate."""
    if displacement_um > translation_max:
        return 0.0
    S = cell_coherence_fast(
        displacement_um, parent_vol, child_vol, translation_max, observed=True
    )
    aff = link_affinity(S)
    if aff <= 0.0:
        return 0.0
    dist_scale = max(translation_max / 2.0, 1e-6)
    return aff * math.exp(-displacement_um / dist_scale)


def link_edge_prob_refined(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
) -> float:
    """FSOT + directed-pair refinement (fsot_structure_math) for hybrid gating."""
    base = link_edge_prob(displacement_um, parent_vol, child_vol, translation_max)
    if base <= 0.0:
        return 0.0
    S_obs = cell_coherence_fast(
        displacement_um, parent_vol, child_vol, translation_max, observed=True
    )
    S_unobs = cell_coherence_fast(
        displacement_um, parent_vol, child_vol, translation_max, observed=False
    )
    directed = cell_pair_directed_delta(
        displacement_um, parent_vol, child_vol, translation_max
    )
    observer_boost = 1.0 + 0.25 * abs(S_obs - S_unobs)
    directed_boost = 1.0 + 0.22 * _sigmoid(directed * 3.0)
    return min(base * observer_boost * directed_boost, 1.0)


def _softmax_over_parents(raw: np.ndarray) -> np.ndarray:
    """Per-child softmax over *valid* parents only (within link radius)."""
    n_p, n_c = raw.shape
    probs = np.zeros_like(raw)
    for cj in range(n_c):
        valid = np.flatnonzero(raw[:, cj] > 0.0)
        if valid.size == 0:
            continue
        col = raw[valid, cj]
        shifted = col - col.max()
        exp = np.exp(shifted)
        probs[valid, cj] = exp / (exp.sum() + 1e-12)
    return probs


def link_cost(
    displacement_um: float,
    parent_vol: float,
    child_vol: float,
    translation_max: float = TRANSLATION_MAX_UM,
) -> float:
    """Lower is better. Inverted FSOT edge probability for Hungarian backends."""
    prob = link_edge_prob(displacement_um, parent_vol, child_vol, translation_max)
    if prob < _edge_threshold():
        return 1e6
    return 1.0 - prob


def _greedy_assign_pairs(
    candidates: list[tuple[float, int, int]],
    n_parents: int,
    n_children: int,
    max_children: int | None = None,
    max_parents: int | None = None,
) -> list[tuple[int, int, float]]:
    max_children = _max_children() if max_children is None else max_children
    max_parents = _max_parents() if max_parents is None else max_parents
    """Greedy one-to-one(+mitosis) matching sorted by FSOT probability (transformer topology)."""
    children_count = [0] * n_parents
    parents_count = [0] * n_children
    edges: list[tuple[int, int, float]] = []
    for prob, i, j in sorted(candidates, reverse=True):
        if children_count[i] >= max_children:
            continue
        if parents_count[j] >= max_parents:
            continue
        edges.append((i, j, prob))
        children_count[i] += 1
        parents_count[j] += 1
    return edges


def link_frame_pair_fsot(
    parents: list[dict],
    children: list[dict],
    idx_parents: list[int],
    idx_children: list[int],
    translation_max: float = TRANSLATION_MAX_UM,
) -> list[tuple[int, int, float, float]]:
    """Link one consecutive frame pair using FSOT fertile-window edge probabilities."""
    if not parents or not children:
        return []

    p_phys = phys_coords(parents)
    c_phys = phys_coords(children)
    edges_out: list[tuple[int, int, float, float]] = []
    used_parent: set[int] = set()
    used_child: set[int] = set()

    # Mitosis: collapse-gated parent → up to two daughters.
    for i, pc in enumerate(parents):
        if not mitosis_ready(_vol_key(pc)):
            continue
        mitosis_cands: list[tuple[float, int]] = []
        for j, cc in enumerate(children):
            d_um = float(np.linalg.norm(c_phys[j] - p_phys[i]))
            if d_um > MITOSIS_DAUGHTER_MAX_UM:
                continue
            prob = link_edge_prob(d_um, _vol_key(pc), _vol_key(cc), translation_max)
            if prob >= _edge_threshold():
                mitosis_cands.append((prob, j))
        mitosis_cands.sort(reverse=True)
        if len(mitosis_cands) < 2:
            continue
        used_parent.add(i)
        for prob, j in mitosis_cands[:2]:
            edges_out.append((idx_parents[i], idx_children[j], prob, 0.0))
            used_child.add(j)

    rem_p = [i for i in range(len(parents)) if i not in used_parent]
    rem_c = [j for j in range(len(children)) if j not in used_child]
    if not rem_p or not rem_c:
        return edges_out

    n_rem_p, n_rem_c = len(rem_p), len(rem_c)
    raw = np.zeros((n_rem_p, n_rem_c), dtype=np.float64)
    for pi, i in enumerate(rem_p):
        for cj, j in enumerate(rem_c):
            d_um = float(np.linalg.norm(c_phys[j] - p_phys[i]))
            raw[pi, cj] = link_edge_prob(
                d_um, _vol_key(parents[i]), _vol_key(children[j]), translation_max
            )

    probs = _softmax_over_parents(raw) if _use_softmax_assign() else raw

    candidates: list[tuple[float, int, int]] = []
    thr = _edge_threshold()
    for pi in range(n_rem_p):
        for cj in range(n_rem_c):
            p = float(probs[pi, cj])
            if p >= thr:
                candidates.append((p, pi, cj))

    for pi, cj, prob in _greedy_assign_pairs(candidates, n_rem_p, n_rem_c):
        edges_out.append((idx_parents[rem_p[pi]], idx_children[rem_c[cj]], prob, 0.0))
    return edges_out


def link_coords_fsot(
    coords: np.ndarray,
    default_vol: float = BASE_CELL_VOL_UM3,
) -> list[tuple[int, int, float, float]]:
    """FSOT linker for U-Net coords. Set FSOT_GAP_LINK=1 for SequenceTracker gap recovery."""
    if len(coords) == 0:
        return []

    by_t: dict[int, list[int]] = {}
    cells_by_idx: dict[int, dict] = {}
    for idx, row in enumerate(coords):
        t = int(row[0])
        by_t.setdefault(t, []).append(idx)
        cells_by_idx[idx] = {
            "z": float(row[1]), "y": float(row[2]), "x": float(row[3]),
            "physical_volume": default_vol, "vol": default_vol,
        }

    for indices in by_t.values():
        estimate_volumes_for_frame([cells_by_idx[i] for i in indices], base_vol=default_vol)

    use_gap = os.environ.get("FSOT_GAP_LINK", "0") == "1"
    if use_gap:
        t_min, t_max = min(by_t), max(by_t)
        tracker = SequenceTracker()
        for t in range(t_min, t_max + 1):
            indices = by_t.get(t, [])
            cells = [cells_by_idx[i] for i in indices]
            tracker.advance(t, cells, indices)
        edges_out: list[tuple[int, int, float, float]] = []
        for src, tgt in tracker.edges:
            if src not in cells_by_idx or tgt not in cells_by_idx:
                continue
            pc, cc = cells_by_idx[src], cells_by_idx[tgt]
            d_um = float(np.linalg.norm(phys_coords([cc])[0] - phys_coords([pc])[0]))
            prob = link_edge_prob(d_um, _vol_key(pc), _vol_key(cc))
            edges_out.append((src, tgt, prob, 0.0))
        return edges_out

    all_edges: list[tuple[int, int, float, float]] = []
    times = sorted(by_t.keys())
    for t0, t1 in zip(times, times[1:]):
        if t1 != t0 + 1:
            continue
        idx0, idx1 = by_t[t0], by_t[t1]
        parents = [cells_by_idx[i] for i in idx0]
        children = [cells_by_idx[i] for i in idx1]
        all_edges.extend(link_frame_pair_fsot(parents, children, idx0, idx1))
    return all_edges


def mitosis_vol_psi(
    volume_um3: float,
    mitosis_vol: float = PHYSICAL_MITOSIS_VOL_UM3,
) -> float:
    """Map volume excess into delta_psi for the mitosis scalar gate (mode B)."""
    ratio = volume_um3 / max(mitosis_vol, 1.0)
    if ratio <= 1.0:
        return 0.0
    return min(0.85 + (ratio - 1.0) * 0.3, 1.25)


def mitosis_scalar(
    volume_um3: float,
    mitosis_vol: float = PHYSICAL_MITOSIS_VOL_UM3,
) -> float:
    return compute_scalar_biological(
        delta_psi=mitosis_vol_psi(volume_um3, mitosis_vol),
        observed=True,
    )


def mitosis_ready(
    volume_um3: float,
    mitosis_vol: float = PHYSICAL_MITOSIS_VOL_UM3,
) -> bool:
    """Parent exceeds volume gate and scalar crosses collapse threshold (§12)."""
    if volume_um3 <= mitosis_vol:
        return False
    S = mitosis_scalar(volume_um3, mitosis_vol)
    return trinary_collapse(S) == 1


def estimate_volumes_for_frame(
    cells: list[dict],
    base_vol: float = BASE_CELL_VOL_UM3,
) -> None:
    """Infer per-detection volume from nearest-neighbor spacing (U-Net coords lack masks)."""
    if not cells:
        return
    coords = phys_coords(cells)
    tree = cKDTree(coords)
    for i, cell in enumerate(cells):
        if _vol_key(cell) > base_vol * 1.05:
            continue
        dists, _ = tree.query(coords[i], k=min(4, len(cells)))
        nn = float(dists[1]) if len(dists) > 1 else float(dists[0])
        nn = max(nn, 3.0)
        est = base_vol * (nn / 12.0) ** 2
        est = float(np.clip(est, base_vol * 0.5, PHYSICAL_MITOSIS_VOL_UM3 * 2.5))
        cell["physical_volume"] = est
        cell["vol"] = est


def max_link_distance_um(gap_frames: int) -> float:
    """Allow farther jumps when bridging over missed detections."""
    gap_frames = max(1, gap_frames)
    return TRANSLATION_MAX_UM * (1.0 + (gap_frames - 1) * GAP_DISTANCE_SCALE)


@dataclass
class DetectionStats:
    cellpose_frames: int = 0
    threshold_frames: int = 0

    @property
    def total(self) -> int:
        return self.cellpose_frames + self.threshold_frames

    def record(self, used_cellpose: bool) -> None:
        if used_cellpose:
            self.cellpose_frames += 1
        else:
            self.threshold_frames += 1

    def summary(self) -> str:
        if self.total == 0:
            return "[DETECTION] no frames processed"
        cp_pct = 100.0 * self.cellpose_frames / self.total
        th_pct = 100.0 * self.threshold_frames / self.total
        level = "OK" if th_pct < 5.0 else ("WARN" if th_pct < 50.0 else "CRITICAL")
        return (f"[DETECTION:{level}] cellpose={self.cellpose_frames} ({cp_pct:.1f}%) "
                f"threshold_fallback={self.threshold_frames} ({th_pct:.1f}%)")


@dataclass
class OpenTrack:
    global_id: int
    cell: dict
    last_t: int
    missing: int = 0


@dataclass
class SequenceTracker:
    """Gap-aware tracker producing (source_global_id, target_global_id) edge pairs."""
    open_tracks: list[OpenTrack] = field(default_factory=list)
    edges: list[tuple[int, int]] = field(default_factory=list)

    def _mitosis_links(self, parent: OpenTrack, child_indices: list[int],
                       children: list[dict], child_global_ids: list[int]) -> list[int]:
        """Link collapse-gated parent to up to two daughters by FSOT edge probability."""
        if not mitosis_ready(_vol_key(parent.cell)):
            return []
        p_phys = phys_coords([parent.cell])[0]
        c_phys = phys_coords(children)
        cand: list[tuple[float, int]] = []
        for j in child_indices:
            d_um = float(np.linalg.norm(c_phys[j] - p_phys))
            if d_um > MITOSIS_DAUGHTER_MAX_UM:
                continue
            prob = link_edge_prob(d_um, _vol_key(parent.cell), _vol_key(children[j]))
            if prob >= _edge_threshold():
                cand.append((prob, j))
        cand.sort(reverse=True)
        if len(cand) < 2:
            return []
        matched = []
        for _, j in cand[:2]:
            self.edges.append((parent.global_id, child_global_ids[j]))
            matched.append(j)
        return matched

    def _assign(self, parents: list[OpenTrack], child_indices: list[int],
                children: list[dict], child_global_ids: list[int], gap: int
                ) -> tuple[set[int], set[int]]:
        """Greedy fertile-window assignment for one gap layer."""
        if not parents or not child_indices:
            return set(), set()

        max_um = max_link_distance_um(gap)
        parent_cells = [p.cell for p in parents]
        child_cells = [children[j] for j in child_indices]
        parent_gids = [p.global_id for p in parents]
        pair_edges = link_frame_pair_fsot(
            parent_cells, child_cells, parent_gids, child_global_ids, translation_max=max_um,
        )

        matched_children: set[int] = set()
        linked_parents: set[int] = set()
        child_gid_to_idx = {gid: j for j, gid in zip(child_indices, child_global_ids)}
        for src_gid, tgt_gid, _prob, _ in pair_edges:
            self.edges.append((src_gid, tgt_gid))
            linked_parents.add(src_gid)
            if tgt_gid in child_gid_to_idx:
                matched_children.add(child_gid_to_idx[tgt_gid])
        return matched_children, linked_parents

    def advance(self, t: int, cells: list[dict], global_ids: list[int]) -> None:
        """Register nodes at time t and emit edges (with gap recovery)."""
        if not cells:
            for track in self.open_tracks:
                track.missing += 1
            self.open_tracks = [tr for tr in self.open_tracks if tr.missing <= GAP_MAX_FRAMES]
            return

        estimate_volumes_for_frame(cells)

        available = set(range(len(cells)))
        next_open: list[OpenTrack] = []
        linked_parents: set[int] = set()

        # Mitosis first on every open track (most recent tails first).
        for track in sorted(self.open_tracks, key=lambda tr: tr.missing):
            if not available:
                break
            matched = self._mitosis_links(track, sorted(available), cells, global_ids)
            if matched:
                linked_parents.add(track.global_id)
            for j in matched:
                available.discard(j)
                next_open.append(OpenTrack(global_ids[j], cells[j], t, 0))

        # Gap layers: try most recent open tracks first, then older missing tails.
        for gap in range(1, GAP_MAX_FRAMES + 1):
            if not available:
                break
            layer = [tr for tr in self.open_tracks
                     if tr.missing + 1 == gap and tr.global_id not in linked_parents]
            if not layer:
                continue
            matched, parents_hit = self._assign(layer, sorted(available), cells, global_ids, gap)
            linked_parents |= parents_hit
            available -= matched
            for j in matched:
                next_open.append(OpenTrack(global_ids[j], cells[j], t, 0))

        # Brand-new tracks for unmatched detections.
        for j in sorted(available):
            next_open.append(OpenTrack(global_ids[j], cells[j], t, 0))

        # Age out unmatched previous tails (linked parents retire).
        for track in self.open_tracks:
            if track.global_id in linked_parents:
                continue
            if any(nt.global_id == track.global_id for nt in next_open):
                continue
            track.missing += 1
            if track.missing <= GAP_MAX_FRAMES:
                next_open.append(track)

        self.open_tracks = next_open


def link_frames(cells_t0: list[dict], cells_t1: list[dict]) -> list[tuple[int, int]]:
    """Consecutive-frame linker returning (i0, j1) index pairs (backward compatible)."""
    if not cells_t0 or not cells_t1:
        return []

    estimate_volumes_for_frame(cells_t0)
    estimate_volumes_for_frame(cells_t1)
    idx0 = list(range(len(cells_t0)))
    idx1 = list(range(len(cells_t1)))
    return [
        (src, tgt)
        for src, tgt, _prob, _ in link_frame_pair_fsot(cells_t0, cells_t1, idx0, idx1)
    ]


def track_sequence(per_t: list[tuple[list[dict], list[int]]]) -> list[tuple[int, int, int, int]]:
    """Full sequence tracker for the benchmark harness.

    per_t: list of (cells, node_ids) per frame.
    Returns edges as (t_src, i_src, t_tgt, j_tgt) into per_t indices.
    """
    tracker = SequenceTracker()
    edge_quads: list[tuple[int, int, int, int]] = []
    prev_edge_count = 0
    id_to_loc: dict[int, tuple[int, int]] = {}

    for t, (cells, ids) in enumerate(per_t):
        for j, nid in enumerate(ids):
            id_to_loc[nid] = (t, j)
        tracker.advance(t, cells, ids)
        for src_gid, tgt_gid in tracker.edges[prev_edge_count:]:
            if src_gid not in id_to_loc or tgt_gid not in id_to_loc:
                continue
            ts, isrc = id_to_loc[src_gid]
            tt, jtgt = id_to_loc[tgt_gid]
            edge_quads.append((ts, isrc, tt, jtgt))
        prev_edge_count = len(tracker.edges)

    return edge_quads