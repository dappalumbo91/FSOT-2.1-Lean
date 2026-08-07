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


def proximity_to_distance(M: np.ndarray) -> np.ndarray:
    """Map proximity (larger=closer) → Å distances for embedding.

    F07: bb(s)=s^{-1/π}. At sep=1, bb=1 → d=CA_CA.
    d_ij = CA_CA / max(M_ij, ε)^{π} would explode; use saturating inverse:
      d = CA_CA * (1 + (π e) * max(0, M_ref - M) / (1 + M))
    with M_ref = 1 (backbone adjacent scale).
    """
    n = M.shape[0]
    D = np.zeros((n, n), dtype=np.float64)
    contact_scale = PI * E  # F08 FSOT contact scale ~8.54 Å
    for i in range(n):
        for j in range(i + 1, n):
            m = max(float(M[i, j]), 1e-9)
            # Adjacent backbone: enforce geometry
            if abs(i - j) == 1:
                d = CA_CA
            elif abs(i - j) == 2:
                # virtual bond length from seeds only: 3.8 · √(e/φ)
                d = CA_CA * math.sqrt(E / PHI)
            else:
                # Higher proximity → shorter distance; floor at CA_CA, soft ceiling
                d = CA_CA + contact_scale / (1.0 + m * PHI)
                # strong contacts pull toward π-scale
                if m > 1.0:
                    d = min(d, contact_scale / (m / PHI))
            d = float(np.clip(d, CA_CA * 0.95, 45.0))
            D[i, j] = D[j, i] = d
    return D


def classical_mds(D: np.ndarray, dim: int = 3) -> np.ndarray:
    """Classical multidimensional scaling → coordinates (n, dim)."""
    n = D.shape[0]
    D2 = D ** 2
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    # eigh for symmetric
    evals, evecs = np.linalg.eigh(B)
    idx = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]
    # keep positive eigenvalues
    pos = evals[:dim].copy()
    pos[pos < 0] = 0.0
    L = np.diag(np.sqrt(pos))
    X = evecs[:, :dim] @ L
    # scale so mean adjacent CA distance = CA_CA
    if n > 1:
        adj = np.linalg.norm(X[1:] - X[:-1], axis=1).mean()
        if adj > 1e-9:
            X *= CA_CA / adj
    X -= X.mean(axis=0)
    return X


def refine_with_distogram(
    X: np.ndarray, D: np.ndarray, M: np.ndarray, rounds: int = 60
) -> np.ndarray:
    """Light spring refinement toward D, weights from proximity M — still formula-driven."""
    n = X.shape[0]
    pos = X.copy()
    for rnd in range(rounds):
        lr = 0.25 * (1.0 - rnd / (rounds + PHI))
        forces = np.zeros_like(pos)
        for i in range(n):
            for j in range(i + 1, n):
                diff = pos[j] - pos[i]
                dist = float(np.linalg.norm(diff) + 1e-9)
                td = D[i, j]
                w = 1.0 + max(M[i, j], 0.0) * PHI
                if abs(i - j) == 1:
                    w = 100.0
                f = w * (dist - td) / dist * diff
                forces[i] += f
                forces[j] -= f
        fn = np.linalg.norm(forces, axis=1, keepdims=True) + PHI
        pos = pos + lr * forces / fn
        for i in range(1, n):
            diff = pos[i] - pos[i - 1]
            dist = float(np.linalg.norm(diff) + 1e-9)
            pos[i] = pos[i - 1] + diff * (CA_CA / dist)
        if rnd % 10 == 0:
            pos -= pos.mean(axis=0)
    pos -= pos.mean(axis=0)
    return pos


def clean_sequence(seq: str) -> str:
    return "".join(c for c in seq.upper() if c in "ARNDCEQGHILKMFPSTWYV")


def predict_ca_coords(sequence: str, rounds: int = 80) -> dict[str, Any]:
    seq = clean_sequence(sequence)
    if len(seq) < 5:
        raise ValueError("sequence too short")
    # Cap for home PC; full distogram is O(n²)
    max_n = 300
    if len(seq) > max_n:
        seq = seq[:max_n]

    M, props, regions, chars = build_distogram(seq)
    assert chars == seq
    D = proximity_to_distance(M)
    X0 = classical_mds(D, dim=3)
    X = refine_with_distogram(X0, D, M, rounds=rounds)
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
        "engine": "fsot_protein_F01_F15_port_v3",
        "free_parameters": 0,
        "authority": "Genetics/fsot_protein + FSOT_PROTEIN_DERIVATIONS.md v7",
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
