"""VizieR WDS catalog fetch — shared by tier62 and tier68 ingests.

CDS TAP endpoint and column names corrected 2026-08 (was TAPVizierTap 404;
ADQL used Sep/RAdeg which are not B/wds/wds columns — use sep1, RAJ2000, DEJ2000).
"""

from __future__ import annotations

import re
import urllib.parse
import xml.etree.ElementTree as ET

from live_api_fetch_lib import fetch_bytes, fetch_json, post_json

# Official CDS VizieR TAP (case-sensitive path).
VIZIER_TAP_ENDPOINTS = (
    "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync",
    "https://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync",
)
VIZIER_VOTABLE = "https://vizier.cds.unistra.fr/viz-bin/votable"


def wds_adql(top: int) -> str:
    # Columns verified live against B/wds/wds metadata (2026-08).
    return (
        f"SELECT TOP {int(top)} WDS, sep1, sep2, mag1, mag2, Comp, RAJ2000, DEJ2000 "
        'FROM "B/wds/wds" WHERE sep1 IS NOT NULL AND sep1 > 0 ORDER BY sep1'
    )


def _parse_rows(payload: object) -> list[dict]:
    """Normalize TAP JSON to list of dict rows."""
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if not isinstance(payload, dict):
        return []
    # CDS TAP often returns {"metadata":[...], "data":[[...], ...]}
    meta = payload.get("metadata")
    data = payload.get("data")
    if isinstance(meta, list) and isinstance(data, list) and data:
        names = [m.get("name") for m in meta if isinstance(m, dict)]
        if names and isinstance(data[0], (list, tuple)):
            out: list[dict] = []
            for row in data:
                if not isinstance(row, (list, tuple)):
                    continue
                out.append({names[i]: row[i] for i in range(min(len(names), len(row)))})
            return out
    for key in ("data", "rows", "result"):
        block = payload.get(key)
        if isinstance(block, list) and block and isinstance(block[0], dict):
            return [r for r in block if isinstance(r, dict)]
    return []


def _row_to_system(row: dict) -> dict | None:
    sid = row.get("WDS") or row.get("wds")
    if not sid:
        return None
    sep = row.get("sep1") or row.get("Sep") or row.get("sep") or row.get("sep2")
    return {
        "id": str(sid).strip(),
        "separation_arcsec": float(sep) if sep is not None else None,
        "mag1": row.get("mag1") or row.get("MAG1"),
        "mag2": row.get("mag2") or row.get("MAG2"),
        "multiplicity": row.get("Comp") or row.get("comp") or row.get("COMP"),
        "ra_deg": row.get("RAJ2000") or row.get("RAdeg"),
        "dec_deg": row.get("DEJ2000") or row.get("DEdeg"),
        "source": "vizier_wds_tap_live",
    }


def _parse_votable_systems(xml_bytes: bytes, *, top: int) -> list[dict]:
    """Minimal VOTable tabledata parser for B/wds fallback."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    # Handle default namespaces by ignoring them in tag match.
    def local(tag: str) -> str:
        return tag.split("}")[-1] if "}" in tag else tag

    fields: list[str] = []
    systems: list[dict] = []
    for el in root.iter():
        if local(el.tag) == "FIELD":
            name = el.attrib.get("name") or el.attrib.get("ID") or ""
            fields.append(name)
        elif local(el.tag) == "TR":
            cells = [ (c.text or "").strip() for c in el if local(c.tag) == "TD" ]
            if not fields or not cells:
                continue
            row = {fields[i]: cells[i] for i in range(min(len(fields), len(cells)))}
            sys = _row_to_system(row)
            if sys and sys.get("separation_arcsec") is not None:
                systems.append(sys)
            if len(systems) >= top:
                break
    return systems


def fetch_wds_systems(*, top: int = 120) -> tuple[list[dict], str]:
    """Return (systems, source_tag). Raises on total failure."""
    adql = wds_adql(top)
    errors: list[str] = []
    tap_params = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
    )
    tap_body = {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}

    attempts: list[tuple[str, object]] = []
    for base in VIZIER_TAP_ENDPOINTS:
        attempts.append(
            (
                f"vizier_tap_get:{base}",
                lambda b=base: fetch_json(f"{b}?{tap_params}", timeout=120, retries=3, backoff_s=2.0),
            )
        )
        attempts.append(
            (
                f"vizier_tap_post:{base}",
                lambda b=base: post_json(b, tap_body, timeout=120, retries=3, backoff_s=2.0),
            )
        )

    for endpoint, fetcher in attempts:
        try:
            rows = _parse_rows(fetcher())
            systems: list[dict] = []
            for row in rows:
                sys = _row_to_system(row)
                if sys is not None:
                    systems.append(sys)
                if len(systems) >= top:
                    break
            if systems:
                return systems, endpoint
            errors.append(f"{endpoint}: empty rows")
        except Exception as exc:
            errors.append(f"{endpoint}: {exc}")

    # VOTable fallback (often works when TAP query shape is finicky).
    try:
        q = urllib.parse.urlencode(
            {
                "-source": "B/wds",
                "-out.max": str(int(top)),
                "-out": "WDS,sep1,mag1,mag2,Comp,RAJ2000,DEJ2000",
            }
        )
        raw = fetch_bytes(f"{VIZIER_VOTABLE}?{q}", timeout=120, retries=3)
        systems = _parse_votable_systems(raw, top=top)
        if systems:
            return systems, "vizier_votable"
        # Some servers ignore -out; parse whatever tabledata we got.
        systems = _parse_votable_systems(raw, top=top)
        if systems:
            return systems, "vizier_votable_raw"
        errors.append("vizier_votable: empty parse")
    except Exception as exc:
        errors.append(f"vizier_votable: {exc}")

    raise RuntimeError("; ".join(errors[-5:]))
