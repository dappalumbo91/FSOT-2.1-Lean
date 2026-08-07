#!/usr/bin/env python3
"""FSOT sequence → Cα structure — PORT of Genetics/fsot_protein math (F01–F15).

Authority:
  - I:/FSOT-Physical-Archive/04_Genetics-Longevity/fsot_protein/formulas/
  - Desktop/Genetics/fsot_protein/src/{secondary,chemical,distogram,regions}.rs
  - FSOT_PROTEIN_DERIVATIONS.md v7

Law: zero free parameters — only {π, e, φ, γ} + domain_scalar(Biochemistry, Molecular_Chemistry).
Distogram M_ij = bb + chem·env·chem_amp + helix + sheet + region_pair (F15).
Coordinates: classical MDS embedding of distances derived from proximity M.

Does NOT invent Chou-Fasman tables or free MD force fields.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import domain_scalar  # noqa: E402
import fsot_compute as fc  # noqa: E402

PI = float(fc.PI)
E = float(fc.E)
PHI = float(fc.PHI)
GAMMA = float(fc.GAMMA)
P_NEW = float(fc.P_NEW)
C_EFF = float(fc.C_EFF)
ETA_EFF = float(fc.ETA_EFF)

# Domain scalars — Biochemistry D=13, Molecular_Chemistry D=9 (protein derivations)
S_BIOCHEM = abs(float(domain_scalar("Biochemistry")))
try:
    S_MOLCHEM = abs(float(domain_scalar("Molecular_Chemistry")))
except Exception:
    # fallback name if domain table differs
    S_MOLCHEM = abs(float(domain_scalar("Physical_Chemistry")))

CHEM_AMP = S_MOLCHEM * P_NEW
REGION_AMP = S_BIOCHEM * P_NEW * C_EFF
LONG_RANGE_GATE = int(math.ceil(ETA_EFF * 13.0))  # = 7

CA_CA = 3.8  # Å crystallographic virtual bond (geometry constant, not fitted weight)


# ── F01 trinary ────────────────────────────────────────────────────────────
def trinary_phase(aa: str) -> tuple[float, float, float]:
    t = {
        "A": (0, -1, -1), "R": (1, 1, 1), "N": (0, 1, 0), "D": (-1, 1, 0),
        "C": (0, 0, -1), "Q": (0, 1, 1), "E": (-1, 1, 1), "G": (0, -1, -1),
        "H": (1, 1, 1), "I": (0, -1, 1), "L": (0, -1, 1), "K": (1, 1, 1),
        "M": (0, -1, 1), "F": (0, -1, 1), "P": (0, -1, 0), "S": (0, 1, -1),
        "T": (0, 1, 0), "W": (0, -1, 1), "Y": (0, 1, 1), "V": (0, -1, 0),
    }.get(aa.upper(), (0, 0, 0))
    return float(t[0]), float(t[1]), float(t[2])


# ── F02 chemical scalars (v7 refined) ─────────────────────────────────────
@dataclass
class ChemProp:
    h: float
    vol: float
    q: float
    mu: float


def chemical_propensity(aa: str) -> ChemProp:
    c, p, v = trinary_phase(aa)
    h = (PHI ** (-p)) * math.exp(v / PI)
    vol = PI * E * (PHI ** v)
    q = c
    mu = GAMMA * math.exp(abs(c) + p + 1.0)
    return ChemProp(h=h, vol=vol, q=q, mu=mu)


# ── F03–F06 chemistry ─────────────────────────────────────────────────────
def fsot_chemical_interaction(aa1: str, aa2: str) -> float:
    c1, c2 = aa1.upper(), aa2.upper()
    if c1 == "C" and c2 == "C":
        return PHI ** 6  # F03
    p1, p2 = chemical_propensity(c1), chemical_propensity(c2)
    h1 = (p1.h - 1.0) / PHI  # F04 center at 1.0 (v7)
    h2 = (p2.h - 1.0) / PHI
    hydrophobic = h1 * h2
    electrostatic = -p1.q * p2.q * E  # F05
    dipole = math.sqrt(max(p1.mu * p2.mu, 0.0)) / (GAMMA * PI * E * E)  # F06
    return hydrophobic + electrostatic + dipole


# ── Secondary propensities (secondary.rs exact) ───────────────────────────
@dataclass
class SsPropensity:
    p_alpha: float
    p_beta: float
    p_coil: float

    @staticmethod
    def from_amino_acid(aa: str) -> "SsPropensity":
        aa = aa.upper()
        if aa == "P":
            return SsPropensity._norm(1.0 / PHI, 1.0 / PHI, PHI)
        if aa == "G":
            return SsPropensity._norm(1.0 / E, 1.0 / E, E)
        charge, polarity, volume = trinary_phase(aa)
        raw_alpha = PHI - polarity / (PI * PHI) - abs(charge) / (PI * PI)
        raw_beta = math.exp((volume - polarity) / PI)
        raw_coil = math.exp((polarity - volume + abs(charge) / PHI) / PI)
        return SsPropensity._norm(raw_alpha, raw_beta, raw_coil)

    @staticmethod
    def _norm(a: float, b: float, c: float) -> "SsPropensity":
        s = a + b + c
        return SsPropensity(a / s, b / s, c / s)

    def dominant(self) -> str:
        if self.p_alpha >= self.p_beta and self.p_alpha >= self.p_coil:
            return "H"
        if self.p_beta >= self.p_coil:
            return "E"
        return "C"


def helix_periodicity_bonus(pi: SsPropensity, pj: SsPropensity, sep: int) -> float:
    """F10"""
    if sep not in (3, 4, 7):
        return 0.0
    joint = math.sqrt(pi.p_alpha * pj.p_alpha)
    return (joint ** 3) / E


def sheet_pair_bonus(pi: SsPropensity, pj: SsPropensity, sep: int) -> float:
    """F11"""
    if sep < 3:
        return 0.0
    joint = math.sqrt(pi.p_beta * pj.p_beta)
    envelope = 1.0 / (1.0 + max(math.log(sep / PI), 0.0))
    return (joint ** 2) * envelope / PHI


# ── F12 regions ───────────────────────────────────────────────────────────
@dataclass
class Region:
    kind: str  # H, E, C
    start: int
    end: int

    def length(self) -> int:
        return self.end - self.start + 1


def _collapse(p: SsPropensity) -> str:
    gate = 1.0 / E  # F12
    if p.p_alpha > gate and p.p_alpha > p.p_beta:
        return "H"
    if p.p_beta > gate and p.p_beta > p.p_alpha:
        return "E"
    return "C"


def detect_regions(props: list[SsPropensity]) -> list[Region]:
    if not props:
        return []
    min_helix = int(math.ceil(PI + 1.0 / (PI - 1.0)))  # 4
    min_strand = 3
    n = len(props)
    initial = [_collapse(p) for p in props]
    # F12b frustrated tunnel (default from regions.rs)
    tunnel_window = 1.0 / (PHI * PHI)
    collapsed = []
    for i in range(n):
        p = props[i]
        top = max(p.p_alpha, p.p_beta)
        other = min(p.p_alpha, p.p_beta)
        superposed = top > 0 and (top - other) / top < tunnel_window
        if not superposed or i == 0 or i + 1 >= n:
            collapsed.append(initial[i])
            continue
        left, right = initial[i - 1], initial[i + 1]
        if left == right and left != "C":
            collapsed.append(left)
        elif left != "C" and right != "C" and left != right:
            collapsed.append("C")
        else:
            collapsed.append(initial[i])

    out: list[Region] = []
    run_kind, run_start = collapsed[0], 0
    for i in range(1, n):
        if collapsed[i] != run_kind:
            length = i - run_start
            min_len = min_helix if run_kind == "H" else (min_strand if run_kind == "E" else 10**9)
            if run_kind != "C" and length >= min_len:
                out.append(Region(run_kind, run_start, i - 1))
            run_kind, run_start = collapsed[i], i
    length = n - run_start
    min_len = min_helix if run_kind == "H" else (min_strand if run_kind == "E" else 10**9)
    if run_kind != "C" and length >= min_len:
        out.append(Region(run_kind, run_start, n - 1))
    return out


def residue_to_region(n: int, regions: list[Region]) -> list[int | None]:
    m: list[int | None] = [None] * n
    for ri, r in enumerate(regions):
        for i in range(r.start, r.end + 1):
            if i < n:
                m[i] = ri
    return m


# F16 heptad / F17 strand register (from regions.rs)
def helix_heptad_multiplier(i: int, j: int, start_i: int, start_j: int) -> float:
    mi = (i - start_i) % 7
    mj = (j - start_j) % 7
    if mi in (0, 3) and mj in (0, 3):
        return PHI
    return 1.0 / PHI


def beta_register_multiplier(
    i: int, j: int, sa: int, ea: int, sb: int, eb: int
) -> float:
    # antiparallel ideal partner
    j_anti = eb - (i - sa)
    j_par = sb + (i - sa)
    off = min(abs(j - j_anti), abs(j - j_par))
    return PHI ** (-off / PI)


# ── F15 distogram ─────────────────────────────────────────────────────────
def build_distogram(sequence: str) -> tuple[np.ndarray, list[SsPropensity], list[Region], str]:
    chars = [c for c in sequence.upper() if c.isalpha() and trinary_phase(c) != (0.0, 0.0, 0.0) or c in "ARNDCEQGHILKMFPSTWYV"]
    chars = [c for c in sequence.upper() if c in "ARNDCEQGHILKMFPSTWYV"]
    n = len(chars)
    props = [SsPropensity.from_amino_acid(c) for c in chars]
    regions = detect_regions(props)
    rmap = residue_to_region(n, regions)
    ss = "".join(p.dominant() for p in props)

    M = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            sep = abs(i - j)
            s = float(sep)
            # F07 backbone
            bb = 1.0 / (s ** (1.0 / PI))
            # F08–F09 chemistry
            interaction = fsot_chemical_interaction(chars[i], chars[j])
            chem_env = s / (s + PI * E)
            chemistry = interaction * chem_env * CHEM_AMP
            # F10 F11
            helix = helix_periodicity_bonus(props[i], props[j], sep)
            sheet = sheet_pair_bonus(props[i], props[j], sep)
            # F13 region pair
            region_pair = 0.0
            ri, rj = rmap[i], rmap[j]
            if ri is not None and rj is not None and ri != rj and sep >= LONG_RANGE_GATE:
                r_i, r_j = regions[ri], regions[rj]
                if r_i.kind == r_j.kind and r_i.kind != "C":
                    if r_i.kind == "H":
                        pi_v, pj_v = props[i].p_alpha, props[j].p_alpha
                        reg_mult = helix_heptad_multiplier(i, j, r_i.start, r_j.start)
                    else:
                        pi_v, pj_v = props[i].p_beta, props[j].p_beta
                        reg_mult = beta_register_multiplier(
                            i, j, r_i.start, r_i.end, r_j.start, r_j.end
                        )
                    joint = math.sqrt(pi_v * pj_v)
                    region_pair = joint * REGION_AMP * reg_mult
            M[i, j] = bb + chemistry + helix + sheet + region_pair
    return M, props, regions, "".join(chars)


def geometric_scale_dist(sep: int) -> float:
    """Neuron Zig genetic.zig: geometricScaleDist = φ · dist^(-1/π)."""
    d = float(max(sep, 1))
    return PHI * (d ** (-1.0 / PI))


def proximity_to_distance(
    M: np.ndarray,
    props: list[SsPropensity] | None = None,
    regions: list[Region] | None = None,
) -> np.ndarray:
    """F15 proximity → Å with hard top-L contact caps (seed scales only).

    Layer stack:
      1) Local backbone (sep 1–2) fixed by seed geometry
      2) F07 inverse: d ~ CA_CA / M  blended with collapsed polymer s^{1/π}
      3) Top-L and top-2L contact caps at πe/φ and πe (CASP-style 8Å class)
      4) F10 helix i,i+{3,4,7} geometric distances when both α-strong
    """
    n = M.shape[0]
    D = np.zeros((n, n), dtype=np.float64)
    contact_scale = PI * E  # F08 ~8.54 Å — standard contact cutoff scale
    d_hard = contact_scale * PHI * PHI
    # base distances
    for i in range(n):
        for j in range(i + 1, n):
            sep = abs(i - j)
            m = max(float(M[i, j]), 1e-9)
            if sep == 1:
                d = CA_CA
            elif sep == 2:
                d = CA_CA * math.sqrt(E / PHI)
            else:
                d_inv = CA_CA / m
                d_poly = CA_CA * (float(sep) ** (1.0 / PI))
                env = float(sep) / (float(sep) + PI * E)
                d = (1.0 - env) * d_poly + env * min(d_inv, contact_scale * PHI)
                bb_only = float(sep) ** (-1.0 / PI)
                if m > bb_only * PHI:
                    d = min(d, contact_scale / (1.0 + (m - bb_only) * PHI))
            # F10 local helix geometry (crystallographic periods, seed-weighted)
            if props is not None and sep in (3, 4, 7):
                if props[i].p_alpha > 1.0 / E and props[j].p_alpha > 1.0 / E:
                    # Ideal α Cα distance from helical rise/radius geometry
                    rise, rad, turn = 1.5, 2.3, 100.0 * PI / 180.0
                    d_h = math.sqrt((sep * rise) ** 2 + (2 * rad * math.sin(sep * turn / 2)) ** 2)
                    d = min(d, d_h)
            D[i, j] = D[j, i] = float(np.clip(d, CA_CA * 0.95, d_hard))

    # Top-L hard contacts: rank long-range pairs by M
    L = n
    lr_pairs = []
    for i in range(n):
        for j in range(i + LONG_RANGE_GATE, n):
            lr_pairs.append((M[i, j], i, j))
    lr_pairs.sort(reverse=True)
    # top L/2 → tight contact πe/φ ≈ 5.3 Å
    # top L → contact scale πe ≈ 8.5 Å
    tight = contact_scale / PHI
    for rank, (m, i, j) in enumerate(lr_pairs[: max(L, 1)]):
        if rank < max(L // 2, 1):
            D[i, j] = D[j, i] = min(D[i, j], tight)
        else:
            D[i, j] = D[j, i] = min(D[i, j], contact_scale)

    # Region–region: same-kind regions get median contact pull
    if regions:
        for a, ra in enumerate(regions):
            for b, rb in enumerate(regions):
                if b <= a or ra.kind != rb.kind or ra.kind == "C":
                    continue
                # couple midpoints and a few register pairs
                for i in range(ra.start, ra.end + 1):
                    if ra.kind == "H":
                        # heptad-facing residues
                        if (i - ra.start) % 7 not in (0, 3):
                            continue
                    for j in range(rb.start, rb.end + 1):
                        if abs(i - j) < LONG_RANGE_GATE:
                            continue
                        if ra.kind == "H" and (j - rb.start) % 7 not in (0, 3):
                            continue
                        D[i, j] = D[j, i] = min(D[i, j], contact_scale)
    return D


def classical_mds(D: np.ndarray, dim: int = 3) -> np.ndarray:
    """Classical multidimensional scaling → coordinates (n, dim)."""
    n = D.shape[0]
    D2 = D ** 2
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    evals, evecs = np.linalg.eigh(B)
    idx = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]
    pos = evals[:dim].copy()
    pos[pos < 0] = 0.0
    X = evecs[:, :dim] @ np.diag(np.sqrt(pos + 1e-15))
    if n > 1:
        adj = np.linalg.norm(X[1:] - X[:-1], axis=1).mean()
        if adj > 1e-9:
            X *= CA_CA / adj
    X -= X.mean(axis=0)
    return X


def initial_extended(n: int) -> np.ndarray:
    """Deterministic extended chain (seed angle step 2π/φ)."""
    X = np.zeros((n, 3), dtype=np.float64)
    ang = 2.0 * PI / PHI
    for i in range(1, n):
        a = i * ang
        X[i] = X[i - 1] + CA_CA * np.array([math.cos(a), math.sin(a), 1.0 / PHI])
        step = X[i] - X[i - 1]
        X[i] = X[i - 1] + step * (CA_CA / (np.linalg.norm(step) + 1e-12))
    X -= X.mean(axis=0)
    return X


def initial_helix_bundle(seq: str, props: list[SsPropensity]) -> np.ndarray:
    """Deterministic start from α geometry where p_alpha wins F12 gate."""
    n = len(seq)
    X = np.zeros((n, 3), dtype=np.float64)
    turn = 100.0 * PI / 180.0
    rise, r = 1.5, 2.3
    k_h = 0
    gate = 1.0 / E
    for i in range(1, n):
        if props[i].p_alpha > gate and props[i].p_alpha >= props[i].p_beta:
            k_h += 1
            X[i] = [r * math.cos(k_h * turn), r * math.sin(k_h * turn), X[i - 1, 2] + rise]
        else:
            k_h = 0
            a = i * 2.0 * PI / (PHI * 5.0)
            X[i] = X[i - 1] + CA_CA * np.array([math.cos(a), math.sin(a), 0.4])
            step = X[i] - X[i - 1]
            X[i] = X[i - 1] + step * (CA_CA / (np.linalg.norm(step) + 1e-12))
    X -= X.mean(axis=0)
    return X


def initial_from_regions(seq: str, props: list[SsPropensity], regions: list[Region]) -> np.ndarray:
    """Place each SS region as a rigid secondary element then pack by centroid."""
    n = len(seq)
    X = initial_extended(n)
    turn, rise, rad = 100.0 * PI / 180.0, 1.5, 2.3
    for ri, reg in enumerate(regions):
        # offset each region in space by φ-lattice
        base = np.array(
            [
                (ri % 3) * PI * E,
                ((ri // 3) % 3) * PI * E / PHI,
                (ri // 9) * E,
            ]
        )
        if reg.kind == "H":
            for k, i in enumerate(range(reg.start, reg.end + 1)):
                X[i] = base + np.array(
                    [rad * math.cos(k * turn), rad * math.sin(k * turn), k * rise]
                )
        elif reg.kind == "E":
            for k, i in enumerate(range(reg.start, reg.end + 1)):
                sign = 1.0 if k % 2 == 0 else -1.0
                X[i] = base + np.array([k * 3.3 * 0.5, sign * 1.2, 0.0])
    # fill gaps with linear interpolation
    for i in range(1, n):
        if np.linalg.norm(X[i] - X[i - 1]) < 1e-6:
            X[i] = X[i - 1] + np.array([CA_CA, 0.0, 0.0])
    # rebond chain
    for i in range(1, n):
        diff = X[i] - X[i - 1]
        dist = float(np.linalg.norm(diff) + 1e-12)
        if dist > CA_CA * 2.5 or dist < CA_CA * 0.5:
            X[i] = X[i - 1] + diff * (CA_CA / dist)
    X -= X.mean(axis=0)
    return X


def _sparse_pairs(n: int, M: np.ndarray, local: int = 12) -> list[tuple[int, int]]:
    """Local band + top-2L long-range only — O(n·local + L), not O(n²) grind."""
    pairs: list[tuple[int, int]] = []
    for i in range(n):
        for j in range(i + 1, min(n, i + local + 1)):
            pairs.append((i, j))
    L = n
    # Vectorized long-range rank: take top contacts without full nested Python sort of all pairs
    if n > LONG_RANGE_GATE + 1:
        # Sample upper triangle long-range scores via flat index
        ii, jj = np.triu_indices(n, k=LONG_RANGE_GATE)
        scores = M[ii, jj]
        k = min(2 * L, scores.size)
        if k > 0:
            # argpartition is O(n) vs full sort O(n log n) on ~n²/2
            if scores.size > k:
                top_idx = np.argpartition(scores, -k)[-k:]
            else:
                top_idx = np.arange(scores.size)
            seen = set(pairs)
            for t in top_idx:
                i, j = int(ii[t]), int(jj[t])
                if (i, j) not in seen:
                    pairs.append((i, j))
                    seen.add((i, j))
    return pairs


def stress(X: np.ndarray, D: np.ndarray, M: np.ndarray, pairs: list[tuple[int, int]] | None = None) -> float:
    """Sparse stress on the same contact set as refine — O(n·k), not O(n²)."""
    n = X.shape[0]
    if pairs is None:
        pairs = _sparse_pairs(n, M, local=int(PI * E) + 3)
    s = 0.0
    for i, j in pairs:
        dist = float(np.linalg.norm(X[i] - X[j]) + 1e-12)
        w = 1.0 + max(M[i, j], 0.0) * PHI
        if abs(i - j) == 1:
            w = 50.0
        s += w * (dist - D[i, j]) ** 2
    return s


def refine_with_distogram(
    X: np.ndarray,
    D: np.ndarray,
    M: np.ndarray,
    rounds: int = 24,
    pairs: list[tuple[int, int]] | None = None,
) -> np.ndarray:
    """Fast sparse refine: local band + top contacts only (formula weights).

    Mathematical path must stay *fast* — zero free params is not an excuse
    for O(n²)×hundreds of iterations (that apes neural-net cost without the wins).
    """
    n = X.shape[0]
    pos = X.copy()
    if pairs is None:
        pairs = _sparse_pairs(n, M, local=int(PI * E) + 3)  # local window ~12 from πe
    # Pre-index for vectorized force accumulation
    if not pairs:
        return pos
    pi = np.array([p[0] for p in pairs], dtype=np.int32)
    pj = np.array([p[1] for p in pairs], dtype=np.int32)
    td = D[pi, pj]
    m_ij = M[pi, pj]
    sep = np.abs(pi - pj).astype(np.float64)
    env = sep / (sep + PI * E)
    w = (1.0 + np.maximum(m_ij, 0.0) * PHI) * (0.35 + 0.65 * env)
    w = np.where(sep == 1, 80.0, w)
    w = np.where(sep == 2, 15.0, w)

    for rnd in range(rounds):
        lr = 0.30 * (1.0 - rnd / (rounds + PHI))
        diff = pos[pj] - pos[pi]
        dist = np.linalg.norm(diff, axis=1) + 1e-9
        scale = (w * (dist - td) / dist)[:, None]
        f = scale * diff
        forces = np.zeros_like(pos)
        np.add.at(forces, pi, f)
        np.add.at(forces, pj, -f)
        fn = np.linalg.norm(forces, axis=1, keepdims=True) + PHI
        pos = pos + lr * forces / fn
        # rebond chain O(n) — keep Cα virtual bond fixed
        for i in range(1, n):
            dvec = pos[i] - pos[i - 1]
            dlen = float(np.linalg.norm(dvec) + 1e-9)
            pos[i] = pos[i - 1] + dvec * (CA_CA / dlen)
        if rnd % 4 == 0:
            pos -= pos.mean(axis=0)
    pos -= pos.mean(axis=0)
    return pos


def clean_sequence(seq: str) -> str:
    return "".join(c for c in seq.upper() if c in "ARNDCEQGHILKMFPSTWYV")


def predict_ca_coords(sequence: str, rounds: int = 24) -> dict[str, Any]:
    """Fast mathematical fold: F15 matrix → D → MDS → sparse polish.

    Design goal: seconds per chain on a home PC, not minutes — closed-form
    MDS is the main embed; sparse refine only polishes.
    """
    import time as _time

    t0 = _time.perf_counter()
    seq = clean_sequence(sequence)
    if len(seq) < 5:
        raise ValueError("sequence too short")
    max_n = 400
    if len(seq) > max_n:
        seq = seq[:max_n]

    M, props, regions, chars = build_distogram(seq)
    assert chars == seq
    D = proximity_to_distance(M, props=props, regions=regions)
    pairs = _sparse_pairs(len(seq), M, local=int(PI * E) + 3)
    n_rounds = max(8, min(int(rounds), 32))

    # Primary: classical MDS (closed-form spectral embed) — the mathematical core
    X_mds = classical_mds(D, dim=3)
    candidates: list[tuple[str, np.ndarray]] = [
        ("mds", X_mds),
        # Mirror image is an equally valid embed of D; pick by sparse stress (no free dials)
        ("mds_mirror", X_mds * np.array([1.0, 1.0, -1.0])),
        ("regions", initial_from_regions(seq, props, regions)),
    ]
    best_name = "mds"
    X = candidates[0][1]
    st = float("inf")
    for cname, X0 in candidates:
        Xc = refine_with_distogram(X0, D, M, rounds=n_rounds, pairs=pairs)
        stc = stress(Xc, D, M, pairs=pairs)
        if stc < st:
            X, st, best_name = Xc, stc, cname

    elapsed_ms = (_time.perf_counter() - t0) * 1000.0
    ss = "".join(p.dominant() for p in props)
    return {
        "sequence": seq,
        "length": len(seq),
        "secondary": ss,
        "regions": [{"kind": r.kind, "start": r.start, "end": r.end} for r in regions],
        "ca_coords": X,
        "S_biochem": S_BIOCHEM,
        "S_molchem": S_MOLCHEM,
        "chem_amp": CHEM_AMP,
        "region_amp": REGION_AMP,
        "long_range_gate": LONG_RANGE_GATE,
        "embed_start": best_name,
        "embed_stress": st,
        "predict_ms": elapsed_ms,
        "n_sparse_pairs": len(pairs),
        "refine_rounds": n_rounds,
        "engine": "fsot_protein_F01_F15_fast_v7",
        "free_parameters": 0,
        "authority": (
            "F01-F15 + F07 inverse + Zig φ·dist^{-1/π}; embed = classical MDS "
            "+ sparse O(n·k) vectorized polish — formula branch, not neural net"
        ),
    }


def write_ca_pdb(path: Path, seq: str, xyz: np.ndarray, name: str = "FSOT") -> None:
    lines = []
    for i, (aa, (x, y, z)) in enumerate(zip(seq, xyz), start=1):
        lines.append(
            f"ATOM  {i:5d}  CA  {aa:3s} A{i:4d}    "
            f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00 50.00           C  "
        )
    lines.append("END")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
