#!/usr/bin/env python3
"""
Ingest FSOT SMILES Lab and NeuroLab rendered data into a unified lab registry.

Reads chemical/biological constants (SMILES), neurological gate/fit data (NeuroLab),
maps them to Lean ledger domains, and writes data/lab_registry.json.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CROSSWALK_PATH = DATA / "lab_domain_crosswalk.yaml"
SECTION_MAP_PATH = DATA / "section_domain_map.json"
OUTPUT_PATH = DATA / "lab_registry.json"
CACHE_PATH = DATA / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import DOMAINS, raw_S, term1, term2, term3  # noqa: E402
from genomic_trinary import trinary_signatures  # noqa: E402

try:
    from parse_neurolab_translations import parse_translations
except ImportError:
    parse_translations = None  # type: ignore


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_crosswalk() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install PyYAML")
    return yaml.safe_load(CROSSWALK_PATH.read_text(encoding="utf-8"))


def load_neurolab_scalars() -> dict[str, float]:
    neurolab_compute = Path(r"C:\Users\damia\Desktop\FSOT NeuroLab\fsot_compute.py")
    if not neurolab_compute.exists():
        return {}
    spec = importlib.util.spec_from_file_location("neurolab_compute", neurolab_compute)
    if spec is None or spec.loader is None:
        return {}
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return {name: float(mod.domain_scalar(name)) for name in mod.DOMAINS}


def load_section_map() -> dict[str, str]:
    if SECTION_MAP_PATH.exists():
        payload = json.loads(SECTION_MAP_PATH.read_text(encoding="utf-8"))
        return payload.get("section_to_domain", {})
    return {}


def ingest_smiles(smiles_root: Path, crosswalk: dict) -> dict:
    json_path = smiles_root / crosswalk["smiles_files"]["dataset_json"]
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    records = payload["records"]
    section_map = load_section_map()

    by_domain: dict[str, list] = defaultdict(list)
    unmapped: list = []
    for rec in records:
        domain = section_map.get(rec["section"])
        if domain:
            by_domain[domain].append(rec)
        else:
            unmapped.append(rec)

    catalog_gap_entries: list[dict] = []
    domain_stats = {}
    for domain, rows in by_domain.items():
        errors = [r["error_pct"] for r in rows if r.get("error_pct") is not None]
        unmatched_rows = [r for r in rows if not r.get("matched")]
        domain_stats[domain] = {
            "record_count": len(rows),
            "matched_count": sum(1 for r in rows if r.get("matched")),
            "unmatched_count": len(unmatched_rows),
            "median_error_pct": sorted(errors)[len(errors) // 2] if errors else None,
            "max_error_pct": max(errors) if errors else None,
            "catalog_gaps": [r["name"] for r in unmatched_rows],
            "sample_names": [r["name"] for r in rows[:5]],
        }
        for r in unmatched_rows:
            catalog_gap_entries.append({
                "section": r.get("section"),
                "name": r.get("name"),
                "lean_domain": domain,
            })

    layer1 = payload.get("layer1", {})
    layer2 = payload.get("layer2", {})
    return {
        "source_path": str(json_path),
        "sha256": sha256_file(json_path),
        "metadata": payload.get("metadata", {}),
        "total_records": len(records),
        "mapped_records": sum(len(v) for v in by_domain.values()),
        "unmapped_records": len(unmapped),
        "layer_constants": {
            "alpha": layer1.get("α_FSOT") or layer1.get("alpha"),
            "k": layer2.get("K"),
            "acoustic_bleed": layer2.get("A_bleed"),
            "acoustic_inflow": layer2.get("A_in"),
        },
        "domain_stats": domain_stats,
        "catalog_gaps": {
            "resolved": 8 - len(catalog_gap_entries),
            "remaining": len(catalog_gap_entries),
            "entries": catalog_gap_entries,
        },
        "bio_sections": {k: domain_stats[k] for k in ("medical", "neural", "chemical", "electron") if k in domain_stats},
        "unmapped_section_sample": list({r["section"] for r in unmapped[:20]}),
    }


def build_domain_bridge(
    crosswalk: dict, neurolab_scalars: dict[str, float], layer_k: float | None = None
) -> list[dict]:
    bridge = []
    for lean_name, cfg in crosswalk.get("lean_domains", {}).items():
        nb_name = cfg.get("neurolab_name")
        oracle_p = DOMAINS.get(lean_name)
        entry: dict = {
            "lean_domain": lean_name,
            "neurolab_domain": nb_name,
            "lean_theorem": cfg.get("lean_theorem"),
            "tags": cfg.get("tags", []),
            "params": {
                "D_eff": cfg.get("D_eff"),
                "recent_hits": cfg.get("recent_hits"),
                "delta_psi": cfg.get("delta_psi"),
                "observed": cfg.get("observed"),
            },
        }
        if oracle_p:
            rs = raw_S(oracle_p)
            entry["lean_oracle"] = {
                "term1": round(term1(oracle_p), 6),
                "term2": round(term2(oracle_p), 6),
                "term3": round(term3(oracle_p), 6),
                "raw_S": round(rs, 6),
                "sign": "+" if rs > 0 else "-",
            }
        if nb_name and nb_name in neurolab_scalars:
            nb_scaled = neurolab_scalars[nb_name]
            entry["neurolab_scalar"] = round(nb_scaled, 6)
            if oracle_p and layer_k:
                nb_raw = nb_scaled / layer_k
                entry["neurolab_raw_S_est"] = round(nb_raw, 6)
                entry["ledger_aligned"] = abs(nb_raw - entry["lean_oracle"]["raw_S"]) < 0.05
        bridge.append(entry)
    return bridge


def ingest_neurolab(neurolab_root: Path, crosswalk: dict, layer_k: float | None = None) -> dict:
    thalamus_path = neurolab_root / crosswalk["neurolab_files"]["thalamic_gate"]
    brain_csv_path = neurolab_root / crosswalk["neurolab_files"]["brain_fit_csv"]
    artic_path = neurolab_root / crosswalk["neurolab_files"]["articulation_manifest"]

    thalamus = json.loads(thalamus_path.read_text(encoding="utf-8"))
    artic = json.loads(artic_path.read_text(encoding="utf-8"))

    with brain_csv_path.open(encoding="utf-8", newline="") as f:
        brain_rows = list(csv.DictReader(f))

    nuclei_summary = []
    for code, nuc in thalamus.get("nuclei", {}).items():
        emb = nuc.get("gate_embedding", [])
        nuclei_summary.append({
            "code": code,
            "full_name": nuc.get("full_name"),
            "modality": nuc.get("modality"),
            "cortical_target": nuc.get("cortical_target"),
            "gate_embedding_dim": len(emb),
            "go_term_count": len(nuc.get("go_terms", [])),
            "allen_genes": [k for k in (nuc.get("allen_expression") or {}) if k != "opentargets"],
            "K_embedded": emb[5] if len(emb) > 5 else None,
        })

    neurolab_scalars = load_neurolab_scalars()
    compute_path = neurolab_root / "fsot_compute.py"

    return {
        "thalamic_gate": {
            "path": str(thalamus_path),
            "sha256": sha256_file(thalamus_path),
            "K": thalamus.get("K"),
            "n_nuclei": thalamus.get("n_nuclei"),
            "nuclei": nuclei_summary,
        },
        "brain_fit": {
            "path": str(brain_csv_path),
            "sha256": sha256_file(brain_csv_path),
            "observable_domains": len(brain_rows),
            "rows": [
                {
                    "observable_domain": r["observable_domain"],
                    "mean_abs_gap": float(r["mean_abs_gap"]),
                    "mean_target": float(r["mean_target"]),
                    "mean_model": float(r["mean_model"]),
                }
                for r in brain_rows
            ],
        },
        "articulation": {
            "path": str(artic_path),
            "case_count": artic.get("case_count"),
            "canary_count": artic.get("canary_case_count"),
            "fsot_knowledge_cases": [
                t["name"] for t in artic.get("targets", [])
                if any(tag in t.get("tags", []) for tag in ("scalar", "fsot", "d_eff", "neuron", "gate"))
            ],
        },
        "domain_bridge": build_domain_bridge(crosswalk, neurolab_scalars, layer_k=layer_k),
        "neurolab_compute": {
            "path": str(compute_path),
            "sha256": sha256_file(compute_path) if compute_path.exists() else None,
        },
    }


def ingest_neurolab_bio(neurolab_root: Path, manifest_path: Path | None = None) -> dict:
    manifest_path = manifest_path or (DATA / "neurolab_bio_manifest.yaml")
    if not manifest_path.exists() or yaml is None or parse_translations is None:
        return {"present": False}

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    jl_path = neurolab_root / manifest["artifacts"]["translations_jl"]["path"]
    translations = parse_translations(jl_path) if jl_path.exists() else {"domains": {}, "total": 0}

    train_path = neurolab_root / manifest["artifacts"]["brain_formula_training"]["path"]
    pathways: list[dict] = []
    if train_path.exists():
        with train_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                pathways.append({
                    "edge_id": row.get("edge_id"),
                    "pathway": row.get("pathway_name"),
                    "observable_domain": row.get("observable_domain"),
                    "primary_domain": row.get("primary_domain"),
                    "abs_gap": float(row.get("abs_gap", 0)),
                    "target_score": float(row.get("target_score", 0)),
                })

    priors_path = neurolab_root / manifest["artifacts"]["brain_component_priors"]["path"]
    component_priors: list[dict] = []
    if priors_path.exists():
        with priors_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                dna_proxy = row.get("dna_proxy", "")
                sig = trinary_signatures(dna_proxy)
                component_priors.append({
                    "component": row.get("component"),
                    "system": row.get("system"),
                    "organization": row.get("organization"),
                    "canonical_function": row.get("canonical_function"),
                    "fsot_coupling": float(row.get("fsot_coupling", 0)),
                    "telemetry_alignment": float(row.get("telemetry_alignment", 0)),
                    "gc_content": float(row.get("gc_content", 0)),
                    "entropy_norm": float(row.get("entropy_norm", 0)),
                    "superposition_ratio": float(row.get("superposition_ratio", 0)),
                    "spin_balance": float(row.get("spin_balance", 0)),
                    "dna_proxy": dna_proxy,
                    "aa_preview": row.get("aa_preview", ""),
                    "reference_url": row.get("reference_url"),
                    "trinary_signature": {
                        "codon_count": sig["codon_count"],
                        "genetic_plus": sig["trinary_counts"]["genetic_plus"],
                        "genetic_zero": sig["trinary_counts"]["genetic_zero"],
                        "genetic_minus": sig["trinary_counts"]["genetic_minus"],
                        "spin_plus": sig["trinary_counts"]["spin_plus"],
                        "spin_minus": sig["trinary_counts"]["spin_minus"],
                        "recomputed_gc_content": round(sig["gc_content"], 4),
                        "recomputed_superposition_ratio": round(sig["superposition_ratio"], 4),
                        "recomputed_spin_balance": round(sig["spin_balance"], 4),
                        "recomputed_entropy_norm": round(sig["entropy_norm"], 4),
                    },
                })

    domain_stats = {}
    for jl_domain, rows in translations.get("domains", {}).items():
        errors = [r["error_pct"] for r in rows if r.get("error_pct") is not None]
        domain_stats[jl_domain] = {
            "record_count": len(rows),
            "matched_count": sum(1 for r in rows if r.get("matched")),
            "max_error_pct": max(errors) if errors else None,
            "lean_domain": manifest.get("translation_domains", {}).get(jl_domain, {}).get("lean_domain"),
        }

    return {
        "present": True,
        "translations_source": str(jl_path),
        "translation_total": translations.get("total", 0),
        "translation_domains": domain_stats,
        "brain_pathways": {
            "count": len(pathways),
            "max_abs_gap": max((p["abs_gap"] for p in pathways), default=0),
            "sample": pathways[:5],
        },
        "brain_component_priors": {
            "path": str(priors_path),
            "sha256": sha256_file(priors_path) if priors_path.exists() else None,
            "count": len(component_priors),
            "components": [p["component"] for p in component_priors],
            "rows": component_priors,
        },
    }


def build_registry(crosswalk: dict | None = None) -> dict:
    crosswalk = crosswalk or load_crosswalk()
    smiles_root = Path(crosswalk["lab_paths"]["smiles_lab"])
    neurolab_root = Path(crosswalk["lab_paths"]["neurolab"])
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}

    return {
        "registry_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_constants_sha256": cache.get("hash_gate", {}).get("authority_sha256"),
        "smiles_lab": ingest_smiles(smiles_root, crosswalk),
        "neurolab": ingest_neurolab(
            neurolab_root,
            crosswalk,
            layer_k=float(cache.get("layer2", {}).get("k", 0)) or None,
        ),
        "neurolab_bio": ingest_neurolab_bio(neurolab_root),
        "verification_hooks": {
            "smiles_tolerance_pct": 5.0,
            "brain_fit_max_gap": 0.15,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest SMILES + NeuroLab into lab_registry.json")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    registry = build_registry()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    smiles = registry["smiles_lab"]
    neuro = registry["neurolab"]
    print(f"Wrote {args.output}")
    print(f"  SMILES records: {smiles['total_records']} ({smiles['mapped_records']} mapped)")
    print(f"  NeuroLab nuclei: {neuro['thalamic_gate']['n_nuclei']}")
    print(f"  Brain fit domains: {neuro['brain_fit']['observable_domains']}")
    print(f"  Domain bridge: {len(neuro['domain_bridge'])} lean<->lab links")
    bio = registry.get("neurolab_bio", {})
    if bio.get("present"):
        priors = bio.get("brain_component_priors", {})
        print(f"  Brain component priors: {priors.get('count', 0)} (trinary signatures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())