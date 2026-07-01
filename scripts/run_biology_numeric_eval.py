#!/usr/bin/env python3
"""
Biology numeric depth: Soul Simulator 234k corpus + unified DB bio subset.

Produces data/biology_numeric_report.json for Biology domain precision depth.
"""

from __future__ import annotations

import argparse
import json
import random
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
CELLULAR_MANIFEST = ROOT / "data" / "cellular_manifest.yaml"
DEFAULT_DB = Path(
    r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\FSOT_UNIFIED.db"
)
OUTPUT = ROOT / "data" / "biology_numeric_report.json"

BIOLOGY_SUBJECTS = {
    "natural science",
    "life science",
    "biology",
}
BIOLOGY_TOPIC_KEYWORDS = (
    "biology",
    "cell",
    "organism",
    "gene",
    "dna",
    "evolution",
    "ecosystem",
    "photosynthesis",
    "mitochond",
    "operon",
    "species",
)


def _is_biology_record(fields: dict) -> bool:
    subject = (fields.get("subject") or "").lower()
    topic = (fields.get("topic") or "").lower()
    category = (fields.get("category") or "").lower()
    skill = (fields.get("skill") or "").lower()
    prompt = (fields.get("prompt") or fields.get("hint") or "").lower()
    blob = " ".join([subject, topic, category, skill, prompt])
    if subject in BIOLOGY_SUBJECTS:
        return True
    return any(kw in blob for kw in BIOLOGY_TOPIC_KEYWORDS)


def sample_soul_biology(corpus_path: Path, sample_size: int = 5000, seed: int = 42) -> dict:
    if not corpus_path.exists():
        return {"error": f"corpus not found: {corpus_path}", "sample_size": 0}
    rng = random.Random(seed)
    reservoir: list[dict] = []
    total = 0
    biology_total = 0
    subject_counts: dict[str, int] = {}
    with corpus_path.open(encoding="utf-8") as f:
        for line in f:
            total += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            fields = row.get("fields") or {}
            if not _is_biology_record(fields):
                continue
            biology_total += 1
            subj = fields.get("subject") or "unknown"
            subject_counts[subj] = subject_counts.get(subj, 0) + 1
            if len(reservoir) < sample_size:
                reservoir.append(row)
            else:
                j = rng.randint(0, biology_total - 1)
                if j < sample_size:
                    reservoir[j] = row
    return {
        "corpus_total": total,
        "biology_records_estimated": biology_total,
        "sample_size": len(reservoir),
        "subject_distribution": dict(sorted(subject_counts.items(), key=lambda x: -x[1])[:12]),
        "sample_records": [
            {
                "subject": (r.get("fields") or {}).get("subject"),
                "topic": (r.get("fields") or {}).get("topic"),
                "category": (r.get("fields") or {}).get("category"),
                "dataset_type": r.get("dataset_type"),
            }
            for r in reservoir[:50]
        ],
    }


def summarize_db_biology(db_path: Path) -> dict:
    if not db_path.exists():
        return {"error": f"db not found: {db_path}"}
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    bio_filter = """
        domain_type LIKE '%bio%' OR concept_name LIKE '%bio%'
        OR concept_name LIKE '%cell%' OR concept_name LIKE '%gene%'
        OR concept_name LIKE '%DNA%' OR concept_name LIKE '%evolution%'
    """
    total = cur.execute(f"SELECT COUNT(1) FROM records WHERE {bio_filter}").fetchone()[0]
    strict = cur.execute(
        f"SELECT COUNT(1) FROM records WHERE strict_empirical=1 AND ({bio_filter})"
    ).fetchone()[0]
    numeric = cur.execute(
        f"""
        SELECT COUNT(1) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE ({bio_filter})
        """
    ).fetchone()[0]
    within_2 = cur.execute(
        f"""
        SELECT COUNT(1) FROM verification_numeric v
        JOIN records r ON r.record_id = v.record_id
        WHERE ({bio_filter}) AND v.error_pct IS NOT NULL AND v.error_pct <= 2.0
        """
    ).fetchone()[0]
    con.close()
    return {
        "db_path": str(db_path),
        "biology_records": total,
        "strict_empirical": strict,
        "verification_numeric": numeric,
        "within_target_2pct": within_2,
    }


def build_report(*, sample_size: int, db_path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(CELLULAR_MANIFEST.read_text(encoding="utf-8"))
    soul_manifest_path = Path(manifest["artifacts"]["soul_simulator_manifest"]["path"])
    soul = json.loads(soul_manifest_path.read_text(encoding="utf-8"))
    corpus = soul_manifest_path.parent / "training_corpus.jsonl"
    soul_sample = sample_soul_biology(corpus, sample_size=sample_size)
    db_summary = summarize_db_biology(db_path)

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    biology_S = float(mod.domain_scalar("Biology"))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "biology_domain_scalar_S": biology_S,
        "soul_manifest": {
            "records_processed": soul.get("records_processed"),
            "file_count": soul.get("file_count"),
            "types": soul.get("types"),
        },
        "soul_biology_sample": soul_sample,
        "unified_db_biology": db_summary,
        "depth_metrics": {
            "soul_records_total": soul.get("records_processed", 0),
            "soul_biology_fraction": (
                soul_sample.get("biology_records_estimated", 0)
                / max(1, soul_sample.get("corpus_total", 1))
            ),
            "numeric_verification_rows": db_summary.get("verification_numeric", 0),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Biology numeric depth eval (Soul + DB)")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--sample-size", type=int, default=5000)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    report = build_report(sample_size=args.sample_size, db_path=args.db)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  soul_records: {report['soul_manifest']['records_processed']}")
    print(f"  biology_estimated: {report['soul_biology_sample'].get('biology_records_estimated')}")
    print(f"  db_bio_numeric: {report['unified_db_biology'].get('verification_numeric')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())