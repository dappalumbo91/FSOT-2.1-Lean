#!/usr/bin/env python3
"""Ingest Tier 7 experiment synthesis labs into lab_registry.json."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "experiment_synthesis_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys_path = ROOT / "scripts"
import sys

sys.path.insert(0, str(sys_path))
from fsot_canonical_adapter import (  # noqa: E402
    canonical_constants,
    canonical_domain_scalar,
    golden_angle_deg,
)


def _load_manifest(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def ingest_neuron(manifest: dict) -> dict:
    src = manifest["sources"]["neuron_hybrid"]
    root = Path(src["root"])
    report_path = root / src["report"]
    if not report_path.exists():
        return {"present": False, "report_path": str(report_path)}
    report = json.loads(report_path.read_text(encoding="utf-8"))
    const = canonical_constants()
    neuron_k = 0.420222080893624
    return {
        "present": True,
        "report_path": str(report_path),
        "specimen_id": report.get("specimen_id"),
        "cell_class": report.get("cell_class"),
        "fi_point_count": len(report.get("sustained_fi") or []),
        "mean_rel_err": float(report.get("mean_rel_err", 1.0)),
        "verifier_confidence": float((report.get("verifier") or {}).get("confidence", 0.0)),
        "soma_gain_base": float((report.get("constants") or {}).get("soma_gain_base", 0.0)),
        "soma_gain_scalar": float((report.get("constants") or {}).get("soma_gain_scalar", 0.0)),
        "neuron_K_cached": neuron_k,
        "canonical_k": const["k"],
        "canonical_psi_con": const["psi_con"],
        "canonical_eta_eff": const["eta_eff"],
        "canonical_neuroscience_S": canonical_domain_scalar(manifest["sources"]["neuron_hybrid"]["domain_compute"]),
        "scalar_legacy": src["scalar_legacy"],
        "scalar_canon": src["scalar_canon"],
    }


def ingest_aether_prime(manifest: dict) -> dict:
    src = manifest["sources"]["aether_prime"]
    root = Path(src["root"])
    distill_path = root / src["distill"]
    config_path = root / src["config"]
    if not distill_path.exists():
        return {"present": False, "distill_path": str(distill_path)}
    rows = []
    for line in distill_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    ops = Counter(r.get("operation") for r in rows)
    const = canonical_constants()
    ga = golden_angle_deg()
    sample = next((r for r in rows if r.get("operation") == "psi_consciousness"), {})
    psi_solver = float((sample.get("solver_output") or {}).get("results", {}).get("psi_con", 0))
    sample_eta = next((r for r in rows if r.get("operation") == "eta_efficiency"), {})
    eta_solver = float((sample_eta.get("solver_output") or {}).get("results", {}).get("eta_eff", 0))
    sample_ga = next((r for r in rows if r.get("operation") == "golden_angle"), {})
    ga_solver = float((sample_ga.get("solver_output") or {}).get("results", {}).get("golden_angle_deg", 0))
    return {
        "present": True,
        "distill_path": str(distill_path),
        "config_path": str(config_path) if config_path.exists() else None,
        "distill_row_count": len(rows),
        "solver_op_count": len(src.get("solver_ops") or []),
        "operation_counts": dict(ops),
        "psi_con_solver": psi_solver,
        "eta_eff_solver": eta_solver,
        "golden_angle_solver_deg": ga_solver,
        "canonical_psi_con": const["psi_con"],
        "canonical_eta_eff": const["eta_eff"],
        "canonical_golden_angle_deg": ga,
        "verifier_reject_count": sum(1 for r in rows if "REJECTED" in (r.get("verifier_feedback") or "")),
    }


def ingest_magic_circle(manifest: dict) -> dict:
    src = manifest["sources"]["magic_circle"]
    root = Path(src["root"])
    config_path = root / src["config"]
    if not config_path.exists():
        return {"present": False, "config_path": str(config_path)}
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    rules = cfg.get("fsot_glyph_rules", {})
    stab = rules.get("stabilization_boundary", {})
    obs = rules.get("observer_effect", {})
    phys = rules.get("physics_math_constraints", {})
    return {
        "present": True,
        "config_path": str(config_path),
        "min_resonance_for_emergence": float(stab.get("min_resonance_for_emergence", 0)),
        "internalized_threshold": float(obs.get("internalized_threshold", 0)),
        "imbalance_penalty_max": float(phys.get("imbalance_penalty_max", 0)),
        "backlash_risk_threshold_high": float(rules.get("backlash", {}).get("risk_threshold_high", 0)),
    }


def ingest_llm_experiments(manifest: dict) -> dict:
    root = Path(manifest["sources"]["llm_experiments"]["root"])
    if not root.exists():
        return {"present": False, "root": str(root)}
    folders = sorted(p.name for p in root.iterdir() if p.is_dir())
    return {
        "present": True,
        "root": str(root),
        "project_folder_count": len(folders),
        "project_folders": folders,
    }


def ingest_neuron_cohort() -> dict:
    cohort_script = ROOT / "scripts" / "run_neuron_cohort_eval.py"
    report_path = ROOT / "data" / "neuron_cohort_report.json"
    if cohort_script.exists():
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(cohort_script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return {"present": False, "error": proc.stderr.strip() or proc.stdout.strip()}
    if not report_path.exists():
        return {"present": False, "report_path": str(report_path)}
    report = json.loads(report_path.read_text(encoding="utf-8"))
    return {"present": True, "report_path": str(report_path), **report}


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest experiment synthesis labs")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()

    manifest = _load_manifest(args.manifest)
    synthesis = {
        "neuron_hybrid_lab": ingest_neuron(manifest),
        "aether_prime_lab": ingest_aether_prime(manifest),
        "magic_circle_lab": ingest_magic_circle(manifest),
        "llm_experiments_lab": ingest_llm_experiments(manifest),
        "manifest_path": str(args.manifest),
        "neuron_cohort_lab": ingest_neuron_cohort(),
    }
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["experiment_synthesis"] = synthesis
    if synthesis["neuron_cohort_lab"].get("present"):
        registry["neuron_cohort_lab"] = synthesis["neuron_cohort_lab"]
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  neuron FI mean rel err: {synthesis['neuron_hybrid_lab'].get('mean_rel_err')}")
    print(f"  aether distill rows: {synthesis['aether_prime_lab'].get('distill_row_count')}")
    print(f"  magic circle config: {synthesis['magic_circle_lab'].get('present')}")
    print(f"  llm folders: {synthesis['llm_experiments_lab'].get('project_folder_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())