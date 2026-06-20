#!/usr/bin/env python3
"""Verify lab_registry.json against canonical constants and Lean oracle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
CACHE_PATH = ROOT / "data" / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import DOMAINS, raw_S  # noqa: E402

LEAN_SIGN_EXPECTATIONS = {
    "neural": "positive",
    "medical": "positive",
    "chemical": "positive",
    "electron": "positive",
    "consciousness": "positive",
    "particle": "positive",
    "quantum": "positive",
    "molecular": "positive",
    "material": "positive",
    "biological": "positive",
    "nuclear": "positive",
    "energy": "positive",
}


def rel_err(a: float, b: float) -> float:
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def check_layer_alignment(registry: dict, cache: dict) -> list[str]:
    issues: list[str] = []
    smiles_layer = registry.get("smiles_lab", {}).get("layer_constants", {})
    cache_l2 = cache.get("layer2", {})

    for name, smiles_val, cache_val in [
        ("k", smiles_layer.get("k"), cache_l2.get("k")),
        ("acoustic_bleed", smiles_layer.get("acoustic_bleed"), cache_l2.get("acoustic_bleed")),
        ("acoustic_inflow", smiles_layer.get("acoustic_inflow"), cache_l2.get("acoustic_inflow")),
    ]:
        if smiles_val is None or cache_val is None:
            issues.append(f"smiles layer missing {name}")
            continue
        err = rel_err(float(smiles_val), float(cache_val))
        if err > 1e-6:
            issues.append(f"SMILES vs canonical {name}: rel_err={err:.3e}")

    thal_K = registry.get("neurolab", {}).get("thalamic_gate", {}).get("K")
    if thal_K is not None:
        err = rel_err(float(thal_K), float(cache_l2.get("k", 0)))
        if err > 1e-6:
            issues.append(f"thalamic K vs canonical k: rel_err={err:.3e}")
    return issues


def check_domain_signs(registry: dict) -> list[str]:
    issues: list[str] = []
    for entry in registry.get("neurolab", {}).get("domain_bridge", []):
        lean = entry.get("lean_domain")
        oracle = entry.get("lean_oracle", {})
        expected = LEAN_SIGN_EXPECTATIONS.get(lean)
        if not expected or not oracle:
            continue
        raw = oracle.get("raw_S", 0)
        if expected == "positive" and raw <= 0:
            issues.append(f"{lean}: expected positive raw_S, oracle={raw}")
        live = DOMAINS.get(lean)
        if live and expected == "positive" and raw_S(live) <= 0:
            issues.append(f"{lean}: live oracle disagrees with sign expectation")
    return issues


def check_smiles_quality(registry: dict, tol_pct: float) -> list[str]:
    issues: list[str] = []
    total_gaps = 0
    for domain, stats in registry.get("smiles_lab", {}).get("domain_stats", {}).items():
        max_err = stats.get("max_error_pct")
        if max_err is not None and max_err > tol_pct:
            issues.append(f"SMILES {domain}: max_error_pct={max_err:.3f} > {tol_pct}")
        gaps = stats.get("catalog_gaps", [])
        total_gaps += len(gaps)
        if gaps:
            issues.append(
                f"SMILES {domain}: {len(gaps)} unresolved catalog gap(s): {', '.join(gaps[:5])}"
            )
    if total_gaps:
        issues.insert(0, f"SMILES catalog gaps: {total_gaps} unmatched record(s) remain")
    return issues


def check_catalog_gaps_resolved(registry: dict) -> dict:
    gaps = registry.get("smiles_lab", {}).get("catalog_gaps", {})
    return {
        "resolved": gaps.get("resolved", 0),
        "remaining": gaps.get("remaining", 0),
        "entries": gaps.get("entries", []),
    }


def check_brain_fit(registry: dict, max_gap: float) -> list[str]:
    issues: list[str] = []
    for row in registry.get("neurolab", {}).get("brain_fit", {}).get("rows", []):
        gap = row.get("mean_abs_gap", 0)
        if gap > max_gap:
            issues.append(f"brain_fit {row['observable_domain']}: mean_abs_gap={gap:.4f} > {max_gap}")
    return issues


def verify_registry(registry_path: Path = REGISTRY_PATH) -> tuple[list[str], dict]:
    if not registry_path.exists():
        return [f"missing registry: {registry_path}"], {}
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}
    hooks = registry.get("verification_hooks", {})

    issues: list[str] = []
    issues.extend(check_layer_alignment(registry, cache))
    issues.extend(check_domain_signs(registry))
    issues.extend(check_smiles_quality(registry, hooks.get("smiles_tolerance_pct", 5.0)))
    issues.extend(check_brain_fit(registry, hooks.get("brain_fit_max_gap", 0.15)))

    gap_info = check_catalog_gaps_resolved(registry)
    summary = {
        "smiles_records": registry.get("smiles_lab", {}).get("total_records"),
        "smiles_mapped": registry.get("smiles_lab", {}).get("mapped_records"),
        "catalog_gaps_remaining": gap_info.get("remaining", 0),
        "nuclei": registry.get("neurolab", {}).get("thalamic_gate", {}).get("n_nuclei"),
        "domain_bridge": len(registry.get("neurolab", {}).get("domain_bridge", [])),
        "issues": len(issues),
    }
    return issues, summary


def main() -> int:
    issues, summary = verify_registry()
    print("=== Lab registry verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())