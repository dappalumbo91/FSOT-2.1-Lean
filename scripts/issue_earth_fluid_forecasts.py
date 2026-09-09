#!/usr/bin/env python3
"""Issue dated, located fluid-pressure forecasts from live public catalogs.

Freeze: predictions/dated_forecasts/<UTC-date>_issue.json
Never overwrite an existing dated issue (timestamp suffix if the day file exists).
LATEST.json is a pointer to the newest issue only.
Score later: python scripts/score_earth_fluid_forecasts.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_earth_fluid_forecast import (  # noqa: E402
    HYDRO_STATIONS,
    TIDE_STATIONS,
    earthquake_forecasts,
    forecast_horizon_days,
    hydrology_forecasts,
    kernel_km,
    solar_forecasts,
    tide_forecasts,
    volcanic_forecasts,
    weather_forecasts,
)

OUT_DIR = ROOT / "predictions" / "dated_forecasts"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query"
SWPC_KP = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
NDBC_LATEST = "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt"
NDBC_CACHE = ROOT / "vendor" / "public_verifiable" / "live_cache" / "noaa_ndbc_cache.json"
COOPS = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
NWIS_IV = "https://waterservices.usgs.gov/nwis/iv/"


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/earth-fluid-forecast"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_usgs(
    days: int = 14,
    minmag: float = 4.5,
    *,
    eventtype: str | None = None,
) -> list[dict]:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days)).strftime("%Y-%m-%d")
    url = (
        f"{USGS}?format=geojson&starttime={start}&minmagnitude={minmag}"
        f"&orderby=time&limit=500"
    )
    if eventtype:
        url += f"&eventtype={urllib.parse.quote(eventtype)}"
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


def _coops_series(station: str, product: str, begin: str, end: str) -> list[dict]:
    url = (
        f"{COOPS}?product={product}&application=FSOT-2.1-Lean"
        f"&station={station}&begin_date={begin}&end_date={end}"
        f"&datum=MLLW&time_zone=gmt&units=metric&format=json"
    )
    if product == "predictions":
        url += "&interval=h"
    try:
        doc = json.loads(_get(url, timeout=40).decode("utf-8"))
    except Exception:
        return []
    return list(doc.get("data") or doc.get("predictions") or [])


def _nearest_val(series: list[dict], target: datetime) -> float | None:
    best = None
    best_dt = None
    for row in series:
        tag = str(row.get("t") or "")
        try:
            t = datetime.strptime(tag, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        try:
            v = float(row.get("v"))
        except (TypeError, ValueError):
            continue
        if best is None or abs((t - target).total_seconds()) < abs((best_dt - target).total_seconds()):
            best, best_dt = v, t
    return best


def fetch_tide_snapshots(issued: datetime) -> list[dict]:
    begin = (issued - timedelta(hours=6)).strftime("%Y%m%d")
    end = (issued + timedelta(days=2)).strftime("%Y%m%d")
    out: list[dict] = []
    for st in TIDE_STATIONS:
        obs_s = _coops_series(st["id"], "water_level", begin, issued.strftime("%Y%m%d"))
        pred_s = _coops_series(st["id"], "predictions", begin, end)
        obs = _nearest_val(obs_s, issued)
        pred = _nearest_val(pred_s, issued)
        if obs is None or pred is None:
            continue
        out.append(
            {
                **st,
                "obs_m": round(obs, 4),
                "pred_m": round(pred, 4),
                "residual_m": round(obs - pred, 4),
            }
        )
    return out


def _nwis_values(ts: dict) -> list[tuple[datetime, float]]:
    vals = (ts.get("values") or [{}])[0].get("value") or []
    out: list[tuple[datetime, float]] = []
    for item in vals:
        raw = item.get("value")
        tag = str(item.get("dateTime") or "")
        if raw in (None, "", "-999999") or not tag:
            continue
        try:
            q = float(raw)
            t = datetime.fromisoformat(tag.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        if q < 0:
            continue
        out.append((t, q))
    return out


def fetch_nwis_snapshots(issued: datetime, days: int = 14) -> list[dict]:
    sites = ",".join(st["id"] for st in HYDRO_STATIONS)
    url = (
        f"{NWIS_IV}?format=json&sites={sites}&parameterCd=00060"
        f"&period=P{int(days)}D"
    )
    try:
        doc = json.loads(_get(url, timeout=60).decode("utf-8"))
    except Exception:
        return []
    series = ((doc.get("value") or {}).get("timeSeries")) or []
    by_site: dict[str, list[tuple[datetime, float]]] = {}
    for ts in series:
        site = str(((ts.get("sourceInfo") or {}).get("siteCode") or [{}])[0].get("value") or "")
        if not site:
            continue
        by_site.setdefault(site, []).extend(_nwis_values(ts))
    half = timedelta(days=days / 2.0)
    out: list[dict] = []
    for st in HYDRO_STATIONS:
        pts = sorted(by_site.get(st["id"]) or [], key=lambda p: p[0])
        if len(pts) < 8:
            continue
        recent = [q for t, q in pts if t >= issued - half]
        prior = [q for t, q in pts if issued - 2 * half <= t < issued - half]
        if not recent or not prior:
            continue
        out.append(
            {
                **st,
                "q_recent": sum(recent) / len(recent),
                "q_prior": sum(prior) / len(prior),
                "n_recent": len(recent),
                "n_prior": len(prior),
            }
        )
    return out


def _issue_path(issued: datetime) -> Path:
    """Never overwrite a frozen dated issue. Timestamp if today's file exists."""
    day = OUT_DIR / f"{issued.strftime('%Y-%m-%d')}_issue.json"
    if day.exists():
        return OUT_DIR / f"{issued.strftime('%Y-%m-%dT%H%M%S')}_issue.json"
    return day


def main() -> int:
    issued = datetime.now(timezone.utc).replace(microsecond=0)
    quakes = fetch_usgs()
    volc_events = fetch_usgs(days=30, minmag=3.0, eventtype="volcanic eruption")
    kp = fetch_swpc_kp()
    buoys = fetch_ndbc()
    tides = fetch_tide_snapshots(issued)
    hydro_snap = fetch_nwis_snapshots(issued)
    eq = earthquake_forecasts(quakes, issued=issued)
    wx = weather_forecasts(buoys, issued=issued)
    sol = solar_forecasts(kp, issued=issued)
    volc_pool = {str(e.get("id") or i): e for i, e in enumerate(quakes + volc_events)}
    volc = volcanic_forecasts(list(volc_pool.values()), issued=issued)
    tide = tide_forecasts(tides, issued=issued)
    hydro = hydrology_forecasts(hydro_snap, issued=issued)
    all_f = eq + wx + sol + volc + tide + hydro
    doc = {
        "schema_version": "1.1",
        "pin": "D1D38A",
        "issued_at": issued.isoformat(),
        "horizon_days_eq": forecast_horizon_days(),
        "kernel_km": kernel_km(),
        "policy": [
            "windowed_spatial_class_not_a_clock_time",
            "pressure_loads_then_POOF",
            "score_in_results_do_not_rewrite_this_issue",
            "never_overwrite_existing_dated_issue",
        ],
        "catalogs": {
            "usgs_n": len(quakes),
            "usgs_volcanic_n": len(volc_events),
            "ndbc_n": len(buoys),
            "swpc_kp_n": len(kp),
            "coops_n": len(tides),
            "nwis_n": len(hydro_snap),
        },
        "forecasts": all_f,
        "n_eq": len(eq),
        "n_wx": len(wx),
        "n_sol": len(sol),
        "n_volc": len(volc),
        "n_tide": len(tide),
        "n_hydro": len(hydro),
        "score_command": "python scripts/score_earth_fluid_forecasts.py",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    day = _issue_path(issued)
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
        f"USGS events used: **{len(quakes)}**. Volcanic-type: **{len(volc_events)}**. "
        f"NDBC stations: **{len(buoys)}**. SWPC Kp samples: **{len(kp)}**. "
        f"CO-OPS stations: **{len(tides)}**. NWIS gages: **{len(hydro_snap)}**.",
        "",
        "Prior frozen issues stay on disk (do not rewrite). This file is the current issue.",
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
            call = f"{pred.get('class')} / {pred.get('basin')}"
        elif fc["kind"] == "tide":
            call = (
                f"surge ≥{pred.get('surge_threshold_m')} m"
                if pred.get("expect_surge")
                else f"residual <{pred.get('surge_threshold_m')} m"
            )
        elif fc["kind"] == "hydrology":
            call = (
                "high_flow"
                if pred.get("expect_high_flow")
                else "quiet_flow"
            )
        lines.append(
            f"| `{fc['id']}` | {fc['kind']} | {loc.get('name')} "
            f"({loc.get('lat')},{loc.get('lon')}) r={loc.get('radius_km')} km | "
            f"{fc['valid_from'][:10]} → {fc['valid_to'][:10]} | {call} | "
            f"{pred.get('valve_state')} |"
        )
    frozen = sorted(p.name for p in OUT_DIR.glob("*_issue.json"))
    lines += [
        "",
        f"This issue JSON: `{day.relative_to(ROOT).as_posix()}`",
        "Pointer: `predictions/dated_forecasts/LATEST.json`",
        "",
        "Frozen issue files (never rewrite): " + ", ".join(f"`{n}`" for n in frozen),
        "",
        "These are **not** USGS/NWS watches. They are FSOT valve cells so we can iron out hit/miss.",
        "",
        "Scores: `results/dated_forecast_scores/REPORT.md` (never rewrite this issue JSON).",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {day}")
    print(f"Wrote {latest}")
    print(f"Wrote {md}")
    print(
        f"  eq={len(eq)} wx={len(wx)} sol={len(sol)} volc={len(volc)} "
        f"tide={len(tide)} hydro={len(hydro)}"
    )
    for fc in eq[:8]:
        print(
            f"  {fc['id']}: {fc['location']['name'][:50]}  "
            f"M>={fc['predicted']['mag_min']} expect={fc['predicted']['expect_event']}  "
            f"{fc['predicted']['valve_state']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
