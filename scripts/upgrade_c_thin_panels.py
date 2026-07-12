#!/usr/bin/env python3
"""Upgrade C_thin extension panels toward B_verified via ingests, rebuilds, and depth relay."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
OUT = ROOT / "data" / "c_thin_upgrade_report.json"

sys.path.insert(0, str(ROOT / "scripts"))
from c_thin_depth_lib import _is_c_thin, _tier, deepen_all_c_thin  # noqa: E402
from tier_gap_fill_lib import _load_json  # noqa: E402


def _collect_thin(ext: dict) -> list[dict]:
    thin: list[dict] = []
    for name, cfg in ext.items():
        bench_path = ROOT / cfg["benchmark_data"]
        if not bench_path.exists():
            continue
        bench = _load_json(bench_path)
        rec = int(bench.get("record_count") or bench.get("observable_count") or 0)
        med = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        if _is_c_thin(bench):
            thin.append(
                {
                    "panel": name,
                    "records": rec,
                    "median_error_pct": med,
                    "ingest_script": cfg.get("ingest_script"),
                    "build_script": cfg.get("build_script"),
                }
            )
    return thin


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")

    import os

    os.environ.setdefault("FSOT_API_MEGA_DEEP", "1")
    for key in (
        "FSOT_TIER38_DEEP",
        "FSOT_TIER60_DEEP",
        "FSOT_TIER62_DEEP",
        "FSOT_TIER68_DEEP",
        "FSOT_TIER79_DEEP",
        "FSOT_TIER80_DEEP",
        "FSOT_TIER81_DEEP",
        "FSOT_TIER82_DEEP",
        "FSOT_TIER84_DEEP",
        "FSOT_TIER85_DEEP",
        "FSOT_TIER86_DEEP",
        "FSOT_TIER87_DEEP",
        "FSOT_TIER88_DEEP",
    ):
        os.environ[key] = "1"

    ext = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")).get("extension_domains") or {}
    thin_before = _collect_thin(ext)
    py = sys.executable
    actions: list[dict] = []

    ingest_scripts = sorted({row["ingest_script"] for row in thin_before if row.get("ingest_script")})
    for script in ingest_scripts:
        cmd = [py, str(ROOT / script), "--deep"]
        rc = subprocess.call(cmd, cwd=ROOT)
        actions.append({"ingest_script": script, "exit_code": rc})

    build_scripts = sorted({row["build_script"] for row in thin_before if row.get("build_script")})
    for script in build_scripts:
        cmd = [py, str(ROOT / script), "--skip-ingest"]
        rc = subprocess.call(cmd, cwd=ROOT)
        actions.append({"build_script": script, "exit_code": rc})

    depth_results = deepen_all_c_thin(ext)
    actions.append({"depth_pass_panels": len(depth_results)})

    subprocess.call([py, str(ROOT / "scripts" / "gen_extension_domains_lean.py")], cwd=ROOT)
    subprocess.call([py, str(ROOT / "scripts" / "sync_core_formula_fractal_branches.py")], cwd=ROOT)
    subprocess.call([py, str(ROOT / "scripts" / "build_scientific_domain_expansion_map.py")], cwd=ROOT)
    subprocess.call([py, str(ROOT / "scripts" / "verify_extension_domains.py")], cwd=ROOT)

    thin_after = _collect_thin(ext)
    promoted = []
    for row in thin_before:
        cfg = ext[row["panel"]]
        bench = _load_json(ROOT / cfg["benchmark_data"])
        rec = int(bench.get("record_count") or 0)
        med = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        tier_after = _tier(float(med) if med is not None else None, rec)
        promoted.append({**row, "records_after": rec, "median_after": med, "tier_after": tier_after})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "c_thin_before": len(thin_before),
        "c_thin_after": len(thin_after),
        "promoted_to_B": sum(1 for r in promoted if r["tier_after"] == "B_verified"),
        "promoted_to_A": sum(1 for r in promoted if r["tier_after"] == "A_strong"),
        "c_thin_panels": promoted,
        "depth_results": depth_results,
        "actions": actions,
        "still_thin": [r["panel"] for r in promoted if r["tier_after"] == "C_thin"],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"C_thin upgrade: {report['c_thin_before']} before → {report['c_thin_after']} after "
        f"({report['promoted_to_B']} → B, {report['promoted_to_A']} → A)"
    )
    if report["still_thin"]:
        print(f"  still thin ({len(report['still_thin'])}): {', '.join(report['still_thin'][:8])}...")
    print(f"Wrote {OUT}")
    return 0 if report["c_thin_after"] == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())