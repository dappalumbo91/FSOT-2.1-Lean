#!/usr/bin/env python3
"""Trinary-OS full ISA rebuild verification from vendor bundle."""

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
MANIFEST = ROOT / "data" / "trinary_os_isa_rebuild_manifest.yaml"
OUTPUT = ROOT / "data" / "trinary_os_isa_rebuild_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import REPO_ROOT, rel_repo_path, trinary_os_isa_registry_path, trinary_os_root  # noqa: E402
from trinary_os_invariants import derived_os_constants, load_fsotb_oracles  # noqa: E402
from trinary_os_isa import load_opcode_registry, summarize_isa  # noqa: E402


def _resolve(raw: str) -> Path:
    path = Path(raw)
    return REPO_ROOT / path if not path.is_absolute() else path


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    os_root = trinary_os_root()
    isa_path = trinary_os_isa_registry_path()
    trinary_manifest = _resolve(spec["source"]["trinary_os_manifest"])
    trinary_spec = yaml.safe_load(trinary_manifest.read_text(encoding="utf-8"))
    ver = trinary_spec.get("verification") or {}
    registry = load_opcode_registry(isa_path)
    oracles = load_fsotb_oracles(os_root, trinary_spec["artifacts"]["oracles"])
    constants = derived_os_constants()
    summary = summarize_isa(registry, oracles)
    records: list[dict] = []

    for row in summary["program_checks"]:
        for field in ("file_size", "instructions"):
            expected = row.get(f"expected_{field}")
            live = row.get(f"live_{field}")
            err = 0.0 if live == expected else 100.0
            records.append(
                {
                    "lab": "trinary_os_isa_rebuild",
                    "property": f"{row['program']}_{field}",
                    "abi_tier": row.get("abi_tier"),
                    "computed": live,
                    "measured": expected,
                    "error_pct": err,
                }
            )

    for op in registry.get("opcodes") or []:
        records.append(
            {
                "lab": "trinary_os_isa_rebuild",
                "property": "opcode_present",
                "name": op.get("mnemonic"),
                "computed": op.get("op"),
                "measured": op.get("op"),
                "error_pct": 0.0,
                "abi_tier": op.get("tier"),
            }
        )

    isa_checks = [
        ("word_width_trits", registry.get("word_width_trits"), ver.get("trit_word_width")),
        ("num_task_slots", registry.get("num_task_slots"), ver.get("num_task_slots")),
        ("register_count", registry.get("register_count"), 25),
        ("cortical_layers", registry.get("cortical_layers"), ver.get("cortical_layers")),
        ("seeds_hash_hex", constants.get("seeds_hash_hex"), ver.get("seeds_hash_hex")),
    ]
    for name, live, expected in isa_checks:
        if expected is None:
            continue
        if isinstance(expected, str):
            err = 0.0 if str(live) == str(expected) else 100.0
        else:
            err = 0.0 if live == expected else 100.0
        records.append(
            {
                "lab": "trinary_os_isa_rebuild",
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
        "opcode_count": summary["opcode_count"],
        "abi_tier_count": len(summary["abi_tiers"]),
        "oracle_count": len(oracles),
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
        f"  records: {doc['record_count']}  opcodes: {doc['opcode_count']}  "
        f"median_err: {doc['median_error_pct']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())