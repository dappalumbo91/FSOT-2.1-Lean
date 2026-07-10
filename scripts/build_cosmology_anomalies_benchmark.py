#!/usr/bin/env python3
"""Build cosmology anomalies benchmark — tensions explained by BH→WH mechanics."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_anomalies_manifest.yaml"
OUTPUT = ROOT / "data" / "cosmology_anomalies_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))
from cosmology_anomalies_physics import load_auxiliary, predict_anomaly  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from cosmology_lambda import H0_CANONICAL  # noqa: E402


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    seed_path = ROOT / spec["source"]["anomalies_seed"]
    anomalies = json.loads(seed_path.read_text(encoding="utf-8")).get("anomalies") or []

    bleed_doc = {}
    bleed_path = ROOT / spec["source"]["bubble_bleed_benchmark"]
    if bleed_path.exists():
        bleed_doc = json.loads(bleed_path.read_text(encoding="utf-8"))

    bleed_frac = float(bleed_doc.get("bubble_bleed_fraction") or 0.015431)
    sectors_doc, nebulae, frbs = load_auxiliary()

    mod, authority_path = load_fsot_compute()
    records: list[dict] = []
    for row in anomalies:
        measured = float(row["measured"])
        computed = predict_anomaly(
            row,
            mod,
            bleed_frac=bleed_frac,
            h0_global=H0_CANONICAL,
            sectors_doc=sectors_doc,
            nebulae=nebulae,
            frbs=frbs,
        )
        if computed is None:
            continue
        err = _error_pct(computed, measured)
        records.append(
            {
                "lab": "cosmology_anomalies_lab",
                "property": row.get("category"),
                "name": row.get("name"),
                "mechanism": row.get("mechanism"),
                "computed": computed if abs(computed) < 1e-6 else round(computed, 8),
                "measured": measured,
                "error_pct": round(err, 6),
                "unit": row.get("unit"),
                "reference": row.get("reference"),
            }
        )

    errs = [float(r["error_pct"]) for r in records]
    resolved = sum(1 for e in errs if e <= 15.0)

    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "mechanism": "bh_wh_bubble_bleed_anomalies",
        "h0_global_fsot": H0_CANONICAL,
        "bubble_bleed_fraction": bleed_frac,
        "record_count": len(records),
        "observable_count": len(records),
        "resolved_within_15pct_count": resolved,
        "resolved_fraction": resolved / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "max_error_pct": max(errs) if errs else None,
        "maps_to_lean": ["cosmological", "cmb", "blackhole"],
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = build(args.manifest)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  anomalies: {bench['record_count']}  resolved≤15%: {bench['resolved_fraction']:.1%}")
    print(f"  median err: {bench['median_error_pct']}%  max err: {bench['max_error_pct']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())