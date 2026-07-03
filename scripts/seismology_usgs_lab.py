"""USGS FDSN earthquake catalog helpers."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


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
                "depth_km": coords[2],
                "lon": coords[0],
                "lat": coords[1],
                "place": props.get("place"),
                "time": props.get("time"),
            }
        )
    return rows