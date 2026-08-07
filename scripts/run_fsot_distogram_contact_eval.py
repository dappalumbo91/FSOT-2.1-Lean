#!/usr/bin/env python3
"""Evaluate FSOT F15 distogram the way the protein stack was designed:

Contact / long-range ranking metrics vs experimental PDB Cα distances
(Pearson, Top-L, LR@|i-j|≥6) — not ad-hoc RMSD embedding.

Authority: FSOT_PROTEIN_DERIVATIONS.md v7 benchmark table (1UBQ, 1CRN, …).

  python scripts/run_fsot_distogram_contact_eval.py
"""

from __future__ import annotations

import json
import math
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_structure_engine import build_distogram, clean_sequence  # noqa: E402
from run_fsot_vs_alphafold_structure import (  # noqa: E402
    fetch_pdb,
    fetch_uniprot_sequence,
    parse_pdb_ca,
    _store,
)

OUT_JSON = ROOT / "data" / "fsot_distogram_contact_eval.json"
OUT_MD = ROOT / "predictions" / "reports" / "FSOT_DISTOGRAM_CONTACT_EVAL.md"

# Classic CASP-style short targets used in protein derivations
TARGETS = [
    ("P62988", "1UBQ", "A", "Ubiquitin"),
    ("P01542", "1CRN", "A", "Crambin"),
    ("P03069", "1VII", "A", "Villin headpiece"),
    ("P06654", "2GB1", "A", "Protein G B1"),
    ("P09017", "1ENH", "A", "Engrailed homeodomain"),
]


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    x = x - x.mean()
    y = y - y.mean()
    d = np.sqrt((x * x).sum() * (y * y).sum())
    if d < 1e-15:
        return 0.0
    return float((x * y).sum() / d)


def contact_metrics(M: np.ndarray, Dtrue: np.ndarray, seq_len: int, contact_A: float = 8.0) -> dict:
    """M = proximity (higher better); Dtrue = experimental Cα distances."""
    n = M.shape[0]
    n = min(n, Dtrue.shape[0])
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j, M[i, j], Dtrue[i, j], abs(i - j)))
    # true contact label
    prox = np.array([p[2] for p in pairs])
    # inverse distance as continuous target (higher = closer)
    invd = np.array([1.0 / max(p[3], 1e-3) for p in pairs])
    contacts = [p for p in pairs if p[3] < contact_A]
    r = pearson(prox, invd)

    # Top-L: top L predicted pairs by M, fraction true contacts
    L = seq_len
    ranked = sorted(pairs, key=lambda t: t[2], reverse=True)
    top = ranked[:L]
    top_hit = sum(1 for t in top if t[3] < contact_A) / max(L, 1)

    # Long-range top L/2 with |i-j|≥6
    lr = [p for p in pairs if p[4] >= 6]
    lr_ranked = sorted(lr, key=lambda t: t[2], reverse=True)
    lr_L = max(L // 2, 1)
    lr_top = lr_ranked[:lr_L]
    lr_hit = sum(1 for t in lr_top if t[3] < contact_A) / lr_L

    return {
        "pearson_prox_vs_invdist": r,
        "top_L_precision": top_hit,
        "long_range_top_L2_precision": lr_hit,
        "n_pairs": len(pairs),
        "n_true_contacts": len(contacts),
    }


def exp_distance_matrix(xyz: np.ndarray) -> np.ndarray:
    n = xyz.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.linalg.norm(xyz[i] - xyz[j]))
            D[i, j] = D[j, i] = d
    return D


def main() -> int:
    store = _store()
    cache = store / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    print("FSOT distogram contact eval (native F15 metrics)")
    rows = []
    for acc, pdb_id, chain, name in TARGETS:
        print(f"\n--- {pdb_id} {name} ---")
        seq = fetch_uniprot_sequence(acc)
        time.sleep(0.3)
        exp = fetch_pdb(pdb_id, chain, cache)
        time.sleep(0.3)
        if not exp:
            print("  PDB fail")
            rows.append({"pdb": pdb_id, "error": "pdb"})
            continue
        exp_seq, exp_xyz = exp
        # use experimental length for fair local matrix
        use_seq = exp_seq if len(exp_seq) >= 20 else (seq or exp_seq)
        if not use_seq:
            rows.append({"pdb": pdb_id, "error": "seq"})
            continue
        # align lengths
        n = min(len(use_seq), len(exp_xyz))
        use_seq = use_seq[:n]
        exp_xyz = exp_xyz[:n]
        M, _, regions, _ = build_distogram(use_seq)
        D = exp_distance_matrix(exp_xyz)
        met = contact_metrics(M, D, n)
        print(
            f"  n={n} regions={len(regions)} Pearson={met['pearson_prox_vs_invdist']:.4f} "
            f"Top-L={met['top_L_precision']:.4f} LR={met['long_range_top_L2_precision']:.4f}"
        )
        rows.append(
            {
                "pdb": pdb_id,
                "name": name,
                "accession": acc,
                "n": n,
                "n_regions": len(regions),
                **met,
                "engine": "fsot_protein_F01_F15_port_v3",
            }
        )

    pearsons = [r["pearson_prox_vs_invdist"] for r in rows if "pearson_prox_vs_invdist" in r]
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Native FSOT protein evaluation: F15 distogram vs experimental contacts",
        "authority": "FSOT_PROTEIN_DERIVATIONS.md v7",
        "note": (
            "This is the metric the protein stack was designed for (Pearson/Top-L/LR). "
            "Cα RMSD embedding is a separate downstream step; contact ranking must work first."
        ),
        "summary": {
            "n_proteins": len(pearsons),
            "median_pearson": float(sorted(pearsons)[len(pearsons) // 2]) if pearsons else None,
            "mean_pearson": float(sum(pearsons) / len(pearsons)) if pearsons else None,
        },
        "results": rows,
    }
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    lines = [
        "# FSOT distogram contact evaluation (F15 native)",
        "",
        f"*Generated {doc['generated_at']}*",
        "",
        doc["note"],
        "",
        f"**Median Pearson:** {doc['summary']['median_pearson']}",
        "",
        "| PDB | Name | n | Pearson | Top-L | LR Top-L/2 |",
        "|-----|------|--:|--------:|------:|-----------:|",
    ]
    for r in rows:
        if "error" in r:
            lines.append(f"| {r.get('pdb')} | err | | | | |")
        else:
            lines.append(
                f"| {r['pdb']} | {r['name']} | {r['n']} | {r['pearson_prox_vs_invdist']:.4f} | "
                f"{r['top_L_precision']:.4f} | {r['long_range_top_L2_precision']:.4f} |"
            )
    lines.append("")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    print(f"Median Pearson {doc['summary']['median_pearson']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
