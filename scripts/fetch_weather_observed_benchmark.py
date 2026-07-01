#!/usr/bin/env python3
"""Download Open-Meteo archive; verify FSOT stability classifier on real observations."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
WEATHER_ROOT = Path(r"C:\Users\damia\Desktop\weather")
SIM_LOG = WEATHER_ROOT / "fsot_weather_sim_log.json"
OUTPUT = ROOT / "data" / "weather_observed_benchmark.json"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

DEFAULT_LAT = 41.43
DEFAULT_LON = -84.87
STABILITY_DELTA_HPA = 3.0

sys.path.insert(0, str(ROOT / "scripts"))
from weather_fsot_scalar import compute_S_D_chaotic, map_to_fsot_params  # noqa: E402


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def fetch_archive(lat: float, lon: float, start: str, end: str) -> dict:
    if requests is None:
        raise RuntimeError("requests required: pip install requests")
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": "pressure_msl,wind_speed_10m,precipitation",
        "timezone": "UTC",
    }
    resp = requests.get(ARCHIVE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def build_from_archive(archive: dict, lat: float, lon: float) -> dict:
    hourly = archive.get("hourly") or {}
    times = hourly.get("time") or []
    pressures = hourly.get("pressure_msl") or []
    winds = hourly.get("wind_speed_10m") or []
    precips = hourly.get("precipitation") or []

    hours: list[dict] = []
    for i, t in enumerate(times):
        p = pressures[i] if i < len(pressures) else None
        w = winds[i] if i < len(winds) else None
        pr = precips[i] if i < len(precips) else None
        if p is None or w is None or pr is None:
            continue
        params = map_to_fsot_params(float(p), float(w), float(pr), observed=True)
        S = compute_S_D_chaotic(params)
        hours.append(
            {
                "timestamp": t,
                "pressure_hPa": float(p),
                "wind_mps": float(w),
                "precip_mm": float(pr),
                "S": round(S, 6),
            }
        )

    records: list[dict] = []
    hits = 0
    total = 0
    for i in range(len(hours) - 1):
        cur = hours[i]
        nxt = hours[i + 1]
        delta_p = abs(nxt["pressure_hPa"] - cur["pressure_hPa"])
        stable_actual = delta_p < STABILITY_DELTA_HPA
        predicted_stable = cur["S"] > 0
        correct = predicted_stable == stable_actual
        if correct:
            hits += 1
        total += 1
        records.append(
            {
                "lab": "weather_lab",
                "property": "stability_classifier",
                "name": cur["timestamp"],
                "computed": 1.0 if predicted_stable else 0.0,
                "measured": 1.0 if stable_actual else 0.0,
                "error_pct": 0.0 if correct else 100.0,
                "S": cur["S"],
                "delta_pressure_hPa": delta_p,
            }
        )

    errs = [r["error_pct"] for r in records]
    return {
        "source": "open-meteo-archive",
        "location": {"lat": lat, "lon": lon},
        "hour_count": len(hours),
        "classification_records": len(records),
        "stability_classification_accuracy": hits / total if total else None,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "max_error_pct": max(errs) if errs else None,
        "records": records,
        "observed_hours": hours,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch weather observed benchmark")
    parser.add_argument("--sim-log", type=Path, default=SIM_LOG)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT)
    parser.add_argument("--lon", type=float, default=DEFAULT_LON)
    parser.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()

    if args.sim_log.exists():
        sim_rows = json.loads(args.sim_log.read_text(encoding="utf-8"))
        start_dt = _parse_ts(sim_rows[0]["timestamp"])
        end_dt = _parse_ts(sim_rows[-1]["timestamp"])
    else:
        start_dt = datetime.utcnow() - timedelta(hours=args.hours)
        end_dt = start_dt + timedelta(hours=args.hours)

    start = start_dt.strftime("%Y-%m-%d")
    end = end_dt.strftime("%Y-%m-%d")

    print(f"Fetching Open-Meteo archive {start}..{end} ({args.lat}, {args.lon})")
    try:
        archive = fetch_archive(args.lat, args.lon, start, end)
        doc = build_from_archive(archive, args.lat, args.lon)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Drop bulky hour payload from committed JSON
    out_doc = {k: v for k, v in doc.items() if k != "observed_hours"}
    args.output.write_text(json.dumps(out_doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  classification records: {out_doc['classification_records']}")
    if out_doc.get("median_error_pct") is not None:
        print(f"  median_error_pct: {out_doc['median_error_pct']:.4f}")
    if out_doc.get("stability_classification_accuracy") is not None:
        print(f"  stability_accuracy: {100 * out_doc['stability_classification_accuracy']:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())