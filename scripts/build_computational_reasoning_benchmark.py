#!/usr/bin/env python3
"""Computational reasoning — FIC scalar sweep oracle + trinary-OS invariants."""

from __future__ import annotations

import argparse
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
MANIFEST = ROOT / "data" / "computational_reasoning_manifest.yaml"
OUTPUT = ROOT / "data" / "computational_reasoning_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fic_lab import run_single  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from fsot_paths import REPO_ROOT  # noqa: E402
from trinary_os_invariants import derived_os_constants  # noqa: E402


def _resolve(raw: str) -> Path:
    path = Path(raw)
    return REPO_ROOT / path if not path.is_absolute() else path


def _fic_records(sweep_path: Path) -> list[dict]:
    mod, _ = load_fsot_compute()
    records: list[dict] = []
    with sweep_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            live = run_single(
                mod,
                D_eff=int(row["D_eff"]),
                delta_psi=float(row["delta_psi"]),
                recent_hits=int(row["recent_hits"]),
                observed=True,
            )
            observed = float(row["S_final"])
            predicted = float(live["S_final"])
            err = abs(predicted - observed) / abs(observed) * 100.0 if observed else 0.0
            records.append(
                {
                    "lab": "fic_intelligence_compressor",
                    "property": "S_final",
                    "D_eff": int(row["D_eff"]),
                    "delta_psi": float(row["delta_psi"]),
                    "recent_hits": int(row["recent_hits"]),
                    "computed": predicted,
                    "measured": observed,
                    "error_pct": err,
                    "fertile": row.get("fertile") == "True",
                    "intelligence_score": float(row.get("intelligence_score") or 0),
                }
            )
    return records


def _trinary_records(manifest_path: Path) -> list[dict]:
    if yaml is None or not manifest_path.exists():
        return []
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = spec.get("verification") or {}
    constants = derived_os_constants()
    records: list[dict] = []
    checks = [
        ("seeds_hash_hex", constants.get("seeds_hash_hex"), ver.get("seeds_hash_hex")),
        ("panel_S_hex", constants.get("panel_S_hex"), ver.get("panel_S_hex")),
        ("num_task_slots", constants.get("num_task_slots"), ver.get("num_task_slots")),
        ("trit_word_width", constants.get("trit_word_width"), ver.get("trit_word_width")),
        ("cortical_layers", constants.get("cortical_layers"), ver.get("cortical_layers")),
    ]
    for name, live, expected in checks:
        if expected is None or live is None:
            continue
        if isinstance(expected, str):
            err = 0.0 if str(live) == str(expected) else 100.0
        else:
            err = abs(float(live) - float(expected)) / max(abs(float(expected)), 1e-12) * 100.0
        records.append(
            {
                "lab": "trinary_os_lab",
                "property": name,
                "computed": live,
                "measured": expected,
                "error_pct": err,
            }
        )
    return records


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    sweep_path = _resolve(spec["source"]["fic_sweep_csv"])
    manifest_path = _resolve(spec["source"]["trinary_os_manifest"])
    records = _fic_records(sweep_path) + _trinary_records(manifest_path)
    errs = sorted(r["error_pct"] for r in records)
    fertile = sum(1 for r in records if r.get("fertile"))
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(sweep_path), str(manifest_path)],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
        "record_count": len(records),
        "observable_count": len(records),
        "fic_sweep_rows": len(records) - len(_trinary_records(manifest_path)),
        "fertile_rows": fertile,
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())