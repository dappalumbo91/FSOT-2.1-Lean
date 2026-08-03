#!/usr/bin/env python3
"""Ingest public MAST observation metadata (optional size-capped image products)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mast_astroquery_lib import ingest_mast_bundle, mast_available  # noqa: E402

REPORT = ROOT / "data" / "mast_astroquery_ingest_report.json"


def main() -> int:
    p = argparse.ArgumentParser(description="MAST public ingest via astroquery (no login)")
    p.add_argument("--object", default="M1", help="Target name (default M1 / Crab)")
    p.add_argument("--collection", default="HST", help="MAST obs_collection (default HST)")
    p.add_argument("--max-obs", type=int, default=5)
    p.add_argument(
        "--download",
        action="store_true",
        help="Also download a size-capped SCIENCE product set (default off)",
    )
    p.add_argument("--max-download-mb", type=float, default=15.0)
    args = p.parse_args()

    ok, msg = mast_available()
    if not ok:
        print(f"FAIL mast unavailable: {msg}")
        print("Install: pip install astroquery astropy")
        REPORT.write_text(
            json.dumps(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "status": "fail",
                    "error": msg,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return 1

    try:
        bundle = ingest_mast_bundle(
            objectname=args.object,
            obs_collection=args.collection,
            max_obs=args.max_obs,
            download=args.download,
            max_download_mb=args.max_download_mb,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL ingest: {exc}")
        REPORT.write_text(
            json.dumps(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "status": "fail",
                    "error": f"{type(exc).__name__}: {exc}"[:500],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return 1

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "auth": "none_public",
        "object": args.object,
        "collection": args.collection,
        "query_rows_total": bundle.get("query_rows_total"),
        "returned": bundle.get("returned"),
        "path": bundle.get("path"),
        "download": bundle.get("download"),
        "docs": bundle.get("docs"),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"OK MAST {args.collection}/{args.object} rows={bundle.get('query_rows_total')} saved={bundle.get('path')}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
