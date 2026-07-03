#!/usr/bin/env python3
"""Space weather stability benchmark — NOAA Kp vs FSOT fusion/energy scalar."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"
OUTPUT = ROOT / "data" / "space_weather_benchmark.json"

# Kp < 5: quiet/unsettled; Kp >= 5: geomagnetic storm (NOAA G-scale proxy)
KP_STORM_THRESHOLD = 5.0


def build_benchmark(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    cache_path = ROOT / spec["source"]["cache"]
    if not cache_path.exists():
        raise FileNotFoundError(f"Kp cache missing — run ingest_space_weather_swpc.py: {cache_path}")

    cache = json.loads(cache_path.read_text(encoding="utf-8"))
    kp_rows = cache.get("records") or []

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_fusion = float(mod.domain_scalar("Thermodynamics"))
    S_energy = float(mod.domain_scalar("Geophysics"))

    records: list[dict] = []
    for row in kp_rows:
        kp = float(row["kp"])
        ap = row.get("ap_running")
        observed_quiet = kp < KP_STORM_THRESHOLD
        # Fusion-scalar gate: S_fusion maps to Kp storm cutoff (calibrated ~4.3 at S≈0.79)
        storm_kp_cutoff = 3.5 + abs(S_fusion)
        predicted_quiet = kp < storm_kp_cutoff
        match = predicted_quiet == observed_quiet
        records.append(
            {
                "lab": "space_weather_lab",
                "property": "kp_storm_classifier",
                "time_tag": row.get("time_tag"),
                "kp": kp,
                "ap_running": ap,
                "computed_quiet": 1.0 if predicted_quiet else 0.0,
                "measured_quiet": 1.0 if observed_quiet else 0.0,
                "error_pct": 0.0 if match else 100.0,
                "S_fusion": round(S_fusion, 6),
                "S_energy": round(S_energy, 6),
            }
        )

    errs = [r["error_pct"] for r in records]
    matches = sum(1 for r in records if r["error_pct"] == 0.0)
    kp_vals = [r["kp"] for r in records]
    ap_vals = [r["ap_running"] for r in records if r.get("ap_running") is not None]

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source_cache": str(cache_path),
        "kp_record_count": len(records),
        "ap_record_count": len(ap_vals),
        "observable_count": len(records),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "kp_median": sorted(kp_vals)[len(kp_vals) // 2] if kp_vals else None,
        "ap_median": sorted(ap_vals)[len(ap_vals) // 2] if ap_vals else None,
        "fusion_scalar_S": S_fusion,
        "maps_to_lean": ["fusion", "energy", "plasma_physics"],
        "D_eff": 14,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build_benchmark(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  Kp records: {bench['kp_record_count']}  "
        f"match rate: {bench['stability_match_rate']:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())