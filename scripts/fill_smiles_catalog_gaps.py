#!/usr/bin/env python3
"""Fill 8 SMILES Lab catalog gaps from data/smiles_catalog_gaps.yaml."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
GAPS_PATH = ROOT / "data" / "smiles_catalog_gaps.yaml"
DEFAULT_SMILES_ROOT = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab")


def load_gaps() -> list[dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install PyYAML")
    payload = yaml.safe_load(GAPS_PATH.read_text(encoding="utf-8"))
    return payload.get("gaps", [])


def gap_key(rec: dict) -> tuple[str, str]:
    return rec["section"], rec["name"]


def build_gap_index(gaps: list[dict]) -> dict[tuple[str, str], dict]:
    return {gap_key(g): g for g in gaps}


def patch_json(json_path: Path, gap_index: dict[tuple[str, str], dict], dry_run: bool) -> int:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    patched = 0
    for rec in payload.get("records", []):
        key = (rec.get("section"), rec.get("name"))
        gap = gap_index.get(key)
        if not gap or rec.get("matched"):
            continue
        rec["target_value"] = gap["target_value"]
        rec["unit"] = gap.get("unit", rec.get("unit"))
        rec["source"] = gap.get("source", rec.get("source"))
        rec["fsot_formula"] = gap["fsot_formula"]
        rec["computed_value"] = gap["computed_value"]
        rec["error_pct"] = gap["error_pct"]
        rec["matched"] = gap["error_pct"] <= 5.0
        patched += 1

    meta = payload.setdefault("metadata", {})
    meta["catalog_gaps_filled"] = patched
    meta["catalog_gaps_filled_at"] = datetime.now(timezone.utc).isoformat()

    if not dry_run and patched:
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return patched


def patch_csv(csv_path: Path, gap_index: dict[tuple[str, str], dict], dry_run: bool) -> int:
    rows: list[dict[str, str]] = []
    patched = 0
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            key = (row.get("section"), row.get("name"))
            gap = gap_index.get(key)
            if gap and row.get("matched", "").lower() != "true":
                row["target_value"] = str(gap["target_value"])
                row["unit"] = gap.get("unit", row.get("unit", ""))
                row["fsot_formula"] = gap["fsot_formula"]
                row["computed_value"] = str(gap["computed_value"])
                row["error_pct"] = str(gap["error_pct"])
                row["matched"] = "True" if gap["error_pct"] <= 5.0 else "False"
                patched += 1
            rows.append(row)

    if not dry_run and patched:
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    return patched


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill SMILES catalog gaps")
    parser.add_argument("--smiles-root", type=Path, default=DEFAULT_SMILES_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    gaps = load_gaps()
    gap_index = build_gap_index(gaps)
    json_path = args.smiles_root / "FSOT_SMILES_Lab_Dataset.json"
    csv_path = args.smiles_root / "FSOT_SMILES_Lab_Dataset.csv"

    if not json_path.exists():
        raise SystemExit(f"SMILES dataset missing: {json_path}")

    n_json = patch_json(json_path, gap_index, args.dry_run)
    n_csv = patch_csv(csv_path, gap_index, args.dry_run) if csv_path.exists() else 0

    remaining = sum(
        1 for r in json.loads(json_path.read_text(encoding="utf-8"))["records"]
        if not r.get("matched") and gap_key(r) in gap_index
    )
    action = "Would patch" if args.dry_run else "Patched"
    if n_json == 0 and remaining == 0:
        print(f"Catalog gaps already resolved ({len(gaps)} definitions, 0 remaining)")
        return 0
    print(f"{action} {n_json} JSON records, {n_csv} CSV rows ({len(gaps)} gap definitions)")
    if remaining > 0:
        print(f"  WARN: {remaining} gap(s) still unmatched")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())