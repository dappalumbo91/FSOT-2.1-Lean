#!/usr/bin/env python3
"""Trinary-OS FSOTB round-trip rebuild smoke from vendor ISA + fixtures."""

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
MANIFEST = ROOT / "data" / "trinary_os_round_trip_manifest.yaml"
OUTPUT = ROOT / "data" / "trinary_os_round_trip_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import rel_repo_path, trinary_os_isa_registry_path, trinary_os_root  # noqa: E402
from trinary_os_round_trip import summarize_round_trip  # noqa: E402


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    os_root = trinary_os_root()
    isa_path = trinary_os_isa_registry_path()
    ver = spec.get("verification") or {}
    summary = summarize_round_trip(os_root, isa_path)
    constants = summary["constants"]
    records: list[dict] = []

    for row in summary["program_checks"]:
        for field in ("file_size", "instructions"):
            expected = row.get(f"expected_{field}")
            live = row.get(f"live_{field}")
            err = 0.0 if live == expected else 100.0
            records.append(
                {
                    "lab": "trinary_os_round_trip",
                    "property": f"{row['program']}_{field}",
                    "abi_tier": row.get("abi_tier"),
                    "computed": live,
                    "measured": expected,
                    "error_pct": err,
                }
            )
        blob_size = row.get("blob_file_size")
        expected_size = row.get("expected_file_size")
        if blob_size is not None and expected_size is not None:
            records.append(
                {
                    "lab": "trinary_os_round_trip",
                    "property": f"{row['program']}_blob_size",
                    "abi_tier": row.get("abi_tier"),
                    "computed": blob_size,
                    "measured": expected_size,
                    "error_pct": 0.0 if blob_size == expected_size else 100.0,
                }
            )
        records.append(
            {
                "lab": "trinary_os_round_trip",
                "property": f"{row['program']}_round_trip_byte_identical",
                "abi_tier": row.get("abi_tier"),
                "computed": 1 if row.get("round_trip_identical") else 0,
                "measured": 1,
                "error_pct": 0.0 if row.get("round_trip_identical") else 100.0,
            }
        )
        records.append(
            {
                "lab": "trinary_os_round_trip",
                "property": f"{row['program']}_mnemonic_registry_coverage",
                "abi_tier": row.get("abi_tier"),
                "computed": 1 if row.get("mnemonic_registry_coverage") else 0,
                "measured": 1,
                "error_pct": 0.0 if row.get("mnemonic_registry_coverage") else 100.0,
            }
        )
        if row.get("panel_S_hex") and ver.get("panel_S_hex"):
            records.append(
                {
                    "lab": "trinary_os_round_trip",
                    "property": f"{row['program']}_panel_S_hex",
                    "computed": row.get("panel_S_hex"),
                    "measured": ver.get("panel_S_hex"),
                    "error_pct": 0.0
                    if str(row.get("panel_S_hex")) == str(ver.get("panel_S_hex"))
                    else 100.0,
                }
            )

    for name, live, expected in [
        ("seeds_hash_hex", constants.get("seeds_hash_hex"), ver.get("seeds_hash_hex")),
        ("word_width_trits", 27, ver.get("trit_word_width")),
        ("num_task_slots", constants.get("num_task_slots"), ver.get("num_task_slots")),
        ("opcode_count", summary.get("opcode_count"), ver.get("opcode_count")),
    ]:
        if expected is None:
            continue
        if isinstance(expected, str):
            err = 0.0 if str(live) == str(expected) else 100.0
        else:
            err = 0.0 if live == expected else 100.0
        records.append(
            {
                "lab": "trinary_os_round_trip",
                "property": name,
                "computed": live,
                "measured": expected,
                "error_pct": err,
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(isa_path), rel_repo_path(os_root)],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
        "opcode_count": summary.get("opcode_count"),
        "program_count": len(summary.get("program_checks") or []),
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
    print(
        f"  records: {doc['record_count']}  programs: {doc['program_count']}  "
        f"median_err: {doc['median_error_pct']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())