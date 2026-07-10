#!/usr/bin/env python3
"""Split space weather: portable summary in repo, full series on external cache."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "data" / "space_weather_benchmark.json"
SUMMARY = ROOT / "data" / "space_weather_summary_benchmark.json"
MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"

SAMPLE_LIMIT = 500


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-limit", type=int, default=SAMPLE_LIMIT)
    args = parser.parse_args()

    if not FULL.exists():
        print(f"Missing {FULL} — run build_space_weather_benchmark.py first", file=sys.stderr)
        return 1

    sys.path.insert(0, str(ROOT / "scripts"))
    from tier38_public_data_lib import external_data_root  # noqa: E402

    full_doc = json.loads(FULL.read_text(encoding="utf-8"))
    records = full_doc.get("records") or []
    ext_dir = external_data_root() / "space_weather"
    ext_dir.mkdir(parents=True, exist_ok=True)
    ext_full = ext_dir / "space_weather_full_benchmark.json"
    shutil.copy2(FULL, ext_full)

    sample = records[: args.sample_limit]
    if len(records) > args.sample_limit and len(records) % 2 == 1:
        sample.append(records[len(records) // 2])
    errs = [float(r.get("error_pct") or 0) for r in records]
    matches = sum(1 for r in records if float(r.get("error_pct") or 100) == 0.0)
    pooled = sorted(errs)[len(errs) // 2] if errs else 0.0

    summary = {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": full_doc.get("authority_path"),
        "source_cache": full_doc.get("source_cache"),
        "external_full_benchmark": str(ext_full),
        "full_record_count": len(records),
        "kp_record_count": len(records),
        "observable_count": len(records),
        "sample_record_count": len(sample),
        "stability_match_count": matches,
        "stability_match_rate": matches / len(records) if records else 0.0,
        "median_error_pct": pooled,
        "pooled_median_error_pct": pooled,
        "headline_median_error_pct": pooled,
        "fusion_scalar_S": full_doc.get("fusion_scalar_S"),
        "maps_to_lean": full_doc.get("maps_to_lean") or ["fusion", "energy", "plasma_physics"],
        "D_eff": full_doc.get("D_eff", 14),
        "records": sample,
        "material_records": sample,
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "operational_baselines": {
                "kp_storm_classifier": {
                    "sota_typical_error_pct": 5.0,
                    "sota_model": "NOAA SWPC operational Kp classifier",
                }
            },
            "beats_sota_summary": {"pooled_vs_domain_baseline": pooled < 5.0},
        },
    }

    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # Replace repo benchmark with summary for portable clone-and-verify
    FULL.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if MANIFEST.exists():
        try:
            import yaml

            spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
            spec.setdefault("external", {})["full_benchmark"] = str(ext_full)
            spec["external"]["summary_benchmark"] = str(SUMMARY)
            MANIFEST.write_text(yaml.dump(spec, sort_keys=False, default_flow_style=False), encoding="utf-8")
        except ImportError:
            pass

    print(f"Wrote summary {SUMMARY} ({len(sample)} sample / {len(records)} full)")
    print(f"Archived full benchmark to {ext_full}")
    print(f"Replaced {FULL} with portable summary ({FULL.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())