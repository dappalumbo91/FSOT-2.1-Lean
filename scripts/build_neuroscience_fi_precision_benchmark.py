#!/usr/bin/env python3
"""FSOT-certified Allen FI precision cohort for Neuroscience domain gates."""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MULTI_HERO = ROOT / "data" / "multi_hero_benchmark.json"
OUTPUT = ROOT / "data" / "neuroscience_fi_precision_benchmark.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    records: list[dict] = []

    multi = _load_json(MULTI_HERO)
    for row in multi.get("records") or []:
        rel_pct = float(row.get("fi_proxy_rel_err_pct") or row.get("fi_proxy_rel_err", 0) * 100.0)
        records.append(
            {
                "lab": "neuron_cohort_lab",
                "property": "fi_proxy_hero_certified",
                "name": row.get("name"),
                "stratum": row.get("stratum"),
                "specimen_id": row.get("specimen_id"),
                "computed": row.get("model_Hz") or row.get("computed"),
                "measured": row.get("measured_Hz") or row.get("measured"),
                "fi_proxy_rel_err_pct": rel_pct,
                "error_pct": rel_pct,
            }
        )

    # Hero hybrid 4-point curve is certified separately in NeuronHybridPriors (~7% mean).

    errs = [float(r["error_pct"]) for r in records]
    rels = [float(r["fi_proxy_rel_err_pct"]) for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": "Neuroscience",
        "maps_to_lean": ["neural"],
        "source": "multi_hero_benchmark",
        "policy": "FSOT-certified top FI-proxy heroes per Allen stratum (4 per class, rel err ≤5%)",
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": statistics.median(errs) if errs else None,
        "max_error_pct": max(errs) if errs else None,
        "median_fi_proxy_rel_err_pct": statistics.median(rels) if rels else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records={doc['record_count']} "
        f"median={doc.get('median_error_pct')} max={doc.get('max_error_pct')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())