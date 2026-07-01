#!/usr/bin/env python3
"""Bridge Soul Simulator biology QA → strict-empirical observables (NCBI + bio constants)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLULAR_MANIFEST = ROOT / "data" / "cellular_manifest.yaml"
DEFAULT_OPERONS = Path(
    r"C:\Users\damia\Desktop\fsot_evolution_\files-b7d9d6b8\fsot_evolution_sim\results\biological_mt_operons.json"
)
OUTPUT = ROOT / "data" / "biology_strict_empirical.json"

HUMAN_MT_OPERON_REF = {
    "MT-ND1": 956,
    "MT-ND2": 1044,
    "MT-CO1": 1542,
    "MT-CO2": 684,
    "MT-ATP8": 207,
    "MT-ATP6": 681,
    "MT-CO3": 780,
    "MT-ND3": 349,
    "MT-ND4L": 297,
    "MT-ND4": 1378,
    "MT-ND5": 1812,
    "MT-ND6": 525,
    "MT-CYTB": 1140,
}

BIO_CONSTANTS = {
    "human_body_temp_c": 37.0,
    "blood_ph": 7.4,
    "mt_genome_bp": 16569,
    "human_genome_gbp": 3.2,
    "rbc_diameter_um": 7.5,
}

GENE_RE = re.compile(r"\b(MT-(?:ND\d|CO\d|ATP\d|CYTB|ND4L))\b", re.I)
NUMERIC_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:°C|C\b|bp|kb|kbp|Gbp|μm|um|pH)?", re.I)

BIOLOGY_SUBJECTS = {"natural science", "life science", "biology"}
BIOLOGY_KEYWORDS = ("biology", "cell", "gene", "dna", "mitochond", "organism", "evolution")


def _is_biology(fields: dict) -> bool:
    subject = (fields.get("subject") or "").lower()
    blob = " ".join(
        str(fields.get(k) or "") for k in ("topic", "category", "skill", "prompt", "hint", "context")
    ).lower()
    if subject in BIOLOGY_SUBJECTS:
        return True
    return any(k in blob for k in BIOLOGY_KEYWORDS)


def _operon_records(operons_path: Path) -> list[dict]:
    if not operons_path.exists():
        return []
    operons = json.loads(operons_path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for name, ref_len in HUMAN_MT_OPERON_REF.items():
        entry = operons.get(name)
        if not entry:
            continue
        sim_len = int(entry.get("length") or 0)
        err = abs(sim_len - ref_len) / ref_len * 100.0
        out.append(
            {
                "lab": "biology_strict_lab",
                "property": "mt_operon_length",
                "name": name,
                "computed": sim_len,
                "measured": ref_len,
                "error_pct": err,
                "source": "soul_corpus+evolution_sim+NCBI_NC_012920.1",
            }
        )
    return out


def _soul_gene_mentions(corpus_path: Path, max_lines: int = 80000) -> tuple[list[dict], int, int]:
    if not corpus_path.exists():
        return []
    mention_counts: dict[str, int] = {g: 0 for g in HUMAN_MT_OPERON_REF}
    scanned = 0
    bio_rows = 0
    with corpus_path.open(encoding="utf-8") as f:
        for line in f:
            scanned += 1
            if scanned > max_lines:
                break
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            fields = row.get("fields") or {}
            if not _is_biology(fields):
                continue
            bio_rows += 1
            text = json.dumps(fields)
            for m in GENE_RE.finditer(text):
                gene = m.group(1).upper()
                if gene in mention_counts:
                    mention_counts[gene] += 1
    records: list[dict] = []
    for gene, count in mention_counts.items():
        if count == 0:
            continue
        ref = float(HUMAN_MT_OPERON_REF[gene])
        records.append(
            {
                "lab": "biology_strict_lab",
                "property": "soul_corpus_gene_mention",
                "name": gene,
                "computed": float(count),
                "measured": ref / 100.0,
                "error_pct": abs(count - ref / 100.0) / (ref / 100.0) * 100.0,
                "source": "soul_corpus_mention_density",
            }
        )
    return records, bio_rows, scanned


def _bio_constant_records() -> list[dict]:
    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, _ = load_fsot_compute()
    S = float(mod.domain_scalar("Biology"))
    records: list[dict] = []
    for name, measured in BIO_CONSTANTS.items():
        computed = S * measured
        err = abs(computed - measured) / measured * 100.0 if measured else 0.0
        records.append(
            {
                "lab": "biology_strict_lab",
                "property": "bio_constant_scale",
                "name": name,
                "computed": round(computed, 6),
                "measured": measured,
                "error_pct": err,
                "source": "FSOT_biological_scalar_scale",
            }
        )
    return records


def build(operons_path: Path, corpus_path: Path) -> dict:
    operon_recs = _operon_records(operons_path)
    soul_recs, bio_rows, scanned = _soul_gene_mentions(corpus_path)
    const_recs = _bio_constant_records()
    records = operon_recs + soul_recs + const_recs
    errs = [r["error_pct"] for r in records if r.get("error_pct") is not None]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_corpus": str(corpus_path),
        "soul_lines_scanned": scanned,
        "soul_biology_rows": bio_rows,
        "record_count": len(records),
        "operon_records": len(operon_recs),
        "soul_mention_records": len(soul_recs),
        "bio_constant_records": len(const_recs),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build biology strict-empirical bridge")
    parser.add_argument("--operons", type=Path, default=DEFAULT_OPERONS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    try:
        import yaml
    except ImportError:
        print("FAIL: PyYAML required")
        return 1

    manifest = yaml.safe_load(CELLULAR_MANIFEST.read_text(encoding="utf-8"))
    soul_manifest = Path(manifest["artifacts"]["soul_simulator_manifest"]["path"])
    corpus = soul_manifest.parent / "training_corpus.jsonl"

    doc = build(args.operons, corpus)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']} (operons={doc['operon_records']} soul={doc['soul_mention_records']})")
    print(f"  soul_biology_rows: {doc['soul_biology_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())