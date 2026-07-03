#!/usr/bin/env python3
"""Split cosmology labs into per-wave registry entries (waves 4–10)."""

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
MANIFEST = ROOT / "data" / "cosmology_per_wave_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import summarize_lambda  # noqa: E402


def _wave_summary(rows: list[dict], wave_num: int) -> dict:
    tag = f"wave{wave_num}"
    wave_rows = [r for r in rows if r.get("wave") == tag]
    base = summarize_lambda(wave_rows)
    errs = [float(r["error_pct"]) for r in wave_rows if r.get("error_pct") is not None]
    return {
        "wave": wave_num,
        "observable_count": base["observable_count"],
        "measured_count": base["measured_count"],
        "max_error_pct": base["max_error_pct"],
        "mean_error_pct": base["mean_error_pct"],
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "rows": wave_rows,
    }


def _wave4_summary(registry: dict) -> dict:
    w4 = registry.get("cosmology_wave4") or {}
    rows = w4.get("rows") or []
    base = summarize_lambda(rows)
    errs = [float(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    return {
        "wave": 4,
        "observable_count": base["observable_count"],
        "measured_count": base["measured_count"],
        "max_error_pct": base["max_error_pct"],
        "mean_error_pct": base["mean_error_pct"],
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
    }


def ingest(registry_path: Path = REGISTRY) -> dict[int, dict]:
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    parent = registry.get("cosmology_higher_waves_lab") or {}
    rows = parent.get("rows") or []

    wave_nums = [4, 5, 6, 7, 8, 9, 10]
    if yaml and MANIFEST.exists():
        spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        wave_nums = [int(w) for w in (spec.get("source") or {}).get("waves") or wave_nums]

    summaries: dict[int, dict] = {}
    for n in wave_nums:
        if n == 4:
            summary = _wave4_summary(registry)
            if not summary.get("observable_count"):
                raise RuntimeError("cosmology_wave4 missing — run ingest_cosmology_wave4.py first")
            parent_lab = "cosmology_wave4"
        else:
            if not rows:
                raise RuntimeError("cosmology_higher_waves_lab missing — run ingest_cosmology_higher_waves.py first")
            summary = _wave_summary(rows, n)
            parent_lab = "cosmology_higher_waves_lab"
        key = f"cosmology_wave{n}_lab"
        registry[key] = {
            **{k: v for k, v in summary.items() if k != "rows"},
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "parent_lab": parent_lab,
        }
        summaries[n] = summary

    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return summaries


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    summaries = ingest(args.registry)
    print(f"Updated {args.registry}")
    for n, s in sorted(summaries.items()):
        print(f"  wave{n}: {s['observable_count']} observables  max_err={s['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())