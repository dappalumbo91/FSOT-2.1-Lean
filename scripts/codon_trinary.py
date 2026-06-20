"""FSOT 64-codon dual-axis trinary encoding — shared by ingest and verification.

Aligns with Genetics/codon_core/src/lib.rs and genomic_trinary.py:
  primary   (spin):     A,G = +1 ; C,T = -1
  secondary (genetic):  A = +1 ; T = -1 ; G,C = 0
"""

from __future__ import annotations

import itertools
import re
from pathlib import Path

PRIMARY_MAP: dict[str, int] = {"A": 1, "G": 1, "C": -1, "T": -1}
SECONDARY_MAP: dict[str, int] = {"A": 1, "T": -1, "G": 0, "C": 0}
VALID_BASES = frozenset("ACGT")
CODON_RE = re.compile(r"^([ACGT]{3})\s*\|\s*\[([-\d, ]+)\]\s*\|\s*\[([-\d, ]+)\]")

STANDARD_CODE: dict[str, str] = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def parse_triplet(text: str) -> tuple[int, int, int]:
    parts = [int(x.strip()) for x in text.split(",")]
    if len(parts) != 3:
        raise ValueError(f"expected 3 trits, got {text!r}")
    return parts[0], parts[1], parts[2]


def encode_codon(codon: str) -> dict:
    codon = codon.upper()
    if len(codon) != 3 or not all(b in VALID_BASES for b in codon):
        raise ValueError(f"invalid codon {codon!r}")
    primary = tuple(PRIMARY_MAP[b] for b in codon)
    secondary = tuple(SECONDARY_MAP[b] for b in codon)
    aa = STANDARD_CODE[codon]
    return {
        "codon": codon,
        "primary": primary,
        "secondary": secondary,
        "primary_key": ",".join(str(x) for x in primary),
        "secondary_key": ",".join(str(x) for x in secondary),
        "amino_acid": aa,
        "is_start": codon == "ATG",
        "is_stop": aa == "*",
    }


def all_codons() -> list[dict]:
    return [encode_codon("".join(bases)) for bases in itertools.product("ACGT", repeat=3)]


def summarize_codons(rows: list[dict]) -> dict:
    primary_patterns = {r["primary_key"] for r in rows}
    secondary_patterns = {r["secondary_key"] for r in rows}
    stop_codons = [r["codon"] for r in rows if r["is_stop"]]
    return {
        "codon_count": len(rows),
        "distinct_primary_patterns": len(primary_patterns),
        "distinct_secondary_patterns": len(secondary_patterns),
        "primary_pattern_space": 8,
        "secondary_pattern_space": 27,
        "stop_codon_count": len(stop_codons),
        "stop_codons": sorted(stop_codons),
        "start_codon": "ATG",
    }


def load_map_file(path: Path) -> dict[str, dict]:
    """Parse Genetics/64_codon_trinary_map.txt into {CODON: {primary, secondary}}."""
    out: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = CODON_RE.search(line)
        if not m:
            continue
        codon = m.group(1)
        out[codon] = {
            "primary": parse_triplet(m.group(2)),
            "secondary": parse_triplet(m.group(3)),
        }
    return out