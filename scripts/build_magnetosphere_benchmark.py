#!/usr/bin/env python3
"""Magnetosphere benchmark — coupled Dst + Kp storm classifier with magnetic-string anchor."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "magnetosphere_manifest.yaml"
OUTPUT = ROOT / "data" / "magnetosphere_benchmark.json"


def _daily_max_kp(kp_cache_path: Path) -> dict[str, float]:
    doc = json.loads(kp_cache_path.read_text(encoding="utf-8"))
    daily: dict[str, float] = defaultdict(float)
    for row in doc.get("records") or []:
        tag = row.get("time_tag") or ""
        day = tag[:10]
        if not day:
            continue
        kp = float(row.get("kp") or 0.0)
        if kp > daily[day]:
            daily[day] = kp
    return dict(daily)


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    geo_path = ROOT / src["geomagnetism_cache"]
    kp_path = ROOT / src["kp_cache"]
    if not geo_path.exists():
        raise FileNotFoundError(f"Run ingest_geomagnetism_swpc.py first: {geo_path}")
    if not kp_path.exists():
        raise FileNotFoundError(f"Kp cache missing: {kp_path}")

    geo = json.loads(geo_path.read_text(encoding="utf-8"))
    daily_kp = _daily_max_kp(kp_path)
    dst_thr = float(src["dst_storm_threshold"])
    kp_thr = float(src["kp_storm_threshold"])
    s_em_ref = float(src["magnetic_S_em"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_em = float(mod.domain_scalar("Electromagnetism"))
    S_fusion = float(mod.domain_scalar("Thermodynamics"))

    records: list[dict] = []
    for row in geo.get("dst") or []:
        tag = row.get("time_tag") or ""
        dst = row.get("dst")
        if dst is None or not tag:
            continue
        day = tag[:10]
        max_kp = daily_kp.get(day, 0.0)
        observed_storm = float(dst) <= dst_thr or max_kp >= kp_thr
        adj_dst = dst_thr - abs(S_em) * 5.0
        adj_kp = kp_thr - abs(S_fusion) * 0.5
        predicted_storm = float(dst) <= adj_dst or max_kp >= adj_kp
        match = observed_storm == predicted_storm
        records.append(
            {
                "lab": "magnetosphere_lab",
                "property": "coupled_dst_kp_storm_classifier",
                "name": tag,
                "dst_nt": float(dst),
                "daily_max_kp": round(max_kp, 3),
                "magnetic_S_em": round(s_em_ref, 6),
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
        "source": "geomagnetism_x_space_weather_x_magnetic_string",
        "record_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 14,
        "crosswalk_modules": [
            "FSOT.Formal.GeomagnetismPriors",
            "FSOT.Formal.SpaceWeatherPriors",
            "FSOT.Formal.MagneticStringPriors",
        ],
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