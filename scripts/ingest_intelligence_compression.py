#!/usr/bin/env python3
"""Ingest FIC sensitivity sweep into lab_registry (Tier 11)."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "intelligence_compression_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fic_lab import summarize_sweep  # noqa: E402


def load_sweep_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    csv_path = ROOT / manifest["artifacts"]["fic_sensitivity_sweep"]["path"]
    if not csv_path.exists():
        sweep_script = ROOT / manifest["artifacts"]["fic_simulation"]["sweep_script"]
        import subprocess

        proc = subprocess.run([sys.executable, str(sweep_script)], check=False)
        if proc.returncode != 0:
            return proc.returncode

    rows = load_sweep_rows(csv_path)
    for row in rows:
        row["S_final"] = float(row["S_final"])
        row["fertile"] = row["fertile"].lower() in ("true", "1", "yes")
        row["intelligence_score"] = float(row["intelligence_score"])
        row["compression_ratio"] = float(row["compression_ratio"])
        row["fidelity_proxy"] = float(row["fidelity_proxy"])
        row["D_eff"] = int(row["D_eff"])
        row["recent_hits"] = int(row["recent_hits"])
        row["delta_psi"] = float(row["delta_psi"])

    summary = summarize_sweep(rows)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["intelligence_compression"] = {
        **summary,
        "sweep_rows": rows[:32],
        "sweep_row_count_full": len(rows),
        "source_repo": manifest["source_repo"],
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  sweep_rows: {len(rows)}  fertile: {summary['fertile_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())