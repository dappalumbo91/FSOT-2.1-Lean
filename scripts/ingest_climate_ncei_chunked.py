#!/usr/bin/env python3
"""
Chunked NOAA NCEI GHCND ingest — one year file at a time, station-filtered streaming.

Does not load full national dataset into memory. Checkpoint/resume via ingest_state.json.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from climate_ncei_lab import (  # noqa: E402
    MANIFEST_PATH,
    chunk_key,
    chunk_path,
    fetch_cdo_year_chunk,
    load_manifest,
    load_state,
    process_year_chunk,
    save_state,
    write_chunk,
)


def ingest(
    *,
    manifest_path: Path,
    start_year: int | None = None,
    end_year: int | None = None,
    max_chunks: int = 0,
    use_cdo_api: bool = False,
    dry_run: bool = False,
) -> dict:
    spec = load_manifest(manifest_path)
    cache = spec["cache"]
    cache_root = ROOT / cache["root"]
    chunks_dir = ROOT / cache["chunks_dir"]
    state_path = ROOT / cache["state_file"]
    stations = [s["id"] for s in spec.get("stations") or []]
    station_set = set(stations)
    elements = set(spec.get("ingest", {}).get("elements") or ["TMAX", "TMIN", "TAVG", "PRCP"])
    y0 = start_year or int(spec["ingest"]["start_year"])
    y1 = end_year or int(spec["ingest"]["end_year"])
    base_url = spec.get("source", {}).get("base_url", "") + "/{year}.csv.gz"
    token = os.environ.get(spec.get("source", {}).get("api_fallback", {}).get("token_env", "NOAA_TOKEN") or "")

    state = load_state(state_path)
    completed = set(state.get("completed_chunks") or [])
    failed = set(state.get("failed_chunks") or [])
    processed = 0
    skipped = 0

    for year in range(y0, y1 + 1):
        pending = [
            sid
            for sid in stations
            if chunk_key(sid, year) not in completed or not chunk_path(cache_root, sid, year).exists()
        ]
        if not pending:
            skipped += len(stations)
            continue
        if max_chunks > 0 and processed >= max_chunks:
            break

        year_data: dict[str, dict] = {}
        if dry_run:
            for station_id in pending:
                print(f"  would ingest {chunk_key(station_id, year)}")
            continue

        try:
            if use_cdo_api and token:
                for station_id in pending:
                    year_data[station_id] = fetch_cdo_year_chunk(
                        station_id, year, token, list(elements & {"TMAX", "TMIN", "TAVG", "PRCP"})
                    )
            else:
                year_data = process_year_chunk(year, station_set, elements, base_url)
        except Exception as exc:
            for station_id in pending:
                key = chunk_key(station_id, year)
                failed.add(key)
                print(f"  FAIL {key}: {exc}")
            continue

        for station_id in pending:
            if max_chunks > 0 and processed >= max_chunks:
                break
            key = chunk_key(station_id, year)
            out = chunk_path(cache_root, station_id, year)
            try:
                monthly = year_data.get(station_id) or {}
                write_chunk(out, station_id, year, monthly)
                completed.add(key)
                failed.discard(key)
                processed += 1
                print(f"  OK {key} months={len(monthly)}", flush=True)
            except Exception as exc:
                failed.add(key)
                print(f"  FAIL {key}: {exc}", flush=True)
        state["completed_chunks"] = sorted(completed)
        state["failed_chunks"] = sorted(failed)
        state["stations"] = stations
        state["year_range"] = [y0, y1]
        save_state(state_path, state)
        time.sleep(0.1)

    return {
        "processed": processed,
        "skipped": skipped,
        "completed_total": len(completed),
        "failed_total": len(failed),
        "chunks_dir": str(chunks_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Chunked NOAA NCEI GHCND ingest")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--start-year", type=int, default=None)
    parser.add_argument("--end-year", type=int, default=None)
    parser.add_argument("--max-chunks", type=int, default=0, help="0 = all pending")
    parser.add_argument("--use-cdo-api", action="store_true", help="Use NOAA CDO API if NOAA_TOKEN set")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    summary = ingest(
        manifest_path=args.manifest,
        start_year=args.start_year,
        end_year=args.end_year,
        max_chunks=args.max_chunks,
        use_cdo_api=args.use_cdo_api,
        dry_run=args.dry_run,
    )
    print("=== NCEI chunked ingest ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    return 0 if summary.get("failed_total", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())