#!/usr/bin/env python3
"""GRACE cryosphere benchmark — month-over-month Greenland mass-loss direction."""

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
MANIFEST = ROOT / "data" / "grace_cryosphere_manifest.yaml"
CACHE = ROOT / "data" / "grace_greenland_cache.json"
OUTPUT = ROOT / "data" / "grace_cryosphere_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_grace_greenland.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    threshold = float(spec["source"]["decline_threshold_gt"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    from geophysical_empirical_scalar import grace_mass_loss_cutoff_gt  # noqa: E402

    loss_cutoff, scalar_meta = grace_mass_loss_cutoff_gt(threshold, mod=mod)

    series = sorted(doc.get("records") or [], key=lambda r: r.get("month") or "")
    records: list[dict] = []
    for prev, cur in zip(series, series[1:]):
        prev_mass = float(prev["mass_gt"])
        cur_mass = float(cur["mass_gt"])
        delta = cur_mass - prev_mass
        observed_loss = delta < threshold
        predicted_loss = delta < loss_cutoff
        match = observed_loss == predicted_loss
        records.append(
            {
                "lab": "grace_cryosphere_lab",
                "property": "greenland_mass_decline_classifier",
                "name": cur.get("month"),
                "mass_gt": round(cur_mass, 3),
                "delta_gt": round(delta, 3),
                "computed_loss": 1.0 if predicted_loss else 0.0,
                "measured_loss": 1.0 if observed_loss else 0.0,
                "error_pct": 0.0 if match else 100.0,
                **scalar_meta,
            }
        )

    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "GFZ_GravIS_Greenland_total",
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 16,
        "crosswalk_modules": ["FSOT.Formal.CryospherePriors", "FSOT.Formal.GraceCryospherePriors"],
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  match: {doc['stability_match_rate']:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())