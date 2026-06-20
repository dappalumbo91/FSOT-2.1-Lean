#!/usr/bin/env python3
"""Verify Fsot trinary OS FSOTB regression oracles and derived constants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "trinary_os_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from trinary_os_invariants import (  # noqa: E402
    derived_os_constants,
    load_fsotb_oracles,
    summarize_trinary_os,
)


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_trinary_os(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    fsot_os_root = Path(manifest["fsot_os_root"])
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not fsot_os_root.exists():
        return [f"missing trinary OS root: {fsot_os_root}"], {}

    oracles = load_fsotb_oracles(fsot_os_root, manifest["artifacts"]["oracles"])
    constants = derived_os_constants()
    live_summary = summarize_trinary_os(oracles, constants)
    stored = registry.get("trinary_os", {})
    tol = ver.get("constant_tolerance", 1e-6)

    if not stored:
        issues.append("trinary_os: not ingested — run ingest_trinary_os.py")
    elif live_summary["oracle_count"] != stored.get("oracle_count"):
        issues.append("trinary_os: oracle_count drift vs registry")

    if live_summary["oracle_count"] < 3:
        issues.append(f"trinary_os: only {live_summary['oracle_count']} oracle files")

    if oracles.get("hello", {}).get("seeds_hash_hex") != ver.get("seeds_hash_hex"):
        issues.append("trinary_os: seeds_hash mismatch")

    if oracles.get("hello", {}).get("panel_S_hex") != ver.get("panel_S_hex"):
        issues.append("trinary_os: panel_S_hex mismatch")

    size_checks = (
        ("hello", "hello_file_size"),
        ("call_ret", "call_ret_file_size"),
        ("spawn_join", "spawn_join_file_size"),
    )
    for key, ver_key in size_checks:
        live_size = oracles.get(key, {}).get("file_size")
        expected = ver.get(ver_key)
        if live_size != expected:
            issues.append(f"trinary_os {key}: file_size {live_size} != {expected}")

    for name in ("num_task_slots", "trit_word_width", "cortical_layers"):
        if constants.get(name) != ver.get(name):
            issues.append(f"trinary_os: {name}={constants.get(name)} != manifest {ver.get(name)}")

    for oracle in oracles.values():
        if oracle.get("panel_S_hex") != ver.get("panel_S_hex"):
            issues.append("trinary_os: inconsistent panel_S_hex across oracles")

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_trinary_os()
    print("=== Trinary OS verification ===")
    for k, v in summary.items():
        if k not in ("issues", "oracles", "constants"):
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:15]:
            print(f"    - {item}")
        return 1
    print("  All Trinary OS checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())