#!/usr/bin/env python3
"""Tier 62 — Gaia DR3 TAP + VizieR WDS ingest with bundled fallback."""

from __future__ import annotations

import argparse
import json
import math
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "stellar_structures"
GAIA_BUNDLED = VENDOR / "gaia_dr3_tap_sample.json"
WDS_BUNDLED = VENDOR / "wds_multiplicity_expanded.json"
GAIA_CACHE = "gaia_dr3_live_cache.json"
WDS_CACHE = "wds_live_cache.json"

GAIA_TAP = "https://gea.esac.esa.int/tap-server/tap/sync"


def _gaia_adql() -> str:
    from live_api_limits import gaia_top_limit  # noqa: WPS433

    limit = gaia_top_limit()
    return (
        f"SELECT TOP {limit} source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag, bp_rp "
        "FROM gaiadr3.gaia_source WHERE parallax > 5 AND parallax/parallax_error > 4 "
        "ORDER BY phot_g_mean_mag"
    )


def external_cache_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    if raw:
        root = Path(raw).expanduser() / "tier62_live_astrometry"
    else:
        root = VENDOR / "live_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def fetch_gaia() -> list[dict]:
    params = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": _gaia_adql()}
    )
    url = f"{GAIA_TAP}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier62"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    rows = payload.get("data") or []
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 8:
            continue
        plx = float(row[3]) if row[3] is not None else None
        out.append(
            {
                "source_id": int(row[0]),
                "ra_deg": float(row[1]) if row[1] is not None else None,
                "dec_deg": float(row[2]) if row[2] is not None else None,
                "parallax_mas": plx,
                "pmra_masyr": float(row[4]) if row[4] is not None else None,
                "pmdec_masyr": float(row[5]) if row[5] is not None else None,
                "phot_g_mean_mag": float(row[6]) if row[6] is not None else None,
                "bp_rp": float(row[7]) if row[7] is not None else None,
                "distance_pc": round(1000.0 / plx, 4) if plx and plx > 0 else None,
                "pm_total_masyr": round(math.hypot(float(row[4] or 0), float(row[5] or 0)), 4),
                "source": "Gaia_DR3_TAP_live",
            }
        )
    return out


def load_gaia_bundled() -> list[dict]:
    if not GAIA_BUNDLED.exists():
        return []
    doc = json.loads(GAIA_BUNDLED.read_text(encoding="utf-8"))
    out: list[dict] = []
    for star in doc.get("stars") or []:
        plx = star.get("parallax_mas")
        pmra = star.get("pmra_masyr")
        pmdec = star.get("pmdec_masyr")
        out.append(
            {
                **star,
                "pm_total_masyr": round(math.hypot(float(pmra or 0), float(pmdec or 0)), 4) if pmra is not None else None,
                "source": "Gaia_DR3_bundled",
            }
        )
    return out


def load_wds_bundled() -> list[dict]:
    if not WDS_BUNDLED.exists():
        return []
    doc = json.loads(WDS_BUNDLED.read_text(encoding="utf-8"))
    return [{**s, "source": "WDS_bundled"} for s in doc.get("systems") or []]


def write_cache(name: str, source: str, objects: list[dict]) -> None:
    doc = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "object_count": len(objects),
        "objects": objects,
    }
    for path in (external_cache_root() / name, VENDOR / name):
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"Wrote {path} ({len(objects)} objects)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--deep", action="store_true", help="Larger Gaia DR3 TAP sample (TOP 60)")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER62_DEEP"] = "1"
    if args.offline:
        gaia = load_gaia_bundled()
        gaia_source = "bundled"
        wds = load_wds_bundled()
        wds_source = "bundled"
    else:
        try:
            gaia = fetch_gaia()
            gaia_source = "Gaia_DR3_TAP_live" if gaia else "bundled_fallback_empty"
            if not gaia:
                gaia = load_gaia_bundled()
        except Exception as exc:
            print(f"Gaia fetch failed ({exc}); bundled fallback")
            gaia = load_gaia_bundled()
            gaia_source = "bundled_fallback"
        wds = load_wds_bundled()
        wds_source = "WDS_bundled_vizier_roadmap"
    write_cache(GAIA_CACHE, gaia_source, gaia)
    write_cache(WDS_CACHE, wds_source, wds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())