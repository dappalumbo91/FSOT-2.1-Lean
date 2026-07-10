#!/usr/bin/env python3
"""Aggregate particle-physics observables: SMILES + thesis waves + Wave-4 + math rules."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
MANIFEST_PATH = ROOT / "data" / "particle_physics_manifest.yaml"
OUTPUT = ROOT / "data" / "particle_physics_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"

from fsot_paths import fsot_compute_path, manifest_path as repo_path, thesis_root  # noqa: E402


def _load_wave4(compute_path: Path) -> list[dict]:
    if not compute_path.exists():
        return []
    sys.path.insert(0, str(ROOT / "scripts"))
    from cosmology_wave4 import summarize_wave4, wave4_observables  # noqa: E402
    from cosmology_lambda import load_fsot_compute  # noqa: E402

    mod = load_fsot_compute(compute_path)
    rows = wave4_observables(mod)
    return rows


def _smiles_particle_rows(dataset_path: Path, section_map_path: Path) -> list[dict]:
    section_map = json.loads(section_map_path.read_text(encoding="utf-8")).get("section_to_domain", {})
    records = json.loads(dataset_path.read_text(encoding="utf-8"))
    if isinstance(records, dict):
        records = records.get("records") or records.get("data") or []
    out: list[dict] = []
    for rec in records:
        if section_map.get(rec.get("section")) != "particle":
            continue
        out.append(
            {
                "source": "smiles_lab",
                "section": rec.get("section"),
                "name": rec.get("name"),
                "computed": rec.get("computed_value"),
                "measured": rec.get("target_value"),
                "error_pct": rec.get("error_pct"),
            }
        )
    return out


def _thesis_particle_rows(thesis_root: Path, categories: list[str]) -> list[dict]:
    out: list[dict] = []
    cat_set = set(categories)
    for wave in (7, 8, 9, 10):
        path = thesis_root / f"wave{wave}_observations.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, row in (data.get("targets") or {}).items():
            if row.get("category") not in cat_set:
                continue
            out.append(
                {
                    "source": "thesis_wave",
                    "wave": wave,
                    "id": key,
                    "name": row.get("name") or key,
                    "category": row.get("category"),
                    "measured": row.get("measured"),
                    "sigma_percent": row.get("sigma_percent"),
                }
            )
    return out


def _math_physics_rules(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = data.get("rules") or []
    out: list[dict] = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        out.append(
            {
                "source": "math_physics_rules",
                "id": rule.get("id"),
                "name": rule.get("name"),
                "category": rule.get("category"),
            }
        )
    return out


def build_benchmark(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]

    smiles_path = repo_path(src["smiles_dataset"])
    section_map = repo_path(src["section_domain_map"])
    if not smiles_path.exists():
        raise FileNotFoundError(f"SMILES dataset missing: {smiles_path}")

    smiles = _smiles_particle_rows(smiles_path, section_map)
    thesis = _thesis_particle_rows(thesis_root(), list(src["thesis_particle_categories"]))
    wave4 = _load_wave4(fsot_compute_path())
    rules = _math_physics_rules(repo_path(src["math_physics_rules"]))

    errs = [float(r["error_pct"]) for r in smiles if r.get("error_pct") is not None]
    errs += [float(r["error_pct"]) for r in wave4 if r.get("error_pct") is not None]
    within_2 = sum(1 for e in errs if e <= 2.0)
    within_5 = sum(1 for e in errs if e <= 5.0)

    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    w4_summary = registry.get("cosmology_wave4", {})

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "smiles_particle_count": len(smiles),
        "thesis_particle_wave_count": len(thesis),
        "wave4_count": len(wave4),
        "math_physics_rule_count": len(rules),
        "observable_count": len(smiles) + len(thesis) + len(wave4) + len(rules),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "max_error_pct": max(errs) if errs else None,
        "within_two_pct_count": within_2,
        "within_five_pct_count": within_5,
        "wave4_max_error_pct": w4_summary.get("max_error_pct"),
        "smiles_particle_records": smiles,
        "thesis_particle_waves": thesis,
        "wave4_observables": wave4,
        "math_physics_rules": rules,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build_benchmark(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  smiles: {bench['smiles_particle_count']}  "
        f"thesis: {bench['thesis_particle_wave_count']}  "
        f"wave4: {bench['wave4_count']}  "
        f"rules: {bench['math_physics_rule_count']}  "
        f"total: {bench['observable_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())