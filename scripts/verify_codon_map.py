#!/usr/bin/env python3
"""Verify FSOT 64-codon trinary map against Genetics source + registry."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "codon_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from codon_trinary import (  # noqa: E402
    all_codons,
    encode_codon,
    load_map_file,
    summarize_codons,
)
from genomic_trinary import GENETIC_MAP, SPIN_MAP  # noqa: E402


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def check_registry_codons(registry: dict, manifest: dict) -> list[str]:
    issues: list[str] = []
    ver = manifest.get("verification", {})
    expected = ver.get("codon_count", 64)
    primary_space = ver.get("primary_pattern_space", 8)
    secondary_space = ver.get("secondary_pattern_space", 27)
    expected_stops = set(ver.get("stop_codons", ["TAA", "TAG", "TGA"]))

    codon = registry.get("codon_trinary_map", {})
    if not codon:
        return ["codon_trinary_map: not ingested — run ingest_codon_map.py"]

    if codon.get("codon_count") != expected:
        issues.append(f"codon_trinary_map: codon_count={codon.get('codon_count')} != {expected}")

    summary = summarize_codons(all_codons())
    for key in (
        "distinct_primary_patterns",
        "distinct_secondary_patterns",
        "stop_codon_count",
    ):
        if codon.get(key) != summary[key]:
            issues.append(f"codon_trinary_map: {key}={codon.get(key)} != source {summary[key]}")

    if codon.get("distinct_primary_patterns") > primary_space:
        issues.append(
            f"primary patterns {codon.get('distinct_primary_patterns')} > {primary_space}"
        )
    if codon.get("distinct_secondary_patterns") > secondary_space:
        issues.append(
            f"secondary patterns {codon.get('distinct_secondary_patterns')} > {secondary_space}"
        )

    rows = codon.get("rows", [])
    if len(rows) != expected:
        issues.append(f"codon_trinary_map: row count {len(rows)} != {expected}")

    seen = set()
    for row in rows:
        c = row.get("codon", "?")
        if c in seen:
            issues.append(f"codon_trinary_map: duplicate codon {c}")
        seen.add(c)
        try:
            expected_row = encode_codon(c)
        except ValueError:
            issues.append(f"codon_trinary_map: invalid codon {c}")
            continue
        if tuple(row.get("primary", ())) != expected_row["primary"]:
            issues.append(f"codon_trinary_map {c}: primary mismatch")
        if tuple(row.get("secondary", ())) != expected_row["secondary"]:
            issues.append(f"codon_trinary_map {c}: secondary mismatch")
        for i, base in enumerate(c):
            if row["primary"][i] != SPIN_MAP[base]:
                issues.append(f"codon_trinary_map {c}: primary[{i}] != SPIN_MAP")
            if row["secondary"][i] != GENETIC_MAP[base]:
                issues.append(f"codon_trinary_map {c}: secondary[{i}] != GENETIC_MAP")

    if set(codon.get("stop_codons", [])) != expected_stops:
        issues.append(f"codon_trinary_map: stop_codons={codon.get('stop_codons')} != {expected_stops}")
    if codon.get("start_codon") != ver.get("start_codon", "ATG"):
        issues.append(f"codon_trinary_map: start_codon={codon.get('start_codon')}")

    return issues


def check_genetics_map_file(manifest: dict) -> list[str]:
    issues: list[str] = []
    genetics_root = Path(manifest["genetics_root"])
    map_path = genetics_root / manifest["artifacts"]["codon_map_txt"]["path"]
    if not map_path.exists():
        return [f"missing codon map file: {map_path}"]

    file_map = load_map_file(map_path)
    if len(file_map) != 64:
        issues.append(f"64_codon_trinary_map.txt: parsed {len(file_map)} rows, expected 64")

    for row in all_codons():
        codon = row["codon"]
        parsed = file_map.get(codon)
        if not parsed:
            issues.append(f"64_codon_trinary_map.txt: missing codon {codon}")
            continue
        if parsed["primary"] != row["primary"]:
            issues.append(f"64_codon_trinary_map.txt {codon}: primary mismatch")
        if parsed["secondary"] != row["secondary"]:
            issues.append(f"64_codon_trinary_map.txt {codon}: secondary mismatch")
    return issues


def check_trinary_codon_project(manifest: dict) -> list[str]:
    issues: list[str] = []
    project_root = Path(manifest["artifacts"]["build_script"]["project_root"])
    build_path = project_root / manifest["artifacts"]["build_script"]["path"]
    if not build_path.exists():
        return [f"missing Trinary Codon build script: {build_path}"]

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "64_codon_trinary_map.txt"
        proc = subprocess.run(
            [sys.executable, str(build_path)],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            issues.append(f"build_64_codon_map.py failed: {proc.stderr.strip() or proc.stdout.strip()}")
            return issues

        generated = project_root / "64_codon_trinary_map.txt"
        if not generated.exists():
            issues.append("build_64_codon_map.py did not emit 64_codon_trinary_map.txt")
            return issues

        file_map = load_map_file(generated)
        if len(file_map) != 64:
            issues.append(f"Trinary Codon project map: parsed {len(file_map)} rows")

        for row in all_codons():
            codon = row["codon"]
            parsed = file_map.get(codon)
            if not parsed:
                issues.append(f"Trinary Codon project map: missing {codon}")
                continue
            if parsed["primary"] != row["primary"] or parsed["secondary"] != row["secondary"]:
                issues.append(f"Trinary Codon project map {codon}: axis mismatch")
    return issues


def verify_codon(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}

    issues: list[str] = []
    issues.extend(check_genetics_map_file(manifest))
    issues.extend(check_trinary_codon_project(manifest))
    issues.extend(check_registry_codons(registry, manifest))

    codon = registry.get("codon_trinary_map", {})
    summary = {
        "codon_count": codon.get("codon_count", 0),
        "distinct_primary_patterns": codon.get("distinct_primary_patterns", 0),
        "distinct_secondary_patterns": codon.get("distinct_secondary_patterns", 0),
        "stop_codon_count": codon.get("stop_codon_count", 0),
        "file_map_rows": codon.get("file_map_rows", 0),
        "issues": len(issues),
    }
    return issues, summary


def main() -> int:
    issues, summary = verify_codon()
    print("=== Codon trinary map verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:20]:
            print(f"    - {item}")
        if len(issues) > 20:
            print(f"    ... and {len(issues) - 20} more")
        return 1
    print("  All codon trinary map checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())