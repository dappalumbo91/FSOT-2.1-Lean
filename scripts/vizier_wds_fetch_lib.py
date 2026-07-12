"""VizieR WDS catalog fetch — shared by tier62 and tier68 ingests."""

from __future__ import annotations

import urllib.parse

from live_api_fetch_lib import fetch_json, post_json

VIZIER_TAP = "https://tapvizier.cds.unistra.fr/TAPVizierTap/sync"
VIZIER_VOTABLE = "https://cdsarc.cds.unistra.fr/viz-bin/votable"


def wds_adql(top: int) -> str:
    return (
        f"SELECT TOP {top} WDS, RAdeg, DEdeg, Sep, mag1, mag2, comp "
        'FROM "II/213/wds" WHERE Sep IS NOT NULL ORDER BY Sep'
    )


def _parse_rows(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        for key in ("data", "rows", "result"):
            data = payload.get(key)
            if isinstance(data, list):
                return [r for r in data if isinstance(r, dict)]
    return []


def fetch_wds_systems(*, top: int = 120) -> tuple[list[dict], str]:
    """Return (systems, source_tag). Raises on total failure."""
    adql = wds_adql(top)
    errors: list[str] = []
    tap_params = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
    )
    tap_body = {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
    attempts: list[tuple[str, object]] = [
        ("vizier_tap_get", lambda: fetch_json(f"{VIZIER_TAP}?{tap_params}", timeout=120, retries=5, backoff_s=3.0)),
        ("vizier_tap_post", lambda: post_json(VIZIER_TAP, tap_body, timeout=120, retries=5, backoff_s=3.0)),
    ]
    for endpoint, fetcher in attempts:
        try:
            rows = _parse_rows(fetcher())
            systems: list[dict] = []
            for row in rows[:top]:
                sep = row.get("Sep") or row.get("sep") or row.get("SEPARATION")
                sid = row.get("WDS") or row.get("wds")
                if not sid:
                    continue
                systems.append(
                    {
                        "id": str(sid),
                        "separation_arcsec": float(sep) if sep is not None else None,
                        "mag1": row.get("mag1") or row.get("MAG1"),
                        "mag2": row.get("mag2") or row.get("MAG2"),
                        "multiplicity": row.get("comp") or row.get("COMP"),
                        "ra_deg": row.get("RAdeg"),
                        "dec_deg": row.get("DEdeg"),
                        "source": "vizier_wds_tap_live",
                    }
                )
            if systems:
                return systems, endpoint
        except Exception as exc:
            errors.append(f"{endpoint}: {exc}")
    raise RuntimeError("; ".join(errors[-3:]))