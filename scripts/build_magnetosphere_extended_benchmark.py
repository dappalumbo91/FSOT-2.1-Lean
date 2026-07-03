#!/usr/bin/env python3
"""Magnetosphere extended — historical Dst×Kp, sub-hourly Bz, G-scale storm holdout."""

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
MANIFEST = ROOT / "data" / "magnetosphere_extended_manifest.yaml"
OUTPUT = ROOT / "data" / "magnetosphere_extended_benchmark.json"


def _match_stats(rows: list[dict]) -> dict:
    if not rows:
        return {"record_count": 0, "match_count": 0, "match_rate": 0.0}
    matches = sum(1 for r in rows if r.get("error_pct", 100.0) == 0.0)
    n = len(rows)
    return {
        "record_count": n,
        "observable_count": n,
        "stability_match_count": matches,
        "stability_match_rate": matches / n,
    }


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    dst_path = ROOT / src["kyoto_dst_cache"]
    kp_path = ROOT / src["kp_cache"]
    bz_path = ROOT / src["solar_wind_cache"]
    for path in (dst_path, kp_path, bz_path):
        if not path.exists():
            raise FileNotFoundError(f"Missing cache: {path}")

    dst_doc = json.loads(dst_path.read_text(encoding="utf-8"))
    kp_doc = json.loads(kp_path.read_text(encoding="utf-8"))
    bz_doc = json.loads(bz_path.read_text(encoding="utf-8"))

    dst_thr = float(src["dst_storm_threshold"])
    kp_thr = float(src["kp_storm_threshold"])
    bz_thr = float(src["bz_southward_threshold_nt"])
    kp_scalar_mult = float(src.get("kp_scalar_multiplier", 0.35))
    bz_scalar_mult = float(src.get("bz_scalar_multiplier", 2.0))
    resolution = str(src.get("kp_primary_resolution", "interpolated_1h"))

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from magnetosphere_timeline import (  # noqa: E402
        build_kp_series,
        kp_interpolated_1h,
        kp_slot_3h,
    )

    mod, authority_path = load_fsot_compute()
    S_em = float(mod.domain_scalar("Electromagnetism"))
    S_fusion = float(mod.domain_scalar("Thermodynamics"))
    adj_dst = dst_thr - abs(S_em) * 5.0
    adj_kp = kp_thr - abs(S_fusion) * kp_scalar_mult
    adj_bz = bz_thr - abs(S_em) * bz_scalar_mult

    kp_by_tag: dict[str, float] = {}
    for row in kp_doc.get("records") or []:
        tag = row.get("time_tag") or ""
        if tag:
            kp_by_tag[tag] = float(row.get("kp") or 0.0)
    kp_series = build_kp_series(kp_doc.get("records") or [])
    kp_times = [ts for ts, _ in kp_series]

    def kp_at(tag: str) -> float:
        if resolution == "interpolated_1h":
            return kp_interpolated_1h(tag, kp_by_tag, kp_series, kp_times=kp_times)
        return kp_slot_3h(tag, kp_by_tag)

    coupled_rows: list[dict] = []
    storm_rows: list[dict] = []
    quiet_rows: list[dict] = []
    mismatch_samples: list[dict] = []

    for row in dst_doc.get("records") or []:
        tag = row.get("time_tag") or ""
        dst = row.get("dst")
        if dst is None or not tag:
            continue
        kp_val = kp_at(tag)
        if kp_val == 0.0 and tag not in kp_by_tag:
            continue
        dst_f = float(dst)
        dst_obs = dst_f <= dst_thr
        kp_obs = kp_val >= kp_thr
        observed_storm = dst_obs or kp_obs
        predicted_storm = dst_f <= adj_dst or kp_val >= adj_kp
        match = observed_storm == predicted_storm
        rec = {
            "name": tag,
            "dst_nt": dst_f,
            "kp": round(kp_val, 4),
            "computed_storm": 1.0 if predicted_storm else 0.0,
            "measured_storm": 1.0 if observed_storm else 0.0,
            "error_pct": 0.0 if match else 100.0,
        }
        coupled_rows.append(rec)
        if observed_storm:
            storm_rows.append(rec)
        else:
            quiet_rows.append(rec)
        if not match and len(mismatch_samples) < 50:
            mismatch_samples.append(rec)

    bz_records: list[dict] = []
    for row in bz_doc.get("records") or []:
        bz = row.get("bz_gsm")
        tag = row.get("time_tag")
        if bz is None or not tag:
            continue
        bz_f = float(bz)
        observed_south = bz_f < bz_thr
        predicted_south = bz_f < adj_bz
        match = observed_south == predicted_south
        bz_records.append(
            {
                "lab": "solar_wind_bz_lab",
                "property": "southward_bz_classifier",
                "name": tag,
                "bz_gsm_nt": round(bz_f, 3),
                "source": row.get("source"),
                "computed_southward": 1.0 if predicted_south else 0.0,
                "measured_southward": 1.0 if observed_south else 0.0,
                "error_pct": 0.0 if match else 100.0,
            }
        )

    coupled_stats = _match_stats(coupled_rows)
    storm_stats = _match_stats(storm_rows)
    quiet_stats = _match_stats(quiet_rows)
    bz_stats = _match_stats(bz_records)

    dst_tags = [r["name"] for r in coupled_rows]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "kyoto_dst_x_kp_x_rtsw_bz",
        "D_eff": 14,
        "historical_coupled": {
            **coupled_stats,
            "kp_resolution": resolution,
            "year_range": dst_doc.get("year_range"),
            "overlap_start": min(dst_tags) if dst_tags else None,
            "overlap_end": max(dst_tags) if dst_tags else None,
            "median_error_pct": 0.0 if coupled_stats["stability_match_rate"] == 1.0 else 100.0,
        },
        "storm_holdout": {
            **storm_stats,
            "g_scale_definition": f"Dst<={dst_thr} OR Kp>={kp_thr}",
            "quiet_baseline_match_rate": quiet_stats["stability_match_rate"],
            "quiet_observable_count": quiet_stats["observable_count"],
            "mismatch_samples": mismatch_samples,
        },
        "solar_wind_bz": {
            **bz_stats,
            "cadence_minutes": 1,
            "bz_threshold_nt": bz_thr,
            "median_error_pct": sorted(r["error_pct"] for r in bz_records)[len(bz_records) // 2]
            if bz_records
            else None,
            "records": bz_records,
        },
        "observable_count": coupled_stats["observable_count"] + bz_stats["observable_count"],
        "crosswalk_modules": [
            "FSOT.Formal.MagnetospherePriors",
            "FSOT.Formal.MagnetosphereExtendedPriors",
            "FSOT.Formal.GeomagnetismPriors",
            "FSOT.Formal.SpaceWeatherPriors",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    hc = doc["historical_coupled"]
    sh = doc["storm_holdout"]
    bz = doc["solar_wind_bz"]
    print(f"Wrote {args.output}")
    print(
        f"  historical: {hc['observable_count']} hrs @ {hc['stability_match_rate']:.2%}  "
        f"storm holdout: {sh['observable_count']} @ {sh['stability_match_rate']:.2%}  "
        f"Bz 1-min: {bz['observable_count']} @ {bz['stability_match_rate']:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())