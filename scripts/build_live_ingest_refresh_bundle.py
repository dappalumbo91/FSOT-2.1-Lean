#!/usr/bin/env python3
"""Orchestrate live catalog ingest (Gaia, GWOSC, NASA NEO) + benchmark regen."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "live_ingest_refresh_report.json"

STEPS = [
    ("Gaia DR3 + WDS", ["scripts/ingest_tier62_live_astrometry.py"]),
    ("GWOSC events", ["scripts/ingest_tier58_live_catalogs.py"]),
    ("NASA NEO / government open data", ["scripts/ingest_tier80_government_open_data.py", "--deep"]),
    ("Tier 68 live ingest", ["scripts/ingest_tier68_live_ingest.py"]),
    ("Rebuild tier68 benchmarks", ["scripts/build_tier68_live_ingest_benchmarks.py"]),
    ("Refresh contested closure", ["scripts/build_contested_observables_closure.py"]),
    ("Refresh domain navigator", ["scripts/build_fsot_domain_navigator_db.py"]),
]


def main() -> int:
    results: list[dict] = []
    for label, args in STEPS:
        cmd = [sys.executable, str(ROOT / args[0]), *args[1:]]
        try:
            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=300)
            ok = r.returncode == 0
            tail = (r.stdout or r.stderr or "")[-400:]
        except Exception as exc:
            ok = False
            tail = str(exc)
        results.append({"step": label, "ok": ok, "tail": tail})
        print(f"{'OK' if ok else 'FAIL'} — {label}")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "steps": results,
        "all_ok": all(r["ok"] for r in results),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())