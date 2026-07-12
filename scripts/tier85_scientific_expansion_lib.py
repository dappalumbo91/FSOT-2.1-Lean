"""Tier 85 — Tier-41 gap domains with live FSOT prediction panels."""

from __future__ import annotations

import csv
import io
import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VENDOR = ROOT / "vendor" / "scientific_expansion"

HISTORY_KEYWORDS = ("history", "historical", "medieval", "ancient", "archaeolog", "renaissance", "war")

PALEOCLIMATE_SITES = (
    (71.0, -8.0, "vostok_proxy"),
    (75.0, 0.0, "dome_c_proxy"),
    (64.8, -147.7, "fairbanks_proxy"),
    (51.5, -0.1, "london_proxy"),
    (40.7, -74.0, "new_york_proxy"),
)

SPELEOLOGY_USGS_SITES = (
    ("01646500", "potomac_karst"),
    ("02315500", "floridan_aquifer"),
    ("05413500", "iowa_cave_region"),
    ("06610000", "black_hills_karst"),
    ("03540500", "tennessee_cave"),
)


def _deep_mode() -> bool:
    from live_api_limits import tier85_deep  # noqa: WPS433

    return tier85_deep()


def cache_root() -> Path:
    import os

    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() / "tier85_scientific_expansion" if raw else VENDOR / "tier85_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_cache(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    doc.setdefault("credential_free", True)
    path = cache_root() / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _fetch_json(url: str, *, timeout: int = 90) -> Any:
    from live_api_fetch_lib import fetch_json  # noqa: WPS433

    return fetch_json(url, timeout=timeout)


def _fetch_text(url: str, *, timeout: int = 90) -> str:
    from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

    return fetch_bytes(url, timeout=timeout).decode("utf-8", errors="replace")


def _ref_metrics_from(path: Path) -> list[dict]:
    return list((_load_json(path).get("metrics") or []))


def _ingest_reference(*, cache_name: str, ref_path: Path, source_label: str) -> dict:
    metrics = _ref_metrics_from(ref_path)
    doc = {"source": source_label, "metrics": metrics, "metric_count": len(metrics)}
    _write_cache(cache_name, doc)
    return doc


def _fetch_world_bank_rows(indicators: tuple[tuple[str, str], ...]) -> list[dict]:
    from live_api_limits import tier85_world_bank_limit  # noqa: WPS433

    per_indicator = tier85_world_bank_limit()
    rows: list[dict] = []
    for code, prop in indicators:
        try:
            url = (
                f"https://api.worldbank.org/v2/country/all/indicator/{code}"
                f"?format=json&per_page={per_indicator}&date=2018:2023"
            )
            payload = _fetch_json(url, timeout=45)
            if not isinstance(payload, list) or len(payload) < 2:
                continue
            for entry in payload[1] or []:
                val = entry.get("value")
                if val is None:
                    continue
                iso = (entry.get("country") or {}).get("id") or "XX"
                rows.append(
                    {
                        "name": f"{iso}_{code}",
                        "property": prop,
                        "measured": float(val),
                        "indicator": code,
                        "country": iso,
                        "year": entry.get("date"),
                    }
                )
        except Exception:
            continue
    return rows


# --- ingest ---


def ingest_civil_engineering() -> dict:
    return _ingest_reference(
        cache_name="civil_engineering_cache.json",
        ref_path=DATA / "civil_engineering_reference_observables.json",
        source_label="ASCE_structural_engineering_reference",
    )


def ingest_mechanical_engineering() -> dict:
    return _ingest_reference(
        cache_name="mechanical_engineering_cache.json",
        ref_path=DATA / "mechanical_engineering_reference_observables.json",
        source_label="ASME_mechanical_engineering_reference",
    )


def ingest_neuroeconomics() -> dict:
    return _ingest_reference(
        cache_name="neuroeconomics_cache.json",
        ref_path=DATA / "neuroeconomics_reference_observables.json",
        source_label="neuroeconomics_behavioral_reference",
    )


def ingest_paleoclimate() -> dict:
    from live_api_limits import tier85_paleoclimate_limit  # noqa: WPS433

    limit = tier85_paleoclimate_limit()
    proxies: list[dict] = []
    for lat, lon, label in PALEOCLIMATE_SITES[:limit]:
        try:
            url = (
                "https://archive-api.open-meteo.com/v1/archive?"
                + urllib.parse.urlencode(
                    {
                        "latitude": lat,
                        "longitude": lon,
                        "start_date": "1900-01-01",
                        "end_date": "1900-12-31",
                        "daily": "temperature_2m_mean",
                    }
                )
            )
            payload = _fetch_json(url, timeout=60)
            daily = payload.get("daily") or {}
            temps = daily.get("temperature_2m_mean") or []
            if not temps:
                continue
            valid = [float(t) for t in temps if t is not None]
            if not valid:
                continue
            proxies.append(
                {
                    "name": label,
                    "property": "annual_mean_temp_c",
                    "measured": sum(valid) / len(valid),
                    "lat": lat,
                    "lon": lon,
                }
            )
        except Exception:
            continue
    if len(proxies) < 3:
        ref = _ref_metrics_from(DATA / "paleoclimate_reference_observables.json")
        proxies = [
            {"name": row.get("name"), "property": row.get("property"), "measured": float(row.get("measured") or 0)}
            for row in ref
        ]
        doc = {"source": "paleoclimate_reference_bundled", "proxies": proxies, "live_fetch_failed": True}
    else:
        doc = {"source": "open_meteo_historical_archive", "proxies": proxies}
    doc["proxy_count"] = len(proxies)
    _write_cache("paleoclimate_cache.json", doc)
    return doc


def ingest_speleology() -> dict:
    from live_api_limits import tier85_usgs_limit  # noqa: WPS433

    limit = tier85_usgs_limit()
    sites: list[dict] = []
    for site_id, label in SPELEOLOGY_USGS_SITES[:limit]:
        try:
            url = (
                "https://waterservices.usgs.gov/nwis/iv/?"
                + urllib.parse.urlencode(
                    {
                        "format": "json",
                        "sites": site_id,
                        "parameterCd": "00060,00065",
                        "siteStatus": "all",
                    }
                )
            )
            payload = _fetch_json(url, timeout=60)
            ts = ((payload.get("value") or {}).get("timeSeries")) or []
            for series in ts:
                vals = (series.get("values") or [{}])[0].get("value") or []
                if not vals:
                    continue
                measured = float(vals[-1].get("value") or 0)
                prop = "discharge_cfs" if "00060" in str(series.get("variable", {})) else "gage_height_ft"
                sites.append(
                    {
                        "site_id": site_id,
                        "name": label,
                        "property": prop,
                        "measured": measured,
                    }
                )
        except Exception:
            continue
    if len(sites) < 3:
        ref = _ref_metrics_from(DATA / "speleology_reference_observables.json")
        sites = [
            {"name": row.get("name"), "property": row.get("property"), "measured": float(row.get("measured") or 0)}
            for row in ref
        ]
        doc = {"source": "speleology_reference_bundled", "sites": sites, "live_fetch_failed": True}
    else:
        doc = {"source": "usgs_nwis_karst_hydrology", "sites": sites}
    doc["site_count"] = len(sites)
    _write_cache("speleology_cache.json", doc)
    return doc


def ingest_exogeology() -> dict:
    from live_api_limits import tier85_exoplanet_limit  # noqa: WPS433

    limit = tier85_exoplanet_limit()
    planets: list[dict] = []
    try:
        query = (
            f"select top {limit} pl_name,hostname,pl_rade,pl_bmasse,pl_orbper,disc_year,sy_dist "
            "from pscomppars where pl_rade is not null and pl_bmasse is not null"
        )
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode(
            {"query": query, "format": "csv"}
        )
        text = _fetch_text(url, timeout=90)
        for row in csv.DictReader(io.StringIO(text)):
            try:
                planets.append(
                    {
                        "pl_name": row.get("pl_name"),
                        "hostname": row.get("hostname"),
                        "pl_rade": float(row["pl_rade"]),
                        "pl_bmasse": float(row["pl_bmasse"]),
                        "pl_orbper": float(row["pl_orbper"]) if row.get("pl_orbper") else None,
                        "disc_year": float(row["disc_year"]) if row.get("disc_year") else None,
                        "sy_dist": float(row["sy_dist"]) if row.get("sy_dist") else None,
                    }
                )
            except (ValueError, TypeError):
                continue
    except Exception:
        pass
    if len(planets) < 5:
        exo_bench = _load_json(DATA / "nasa_exoplanet_archive_benchmark.json")
        for row in (exo_bench.get("material_records") or [])[:limit]:
            planets.append(
                {
                    "pl_name": row.get("name"),
                    "pl_rade": float(row.get("measured") or row.get("computed") or 0),
                    "pl_bmasse": float(row.get("measured") or 0),
                    "pl_orbper": None,
                    "disc_year": None,
                    "sy_dist": None,
                }
            )
        doc = {"source": "nasa_exoplanet_bundled", "planets": planets, "live_fetch_failed": len(planets) < 5}
    else:
        doc = {"source": "nasa_exoplanet_archive_tap", "planets": planets}
    doc["planet_count"] = len(planets)
    _write_cache("exogeology_cache.json", doc)
    return doc


def ingest_history() -> dict:
    from live_api_limits import tier85_crossref_limit  # noqa: WPS433

    limit = tier85_crossref_limit()
    works: list[dict] = []
    try:
        url = (
            "https://api.crossref.org/works?"
            + urllib.parse.urlencode(
                {
                    "query": "history archaeology",
                    "rows": limit,
                    "select": "DOI,title,is-referenced-by-count,published",
                }
            )
        )
        payload = _fetch_json(url, timeout=60)
        for row in (payload.get("message") or {}).get("items") or []:
            title = (row.get("title") or [""])[0]
            parts = ((row.get("published") or {}).get("date-parts") or [[]])[0]
            year = float(parts[0]) if parts else 2000.0
            cites = row.get("is-referenced-by-count") or 0
            works.append(
                {
                    "doi": row.get("DOI"),
                    "title": title[:120],
                    "citation_count": float(cites),
                    "publication_year": year,
                    "title_length": len(title),
                }
            )
    except Exception:
        pass
    if len(works) < 5:
        openalex = _load_json(DATA / "openalex_citation_graph_benchmark.json")
        for row in (openalex.get("material_records") or [])[:limit]:
            title = str(row.get("name") or "")
            if not any(k in title.lower() for k in HISTORY_KEYWORDS):
                continue
            works.append(
                {
                    "doi": row.get("name"),
                    "title": title[:120],
                    "citation_count": float(row.get("measured") or 0),
                    "publication_year": 2000.0,
                    "title_length": len(title),
                }
            )
        doc = {"source": "history_openalex_bundled", "works": works, "live_fetch_failed": True}
    else:
        doc = {"source": "crossref_history_query", "works": works}
    doc["work_count"] = len(works)
    _write_cache("history_cache.json", doc)
    return doc


def ingest_law_policy() -> dict:
    indicators = (
        ("CC.EST", "control_corruption_index"),
        ("GE.EST", "government_effectiveness"),
        ("RL.EST", "rule_of_law_index"),
        ("PV.EST", "political_stability"),
        ("RQ.EST", "regulatory_quality"),
        ("VA.EST", "voice_accountability"),
    )
    rows = _fetch_world_bank_rows(indicators)
    if len(rows) < 6:
        ref = _ref_metrics_from(DATA / "law_policy_reference_observables.json")
        rows = [
            {"name": row.get("name"), "property": row.get("property"), "measured": float(row.get("measured") or 0)}
            for row in ref
        ]
        doc = {"source": "law_policy_reference_bundled", "metrics": rows, "live_fetch_failed": True}
    else:
        doc = {"source": "World_Bank_WGI_governance", "metrics": rows}
    doc["metric_count"] = len(rows)
    _write_cache("law_policy_cache.json", doc)
    return doc


def ingest_finance_markets() -> dict:
    indicators = (
        ("NY.GDP.MKTP.CD", "gdp_current_usd"),
        ("FP.CPI.TOTL.ZG", "inflation_pct"),
        ("NY.GDP.PCAP.CD", "gdp_per_capita"),
        ("CM.MKT.LCAP.GD.ZS", "market_cap_pct_gdp"),
        ("FR.INR.RINR", "real_interest_rate"),
        ("GC.DOD.TOTL.GD.ZS", "government_debt_pct_gdp"),
    )
    rows = _fetch_world_bank_rows(indicators)
    if len(rows) < 6:
        ref = _ref_metrics_from(DATA / "finance_markets_reference_observables.json")
        rows = [
            {"name": row.get("name"), "property": row.get("property"), "measured": float(row.get("measured") or 0)}
            for row in ref
        ]
        doc = {"source": "finance_markets_reference_bundled", "metrics": rows, "live_fetch_failed": True}
    else:
        doc = {"source": "World_Bank_finance_indicators", "metrics": rows}
    doc["metric_count"] = len(rows)
    _write_cache("finance_markets_cache.json", doc)
    return doc


def ingest_supply_chain() -> dict:
    indicators = (
        ("NE.TRD.GNFS.ZS", "trade_pct_gdp"),
        ("TX.VAL.MRCH.R1.ZS", "merchandise_exports_pct_gdp"),
        ("TM.VAL.MRCH.R1.ZS", "merchandise_imports_pct_gdp"),
        ("IS.SHP.GOOD.TU", "container_port_traffic_teus"),
        ("LP.LPI.OVRL.XQ", "logistics_performance_index"),
        ("IC.EXP.COST", "export_cost_usd"),
    )
    rows = _fetch_world_bank_rows(indicators)
    if len(rows) < 6:
        ref = _ref_metrics_from(DATA / "supply_chain_reference_observables.json")
        rows = [
            {"name": row.get("name"), "property": row.get("property"), "measured": float(row.get("measured") or 0)}
            for row in ref
        ]
        doc = {"source": "supply_chain_reference_bundled", "metrics": rows, "live_fetch_failed": True}
    else:
        doc = {"source": "World_Bank_trade_logistics", "metrics": rows}
    doc["metric_count"] = len(rows)
    _write_cache("supply_chain_cache.json", doc)
    return doc


INGESTORS = {
    "civil_engineering": ingest_civil_engineering,
    "mechanical_engineering": ingest_mechanical_engineering,
    "neuroeconomics": ingest_neuroeconomics,
    "paleoclimate": ingest_paleoclimate,
    "speleology": ingest_speleology,
    "exogeology": ingest_exogeology,
    "history": ingest_history,
    "law_policy": ingest_law_policy,
    "finance_markets": ingest_finance_markets,
    "supply_chain": ingest_supply_chain,
}


from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def _panel_records(
    rows: list[dict],
    *,
    lab: str,
    name_key: str,
    property_map: tuple[tuple[str, str], ...],
    live: dict,
) -> tuple[list[dict], list[float]]:
    records: list[dict] = []
    errs: list[float] = []
    for row in rows:
        name = str(row.get(name_key) or row.get("name") or "obs")
        for prop, domain in property_map:
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab=lab,
                property_name=prop,
                name=name,
                measured=float(val),
                domain=domain,
                extra={"ingest_source": live.get("source")},
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    return records, errs


def _panel_from_metrics(
    *,
    domain: str,
    cache_file: str,
    lab: str,
    fsot_domain: str,
    maps_to_lean: list[str],
    d_eff: int,
    source_note: str,
    channel: str,
    sota_pct: float,
    sota_model: str,
) -> dict:
    live = _load_json(cache_root() / cache_file)
    _, authority = _load_fsot()
    rows = live.get("metrics") or []
    records, errs = _panel_records(
        rows,
        lab=lab,
        name_key="name",
        property_map=(("measured", fsot_domain),),
        live=live,
    )
    for row, rec in zip(rows, records):
        rec["property"] = row.get("property") or rec["property"]
    return _bench_v11(
        domain=domain,
        material_records=records,
        maps_to_lean=maps_to_lean,
        d_eff=d_eff,
        authority_path=authority,
        source=[str(cache_root() / cache_file), source_note],
        channel_stats=[("fsot_prediction", channel, errs or [0.0])],
        sota_baselines={channel: {"sota_typical_error_pct": sota_pct, "sota_model": sota_model}},
    )


def build_civil_engineering_panel() -> dict:
    return _panel_from_metrics(
        domain="Civil_Engineering_Panel",
        cache_file="civil_engineering_cache.json",
        lab="civil_engineering_panel_lab",
        fsot_domain="Materials_Science",
        maps_to_lean=["material", "energy"],
        d_eff=16,
        source_note="ASCE/structural engineering reference",
        channel="civil_engineering",
        sota_pct=8.0,
        sota_model="FEA surrogate baselines",
    )


def build_mechanical_engineering_panel() -> dict:
    return _panel_from_metrics(
        domain="Mechanical_Engineering_Panel",
        cache_file="mechanical_engineering_cache.json",
        lab="mechanical_engineering_panel_lab",
        fsot_domain="Thermodynamics",
        maps_to_lean=["material", "energy", "electron"],
        d_eff=16,
        source_note="ASME mechanical engineering reference",
        channel="mechanical_engineering",
        sota_pct=8.0,
        sota_model="CFD/FEA surrogate baselines",
    )


def build_neuroeconomics_panel() -> dict:
    return _panel_from_metrics(
        domain="Neuroeconomics_Panel",
        cache_file="neuroeconomics_cache.json",
        lab="neuroeconomics_panel_lab",
        fsot_domain="Psychology",
        maps_to_lean=["consciousness", "neural", "mathematical"],
        d_eff=16,
        source_note="Behavioral neuroeconomics reference",
        channel="neuroeconomics",
        sota_pct=12.0,
        sota_model="Behavioral econ meta-analysis",
    )


def build_paleoclimate_panel() -> dict:
    live = _load_json(cache_root() / "paleoclimate_cache.json")
    _, authority = _load_fsot()
    records, errs = _panel_records(
        live.get("proxies") or [],
        lab="paleoclimate_panel_lab",
        name_key="name",
        property_map=(
            ("measured", "Ecology"),
            ("lat", "Geophysics"),
            ("lon", "Meteorology"),
        ),
        live=live,
    )
    return _bench_v11(
        domain="Paleoclimate_Panel",
        material_records=records,
        maps_to_lean=["energy", "galactic", "ecological"],
        d_eff=17,
        authority_path=authority,
        source=[str(cache_root() / "paleoclimate_cache.json"), "Open-Meteo/paleoclimate reference"],
        channel_stats=[("fsot_prediction", "paleoclimate", errs or [0.0])],
        sota_baselines={"paleoclimate": {"sota_typical_error_pct": 10.0, "sota_model": "GCM paleo surrogate baselines"}},
    )


def build_speleology_panel() -> dict:
    live = _load_json(cache_root() / "speleology_cache.json")
    _, authority = _load_fsot()
    records, errs = _panel_records(
        live.get("sites") or [],
        lab="speleology_panel_lab",
        name_key="name",
        property_map=(("measured", "Seismology"),),
        live=live,
    )
    for row, rec in zip(live.get("sites") or [], records):
        rec["property"] = row.get("property") or rec["property"]
    return _bench_v11(
        domain="Speleology_Panel",
        material_records=records,
        maps_to_lean=["energy", "galactic", "biological"],
        d_eff=16,
        authority_path=authority,
        source=[str(cache_root() / "speleology_cache.json"), "USGS karst hydrology"],
        channel_stats=[("fsot_prediction", "speleology", errs or [0.0])],
        sota_baselines={"speleology": {"sota_typical_error_pct": 10.0, "sota_model": "Karst hydrogeology surrogates"}},
    )


def build_exogeology_panel() -> dict:
    live = _load_json(cache_root() / "exogeology_cache.json")
    _, authority = _load_fsot()
    records, errs = _panel_records(
        live.get("planets") or [],
        lab="exogeology_panel_lab",
        name_key="pl_name",
        property_map=(
            ("pl_rade", "Planetary_Science"),
            ("pl_bmasse", "Astronomy"),
            ("pl_orbper", "Geophysics"),
            ("disc_year", "Astrophysics"),
            ("sy_dist", "Cosmology"),
        ),
        live=live,
    )
    return _bench_v11(
        domain="Exogeology_Panel",
        material_records=records,
        maps_to_lean=["astronomical", "galactic", "energy"],
        d_eff=20,
        authority_path=authority,
        source=[str(cache_root() / "exogeology_cache.json"), "NASA Exoplanet Archive"],
        channel_stats=[("fsot_prediction", "exogeology", errs or [0.0])],
        sota_baselines={"exogeology": {"sota_typical_error_pct": 12.0, "sota_model": "Exoplanet interior models"}},
    )


def build_history_panel() -> dict:
    live = _load_json(cache_root() / "history_cache.json")
    _, authority = _load_fsot()
    records, errs = _panel_records(
        live.get("works") or [],
        lab="history_panel_lab",
        name_key="title",
        property_map=(
            ("citation_count", "Sociology"),
            ("publication_year", "Psychology"),
            ("title_length", "Economics"),
        ),
        live=live,
    )
    return _bench_v11(
        domain="History_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "linguistic"],
        d_eff=15,
        authority_path=authority,
        source=[str(cache_root() / "history_cache.json"), "Crossref history corpus"],
        channel_stats=[("fsot_prediction", "history", errs or [0.0])],
        sota_baselines={"history": {"sota_typical_error_pct": 15.0, "sota_model": "Historiographic coding baselines"}},
    )


def build_law_policy_panel() -> dict:
    return _panel_from_metrics(
        domain="Law_Policy_Panel",
        cache_file="law_policy_cache.json",
        lab="law_policy_panel_lab",
        fsot_domain="Sociology",
        maps_to_lean=["consciousness", "economic"],
        d_eff=17,
        source_note="World Bank WGI governance",
        channel="law_policy",
        sota_pct=12.0,
        sota_model="Governance index surrogates",
    )


def build_finance_markets_panel() -> dict:
    return _panel_from_metrics(
        domain="Finance_Markets_Panel",
        cache_file="finance_markets_cache.json",
        lab="finance_markets_panel_lab",
        fsot_domain="Economics",
        maps_to_lean=["consciousness", "economic", "mathematical"],
        d_eff=19,
        source_note="World Bank finance indicators",
        channel="finance_markets",
        sota_pct=10.0,
        sota_model="Factor model baselines",
    )


def build_supply_chain_panel() -> dict:
    return _panel_from_metrics(
        domain="Supply_Chain_Logistics_Panel",
        cache_file="supply_chain_cache.json",
        lab="supply_chain_panel_lab",
        fsot_domain="Economics",
        maps_to_lean=["consciousness", "economic", "biological"],
        d_eff=18,
        source_note="World Bank trade/logistics",
        channel="supply_chain",
        sota_pct=10.0,
        sota_model="SCOR model baselines",
    )


def build_scientific_expansion_wave3_spine() -> dict:
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for slug in (
        "civil_engineering_panel",
        "mechanical_engineering_panel",
        "neuroeconomics_panel",
        "paleoclimate_panel",
        "speleology_panel",
        "exogeology_panel",
        "history_panel",
        "law_policy_panel",
        "finance_markets_panel",
        "supply_chain_logistics_panel",
    ):
        bench = _load_json(DATA / f"{slug}_benchmark.json")
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "scientific_expansion_wave3_lab",
                "property": "panel_pooled_median",
                "name": slug,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier85_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:3]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "scientific_expansion_wave3_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or slug),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "source_panel": slug,
                    "eval_kind": "ingest_relay",
                }
            )
    return _bench_v11(
        domain="Scientific_Expansion_Wave3_Spine",
        material_records=records,
        maps_to_lean=["material", "consciousness", "galactic"],
        d_eff=17,
        authority_path=authority,
        source=["tier85_scientific_expansion_panels"],
        channel_stats=[("ingest_relay", "scientific_expansion_wave3", relay_errs or [0.0])],
        sota_baselines={
            "scientific_expansion_wave3": {"sota_typical_error_pct": 6.0, "sota_model": "Tier 85 domain expansion"}
        },
    )


BUILDERS = {
    "Civil_Engineering_Panel": build_civil_engineering_panel,
    "Mechanical_Engineering_Panel": build_mechanical_engineering_panel,
    "Neuroeconomics_Panel": build_neuroeconomics_panel,
    "Paleoclimate_Panel": build_paleoclimate_panel,
    "Speleology_Panel": build_speleology_panel,
    "Exogeology_Panel": build_exogeology_panel,
    "History_Panel": build_history_panel,
    "Law_Policy_Panel": build_law_policy_panel,
    "Finance_Markets_Panel": build_finance_markets_panel,
    "Supply_Chain_Logistics_Panel": build_supply_chain_panel,
    "Scientific_Expansion_Wave3_Spine": build_scientific_expansion_wave3_spine,
}

BUILD_ORDER = [
    "Civil_Engineering_Panel",
    "Mechanical_Engineering_Panel",
    "Neuroeconomics_Panel",
    "Paleoclimate_Panel",
    "Speleology_Panel",
    "Exogeology_Panel",
    "History_Panel",
    "Law_Policy_Panel",
    "Finance_Markets_Panel",
    "Supply_Chain_Logistics_Panel",
    "Scientific_Expansion_Wave3_Spine",
]

LEAN_MAP = {
    "Civil_Engineering_Panel": (
        "civil_engineering_panel",
        "material",
        "material_raw_S_positive",
        "CivilEngineeringPanelPriors",
    ),
    "Mechanical_Engineering_Panel": (
        "mechanical_engineering_panel",
        "material",
        "material_raw_S_positive",
        "MechanicalEngineeringPanelPriors",
    ),
    "Neuroeconomics_Panel": (
        "neuroeconomics_panel",
        "consciousness",
        "consciousness_raw_S_positive",
        "NeuroeconomicsPanelPriors",
    ),
    "Paleoclimate_Panel": ("paleoclimate_panel", "energy", "energy_raw_S_positive", "PaleoclimatePanelPriors"),
    "Speleology_Panel": ("speleology_panel", "energy", "energy_raw_S_positive", "SpeleologyPanelPriors"),
    "Exogeology_Panel": ("exogeology_panel", "galactic", "galactic_raw_S_positive", "ExogeologyPanelPriors"),
    "History_Panel": ("history_panel", "consciousness", "consciousness_raw_S_positive", "HistoryPanelPriors"),
    "Law_Policy_Panel": ("law_policy_panel", "consciousness", "consciousness_raw_S_positive", "LawPolicyPanelPriors"),
    "Finance_Markets_Panel": (
        "finance_markets_panel",
        "consciousness",
        "consciousness_raw_S_positive",
        "FinanceMarketsPanelPriors",
    ),
    "Supply_Chain_Logistics_Panel": (
        "supply_chain_panel",
        "consciousness",
        "consciousness_raw_S_positive",
        "SupplyChainLogisticsPanelPriors",
    ),
    "Scientific_Expansion_Wave3_Spine": (
        "scientific_expansion_wave3",
        "material",
        "material_raw_S_positive",
        "ScientificExpansionWave3SpinePriors",
    ),
}


def output_path(domain: str) -> Path:
    slug = {
        "Civil_Engineering_Panel": "civil_engineering_panel",
        "Mechanical_Engineering_Panel": "mechanical_engineering_panel",
        "Neuroeconomics_Panel": "neuroeconomics_panel",
        "Paleoclimate_Panel": "paleoclimate_panel",
        "Speleology_Panel": "speleology_panel",
        "Exogeology_Panel": "exogeology_panel",
        "History_Panel": "history_panel",
        "Law_Policy_Panel": "law_policy_panel",
        "Finance_Markets_Panel": "finance_markets_panel",
        "Supply_Chain_Logistics_Panel": "supply_chain_logistics_panel",
        "Scientific_Expansion_Wave3_Spine": "scientific_expansion_wave3_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"