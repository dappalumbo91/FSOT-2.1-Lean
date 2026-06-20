#!/usr/bin/env python3
"""Verify FSOT weather scalar simulation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "weather_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from weather_lab import load_weather_log, summarize_weather  # noqa: E402


def verify_weather(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["weather_root"])
    log_path = root / manifest["artifacts"]["sim_log"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not log_path.exists():
        return [f"missing weather log: {log_path}"], {}

    live = summarize_weather(load_weather_log(log_path))
    if not registry.get("weather_lab"):
        issues.append("weather_lab: not ingested — run ingest_weather_lab.py")
    if live["hour_count"] < ver.get("hour_count_min", 24):
        issues.append(f"weather_lab: only {live['hour_count']} hours")
    expected_d = ver.get("D_eff", 15.0)
    if expected_d not in (live.get("D_eff_values") or []):
        issues.append(f"weather_lab: D_eff {live.get('D_eff_values')} missing {expected_d}")
    if live["positive_S_hours"] < ver.get("min_positive_S_hours", 24):
        issues.append(f"weather_lab: only {live['positive_S_hours']} positive-S hours")

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_weather()
    print("=== Weather Lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All weather Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())