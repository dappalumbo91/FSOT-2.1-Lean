#!/usr/bin/env python3
"""Ingest open, no-credential scientific sources into vendor/open_science/."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from open_science_sources_lib import (  # noqa: E402
    OPEN_SOURCES,
    fetch_source,
    open_sources_manifest,
    vendor_dir,
)

OUT_SUMMARY = ROOT / "data" / "open_science_ingest_report.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest open scientific sources (no credentials)")
    parser.add_argument("--only", nargs="*", help="Optional source ids to ingest")
    args = parser.parse_args()

    wanted = set(args.only) if args.only else None
    results = []
    ok = 0
    fail = 0
    for src in OPEN_SOURCES:
        if wanted and src.id not in wanted:
            continue
        try:
            doc = fetch_source(src)
            path = vendor_dir(src.id) / "live.json"
            path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
            results.append(
                {
                    "source_id": src.id,
                    "status": "ok",
                    "path": str(path.relative_to(ROOT)),
                    "family": src.family,
                    "auth": "none",
                }
            )
            ok += 1
            print(f"OK  {src.id}")
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "source_id": src.id,
                    "status": "fail",
                    "error": f"{type(exc).__name__}: {exc}"[:400],
                    "family": src.family,
                    "auth": "none",
                }
            )
            fail += 1
            print(f"FAIL {src.id}: {exc}")

    manifest = open_sources_manifest()
    (ROOT / "data" / "open_science_sources_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "no_signup_no_credentials",
        "ok_count": ok,
        "fail_count": fail,
        "results": results,
    }
    OUT_SUMMARY.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_SUMMARY} ({ok} ok / {fail} fail)")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
