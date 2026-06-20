"""FSOT protein amino-acid trinary phases — shared by ingest and verification."""

from __future__ import annotations

# Source of truth: Genetics/fsot_protein/src/secondary.rs :: trinary_phase
# [Charge, Polarity, Volume] in {-1, 0, +1}
AMINO_ACID_TRINARY: dict[str, tuple[int, int, int]] = {
    "A": (0, -1, -1),
    "R": (1, 1, 1),
    "N": (0, 1, 0),
    "D": (-1, 1, 0),
    "C": (0, 0, -1),
    "Q": (0, 1, 1),
    "E": (-1, 1, 1),
    "G": (0, -1, -1),
    "H": (1, 1, 1),
    "I": (0, -1, 1),
    "L": (0, -1, 1),
    "K": (1, 1, 1),
    "M": (0, -1, 1),
    "F": (0, -1, 1),
    "P": (0, -1, 0),
    "S": (0, 1, -1),
    "T": (0, 1, 0),
    "W": (0, -1, 1),
    "Y": (0, 1, 1),
    "V": (0, -1, 0),
}

AMINO_ACID_NAMES: dict[str, str] = {
    "A": "Alanine",
    "R": "Arginine",
    "N": "Asparagine",
    "D": "Aspartic Acid",
    "C": "Cysteine",
    "Q": "Glutamine",
    "E": "Glutamic Acid",
    "G": "Glycine",
    "H": "Histidine",
    "I": "Isoleucine",
    "L": "Leucine",
    "K": "Lysine",
    "M": "Methionine",
    "F": "Phenylalanine",
    "P": "Proline",
    "S": "Serine",
    "T": "Threonine",
    "W": "Tryptophan",
    "Y": "Tyrosine",
    "V": "Valine",
}

VALID_TRITS = frozenset((-1, 0, 1))


def pattern_key(phase: tuple[int, int, int]) -> str:
    return f"{phase[0]},{phase[1]},{phase[2]}"


def summarize_phases() -> dict:
    patterns = {pattern_key(v) for v in AMINO_ACID_TRINARY.values()}
    return {
        "amino_acid_count": len(AMINO_ACID_TRINARY),
        "distinct_trinary_patterns": len(patterns),
        "pattern_space_size": 27,
        "patterns": sorted(patterns),
    }