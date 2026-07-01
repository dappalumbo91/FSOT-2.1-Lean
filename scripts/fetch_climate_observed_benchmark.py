#!/usr/bin/env python3
"""Open-Meteo fallback climate benchmark (use build_climate_observed_benchmark.py for NCEI)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "climate_observed_benchmark.json"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

sys.path.insert(0, str(ROOT / "scripts"))
from weather_fsot_scalar import compute_S_D_chaotic, map_to_fsot_params  # noqa: E402

DEFAULT_LAT = 39.74
DEFAULT_LON = -104.99
ANOMALY_TEMP_TOLERANCE_C = 2.5


def fetch_monthly(lat: float, lon: float, start: str, end: str) -> dict:
    if requests is None:
        raise RuntimeError("requests required: pip install requests")
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": "temperature_2m_mean,precipitation_sum,pressure_msl_mean,windspeed_10m_max",
        "timezone": "UTC",
    }
    resp = requests.get(ARCHIVE_URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def build_benchmark(archive: dict, lat: float, lon: float) -> dict:
    daily = archive.get("daily") or {}
    times = daily.get("time") or []
    temps = daily.get("temperature_2m_mean") or []
    precips = daily.get("precipitation_sum") or []
    pressures = daily.get("pressure_msl_mean") or []
    winds = daily.get("windspeed_10m_max") or []

    monthly: dict[str, list[float]] = {}
    monthly_p: dict[str, list[float]] = {}
    monthly_w: dict[str, list[float]] = {}
    monthly_pr: dict[str, list[float]] = {}
    by_cal_month: dict[str, list[float]] = {}
    for i, t in enumerate(times):
        month = t[:7]
        cal_m = t[5:7]
        if i < len(temps) and temps[i] is not None:
            val = float(temps[i])
            monthly.setdefault(month, []).append(val)
            by_cal_month.setdefault(cal_m, []).append(val)
        if i < len(precips) and precips[i] is not None:
            monthly_pr.setdefault(month, []).append(float(precips[i]))
        if i < len(pressures) and pressures[i] is not None:
            monthly_p.setdefault(month, []).append(float(pressures[i]))
        if i < len(winds) and winds[i] is not None:
            monthly_w.setdefault(month, []).append(float(winds[i]))

    month_clim = {m: sum(v) / len(v) for m, v in by_cal_month.items()}
    records: list[dict] = []
    for month in sorted(monthly.keys()):
        t_mean = sum(monthly[month]) / len(monthly[month])
        cal_m = month[5:7]
        anomaly = t_mean - month_clim.get(cal_m, t_mean)
        p = sum(monthly_p.get(month, [1013.0])) / max(1, len(monthly_p.get(month, [1013.0])))
        w = sum(monthly_w.get(month, [5.0])) / max(1, len(monthly_w.get(month, [5.0])))
        pr = sum(monthly_pr.get(month, [0.0])) / max(1, len(monthly_pr.get(month, [0.0])))
        params = map_to_fsot_params(p, w, pr, observed=True)
        params["D_eff"] = 16.0
        S = compute_S_D_chaotic(params)
        predicted_stable = S > 0
        observed_stable = abs(anomaly) < ANOMALY_TEMP_TOLERANCE_C
        match = predicted_stable == observed_stable
        records.append(
            {
                "lab": "climate_lab",
                "property": "monthly_temp_anomaly_stability",
                "name": month,
                "computed": 1.0 if predicted_stable else 0.0,
                "measured": 1.0 if observed_stable else 0.0,
                "error_pct": 0.0 if match else 100.0,
                "anomaly_c": round(anomaly, 4),
                "S": round(S, 6),
            }
        )

    errs = [r["error_pct"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Open-Meteo_archive_api",
        "note": "Lightweight monthly sample; not full NOAA NCEI ingest",
        "latitude": lat,
        "longitude": lon,
        "climatology_method": "per_calendar_month_baseline",
        "month_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch climate observed benchmark")
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT)
    parser.add_argument("--lon", type=float, default=DEFAULT_LON)
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    archive = fetch_monthly(args.lat, args.lon, args.start, args.end)
    doc = build_benchmark(archive, args.lat, args.lon)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  months: {doc['month_count']}  median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())