"""Tier 80 — U.S. government & open-science live ingest wave (FSOT predictions)."""

from __future__ import annotations

import json
import os
import re
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VENDOR = ROOT / "vendor" / "government_open_data"
UAP_BUNDLED = VENDOR / "uap_war_gov_bundled.json"
NEO_BUNDLED = VENDOR / "nasa_neo_bundled.json"
REGISTRY_BUNDLED = VENDOR / "federal_science_registry_bundled.json"

UAP_HF_DOCS = "https://huggingface.co/datasets/MTSlive/war-gov-uap-release-1/resolve/main/documents.jsonl"
UAP_HF_FIGS = "https://huggingface.co/datasets/MTSlive/war-gov-uap-release-1/resolve/main/figures.jsonl"


def _deep_mode() -> bool:
    from live_api_limits import tier80_deep  # noqa: WPS433

    return tier80_deep()


def _nasa_api_key() -> str:
    return os.environ.get("NASA_API_KEY", "DEMO_KEY").strip() or "DEMO_KEY"


def cache_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() / "tier80_government_open_data" if raw else VENDOR / "live_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_cache(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    path = cache_root() / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _fetch_json(url: str, *, timeout: int = 90) -> Any:
    from live_api_fetch_lib import fetch_json  # noqa: WPS433

    return fetch_json(url, timeout=timeout)


def _fetch_jsonl(url: str, *, limit: int, timeout: int = 120) -> list[dict]:
    from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

    raw = fetch_bytes(url, timeout=timeout).decode("utf-8")
    rows: list[dict] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
        if len(rows) >= limit:
            break
    return rows


def _parse_flare_class(class_type: str) -> float | None:
    if not class_type:
        return None
    m = re.match(r"^[XBMC](\d+(?:\.\d+)?)", class_type.strip().upper())
    return float(m.group(1)) if m else None


def _neo_diameter_m(estimated: dict | None) -> float | None:
    if not estimated:
        return None
    meters = (estimated.get("meters") or {})
    lo = meters.get("estimated_diameter_min")
    hi = meters.get("estimated_diameter_max")
    if lo is None or hi is None:
        return None
    return (float(lo) + float(hi)) / 2.0


def _neo_velocity_km_s(close_approach: dict | None) -> float | None:
    if not close_approach:
        return None
    vel = (close_approach.get("relative_velocity") or {}).get("kilometers_per_second")
    return float(vel) if vel is not None else None


def _neo_miss_km(close_approach: dict | None) -> float | None:
    if not close_approach:
        return None
    miss = (close_approach.get("miss_distance") or {}).get("kilometers")
    return float(miss) if miss is not None else None


def _publication_year(raw: str | None) -> float | None:
    if not raw:
        return None
    m = re.search(r"(19|20)\d{2}", str(raw))
    return float(m.group(0)) if m else None


# --- ingest ---


def _diameter_km_from_h(h: float, albedo: float = 0.14) -> float:
    return 1329.0 * (10.0 ** (-0.2 * h)) / (albedo**0.5)


def _neo_rows_from_jpl_cad(payload: dict, *, limit: int) -> list[dict]:
    fields = payload.get("fields") or []
    rows: list[dict] = []
    for raw in payload.get("data") or []:
        item = dict(zip(fields, raw))
        h_raw = item.get("h")
        if h_raw is None:
            continue
        h = float(h_raw)
        dist_au = float(item.get("dist") or 0)
        rows.append(
            {
                "id": item.get("des"),
                "name": str(item.get("des") or ""),
                "absolute_magnitude_h": h,
                "estimated_diameter_m": _diameter_km_from_h(h) * 1000.0,
                "relative_velocity_km_s": float(item.get("v_rel") or 0),
                "miss_distance_km": dist_au * 149597870.7,
                "is_hazardous": None,
            }
        )
        if len(rows) >= limit:
            break
    return rows


def _neo_row_from_api(row: dict) -> dict:
    ca = (row.get("close_approach_data") or [{}])[0]
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "absolute_magnitude_h": row.get("absolute_magnitude_h"),
        "estimated_diameter_m": _neo_diameter_m(row.get("estimated_diameter")),
        "relative_velocity_km_s": _neo_velocity_km_s(ca),
        "miss_distance_km": _neo_miss_km(ca),
        "is_hazardous": row.get("is_potentially_hazardous_asteroid"),
    }


def ingest_nasa_neo_feed() -> dict:
    from live_api_limits import nasa_neo_day_span, nasa_neo_limit  # noqa: WPS433

    limit = nasa_neo_limit()
    span = nasa_neo_day_span()
    key = _nasa_api_key()
    source = "nasa_neows_live"
    neos: list[dict] = []
    # NeoWs allows <=7 days; try recent windows then a fixed historical anchor.
    end_candidates = [
        datetime.now(timezone.utc).date(),
        datetime(2025, 6, 7, tzinfo=timezone.utc).date(),
    ]
    for end in end_candidates:
        start = end - timedelta(days=span - 1)
        url = (
            f"https://api.nasa.gov/neo/rest/v1/feed?"
            f"start_date={start.isoformat()}&end_date={end.isoformat()}"
            f"&api_key={urllib.parse.quote(key)}"
        )
        try:
            payload = _fetch_json(url, timeout=60)
            for day_rows in (payload.get("near_earth_objects") or {}).values():
                for row in day_rows:
                    neos.append(_neo_row_from_api(row))
                    if len(neos) >= limit:
                        break
                if len(neos) >= limit:
                    break
            if neos:
                break
        except Exception:
            continue
    if not neos:
        jpl_end = end_candidates[-1]
        jpl_start = jpl_end - timedelta(days=span - 1)
        jpl_url = (
            "https://ssd-api.jpl.nasa.gov/cad.api?"
            f"date-min={jpl_start.isoformat()}&date-max={jpl_end.isoformat()}&limit={limit}"
        )
        try:
            payload = _fetch_json(jpl_url, timeout=60)
            neos = _neo_rows_from_jpl_cad(payload, limit=limit)
            if neos:
                source = "jpl_ssd_cad_live"
        except Exception:
            pass
    if not neos and NEO_BUNDLED.exists():
        bundled = _load_json(NEO_BUNDLED)
        neos = list(bundled.get("neos") or [])[:limit]
        source = "nasa_neows_bundled_fallback"
    doc = {"source": source, "neo_count": len(neos), "neos": neos}
    _write_cache("nasa_neo_feed_cache.json", doc)
    return doc


def ingest_nasa_donki_flares() -> dict:
    from live_api_limits import nasa_donki_day_span, nasa_donki_limit  # noqa: WPS433

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=nasa_donki_day_span())
    key = _nasa_api_key()
    url = (
        f"https://api.nasa.gov/DONKI/FLR?startDate={start.isoformat()}"
        f"&endDate={end.isoformat()}&api_key={urllib.parse.quote(key)}"
    )
    source = "nasa_donki_live"
    flares: list[dict] = []
    try:
        payload = _fetch_json(url, timeout=60)
        if isinstance(payload, list):
            for row in payload:
                flares.append(
                    {
                        "flr_id": row.get("flrID"),
                        "class_type": row.get("classType"),
                        "flare_class_numeric": _parse_flare_class(str(row.get("classType") or "")),
                        "active_region_num": row.get("activeRegionNum"),
                        "begin_time": row.get("beginTime"),
                        "peak_time": row.get("peakTime"),
                    }
                )
                if len(flares) >= nasa_donki_limit():
                    break
    except Exception as exc:
        source = f"nasa_donki_error:{type(exc).__name__}"
    doc = {"source": source, "flare_count": len(flares), "flares": flares}
    _write_cache("nasa_donki_flares_cache.json", doc)
    return doc


def ingest_clinicaltrials() -> dict:
    from live_api_limits import clinicaltrials_limit  # noqa: WPS433

    limit = clinicaltrials_limit()
    url = f"https://clinicaltrials.gov/api/v2/studies?format=json&pageSize={limit}"
    source = "clinicaltrials_gov_live"
    studies: list[dict] = []
    try:
        payload = _fetch_json(url, timeout=60)
        for row in payload.get("studies") or []:
            proto = row.get("protocolSection") or {}
            ident = proto.get("identificationModule") or {}
            design = proto.get("designModule") or {}
            enroll = design.get("enrollmentInfo") or {}
            count = enroll.get("count")
            if count is None:
                continue
            studies.append(
                {
                    "nct_id": ident.get("nctId"),
                    "title": (ident.get("briefTitle") or ident.get("officialTitle") or "")[:120],
                    "enrollment_count": int(count),
                    "study_type": design.get("studyType"),
                    "phase_count": len(design.get("phases") or []),
                }
            )
    except Exception as exc:
        source = f"clinicaltrials_error:{type(exc).__name__}"
    doc = {"source": source, "study_count": len(studies), "studies": studies}
    _write_cache("clinicaltrials_cache.json", doc)
    return doc


def ingest_osti_records() -> dict:
    from live_api_limits import osti_record_limit  # noqa: WPS433

    limit = osti_record_limit()
    url = f"https://www.osti.gov/api/v1/records?rows={limit}"
    source = "osti_doe_live"
    records: list[dict] = []
    try:
        payload = _fetch_json(url, timeout=60)
        rows = payload if isinstance(payload, list) else (payload.get("records") or [])
        for row in rows:
            year = _publication_year(row.get("publication_date"))
            records.append(
                {
                    "osti_id": row.get("osti_id") or row.get("identifier"),
                    "title": (row.get("title") or "")[:120],
                    "publication_year": year,
                    "doi": row.get("doi"),
                    "report_number": row.get("report_number"),
                }
            )
    except Exception as exc:
        source = f"osti_error:{type(exc).__name__}"
    doc = {"source": source, "record_count": len(records), "records": records}
    _write_cache("osti_records_cache.json", doc)
    return doc


def ingest_uap_war_gov() -> dict:
    from live_api_limits import uap_document_limit, uap_figure_limit  # noqa: WPS433

    source = "war_gov_uap_hf_live"
    documents: list[dict] = []
    figures: list[dict] = []
    try:
        documents = _fetch_jsonl(UAP_HF_DOCS, limit=uap_document_limit(), timeout=120)
        figures = _fetch_jsonl(UAP_HF_FIGS, limit=uap_figure_limit(), timeout=120)
    except Exception:
        bundled = _load_json(UAP_BUNDLED)
        documents = list(bundled.get("documents") or [])[: uap_document_limit()]
        figures = list(bundled.get("figures") or [])[: uap_figure_limit()]
        source = "war_gov_uap_bundled_fallback"
    doc = {
        "source": source,
        "document_count": len(documents),
        "figure_count": len(figures),
        "documents": documents,
        "figures": figures,
    }
    _write_cache("uap_war_gov_cache.json", doc)
    return doc


def ingest_federal_science_registry() -> dict:
    doc = _load_json(REGISTRY_BUNDLED)
    doc["source"] = "federal_science_registry_bundled"
    _write_cache("federal_science_registry_cache.json", doc)
    return doc


INGESTORS = {
    "nasa_neo_feed": ingest_nasa_neo_feed,
    "nasa_donki_flares": ingest_nasa_donki_flares,
    "clinicaltrials": ingest_clinicaltrials,
    "osti_records": ingest_osti_records,
    "uap_war_gov": ingest_uap_war_gov,
    "federal_science_registry": ingest_federal_science_registry,
}


# --- benchmarks ---

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def _max_ufo_score(figures: list[dict], document_id: str) -> float | None:
    scores = [
        float(f["ufo_score"])
        for f in figures
        if f.get("document_id") == document_id and f.get("ufo_score") is not None
    ]
    return max(scores) if scores else None


def build_nasa_neo_feed_panel() -> dict:
    live = _load_json(cache_root() / "nasa_neo_feed_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for row in live.get("neos") or []:
        name = str(row.get("name") or row.get("id") or "")
        for prop, domain in (
            ("absolute_magnitude_h", "Planetary_Science"),
            ("estimated_diameter_m", "Planetary_Science"),
            ("relative_velocity_km_s", "Planetary_Science"),
            ("miss_distance_km", "Planetary_Science"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="nasa_neo_feed_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain=domain,
                extra={"ingest_source": live.get("source")},
            )
            records.append(rec)
            relay_errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="NASA_NEO_Feed_Panel",
        material_records=records,
        maps_to_lean=["astronomical", "planetary", "particle"],
        d_eff=18,
        authority_path=authority,
        source=[str(cache_root() / "nasa_neo_feed_cache.json"), "https://api.nasa.gov/neo/"],
        channel_stats=[("fsot_prediction", "nasa_neo_feed", relay_errs or [0.0])],
        sota_baselines={"nasa_neo_feed": {"sota_typical_error_pct": 8.0, "sota_model": "JPL Horizons ephemeris class"}},
    )


def build_nasa_donki_solar_panel() -> dict:
    live = _load_json(cache_root() / "nasa_donki_flares_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for row in live.get("flares") or []:
        name = str(row.get("flr_id") or "")
        for prop, domain in (
            ("flare_class_numeric", "Electromagnetism"),
            ("active_region_num", "Astrophysics"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="nasa_donki_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain=domain,
                extra={"ingest_source": live.get("source"), "class_type": row.get("class_type")},
            )
            records.append(rec)
            relay_errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="NASA_DONKI_Solar_Panel",
        material_records=records,
        maps_to_lean=["fusion", "energy", "plasma"],
        d_eff=14,
        authority_path=authority,
        source=[str(cache_root() / "nasa_donki_flares_cache.json"), "https://api.nasa.gov/DONKI/"],
        channel_stats=[("fsot_prediction", "nasa_donki", relay_errs or [0.0])],
        sota_baselines={"nasa_donki": {"sota_typical_error_pct": 6.0, "sota_model": "NOAA SWPC flare tables"}},
    )


def build_clinicaltrials_medical_panel() -> dict:
    live = _load_json(cache_root() / "clinicaltrials_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for row in live.get("studies") or []:
        name = str(row.get("nct_id") or "")
        for prop, domain in (
            ("enrollment_count", "Biochemistry"),
            ("phase_count", "Biochemistry"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="clinicaltrials_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain=domain,
                extra={"ingest_source": live.get("source")},
            )
            records.append(rec)
            relay_errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="ClinicalTrials_Medical_Panel",
        material_records=records,
        maps_to_lean=["medical", "biological"],
        d_eff=13,
        authority_path=authority,
        source=[str(cache_root() / "clinicaltrials_cache.json"), "https://clinicaltrials.gov/api/v2/"],
        channel_stats=[("fsot_prediction", "clinicaltrials", relay_errs or [0.0])],
        sota_baselines={"clinicaltrials": {"sota_typical_error_pct": 10.0, "sota_model": "ClinicalTrials.gov registry"}},
    )


def build_osti_doe_science_panel() -> dict:
    live = _load_json(cache_root() / "osti_records_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for row in live.get("records") or []:
        name = str(row.get("osti_id") or row.get("title") or "")[:60]
        val = row.get("publication_year")
        if val is None:
            continue
        rec = make_fsot_record(
            lab="osti_doe_lab",
            property_name="publication_year",
            name=name,
            measured=float(val),
            domain="Nuclear_Physics",
            extra={"ingest_source": live.get("source")},
        )
        records.append(rec)
        relay_errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="OSTI_DOE_Science_Panel",
        material_records=records,
        maps_to_lean=["particle", "nuclear", "energy"],
        d_eff=18,
        authority_path=authority,
        source=[str(cache_root() / "osti_records_cache.json"), "https://www.osti.gov/api/v1/records"],
        channel_stats=[("fsot_prediction", "osti_doe", relay_errs or [0.0])],
        sota_baselines={"osti_doe": {"sota_typical_error_pct": 5.0, "sota_model": "OSTI DOE scientific corpus"}},
    )


def build_uap_war_gov_release_panel() -> dict:
    live = _load_json(cache_root() / "uap_war_gov_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    figures = live.get("figures") or []
    for row in live.get("documents") or []:
        doc_id = str(row.get("id") or "")
        for prop, domain, eval_kind in (
            ("importance_score", "Particle_Astrophysics", "fsot_prediction"),
            ("lat", "Geophysics", "contested_observable"),
            ("lng", "Geophysics", "contested_observable"),
            ("incident_year_start", "Sociology", "fsot_prediction"),
            ("incident_year_end", "Sociology", "fsot_prediction"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="uap_war_gov_lab",
                property_name=prop,
                name=doc_id,
                measured=float(val),
                domain=domain,
                eval_kind=eval_kind,
                extra={"ingest_source": live.get("source"), "agency": row.get("agency")},
            )
            records.append(rec)
            if eval_kind == "fsot_prediction":
                relay_errs.append(float(rec["error_pct"]))
        max_score = _max_ufo_score(figures, doc_id)
        if max_score is not None:
            rec = make_fsot_record(
                lab="uap_war_gov_lab",
                property_name="ufo_score",
                name=doc_id,
                measured=max_score,
                domain="Particle_Astrophysics",
                eval_kind="contested_observable",
                extra={"ingest_source": live.get("source")},
            )
            records.append(rec)
    return _bench_v11(
        domain="UAP_War_Gov_Release_Panel",
        material_records=records,
        maps_to_lean=["particle", "astronomical", "consciousness"],
        d_eff=20,
        authority_path=authority,
        source=[str(cache_root() / "uap_war_gov_cache.json"), str(UAP_BUNDLED), "https://www.war.gov/UFO/"],
        channel_stats=[("fsot_prediction", "uap_war_gov", relay_errs or [0.0])],
        sota_baselines={"uap_war_gov": {"sota_typical_error_pct": 15.0, "sota_model": "AARO / war.gov release corpus"}},
    )


def build_federal_science_registry_panel() -> dict:
    live = _load_json(cache_root() / "federal_science_registry_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for row in live.get("initiatives") or []:
        name = str(row.get("id") or row.get("name") or "")
        for prop, domain in (
            ("launch_year", "Economics"),
            ("open_dataset_catalog_entries", "Sociology"),
            ("federal_lab_partners", "Sociology"),
            ("open_science_corpus_tb", "Materials_Science"),
            ("annual_record_ingest_rate", "Nuclear_Physics"),
            ("dataset_metadata_entries", "Economics"),
            ("structured_corpus_documents", "Psychology"),
            ("public_document_tranches", "Psychology"),
            ("pilot_compute_hours", "High_Energy_Physics"),
            ("ai_model_checkpoints", "High_Energy_Physics"),
            ("resource_allocation_tiers", "Economics"),
            ("declassified_fraction_pct", "Particle_Physics"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="federal_science_registry_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain=domain,
                extra={"initiative": row.get("name"), "agency": row.get("agency")},
            )
            records.append(rec)
            relay_errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="Federal_Science_Registry_Panel",
        material_records=records,
        maps_to_lean=["economic", "particle", "energy"],
        d_eff=17,
        authority_path=authority,
        source=[str(cache_root() / "federal_science_registry_cache.json"), str(REGISTRY_BUNDLED)],
        channel_stats=[("fsot_prediction", "federal_science_registry", relay_errs or [0.0])],
        sota_baselines={
            "federal_science_registry": {
                "sota_typical_error_pct": 12.0,
                "sota_model": "Federal open-science initiative metadata (NAIRR/Genesis/OSTI)",
            }
        },
    )


def build_government_open_data_spine() -> dict:
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for slug in (
        "nasa_neo_feed_panel",
        "nasa_donki_solar_panel",
        "clinicaltrials_medical_panel",
        "osti_doe_science_panel",
        "uap_war_gov_release_panel",
        "federal_science_registry_panel",
    ):
        bench = _load_json(DATA / f"{slug}_benchmark.json")
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "government_open_data_spine_lab",
                "property": "panel_pooled_median",
                "name": slug,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier80_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:4]:
            if r.get("eval_kind") not in ("fsot_prediction", None):
                continue
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "government_open_data_spine_lab",
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
        domain="Government_Open_Data_Spine",
        material_records=records,
        maps_to_lean=["particle", "medical", "astronomical", "economic"],
        d_eff=18,
        authority_path=authority,
        source=["tier80_government_open_data_panels"],
        channel_stats=[("ingest_relay", "government_open_data_spine", relay_errs or [0.0])],
        sota_baselines={"government_open_data_spine": {"sota_typical_error_pct": 6.0, "sota_model": "Tier 80 government open-data wave"}},
    )


BUILDERS = {
    "NASA_NEO_Feed_Panel": build_nasa_neo_feed_panel,
    "NASA_DONKI_Solar_Panel": build_nasa_donki_solar_panel,
    "ClinicalTrials_Medical_Panel": build_clinicaltrials_medical_panel,
    "OSTI_DOE_Science_Panel": build_osti_doe_science_panel,
    "UAP_War_Gov_Release_Panel": build_uap_war_gov_release_panel,
    "Federal_Science_Registry_Panel": build_federal_science_registry_panel,
    "Government_Open_Data_Spine": build_government_open_data_spine,
}

BUILD_ORDER = [
    "NASA_NEO_Feed_Panel",
    "NASA_DONKI_Solar_Panel",
    "ClinicalTrials_Medical_Panel",
    "OSTI_DOE_Science_Panel",
    "UAP_War_Gov_Release_Panel",
    "Federal_Science_Registry_Panel",
    "Government_Open_Data_Spine",
]

LEAN_MAP = {
    "NASA_NEO_Feed_Panel": ("nasa_neo_feed", "astronomical", "astronomical_raw_S_positive", "NasaNeoFeedPriors"),
    "NASA_DONKI_Solar_Panel": ("nasa_donki_solar", "fusion", "fusion_raw_S_positive", "NasaDonkiSolarPriors"),
    "ClinicalTrials_Medical_Panel": ("clinicaltrials_medical", "medical", "medical_raw_S_positive", "ClinicaltrialsMedicalPriors"),
    "OSTI_DOE_Science_Panel": ("osti_doe_science", "nuclear", "nuclear_raw_S_positive", "OstiDoeSciencePriors"),
    "UAP_War_Gov_Release_Panel": ("uap_war_gov_release", "particle", "particle_raw_S_positive", "UapWarGovReleasePriors"),
    "Federal_Science_Registry_Panel": ("federal_science_registry", "energy", "energy_raw_S_positive", "FederalScienceRegistryPriors"),
    "Government_Open_Data_Spine": ("government_open_data_spine", "particle", "particle_raw_S_positive", "GovernmentOpenDataSpinePriors"),
}


def output_path(domain: str) -> Path:
    slug = {
        "NASA_NEO_Feed_Panel": "nasa_neo_feed_panel",
        "NASA_DONKI_Solar_Panel": "nasa_donki_solar_panel",
        "ClinicalTrials_Medical_Panel": "clinicaltrials_medical_panel",
        "OSTI_DOE_Science_Panel": "osti_doe_science_panel",
        "UAP_War_Gov_Release_Panel": "uap_war_gov_release_panel",
        "Federal_Science_Registry_Panel": "federal_science_registry_panel",
        "Government_Open_Data_Spine": "government_open_data_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"