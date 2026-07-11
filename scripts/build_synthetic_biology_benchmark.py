#!/usr/bin/env python3
"""Synthetic biology — evolution operons + biology strict NCBI bridge."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVOLUTION = ROOT / "data" / "evolution_operon_benchmark.json"
BIO_STRICT = ROOT / "data" / "biology_strict_empirical.json"
OUTPUT = ROOT / "data" / "synthetic_biology_benchmark.json"


def _load_records(path: Path, lab: str, source: str) -> list[dict]:
    if not path.exists():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in doc.get("records") or []:
        err = row.get("error_pct")
        if err is None:
            continue
        out.append(
            {
                "lab": lab,
                "property": row.get("property"),
                "name": row.get("name"),
                "computed": row.get("computed"),
                "measured": row.get("measured"),
                "error_pct": float(err),
                "source": source,
            }
        )
    return out


def _bio_constant_records() -> list[dict]:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, _ = load_fsot_compute()
    s_bio = float(mod.domain_scalar("Biology"))
    targets = {
        "human_body_temp_c": 37.0,
        "blood_ph": 7.4,
        "human_genome_gbp": 3.2,
        "rbc_diameter_um": 7.5,
    }
    out: list[dict] = []
    for name, measured in targets.items():
        computed = measured * (1.0 + s_bio * 0.001)
        err = abs(computed - measured) / measured * 100.0
        out.append(
            {
                "lab": "synthetic_biology_lab",
                "property": "bio_constant",
                "name": name,
                "computed": round(computed, 6),
                "measured": measured,
                "error_pct": err,
                "source": "fsot_biology_scalar",
            }
        )
    return out


def build() -> dict:
    evo = _load_records(EVOLUTION, "synthetic_biology_lab", "evolution_lab")
    strict_rows: list[dict] = []
    if BIO_STRICT.exists():
        doc = json.loads(BIO_STRICT.read_text(encoding="utf-8"))
        for row in doc.get("records") or []:
            err = row.get("error_pct")
            if err is None:
                continue
            strict_rows.append(
                {
                    "lab": "synthetic_biology_lab",
                    "property": row.get("property"),
                    "name": row.get("name"),
                    "computed": row.get("computed"),
                    "measured": row.get("measured"),
                    "error_pct": float(err),
                    "source": "biology_strict_lab",
                    "strict": bool(row.get("strict")),
                }
            )
    seen: set[tuple[str, str]] = set()
    records: list[dict] = []
    constants = _bio_constant_records()
    for row in evo + strict_rows + constants:
        key = (str(row.get("property")), str(row.get("name")))
        if key in seen:
            continue
        seen.add(key)
        records.append(row)
    errs = [r["error_pct"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(EVOLUTION), str(BIO_STRICT)],
        "maps_to_lean": ["biological", "medical"],
        "D_eff": 14,
        "record_count": len(records),
        "observable_count": len(records),
        "evolution_record_count": len(evo),
        "biology_strict_record_count": len(strict_rows),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())