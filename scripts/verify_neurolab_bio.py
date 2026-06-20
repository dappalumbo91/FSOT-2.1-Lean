#!/usr/bin/env python3
"""Verify FSOT NeuroLab biological/neural data against Lean ledger + mathematics."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "neurolab_bio_manifest.yaml"
TRANSLATIONS_PATH = ROOT / "data" / "neurolab_translations_bio.json"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
CACHE_PATH = ROOT / "data" / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import DOMAINS, raw_S  # noqa: E402
from genomic_trinary import trinary_signatures  # noqa: E402
from parse_neurolab_translations import parse_translations  # noqa: E402


def rel_err(a: float, b: float) -> float:
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def check_translations(manifest: dict, translations: dict) -> list[str]:
    issues: list[str] = []
    tol = manifest["verification"]["translation_tolerance_pct"]
    domain_map = manifest.get("translation_domains", {})

    for jl_domain, cfg in domain_map.items():
        rows = translations.get("domains", {}).get(jl_domain, [])
        if not rows:
            issues.append(f"translations: no records for {jl_domain}")
            continue
        unmatched = [r for r in rows if not r.get("matched")]
        max_err = max((r.get("error_pct", 0) for r in rows), default=0)
        if max_err > tol:
            issues.append(f"translations {jl_domain}: max_error_pct={max_err:.3f} > {tol}")
        if unmatched:
            names = ", ".join(r["name"] for r in unmatched[:3])
            issues.append(f"translations {jl_domain}: {len(unmatched)} unmatched ({names})")

        lean = cfg.get("lean_domain")
        if lean and lean in DOMAINS and raw_S(DOMAINS[lean]) <= 0:
            issues.append(f"translations {jl_domain}: Lean oracle {lean} not positive")
    return issues


def check_brain_pathways(manifest: dict, neurolab_root: Path) -> list[str]:
    issues: list[str] = []
    max_gap = manifest["verification"]["brain_pathway_max_gap"]
    train_path = neurolab_root / manifest["artifacts"]["brain_formula_training"]["path"]
    if not train_path.exists():
        return [f"missing brain training CSV: {train_path}"]

    with train_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        gap = float(row.get("abs_gap", 0))
        if gap > max_gap:
            issues.append(
                f"pathway {row.get('edge_id')}: abs_gap={gap:.4f} > {max_gap}"
            )
    return issues


def check_brain_component_priors(registry: dict, manifest: dict) -> list[str]:
    issues: list[str] = []
    priors = registry.get("neurolab_bio", {}).get("brain_component_priors", {})
    if not priors or priors.get("count", 0) == 0:
        return ["brain_component_priors: not ingested into lab_registry.json"]

    ver = manifest.get("verification", {})
    expected = ver.get("brain_component_priors_count", 10)
    dna_len = ver.get("brain_component_priors_dna_length", 72)
    gc_tol = ver.get("brain_component_priors_gc_sp_tolerance", 1e-6)
    sig_tol = ver.get("brain_component_priors_signature_tolerance", 1e-4)
    expected_codons = ver.get("brain_component_priors_codon_count", 24)

    if priors.get("count") != expected:
        issues.append(
            f"brain_component_priors: count={priors.get('count')} != expected {expected}"
        )

    valid_bases = set("ATCG")
    for row in priors.get("rows", []):
        name = row.get("component", "?")
        dna = row.get("dna_proxy", "")
        if len(dna) != dna_len:
            issues.append(f"brain_component_priors {name}: dna_proxy length {len(dna)} != {dna_len}")
        if dna and not all(base in valid_bases for base in dna):
            issues.append(f"brain_component_priors {name}: invalid bases in dna_proxy")
        gc = row.get("gc_content")
        sp = row.get("superposition_ratio")
        if gc is not None and sp is not None and abs(gc - sp) > gc_tol:
            issues.append(
                f"brain_component_priors {name}: gc_content={gc} != superposition_ratio={sp}"
            )
        for field in ("gc_content", "entropy_norm", "fsot_coupling", "telemetry_alignment"):
            val = row.get(field)
            if val is None:
                issues.append(f"brain_component_priors {name}: missing {field}")
            elif not (0.0 <= float(val) <= 1.0):
                issues.append(f"brain_component_priors {name}: {field}={val} outside [0,1]")
        if row.get("aa_preview") and "-" not in str(row.get("aa_preview")):
            issues.append(f"brain_component_priors {name}: aa_preview missing peptide separators")

        sig = trinary_signatures(dna)
        if sig["codon_count"] != expected_codons:
            issues.append(
                f"brain_component_priors {name}: codon_count={sig['codon_count']} != {expected_codons}"
            )
        for field, actual, expected_val in (
            ("gc_content", sig["gc_content"], gc),
            ("superposition_ratio", sig["superposition_ratio"], sp),
            ("spin_balance", sig["spin_balance"], row.get("spin_balance")),
        ):
            if expected_val is None:
                continue
            if abs(float(actual) - float(expected_val)) > sig_tol:
                issues.append(
                    f"brain_component_priors {name}: recomputed {field}={actual:.6f} "
                    f"!= registry {expected_val}"
                )

        trinary = row.get("trinary_signature")
        if not trinary:
            issues.append(f"brain_component_priors {name}: missing trinary_signature in registry")
        else:
            counts = sig["trinary_counts"]
            for key in ("genetic_plus", "genetic_zero", "genetic_minus", "spin_plus", "spin_minus"):
                if trinary.get(key) != counts[key]:
                    issues.append(
                        f"brain_component_priors {name}: trinary_signature.{key}="
                        f"{trinary.get(key)} != {counts[key]}"
                    )
    return issues


def check_thalamic_k(registry: dict, cache: dict, manifest: dict) -> list[str]:
    issues: list[str] = []
    tol = manifest["verification"]["thalamic_k_rel_err"]
    thal_K = registry.get("neurolab", {}).get("thalamic_gate", {}).get("K")
    canon_k = cache.get("layer2", {}).get("k")
    if thal_K is None or canon_k is None:
        issues.append("thalamic K or canonical k missing")
        return issues
    err = rel_err(float(thal_K), float(canon_k))
    if err > tol:
        issues.append(f"thalamic K rel_err={err:.3e} > {tol}")
    return issues


def verify_bio(
    manifest_path: Path = MANIFEST_PATH,
    translations_path: Path = TRANSLATIONS_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    neurolab_root = Path(manifest["neurolab_root"])
    jl_path = neurolab_root / manifest["artifacts"]["translations_jl"]["path"]

    if translations_path.exists():
        translations = json.loads(translations_path.read_text(encoding="utf-8"))
    elif jl_path.exists():
        translations = parse_translations(jl_path)
        translations_path.write_text(json.dumps(translations, indent=2), encoding="utf-8")
    else:
        return [f"missing translations: {jl_path}"], {}

    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}

    issues: list[str] = []
    issues.extend(check_translations(manifest, translations))
    issues.extend(check_brain_pathways(manifest, neurolab_root))
    issues.extend(check_brain_component_priors(registry, manifest))
    issues.extend(check_thalamic_k(registry, cache, manifest))

    summary = {
        "translation_total": translations.get("total", 0),
        "translation_domains": translations.get("counts", {}),
        "brain_pathways": 0,
        "brain_component_priors": registry.get("neurolab_bio", {})
        .get("brain_component_priors", {})
        .get("count", 0),
        "issues": len(issues),
    }
    train_path = neurolab_root / manifest["artifacts"]["brain_formula_training"]["path"]
    if train_path.exists():
        with train_path.open(encoding="utf-8", newline="") as f:
            summary["brain_pathways"] = sum(1 for _ in csv.DictReader(f))

    return issues, summary


def main() -> int:
    issues, summary = verify_bio()
    print("=== NeuroLab biological verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All NeuroLab bio checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())