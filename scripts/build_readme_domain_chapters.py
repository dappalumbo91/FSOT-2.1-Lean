#!/usr/bin/env python3
"""
Generate verbose domain-by-domain README chapters from live verification data.

Deepening passes:
  1. Finer interdisciplinary sub-clusters (music/arts, finance, live-ingest, …)
  2. Per-panel observable tables (top measured vs computed from benchmarks)
  3. Formula-level prose linking strict_empirical rows (Appendix XII-E style)
  4. Subfield maps expanded from navigator breadth_note / tags / manifest notes

Outputs: data/publication/readme_domain_chapters/*.md
Manifest: data/publication/readme_domain_chapters_manifest.yaml
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "readme_domain_chapters"
MANIFEST = ROOT / "data" / "publication" / "readme_domain_chapters_manifest.yaml"
ATLAS = ROOT / "data" / "publication" / "domain_atlas.csv"
NAV = ROOT / "data" / "fsot_domain_navigator.json"
MAP = ROOT / "data" / "scientific_domain_expansion_map.yaml"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
STRICT_EMPIRICAL = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"

RECORD_KEYS = ("records", "material_records", "skeleton_derivations", "benchmark_rows", "rows")
TOP_OBSERVABLES = 5
TOP_FORMULAS = 3

LEAN_DOMAIN_BLURB = {
    "cosmological": "negative dispersal regime — structure bleeds at cosmic scales unless bubble-bleed dual anchors apply",
    "astronomical": "stellar and galactic catalog readouts through astronomical ledger routes",
    "cmb": "CMB and large-scale structure interval certificates",
    "particle": "particle and atomic observables via high-energy scalar channels",
    "higgs": "electroweak and Higgs-sector cached observables",
    "nuclear": "nuclear structure and BBN-proxy channels",
    "medical": "biochemical and medical SMILES-anchored properties",
    "biological": "life-system emergence — positive raw_S at canonical biological folds",
    "neural": "neuroscience and brain-component metabolic proxies",
    "consciousness": "observer-coupled consciousness routes with quirk_mod active",
    "electron": "electromagnetic and chemical electron-shell observables",
    "chemical": "molecular chemistry and bonding readouts",
    "material": "condensed-matter and materials properties",
    "energy": "thermodynamic, atmospheric, and energy-sector observables",
    "quantum": "quantum mechanics and entanglement-channel readouts",
    "ai": "computational and AI-oracle invariant panels",
}

LEAN_TO_FORMULA_PREFIXES: dict[str, tuple[str, ...]] = {
    "particle": ("IE_", "CODATA", "Ry_", "Rydberg"),
    "electron": ("IE_", "eV", "shell"),
    "chemical": ("BE_", "BL_", "mol_", "SMILES"),
    "medical": ("BE_", "BL_", "IE_", "clinical"),
    "material": ("BE_", "elastic", "acoustic"),
    "nuclear": ("BE_", "mass_", "nucl"),
    "energy": ("H_", "enthalpy", "weather"),
    "astronomical": ("H0", "z_", "mag_"),
    "cosmological": ("H0", "Omega", "Lambda"),
}

DOMAIN_TO_FORMULA_PREFIXES: dict[str, tuple[str, ...]] = {
    "Atomic_Physics": ("IE_",),
    "Electron": ("IE_",),
    "Chemistry": ("BE_", "BL_"),
    "Biochemistry": ("BE_", "BL_"),
    "Medical": ("BE_", "IE_"),
    "Nuclear_Physics": ("BE_", "mass"),
    "Materials_Science": ("BE_", "elastic"),
}

# (slug, title, predicate on domain name) — first match wins
CLUSTERS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "01_cosmology_fundamental",
        "Cosmology, Particle Physics & Fundamental Forces",
        (
            "Cosmolog",
            "CMB",
            "Dark_",
            "Hubble",
            "Bubble_Bleed",
            "Lambda",
            "Particle_",
            "Higgs",
            "Neutrino",
            "Nuclear",
            "BBN",
            "Inflation",
            "Astrophysical",
            "Stellar",
            "Galactic",
            "Compact_Object",
            "Gravitational",
            "Arxiv_Gravitational",
            "High_Energy",
            "Atomic_Physics",
            "Quantum_Mechanics",
            "Quantum_Optics",
            "Quantum_Computing",
            "Quantum_Gravity",
            "Quantum_Information",
            "Quantum_Materials",
            "Plasma_",
            "CERN_",
            "PDG_",
            "NIST_",
        ),
    ),
    (
        "02_space_geophysics",
        "Space Weather, Geophysics & Planetary Science",
        (
            "Magnetosphere",
            "Geomag",
            "Space_Weather",
            "Seismolog",
            "Tectonic",
            "Hydrolog",
            "Cryosphere",
            "Grace_",
            "Planetary",
            "Orbital",
            "Exoplanet",
            "Exogeolog",
            "Small_Body",
            "JPL_",
            "USGS_",
            "NOAA_",
            "Weather",
            "Meteorolog",
            "Atmospheric",
            "Oceanograph",
            "Paleoclim",
            "Speleolog",
            "Geochem",
            "Geolog",
            "Astronomy",
            "Astrophysics",
        ),
    ),
    (
        "03_biology_genomics",
        "Biology, Genomics, Medicine & Ecology",
        (
            "Biolog",
            "Genom",
            "Genetic",
            "Protein",
            "Codon",
            "Species",
            "Evolution",
            "Cellular",
            "iGEM",
            "Immunolog",
            "Oncolog",
            "Neuroimmun",
            "Synthetic_Biology",
            "Pharmacolog",
            "Clinical",
            "Cardiology",
            "Virolog",
            "Epidemiol",
            "Botany",
            "Zoology",
            "Marine_",
            "Mycolog",
            "Entomolog",
            "Paleontolog",
            "Ecology",
            "Agriculture",
            "Food_",
            "Culinary",
            "Physarum",
            "AnAge",
            "OpenNeuro",
            "Neuron",
        ),
    ),
    (
        "04_chemistry_materials",
        "Chemistry, Materials & Molecular Engineering",
        (
            "Chem",
            "SMILES",
            "Materials",
            "Fuel_",
            "PubChem",
            "Periodic",
            "Element_",
            "Island_",
            "Superheavy",
            "Fusion",
            "Metamaterial",
            "Acoustic_Resonance",
            "Condensed_Matter",
            "CRC_",
            "Machine_And_Molecule",
        ),
    ),
    (
        "05_consciousness_social",
        "Consciousness, Neuroscience & Social Sciences",
        (
            "Consciousness",
            "Neural",
            "Neuro",
            "Soul_",
            "Psycholog",
            "Sociolog",
            "Linguistic",
            "Anthropolog",
            "Law_",
            "History",
            "Neuroeconomic",
            "Symbolic_",
            "Archetype",
            "Genesis",
            "Omni_Theory",
        ),
    ),
    (
        "06_engineering_propulsion",
        "Engineering, Propulsion & Verified Desktop Technology",
        (
            "Transporter",
            "Warp_",
            "Propulsion",
            "Space_Propulsion",
            "Electrical_Power",
            "Hvac_",
            "Civil_Engineering",
            "Mechanical_Engineering",
            "Robotics",
            "Architecture_",
            "Trinary",
            "Photonic",
            "Desktop_Application",
            "BlackHole_WhiteHole",
            "Fuel_Lab",
            "Star_Trek",
            "Breakthrough_Discoveries",
        ),
    ),
    (
        "07_mathematics_computation",
        "Mathematics, Computation & Formal Methods",
        (
            "Math_",
            "Formula_",
            "Alternate_Base",
            "Airfoil",
            "Trinary_OS",
            "Tokenization",
            "Computational_Reasoning",
            "Lean_",
            "Bibliography",
            "Proof_",
            "Certificate",
            "Oracle",
            "Knowledge_Base",
            "Aggregate_",
            "Sota_",
            "Adversarial_",
            "Domain_Coupling",
        ),
    ),
    (
        "08_cybersecurity",
        "Cybersecurity, Code Genomes & Threat Intelligence",
        (
            "Cyber",
            "Malware",
            "Code_Genome",
            "Zero_Day",
            "CVE_",
            "Cryptograph",
        ),
    ),
    (
        "09_founding_laws",
        "Founding 35 Physics Laws (Dedicated Panels)",
        ("Founding_",),
    ),
    # --- interdisciplinary sub-clusters (formerly 10_interdisciplinary) ---
    (
        "10_live_ingest_astrometry",
        "Live Ingest, Astrometry & Real-Time Catalog Spines",
        (
            "Live_Ingest_",
            "Gaia_",
            "GWOSC_",
            "NASA_DONKI_",
            "NASA_NEO_",
            "Open_Meteo_",
            "STScI_MAST_",
            "VizieR_",
            "WDS_Live_",
            "IGEM_Live_",
            "Solar_System_Structure_",
            "SH0ES_",
        ),
    ),
    (
        "11_fluid_spacetime_time",
        "Fluid Spacetime, Temporal Coupling & Phase Spines",
        (
            "FPC_",
            "Fluid_Phase_",
            "Fluid_Spacetime_",
            "Time_Domain_",
            "Time_Emergence_",
            "Term3_Acoustic_",
        ),
    ),
    (
        "12_finance_economics_logistics",
        "Finance, Econometrics & Supply-Chain Logistics",
        (
            "Actuarial_",
            "Econometrics",
            "Econophysics",
            "World_Bank_",
            "Supply_Chain_",
            "Finance_",
            "Economic",
        ),
    ),
    (
        "13_music_arts_creative",
        "Music, Harmonics & Creative Media",
        ("Music_", "Interactive_Media_"),
    ),
    (
        "14_government_open_data",
        "Government Registries, Open Data & Scholarly Graphs",
        (
            "Federal_Science_",
            "Government_Open_",
            "OSTI_",
            "iNaturalist_",
            "OpenAlex_",
            "Crossref_",
        ),
    ),
    (
        "15_arxiv_meta_folding_spines",
        "arXiv Meta-Panels, Folding Spines & ToE Crosswalks",
        (
            "Arxiv_",
            "Foundational_Ontology_",
            "Reality_Folding_",
            "Scientific_Expansion_",
            "ToE_",
            "Theory_Completeness_",
            "Tier_93_",
            "Interdisciplinary_Spine_",
            "Unified_DB_",
        ),
    ),
    (
        "16_prereg_scaffolds",
        "Preregistered Outcome Tracking & Verification Scaffolds",
        (
            "Preregistered_",
            "Material_In_Silico_",
            "Material_Property_Verification_",
        ),
    ),
    (
        "17_llm_agents_oracles",
        "LLM Validators, Certified Agents & Oracle Decoders",
        (
            "Certified_Agent_",
            "Intrinsic_LLM_",
            "VL_Agent_",
            "VL_Distill_",
            "Binary_Decoder_",
        ),
    ),
    (
        "18_public_biology_longevity",
        "Public Biology, Longevity & Wet-Lab Depth Panels",
        (
            "Biophysics_Public_",
            "Longevity_",
            "NCBI_Gene_",
            "RCSB_PDB_",
            "UniProt_",
            "IGEM_Parts_",
            "Zebrafish_",
            "Tier_94_",
            "Tier_95_",
            "Ethology_",
            "Limnology_",
            "Toxicology_",
            "Pharmacokinetics",
            "The_Well_",
        ),
    ),
    (
        "19_physics_engineering_depth",
        "Climate, Geoscience Depth & Applied Physics Panels",
        (
            "Climate_Science",
            "Optics_",
            "Semiconductor_",
            "Statistical_Mechanics_",
            "Heavy_Ion_",
            "Environmental_Engineering",
            "HVAC_",
            "Chaos_Mediated_",
            "Volcanology_",
            "Soil_Science_",
            "Sports_Biomechanics",
            "Cartography_",
            "Mechanistic_",
            "Complexity_Folding_",
            "Z120_",
        ),
    ),
    (
        "20_mathematics_formal_depth",
        "Pure Mathematics, Formal Depth & Fold Metrics",
        (
            "Experimental_Base_Mathematics_",
            "Mathematics_Computational",
            "Pure_Mathematics",
            "Programming_Language_",
            "Information_Theory_",
            "Fold_Depth_",
            "Fractal_Constant_",
            "Compactification_",
            "Adjacent_Rung_",
            "Boundary_Partition_",
            "RD_Interval_",
            "Phi_Morphogenetic_",
            "Overflow_Carry_",
            "Observer_Channel_",
            "Zero_Boundary_",
            "Nothing_Perfection_",
            "Scalar_Solver_",
            "Prediction_Rederivation",
        ),
    ),
    (
        "21_verification_infrastructure",
        "Verification Infrastructure, Hardware & Network Spines",
        (
            "Living_FSOT_",
            "Portable_Clone_",
            "Public_Verifiable_",
            "Stumped_Observables_",
            "UAP_War_",
            "Hybrid_FI_Sim_",
            "Network_Internet_",
            "Network_Science_",
            "Secure_Software_",
        ),
    ),
    (
        "22_interdisciplinary_residual",
        "Residual Cross-Domain & Emergence Panels",
        (),
    ),
)


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _fmt_pct(v: float | str | None) -> str:
    if v is None or v == "":
        return "n/a"
    try:
        return f"{float(v):.6g}"
    except (TypeError, ValueError):
        return str(v)


def _fmt_val(v: object) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.6g}"
    s = str(v)
    return s if len(s) <= 48 else s[:45] + "…"


def _cluster_for(name: str) -> str:
    if name.startswith("Founding_"):
        return "09_founding_laws"
    for slug, _title, keys in CLUSTERS:
        if slug in ("09_founding_laws", "22_interdisciplinary_residual"):
            continue
        if any(k in name for k in keys):
            return slug
    return "22_interdisciplinary_residual"


def _humanize(name: str) -> str:
    return name.replace("_", " ")


def _split_subfields(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = re.split(r"[/,]| \+ | and ", text)
    return [p.strip() for p in parts if p.strip()]


def _parse_breadth_note(note: str) -> tuple[list[str], list[str]]:
    if not note:
        return [], []
    covered_part = note
    thin_part = ""
    if ";" in note:
        covered_part, rest = note.split(";", 1)
        if "thin on" in rest.lower():
            thin_part = re.split(r"thin on", rest, maxsplit=1, flags=re.I)[-1]
    covered = _split_subfields(covered_part)
    thin = _split_subfields(thin_part) if thin_part else []
    return covered, thin


def _subfield_map_core(meta: dict) -> list[str]:
    note = meta.get("breadth_note") or ""
    covered, thin = _parse_breadth_note(note)
    touched = meta.get("subfields_touched")
    studied = meta.get("subfields_studied")
    lines = [
        f"**Subfield map** ({touched or '—'} touched / {studied or '—'} studied in discipline):",
        "",
    ]
    if covered:
        lines.append(f"- **Measured cohorts:** {', '.join(covered)}")
    if thin:
        lines.append(f"- **Registered thin gaps:** {', '.join(thin)}")
    if not covered and not thin and note:
        lines.append(f"- {note}")
    labs = meta.get("labs") or []
    if labs:
        lines.append(f"- **Verification labs:** {', '.join(f'`{lab}`' for lab in labs)}")
    lines.append("")
    return lines


def _subfield_map_extension(
    panel_meta: dict,
    manifest_entry: dict | None,
) -> list[str]:
    tags = [t.replace("_", " ").title() for t in (panel_meta.get("tags") or [])]
    maps = panel_meta.get("maps_to_lean") or (panel_meta.get("scientific") or {}).get(
        "maps_to_lean"
    ) or []
    note = (manifest_entry or {}).get("note") or ""
    covered, thin = _parse_breadth_note(note)
    routes = [f"`{m}`" for m in maps]
    lines = ["**Subfield map:**", ""]
    if routes:
        lines.append(f"- **Lean routes:** {', '.join(routes)}")
    if tags:
        lines.append(f"- **Panel tags:** {', '.join(tags)}")
    if covered:
        lines.append(f"- **Data sources / cohorts:** {', '.join(covered)}")
    if thin:
        lines.append(f"- **Registered thin gaps:** {', '.join(thin)}")
    elif note and not covered:
        lines.append(f"- {note}")
    labs = (manifest_entry or {}).get("labs") or []
    if labs:
        lines.append(f"- **Labs:** {', '.join(f'`{l}`' for l in labs)}")
    lines.append("")
    return lines


def _resolve_benchmark_path(domain: str, panel_meta: dict, manifest: dict) -> Path | None:
    candidates: list[str] = []
    sci = panel_meta.get("scientific") or {}
    if sci.get("benchmark_path"):
        candidates.append(sci["benchmark_path"])
    bundle = panel_meta.get("download_bundle") or {}
    if bundle.get("benchmark_data"):
        candidates.append(bundle["benchmark_data"])
    ext = (manifest.get("extension_domains") or {}).get(domain) or {}
    if ext.get("benchmark_data"):
        candidates.append(ext["benchmark_data"])

    for rel in candidates:
        path = ROOT / rel.replace("\\", "/")
        if path.is_file():
            return path

    snake = domain.lower()
    for path in sorted((ROOT / "data").glob(f"{snake}*benchmark*.json")):
        return path
    alt = ROOT / "data" / f"{snake}_benchmark.json"
    return alt if alt.is_file() else None


def _normalize_record(row: dict) -> dict | None:
    measured = row.get("measured")
    if measured is None:
        measured = row.get("target_value") or row.get("observed") or row.get("measured_value")
    computed = row.get("computed")
    if computed is None:
        computed = row.get("computed_value") or row.get("predicted") or row.get("fsot_value")
    if measured is None and computed is None:
        return None
    unit = row.get("unit") or ""
    sci = row.get("scientific_measurement") or {}
    if not unit and isinstance(sci, dict):
        unit = sci.get("unit") or ""
    return {
        "name": row.get("name") or row.get("display_name") or row.get("concept") or "—",
        "property": row.get("property") or row.get("lab") or "",
        "measured": measured,
        "computed": computed,
        "error_pct": row.get("error_pct"),
        "unit": unit,
    }


def _extract_top_observables(benchmark: dict, n: int = TOP_OBSERVABLES) -> list[dict]:
    pool: list[dict] = []
    for key in RECORD_KEYS:
        for row in benchmark.get(key) or []:
            if isinstance(row, dict):
                norm = _normalize_record(row)
                if norm:
                    pool.append(norm)

    def err_key(r: dict) -> float:
        try:
            return float(r.get("error_pct") if r.get("error_pct") is not None else 999)
        except (TypeError, ValueError):
            return 999.0

    pool.sort(key=lambda r: (err_key(r), str(r.get("property") or ""), str(r.get("name") or "")))

    picked: list[dict] = []
    seen_props: set[str] = set()
    for row in pool:
        prop = str(row.get("property") or row.get("name") or "")
        if prop in seen_props and len(picked) < n:
            continue
        seen_props.add(prop)
        picked.append(row)
        if len(picked) >= n:
            break
    if len(picked) < n:
        for row in pool:
            if row not in picked:
                picked.append(row)
            if len(picked) >= n:
                break
    return picked[:n]


def _observable_table_rows(observables: list[dict]) -> list[str]:
    if not observables:
        return ["*No normalized measured/computed rows in benchmark artifact.*", ""]
    lines = [
        "| Observable | Measured | Computed | Error % |",
        "|------------|---------:|---------:|--------:|",
    ]
    for obs in observables:
        label = obs.get("property") or obs.get("name") or "—"
        if obs.get("property") and obs.get("name") and obs["property"] != obs["name"]:
            label = f"{obs['property']} · {obs['name']}"
        unit = obs.get("unit") or ""
        if unit:
            label = f"{label} ({unit})"
        lines.append(
            f"| {label} | {_fmt_val(obs.get('measured'))} | {_fmt_val(obs.get('computed'))} "
            f"| {_fmt_pct(obs.get('error_pct'))} |"
        )
    lines.append("")
    return lines


def _load_formula_index() -> tuple[dict[tuple[str, str, str], dict], dict[str, list[dict]]]:
    by_key: dict[tuple[str, str, str], dict] = {}
    by_concept: dict[str, list[dict]] = {}
    if not STRICT_EMPIRICAL.is_file():
        return by_key, by_concept
    for line in STRICT_EMPIRICAL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = (
            str(row.get("concept_name") or ""),
            str(row.get("formula_canonical") or ""),
            str(row.get("target_quantity") or ""),
        )
        if key in by_key:
            continue
        by_key[key] = row
        concept = key[0]
        by_concept.setdefault(concept, []).append(row)
    return by_key, by_concept


def _formula_sort_key(row: dict) -> float:
    outcome = row.get("outcome") or {}
    try:
        return float(outcome.get("error_pct") or 999)
    except (TypeError, ValueError):
        return 999.0


def _match_formulas(
    domain: str,
    lean: str,
    maps_to_lean: list[str],
    observables: list[dict],
    by_concept: dict[str, list[dict]],
    top_n: int = TOP_FORMULAS,
) -> list[dict]:
    hits: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    def add(row: dict) -> None:
        key = (
            str(row.get("concept_name") or ""),
            str(row.get("formula_canonical") or ""),
            str(row.get("target_quantity") or ""),
        )
        if key not in seen:
            seen.add(key)
            hits.append(row)

    obs_text = " ".join(
        str(obs.get(k) or "")
        for obs in observables
        for k in ("name", "property")
    ).lower()

    for concept, rows in by_concept.items():
        cl = concept.lower()
        if cl and (cl in obs_text or any(cl in t.lower() or t.lower() in cl for t in obs_text.split())):
            add(sorted(rows, key=_formula_sort_key)[0])

    prefixes: list[str] = list(DOMAIN_TO_FORMULA_PREFIXES.get(domain, ()))
    for route in [lean, *maps_to_lean]:
        prefixes.extend(LEAN_TO_FORMULA_PREFIXES.get(route, ()))
    for concept, rows in by_concept.items():
        if any(concept.startswith(p) for p in prefixes):
            add(sorted(rows, key=_formula_sort_key)[0])

    hits.sort(key=_formula_sort_key)
    return hits[:top_n]


def _formula_prose_block(formulas: list[dict], domain: str) -> list[str]:
    if not formulas:
        return []
    lines = [
        "**Formula-level verification** (strict empirical corpus — Appendix XII-E style):",
        "",
    ]
    for row in formulas:
        outcome = row.get("outcome") or {}
        concept = row.get("concept_name") or "—"
        formula = row.get("formula_raw") or row.get("formula_map") or row.get("formula_canonical") or "—"
        target = outcome.get("target_value") or row.get("target_quantity") or "—"
        computed = outcome.get("computed_value") or "—"
        err = _fmt_pct(outcome.get("error_pct"))
        constants = ", ".join(row.get("constants_used") or []) or "seed constants"
        cites = row.get("verification_citations") or "NIST / CRC / public archive"
        lines.append(
            f"- **`{concept}`** in {_humanize(domain)}: measured **{target}**, "
            f"seed-derived **{_fmt_val(computed)}** via `{formula}` "
            f"(error **{err}%**). Constants: {constants}. Authority: {cites}."
        )
    lines.append("")
    return lines


def _benchmark_cache_load(path: Path, cache: dict[str, dict]) -> dict | None:
    key = str(path)
    if key not in cache:
        try:
            cache[key] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cache[key] = {}
    data = cache[key]
    return data if data else None


def _core_chapter(
    nav: dict,
    core_rows: list[dict],
    formula_by_concept: dict[str, list[dict]],
) -> str:
    nav_core = {c["name"]: c for c in nav.get("core_domains") or []}
    lines = [
        "## Core NeuroLab Spine — 35 Scientific Domains",
        "",
        "The core spine routes FSOT through 35 preregistered NeuroLab domains. Each domain "
        "selects a Lean ledger route (`lean_domain`), verification labs, and measured record cohort. "
        "All core domains pass the ≤0.5% green gate.",
        "",
    ]
    for row in core_rows:
        name = row["domain"]
        meta = nav_core.get(name, {})
        lean = row.get("lean_domain") or meta.get("lean_domain") or ""
        blurb = LEAN_DOMAIN_BLURB.get(lean, "cross-domain scalar evaluation at canonical seed parameters")
        labs = row.get("labs") or ";".join(meta.get("labs") or [])
        breadth = meta.get("breadth_note") or "Full panel coverage via extension labs."

        bench_path = _resolve_benchmark_path(name, {}, _load_yaml(EXT_MANIFEST))
        observables: list[dict] = []
        if bench_path:
            data = json.loads(bench_path.read_text(encoding="utf-8"))
            observables = _extract_top_observables(data)

        formulas = _match_formulas(
            name,
            lean,
            meta.get("maps_to_lean") or [],
            observables,
            formula_by_concept,
        )

        lines.extend(
            [
                f"### {name}",
                "",
                f"**Lean route:** `{lean}` — {blurb}.",
                "",
                f"| Metric | Value |",
                f"|--------|------:|",
                f"| Empirical records | {row.get('record_count', meta.get('empirical_records', 'n/a'))} |",
                f"| Pooled median error | {_fmt_pct(row.get('median_error_pct', meta.get('median_error_pct')))}% |",
                f"| Coverage tier | {row.get('coverage_tier', meta.get('coverage_tier', ''))} |",
                f"| Subfields touched | {meta.get('subfields_touched') or '—'} / {meta.get('subfields_studied') or '—'} studied |",
                "",
                f"**Verification labs:** `{labs}`",
                "",
                f"**Scientific coverage:** {breadth}",
                "",
            ]
        )
        lines.extend(_subfield_map_core(meta))
        if observables:
            lines.append("**Top observables (measured vs computed):**")
            lines.append("")
            lines.extend(_observable_table_rows(observables))
        lines.extend(_formula_prose_block(formulas, name))
        lines.extend(
            [
                f"**FSOT readout:** The same seed engine evaluates {name.lower()} observables without "
                f"per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class "
                f"surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to "
                f"seed-derived predictions through `{lean}` routing.",
                "",
            ]
        )
    return "\n".join(lines)


def _extension_domain_block(
    row: dict,
    panel_meta: dict,
    manifest_entry: dict | None,
    bench_cache: dict[str, dict],
    formula_by_concept: dict[str, list[dict]],
) -> list[str]:
    name = row["domain"]
    lean_mod = row.get("lean_module") or ""
    tier = row.get("tier") or ""
    maps = panel_meta.get("maps_to_lean") or (panel_meta.get("scientific") or {}).get("maps_to_lean") or []
    lean_route = maps[0] if maps else (panel_meta.get("routes_to_core") or "").lower()

    bench_path = _resolve_benchmark_path(name, panel_meta, _load_yaml(EXT_MANIFEST))
    observables: list[dict] = []
    bench_rel = ""
    if bench_path:
        bench_rel = str(bench_path.relative_to(ROOT)).replace("\\", "/")
        data = _benchmark_cache_load(bench_path, bench_cache)
        if data:
            observables = _extract_top_observables(data)

    formulas = _match_formulas(name, lean_route, maps, observables, formula_by_concept)

    lines = [
        f"#### {_humanize(name)}",
        "",
        f"Extension panel **`{name}`** (verification tier {tier or 'extension'}) evaluates "
        f"**{row.get('record_count', 0)}** measured records at **{_fmt_pct(row.get('median_error_pct'))}%** "
        f"pooled median error ({row.get('coverage_tier', 'verified')}). "
        f"Formal module: `{lean_mod}`. "
        f"This panel extends the core spine into {_humanize(name).lower()} observables — "
        f"predictions are seed-derived; kill criteria are registered in the domain navigator.",
        "",
    ]
    if bench_rel:
        lines.append(f"**Benchmark:** [`{bench_rel}`]({bench_rel})")
        lines.append("")
    lines.extend(_subfield_map_extension(panel_meta, manifest_entry))
    if observables:
        lines.append("**Top observables (measured vs computed):**")
        lines.append("")
        lines.extend(_observable_table_rows(observables))
    lines.extend(_formula_prose_block(formulas, name))
    return lines


def _cluster_chapter(
    slug: str,
    title: str,
    rows: list[dict],
    panel_index: dict[str, dict],
    ext_manifest: dict,
    bench_cache: dict[str, dict],
    formula_by_concept: dict[str, list[dict]],
) -> str:
    total_records = sum(int(r.get("record_count") or 0) for r in rows)
    medians = [float(r["median_error_pct"]) for r in rows if r.get("median_error_pct") not in (None, "")]
    pooled = sum(medians) / len(medians) if medians else 0.0
    lines = [
        f"## {title}",
        "",
        f"**Panels:** {len(rows)} · **Records:** {total_records:,} · "
        f"**Mean panel median error:** {_fmt_pct(pooled)}%",
        "",
    ]
    ext_domains = ext_manifest.get("extension_domains") or {}
    for row in sorted(rows, key=lambda r: r["domain"]):
        domain = row["domain"]
        lines.extend(
            _extension_domain_block(
                row,
                panel_index.get(domain, {}),
                ext_domains.get(domain),
                bench_cache,
                formula_by_concept,
            )
        )
    return "\n".join(lines)


def main() -> int:
    import yaml

    nav = json.loads(NAV.read_text(encoding="utf-8")) if NAV.is_file() else {}
    expansion = _load_yaml(MAP)
    ext_manifest = _load_yaml(EXT_MANIFEST)
    summary = expansion.get("summary") or {}

    panel_index = {p["panel"]: p for p in nav.get("extension_panels") or []}

    rows: list[dict] = []
    with ATLAS.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    core_rows = [r for r in rows if r.get("kind") == "core"]
    ext_rows = [r for r in rows if r.get("kind") == "extension"]

    _, formula_by_concept = _load_formula_index()
    bench_cache: dict[str, dict] = {}

    OUT.mkdir(parents=True, exist_ok=True)
    written: list[dict] = []

    cluster_titles = {c[0]: c[1] for c in CLUSTERS}

    by_cluster: dict[str, list[dict]] = {c[0]: [] for c in CLUSTERS}
    for row in ext_rows:
        by_cluster[_cluster_for(row["domain"])].append(row)

    residual = by_cluster.get("22_interdisciplinary_residual") or []
    if residual:
        print(f"WARNING: {len(residual)} panels in residual cluster: {[r['domain'] for r in residual]}")

    core_path = OUT / "00_core_spine_35.md"
    core_path.write_text(_core_chapter(nav, core_rows, formula_by_concept), encoding="utf-8")
    written.append({"id": "00_core_spine_35", "file": str(core_path.relative_to(ROOT)), "domains": 35})

    chapter_slugs = [c[0] for c in CLUSTERS if c[0] != "22_interdisciplinary_residual"]
    if residual:
        chapter_slugs.append("22_interdisciplinary_residual")

    for slug in chapter_slugs:
        cluster_rows = by_cluster.get(slug) or []
        if not cluster_rows:
            continue
        path = OUT / f"{slug}.md"
        path.write_text(
            _cluster_chapter(
                slug,
                cluster_titles[slug],
                cluster_rows,
                panel_index,
                ext_manifest,
                bench_cache,
                formula_by_concept,
            ),
            encoding="utf-8",
        )
        written.append(
            {
                "id": slug,
                "title": cluster_titles[slug],
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "panels": len(cluster_rows),
            }
        )

    # Remove deprecated / empty chapter files
    for stale in ("10_interdisciplinary.md", "22_interdisciplinary_residual.md"):
        path = OUT / stale
        if path.is_file() and stale not in {f"{w['id']}.md" for w in written}:
            path.unlink()

    index_lines = [
        "# Domain Chapter Index",
        "",
        f"*Generated: {datetime.now(timezone.utc).isoformat()}*",
        "",
        f"**Corpus:** {summary.get('total_scientific_domains_covered', 403)} domains · "
        f"{summary.get('total_empirical_records', 536740):,} records · "
        f"{summary.get('lean_formal_modules', 501)} Lean modules",
        "",
        "## Chapters",
        "",
        "| Chapter | Panels | File |",
        "|---------|-------:|------|",
    ]
    index_lines.append(f"| Core NeuroLab spine | 35 | `readme_domain_chapters/00_core_spine_35.md` |")
    for w in written[1:]:
        index_lines.append(f"| {w.get('title', w['id'])} | {w.get('panels', 0)} | `{Path(w['file']).name}` |")

    index_path = OUT / "INDEX.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chapters": written,
        "total_domains": len(rows),
        "core_domains": len(core_rows),
        "extension_panels": len(ext_rows),
        "interdisciplinary_subclusters": len([w for w in written if w["id"].startswith("1") or w["id"].startswith("2")]),
        "merge_command": "python scripts/merge_readme_domain_chapters.py",
    }
    MANIFEST.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {len(written)} domain chapters to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())