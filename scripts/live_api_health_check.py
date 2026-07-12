#!/usr/bin/env python3
"""Probe every FSOT live API channel and report status (not rate-limit guessing)."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from live_api_fetch_lib import fetch_json, ssl_context  # noqa: E402
from live_api_limits import (  # noqa: E402
    gaia_top_limit,
    materials_project_api_limit,
    mega_deep,
    wds_vizier_top_limit,
)

OUT = ROOT / "data" / "live_api_health_report.json"


def _probe(name: str, fn) -> dict:
    try:
        detail = fn()
        return {"channel": name, "status": "ok", "detail": detail}
    except Exception as exc:
        return {
            "channel": name,
            "status": "fail",
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
        }


def main() -> int:
    deep = mega_deep() or os.environ.get("FSOT_TIER68_DEEP", "")
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "mega_deep": bool(deep),
        "channels": [],
    }

    def gbif():
        url = "https://api.gbif.org/v1/occurrence/search?limit=3&hasCoordinate=true"
        data = fetch_json(url, timeout=30)
        return f"count={data.get('count')}"

    def gwosc():
        data = fetch_json("https://www.gw-openscience.org/eventapi/json/", timeout=30)
        return f"catalogs={len(data) if isinstance(data, dict) else len(data)}"

    def simbad():
        import urllib.parse

        adql = "SELECT TOP 3 main_id FROM basic"
        p = urllib.parse.urlencode(
            {"request": "doQuery", "lang": "adql", "format": "json", "query": adql}
        )
        url = f"https://simbad.cds.unistra.fr/simbad/sim-tap/sync?{p}"
        data = fetch_json(url, timeout=60)
        return f"rows={len(data.get('data') or [])}"

    def gaia():
        import urllib.parse

        adql = "SELECT TOP 3 source_id FROM gaiadr3.gaia_source"
        p = urllib.parse.urlencode(
            {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
        )
        url = f"https://gea.esac.esa.int/tap-server/tap/sync?{p}"
        data = fetch_json(url, timeout=90)
        return f"rows={len(data.get('data') or [])}"

    def vizier_wds():
        from vizier_wds_fetch_lib import fetch_wds_systems  # noqa: WPS433

        systems, src = fetch_wds_systems(top=min(10, wds_vizier_top_limit()))
        return f"source={src} n={len(systems)}"

    def materials():
        key = os.environ.get("MP_API_KEY", "").strip()
        if not key:
            return "skipped_no_MP_API_KEY (bundled+expansion panel used)"
        url = (
            "https://api.materialsproject.org/materials/summary/"
            f"?_limit={min(5, materials_project_api_limit())}"
        )
        req = urllib.request.Request(
            url, headers={"X-API-KEY": key, "User-Agent": "FSOT-health"}
        )
        with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as resp:
            data = json.loads(resp.read().decode())
        return f"rows={len(data.get('data') or [])}"

    def openneuro():
        from openneuro_live_lib import fetch_openneuro_datasets  # noqa: WPS433

        ds = fetch_openneuro_datasets(pages=1, page_size=3)
        return f"datasets={len(ds)}"

    def pubchem():
        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/"
            "MolecularWeight/JSON"
        )
        data = fetch_json(url, timeout=30)
        return "cid=2244 ok"

    def nasa_neo():
        key = os.environ.get("NASA_API_KEY", "DEMO_KEY").strip() or "DEMO_KEY"
        url = (
            "https://api.nasa.gov/neo/rest/v1/feed?"
            "start_date=2025-06-01&end_date=2025-06-03&"
            f"api_key={urllib.parse.quote(key)}"
        )
        data = fetch_json(url, timeout=30)
        return f"element_count={data.get('element_count')}"

    def nasa_donki():
        key = os.environ.get("NASA_API_KEY", "DEMO_KEY").strip() or "DEMO_KEY"
        url = (
            "https://api.nasa.gov/DONKI/FLR?startDate=2025-01-01&endDate=2025-01-15&"
            f"api_key={urllib.parse.quote(key)}"
        )
        data = fetch_json(url, timeout=30)
        return f"flares={len(data) if isinstance(data, list) else 0}"

    def clinicaltrials():
        data = fetch_json(
            "https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=3",
            timeout=30,
        )
        return f"studies={len(data.get('studies') or [])}"

    def osti():
        data = fetch_json("https://www.osti.gov/api/v1/records?rows=3", timeout=30)
        rows = data if isinstance(data, list) else (data.get("records") or [])
        return f"records={len(rows)}"

    def uap_war_gov():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://huggingface.co/datasets/MTSlive/war-gov-uap-release-1/resolve/main/documents.jsonl",
            timeout=45,
        ).decode("utf-8")
        n = sum(1 for line in raw.splitlines() if line.strip())
        return f"documents_jsonl_lines={n}"

    for name, fn in (
        ("gbif", gbif),
        ("gwosc", gwosc),
        ("simbad_tap", simbad),
        ("gaia_dr3_tap", gaia),
        ("vizier_wds", vizier_wds),
        ("materials_project", materials),
        ("openneuro_graphql", openneuro),
        ("pubchem_pug", pubchem),
        ("nasa_neo_feed", nasa_neo),
        ("nasa_donki_flr", nasa_donki),
        ("clinicaltrials_v2", clinicaltrials),
        ("osti_doe_records", osti),
        ("uap_war_gov_hf", uap_war_gov),
    ):
        row = _probe(name, fn)
        report["channels"].append(row)
        tag = "OK" if row["status"] == "ok" else "FAIL"
        print(f"{tag} {name}: {row.get('detail') or row.get('error')}")

    fails = [c for c in report["channels"] if c["status"] == "fail"]
    report["fail_count"] = len(fails)
    report["ok_count"] = len(report["channels"]) - len(fails)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT} ({report['ok_count']} ok / {report['fail_count']} fail)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())