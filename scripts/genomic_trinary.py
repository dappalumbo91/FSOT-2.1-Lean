"""FSOT genomic trinary signatures — shared by ingest and verification."""

from __future__ import annotations

GENETIC_MAP: dict[str, int] = {"A": 1, "T": -1, "G": 0, "C": 0}
SPIN_MAP: dict[str, int] = {"A": 1, "G": 1, "C": -1, "T": -1}
DNA_ALPHABET = frozenset("ATCG")


def normalized_entropy(sequence: str) -> float:
    if not sequence:
        return 0.0
    total = len(sequence)
    entropy = 0.0
    for base in DNA_ALPHABET:
        count = sequence.count(base)
        if count:
            probability = count / total
            entropy -= probability * __import__("math").log2(probability)
    return entropy / __import__("math").log2(len(DNA_ALPHABET))


def trinary_signatures(dna: str) -> dict:
    """Recompute FSOT trinary features from a dna_proxy sequence."""
    dna = dna.upper()
    genetic_vector = [GENETIC_MAP[base] for base in dna]
    spin_vector = [SPIN_MAP[base] for base in dna]
    length = max(len(dna), 1)
    gc_content = (dna.count("G") + dna.count("C")) / length
    superposition_ratio = genetic_vector.count(0) / length
    spin_balance = sum(spin_vector) / length
    counts = {
        "genetic_plus": genetic_vector.count(1),
        "genetic_zero": genetic_vector.count(0),
        "genetic_minus": genetic_vector.count(-1),
        "spin_plus": spin_vector.count(1),
        "spin_minus": spin_vector.count(-1),
    }
    return {
        "dna_length": len(dna),
        "codon_count": len(dna) // 3,
        "gc_content": gc_content,
        "entropy_norm": normalized_entropy(dna),
        "superposition_ratio": superposition_ratio,
        "spin_balance": spin_balance,
        "genetic_vector": genetic_vector,
        "spin_vector": spin_vector,
        "trinary_counts": counts,
    }