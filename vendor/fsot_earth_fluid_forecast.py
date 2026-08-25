#!/usr/bin/env python3
"""Dated, located fluid-pressure forecasts for Earth systems.

Earthquakes, storms, flares, and eruptions are the same valve as C2/C10:
pressure loads (SUCTION / infall) then the orifice opens (POOF / release).
We do not invent a city and a clock time. We take the live catalog, find
where the pressure cell *is*, and freeze a calendar window + radius so the
next USGS / NDBC / SWPC pull can score hit or miss.

Kernel length (km) = R_earth · POOF / 25
  — compactification: crustal orifice scale is Earth radius × valve / ceiling.

Forecast horizon (days) = φ^4 ≈ 6.85 → 7 day earthquake window.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

try:
    from fsot_compute import PHI, POOF, SUCTION, domain_scalar  # type: ignore
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path as _P

    sys.path.insert(0, str(_P(__file__).resolve().parent))
    from fsot_compute import PHI, POOF, SUCTION, domain_scalar

R_EARTH_KM = 6371.0


def f(x: Any) -> float:
    return float(x)


def kernel_km() -> float:
    return R_EARTH_KM * f(POOF) / 25.0


def forecast_horizon_days() -> int:
    return max(1, int(round(f(PHI) ** 4)))


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(min(1.0, math.sqrt(a)))


def event_weight(mag: float) -> float:
    """Moment-like weight: 10^(M − 4.5). Seed-free relative counting."""
    return 10.0 ** (float(mag) - 4.5)


def cell_pressure(center: dict[str, float], events: list[dict[str, Any]]) -> float:
    """Catalog-normalized kernel density. Uniform → ~0 relative; cluster → high."""
    k = kernel_km()
    acc = 0.0
    for ev in events:
        d = haversine_km(center["lat"], center["lon"], float(ev["lat"]), float(ev["lon"]))
        acc += event_weight(float(ev["mag"])) / (1.0 + d / k)
    n = max(len(events), 1)
    mean = acc / n
    return acc / (1.0 + mean)  # bounded, still ranks clusters


def valve_state(events: list[dict[str, Any]], *, now_ms: int, half_ms: int) -> str:
    """Loading (SUCTION) vs release (POOF) from the recent rate in the cell."""
    recent = [e for e in events if int(e["time"]) >= now_ms - half_ms]
    prior = [e for e in events if now_ms - 2 * half_ms <= int(e["time"]) < now_ms - half_ms]
    wr = sum(event_weight(float(e["mag"])) for e in recent)
    wp = sum(event_weight(float(e["mag"])) for e in prior)
    big = any(float(e["mag"]) >= 5.5 for e in recent)
    if wr > wp * 1.15:
        return "loading_suction"
    if big and wr <= wp:
        return "post_poof_aftershock"
    if wr < wp * 0.7:
        return "released"
    return "steady"


def cluster_cells(events: list[dict[str, Any]], *, top_n: int = 8) -> list[dict[str, Any]]:
    """Greedy non-overlapping pressure cells around the heaviest events."""
    k = kernel_km()
    ranked = sorted(events, key=lambda e: -float(e["mag"]))
    cells: list[dict[str, Any]] = []
    used: list[dict[str, float]] = []
    for ev in ranked:
        lat, lon = float(ev["lat"]), float(ev["lon"])
        if any(haversine_km(lat, lon, u["lat"], u["lon"]) < 2.0 * k for u in used):
            continue
        members = [
            e
            for e in events
            if haversine_km(lat, lon, float(e["lat"]), float(e["lon"])) <= k
        ]
        if len(members) < 2 and float(ev["mag"]) < 5.5:
            continue
        wlat = sum(float(e["lat"]) * event_weight(float(e["mag"])) for e in members)
        wlon = sum(float(e["lon"]) * event_weight(float(e["mag"])) for e in members)
        wsum = sum(event_weight(float(e["mag"])) for e in members) or 1.0
        center = {"lat": wlat / wsum, "lon": wlon / wsum}
        used.append(center)
        cells.append(
            {
                "lat": center["lat"],
                "lon": center["lon"],
                "n": len(members),
                "max_mag": max(float(e["mag"]) for e in members),
                "place": str(ev.get("place") or "unnamed"),
                "members": members,
                "pressure": cell_pressure(center, events),
            }
        )
        if len(cells) >= top_n:
            break
    cells.sort(key=lambda c: -float(c["pressure"]))
    return cells


def earthquake_forecasts(
    events: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    days = forecast_horizon_days()
    half_ms = int(days * 0.5 * 86400 * 1000)
    now_ms = int(issued.timestamp() * 1000)
    valid_from = issued
    valid_to = issued + timedelta(days=days)
    s_seis = abs(f(domain_scalar("Seismology")))
    out: list[dict[str, Any]] = []
    for i, cell in enumerate(cluster_cells(events), start=1):
        state = valve_state(cell["members"], now_ms=now_ms, half_ms=half_ms)
        mag_min = 5.0 if float(cell["max_mag"]) >= 6.0 else 4.5
        # Loading cells: expect a release. Post-POOF: aftershocks. Released: still a residual cell.
        expect = True
        if state == "released" and float(cell["max_mag"]) < 5.5:
            expect = False
        fid = f"FCAST-EQ-{issued.strftime('%Y%m%d')}-{i:02d}"
        out.append(
            {
                "id": fid,
                "kind": "earthquake",
                "issued_at": issued.isoformat(),
                "valid_from": valid_from.isoformat(),
                "valid_to": valid_to.isoformat(),
                "location": {
                    "name": cell["place"],
                    "lat": round(float(cell["lat"]), 4),
                    "lon": round(float(cell["lon"]), 4),
                    "radius_km": round(kernel_km(), 1),
                },
                "predicted": {
                    "class": "M_ge_threshold_in_window",
                    "mag_min": mag_min,
                    "min_count": 1 if expect else 0,
                    "expect_event": expect,
                    "valve_state": state,
                    "fsot_pressure": round(float(cell["pressure"]), 4),
                    "n_recent": int(cell["n"]),
                    "max_mag_recent": float(cell["max_mag"]),
                    "S_seismology": round(s_seis, 6),
                    "poof": f(POOF),
                    "suction": f(SUCTION),
                },
                "kill_if": (
                    f"{'No' if expect else 'An'} USGS M≥{mag_min} inside "
                    f"{kernel_km():.0f} km of ({cell['lat']:.3f},{cell['lon']:.3f}) "
                    f"between {valid_from.date()} and {valid_to.date()}"
                ),
                "score_query": {
                    "lat": cell["lat"],
                    "lon": cell["lon"],
                    "radius_km": kernel_km(),
                    "mag_min": mag_min,
                    "start": valid_from.strftime("%Y-%m-%d"),
                    "end": valid_to.strftime("%Y-%m-%d"),
                },
            }
        )
    return out


def weather_forecasts(
    buoys: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """Storm-sector marine cells: lowest pressure / highest gust = loaded valve."""
    valid_to = issued + timedelta(hours=48)
    ranked = []
    for b in buoys:
        try:
            pres = float(b.get("pres") or 0)
            gst = float(b.get("gst") or b.get("wspd") or 0)
        except (TypeError, ValueError):
            continue
        if pres <= 0:
            continue
        ranked.append((pres - 0.4 * gst, b, pres, gst))
    ranked.sort(key=lambda t: t[0])
    out: list[dict[str, Any]] = []
    for i, (_score, b, pres, gst) in enumerate(ranked[:5], start=1):
        storm = pres < 1000.0 or gst >= 15.0
        fid = f"FCAST-WX-{issued.strftime('%Y%m%d')}-{i:02d}"
        lat = float(b.get("lat") or 0)
        lon = float(b.get("lon") or 0)
        bid = str(b.get("buoy_id") or b.get("station") or f"buoy{i}")
        out.append(
            {
                "id": fid,
                "kind": "weather",
                "issued_at": issued.isoformat(),
                "valid_from": issued.isoformat(),
                "valid_to": valid_to.isoformat(),
                "location": {
                    "name": f"NDBC {bid}",
                    "lat": lat,
                    "lon": lon,
                    "radius_km": 50.0,
                    "buoy_id": bid,
                },
                "predicted": {
                    "class": "storm_sector" if storm else "quiet_sector",
                    "pres_max_hpa": 1010.0 if storm else 1035.0,
                    "gst_min_ms": 8.0 if storm else 0.0,
                    "valve_state": "loading_suction" if storm else "steady",
                    "pres_now": pres,
                    "gst_now": gst,
                },
                "kill_if": (
                    f"NDBC {bid} next 48h: "
                    + (
                        "pressure stays ≥1010 hPa AND gust <8 m/s"
                        if storm
                        else "pressure drops below 1005 hPa or gust ≥12 m/s"
                    )
                ),
                "score_query": {"buoy_id": bid, "storm": storm},
            }
        )
    return out


def solar_forecasts(
    kp_series: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """Quiet vs storm sector for the next 72 h from the recent Kp trend."""
    valid_to = issued + timedelta(hours=72)
    vals = []
    for row in kp_series[-24:]:
        try:
            vals.append(float(row.get("kp_index") or row.get("kp") or 0))
        except (TypeError, ValueError):
            continue
    if not vals:
        return []
    latest = vals[-1]
    rising = len(vals) >= 4 and vals[-1] > vals[-4]
    storm = latest >= 4.0 or (rising and latest >= 3.0)
    fid = f"FCAST-SOL-{issued.strftime('%Y%m%d')}-01"
    return [
        {
            "id": fid,
            "kind": "solar",
            "issued_at": issued.isoformat(),
            "valid_from": issued.isoformat(),
            "valid_to": valid_to.isoformat(),
            "location": {
                "name": "Earth magnetosphere (planetary Kp)",
                "lat": 0.0,
                "lon": 0.0,
                "radius_km": R_EARTH_KM,
            },
            "predicted": {
                "class": "storm_sector" if storm else "quiet_sector",
                "kp_threshold": 5.0 if storm else 5.0,
                "expect_kp_ge_5": storm,
                "kp_now": latest,
                "valve_state": "loading_suction" if rising else "steady",
            },
            "kill_if": (
                "NOAA SWPC planetary Kp does "
                + ("NOT reach 5" if storm else "reach 5 or above")
                + " in the next 72 hours"
            ),
            "score_query": {"expect_kp_ge_5": storm},
        }
    ]


def volcanic_forecasts(
    events: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """Volcanic-type USGS events are POOF cells; 14-day continuation window."""
    volc = [
        e
        for e in events
        if "volcan" in str(e.get("place") or "").lower()
        or str(e.get("type") or "").lower() in {"volcanic eruption", "explosion"}
    ]
    if not volc:
        return []
    days = forecast_horizon_days() * 2
    valid_to = issued + timedelta(days=days)
    out: list[dict[str, Any]] = []
    for i, cell in enumerate(cluster_cells(volc, top_n=4), start=1):
        fid = f"FCAST-VOLC-{issued.strftime('%Y%m%d')}-{i:02d}"
        out.append(
            {
                "id": fid,
                "kind": "volcanic",
                "issued_at": issued.isoformat(),
                "valid_from": issued.isoformat(),
                "valid_to": valid_to.isoformat(),
                "location": {
                    "name": cell["place"],
                    "lat": round(float(cell["lat"]), 4),
                    "lon": round(float(cell["lon"]), 4),
                    "radius_km": round(kernel_km(), 1),
                },
                "predicted": {
                    "class": "volcanic_or_explosion_in_window",
                    "mag_min": 4.0,
                    "min_count": 1,
                    "expect_event": True,
                    "valve_state": "loading_suction",
                    "fsot_pressure": round(float(cell["pressure"]), 4),
                },
                "kill_if": (
                    f"No USGS volcanic/explosion or M≥4 within {kernel_km():.0f} km "
                    f"of {cell['place']} by {valid_to.date()}"
                ),
                "score_query": {
                    "lat": cell["lat"],
                    "lon": cell["lon"],
                    "radius_km": kernel_km(),
                    "mag_min": 4.0,
                    "start": issued.strftime("%Y-%m-%d"),
                    "end": valid_to.strftime("%Y-%m-%d"),
                    "volcanic": True,
                },
            }
        )
    return out
