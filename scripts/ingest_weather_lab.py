#!/usr/bin/env python3
"""Ingest FSOT weather simulation log into lab_registry.json."""

from __future__ import annotations

import argparse
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


def ingest_weather(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["weather_root"])
    log_path = root / manifest["artifacts"]["sim_log"]["path"]
    rows = load_weather_log(log_path)
    return {"present": log_path.exists(), "log_path": str(log_path), **summarize_weather(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest weather sim log")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    weather = ingest_weather()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["weather_lab"] = weather
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  hours: {weather['hour_count']}  S_mean: {weather['S_mean']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())