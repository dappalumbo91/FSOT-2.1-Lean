#!/usr/bin/env python3
"""Build open-science expansion benchmarks from live vendor caches.

Produces:
  - data/open_science_live_concordance_benchmark.json
  - data/open_science_seed_constants_benchmark.json
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from open_science_sources_lib import (  # noqa: E402
    OPEN_SOURCES,
    build_evidence_rows,
    build_seed_constant_rows,
    vendor_dir,
)

OUT_CONCORD = ROOT / "data" / "open_science_live_concordance_benchmark.json"
OUT_SEEDS = ROOT / "data" / "open_science_seed_constants_benchmark.json"


def _median(vals: list[float]) -> float | None:
    return statistics.median(vals) if vals else None


def main() -> int:
    evidence_rows: list[dict] = []
    streams_ok = 0
    streams_fail = 0

    for src in OPEN_SOURCES:
        live = vendor_dir(src.id) / "live.json"
        if not live.exists():
            streams_fail += 1
            evidence_rows.append(
                {
                    "id": f"{src.id}_missing_cache",
                    "name": src.id,
                    "kind": "open_stream_evidence",
                    "error_pct": 100.0,
                    "green_eligible": False,
                    "status": "missing_cache",
                    "source": src.id,
                    "family": src.family,
                }
            )
            continue
        doc = json.loads(live.read_text(encoding="utf-8"))
        streams_ok += 1
        evidence_rows.extend(build_evidence_rows(src, doc))

    seed_rows = build_seed_constant_rows()
    seed_errs = [float(r["error_pct"]) for r in seed_rows if r.get("green_eligible")]
    green_errs = [
        float(r["error_pct"])
        for r in evidence_rows
        if r.get("green_eligible") and r.get("error_pct") is not None
    ]

    seed_doc = {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": "Open_Science_Seed_Constants",
        "authority_path": "vendor/fsot_compute.py",
        "source": ["python_mathlib_identity", "nist_codata_ascii"],
        "maps_to_lean": ["atomic", "particle"],
        "D_eff": 7,
        "record_count": len(seed_rows),
        "observable_count": len(seed_rows),
        "scalar_record_count": len(seed_rows),
        "scalar_gate_applicable": True,
        "median_error_pct": _median(seed_errs),
        "pooled_median_error_pct": _median(seed_errs),
        "headline_median_error_pct": _median(seed_errs),
        "fsot_precision_gate_pct": 0.5,
        "policy": "no_signup_no_credentials",
        "scientific_metric_primary": "relative_percent_error",
        "scientific_metric_also": ["ppm_when_sub_0.01pct"],
        "records": seed_rows,
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "note": "Seed identities and NIST CODATA anchors; zero free parameters",
        },
    }

    concord_doc = {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": "Open_Science_Live_Concordance",
        "authority_path": "vendor/fsot_compute.py",
        "source": [s.id for s in OPEN_SOURCES],
        "maps_to_lean": ["biology", "chemistry", "cosmology", "earth_science"],
        "D_eff": 12,
        "record_count": len(evidence_rows),
        "observable_count": len(evidence_rows),
        "streams_ok": streams_ok,
        "streams_missing": streams_fail,
        "scalar_record_count": len(green_errs),
        "scalar_gate_applicable": bool(green_errs),
        "median_error_pct": _median(green_errs) if green_errs else 0.0,
        "pooled_median_error_pct": _median(green_errs) if green_errs else 0.0,
        "headline_median_error_pct": _median(green_errs) if green_errs else 0.0,
        "fsot_precision_gate_pct": 0.5,
        "policy": "no_signup_no_credentials",
        "scientific_metric_primary": "mixed_stream_and_literature_integrity",
        "scientific_metric_also": [
            "stream_availability",
            "relative_percent_error",
            "year_over_year_percent_change",
        ],
        "records": evidence_rows,
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "note": (
                "Open streams bolster real-data connectivity. Green-eligible rows are "
                "seed/NIST/literature integrity checks — not post-hoc fits."
            ),
        },
    }

    OUT_SEEDS.write_text(json.dumps(seed_doc, indent=2), encoding="utf-8")
    OUT_CONCORD.write_text(json.dumps(concord_doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_SEEDS} n={len(seed_rows)} median={seed_doc['median_error_pct']}")
    print(
        f"Wrote {OUT_CONCORD} n={len(evidence_rows)} streams_ok={streams_ok} "
        f"green_median={concord_doc['median_error_pct']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
