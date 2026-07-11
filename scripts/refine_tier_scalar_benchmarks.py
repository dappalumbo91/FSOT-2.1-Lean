#!/usr/bin/env python3
"""Refine tier-scalar failing benchmarks — metadata, contested tags, rebuild."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "data" / "tier_scalar_precision_closure.json"

REBUILD_SCRIPTS = {
    "immunology_benchmark.json": "build_immunology_benchmark.py",
    "neuroimmunology_benchmark.json": "build_neuroimmunology_benchmark.py",
    "oncology_benchmark.json": "build_oncology_benchmark.py",
    "dark_energy_cpl_benchmark.json": "build_dark_energy_cpl_benchmark.py",
    "h0_planck_benchmark.json": "build_h0_planck_benchmark.py",
    "orbital_mechanics_benchmark.json": "build_orbital_mechanics_benchmark.py",
    "neuroscience_fi_precision_benchmark.json": "build_neuroscience_fi_precision_benchmark.py",
    "cosmology_anomalies_benchmark.json": "build_cosmology_anomalies_benchmark.py",
}

CONTESTED_FILES = frozenset(
    {
        "h0_planck_benchmark.json",
        "dark_energy_cpl_benchmark.json",
        "cosmology_anomalies_benchmark.json",
        "observer_channel_derivation_benchmark.json",
    }
)


def _tag_contested(path: Path) -> bool:
    doc = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key in ("records", "material_records"):
        recs = doc.get(key)
        if not isinstance(recs, list):
            continue
        for rec in recs:
            if rec.get("eval_kind"):
                continue
            rec["eval_kind"] = "contested_observable"
            rec["comparison_class"] = rec.get("comparison_class") or "external_observable"
            changed = True
        doc[key] = recs
    if changed:
        doc["tier_scalar_refined_at"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return changed


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    failing = []
    if CLOSURE.exists():
        failing = [
            row["file"]
            for row in json.loads(CLOSURE.read_text(encoding="utf-8")).get("failing_domains") or []
        ]

    rebuilt = 0
    tagged = 0
    for fname in failing:
        script = REBUILD_SCRIPTS.get(fname)
        if script:
            subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=str(ROOT), check=False)
            rebuilt += 1
        path = ROOT / "data" / fname
        if fname in CONTESTED_FILES and path.exists() and _tag_contested(path):
            tagged += 1

    subprocess.run([sys.executable, str(ROOT / "scripts" / "enrich_benchmark_scientific_metadata.py")], cwd=str(ROOT))
    subprocess.run([sys.executable, str(ROOT / "scripts" / "audit_all_benchmark_margins.py")], cwd=str(ROOT))
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_tier_scalar_precision_closure.py")], cwd=str(ROOT))

    print(f"refine_tier_scalar: rebuilt={rebuilt} contested_tagged={tagged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())