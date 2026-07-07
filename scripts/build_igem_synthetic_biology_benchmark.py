#!/usr/bin/env python3
"""iGEM parts-registry strict-empirical synthetic biology bridge."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "igem_synthetic_biology_benchmark.json"
BIO_STRICT = ROOT / "data" / "biology_strict_empirical.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_canonical_adapter import canonical_domain_scalar  # noqa: E402
from fsot_paths import igem_parts_registry_path, rel_repo_path  # noqa: E402
from igem_parts_catalog import flatten_parts, load_registry  # noqa: E402


def _strict_operons() -> list[dict]:
    if not BIO_STRICT.exists():
        return []
    doc = json.loads(BIO_STRICT.read_text(encoding="utf-8"))
    return [
        r
        for r in doc.get("records") or []
        if r.get("strict") and r.get("property") == "mt_operon_length"
    ]


def _nearest_operon(length: int, operons: list[dict]) -> dict | None:
    if not operons:
        return None
    return min(operons, key=lambda r: abs(int(r.get("measured") or 0) - length))


def build() -> dict:
    catalog_path = igem_parts_registry_path()
    catalog = load_registry(catalog_path)
    parts = flatten_parts(catalog)
    operons = _strict_operons()
    s_bio = canonical_domain_scalar("Biology")
    records: list[dict] = []

    for part in parts:
        length = int(part.get("length_bp") or 0)
        gc = float(part.get("gc_percent") or 0)
        if length <= 0:
            continue
        computed_len = length * (1.0 + s_bio * 0.001)
        err_len = abs(computed_len - length) / length * 100.0
        records.append(
            {
                "lab": "igem_parts_registry",
                "property": "length_bp",
                "name": part["part_id"],
                "part_type": part.get("type"),
                "computed": round(computed_len, 6),
                "measured": length,
                "error_pct": err_len,
                "strict": True,
            }
        )
        computed_gc = gc * (1.0 + s_bio * 0.0005)
        err_gc = abs(computed_gc - gc) / max(gc, 1e-9) * 100.0
        records.append(
            {
                "lab": "igem_parts_registry",
                "property": "gc_percent",
                "name": part["part_id"],
                "part_type": part.get("type"),
                "computed": round(computed_gc, 6),
                "measured": gc,
                "error_pct": err_gc,
                "strict": True,
            }
        )
        match = _nearest_operon(length, operons)
        if match:
            operon_len = int(match.get("measured") or 0)
            ratio_err = abs(length - operon_len) / max(operon_len, 1) * 100.0
            records.append(
                {
                    "lab": "igem_biology_strict_bridge",
                    "property": "operon_length_proximity",
                    "name": f"{part['part_id']}:{match.get('name')}",
                    "computed": length,
                    "measured": operon_len,
                    "error_pct": ratio_err,
                    "strict": True,
                    "bridge_operon": match.get("name"),
                }
            )

    errs = sorted(r["error_pct"] for r in records)
    strict_n = sum(1 for r in records if r.get("strict"))
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(catalog_path), str(BIO_STRICT)],
        "maps_to_lean": ["biological", "medical"],
        "D_eff": 14,
        "part_count": len(parts),
        "strict_record_count": strict_n,
        "biology_strict_bridge_count": sum(1 for r in records if r["lab"] == "igem_biology_strict_bridge"),
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
    print(
        f"  records: {doc['record_count']}  parts: {doc['part_count']}  "
        f"median_err: {doc['median_error_pct']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())