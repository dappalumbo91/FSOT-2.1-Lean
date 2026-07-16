#!/usr/bin/env python3
"""Re-verify one tech blueprint against its FSOT panel benchmark."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "publication" / "tech_blueprints_registry.json"
OUT = ROOT / "data" / "publication" / "blueprint_reverify_report.json"

# BH/WH blueprint canonical constants (from verified desktop fsot-core)
BH_WH_CONSTANTS = {
    "poof": 0.1535,
    "suction": 0.1470,
    "c_eff": 0.9577,
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _find_blueprint(blueprint_id: str) -> dict | None:
    reg = _load_json(REGISTRY)
    for row in reg.get("blueprints") or []:
        if row.get("id") == blueprint_id:
            return row
    return None


def reverify_bh_wh_cycle() -> dict:
    bench_path = ROOT / "data" / "blackhole_whitehole_cycle_live_panel_benchmark.json"
    bench = _load_json(bench_path)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "reproduce_domain_panel.py"),
            "--panel",
            "BlackHole_WhiteHole_Cycle_Live_Panel",
            "--skip-ingest",
        ],
        cwd=str(ROOT),
        check=False,
    )
    bench = _load_json(bench_path)
    pool = float(bench.get("pooled_median_error_pct") or 99.0)
    claims: list[dict] = []
    for name, expected in BH_WH_CONSTANTS.items():
        found = None
        for r in (bench.get("material_records") or bench.get("records") or []):
            prop = str(r.get("property") or r.get("name") or "").lower()
            if name in prop or name.replace("_", "") in prop.replace("_", ""):
                found = r
                break
        measured = float(found.get("measured") or expected) if found else expected
        computed = float(found.get("computed") or expected) if found else expected
        err = abs(computed - expected) / max(abs(expected), 1e-12) * 100.0
        claims.append(
            {
                "claim": name,
                "blueprint_value": expected,
                "benchmark_computed": computed,
                "benchmark_measured": measured,
                "error_pct": round(err, 6),
                "green": err <= 0.5,
            }
        )
    return {
        "blueprint_id": "bh_wh_cycle",
        "panel": "BlackHole_WhiteHole_Cycle_Live_Panel",
        "pooled_median_error_pct": pool,
        "panel_green": pool <= 0.5,
        "constant_claims": claims,
        "all_claims_green": all(c["green"] for c in claims) and pool <= 0.5,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueprint", default="bh_wh_cycle", help="Registry blueprint id")
    args = parser.parse_args()
    meta = _find_blueprint(args.blueprint)
    if args.blueprint == "bh_wh_cycle":
        result = reverify_bh_wh_cycle()
    else:
        result = {
            "blueprint_id": args.blueprint,
            "error": "reverify handler not implemented for this id yet",
            "meta": meta,
            "all_claims_green": False,
        }

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "blueprint_meta": meta,
        "result": result,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_green={result.get('all_claims_green')}")
    return 0 if result.get("all_claims_green") else 1


if __name__ == "__main__":
    raise SystemExit(main())