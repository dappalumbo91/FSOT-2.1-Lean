#!/usr/bin/env python3
"""Linguistics formal — measured anchors + FSOT derivation error bridge."""

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
MANIFEST = ROOT / "data" / "linguistics_formal_manifest.yaml"
OUTPUT = ROOT / "data" / "linguistics_formal_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import REPO_ROOT, linguistics_root  # noqa: E402
from linguistics_targets import (  # noqa: E402
    load_derivations_db,
    load_derivations_json,
    load_targets_csv,
    merge_targets,
)


def _resolve(raw: str) -> Path:
    path = Path(raw)
    return REPO_ROOT / path if not path.is_absolute() else path


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    root = linguistics_root() or _resolve(spec["source"]["linguistics_root"])
    csv_path = root / spec["source"]["targets_csv"]
    json_path = root / spec["source"]["derivations_json"]
    db_path = root / "db" / "linguistics.db"
    derivations = load_derivations_json(json_path)
    if not derivations and db_path.exists():
        derivations = load_derivations_db(db_path)
    rows = merge_targets(load_targets_csv(csv_path), derivations)
    records: list[dict] = []
    for row in rows:
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "linguistics_formal_lab",
                "name": row.get("name"),
                "group": row.get("group"),
                "measured": row.get("measured"),
                "computed": row.get("computed"),
                "error_pct": float(err),
                "unit": row.get("unit"),
                "formula": row.get("formula"),
            }
        )
    errs = sorted(abs(r["error_pct"]) for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(csv_path), str(db_path)],
        "maps_to_lean": ["consciousness", "neural"],
        "D_eff": 12,
        "record_count": len(records),
        "observable_count": len(records),
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