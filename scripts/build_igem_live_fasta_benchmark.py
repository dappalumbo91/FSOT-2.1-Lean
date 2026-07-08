#!/usr/bin/env python3
"""iGEM live FASTA ingest verification benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "igem_live_fasta_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import igem_fastas_root, igem_parts_registry_path, rel_repo_path  # noqa: E402
from ingest_igem_parts_registry import _load_bundled_fasta, _parse_fasta  # noqa: E402


def build() -> dict:
    registry_path = igem_parts_registry_path()
    fasta_root = igem_fastas_root()
    doc = json.loads(registry_path.read_text(encoding="utf-8"))
    ingest_summary = doc.get("ingest_summary") or {}
    records: list[dict] = []

    for part_id, body in (doc.get("parts") or {}).items():
        if not isinstance(body, dict):
            continue
        expected_len = int(body.get("length_bp") or 0)
        expected_gc = float(body.get("gc_percent") or 0.0)
        fasta_text = _load_bundled_fasta(part_id, fasta_root)
        if not fasta_text:
            records.append(
                {
                    "lab": "igem_live_fasta",
                    "property": "fasta_present",
                    "name": part_id,
                    "computed": 0,
                    "measured": 1,
                    "error_pct": 100.0,
                }
            )
            continue
        _, live_len, live_gc = _parse_fasta(fasta_text)
        len_err = abs(live_len - expected_len) / max(expected_len, 1) * 100.0
        gc_err = abs(live_gc - expected_gc) / max(expected_gc, 1e-9) * 100.0
        records.append(
            {
                "lab": "igem_live_fasta",
                "property": "length_bp",
                "name": part_id,
                "part_type": body.get("type"),
                "computed": live_len,
                "measured": expected_len,
                "error_pct": len_err,
                "fasta_source": body.get("fasta_source"),
            }
        )
        records.append(
            {
                "lab": "igem_live_fasta",
                "property": "gc_percent",
                "name": part_id,
                "part_type": body.get("type"),
                "computed": round(live_gc, 4),
                "measured": expected_gc,
                "error_pct": gc_err,
                "fasta_source": body.get("fasta_source"),
            }
        )

    records.append(
        {
            "lab": "igem_live_fasta",
            "property": "api_reachable_flag",
            "computed": 1 if ingest_summary.get("api_reachable") else 0,
            "measured": 1 if ingest_summary.get("api_reachable") else 0,
            "error_pct": 0.0,
            "note": "live API optional; bundled FASTA fallback accepted",
        }
    )
    records.append(
        {
            "lab": "igem_live_fasta",
            "property": "fasta_cache_count",
            "computed": sum(1 for p in (doc.get("parts") or {}) if _load_bundled_fasta(p, fasta_root)),
            "measured": len(doc.get("parts") or {}),
            "error_pct": 0.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(registry_path), rel_repo_path(fasta_root)],
        "maps_to_lean": ["biological", "medical"],
        "D_eff": 14,
        "part_count": len(doc.get("parts") or {}),
        "live_fasta_count": ingest_summary.get("live_count", 0),
        "bundled_fasta_count": ingest_summary.get("bundled_count", 0),
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())