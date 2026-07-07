#!/usr/bin/env python3
"""Trinary-OS portable vendor bundle — FSOTB oracles + derived ISA constants."""

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
MANIFEST = ROOT / "data" / "trinary_os_portable_manifest.yaml"
OUTPUT = ROOT / "data" / "trinary_os_portable_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import REPO_ROOT, rel_repo_path, trinary_os_root  # noqa: E402
from trinary_os_invariants import derived_os_constants, load_fsotb_oracles  # noqa: E402


def _resolve(raw: str) -> Path:
    path = Path(raw)
    return REPO_ROOT / path if not path.is_absolute() else path


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    os_root = trinary_os_root()
    trinary_manifest = _resolve(spec["source"]["trinary_os_manifest"])
    trinary_spec = yaml.safe_load(trinary_manifest.read_text(encoding="utf-8"))
    ver = trinary_spec.get("verification") or {}
    oracles = load_fsotb_oracles(os_root, trinary_spec["artifacts"]["oracles"])
    constants = derived_os_constants()
    records: list[dict] = []

    hash_checks = [
        ("seeds_hash_hex", oracles.get("hello", {}).get("seeds_hash_hex"), ver.get("seeds_hash_hex")),
        ("panel_S_hex", oracles.get("hello", {}).get("panel_S_hex"), ver.get("panel_S_hex")),
    ]
    for name, live, expected in hash_checks:
        err = 0.0 if str(live) == str(expected) else 100.0
        records.append(
            {
                "lab": "trinary_os_portable",
                "property": name,
                "computed": live,
                "measured": expected,
                "error_pct": err,
            }
        )

    size_checks = (
        ("hello", "hello_file_size"),
        ("call_ret", "call_ret_file_size"),
        ("spawn_join", "spawn_join_file_size"),
    )
    for key, ver_key in size_checks:
        live = oracles.get(key, {}).get("file_size")
        expected = ver.get(ver_key)
        err = 0.0 if live == expected else 100.0
        records.append(
            {
                "lab": "trinary_os_portable",
                "property": ver_key,
                "computed": live,
                "measured": expected,
                "error_pct": err,
            }
        )

    for name in ("num_task_slots", "trit_word_width", "cortical_layers"):
        live = constants.get(name)
        expected = ver.get(name)
        err = 0.0 if live == expected else 100.0
        records.append(
            {
                "lab": "trinary_os_portable",
                "property": name,
                "computed": live,
                "measured": expected,
                "error_pct": err,
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(os_root), rel_repo_path(trinary_manifest)],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
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
    print(f"  records: {doc['record_count']}  oracles: {doc['oracle_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())