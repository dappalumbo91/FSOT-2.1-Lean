"""USGS FDSN earthquake catalog helpers."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

MOMENT_MAG_TYPES = frozenset({"mww", "mw", "mwb", "mwr", "mwc"})


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    import math

    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def min_plate_boundary_distance_km(lon: float, lat: float, plate_features: list[dict]) -> float:
    best = float("inf")
    for feat in plate_features:
        geom = feat.get("geometry") or {}
        for coord in geom.get("coordinates") or []:
            if not coord or len(coord) < 2:
                continue
            d = haversine_km(lon, lat, float(coord[0]), float(coord[1]))
            if d < best:
                best = d
    return best


def fetch_earthquakes(
    *,
    starttime: str,
    endtime: str,
    minmagnitude: float,
    limit: int,
) -> list[dict[str, Any]]:
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": minmagnitude,
        "limit": limit,
    }
    url = USGS_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/seismology"})
    doc = json.loads(urllib.request.urlopen(req, timeout=60).read())
    rows: list[dict[str, Any]] = []
    for feat in doc.get("features") or []:
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None, None]
        rows.append(
            {
                "id": feat.get("id"),
                "mag": props.get("mag"),
                "mag_type": props.get("magType"),
                "mmi": props.get("mmi"),
                "cdi": props.get("cdi"),
                "gap": props.get("gap"),
                "rms": props.get("rms"),
                "net": props.get("net"),
                "depth_km": coords[2],
                "lon": coords[0],
                "lat": coords[1],
                "place": props.get("place"),
                "time": props.get("time"),
            }
        )
    return rows