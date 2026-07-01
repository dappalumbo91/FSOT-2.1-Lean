#!/usr/bin/env python3
"""Bridge Desktop thesis simulation lab → wave + intrinsic screen observables."""

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
MANIFEST_PATH = ROOT / "data" / "thesis_simulation_manifest.yaml"
OUTPUT = ROOT / "data" / "thesis_simulation_benchmark.json"


def _load_wave_targets(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    targets = data.get("targets") or {}
    if not isinstance(targets, dict):
        return []
    out: list[dict] = []
    for key, row in targets.items():
        if not isinstance(row, dict):
            continue
        sigma = row.get("sigma_percent")
        try:
            sigma_f = float(sigma) if sigma is not None and str(sigma).strip() != "" else None
        except (TypeError, ValueError):
            sigma_f = None
        out.append(
            {
                "id": key,
                "name": row.get("name") or key,
                "category": row.get("category"),
                "measured": row.get("measured"),
                "unit": row.get("unit"),
                "sigma_percent": sigma_f,
            }
        )
    return out


def _load_intrinsic_screens(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    out: list[dict] = []
    for row in data:
        if not isinstance(row, dict):
            continue
        entry = {"source_file": path.name, "name": row.get("name")}
        for key in ("rmse", "mae", "r2"):
            val = row.get(key)
            if val is not None:
                try:
                    entry[key] = float(val)
                except (TypeError, ValueError):
                    pass
        out.append(entry)
    return out


def build_benchmark(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    thesis_root = Path(spec["source"]["thesis_root"])

    wave_records: list[dict] = []
    wave_by_file: dict[str, int] = {}
    for rel in spec["source"]["wave_observations"]:
        path = thesis_root / rel
        if not path.exists():
            print(f"WARN: missing wave file {path}", file=sys.stderr)
            continue
        rows = _load_wave_targets(path)
        wave_by_file[rel] = len(rows)
        for row in rows:
            row["wave_file"] = rel
            wave_records.append(row)

    intrinsic_records: list[dict] = []
    intrinsic_by_file: dict[str, int] = {}
    for rel in spec["source"]["intrinsic_screens"]:
        path = thesis_root / rel
        if not path.exists():
            print(f"WARN: missing intrinsic file {path}", file=sys.stderr)
            continue
        rows = _load_intrinsic_screens(path)
        intrinsic_by_file[rel] = len(rows)
        intrinsic_records.extend(rows)

    rmses = [r["rmse"] for r in intrinsic_records if r.get("rmse") is not None]
    r2s = [r["r2"] for r in intrinsic_records if r.get("r2") is not None]
    best_rmse = min(rmses) if rmses else None
    best_r2 = max(r2s) if r2s else None

    lab_cfg_path = thesis_root / spec["source"].get("lab_config", "wave7_lab_config.json")
    lab_config_present = lab_cfg_path.exists()

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(thesis_root),
        "wave_file_count": len(wave_by_file),
        "wave_target_count": len(wave_records),
        "wave_by_file": wave_by_file,
        "intrinsic_screen_count": len(intrinsic_records),
        "intrinsic_by_file": intrinsic_by_file,
        "intrinsic_best_rmse": best_rmse,
        "intrinsic_best_r2": best_r2,
        "lab_config_present": lab_config_present,
        "observable_count": len(wave_records) + len(intrinsic_records),
        "wave_observables": wave_records,
        "intrinsic_screens": intrinsic_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = build_benchmark(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  wave targets: {bench['wave_target_count']}  "
        f"intrinsic screens: {bench['intrinsic_screen_count']}  "
        f"best_rmse: {bench.get('intrinsic_best_rmse')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())