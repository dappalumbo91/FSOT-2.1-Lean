#!/usr/bin/env python3
"""Build data/fsot_verification_progress.yaml — where we are in the verification arc."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "fsot_verification_progress.yaml"
FORMAL = ROOT / "FSOT" / "Formal"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_progress() -> dict:
    cert = _load_json(ROOT / "data" / "certificate.json")
    registry = _load_json(ROOT / "data" / "lab_registry.json")
    cohort = _load_json(ROOT / "data" / "neuron_cohort_report.json")
    allen_verify = _load_json(ROOT / "data" / "allen_sdk_verification.json")

    proved = cert.get("proved_claims")
    proved_n = len(proved) if isinstance(proved, list) else proved

    lean_modules = sorted(p.stem for p in FORMAL.glob("*.lean"))
    syn = registry.get("experiment_synthesis", {})
    strata = cohort.get("cohort_strata", {})

    tiers = [
        {
            "tier": 1,
            "name": "Core scalar + domains",
            "status": "complete",
            "artifacts": ["FSOT.Formal.Domains", "FSOT.Formal.Bounds", "FSOT.Formal.Theorems"],
        },
        {
            "tier": 2,
            "name": "Lab ingest (SMILES, NeuroLab, cosmology, …)",
            "status": "complete",
            "artifacts": [m for m in lean_modules if m.endswith("Priors") or m in ("CosmologyLab", "PhotonicForge")],
        },
        {
            "tier": 7,
            "name": "Experiment synthesis (neuron, Aether, magic circle, LLM inventory)",
            "status": "complete",
            "metrics": {
                "hero_fi_mean_rel_err": syn.get("neuron_hybrid_lab", {}).get("mean_rel_err"),
                "aether_distill_rows": syn.get("aether_prime_lab", {}).get("distill_row_count"),
                "llm_folders": syn.get("llm_experiments_lab", {}).get("project_folder_count"),
            },
        },
        {
            "tier": "7b",
            "name": "Neuron cohort + canonical scalar bridge",
            "status": "complete",
            "metrics": {
                "cohort_cells": cohort.get("cohort_fi_proxy", {}).get("cell_count"),
                "canonical_bridge_delta": (cohort.get("canonical_scalar_bridge") or {}).get(
                    "canonical_vs_certified_delta"
                ),
                "allensdk_verified": allen_verify.get("allensdk_installed"),
            },
        },
        {
            "tier": 8,
            "name": "Allen per-class strata + held-out cohort",
            "status": "complete" if strata.get("strata") else "pending",
            "metrics": {
                "held_out_cells": (strata.get("held_out_fi_proxy") or {}).get("cell_count"),
                "strata_count": len(strata.get("strata") or {}),
            },
        },
    ]

    next_steps = [
        "Per-stratum hybrid FI sim (not just slope proxy) for top specimens per class",
        "Multi-hero held-out: certify 3–5 specimens per Sst/PV/VIP/L2/3",
        "Tighten canonical bridge per-class using psi_con/eta_eff only",
        "Wire remaining LLM experiment folders into Lean namespaces",
        "Cohort train/holdout split with Lean regression gates",
    ]

    completed = [t for t in tiers if t.get("status") == "complete"]
    pending = [t for t in tiers if t.get("status") != "complete"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "remote": "https://github.com/dappalumbo91/FSOT-2.1-Lean.git",
        "summary": {
            "lean_formal_modules": len(lean_modules),
            "proved_claims": proved_n,
            "sorry_count_formal": cert.get("sorry_count_formal", 0),
            "lean_build_ok": cert.get("lean_build_ok"),
            "tiers_complete": len(completed),
            "tiers_total": len(tiers),
            "percent_complete": round(100.0 * len(completed) / max(1, len(tiers)), 1),
        },
        "current_position": "Tier 8 strata certified; precision refinement phase next",
        "tiers": tiers,
        "next_steps": next_steps,
        "key_metrics": {
            "strict_empirical_records": registry.get("formula_corpus", {}).get("records_total")
            or registry.get("knowledge_base", {}).get("strict_empirical"),
            "smiles_mapped": registry.get("smiles_lab", {}).get("mapped_records"),
            "allen_catalog_cells": cohort.get("total_cells_in_catalog"),
            "allen_eval_cells": cohort.get("cohort_fi_proxy", {}).get("cell_count"),
            "hero_fi_pct": round(100 * float((cohort.get("hero_certified_fi") or {}).get("mean_rel_err", 1)), 2),
            "canonical_bridge_fi_pct": round(
                100 * float((cohort.get("canonical_scalar_bridge") or {}).get("hero_canonical_mean_rel_err", 1)), 2
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT verification progress tracker")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if yaml is None:
        raise RuntimeError("PyYAML required")
    doc = build_progress()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {args.output}")
    print(f"  progress: {s['percent_complete']}% ({s['tiers_complete']}/{s['tiers_total']} tiers)")
    print(f"  proved claims: {s['proved_claims']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())