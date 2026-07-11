#!/usr/bin/env python3
"""Enrich extension benchmark JSONs with display labels and scientific measurement metadata."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_label_registry_lib import annotate_record, resolve_extension_domain  # noqa: E402
from literature_uncertainty_lib import is_contested_record  # noqa: E402
from scientific_measurement_lib import domain_precision_summary, measurement_envelope  # noqa: E402


def _yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


MAX_PER_RECORD_ENRICH = 10_000


def enrich_benchmark(path: Path, domain_key: str) -> dict | None:
    if not path.exists():
        return None
    doc = json.loads(path.read_text(encoding="utf-8"))
    domain_meta = resolve_extension_domain(domain_key)
    doc["display_name"] = domain_meta["display_name"]
    doc["tier_label"] = domain_meta["tier_label"]

    for key in ("records", "material_records"):
        recs = doc.get(key)
        if not isinstance(recs, list):
            continue
        if len(recs) > MAX_PER_RECORD_ENRICH:
            doc["scientific_precision_summary"] = domain_precision_summary(recs)
            continue
        enriched: list[dict] = []
        for rec in recs:
            row = annotate_record(rec)
            row["scientific_measurement"] = measurement_envelope(row, contested=is_contested_record(row))
            enriched.append(row)
        doc[key] = enriched
        doc["scientific_precision_summary"] = domain_precision_summary(enriched)

    doc["scientific_metadata_enriched_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return {"domain": domain_key, "path": str(path), "records": len(doc.get("records") or doc.get("material_records") or [])}


def main() -> int:
    spec = _yaml(MANIFEST)
    results: list[dict] = []
    for name, cfg in (spec.get("extension_domains") or {}).items():
        rel = cfg.get("benchmark_data")
        if not rel:
            continue
        meta = enrich_benchmark(ROOT / rel, name)
        if meta:
            results.append(meta)

    print(f"Enriched {len(results)} extension benchmarks with labels + scientific metadata")
    for row in results[:5]:
        print(f"  {row['domain']}: {row['records']} records")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())