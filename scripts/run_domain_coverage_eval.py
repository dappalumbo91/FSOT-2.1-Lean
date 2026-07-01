#!/usr/bin/env python3
"""Evaluate all 35 FSOT NeuroLab domains against Lean ledger + empirical labs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_YAML = ROOT / "data" / "fsot_35_domain_registry.yaml"
REPORT_PATH = ROOT / "data" / "domain_coverage_report.json"
LAB_REGISTRY = ROOT / "data" / "lab_registry.json"
ALIGNMENT = ROOT / "data" / "neurolab_ledger_alignment.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import DOMAINS as LEAN_DOMAINS, raw_S  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402


LEAN_SIGN_THEOREMS = {
    "cosmological": "cosmological_raw_S_negative",
    "dark_energy": "dark_energy_raw_S_negative",
    "cmb": "cmb_raw_S_negative",
    "ai": "ai_raw_S_non_positive",
    "neural": "neural_raw_S_positive",
    "quantum": "quantum_raw_S_positive",
    "particle": "particle_raw_S_positive",
    "chemical": "chemical_raw_S_positive",
    "electron": "electron_raw_S_positive",
    "medical": "medical_raw_S_positive",
    "molecular": "molecular_raw_S_positive",
    "material": "material_raw_S_positive",
    "biological": "biological_raw_S_positive",
    "nuclear": "nuclear_raw_S_positive",
    "energy": "energy_raw_S_positive",
    "consciousness": "consciousness_raw_S_positive",
    "astronomical": "astronomical_raw_S_positive",
    "higgs": "higgs_raw_S_positive",
    "galactic": "galactic_raw_S_positive",
    "fusion": "fusion_raw_S_positive",
    "proton": "proton_raw_S_positive",
    "blackhole": "blackhole_raw_S_positive",
}


def _lab_record_count(registry: dict, lab_key: str) -> tuple[int, float | None]:
    """Return (record_count, median_error_pct or None) for a lab registry entry."""
    lab = registry.get(lab_key, {})
    if not lab or not lab.get("present", True) and lab_key.endswith("_lab"):
        if not lab:
            return 0, None

    if lab_key == "smiles_lab":
        return int(lab.get("mapped_records") or 0), float((lab.get("metadata") or {}).get("median_error_pct") or 0)

    if lab_key == "neuron_cohort_lab":
        proxy = lab.get("cohort_fi_proxy", {})
        return int(proxy.get("cell_count") or 0), float(proxy.get("fi_median_rel_err") or 0) * 100

    if lab_key == "cosmology_lambda_cdm":
        rows = lab.get("rows") or []
        errs = [abs(r.get("error_pct", 100)) for r in rows if r.get("error_pct") is not None]
        med = sorted(errs)[len(errs) // 2] if errs else None
        return len(rows), med

    if lab_key == "cosmology_wave4":
        return int(lab.get("observable_count") or lab.get("wave4_count") or 0), float(lab.get("mean_error_pct") or 0)

    if lab_key == "weather_lab":
        return int(lab.get("hour_count") or 0), None

    if lab_key == "fuel_lab":
        return int(lab.get("entry_count") or lab.get("resolved_count") or 0), float(lab.get("max_error_pct") or 0)

    if lab_key in ("species_lab", "species_catalog"):
        return int(lab.get("property_count") or lab.get("species_count") or 0), float(lab.get("mean_error_pct") or 0)

    if lab_key == "linguistics_lab":
        rows = lab.get("rows") or []
        errs = [abs(r.get("error_pct", 100)) for r in rows if r.get("error_pct") is not None]
        med = sorted(errs)[len(errs) // 2] if errs else None
        return len(rows), med

    if lab_key == "evolution_lab":
        return int(lab.get("operon_count") or 0), None

    if lab_key == "cellular_lab":
        return int(lab.get("soul_records_processed") or 0), None

    if lab_key == "neurolab_bio":
        return int(lab.get("translation_total") or 0), None

    if lab_key == "blackhole_thesis":
        return int(lab.get("observable_count") or 0), float(lab.get("max_error_pct") or 0)

    if lab_key in ("trinary_fluid_lab", "trinary_fluid_computer"):
        return int(lab.get("metatron_pathways") or 0), float(lab.get("engine_accuracy_pct") or 0)

    if lab_key in ("vib_register_lab", "vibra_register"):
        return int(lab.get("trial_count") or 2), None

    if lab_key in ("trinary_os_lab", "trinary_os"):
        return int(lab.get("oracle_count") or 0), None

    return int(lab.get("count") or lab.get("record_count") or 0), None


def _expected_lean_params(lean_domain: str, overrides_yaml: dict) -> dict | None:
    for _name, spec in (overrides_yaml.get("overrides") or {}).items():
        if spec.get("lean_domain") == lean_domain:
            return {
                "D_eff": int(spec["D_eff"]),
                "recent_hits": int(spec["hits"]),
                "delta_psi": float(spec["delta_psi"]),
                "observed": bool(spec["observed"]),
            }
    if lean_domain in LEAN_DOMAINS:
        p = LEAN_DOMAINS[lean_domain]
        return {
            "D_eff": int(p.D_eff),
            "recent_hits": int(p.recent_hits),
            "delta_psi": float(p.delta_psi),
            "observed": bool(p.observed),
        }
    return None


def _aligns(compute_cfg, lean_domain: str, overrides_yaml: dict, tol: float) -> bool | None:
    lp = _expected_lean_params(lean_domain, overrides_yaml)
    if lp is None:
        return None
    return (
        int(compute_cfg.D_eff) == lp["D_eff"]
        and int(compute_cfg.hits) == lp["recent_hits"]
        and abs(float(compute_cfg.delta_psi) - lp["delta_psi"]) < tol
        and bool(compute_cfg.observed) == lp["observed"]
    )


def evaluate() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
    alignment_yaml = (
        yaml.safe_load(ALIGNMENT.read_text(encoding="utf-8")) if ALIGNMENT.exists() else {}
    )
    registry = json.loads(LAB_REGISTRY.read_text(encoding="utf-8")) if LAB_REGISTRY.exists() else {}
    mod, authority_path = load_fsot_compute()
    tol = float(spec["verification"].get("lean_align_tol", 1e-9))

    lean_overrides = spec.get("lean_overrides", {})
    empirical_sources = spec.get("empirical_sources", {})
    domains_out = []

    for name in sorted(mod.DOMAINS.keys()):
        cfg = mod.DOMAINS[name]
        S = float(mod.domain_scalar(name))
        in_lean_override = name in lean_overrides
        lean_domain = lean_overrides.get(name)
        if lean_domain is None:
            src = empirical_sources.get(name, {})
            lean_domain = src.get("lean_domain")

        empirical_records = 0
        empirical_detail = []
        median_errors = []
        for lab_key in (empirical_sources.get(name, {}).get("labs") or []):
            n, med = _lab_record_count(registry, lab_key)
            empirical_records += n
            if n > 0:
                empirical_detail.append({"lab": lab_key, "records": n, "median_error_pct": med})
            if med is not None:
                median_errors.append(med)

        lean_raw = None
        if lean_domain and lean_domain in LEAN_DOMAINS:
            lean_raw = raw_S(LEAN_DOMAINS[lean_domain])

        domains_out.append(
            {
                "neurolab_domain": name,
                "lean_domain": lean_domain,
                "D_eff": int(cfg.D_eff),
                "hits": int(cfg.hits),
                "delta_psi": float(cfg.delta_psi),
                "observed": bool(cfg.observed),
                "domain_scalar_S": S,
                "scalar_sign": "negative" if S < -1e-12 else ("positive" if S > 1e-12 else "zero"),
                "lean_raw_S": lean_raw,
                "lean_sign_theorem": LEAN_SIGN_THEOREMS.get(lean_domain or ""),
                "lean_param_aligned": (
                    _aligns(cfg, lean_domain, alignment_yaml, tol) if in_lean_override else None
                ),
                "lean_override": in_lean_override,
                "empirical_records": empirical_records,
                "empirical_sources": empirical_detail,
                "empirical_median_error_pct": (
                    sorted(median_errors)[len(median_errors) // 2] if median_errors else None
                ),
                "has_empirical_data": empirical_records > 0,
            }
        )

    empirical_domains = [d for d in domains_out if d["has_empirical_data"]]
    lean_mapped = [d for d in domains_out if d.get("lean_override")]
    aligned = [d for d in domains_out if d.get("lean_param_aligned") is True]

    return {
        "authority_path": str(authority_path),
        "domain_count": len(domains_out),
        "domains_with_empirical_data": len(empirical_domains),
        "total_empirical_records": sum(d["empirical_records"] for d in domains_out),
        "lean_mapped_count": len(lean_mapped),
        "lean_param_aligned_count": len(aligned),
        "negative_scalar_domains": [d["neurolab_domain"] for d in domains_out if d["scalar_sign"] == "negative"],
        "domains": domains_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 35-domain coverage evaluation")
    parser.add_argument("--output", type=Path, default=REPORT_PATH)
    args = parser.parse_args()
    report = evaluate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  domains: {report['domain_count']}")
    print(f"  with empirical data: {report['domains_with_empirical_data']}")
    print(f"  total empirical records: {report['total_empirical_records']}")
    print(f"  lean aligned: {report['lean_param_aligned_count']}/{report['lean_mapped_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())