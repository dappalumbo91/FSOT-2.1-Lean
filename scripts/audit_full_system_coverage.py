#!/usr/bin/env python3
"""Full FSOT system coverage audit — core 35, extensions, depth vs field breadth."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "full_system_coverage_audit.json"

# Approximate share of major subfields touched (honest editorial estimate for audit display)
FIELD_BREADTH: dict[str, dict] = {
    "Particle_Physics": {"studied_subfields": 12, "touched": 4, "note": "PDG/Higgs/CERN; thin on neutrino oscillation, lattice QCD"},
    "Quantum_Mechanics": {"studied_subfields": 10, "touched": 3, "note": "NIST constants; thin on entanglement benchmarks, decoherence"},
    "Atomic_Physics": {"studied_subfields": 8, "touched": 3, "note": "CODATA + periodic table; thin on Rydberg molecules, laser cooling"},
    "Physical_Chemistry": {"studied_subfields": 10, "touched": 4, "note": "PubChem thermochem; thin on kinetics, surface chem"},
    "Chemistry": {"studied_subfields": 15, "touched": 6, "note": "PubChem/CRC; thin on organometallic, solid-state synth"},
    "Electromagnetism": {"studied_subfields": 9, "touched": 4, "note": "GOES x-ray, geomagnetism; thin on antenna theory, plasmonics"},
    "Molecular_Chemistry": {"studied_subfields": 8, "touched": 4, "note": "SMILES/PDB; thin on conformer ensembles"},
    "Optics": {"studied_subfields": 9, "touched": 4, "note": "Interferometry depth — LIGO/JWST reference + MAST em wavelengths"},
    "Acoustics": {"studied_subfields": 7, "touched": 2, "note": "SMILES relay; thin on sonar, architectural acoustics"},
    "Quantum_Computing": {"studied_subfields": 8, "touched": 6, "note": "Math-first QC depth — gate fidelity, error correction, formal rules; physical QC verifies"},
    "Quantum_Optics": {"studied_subfields": 7, "touched": 2, "note": "Cross-domain; thin on squeezed light, cavity QED"},
    "Biology": {"studied_subfields": 20, "touched": 6, "note": "UniProt/GBIF/NCBI; thin on developmental, structural bio"},
    "Thermodynamics": {"studied_subfields": 8, "touched": 4, "note": "Fuel/NIST; thin on non-equilibrium, phase diagrams"},
    "Biochemistry": {"studied_subfields": 12, "touched": 5, "note": "PDB/ChEMBL/ClinicalTrials; thin on metabolomics"},
    "Neuroscience": {"studied_subfields": 15, "touched": 7, "note": "Connectomics depth panel — neuron cohort strata + catalog coverage + OpenNeuro"},
    "Condensed_Matter": {"studied_subfields": 14, "touched": 5, "note": "Superconductivity Tc depth — literature + breakthrough + quantum materials"},
    "Fluid_Dynamics": {"studied_subfields": 10, "touched": 4, "note": "Fluid spacetime + HVAC; thin on turbulence DNS"},
    "Nuclear_Physics": {"studied_subfields": 10, "touched": 4, "note": "OSTI/HEP; thin on cross-section databases"},
    "Ecology": {"studied_subfields": 12, "touched": 5, "note": "GBIF/iNaturalist; thin on food-web, population dynamics"},
    "Meteorology": {"studied_subfields": 10, "touched": 5, "note": "Open-Meteo/NDBC; thin on NWP ensemble verification"},
    "Materials_Science": {"studied_subfields": 14, "touched": 5, "note": "Materials Project bundled; thin on creep, fracture"},
    "Psychology": {"studied_subfields": 12, "touched": 3, "note": "OpenAlex/citations; thin on psychometrics, RCT outcomes"},
    "Atmospheric_Physics": {"studied_subfields": 10, "touched": 4, "note": "Weather/climate; thin on aerosol microphysics"},
    "Oceanography": {"studied_subfields": 11, "touched": 5, "note": "NOAA tides/NDBC; thin on ARGO float profiles"},
    "Seismology": {"studied_subfields": 8, "touched": 5, "note": "USGS deep catalog; thin on full moment-tensor relay"},
    "Sociology": {"studied_subfields": 10, "touched": 3, "note": "UAP years/registry; thin on survey panels, networks"},
    "High_Energy_Physics": {"studied_subfields": 9, "touched": 5, "note": "CERN/GWOSC/Higgs; thin on B-physics, jet substructure"},
    "Geophysics": {"studied_subfields": 11, "touched": 5, "note": "USGS/seismology/grace; thin on magnetotellurics"},
    "Astronomy": {"studied_subfields": 15, "touched": 7, "note": "Gaia/SIMBAD/MAST/WDS; thin on radio VLBI"},
    "Economics": {"studied_subfields": 10, "touched": 4, "note": "World Bank/Crossref; thin on macro VAR, trade gravity"},
    "Planetary_Science": {"studied_subfields": 12, "touched": 6, "note": "Exoplanet/JPL NEO/Horizons; thin on regolith, atm chemistry"},
    "Quantum_Gravity": {"studied_subfields": 6, "touched": 2, "note": "Scaffold/crosswalk; thin on LQG observables"},
    "Particle_Astrophysics": {"studied_subfields": 10, "touched": 5, "note": "GWOSC/UAP; thin on cosmic-ray spectrum"},
    "Astrophysics": {"studied_subfields": 14, "touched": 6, "note": "Stellar/galactic; thin on stellar evolution grids"},
    "Cosmology": {"studied_subfields": 12, "touched": 7, "note": "CMB/bubble-bleed/H0; thin on BAO full survey ingest"},
    "Volcanology": {"studied_subfields": 8, "touched": 2, "note": "GVP/USGS geohazard; thin on gas geochemistry, lahars"},
    "Limnology": {"studied_subfields": 9, "touched": 2, "note": "USGS NWIS lakes; thin on paleolimnology, food-web"},
    "Radio_Astronomy": {"studied_subfields": 10, "touched": 2, "note": "VizieR NVSS; thin on VLBI, polarization"},
    "Petrology_Geochemistry": {"studied_subfields": 10, "touched": 2, "note": "EarthChem oxides; thin on isotope thermometry"},
    "Actuarial_Science": {"studied_subfields": 8, "touched": 2, "note": "SSA mortality; thin on catastrophe, annuity"},
    "Ethology": {"studied_subfields": 9, "touched": 2, "note": "Movement/migration; thin on cognition, signaling"},
    "Toxicology": {"studied_subfields": 10, "touched": 2, "note": "PubChem BioAssay; thin on ADME, in vivo LD50"},
    "Soil_Science": {"studied_subfields": 11, "touched": 2, "note": "ISRIC SoilGrids; thin on pedogenesis, microbiome"},
    "Neutrino_Physics": {"studied_subfields": 8, "touched": 2, "note": "PDG oscillation params; thin on sterile, CEνNS"},
    "Cartography_GIS": {"studied_subfields": 9, "touched": 2, "note": "Natural Earth; thin on topology, remote sensing"},
}

UNENTERED_CANDIDATES = [
    {
        "domain": "Epidemiology",
        "fsot_nearest": "Medical / Biochemistry",
        "public_api": "https://data.cdc.gov/ (Socrata open data, no key)",
        "why": "Disease incidence, R0, vaccination coverage — independent public-health validation",
    },
    {
        "domain": "Virology",
        "fsot_nearest": "Biology / Immunology",
        "public_api": "https://www.ncbi.nlm.nih.gov/genbank/ + Virus Pathogen DB",
        "why": "Genome length, mutation rate — complements NCBI gene panel",
    },
    {
        "domain": "Paleontology",
        "fsot_nearest": "Geology / Ecology",
        "public_api": "https://paleobiodb.org/data1.2/ (PBDB public API)",
        "why": "Fossil occurrence depth/age — deep-time cross-check vs climate",
    },
    {
        "domain": "Volcanology",
        "fsot_nearest": "Geophysics / Seismology",
        "public_api": "https://volcano.si.edu/database/ + USGS volcano API",
        "why": "VEI, eruption chronology — geohazard independent channel",
    },
    {
        "domain": "Limnology",
        "fsot_nearest": "Hydrology / Ecology",
        "public_api": "https://waterservices.usgs.gov/ (lake sites) + EPA STORET",
        "why": "Freshwater chemistry — fills gap between ocean and streamflow",
    },
    {
        "domain": "Radio_Astronomy",
        "fsot_nearest": "Astronomy / Astrophysics",
        "public_api": "https://archive.nrao.edu/ + VizieR radio catalogs",
        "why": "Flux density, spectral index — optical-heavy astronomy balance",
    },
    {
        "domain": "Petrology_Geochemistry",
        "fsot_nearest": "Geochemistry / Materials_Science",
        "public_api": "https://earthchem.org/ + OpenGEOTHERM",
        "why": "Melt inclusion chemistry, isotope ratios — solid-earth gap",
    },
    {
        "domain": "Actuarial_Science",
        "fsot_nearest": "Economics / Statistics",
        "public_api": "https://www.ssa.gov/oact/STATS/ (public mortality tables)",
        "why": "Mortality/life-table scalars — independent of World Bank macro",
    },
    {
        "domain": "Ethology",
        "fsot_nearest": "Ecology / Zoology",
        "public_api": "https://www.movebank.org/ (animal tracking, public subset)",
        "why": "Movement speed, migration distance — behavioral ecology layer",
    },
    {
        "domain": "Arxiv_Gravitational_Waves_Theory",
        "fsot_nearest": "Particle_Astrophysics",
        "public_api": "http://export.arxiv.org/api/query (gr-qc, no key)",
        "why": "Preprint metadata crosswalk — complements GWOSC events",
    },
]


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")

    coverage = json.loads((ROOT / "data" / "domain_coverage_report.json").read_text(encoding="utf-8"))
    sci = json.loads((ROOT / "data" / "scientific_domain_expansion_map.json").read_text(encoding="utf-8"))
    ext = yaml.safe_load((ROOT / "data" / "extension_domains_manifest.yaml").read_text(encoding="utf-8"))

    ext_domains = ext.get("extension_domains") or {}
    fsot_by_panel: dict[str, list[dict]] = defaultdict(list)

    for name, cfg in ext_domains.items():
        bench_path = ROOT / cfg["benchmark_data"]
        rec = int(0)
        pooled = None
        if bench_path.exists():
            bench = json.loads(bench_path.read_text(encoding="utf-8"))
            rec = int(bench.get("record_count") or bench.get("observable_count") or 0)
            pooled = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        for row in (bench_path.exists() and json.loads(bench_path.read_text(encoding="utf-8")).get("material_records") or []):
            fd = row.get("fsot_domain")
            if fd:
                fsot_by_panel[fd].append({"panel": name, "property": row.get("property")})
        fsot_by_panel  # material_records scan above is partial; use bench only

    # Aggregate fsot_domain from all benchmarks
    domain_records: dict[str, int] = defaultdict(int)
    domain_panels: dict[str, set[str]] = defaultdict(set)
    for name, cfg in ext_domains.items():
        bench_path = ROOT / cfg["benchmark_data"]
        if not bench_path.exists():
            continue
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        for row in (bench.get("material_records") or bench.get("records") or []):
            fd = row.get("fsot_domain")
            if fd:
                domain_records[fd] += 1
                domain_panels[fd].add(name)

    core_audit = []
    for dom in coverage.get("domains") or []:
        name = dom["neurolab_domain"]
        breadth = FIELD_BREADTH.get(name, {"studied_subfields": 8, "touched": 2, "note": "estimate pending"})
        touched = breadth["touched"]
        studied = breadth["studied_subfields"]
        pct = round(100.0 * touched / max(studied, 1), 1)
        core_audit.append(
            {
                "fsot_core_domain": name,
                "empirical_records": dom.get("empirical_records"),
                "median_error_pct": dom.get("empirical_median_error_pct"),
                "extension_panels_routing_here": len(domain_panels.get(name, set())),
                "fsot_prediction_records_in_extensions": domain_records.get(name, 0),
                "field_subfields_studied_in_discipline": studied,
                "subfields_touched_by_fsot": touched,
                "coverage_vs_field_pct": pct,
                "depth_note": breadth.get("note"),
                "coverage_tier": next(
                    (x.get("coverage_tier") for x in sci.get("neurolab_domains") or [] if x.get("domain") == name),
                    None,
                ),
            }
        )

    ext_list = []
    for name, cfg in sorted(ext_domains.items(), key=lambda x: x[1].get("tier", 0)):
        bench_path = ROOT / cfg["benchmark_data"]
        rec = pooled = None
        if bench_path.exists():
            bench = json.loads(bench_path.read_text(encoding="utf-8"))
            rec = bench.get("record_count") or bench.get("observable_count")
            pooled = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        ext_list.append(
            {
                "panel": name,
                "tier": cfg.get("tier"),
                "records": rec,
                "pooled_median_error_pct": pooled,
                "observed": cfg.get("observed"),
                "ingest": cfg.get("ingest_script") or cfg.get("ingest"),
            }
        )

    audit = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "fsot_formula_core_domains": 35,
            "core_domains_with_empirical_data": coverage.get("domains_with_empirical_data"),
            "core_total_empirical_records": coverage.get("total_empirical_records"),
            "extension_panels_verified": len(ext_domains),
            "total_scientific_surface": sci.get("summary", {}).get("total_scientific_domains_covered"),
            "tier_A_strong": sci.get("summary", {}).get("tier_distribution", {}).get("A_strong"),
            "tier_B_verified": sci.get("summary", {}).get("tier_distribution", {}).get("B_verified"),
            "tier_C_thin": sci.get("summary", {}).get("tier_distribution", {}).get("C_thin"),
            "lean_formal_modules": sci.get("summary", {}).get("lean_formal_modules"),
            "credential_free_policy": "scripts/public_api_policy.py",
        },
        "core_35_depth_audit": sorted(core_audit, key=lambda x: x.get("coverage_vs_field_pct", 0)),
        "extension_panel_index": ext_list,
        "ten_unentered_domain_candidates": UNENTERED_CANDIDATES,
    }
    OUT.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  core: 35 | extensions: {len(ext_domains)} | total surface: {audit['summary']['total_scientific_surface']}")
    print(f"  records: {audit['summary']['core_total_empirical_records']}")
    thin = [d for d in core_audit if d["coverage_vs_field_pct"] < 35]
    print(f"  thinnest core domains (<35% field breadth): {[d['fsot_core_domain'] for d in thin[:8]]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())