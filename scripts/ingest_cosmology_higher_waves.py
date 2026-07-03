#!/usr/bin/env python3
"""Ingest fsot_compute waves 5–10 into lab_registry."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_higher_waves_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from cosmology_waves import summarize_waves, wave_observables  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    src = spec["source"]
    compute_path = Path(src["cosmology_root"]) / src["fsot_compute"]
    mod = load_fsot_compute(compute_path)
    wave_nums = [int(w) for w in src["waves"]]
    rows: list[dict] = []
    for n in wave_nums:
        rows.extend(wave_observables(mod, n))
    summary = summarize_waves(rows, wave_nums)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["cosmology_higher_waves_lab"] = {
        **summary,
        "waves": wave_nums,
        "rows": rows,
        "compute_path": str(compute_path),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  waves 5–10 observables: {summary['observable_count']}  max_err: {summary['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())