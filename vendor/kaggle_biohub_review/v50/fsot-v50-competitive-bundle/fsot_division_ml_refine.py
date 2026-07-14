#!/usr/bin/env python3
"""Re-resolve parent swaps on division frames with transformer edge scores."""

from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

from predict_unet_transformer import (
    PredictConfig,
    _load_frame,
    extract_pos_features,
)
from tracking_cellmot.io import open_dataset


def _idx_by_time(coords: np.ndarray) -> dict[int, list[int]]:
    by_t: dict[int, list[int]] = defaultdict(list)
    for i in range(len(coords)):
        by_t[int(coords[i, 0])].append(i)
    return by_t


def _refine_edge_threshold(cfg: PredictConfig) -> float:
    """Lower softmax threshold for division-frame refine (many sources dilute peaks)."""
    raw = os.environ.get(
        "FSOT_ML_REFINE_EDGE_THRESHOLD",
        os.environ.get("CELLMOT_EDGE_THRESHOLD", str(cfg.threshold)),
    )
    return float(raw)


def _refine_mode() -> str:
    return os.environ.get("FSOT_ML_REFINE_MODE", "replace").strip().lower()


def _refine_mode_for_frame(t_src: int) -> str:
    replace_frames = {
        int(x.strip())
        for x in os.environ.get("FSOT_ML_REFINE_REPLACE_FRAMES", "").split(",")
        if x.strip().isdigit()
    }
    merge_frames = {
        int(x.strip())
        for x in os.environ.get("FSOT_ML_REFINE_MERGE_FRAMES", "").split(",")
        if x.strip().isdigit()
    }
    if t_src in replace_frames:
        return "replace"
    if t_src in merge_frames:
        return "merge"
    return _refine_mode()


def _swap_conflicts(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
) -> tuple[dict[tuple[int, int], set[int]], dict[tuple[int, int], list[tuple[int, int, float, float]]]]:
    """Map (t, t+1) -> children with >1 incoming parent."""
    idx_t = {i: int(coords[i, 0]) for i in range(len(coords))}
    by_ft: dict[tuple[int, int], list[tuple[int, int, float, float]]] = defaultdict(list)
    for s, t, p, d in edges:
        ts, tt = idx_t.get(s, -9), idx_t.get(t, -9)
        if tt == ts + 1:
            by_ft[(ts, tt)].append((s, t, p, d))

    conflict_children: dict[tuple[int, int], set[int]] = {}
    for key, elist in by_ft.items():
        child_parents: dict[int, list[int]] = defaultdict(list)
        for s, t, _, _ in elist:
            child_parents[t].append(s)
        bad = {c for c, ps in child_parents.items() if len(ps) > 1}
        if bad:
            conflict_children[key] = bad
    return conflict_children, by_ft


@torch.no_grad()
def _ml_edge_probs(
    model,
    device: torch.device,
    cfg: PredictConfig,
    ds_path: Path,
    coords: np.ndarray,
    idx_src: list[int],
    idx_tgt: list[int],
    t_src: int,
    t_tgt: int,
    downsample: tuple[int, ...],
) -> np.ndarray | None:
    """Return (n_src, n_tgt) edge probabilities for one frame pair."""
    ds = open_dataset(ds_path, normalize=False, load_image=False, downsample=downsample)
    import zarr

    zarr_arr = zarr.open_group(str(ds.zarr_path), mode="r")["0"]
    q_low = float(ds.quantiles["0.001"])
    q_high = float(ds.quantiles["0.999"])
    target_shape = list(ds.image_shape[1:])
    ds_arr = torch.from_numpy(np.array(downsample, dtype=np.float32)).to(device)

    imgs = torch.stack([
        _load_frame(zarr_arr, t_src, target_shape, downsample),
        _load_frame(zarr_arr, t_tgt, target_shape, downsample),
    ])
    imgs = ((imgs - q_low) / (q_high - q_low + 1e-6)).clamp(0.0).unsqueeze(0).to(device)
    unet_out, _ = model.encode(imgs)
    del imgs

    c_src = coords[idx_src]
    c_tgt = coords[idx_tgt]
    n_src, n_tgt = len(idx_src), len(idx_tgt)
    if n_src == 0 or n_tgt == 0:
        return None

    p_coords_src = torch.from_numpy(c_src[:, 1:].astype(np.float32)).unsqueeze(0).to(device)
    p_coords_tgt = torch.from_numpy(c_tgt[:, 1:].astype(np.float32)).unsqueeze(0).to(device)
    window_shape = (2,) + tuple(ds.image_shape[1:])
    c_src_rel = c_src.copy()
    c_src_rel[:, 0] = 0
    c_tgt_rel = c_tgt.copy()
    c_tgt_rel[:, 0] = 1
    p_pos_src = torch.from_numpy(extract_pos_features(c_src_rel, window_shape)).unsqueeze(0).to(device)
    p_pos_tgt = torch.from_numpy(extract_pos_features(c_tgt_rel, window_shape)).unsqueeze(0).to(device)
    p_mask_src = torch.ones(1, n_src, dtype=torch.bool, device=device)
    p_mask_tgt = torch.ones(1, n_tgt, dtype=torch.bool, device=device)

    unet_feat_src = model._index_features(unet_out[:, 0], p_coords_src, p_mask_src)
    unet_feat_tgt = model._index_features(unet_out[:, 1], p_coords_tgt, p_mask_tgt)
    edge_logits = model.predict_edges(
        unet_feat_src, unet_feat_tgt,
        p_coords_src * ds_arr, p_coords_tgt * ds_arr,
        p_pos_src, p_pos_tgt,
        p_mask_src, p_mask_tgt,
    )[0]

    if cfg.edge_activation == "softmax":
        return torch.softmax(edge_logits, dim=0).cpu().numpy()
    return torch.sigmoid(edge_logits).cpu().numpy()


@torch.no_grad()
def _ml_greedy_pair_edges(
    model,
    device: torch.device,
    cfg: PredictConfig,
    ds_path: Path,
    coords: np.ndarray,
    idx_src: list[int],
    idx_tgt: list[int],
    t_src: int,
    t_tgt: int,
    downsample: tuple[int, ...],
    *,
    probs: np.ndarray | None = None,
) -> list[tuple[int, int, float, float]]:
    """Transformer greedy assignment for one consecutive frame pair."""
    c_src = coords[idx_src]
    c_tgt = coords[idx_tgt]
    n_src, n_tgt = len(idx_src), len(idx_tgt)
    if n_src == 0 or n_tgt == 0:
        return []

    if probs is None:
        probs = _ml_edge_probs(
            model, device, cfg, ds_path, coords,
            idx_src, idx_tgt, t_src, t_tgt, downsample,
        )
    if probs is None:
        return []

    thr = _refine_edge_threshold(cfg)
    max_children = int(os.environ.get("FSOT_ML_MAX_CHILDREN", "2"))
    max_parents = int(os.environ.get("FSOT_ML_MAX_PARENTS", "1"))

    candidates = sorted(
        [(probs[i, j], i, j) for i in range(n_src) for j in range(n_tgt) if probs[i, j] > thr],
        reverse=True,
    )
    children_count: dict[int, int] = {}
    parents_count: dict[int, int] = {}
    out: list[tuple[int, int, float, float]] = []
    for prob, i, j in candidates:
        if children_count.get(i, 0) >= max_children:
            continue
        if parents_count.get(j, 0) >= max_parents:
            continue
        gi, gj = idx_src[i], idx_tgt[j]
        dist = float(np.linalg.norm(c_src[i, 1:].astype(np.float32) - c_tgt[j, 1:].astype(np.float32)))
        out.append((gi, gj, float(prob), dist))
        children_count[i] = children_count.get(i, 0) + 1
        parents_count[j] = parents_count.get(j, 0) + 1
    return out


def _ml_parent_top_edges(
    probs: np.ndarray,
    idx_src: list[int],
    idx_tgt: list[int],
    coords: np.ndarray,
    parent_gids: set[int],
    *,
    max_children: int = 2,
    min_prob: float = 0.01,
) -> list[tuple[int, int, float, float]]:
    """Top-k ML daughters per parent (surgical division fix)."""
    gid_to_i = {gid: i for i, gid in enumerate(idx_src)}
    c_src = coords[idx_src]
    c_tgt = coords[idx_tgt]
    out: list[tuple[int, int, float, float]] = []
    for gid in parent_gids:
        i = gid_to_i.get(gid)
        if i is None:
            continue
        row = probs[i]
        order = np.argsort(row)[::-1]
        added = 0
        for j in order:
            if added >= max_children:
                break
            prob = float(row[j])
            if prob < min_prob:
                break
            gi, gj = idx_src[i], idx_tgt[j]
            dist = float(np.linalg.norm(c_src[i, 1:].astype(np.float32) - c_tgt[j, 1:].astype(np.float32)))
            out.append((gi, gj, prob, dist))
            added += 1
    return out


def _parents_needing_ml(
    fsot_ft: list[tuple[int, int, float, float]],
    conflict_children: set[int],
    probs: np.ndarray,
    idx_src: list[int],
    idx_tgt: list[int],
    cfg: PredictConfig,
    *,
    margin: float = 0.08,
) -> set[int]:
    """Parents to reassign: multi-child, conflict, or ML disagrees with FSOT."""
    child_parents: dict[int, list[int]] = defaultdict(list)
    parent_children: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for s, t, p, _ in fsot_ft:
        child_parents[t].append(s)
        parent_children[s].append((t, p))

    redo: set[int] = set()
    for c in conflict_children:
        redo.update(child_parents.get(c, []))
    for s, chs in parent_children.items():
        if len(chs) >= 2:
            redo.add(s)

    gid_to_i = {gid: i for i, gid in enumerate(idx_src)}
    for s, chs in parent_children.items():
        if s in redo or len(chs) != 1:
            continue
        i = gid_to_i.get(s)
        if i is None:
            continue
        cur_t, cur_p = chs[0]
        j = idx_tgt.index(cur_t) if cur_t in idx_tgt else -1
        ml_best_j = int(np.argmax(probs[i]))
        ml_best_p = float(probs[i, ml_best_j])
        cur_ml_p = float(probs[i, j]) if j >= 0 else 0.0
        if ml_best_j != j and ml_best_p > cur_ml_p + margin and ml_best_p > _refine_edge_threshold(cfg):
            redo.add(s)
    return redo


def _supplement_argmax_edges(
    probs: np.ndarray,
    idx_src: list[int],
    idx_tgt: list[int],
    coords: np.ndarray,
    existing: list[tuple[int, int, float, float]],
    *,
    max_um: float = 40.0,
    min_prob: float = 0.08,
) -> list[tuple[int, int, float, float]]:
    """Add per-parent ML argmax daughters missing from greedy assignment."""
    from fsot_cellular_bridge import phys_coords

    have = {(s, t) for s, t, _, _ in existing}
    c_src = coords[idx_src]
    c_tgt = coords[idx_tgt]
    pc_src = phys_coords([
        {"z": float(c[1]), "y": float(c[2]), "x": float(c[3])} for c in c_src
    ])
    pc_tgt = phys_coords([
        {"z": float(c[1]), "y": float(c[2]), "x": float(c[3])} for c in c_tgt
    ])
    extra: list[tuple[int, int, float, float]] = []
    for i, gid in enumerate(idx_src):
        j = int(np.argmax(probs[i]))
        prob = float(probs[i, j])
        if prob < min_prob:
            continue
        gj = idx_tgt[j]
        if (gid, gj) in have:
            continue
        d_um = float(np.linalg.norm(pc_src[i] - pc_tgt[j]))
        if d_um > max_um:
            continue
        dist = float(np.linalg.norm(c_src[i, 1:].astype(np.float32) - c_tgt[j, 1:].astype(np.float32)))
        extra.append((gid, gj, prob, dist))
        have.add((gid, gj))
    return extra


def _merge_frame_edges(
    fsot_ft: list[tuple[int, int, float, float]],
    ml_edges: list[tuple[int, int, float, float]],
    redo_parents: set[int],
    conflict_children: set[int],
) -> list[tuple[int, int, float, float]]:
    """Keep stable FSOT links; replace only conflicted / mislinked parents."""
    kept = [
        (s, t, p, d) for s, t, p, d in fsot_ft
        if s not in redo_parents and t not in conflict_children
    ]
    ml_by_parent: dict[int, list[tuple[int, int, float, float]]] = defaultdict(list)
    for e in ml_edges:
        if e[0] in redo_parents:
            ml_by_parent[e[0]].append(e)
    added: list[tuple[int, int, float, float]] = []
    for s in sorted(redo_parents):
        parent_ml = ml_by_parent.get(s, [])
        if parent_ml:
            added.extend(parent_ml)
        else:
            added.extend([(a, b, p, d) for a, b, p, d in fsot_ft if a == s])
    return kept + added


def _mitosis_dense_pairs(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
) -> set[tuple[int, int]]:
    """Frame pairs with multiple parents linking into a tight daughter cluster."""
    from fsot_cellular_bridge import MITOSIS_DAUGHTER_MAX_UM, phys_coords

    idx_t = {i: int(coords[i, 0]) for i in range(len(coords))}
    by_ft: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for s, t, _, _ in edges:
        ts, tt = idx_t.get(s, -9), idx_t.get(t, -9)
        if tt == ts + 1:
            by_ft[(ts, tt)].append((s, t))

    dense: set[tuple[int, int]] = set()
    for key, pairs in by_ft.items():
        if len(pairs) < 3:
            continue
        tgt_indices = list({t for _, t in pairs})
        if len(tgt_indices) < 2:
            continue
        cells = [{"z": float(coords[i, 1]), "y": float(coords[i, 2]), "x": float(coords[i, 3])}
                 for i in tgt_indices]
        pc = phys_coords(cells)
        diam = 0.0
        for i in range(len(pc)):
            for j in range(i + 1, len(pc)):
                diam = max(diam, float(np.linalg.norm(pc[i] - pc[j])))
        if diam <= MITOSIS_DAUGHTER_MAX_UM * 1.5 and len({s for s, _ in pairs}) >= 2:
            dense.add(key)
    return dense


def _parse_frame_list(env_key: str) -> set[int]:
    raw = os.environ.get(env_key, "").strip()
    return {int(x.strip()) for x in raw.split(",") if x.strip().isdigit()}


def _edges_on_frames(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
    frames: set[int],
) -> list[tuple[int, int, float, float]]:
    idx_t = {i: int(coords[i, 0]) for i in range(len(coords))}
    return [
        e for e in edges
        if idx_t.get(e[0], -9) in frames and idx_t.get(e[1], -9) == idx_t.get(e[0], -9) + 1
    ]


def _union_edges(
    primary: list[tuple[int, int, float, float]],
    extra: list[tuple[int, int, float, float]],
) -> list[tuple[int, int, float, float]]:
    best: dict[tuple[int, int], tuple[int, int, float, float]] = {}
    for e in primary:
        best[(e[0], e[1])] = e
    for e in extra:
        key = (e[0], e[1])
        if key not in best or e[2] > best[key][2]:
            best[key] = e
    return list(best.values())


def refine_fsot_edges_ml(
    coords: np.ndarray,
    edges: list[tuple[int, int, float, float]],
    model,
    device: torch.device,
    cfg: PredictConfig,
    ds_path: Path,
    *,
    downsample: tuple[int, ...] = (1, 4, 4),
    window_size: int = 2,
) -> list[tuple[int, int, float, float]]:
    """Re-assign division frame-pairs with transformer; keep other FSOT edges."""
    preserve_frames = _parse_frame_list("FSOT_ML_PRESERVE_FSOT_FRAMES")
    fsot_backup = _edges_on_frames(coords, edges, preserve_frames) if preserve_frames else []

    idx_t = {i: int(coords[i, 0]) for i in range(len(coords))}
    swap_children, by_ft = _swap_conflicts(coords, edges)

    refine_pairs: set[tuple[int, int]] = set()
    env_frames = os.environ.get("FSOT_ML_REFINE_FRAMES", "").strip()
    if env_frames:
        for tok in env_frames.split(","):
            if tok.strip().isdigit():
                t = int(tok.strip())
                refine_pairs.add((t, t + 1))
    refine_pairs |= _mitosis_dense_pairs(coords, edges)
    refine_pairs |= set(swap_children.keys())

    if not refine_pairs:
        return edges

    by_t = _idx_by_time(coords)
    pair_out: dict[tuple[int, int], list[tuple[int, int, float, float]]] = {}

    for t_src, t_tgt in sorted(refine_pairs):
        mode = _refine_mode_for_frame(t_src)
        idx_src = by_t.get(t_src, [])
        idx_tgt = by_t.get(t_tgt, [])
        fsot_ft = by_ft.get((t_src, t_tgt), [])
        if not idx_src or not idx_tgt:
            pair_out[(t_src, t_tgt)] = fsot_ft
            continue

        probs = _ml_edge_probs(
            model, device, cfg, ds_path, coords,
            idx_src, idx_tgt, t_src, t_tgt, downsample,
        )
        if probs is None:
            pair_out[(t_src, t_tgt)] = fsot_ft
            continue

        conflicts = swap_children.get((t_src, t_tgt), set())
        if mode == "merge":
            redo = _parents_needing_ml(fsot_ft, conflicts, probs, idx_src, idx_tgt, cfg)
            ml_edges = _ml_parent_top_edges(
                probs, idx_src, idx_tgt, coords, redo,
                max_children=int(os.environ.get("FSOT_ML_MAX_CHILDREN", "2")),
                min_prob=min(0.01, _refine_edge_threshold(cfg) * 0.5),
            )
            pair_edges = _merge_frame_edges(fsot_ft, ml_edges, redo, conflicts)
            pair_out[(t_src, t_tgt)] = pair_edges
            print(
                f"[ML-REFINE] t={t_src}->{t_tgt} mode=merge fsot={len(fsot_ft)} "
                f"redo={len(redo)} ml={len(ml_edges)} out={len(pair_edges)}"
            )
            continue

        ml_edges = _ml_greedy_pair_edges(
            model, device, cfg, ds_path, coords,
            idx_src, idx_tgt, t_src, t_tgt, downsample, probs=probs,
        )
        if os.environ.get("FSOT_ML_SUPPLEMENT_ARGMAX", "1") == "1":
            extra = _supplement_argmax_edges(probs, idx_src, idx_tgt, coords, ml_edges)
            if extra:
                ml_edges = ml_edges + extra
        if ml_edges:
            pair_out[(t_src, t_tgt)] = ml_edges
            print(
                f"[ML-REFINE] t={t_src}->{t_tgt} mode=replace fsot={len(fsot_ft)} "
                f"ml={len(ml_edges)}"
            )
        else:
            pair_out[(t_src, t_tgt)] = fsot_ft

    out: list[tuple[int, int, float, float]] = []
    for e in edges:
        key = (idx_t.get(e[0], -9), idx_t.get(e[1], -9))
        if key in pair_out:
            continue
        out.append(e)
    for key in sorted(pair_out):
        out.extend(pair_out[key])

    if fsot_backup:
        before = len(out)
        out = _union_edges(out, fsot_backup)
        print(
            f"[ML-REFINE] preserved FSOT on frames {sorted(preserve_frames)}: "
            f"{len(fsot_backup)} backup -> {len(out)} edges (was {before})"
        )

    print(f"[ML-REFINE] pairs={len(refine_pairs)} edges {len(edges)} -> {len(out)}")
    return out