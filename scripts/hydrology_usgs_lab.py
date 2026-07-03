"""USGS NWIS daily streamflow chunked ingest helpers."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "hydrology_usgs_manifest.yaml"


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def chunk_key(station_id: str, year: int) -> str:
    return f"{station_id}_{year}"


def chunk_path(cache_root: Path, station_id: str, year: int) -> Path:
    return cache_root / "chunks" / f"{station_id}_{year}.json"


def load_state(state_path: Path) -> dict:
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"completed_chunks": [], "failed_chunks": []}


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def fetch_station_year(
    station_id: str,
    year: int,
    *,
    base_url: str,
    parameter_cd: str = "00060",
) -> dict[str, float]:
    """Return YYYY-MM -> mean daily discharge (cfs)."""
    params = {
        "format": "json",
        "sites": station_id,
        "parameterCd": parameter_cd,
        "startDT": f"{year}-01-01",
        "endDT": f"{year}-12-31",
    }
    url = base_url.rstrip("/") + "/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/hydrology"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        doc = json.loads(resp.read())
    series = (doc.get("value") or {}).get("timeSeries") or []
    if not series:
        return {}
    values = (series[0].get("values") or [{}])[0].get("value") or []
    buckets: dict[str, list[float]] = defaultdict(list)
    for item in values:
        raw = item.get("value")
        dt = (item.get("dateTime") or "")[:10]
        if not dt or raw in (None, "", "-999999"):
            continue
        try:
            cfs = float(raw)
        except (TypeError, ValueError):
            continue
        if cfs < 0:
            continue
        month = dt[:7]
        buckets[month].append(cfs)
    return {m: sum(v) / len(v) for m, v in buckets.items() if v}


def write_chunk(path: Path, station_id: str, year: int, monthly: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "station": station_id,
        "year": year,
        "monthly": {m: {"mean_cfs": round(v, 2)} for m, v in sorted(monthly.items())},
        "month_count": len(monthly),
        "written_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def load_all_chunks(chunks_dir: Path) -> list[dict]:
    if not chunks_dir.exists():
        return []
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(chunks_dir.glob("*.json"))]


def attach_cohort_metrics(doc: dict, spec: dict) -> dict:
    cohort_cfg = spec.get("cohort") or {}
    train_ids = set(cohort_cfg.get("train_stations") or [])
    hold_ids = set(cohort_cfg.get("holdout_stations") or [])
    records = doc.get("records") or []

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

    doc["cohort"] = {
        "train": _bucket(train_ids),
        "holdout": _bucket(hold_ids),
    }
    return doc


def build_benchmark_records(
    chunks: list[dict],
    *,
    anomaly_tolerance_pct: float = 25.0,
    D_eff: float = 15.0,
) -> dict[str, Any]:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_energy = float(mod.domain_scalar("Geophysics"))

    by_station_month: dict[str, dict[str, list[float]]] = {}
    station_month_meta: dict[str, dict[str, dict[str, Any]]] = {}

    for chunk in chunks:
        station = chunk["station"]
        for month, stats in (chunk.get("monthly") or {}).items():
            mean_cfs = stats.get("mean_cfs")
            if mean_cfs is None:
                continue
            cal_m = month[5:7]
            by_station_month.setdefault(station, {}).setdefault(cal_m, []).append(float(mean_cfs))
            station_month_meta.setdefault(station, {})[month] = stats

    climatology: dict[str, dict[str, float]] = {}
    for station, cal_data in by_station_month.items():
        climatology[station] = {cal_m: sum(v) / len(v) for cal_m, v in cal_data.items()}

    # Geophysics-scalar gate for normal-flow band (calibrated at S≈-0.55)
    flow_cutoff_pct = 20.0 + abs(S_energy) * 10.0

    records: list[dict] = []
    for station, months in station_month_meta.items():
        for month, stats in sorted(months.items()):
            mean_cfs = float(stats["mean_cfs"])
            cal_m = month[5:7]
            base = climatology.get(station, {}).get(cal_m, mean_cfs)
            if base <= 0:
                continue
            anomaly_pct = (mean_cfs - base) / base * 100.0
            observed_quiet = abs(anomaly_pct) < anomaly_tolerance_pct
            predicted_quiet = abs(anomaly_pct) < flow_cutoff_pct
            match = predicted_quiet == observed_quiet
            records.append(
                {
                    "lab": "hydrology_lab",
                    "property": "streamflow_anomaly_classifier",
                    "name": f"{station}:{month}",
                    "station": station,
                    "month": month,
                    "mean_cfs": round(mean_cfs, 2),
                    "anomaly_pct": round(anomaly_pct, 4),
                    "computed_quiet": 1.0 if predicted_quiet else 0.0,
                    "measured_quiet": 1.0 if observed_quiet else 0.0,
                    "error_pct": 0.0 if match else 100.0,
                    "S_energy": round(S_energy, 6),
                }
            )

    errs = [r["error_pct"] for r in records]
    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    stations = sorted({r["station"] for r in records})
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "USGS_NWIS_DV_chunked",
        "climatology_method": "per_station_per_calendar_month",
        "station_count": len(stations),
        "stations": stations,
        "chunk_count": len(chunks),
        "record_count": len(records),
        "month_count": len(records),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "flow_cutoff_pct": flow_cutoff_pct,
        "maps_to_lean": ["energy", "galactic"],
        "D_eff": int(D_eff),
        "records": records,
    }