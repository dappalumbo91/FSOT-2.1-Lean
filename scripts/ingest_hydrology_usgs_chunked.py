#!/usr/bin/env python3
"""Chunked USGS NWIS daily streamflow ingest — one station-year at a time."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hydrology_usgs_lab import (  # noqa: E402
    MANIFEST_PATH,
    chunk_key,
    chunk_path,
    fetch_station_year,
    load_manifest,
    load_state,
    save_state,
    write_chunk,
)


def ingest(
    *,
    manifest_path: Path,
    start_year: int | None = None,
    end_year: int | None = None,
    max_chunks: int = 0,
) -> dict:
    spec = load_manifest(manifest_path)
    cache_root = ROOT / spec["cache"]["root"]
    state_path = ROOT / spec["cache"]["state_file"]
    stations = [s["id"] for s in spec.get("stations") or []]
    y0 = start_year or int(spec["ingest"]["start_year"])
    y1 = end_year or int(spec["ingest"]["end_year"])
    base_url = spec["source"]["base_url"]
    param = spec["source"].get("parameter_cd", "00060")

    state = load_state(state_path)
    completed = set(state.get("completed_chunks") or [])
    failed = set(state.get("failed_chunks") or [])
    processed = 0

    for year in range(y0, y1 + 1):
        for station_id in stations:
            key = chunk_key(station_id, year)
            out = chunk_path(cache_root, station_id, year)
            if key in completed and out.exists():
                continue
            if max_chunks > 0 and processed >= max_chunks:
                break
            try:
                monthly = fetch_station_year(
                    station_id,
                    year,
                    base_url=base_url,
                    parameter_cd=param,
                )
                if not monthly:
                    failed.add(key)
                    print(f"  FAIL {key}: empty series")
                    continue
                write_chunk(out, station_id, year, monthly)
                completed.add(key)
                failed.discard(key)
                processed += 1
                print(f"  OK {key} months={len(monthly)}", flush=True)
            except Exception as exc:
                failed.add(key)
                print(f"  FAIL {key}: {exc}", flush=True)
            time.sleep(0.15)
        if max_chunks > 0 and processed >= max_chunks:
            break

    state["completed_chunks"] = sorted(completed)
    state["failed_chunks"] = sorted(failed)
    state["stations"] = stations
    state["year_range"] = [y0, y1]
    save_state(state_path, state)

    return {
        "processed": processed,
        "completed_total": len(completed),
        "failed_total": len(failed),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--start-year", type=int, default=None)
    parser.add_argument("--end-year", type=int, default=None)
    parser.add_argument("--max-chunks", type=int, default=0)
    args = parser.parse_args()
    result = ingest(
        manifest_path=args.manifest,
        start_year=args.start_year,
        end_year=args.end_year,
        max_chunks=args.max_chunks,
    )
    print(
        f"Chunked hydrology ingest: processed={result['processed']} "
        f"completed={result['completed_total']} failed={result['failed_total']}"
    )
    return 0 if result["failed_total"] == 0 or result["processed"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())