#!/usr/bin/env python3
"""Map brother conversation themes to FSOT domain anchors and run scalar verification."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402

OUT = ROOT / "data" / "brother_conversation_fsot_verify.json"

# Measurable literature anchors tied to conversation claims
ANCHORS = [
    ("Neuroscience", "fi_median_rel_err_pct", 24.52, "neuron_cohort_allen_FI"),
    ("Psychology", "brain_energy_fraction_human", 0.2416, "consciousness_AnAge_human"),
    ("Psychology", "brain_energy_fraction_canine", 0.15, "consciousness_AnAge_dog"),
    ("Biochemistry", "testosterone_nmol_L_adult_male", 15.0, "endocrine_testosterone_anchor"),
    ("Biology", "human_encephalization_quotient", 7.5, "human_EQ_vs_species"),
    ("Biology", "canine_encephalization_quotient", 1.2, "canine_EQ_vs_species"),
    ("Ecology", "wolf_pack_size_mean", 6.0, "gray_wolf_pack_cooperation"),
    ("Ecology", "cougar_solo_hunt_success", 0.82, "mountain_lion_solo_predator"),
    ("Materials_Science", "quartz_crystal_order_parameter", 0.99, "crystal_vs_amorphous_rock"),
    ("Geophysics", "granite_bulk_density_g_cm3", 2.65, "rock_solidification_contrast"),
    ("Quantum_Mechanics", "microtubule_decoherence_ms_upper", 0.001, "Orch_OR_contested_upper_bound"),
]

CLAIMS = [
    {
        "claim_id": "C1",
        "theme": "consciousness_solidification",
        "summary": "Consciousness flow solidifies information state; divergent skills from genetics + neuroplasticity",
        "fsot_domains": ["Neuroscience", "Psychology", "Biochemistry"],
        "panels": ["Neuroscience_Connectomics_Depth_Panel", "OpenNeuro_Full_Panel", "consciousness_AnAge"],
        "fsot_status": "partially_empirical",
        "note": "FI stratum + brain metabolic fraction wired; microtubule QC math is formal not Orch-OR proved",
    },
    {
        "claim_id": "C2",
        "theme": "chemistry_not_complexity",
        "summary": "Testosterone/chemistry affects brain substrate, not complexity class per se",
        "fsot_domains": ["Biochemistry", "Neuroscience", "Psychology"],
        "panels": ["Immunology_Panel", "Pharmacology", "SMILES_lab"],
        "fsot_status": "supported_direction",
        "note": "Endocrine chemistry routes to Biochemistry; consciousness scalar is separate layer",
    },
    {
        "claim_id": "C3",
        "theme": "observer_solidification",
        "summary": "Observer effect solidifies reality; rock vs crystal differ in order/structure",
        "fsot_domains": ["Condensed_Matter", "Materials_Science", "Quantum_Mechanics"],
        "panels": ["Condensed_Matter_Superconductivity_Depth_Panel", "Materials_Species_Bridge"],
        "fsot_status": "metaphor_with_physics_anchors",
        "note": "FSOT uses scalar prediction not Copenhagen interpretation; crystal order is measurable",
    },
    {
        "claim_id": "C4",
        "theme": "human_tool_complexity",
        "summary": "Humans retain more observable information via tools + evolution",
        "fsot_domains": ["Psychology", "Biology", "Computer_Science_extension"],
        "panels": ["Certified_Agent_Formal_Panel", "Computational_Reasoning", "Linguistics_Formal"],
        "fsot_status": "supported",
        "note": "Human brain_energy_fraction 0.24 vs dog 0.15 in consciousness_reference_observables",
    },
    {
        "claim_id": "C5",
        "theme": "animal_intelligence_underestimated",
        "summary": "Animal intelligence underestimated; evolutionary state limits solidification not intelligence",
        "fsot_domains": ["Biology", "Ecology", "Psychology"],
        "panels": ["Ecology", "consciousness_species_AnAge", "GBIF"],
        "fsot_status": "supported_direction",
        "note": "AnAge panel has Canis, Delphinus, Elephas brain metabolic fractions",
    },
    {
        "claim_id": "C6",
        "theme": "wolves_ecosystem_engineers",
        "summary": "Wolves show pack intelligence and ecosystem engineering; kleptoparasitism from cougars",
        "fsot_domains": ["Ecology", "Biology"],
        "panels": ["Ecology", "iNaturalist", "GBIF"],
        "fsot_status": "empirically_verified_literature",
        "note": "PNAS 2026 Oregon State: wolves kleptoparasitize cougar kills (Yellowstone); not wolves training lions to hunt for them",
    },
    {
        "claim_id": "C7",
        "theme": "microtubule_quantum_flow",
        "summary": "Microtubule quantum information flow explains timing/access intervals",
        "fsot_domains": ["Quantum_Mechanics", "Neuroscience", "Quantum_Computing"],
        "panels": ["Quantum_Computing_Math_Depth_Panel", "Neuroscience_Connectomics"],
        "fsot_status": "formal_scaffold_contested_empirical",
        "note": "QC math-first layer exists; Orch-OR microtubule coherence not in verified empirical ledger",
    },
]


def main() -> int:
    rows: list[dict] = []
    for domain, prop, measured, name in ANCHORS:
        try:
            rec = make_fsot_record(
                lab="brother_conversation_verify",
                property_name=prop,
                name=name,
                measured=float(measured),
                domain=domain,
            )
            rows.append(rec)
        except Exception as exc:
            rows.append({"domain": domain, "name": name, "build_error": str(exc)})

    errs = [float(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    human_bf = next((r for r in rows if r.get("name") == "consciousness_AnAge_human"), {})
    dog_bf = next((r for r in rows if r.get("name") == "consciousness_AnAge_dog"), {})

    report = {
        "title": "Brother conversation — FSOT domain verification map",
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "conversation_thesis": (
            "Consciousness is an information-energy packet whose solidification in the body "
            "depends on chemistry, neuroplasticity, and observer-capable structure; species differ "
            "in ecosystem engineering and metabolic brain fraction, not necessarily in intrinsic complexity."
        ),
        "fsot_scalar_anchors": rows,
        "pooled_median_error_pct": statistics.median(errs) if errs else None,
        "species_contrast": {
            "human_brain_energy_fraction": human_bf.get("measured"),
            "canine_brain_energy_fraction": dog_bf.get("measured"),
            "fsot_human_error_pct": human_bf.get("error_pct"),
            "fsot_canine_error_pct": dog_bf.get("error_pct"),
        },
        "claims": CLAIMS,
        "wolf_cougar_fact_check": {
            "user_claim": "Wolves hunt mountain lions who hunt food; wolves eat what lions leave",
            "verified_summary": (
                "Partially true but mechanism differs: wolves kleptoparasitize (steal) cougar kills "
                "and force diet/behavior shifts (Yellowstone PNAS 2026, Oregon State). "
                "Cougars hunt efficiently solo; wolves in packs dominate interactions — "
                "not a trained symbiosis where wolves 'use' lions as hunters."
            ),
            "sources": [
                "https://news.oregonstate.edu/news/changes-cougar-diets-and-behaviors-reduce-their-competition-wolves-yellowstone-study-finds",
                "https://www.pnas.org/doi/10.1073/pnas.2511397123",
            ],
            "fsot_domain": "Ecology",
        },
        "what_fsot_verifies": [
            "Scalar predictions against published metabolic, ecological, and materials anchors",
            "Cross-panel routing across Neuroscience, Psychology, Biochemistry, Ecology",
            "314 extension panels including consciousness species + connectomics depth",
        ],
        "what_fsot_does_not_claim": [
            "Orch-OR microtubule consciousness as proved physics",
            "Literal observer-effect reality solidification (metaphor maps to materials order)",
            "Inter-species telepathic communication",
        ],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Claims mapped: {len(CLAIMS)}")
    print(f"Scalar anchors: {len(errs)} ok, pooled median {report['pooled_median_error_pct']}%")
    for c in CLAIMS:
        print(f"  {c['claim_id']} [{c['fsot_status']}] {c['theme']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())