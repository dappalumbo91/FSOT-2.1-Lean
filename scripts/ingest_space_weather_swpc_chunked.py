#!/usr/bin/env python3
"""
Chunked GFZ Kp/ap historical ingest — stream Kp_ap_since_1932.txt by year.

Checkpoint/resume via space_weather_cache/ingest_state.json.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from space_weather_gfz_lab import (  # noqa: E402
    chunk_key,
    chunk_path,
    load_manifest,
    load_state,
    save_state,
    stream_gfz_rows,
    write_year_chunk,
)

MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"


def ingest(
    *,
    manifest_path: Path = MANIFEST,
    start_year: int | None = None,
    end_year: int | None = None,
    force: bool = False,
) -> dict:
    spec = load_manifest(manifest_path)
    hist = spec.get("historical") or {}
    cache = spec.get("cache") or {}
    cache_root = ROOT / cache.get("root", "data/space_weather_cache")
    state_path = ROOT / cache.get("state_file", "data/space_weather_cache/ingest_state.json")
    y0 = start_year or int(hist.get("start_year", 2018))
    y1 = end_year or int(hist.get("end_year", 2024))
    url = hist.get("gfz_kp_url")

    state = load_state(state_path)
    completed = set(state.get("completed_chunks") or [])
    failed = set(state.get("failed_chunks") or [])
    pending_years = [
        year
        for year in range(y0, y1 + 1)
        if force or chunk_key(year) not in completed or not chunk_path(cache_root, year).exists()
    ]
    if not pending_years:
        print(f"All year chunks present for {y0}–{y1}")
        return {
            "processed_years": [],
            "completed_total": len(completed),
            "failed_total": len(failed),
            "year_range": [y0, y1],
            "skipped": True,
        }

    buffers: dict[int, list[dict]] = {year: [] for year in pending_years}
    processed_years: set[int] = set()
    pending_set = set(pending_years)

    for row in stream_gfz_rows(url):
        year = int(row["time_tag"][:4])
        if year not in pending_set:
            continue
        buffers[year].append(row)

    for year in pending_years:
        key = chunk_key(year)
        out = chunk_path(cache_root, year)
        if not force and key in completed and out.exists():
            continue
        records = buffers.get(year) or []
        if not records:
            failed.add(key)
            print(f"  FAIL {key}: no rows in stream")
            continue
        try:
            write_year_chunk(out, year, records)
            completed.add(key)
            failed.discard(key)
            processed_years.add(year)
            print(f"  OK {key} records={len(records)}", flush=True)
        except Exception as exc:
            failed.add(key)
            print(f"  FAIL {key}: {exc}", flush=True)

    state["completed_chunks"] = sorted(completed)
    state["failed_chunks"] = sorted(failed)
    state["year_range"] = [y0, y1]
    state["source_url"] = url
    save_state(state_path, state)

    return {
        "processed_years": sorted(processed_years),
        "completed_total": len(completed),
        "failed_total": len(failed),
        "year_range": [y0, y1],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--start-year", type=int, default=None)
    parser.add_argument("--end-year", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = ingest(
        manifest_path=args.manifest,
        start_year=args.start_year,
        end_year=args.end_year,
        force=args.force,
    )
    print(
        f"Chunked ingest done: years={result['year_range']} "
        f"processed={len(result['processed_years'])} "
        f"completed={result['completed_total']} failed={result['failed_total']}"
    )
    return 0 if result["failed_total"] == 0 or result["processed_years"] else 1


if __name__ == "__main__":
    raise SystemExit(main())