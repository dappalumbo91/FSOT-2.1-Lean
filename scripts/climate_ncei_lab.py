"""NOAA NCEI GHCND chunked ingest helpers — stream year files, aggregate monthly."""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "climate_ncei_manifest.yaml"

GHCND_BY_YEAR = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/{year}.csv.gz"
CDO_API = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"


@dataclass
class MonthAgg:
    tmax_sum: float = 0.0
    tmin_sum: float = 0.0
    tavg_sum: float = 0.0
    prcp_sum: float = 0.0
    tmax_n: int = 0
    tmin_n: int = 0
    tavg_n: int = 0
    prcp_n: int = 0

    def ingest(self, element: str, value: int) -> None:
        if value == -9999:
            return
        if element == "TMAX":
            self.tmax_sum += value / 10.0
            self.tmax_n += 1
        elif element == "TMIN":
            self.tmin_sum += value / 10.0
            self.tmin_n += 1
        elif element == "TAVG":
            self.tavg_sum += value / 10.0
            self.tavg_n += 1
        elif element == "PRCP":
            self.prcp_sum += value / 10.0
            self.prcp_n += 1

    def to_dict(self) -> dict[str, Any]:
        tmax = self.tmax_sum / self.tmax_n if self.tmax_n else None
        tmin = self.tmin_sum / self.tmin_n if self.tmin_n else None
        tavg = self.tavg_sum / self.tavg_n if self.tavg_n else None
        if tavg is None and tmax is not None and tmin is not None:
            tavg = (tmax + tmin) / 2.0
        prcp = self.prcp_sum / self.prcp_n if self.prcp_n else 0.0
        return {
            "tmax_mean_c": tmax,
            "tmin_mean_c": tmin,
            "tavg_mean_c": tavg,
            "prcp_mm": prcp,
            "days_tmax": self.tmax_n,
            "days_tmin": self.tmin_n,
        }


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def chunk_path(cache_root: Path, station_id: str, year: int) -> Path:
    return cache_root / "chunks" / f"{station_id}_{year}.json"


def chunk_key(station_id: str, year: int) -> str:
    return f"{station_id}_{year}"


def load_state(state_path: Path) -> dict:
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"completed_chunks": [], "failed_chunks": []}


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def stream_ghcnd_year(year: int, station_ids: set[str], base_url: str | None = None) -> Iterator[tuple[str, str, str, int]]:
    """Yield (station, date_yyyymmdd, element, value) for target stations only."""
    url = (base_url or GHCND_BY_YEAR).format(year=year)
    with urllib.request.urlopen(url, timeout=120) as resp:
        with gzip.open(resp, "rt", encoding="utf-8", errors="replace") as gz:
            for line in gz:
                parts = line.strip().split(",")
                if len(parts) < 4:
                    continue
                station, date, element, raw = parts[0], parts[1], parts[2], parts[3]
                if station not in station_ids:
                    continue
                try:
                    value = int(raw)
                except ValueError:
                    continue
                yield station, date, element, value


def process_year_chunk(
    year: int,
    station_ids: set[str],
    elements: set[str],
    base_url: str | None = None,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Return {station_id: {YYYY-MM: month_stats}} for one year."""
    buckets: dict[str, dict[str, MonthAgg]] = {}
    for station, date, element, value in stream_ghcnd_year(year, station_ids, base_url):
        if element not in elements:
            continue
        month = f"{date[:4]}-{date[4:6]}"
        buckets.setdefault(station, {}).setdefault(month, MonthAgg()).ingest(element, value)
    return {
        station: {m: agg.to_dict() for m, agg in months.items()}
        for station, months in buckets.items()
    }


def write_chunk(path: Path, station_id: str, year: int, monthly: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "station": station_id,
        "year": year,
        "source": "NOAA_NCEI_GHCND_by_year",
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "monthly": monthly,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def fetch_cdo_year_chunk(
    station_id: str,
    year: int,
    token: str,
    elements: list[str],
) -> dict[str, dict[str, Any]]:
    """Optional NOAA CDO API path (paginated) when NOAA_TOKEN is set."""
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("requests required for CDO API") from exc

    buckets: dict[str, MonthAgg] = {}
    offset = 1
    limit = 1000
    headers = {"token": token}
    while True:
        params = {
            "datasetid": "GHCND",
            "stationid": f"GHCND:{station_id}",
            "startdate": f"{year}-01-01",
            "enddate": f"{year}-12-31",
            "datatypeid": ",".join(elements),
            "units": "metric",
            "limit": limit,
            "offset": offset,
        }
        resp = requests.get(CDO_API, params=params, headers=headers, timeout=60)
        resp.raise_for_status()
        doc = resp.json()
        results = doc.get("results") or []
        if not results:
            break
        for row in results:
            date = (row.get("date") or "")[:10].replace("-", "")
            element = row.get("datatype") or ""
            value = row.get("value")
            if not date or value is None:
                continue
            # CDO metric: TMAX/TMIN already °C*10 or similar; normalize
            el = element.replace("GHCND_", "") if element.startswith("GHCND_") else element
            if el not in elements:
                continue
            month = f"{date[:4]}-{date[4:6]}"
            ival = int(round(float(value) * 10)) if el in ("TMAX", "TMIN", "TAVG") else int(float(value) * 10)
            buckets.setdefault(month, MonthAgg()).ingest(el, ival)
        offset += limit
        if offset > int(doc.get("metadata", {}).get("resultset", {}).get("count", 0)):
            break
        time.sleep(0.2)
    return {m: agg.to_dict() for m, agg in buckets.items()}


def load_all_chunks(chunks_dir: Path) -> list[dict]:
    chunks: list[dict] = []
    if not chunks_dir.exists():
        return chunks
    for path in sorted(chunks_dir.glob("*.json")):
        chunks.append(json.loads(path.read_text(encoding="utf-8")))
    return chunks


def build_benchmark_records(
    chunks: list[dict],
    *,
    anomaly_tolerance_c: float = 2.5,
    D_eff: float = 16.0,
) -> dict[str, Any]:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from weather_fsot_scalar import compute_S_D_chaotic, map_to_fsot_params  # noqa: E402

    # station -> cal_month -> list of tavg observations
    by_station_month: dict[str, dict[str, list[float]]] = {}
    station_month_meta: dict[str, dict[str, dict[str, Any]]] = {}

    for chunk in chunks:
        station = chunk["station"]
        for month, stats in (chunk.get("monthly") or {}).items():
            tavg = stats.get("tavg_mean_c")
            if tavg is None:
                continue
            cal_m = month[5:7]
            by_station_month.setdefault(station, {}).setdefault(cal_m, []).append(float(tavg))
            station_month_meta.setdefault(station, {})[month] = stats

    climatology: dict[str, dict[str, float]] = {}
    for station, cal_data in by_station_month.items():
        climatology[station] = {cal_m: sum(v) / len(v) for cal_m, v in cal_data.items()}

    records: list[dict] = []
    for station, months in station_month_meta.items():
        for month, stats in sorted(months.items()):
            tavg = stats.get("tavg_mean_c")
            if tavg is None:
                continue
            cal_m = month[5:7]
            base = climatology.get(station, {}).get(cal_m, tavg)
            anomaly = float(tavg) - base
            prcp = float(stats.get("prcp_mm") or 0.0)
            params = map_to_fsot_params(1013.25, 5.0, prcp, observed=True)
            params["D_eff"] = D_eff
            S = compute_S_D_chaotic(params)
            predicted_stable = S > 0
            observed_stable = abs(anomaly) < anomaly_tolerance_c
            match = predicted_stable == observed_stable
            records.append(
                {
                    "lab": "climate_lab",
                    "property": "ncei_ghcnd_monthly_temp_anomaly_stability",
                    "name": f"{station}:{month}",
                    "station": station,
                    "month": month,
                    "computed": 1.0 if predicted_stable else 0.0,
                    "measured": 1.0 if observed_stable else 0.0,
                    "error_pct": 0.0 if match else 100.0,
                    "anomaly_c": round(anomaly, 4),
                    "tavg_c": round(float(tavg), 4),
                    "prcp_mm": round(prcp, 2),
                    "S": round(S, 6),
                }
            )

    errs = [r["error_pct"] for r in records]
    stations = sorted({r["station"] for r in records})
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "NOAA_NCEI_GHCND_by_year_chunked",
        "climatology_method": "per_station_per_calendar_month",
        "station_count": len(stations),
        "stations": stations,
        "chunk_count": len(chunks),
        "record_count": len(records),
        "month_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def cohort_split_metrics(
    records: list[dict],
    train_stations: set[str],
    holdout_stations: set[str],
) -> dict[str, Any]:
    """Train/holdout station cohort metrics for climate generalization gates."""

    def _bucket(ids: set[str]) -> dict[str, Any]:
        subset = [r for r in records if r.get("station") in ids]
        errs = [float(r["error_pct"]) for r in subset if r.get("error_pct") is not None]
        active = sorted({r["station"] for r in subset})
        return {
            "stations": active,
            "station_count": len(active),
            "record_count": len(subset),
            "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        }

    return {
        "train": _bucket(train_stations),
        "holdout": _bucket(holdout_stations),
    }


def attach_cohort_metrics(doc: dict, manifest: dict) -> dict:
    cohort = manifest.get("cohort") or {}
    train = set(cohort.get("train_stations") or [])
    holdout = set(cohort.get("holdout_stations") or [])
    if not train or not holdout:
        return doc
    metrics = cohort_split_metrics(doc.get("records") or [], train, holdout)
    doc["cohort"] = {
        **metrics,
        "holdout_median_error_max_pct": float(cohort.get("holdout_median_error_max_pct", 5.0)),
        "holdout_min_records": int(cohort.get("holdout_min_records", 200)),
        "train_station_ids": sorted(train),
        "holdout_station_ids": sorted(holdout),
    }
    return doc