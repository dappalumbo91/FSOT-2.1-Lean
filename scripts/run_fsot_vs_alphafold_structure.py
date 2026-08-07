#!/usr/bin/env python3
"""FSOT vs AlphaFold structure head-to-head (experimental PDB ground truth).

Pipeline
--------
  1. Fetch UniProt sequence (sequence-only input for FSOT)
  2. FSOT predicts Cα coordinates (fsot_structure_engine — zero free params)
  3. Fetch experimental structure from RCSB PDB (ground truth)
  4. Fetch AlphaFold DB model (competitor)
  5. Kabsch-align each prediction to experimental Cα; report RMSD
  6. Dual scoreboard: lower RMSD to experiment wins

Storage-capped for home PC (Omen-class). No full proteome dump.

  python scripts/run_fsot_vs_alphafold_structure.py
  python scripts/run_fsot_vs_alphafold_structure.py --max-proteins 8 --rounds 100
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_structure_engine import predict_ca_coords, write_ca_pdb, clean_sequence  # noqa: E402

EXTERNAL = Path(r"G:\FSOT-PublicData\anomaly_observables\fsot_vs_alphafold")
LOCAL = ROOT / "vendor" / "fsot_vs_alphafold"
OUT_JSON = ROOT / "data" / "fsot_vs_alphafold_structure.json"
OUT_MD = ROOT / "predictions" / "reports" / "FSOT_VS_ALPHAFOLD_STRUCTURE.md"

# (uniprot, pdb_id, chain, plain_name) — short, classic, experimental structures
# Chosen for Omen-scale run: small–medium chains with clear PDB entries
BENCHMARK_SET: list[tuple[str, str, str, str]] = [
    ("P69905", "1A3N", "A", "Hemoglobin alpha"),
    ("P68871", "1A3N", "B", "Hemoglobin beta"),
    ("P00918", "1CA2", "A", "Carbonic anhydrase II"),
    ("P00441", "2C9V", "A", "SOD1"),
    ("P61626", "1LZ1", "A", "Lysozyme human"),
    ("P61823", "7RSA", "A", "RNase A"),
    ("P0CG47", "1UBQ", "A", "Ubiquitin"),
    ("P01308", "4INS", "A", "Insulin"),
    ("P04637", "1TUP", "A", "p53 DNA-binding"),
    ("P0DP23", "1CLL", "A", "Calmodulin"),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _store() -> Path:
    try:
        EXTERNAL.mkdir(parents=True, exist_ok=True)
        return EXTERNAL
    except OSError:
        LOCAL.mkdir(parents=True, exist_ok=True)
        return LOCAL


def http_bytes(url: str, timeout: int = 90) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/structure-h2h"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def http_json(url: str, timeout: int = 60) -> Any:
    raw = http_bytes(url, timeout=timeout)
    if raw is None:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


def fetch_uniprot_sequence(acc: str) -> str | None:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
    data = http_json(url)
    if not isinstance(data, dict):
        return None
    seq = (data.get("sequence") or {}).get("value")
    return clean_sequence(seq) if seq else None


def parse_pdb_ca(text: str, chain: str | None = None) -> tuple[str, np.ndarray]:
    """Return (sequence, CA coords) from PDB text."""
    seq = []
    coords = []
    aa3_to_1 = {
        "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
        "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
        "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
        "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
        "MSE": "M", "SEC": "C",
    }
    seen = set()
    for line in text.splitlines():
        if not line.startswith("ATOM"):
            continue
        if line[12:16].strip() != "CA":
            continue
        ch = line[21].strip()
        if chain and ch != chain:
            continue
        resseq = line[22:26].strip()
        key = (ch, resseq)
        if key in seen:
            continue
        seen.add(key)
        resname = line[17:20].strip()
        aa = aa3_to_1.get(resname)
        if not aa:
            continue
        x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
        seq.append(aa)
        coords.append([x, y, z])
    if not coords:
        return "", np.zeros((0, 3))
    return "".join(seq), np.array(coords, dtype=np.float64)


def fetch_pdb(pdb_id: str, chain: str, cache: Path) -> tuple[str, np.ndarray] | None:
    path = cache / f"{pdb_id}.pdb"
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
        raw = http_bytes(url)
        if not raw:
            return None
        text = raw.decode("utf-8", errors="replace")
        path.write_text(text, encoding="utf-8")
    seq, xyz = parse_pdb_ca(text, chain=chain)
    if len(seq) < 5:
        # try without chain filter
        seq, xyz = parse_pdb_ca(text, chain=None)
    if len(seq) < 5:
        return None
    return seq, xyz


def fetch_alphafold_pdb(acc: str, cache: Path) -> tuple[str, np.ndarray] | None:
    """Download AF model PDB via prediction API file URL or known pattern."""
    meta_path = cache / f"afmeta_{acc}.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        meta = http_json(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}")
        if meta is None:
            return None
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    if not isinstance(meta, list) or not meta:
        return None
    entry = meta[0]
    pdb_url = entry.get("pdbUrl") or entry.get("modelUrl")
    if not pdb_url:
        # construct from model id
        mid = entry.get("modelEntityId") or entry.get("entryId") or f"AF-{acc}-F1"
        # classic CDN pattern
        pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v4.pdb"
    path = cache / f"af_{acc}.pdb"
    if not path.is_file():
        raw = http_bytes(str(pdb_url))
        if not raw:
            # try v6 / v3 fallbacks
            for ver in ("v6", "v4", "v3"):
                alt = f"https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_{ver}.pdb"
                raw = http_bytes(alt)
                if raw:
                    break
        if not raw:
            return None
        path.write_bytes(raw)
    text = path.read_text(encoding="utf-8", errors="replace")
    seq, xyz = parse_pdb_ca(text, chain=None)
    if len(seq) < 5:
        return None
    return seq, xyz


def kabsch_rmsd(p: np.ndarray, q: np.ndarray) -> float:
    """RMSD after optimal rotation (Kabsch). p,q shape (n,3)."""
    assert p.shape == q.shape and p.shape[0] >= 3
    p = p - p.mean(axis=0)
    q = q - q.mean(axis=0)
    H = p.T @ q
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    sign = 1.0 if d >= 0 else -1.0
    R = Vt.T @ np.diag([1.0, 1.0, sign]) @ U.T
    p_align = p @ R.T
    diff = p_align - q
    return float(np.sqrt((diff * diff).sum() / p.shape[0]))


def align_by_sequence(
    pred_seq: str, pred_xyz: np.ndarray, exp_seq: str, exp_xyz: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int]:
    """Greedy N-terminal trim to common length min; prefer matching substring."""
    n = min(len(pred_seq), len(exp_seq), len(pred_xyz), len(exp_xyz))
    # find best offset of exp in pred or vice versa by simple identity window
    best_i, best_j, best_len, best_score = 0, 0, n, -1
    # restrict search for speed
    max_shift = min(30, abs(len(pred_seq) - len(exp_seq)) + 15)
    for i in range(0, min(max_shift, max(1, len(pred_seq) - 20))):
        for j in range(0, min(max_shift, max(1, len(exp_seq) - 20))):
            m = min(len(pred_seq) - i, len(exp_seq) - j)
            if m < 20:
                continue
            # sample score
            step = max(1, m // 40)
            score = sum(
                1 for k in range(0, m, step) if pred_seq[i + k] == exp_seq[j + k]
            )
            if score > best_score:
                best_score = score
                best_i, best_j, best_len = i, j, m
    # fallback pure trim
    if best_score < 5:
        best_i = best_j = 0
        best_len = n
    L = min(best_len, len(pred_xyz) - best_i, len(exp_xyz) - best_j)
    # optionally shrink to high-identity core
    return pred_xyz[best_i : best_i + L], exp_xyz[best_j : best_j + L], L


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-proteins", type=int, default=8)
    ap.add_argument("--rounds", type=int, default=90)
    ap.add_argument("--sleep", type=float, default=0.4)
    args = ap.parse_args()

    store = _store()
    cache = store / "cache"
    pred_dir = store / "fsot_preds"
    cache.mkdir(parents=True, exist_ok=True)
    pred_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("FSOT vs ALPHAFOLD — structure head-to-head (PDB ground truth)")
    print(f"  store   = {store}")
    print(f"  rounds  = {args.rounds}")
    print("  engine  = fsot_structure_engine (0 free parameters)")
    print("  metric  = Cα RMSD after Kabsch to experimental PDB")
    print("=" * 64)

    results = []
    for acc, pdb_id, chain, name in BENCHMARK_SET[: args.max_proteins]:
        print(f"\n--- {acc} {name} (PDB {pdb_id}) ---")
        seq = fetch_uniprot_sequence(acc)
        time.sleep(args.sleep)
        if not seq:
            print("  UniProt sequence FAIL")
            results.append({"accession": acc, "name": name, "error": "uniprot_seq"})
            continue
        print(f"  sequence length {len(seq)}")

        # FSOT prediction
        try:
            pred = predict_ca_coords(seq, rounds=args.rounds)
            fsot_xyz = pred["ca_coords"]
            fsot_seq = pred["sequence"]
            write_ca_pdb(pred_dir / f"FSOT_{acc}.pdb", fsot_seq, fsot_xyz, name=acc)
            print(f"  FSOT predicted {len(fsot_seq)} CA  ss_H={pred['secondary'].count('H')}")
        except Exception as e:
            print(f"  FSOT predict FAIL {e}")
            results.append({"accession": acc, "name": name, "error": f"fsot:{e}"})
            continue

        # Experimental
        exp = fetch_pdb(pdb_id, chain, cache)
        time.sleep(args.sleep)
        if not exp:
            print("  PDB experimental FAIL")
            results.append({"accession": acc, "name": name, "error": "pdb_fetch", "fsot_len": len(fsot_seq)})
            continue
        exp_seq, exp_xyz = exp
        print(f"  PDB experimental CA n={len(exp_seq)}")

        # AlphaFold
        af = fetch_alphafold_pdb(acc, cache)
        time.sleep(args.sleep)
        af_rmsd = None
        af_n = None
        if af:
            af_seq, af_xyz = af
            print(f"  AlphaFold model CA n={len(af_seq)}")
            a_pred, a_exp, Ln = align_by_sequence(af_seq, af_xyz, exp_seq, exp_xyz)
            if Ln >= 20:
                af_rmsd = kabsch_rmsd(a_pred, a_exp)
                af_n = Ln
                print(f"  AF  RMSD={af_rmsd:.3f} Å  (n={Ln})")
            else:
                print("  AF align too short")
        else:
            print("  AlphaFold model FAIL")

        # FSOT vs experimental
        f_pred, f_exp, Ln = align_by_sequence(fsot_seq, fsot_xyz, exp_seq, exp_xyz)
        if Ln < 20:
            print("  FSOT align too short")
            results.append({"accession": acc, "name": name, "error": "align_short"})
            continue
        fsot_rmsd = kabsch_rmsd(f_pred, f_exp)
        print(f"  FSOT RMSD={fsot_rmsd:.3f} Å  (n={Ln})")

        win = None
        if af_rmsd is not None:
            win = "FSOT" if fsot_rmsd < af_rmsd else "AlphaFold"
            if abs(fsot_rmsd - af_rmsd) < 0.05:
                win = "tie"
        rec = {
            "accession": acc,
            "name": name,
            "pdb_id": pdb_id,
            "chain": chain,
            "seq_len_uniprot": len(seq),
            "fsot_rmsd_A": fsot_rmsd,
            "fsot_align_n": Ln,
            "af_rmsd_A": af_rmsd,
            "af_align_n": af_n,
            "winner_lower_rmsd": win,
            "fsot_secondary": pred["secondary"][:80],
            "S_biochem": pred.get("S_biochem"),
            "S_molchem": pred.get("S_molchem"),
            "engine": pred["engine"],
            "free_parameters": 0,
            "authority": pred.get("authority"),
        }
        results.append(rec)
        print(f"  WINNER: {win}")

    # summary
    paired = [r for r in results if r.get("fsot_rmsd_A") is not None and r.get("af_rmsd_A") is not None]
    fsot_wins = sum(1 for r in paired if r.get("winner_lower_rmsd") == "FSOT")
    af_wins = sum(1 for r in paired if r.get("winner_lower_rmsd") == "AlphaFold")
    ties = sum(1 for r in paired if r.get("winner_lower_rmsd") == "tie")
    fsot_rmsd_list = [r["fsot_rmsd_A"] for r in results if r.get("fsot_rmsd_A") is not None]
    af_rmsd_list = [r["af_rmsd_A"] for r in results if r.get("af_rmsd_A") is not None]

    def med(xs):
        if not xs:
            return None
        s = sorted(xs)
        return s[len(s) // 2]

    doc = {
        "generated_at": _now(),
        "mission": "FSOT sequence-only structure prediction vs AlphaFold, scored on experimental PDB Cα RMSD",
        "engine": "fsot_structure_engine_v1",
        "free_parameters": 0,
        "metric": "Cα RMSD (Å) after Kabsch alignment to experimental PDB",
        "lower_is_better": True,
        "hardware_note": "Designed to run on HP Omen-class desktop, storage-capped cache",
        "summary": {
            "proteins_attempted": len(BENCHMARK_SET[: args.max_proteins]),
            "proteins_scored_fsot": len(fsot_rmsd_list),
            "proteins_scored_both": len(paired),
            "fsot_median_rmsd_A": med(fsot_rmsd_list),
            "af_median_rmsd_A": med(af_rmsd_list),
            "fsot_wins": fsot_wins,
            "alphafold_wins": af_wins,
            "ties": ties,
            "fsot_win_rate": (fsot_wins / len(paired)) if paired else None,
        },
        "results": results,
        "next_iterations": [
            "Increase refine rounds / multi-start from secondary string variants",
            "Add side-chain packing after Cα (still seed-only)",
            "Expand benchmark set (CASP-style hard targets)",
            "Distogram assembly F15 full matrix for n>200",
        ],
    }

    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    (store / "fsot_vs_alphafold_structure.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")

    s = doc["summary"]
    lines = [
        "# FSOT vs AlphaFold — structure head-to-head",
        "",
        f"*Generated {doc['generated_at']}*",
        "",
        "## Mission",
        "",
        doc["mission"],
        "",
        f"- Engine: `{doc['engine']}` · **free parameters: 0**",
        f"- Metric: {doc['metric']} (lower is better)",
        f"- Hardware: {doc['hardware_note']}",
        "",
        "## Scoreboard",
        "",
        f"| Side | Median Cα RMSD (Å) | Wins |",
        f"|------|-------------------:|-----:|",
        f"| **FSOT** | **{s.get('fsot_median_rmsd_A')}** | **{s.get('fsot_wins')}** |",
        f"| AlphaFold | {s.get('af_median_rmsd_A')} | {s.get('alphafold_wins')} |",
        f"| Ties | — | {s.get('ties')} |",
        "",
        f"Paired proteins: **{s.get('proteins_scored_both')}** · FSOT win rate: **{s.get('fsot_win_rate')}**",
        "",
        "## Per protein",
        "",
        "| UniProt | Name | PDB | FSOT RMSD Å | AF RMSD Å | Winner |",
        "|---------|------|-----|------------:|----------:|:------:|",
    ]
    for r in results:
        if r.get("error"):
            lines.append(
                f"| {r.get('accession')} | {r.get('name')} | {r.get('pdb_id','')} | err | err | {r.get('error')} |"
            )
        else:
            lines.append(
                f"| {r.get('accession')} | {r.get('name')} | {r.get('pdb_id')} | "
                f"{r.get('fsot_rmsd_A'):.3f} | {r.get('af_rmsd_A') if r.get('af_rmsd_A') is not None else '—'} | "
                f"{r.get('winner_lower_rmsd')} |"
            )
    lines.extend(
        [
            "",
            "## How to run",
            "",
            "```powershell",
            "python scripts/run_fsot_vs_alphafold_structure.py --max-proteins 8 --rounds 90",
            "```",
            "",
            "## Next",
            "",
        ]
    )
    for x in doc["next_iterations"]:
        lines.append(f"- {x}")
    lines.append("")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 64)
    print("SCOREBOARD")
    print(f"  FSOT median RMSD: {s.get('fsot_median_rmsd_A')} Å  wins={s.get('fsot_wins')}")
    print(f"  AF   median RMSD: {s.get('af_median_rmsd_A')} Å  wins={s.get('alphafold_wins')}")
    print(f"  ties={s.get('ties')}  paired={s.get('proteins_scored_both')}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
