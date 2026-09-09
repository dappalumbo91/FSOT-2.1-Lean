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
    """Crustal cell: one compactified slice of Earth's orifice."""
    return R_EARTH_KM * f(POOF) / 25.0


def cycle_km() -> float:
    """Planetary-cycle coupling: the same orifice without the 25-D fold.

    Solar, volcanic arc, trench, and basin tanks talk at R⊕·POOF, not at
    the 39 km cell. Not a new coefficient — compactification denominator
    off. Issued kill_if stays on kernel_km.
    """
    return R_EARTH_KM * f(POOF)


def forecast_horizon_days() -> int:
    return max(1, int(round(f(PHI) ** 4)))


def omori_p() -> float:
    """Aftershock productivity slope. Same unity as Gutenberg–Richter b = φ − 1/φ."""
    return 1.0


def omori_c_days() -> float:
    """Characteristic delay after POOF. 1/φ days — timing handle for always-on scoring."""
    return 1.0 / f(PHI)


def omori_rate(t_days_since_poof: float) -> float:
    """n(t) ∝ 1 / (t + c)^p. Relative rate, not a fitted aftershock model."""
    return 1.0 / (max(t_days_since_poof, 0.0) + omori_c_days()) ** omori_p()


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
        # Loading cells: continuation class is M>=4.5 (Timor 4.8 at 3.4 km missed a 5.0 bar).
        # Released/steady: only an M>=5 breaks a quiet hold.
        expect = state in {"loading_suction", "post_poof_aftershock"}
        mag_min = 4.5 if expect else 5.0
        fid = f"FCAST-EQ-{issued.strftime('%Y%m%dT%H%M')}-{i:02d}"
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
                    "refine_note": "M>=threshold only on loading/post_poof; released/steady hold if quiet",
                    "S_seismology": round(s_seis, 6),
                    "poof": f(POOF),
                    "suction": f(SUCTION),
                    "omori_p": omori_p(),
                    "omori_c_days": omori_c_days(),
                    "timing_note": "after POOF, relative aftershock rate ~ 1/(t+1/φ)^1",
                    "cycle_radius_km": round(cycle_km(), 1),
                    "neighbor_kinds": ["volcanic", "solar", "earthquake"],
                    "cycle_note": (
                        "Cell is R⊕·POOF/25. If the cell is quiet, look for POOF "
                        "in the planetary cycle (R⊕·POOF) — arc/trench/solar tanks. "
                        "Does not rewrite kill_if."
                    ),
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


def marine_basin(lat: float, lon: float) -> str:
    """Ocean-air tanks by geography so storm cells are not all one pole."""
    if lat >= 60.0:
        return "arctic"
    if lat <= -40.0:
        return "southern"
    if 18.0 <= lat <= 32.0 and -98.0 <= lon <= -80.0:
        return "gulf"
    if abs(lat) < 20.0:
        return "tropics"
    if lon <= -100.0 or lon >= 120.0:
        return "pacific"
    if -80.0 <= lon <= 40.0:
        return "atlantic"
    return "other"


def weather_forecasts(
    buoys: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """Storm-sector marine cells, one loaded cell per ocean basin (not Arctic-only)."""
    valid_to = issued + timedelta(hours=48)
    ranked: list[tuple[float, dict[str, Any], float, float, str]] = []
    for b in buoys:
        try:
            pres = float(b.get("pres") or 0)
            gst = float(b.get("gst") or b.get("wspd") or 0)
            lat = float(b.get("lat") or 0)
            lon = float(b.get("lon") or 0)
        except (TypeError, ValueError):
            continue
        if pres <= 0:
            continue
        ranked.append((pres - 0.4 * gst, b, pres, gst, marine_basin(lat, lon)))
    ranked.sort(key=lambda t: t[0])
    picked: list[tuple[float, dict[str, Any], float, float, str]] = []
    used_basins: set[str] = set()

    def _storm(pres: float, gst: float) -> bool:
        return pres < 1000.0 or gst >= 15.0

    def _quiet_clean(pres: float, gst: float) -> bool:
        # Inside the quiet kill envelope (pres≥1010 and gst<8), not the 1000–1005 / 12–15 gap.
        return pres >= 1010.0 and gst < 8.0

    for row in ranked:
        if row[4] == "other":
            continue
        if not _storm(row[2], row[3]):
            continue
        if row[4] in used_basins:
            continue
        used_basins.add(row[4])
        picked.append(row)
        if len(picked) >= 6:
            break
    if len(picked) < 6:
        for row in ranked:
            if row in picked or row[4] == "other":
                continue
            if row[4] in used_basins:
                continue
            if not _quiet_clean(row[2], row[3]):
                continue
            used_basins.add(row[4])
            picked.append(row)
            if len(picked) >= 6:
                break
    out: list[dict[str, Any]] = []
    for i, (_score, b, pres, gst, basin) in enumerate(picked, start=1):
        storm = pres < 1000.0 or gst >= 15.0
        fid = f"FCAST-WX-{issued.strftime('%Y%m%dT%H%M')}-{i:02d}"
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
                    "name": f"NDBC {bid} ({basin})",
                    "lat": lat,
                    "lon": lon,
                    "radius_km": 50.0,
                    "buoy_id": bid,
                    "basin": basin,
                },
                "predicted": {
                    "class": "storm_sector" if storm else "quiet_sector",
                    "pres_max_hpa": 1010.0 if storm else 1035.0,
                    "gst_min_ms": 8.0 if storm else 0.0,
                    "valve_state": "loading_suction" if storm else "steady",
                    "pres_now": pres,
                    "gst_now": gst,
                    "basin": basin,
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
    fid = f"FCAST-SOL-{issued.strftime('%Y%m%dT%H%M')}-01"
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
        fid = f"FCAST-VOLC-{issued.strftime('%Y%m%dT%H%M')}-{i:02d}"
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
                    "cycle_radius_km": round(cycle_km(), 1),
                    "neighbor_kinds": ["earthquake", "solar", "volcanic"],
                    "cycle_note": (
                        "Volcanic arc is one tank with the trench. Cell kill_if "
                        "stays 39 km; cycle POOF is R⊕·POOF (~978 km) plus Kp."
                    ),
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


# NOAA CO-OPS stations already residual-gated in noaa_coastal_tides_benchmark.json
TIDE_STATIONS: list[dict[str, Any]] = [
    {"id": "9414290", "name": "San Francisco", "lat": 37.8063, "lon": -122.4659},
    {"id": "8443970", "name": "Boston", "lat": 42.3534, "lon": -71.0534},
    {"id": "8724580", "name": "Key West", "lat": 24.5508, "lon": -81.8081},
    {"id": "9447130", "name": "Seattle", "lat": 47.6026, "lon": -122.3393},
    {"id": "8638610", "name": "Sewells Point", "lat": 36.9467, "lon": -76.3300},
    {"id": "8518750", "name": "The Battery NY", "lat": 40.7006, "lon": -74.0142},
    {"id": "9410170", "name": "Los Angeles", "lat": 33.7200, "lon": -118.2722},
    {"id": "8771341", "name": "Galveston", "lat": 29.3100, "lon": -94.7933},
]


def surge_class_m() -> float:
    """Surge residual class in metres = POOF. Seed-closed; not a fitted β."""
    return f(POOF)


def surge_issue_m() -> float:
    """Issue a surge cell only if residual is clearly above POOF.

    Bar = POOF·(1+POOF) — same 1+POOF grammar as hydrology load.
    Scoring / kill bar stays surge_class_m() = POOF.
    Closes the San Francisco 8.5 mm miss: snapshot 0.157 m was only
    3.5 mm over POOF and the window dropped to 0.145 m.
    """
    p = f(POOF)
    return p * (1.0 + p)


def tide_forecasts(
    snapshots: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """48 h high-water *surge* class at CO-OPS stations.

    Harmonic high water always happens. The valve is the residual
    (observed − predicted). Issue surge only if residual now ≥ POOF·(1+POOF).
    Gap zone [POOF, issue bar) is not labeled surge or harmonic.
    """
    valid_to = issued + timedelta(hours=48)
    score_thr = surge_class_m()
    issue_thr = surge_issue_m()
    loaded = [s for s in snapshots if float(s.get("residual_m") or 0) >= issue_thr]
    quiet = [s for s in snapshots if float(s.get("residual_m") or 0) < score_thr]
    picked = loaded[:6]
    if len(picked) < 4:
        for s in quiet:
            picked.append(s)
            if len(picked) >= 4:
                break
    out: list[dict[str, Any]] = []
    for i, st in enumerate(picked, start=1):
        resid = float(st.get("residual_m") or 0)
        storm = resid >= issue_thr
        sid = str(st["id"])
        fid = f"FCAST-TIDE-{issued.strftime('%Y%m%dT%H%M')}-{i:02d}"
        out.append(
            {
                "id": fid,
                "kind": "tide",
                "issued_at": issued.isoformat(),
                "valid_from": issued.isoformat(),
                "valid_to": valid_to.isoformat(),
                "location": {
                    "name": f"NOAA {st.get('name')} ({sid})",
                    "lat": float(st["lat"]),
                    "lon": float(st["lon"]),
                    "radius_km": 39.1,
                    "station_id": sid,
                },
                "predicted": {
                    "class": "surge_sector" if storm else "harmonic_sector",
                    "surge_threshold_m": round(score_thr, 4),
                    "surge_issue_threshold_m": round(issue_thr, 4),
                    "residual_now_m": round(resid, 4),
                    "obs_now_m": st.get("obs_m"),
                    "pred_now_m": st.get("pred_m"),
                    "expect_surge": storm,
                    "valve_state": "loading_suction" if storm else "steady",
                },
                "kill_if": (
                    f"CO-OPS {sid} next 48h: max(obs−pred) "
                    + (f"< {score_thr:.3f} m" if storm else f"≥ {score_thr:.3f} m")
                ),
                "score_query": {
                    "station_id": sid,
                    "expect_surge": storm,
                    "surge_threshold_m": score_thr,
                    "start": issued.strftime("%Y-%m-%d"),
                    "end": valid_to.strftime("%Y-%m-%d"),
                },
            }
        )
    return out


# USGS NWIS reference gages from data/hydrology_usgs_manifest.yaml
# Dated-forecast gages. IDs verified 2026-09-07 against NWIS site service
# (names+coords were already right; several IDs had pointed at other rivers).
# 06803510 is Little Salt Creek near Lincoln NE, not Hermann — that ID
# stays frozen on issued JSON. Manifest/benchmark IDs are a separate ingest.
HYDRO_STATIONS: list[dict[str, Any]] = [
    {"id": "01646500", "name": "Potomac River near Washington DC", "lat": 38.95, "lon": -77.13},
    {"id": "05464500", "name": "Cedar River at Cedar Rapids IA", "lat": 41.97, "lon": -91.67},
    {"id": "08114000", "name": "Brazos River at Richmond TX", "lat": 29.58, "lon": -95.76},
    {"id": "09380000", "name": "Colorado River at Lees Ferry AZ", "lat": 36.86, "lon": -111.59},
    {"id": "06934500", "name": "Missouri River at Hermann MO", "lat": 38.71, "lon": -91.43},
    {"id": "14144700", "name": "Columbia River at Vancouver WA", "lat": 45.62, "lon": -122.67},
    {"id": "023177483", "name": "Withlacoochee River at Skipper Bridge GA", "lat": 30.85, "lon": -83.28},
    {"id": "03072655", "name": "Monongahela River near Masontown PA", "lat": 39.84, "lon": -79.88},
]


def hydrology_load_bar() -> float:
    """Recent/prior discharge ratio that counts as loading. Seed-closed: 1+POOF."""
    return 1.0 + f(POOF)


def hydrology_forecasts(
    snapshots: list[dict[str, Any]],
    *,
    issued: datetime,
) -> list[dict[str, Any]]:
    """7-day flood/quiet class windows at NWIS gages. Same valve as EQ cells."""
    days = forecast_horizon_days()
    valid_to = issued + timedelta(days=days)
    bar = hydrology_load_bar()
    out: list[dict[str, Any]] = []
    for i, st in enumerate(snapshots, start=1):
        q_recent = float(st.get("q_recent") or 0)
        q_prior = float(st.get("q_prior") or 0)
        if q_recent <= 0 or q_prior <= 0:
            continue
        ratio = q_recent / q_prior
        loading = ratio >= bar
        released = ratio <= 1.0 / bar
        if loading:
            state = "loading_suction"
        elif released:
            state = "released"
        else:
            state = "steady"
        expect_high = loading
        fid = f"FCAST-HYDRO-{issued.strftime('%Y%m%dT%H%M')}-{i:02d}"
        sid = str(st["id"])
        out.append(
            {
                "id": fid,
                "kind": "hydrology",
                "issued_at": issued.isoformat(),
                "valid_from": issued.isoformat(),
                "valid_to": valid_to.isoformat(),
                "location": {
                    "name": f"USGS {sid} {st.get('name')}",
                    "lat": float(st["lat"]),
                    "lon": float(st["lon"]),
                    "radius_km": round(kernel_km(), 1),
                    "site_id": sid,
                },
                "predicted": {
                    "class": "high_flow_sector" if expect_high else "quiet_flow_sector",
                    "expect_high_flow": expect_high,
                    "q_recent_cfs": round(q_recent, 2),
                    "q_prior_cfs": round(q_prior, 2),
                    "load_ratio": round(ratio, 4),
                    "load_bar": round(bar, 4),
                    "valve_state": state,
                },
                "kill_if": (
                    f"USGS {sid} next {days}d mean discharge "
                    + (
                        f"falls below prior {q_prior:.0f} cfs"
                        if expect_high
                        else f"rises to ≥ {q_prior * bar:.0f} cfs"
                    )
                ),
                "score_query": {
                    "site_id": sid,
                    "expect_high_flow": expect_high,
                    "q_prior_cfs": q_prior,
                    "load_bar": bar,
                    "start": issued.strftime("%Y-%m-%d"),
                    "end": valid_to.strftime("%Y-%m-%d"),
                },
            }
        )
    return out
