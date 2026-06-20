"""FSOT protein formula closed forms — shared by ingest and verification."""

from __future__ import annotations

import math

from protein_trinary import AMINO_ACID_TRINARY

PI = math.pi
E = math.e
PHI = (1 + math.sqrt(5)) / 2
GAMMA = 0.5772156649015329

FORMULA_IDS = [
    "F01_amino_acid_trinary_phase",
    "F02_aa_chemical_scalar_table",
    "F03_disulfide_bridge",
    "F04_hydrophobic_interaction",
    "F05_electrostatic_interaction",
    "F06_dipole_interaction",
    "F07_backbone_proximity",
    "F08_chemistry_envelope",
    "F09_chemistry_amplitude",
    "F10_helix_periodicity_bonus",
    "F11_sheet_pair_bonus",
    "F12_region_detection_gate",
    "F13_region_pair_contact",
    "F14_long_range_gate",
    "F15_distogram_assembly",
]

PROPOSED_FORMULA_IDS = [
    "F16_heptad_register",
    "F17_strand_register",
    "F18_disulfide_geometry_gate",
]


def chemical_propensity(letter: str) -> dict[str, float]:
    c, p, v = AMINO_ACID_TRINARY[letter]
    h = PHI ** (-p) * math.exp(v / PI)
    vol = PI * E * (PHI ** v)
    q = float(c)
    mu = GAMMA * math.exp(abs(c) + p + 1.0)
    return {
        "hydrophobicity_fsot": h,
        "volume_fsot": vol,
        "charge": q,
        "dipole_moment": mu,
    }


def disulfide_bridge() -> float:
    return PHI ** 6


def hydrophobic_term(aa1: str, aa2: str) -> float:
    p1 = chemical_propensity(aa1)
    p2 = chemical_propensity(aa2)
    h1 = (p1["hydrophobicity_fsot"] - 1.0) / PHI
    h2 = (p2["hydrophobicity_fsot"] - 1.0) / PHI
    return h1 * h2


def electrostatic_term(aa1: str, aa2: str) -> float:
    p1 = chemical_propensity(aa1)
    p2 = chemical_propensity(aa2)
    return -p1["charge"] * p2["charge"] * E


def dipole_term(aa1: str, aa2: str) -> float:
    p1 = chemical_propensity(aa1)
    p2 = chemical_propensity(aa2)
    return math.sqrt(p1["dipole_moment"] * p2["dipole_moment"]) / (GAMMA * PI * E * E)


def fsot_chemical_interaction(aa1: str, aa2: str) -> float:
    if aa1 == "C" and aa2 == "C":
        return disulfide_bridge()
    return hydrophobic_term(aa1, aa2) + electrostatic_term(aa1, aa2) + dipole_term(aa1, aa2)


def dipole_damping_denominator() -> float:
    return GAMMA * PI * E * E