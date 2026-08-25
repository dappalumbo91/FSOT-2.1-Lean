#!/usr/bin/env python3
"""Issue dated, located fluid-pressure forecasts from live public catalogs.

Freeze: predictions/dated_forecasts/<UTC-date>_issue.json + LATEST.json
Score later: python scripts/score_earth_fluid_forecasts.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_earth_fluid_forecast import (  # noqa: E402
    earthquake_forecasts,
    forecast_horizon_days,
    kernel_km,
    solar_forecasts,
    volcanic_forecasts,
    weather_forecasts,
)

OUT_DIR = ROOT / "predictions" / "dated_forecasts"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query"
SWPC_KP = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
NDBC_LATEST = "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt"
NDBC_CACHE = ROOT / "vendor" / "public_verifiable" / "live_cache" / "noaa_ndbc_cache.json"


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/earth-fluid-forecast"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_usgs(days: int = 14, minmag: float = 4.5) -> list[dict]:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days)).strftime("%Y-%m-%d")
    url = (
        f"{USGS}?format=geojson&starttime={start}&minmagnitude={minmag}"
        f"&orderby=time&limit=500"
    )
    doc = json.loads(_get(url).decode("utf-8"))
    rows = []
    for feat in doc.get("features") or []:
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None, None]
        if coords[0] is None or props.get("mag") is None:
            continue
        rows.append(
            {
                "id": feat.get("id"),
                "mag": float(props["mag"]),
                "lat": float(coords[1]),
                "lon": float(coords[0]),
                "depth_km": coords[2],
                "place": props.get("place"),
                "time": props.get("time"),
                "type": props.get("type"),
            }
        )
    return rows


def fetch_swpc_kp() -> list[dict]:
    try:
        doc = json.loads(_get(SWPC_KP).decode("utf-8"))
    except Exception:
        return []
    if isinstance(doc, list):
        return doc
    return []


def fetch_ndbc() -> list[dict]:
    try:
        text = _get(NDBC_LATEST, timeout=45).decode("utf-8", errors="replace")
    except Exception:
        text = ""
    rows: list[dict] = []
    if text:
        for line in text.splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 17:
                continue
            try:
                rows.append(
                    {
                        "buoy_id": parts[0],
                        "lat": float(parts[1]),
                        "lon": float(parts[2]),
                        "wspd": float(parts[9]) if parts[9] not in {"MM", "999"} else 0.0,
                        "gst": float(parts[10]) if parts[10] not in {"MM", "999"} else 0.0,
                        "pres": float(parts[15]) if parts[15] not in {"MM", "9999"} else 0.0,
                    }
                )
            except ValueError:
                continue
    if rows:
        return rows
    if NDBC_CACHE.is_file():
        cached = json.loads(NDBC_CACHE.read_text(encoding="utf-8"))
        return list(cached.get("rows") or [])
    return []


def main() -> int:
    issued = datetime.now(timezone.utc).replace(microsecond=0)
    quakes = fetch_usgs()
    kp = fetch_swpc_kp()
    buoys = fetch_ndbc()
    eq = earthquake_forecasts(quakes, issued=issued)
    wx = weather_forecasts(buoys, issued=issued)
    sol = solar_forecasts(kp, issued=issued)
    volc = volcanic_forecasts(quakes, issued=issued)
    all_f = eq + wx + sol + volc
    doc = {
        "schema_version": "1.0",
        "pin": "D1D38A",
        "issued_at": issued.isoformat(),
        "horizon_days_eq": forecast_horizon_days(),
        "kernel_km": kernel_km(),
        "policy": [
            "windowed_spatial_class_not_a_clock_time",
            "pressure_loads_then_POOF",
            "score_in_results_do_not_rewrite_this_issue",
        ],
        "catalogs": {
            "usgs_n": len(quakes),
            "ndbc_n": len(buoys),
            "swpc_kp_n": len(kp),
        },
        "forecasts": all_f,
        "n_eq": len(eq),
        "n_wx": len(wx),
        "n_sol": len(sol),
        "n_volc": len(volc),
        "score_command": "python scripts/score_earth_fluid_forecasts.py",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    day = OUT_DIR / f"{issued.strftime('%Y-%m-%d')}_issue.json"
    latest = OUT_DIR / "LATEST.json"
    text = json.dumps(doc, indent=2)
    day.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    md = ROOT / "predictions" / "reports" / "DATED_FLUID_FORECASTS.md"
    lines = [
        "# Dated fluid-pressure forecasts (this issue)",
        "",
        f"*Issued {issued.isoformat()} · pin D1D38A · kernel **{kernel_km():.1f} km** · EQ window **{forecast_horizon_days()} d***",
        "",
        "Pressure loads (SUCTION). The orifice opens (POOF). Location = catalog pressure cell.",
        "Date = calendar window. Score with `python scripts/score_earth_fluid_forecasts.py`.",
        "",
        f"USGS events used: **{len(quakes)}**. NDBC stations: **{len(buoys)}**. SWPC Kp samples: **{len(kp)}**.",
        "",
        "| ID | Kind | Where | Window | Call | Valve |",
        "|----|------|-------|--------|------|-------|",
    ]
    for fc in all_f:
        loc = fc["location"]
        pred = fc["predicted"]
        call = pred.get("class")
        if fc["kind"] == "earthquake":
            call = (
                f"M≥{pred['mag_min']} count≥{pred['min_count']}"
                if pred.get("expect_event")
                else f"no M≥{pred['mag_min']}"
            )
        elif fc["kind"] == "solar":
            call = "Kp≥5" if pred.get("expect_kp_ge_5") else "Kp stays <5"
        elif fc["kind"] == "weather":
            call = pred.get("class")
        lines.append(
            f"| `{fc['id']}` | {fc['kind']} | {loc.get('name')} "
            f"({loc.get('lat')},{loc.get('lon')}) r={loc.get('radius_km')} km | "
            f"{fc['valid_from'][:10]} → {fc['valid_to'][:10]} | {call} | "
            f"{pred.get('valve_state')} |"
        )
    lines += [
        "",
        "Frozen JSON: `predictions/dated_forecasts/LATEST.json`",
        "",
        "These are **not** USGS/NWS watches. They are FSOT valve cells so we can iron out hit/miss.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {day}")
    print(f"Wrote {latest}")
    print(f"Wrote {md}")
    print(f"  eq={len(eq)} wx={len(wx)} sol={len(sol)} volc={len(volc)}")
    for fc in eq[:8]:
        print(
            f"  {fc['id']}: {fc['location']['name'][:50]}  "
            f"M>={fc['predicted']['mag_min']} expect={fc['predicted']['expect_event']}  "
            f"{fc['predicted']['valve_state']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
