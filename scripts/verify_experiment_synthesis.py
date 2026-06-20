#!/usr/bin/env python3
"""Verify Tier 7 experiment synthesis labs against fsot_compute canon."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "experiment_synthesis_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_canonical_adapter import (  # noqa: E402
    canonical_constants,
    canonical_domain_scalar,
    golden_angle_deg,
    rel_err,
)


def verify_experiment_synthesis(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    syn = registry.get("experiment_synthesis", {})
    issues: list[str] = []
    const = canonical_constants()

    neuron = syn.get("neuron_hybrid_lab", {})
    if not neuron.get("present"):
        issues.append("neuron_hybrid_lab: not ingested")
    else:
        if neuron.get("mean_rel_err", 1.0) > ver.get("neuron_mean_rel_err_max", 0.15):
            issues.append(f"neuron_hybrid_lab: mean_rel_err {neuron['mean_rel_err']:.4f} too high")
        if neuron.get("verifier_confidence", 0) < ver.get("neuron_verifier_confidence_min", 0.9):
            issues.append("neuron_hybrid_lab: verifier confidence too low")
        k_tol = ver.get("neuron_K_abs_tol", 5e-4)
        if abs(neuron.get("neuron_K_cached", 0) - const["k"]) > k_tol:
            issues.append("neuron_hybrid_lab: K mismatch vs fsot_compute")
        neuro_s = canonical_domain_scalar(manifest["sources"]["neuron_hybrid"]["domain_compute"])
        if neuro_s <= 0:
            issues.append("neuron_hybrid_lab: Neuroscience domain S not positive")

    aether = syn.get("aether_prime_lab", {})
    if not aether.get("present"):
        issues.append("aether_prime_lab: not ingested")
    else:
        if aether.get("distill_row_count", 0) < ver.get("aether_distill_row_min", 100):
            issues.append("aether_prime_lab: insufficient distill rows")
        tol = ver.get("aether_constant_rel_tol", 1e-5)
        for key, canon_key in (
            ("psi_con_solver", "psi_con"),
            ("eta_eff_solver", "eta_eff"),
        ):
            if rel_err(aether.get(key, 0), const[canon_key]) > tol:
                issues.append(f"aether_prime_lab: {key} drift from canon")
        if rel_err(aether.get("golden_angle_solver_deg", 0), golden_angle_deg()) > tol:
            issues.append("aether_prime_lab: golden_angle drift from canon")

    magic = syn.get("magic_circle_lab", {})
    if not magic.get("present"):
        issues.append("magic_circle_lab: not ingested")
    else:
        if magic.get("min_resonance_for_emergence", 1) > ver.get("magic_min_resonance_max", 0.5):
            issues.append("magic_circle_lab: min_resonance out of expected range")
        if magic.get("internalized_threshold", 0) < ver.get("magic_internalized_min", 0.9):
            issues.append("magic_circle_lab: internalized_threshold too low")

    llm = syn.get("llm_experiments_lab", {})
    if not llm.get("present"):
        issues.append("llm_experiments_lab: root missing")

    cohort = registry.get("neuron_cohort_lab", {})
    if not cohort.get("present"):
        issues.append("neuron_cohort_lab: not ingested")
    else:
        proxy = cohort.get("cohort_fi_proxy", {})
        hero = cohort.get("hero_certified_fi", {})
        bridge = cohort.get("neurolab_smiles_bridge", {})
        if proxy.get("cell_count", 0) < ver.get("min_cell_count", 2000):
            issues.append(f"neuron_cohort: only {proxy.get('cell_count')} cells")
        if proxy.get("fi_median_rel_err", 1) > ver.get("fi_median_rel_err_max", 0.30):
            issues.append("neuron_cohort: FI median rel err too high")
        if proxy.get("fi_pearson_r", 0) < ver.get("fi_pearson_r_min", 0.55):
            issues.append("neuron_cohort: FI pearson r too low")
        if hero.get("mean_rel_err", 1) > ver.get("hybrid_mean_rel_err_max", 0.15):
            issues.append("neuron_cohort: hero certified FI error too high")
        canon_bridge = cohort.get("canonical_scalar_bridge", {})
        if canon_bridge.get("hero_canonical_mean_rel_err", 1) > ver.get(
            "canonical_bridge_mean_rel_err_max", 0.12
        ):
            issues.append("neuron_cohort: canonical bridge FI error too high")
        if not canon_bridge.get("within_few_points", False):
            issues.append("neuron_cohort: canonical bridge delta from certified too large")
        if bridge.get("smiles_mapped_records", 0) < ver.get("smiles_mapped_min", 1400):
            issues.append("neuron_cohort: SMILES mapped count too low")
        if bridge.get("strict_empirical_records", 0) < ver.get("strict_empirical_min", 7900):
            issues.append("neuron_cohort: strict empirical count too low")

    summary = {
        "neuron_mean_rel_err": neuron.get("mean_rel_err"),
        "aether_distill_rows": aether.get("distill_row_count"),
        "magic_present": magic.get("present"),
        "llm_folder_count": llm.get("project_folder_count"),
        "cohort_cell_count": cohort.get("cohort_fi_proxy", {}).get("cell_count"),
        "hero_certified_err": cohort.get("hero_certified_fi", {}).get("mean_rel_err"),
        "issues": len(issues),
    }
    return issues, summary


def main() -> int:
    issues, summary = verify_experiment_synthesis()
    print("=== Experiment Synthesis verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All experiment synthesis checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())