#!/usr/bin/env python3
"""Geomagnetism benchmark — Dst/GOES storm classifier."""

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
MANIFEST = ROOT / "data" / "geomagnetism_manifest.yaml"
CACHE = ROOT / "data" / "geomagnetism_swpc_cache.json"
OUTPUT = ROOT / "data" / "geomagnetism_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_geomagnetism_swpc.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    dst_thr = float(spec["source"]["dst_storm_threshold"])
    hp_thr = float(spec["source"]["hp_storm_threshold"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_em = float(mod.domain_scalar("Electromagnetism"))
    union_classifier = str(spec.get("classifier_mode") or "union") == "union"

    sys.path.insert(0, str(ROOT / "scripts"))
    from magnetosphere_timeline import dst_storm_predicted, kp_storm_predicted  # noqa: E402

    records: list[dict] = []
    for row in doc.get("dst") or []:
        dst = row.get("dst")
        if dst is None:
            continue
        observed_storm = float(dst) <= dst_thr
        adj_thr = dst_thr - abs(S_em) * 5.0
        predicted_storm = dst_storm_predicted(
            float(dst), dst_thr=dst_thr, adj_dst=adj_thr, union_classifier=union_classifier
        )
        match = observed_storm == predicted_storm
        records.append(
            {
                "lab": "geomagnetism_lab",
                "property": "dst_storm_classifier",
                "name": row.get("time_tag"),
                "dst_nt": float(dst),
                "computed_storm": 1.0 if predicted_storm else 0.0,
                "measured_storm": 1.0 if observed_storm else 0.0,
                "error_pct": 0.0 if match else 100.0,
            }
        )

    for row in doc.get("goes_magnetometers") or []:
        hp = row.get("Hp")
        if hp is None:
            continue
        observed_storm = float(hp) >= hp_thr
        adj_thr = hp_thr - abs(S_em) * 10.0
        predicted_storm = kp_storm_predicted(
            float(hp), kp_thr=hp_thr, adj_kp=adj_thr, union_classifier=union_classifier
        )
        match = observed_storm == predicted_storm
        records.append(
            {
                "lab": "geomagnetism_lab",
                "property": "hp_storm_classifier",
                "name": row.get("time_tag"),
                "hp_nt": float(hp),
                "computed_storm": 1.0 if predicted_storm else 0.0,
                "measured_storm": 1.0 if observed_storm else 0.0,
                "error_pct": 0.0 if match else 100.0,
            }
        )

    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "NOAA_SWPC_geomag",
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 13,
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