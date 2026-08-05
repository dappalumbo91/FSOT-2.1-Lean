# Benchmark data citations & public anchors

**Generated:** `2026-08-05T14:42:38.052072+00:00`  
**Panels scanned:** 432  
**Unique resolved anchors:** 833  
**API registry entries:** 36 · open-science no-key: 20

This ledger supports **multiprover + empirical reproducibility**: measured targets 
are tied to **public datasets, APIs, or literature landing pages**, not private files.

## Policy

| Case | How we cite |
|------|-------------|
| Full catalog (e.g. MPCORB / Harvard–CfA MPC) | One dataset entry + official URL |
| Individual public tables | Each named source + URL when known |
| Live API ingest | API id + base URL from `data/api_requirements.yaml` |
| Portable vendor cache | In-repo path + ingest script to rebuild from public net |

## Kind summary

| Kind | Count |
|------|------:|
| `dataset` | 690 |
| `unresolved` | 417 |
| `vendor_cache` | 373 |
| `process` | 331 |
| `literature` | 313 |
| `software` | 161 |
| `api` | 155 |
| `ingest_script` | 130 |
| `url` | 11 |

## Global public anchors (deduplicated)

| Kind | Title | URL / location | # panels |
|------|-------|----------------|---------:|
| api | AlphaFold DB prediction metadata (P53) | https://alphafold.ebi.ac.uk/api/prediction/P04637 | 1 |
| api | ChEMBL API | https://www.ebi.ac.uk/chembl/ | 5 |
| api | Crossref funders (open) | https://api.crossref.org/funders?query=national+science+foundation&rows=3 | 1 |
| api | Ensembl REST API | https://rest.ensembl.org/ | 1 |
| api | FDA open drug labeling records | https://api.fda.gov/drug/label.json?limit=5 | 1 |
| api | GBIF Occurrence API | https://api.gbif.org/v1/ | 13 |
| api | GWAS Catalog studies (EBI) | https://www.ebi.ac.uk/gwas/rest/api/studies?size=5 | 1 |
| api | JPL Horizons system | https://ssd.jpl.nasa.gov/horizons/ | 2 |
| api | JPL Solar System Dynamics / Horizons | https://ssd.jpl.nasa.gov/ | 5 |
| api | NASA Exoplanet Archive TAP | https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html | 1 |
| api | NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) | https://api.nasa.gov/ | 8 |
| api | NCBI E-utilities / Gene / datasets | https://www.ncbi.nlm.nih.gov/books/NBK25501/ | 5 |
| api | NCBI PubMed eSearch (open eutils) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Hubble+tension&retmode=json&retmax=5 | 1 |
| api | NOAA tides, climate, space-weather open services | https://www.noaa.gov/ | 9 |
| api | Open-Meteo weather API / archive | https://open-meteo.com/ | 6 |
| api | OpenAlex scholarly graph API | https://api.openalex.org/ | 8 |
| api | Our World in Data CO2 codebook (GitHub raw) | https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv | 1 |
| api | PubChem PUG REST | https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest | 13 |
| api | RCSB PDB REST API | https://data.rcsb.org/ | 2 |
| api | STRING protein network API version | https://string-db.org/api/json/version | 1 |
| api | USGS earthquake / water / hazards open APIs | https://earthquake.usgs.gov/fdsnws/event/1/ | 10 |
| api | UniProt REST API | https://www.uniprot.org/help/api | 1 |
| api | Wikidata entity for π | https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q167&format=json | 1 |
| api | World Bank Open Data Indicators API | https://api.worldbank.org/v2/ | 17 |
| api | World Bank population indicator | https://api.worldbank.org/v2/country/USA/indicator/SP.POP.TOTL?format=json&per_page=5 | 1 |
| api | Zenodo open research records (physics) | https://zenodo.org/api/records/?q=subject:physics&size=3&sort=mostrecent | 1 |
| api | anage | https://genomics.senescence.info/species/dataset.zip | 4 |
| api | arXiv API / metadata | https://arxiv.org/help/api/ | 5 |
| api | obis | https://api.obis.org/v3/occurrence | 2 |
| api | openneuro | https://openneuro.org/crn/graphql | 2 |
| dataset | BRENDA enzyme database | https://www.brenda-enzymes.org/ | 20 |
| dataset | CERN Open Data | https://opendata.cern.ch/ | 3 |
| dataset | GitHub OSS corpus JetBrains/kotlin | https://github.com/JetBrains/kotlin | 1 |
| dataset | GitHub OSS corpus USGS/GVP | https://github.com/USGS/GVP | 1 |
| dataset | GitHub OSS corpus WDS/literature | https://github.com/WDS/literature | 1 |
| dataset | GitHub OSS corpus apple/swift | https://github.com/apple/swift | 1 |
| dataset | GitHub OSS corpus data/acoustic_resonance_materials_benchmark.json | https://github.com/data/acoustic_resonance_materials_benchmark.json | 3 |
| dataset | GitHub OSS corpus data/adjacent_rung_coupling_benchmark.json | https://github.com/data/adjacent_rung_coupling_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/adversarial_fractal_break_benchmark.json | https://github.com/data/adversarial_fractal_break_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/agriculture_agroecology_gap_fill_benchmark.json | https://github.com/data/agriculture_agroecology_gap_fill_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/ai_galactic_orbital_bridge_benchmark.json | https://github.com/data/ai_galactic_orbital_bridge_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/alternate_base_mathematics_explorer_panel_benchmark.json | https://github.com/data/alternate_base_mathematics_explorer_panel_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/alternate_base_mathematics_spine_benchmark.json | https://github.com/data/alternate_base_mathematics_spine_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/anthropology_extension_benchmark.json | https://github.com/data/anthropology_extension_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/architecture_building_science_gap_fill_benchmark.json | https://github.com/data/architecture_building_science_gap_fill_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/arxiv_brain_knowledge_panel_benchmark.json | https://github.com/data/arxiv_brain_knowledge_panel_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/arxiv_primitives_panel_benchmark.json | https://github.com/data/arxiv_primitives_panel_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/arxiv_primitives_v14_benchmark.json | https://github.com/data/arxiv_primitives_v14_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/astrophysical_structure_crosswalk_benchmark.json | https://github.com/data/astrophysical_structure_crosswalk_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/atomic_physics_gap_fill_benchmark.json | https://github.com/data/atomic_physics_gap_fill_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/bibliography_lean_corpus_benchmark.json | https://github.com/data/bibliography_lean_corpus_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/binary_decoder_rendlesham_benchmark.json | https://github.com/data/binary_decoder_rendlesham_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/biological_cuda_physarum_benchmark.json | https://github.com/data/biological_cuda_physarum_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/biology_developmental_structural_depth_panel_benchmark.json | https://github.com/data/biology_developmental_structural_depth_panel_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/biology_strict_empirical.json | https://github.com/data/biology_strict_empirical.json | 1 |
| dataset | GitHub OSS corpus data/boundary_partition_tightening_benchmark.json | https://github.com/data/boundary_partition_tightening_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/breakthrough_discoveries_2024_2026_benchmark.json | https://github.com/data/breakthrough_discoveries_2024_2026_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/canonical_constants.json | https://github.com/data/canonical_constants.json | 1 |
| dataset | GitHub OSS corpus data/chaos_mediated_phase_transitions_benchmark.json | https://github.com/data/chaos_mediated_phase_transitions_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/climate_observed_benchmark.json | https://github.com/data/climate_observed_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/consciousness_econ_benchmark.json | https://github.com/data/consciousness_econ_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/consciousness_reference_observables.json | https://github.com/data/consciousness_reference_observables.json | 2 |
| dataset | GitHub OSS corpus data/consciousness_resonance_reference.json | https://github.com/data/consciousness_resonance_reference.json | 1 |
| dataset | GitHub OSS corpus data/consciousness_soul_bridge_reference.json | https://github.com/data/consciousness_soul_bridge_reference.json | 1 |
| dataset | GitHub OSS corpus data/cosmology_extended_benchmark.json | https://github.com/data/cosmology_extended_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/culinary_recipe_observables.json | https://github.com/data/culinary_recipe_observables.json | 1 |
| dataset | GitHub OSS corpus data/dark_energy_cpl_reference.json | https://github.com/data/dark_energy_cpl_reference.json | 1 |
| dataset | GitHub OSS corpus data/external_oss_code_genome_benchmark.json | https://github.com/data/external_oss_code_genome_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/founding_unmapped_laws_reference.json | https://github.com/data/founding_unmapped_laws_reference.json | 7 |
| dataset | GitHub OSS corpus data/higgs_mass_benchmark.json | https://github.com/data/higgs_mass_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/higgs_mass_reference_observables.json | https://github.com/data/higgs_mass_reference_observables.json | 1 |
| dataset | GitHub OSS corpus data/immunology_benchmark.json | https://github.com/data/immunology_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/materials_species_bridge_benchmark.json | https://github.com/data/materials_species_bridge_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/observer_channel_derivation_benchmark.json | https://github.com/data/observer_channel_derivation_benchmark.json | 2 |
| dataset | GitHub OSS corpus data/particle_physics_gap_fill_benchmark.json | https://github.com/data/particle_physics_gap_fill_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/planetary_jpl_cache.json | https://github.com/data/planetary_jpl_cache.json | 1 |
| dataset | GitHub OSS corpus data/planetary_structure_benchmark.json | https://github.com/data/planetary_structure_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/programming_language_laws_benchmark.json | https://github.com/data/programming_language_laws_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/quantum_computing_math_depth_panel_benchmark.json | https://github.com/data/quantum_computing_math_depth_panel_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/sector_h0_seed.json | https://github.com/data/sector_h0_seed.json | 3 |
| dataset | GitHub OSS corpus data/sh0es_host_coordinates.json | https://github.com/data/sh0es_host_coordinates.json | 1 |
| dataset | GitHub OSS corpus data/stumped_observables_reference.json | https://github.com/data/stumped_observables_reference.json | 2 |
| dataset | GitHub OSS corpus data/symbolic_archetype_reference.json | https://github.com/data/symbolic_archetype_reference.json | 1 |
| dataset | GitHub OSS corpus data/synthetic_biology_benchmark.json | https://github.com/data/synthetic_biology_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/trinary_os_isa_rebuild_benchmark.json | https://github.com/data/trinary_os_isa_rebuild_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/trinary_os_manifest.yaml | https://github.com/data/trinary_os_manifest.yaml | 1 |
| dataset | GitHub OSS corpus data/trinary_os_portable_benchmark.json | https://github.com/data/trinary_os_portable_benchmark.json | 1 |
| dataset | GitHub OSS corpus data/trinary_os_round_trip_benchmark.json | https://github.com/data/trinary_os_round_trip_benchmark.json | 1 |
| dataset | GitHub OSS corpus docs/CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md | https://github.com/docs/CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md | 1 |
| dataset | GitHub OSS corpus docs/ENGINEERING_HARDWARE_CODE_DIRECTION.md | https://github.com/docs/ENGINEERING_HARDWARE_CODE_DIRECTION.md | 1 |
| dataset | GitHub OSS corpus docs/NEURON_ZIG_TO_OS_ROADMAP.md | https://github.com/docs/NEURON_ZIG_TO_OS_ROADMAP.md | 1 |
| dataset | GitHub OSS corpus docs/OPH_FSOT_CHALLENGE_RESPONSE.md | https://github.com/docs/OPH_FSOT_CHALLENGE_RESPONSE.md | 1 |
| dataset | GitHub OSS corpus docs/T3_T4_GR_SM_DEEPENING.md | https://github.com/docs/T3_T4_GR_SM_DEEPENING.md | 1 |
| dataset | GitHub OSS corpus docs/TOE_CLAIM_BOUNDARIES.md | https://github.com/docs/TOE_CLAIM_BOUNDARIES.md | 1 |
| dataset | GitHub OSS corpus expressjs/express | https://github.com/expressjs/express | 1 |
| dataset | GitHub OSS corpus facebook/react | https://github.com/facebook/react | 1 |
| dataset | GitHub OSS corpus golang/go | https://github.com/golang/go | 1 |
| dataset | GitHub OSS corpus haskell/bytestring | https://github.com/haskell/bytestring | 1 |
| dataset | GitHub OSS corpus kubernetes/client-go | https://github.com/kubernetes/client-go | 1 |
| dataset | GitHub OSS corpus leanprover/lean4 | https://github.com/leanprover/lean4 | 1 |
| dataset | GitHub OSS corpus nodejs/node | https://github.com/nodejs/node | 2 |
| dataset | GitHub OSS corpus openjdk/jdk | https://github.com/openjdk/jdk | 1 |
| dataset | GitHub OSS corpus openssl/openssl | https://github.com/openssl/openssl | 5 |
| dataset | GitHub OSS corpus parity/golden.json | https://github.com/parity/golden.json | 4 |
| dataset | GitHub OSS corpus psutil/host | https://github.com/psutil/host | 2 |
| dataset | GitHub OSS corpus python/cpython | https://github.com/python/cpython | 2 |
| dataset | GitHub OSS corpus pytorch/pytorch | https://github.com/pytorch/pytorch | 1 |
| dataset | GitHub OSS corpus redis/redis | https://github.com/redis/redis | 1 |
| dataset | GitHub OSS corpus rust-lang/rust | https://github.com/rust-lang/rust | 3 |
| dataset | GitHub OSS corpus scripts/build_cosmology_bubble_bleed_benchmark.py | https://github.com/scripts/build_cosmology_bubble_bleed_benchmark.py | 1 |
| dataset | GitHub OSS corpus scripts/consciousness_econ_lib.py | https://github.com/scripts/consciousness_econ_lib.py | 1 |
| dataset | GitHub OSS corpus scripts/consciousness_soul_bridge_lib.py | https://github.com/scripts/consciousness_soul_bridge_lib.py | 1 |
| dataset | GitHub OSS corpus scripts/dark_energy_dual_readout_lib.py | https://github.com/scripts/dark_energy_dual_readout_lib.py | 3 |
| dataset | GitHub OSS corpus scripts/higgs_mass_formula_eval.py | https://github.com/scripts/higgs_mass_formula_eval.py | 2 |
| dataset | GitHub OSS corpus scripts/math_generator_benchmark_formula_eval.py | https://github.com/scripts/math_generator_benchmark_formula_eval.py | 1 |
| dataset | GitHub OSS corpus scripts/symbolic_archetype_lib.py | https://github.com/scripts/symbolic_archetype_lib.py | 1 |
| dataset | GitHub OSS corpus simonmar/async | https://github.com/simonmar/async | 1 |
| dataset | GitHub OSS corpus sqlite/sqlite | https://github.com/sqlite/sqlite | 1 |
| dataset | GitHub OSS corpus torvalds/linux | https://github.com/torvalds/linux | 4 |
| dataset | GitHub OSS corpus vendor/bibliography_corpus | https://github.com/vendor/bibliography_corpus | 1 |
| dataset | GitHub OSS corpus vendor/certified_agent | https://github.com/vendor/certified_agent | 1 |
| dataset | GitHub OSS corpus vendor/cybersecurity | https://github.com/vendor/cybersecurity | 1 |
| dataset | GitHub OSS corpus vendor/formula_corpus_cnc | https://github.com/vendor/formula_corpus_cnc | 1 |
| dataset | GitHub OSS corpus vendor/fsot_compute.py | https://github.com/vendor/fsot_compute.py | 9 |
| dataset | GitHub OSS corpus vendor/physarum | https://github.com/vendor/physarum | 1 |
| dataset | GitHub OSS corpus vendor/propulsion_electrical | https://github.com/vendor/propulsion_electrical | 1 |
| dataset | GitHub OSS corpus vendor/public_data | https://github.com/vendor/public_data | 1 |
| dataset | GitHub OSS corpus vendor/reference_anchors | https://github.com/vendor/reference_anchors | 1 |
| dataset | GitHub OSS corpus vendor/rust_lean_bridge | https://github.com/vendor/rust_lean_bridge | 1 |
| dataset | GitHub OSS corpus vendor/thesis | https://github.com/vendor/thesis | 1 |
| dataset | GitHub OSS corpus vendor/tokenization | https://github.com/vendor/tokenization | 1 |
| dataset | GitHub OSS corpus vendor/trinary_os | https://github.com/vendor/trinary_os | 4 |
| dataset | GitHub OSS corpus vendor/vl_distill | https://github.com/vendor/vl_distill | 1 |
| dataset | GitHub OSS corpus ziglang/zig | https://github.com/ziglang/zig | 1 |
| dataset | Minor Planet Center Orbit Database (MPCORB) | https://minorplanetcenter.net/data | 7 |
| dataset | Minor Planet Center data services | https://minorplanetcenter.net/ | 7 |
| dataset | NASA Kepler / exoplanet archives (as cited per panel) | https://exoplanetarchive.ipac.caltech.edu/ | 1 |
| dataset | NIST CODATA / Constants | https://physics.nist.gov/cuu/Constants/ | 107 |
| dataset | NIST CODATA recommended values (ASCII table) | https://physics.nist.gov/cuu/Constants/Table/allascii.txt | 7 |
| dataset | NOAA NCEI climate data | https://www.ncei.noaa.gov/ | 1 |
| dataset | Particle Data Group Review of Particle Physics | https://pdg.lbl.gov/ | 9 |
| dataset | Planck Collaboration cosmological parameters | https://www.cosmos.esa.int/web/planck | 4 |
| dataset | SSA Office of the Chief Actuary life tables | https://www.ssa.gov/oact/STATS/table4c6.html | 1 |
| dataset | vendor/formula_corpus/by_domain/strict_empirical.jsonl | https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl | 103 |
| literature | Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) | https://www.nist.gov/pml/journal-physical-and-chemical-reference-data | 42 |
| literature | Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution | https://www.routledge.com/ | 74 |
| literature | Long & Greenwood (1997) — materials / thermoelectric class reference | https://ui.adsabs.harvard.edu/ | 71 |
| literature | Snyder & Toberer, Nature Materials 7, 105 (2008) | https://doi.org/10.1038/nmat2090 | 68 |
| software | FSOT scalar authority (pin D1D38A) | https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py | 120 |
| unresolved | 4 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | 9_language_bridges | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | AHA/ESC cardiology reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ASCE/structural engineering reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ASHRAE_HVAC | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ASM International | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ASME mechanical engineering reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Adjacent_Rung_Coupling | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Adversarial_Fractal_Break_Tests | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Behavioral neuroeconomics reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | BlackHoleThesisPriors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | C:\Users\damia\Desktop\FSOT-2.1-Lean\verification\c\fsot_pack_parity\fsot_pack_parity.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | C:\Users\damia\Desktop\fsot code language | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star | Named in panel source; add explicit public URL if this is an external authority | 4 |
| unresolved | CRC Handbook | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | CRYPTOGRAPHY_RULES | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | CVE_CWE_shape | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Compactification_Ladder | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Cosmology_Anomalies | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Crossref history corpus | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Danio rerio | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Dark_Sector_Open_Problems | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | EarthChem subset | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | FLUID_MECHANICS_rules | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | FPC_Temporal_Coupling | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | FSOT.Formal.Cosmology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | FSOT.Formal.Scalar.consciousness_factor | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | FSOT/Formal/*Priors.lean | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Fold_Depth_Metrics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Fractal_Constant_Recursion | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | G:\FSOT-PublicData\trinary_os | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | GFZ_GravIS_Greenland_total | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | GR Schwarzschild vs FPC whirlpool horizon stack | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | GR dτ/dt at r=3M (photon sphere), M Schwarzschild mass | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Greenwich τ anchor — longitude is θ phase label, not rate multiplier | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Hubble_Bubble_Tension | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | I:\FSOT-Physical-Archive\08_Verified-Desktop-Projects\fuel_lab\engine_simulator\REAL_DATA_PROVENANCE.md | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | I:\Protofluid-Language-Translator-2.0-Zig | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | I:\fsot-neuron-zig | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | IEEE robotics reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | IERS Earth sidereal | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | IERS Earth sidereal + NULL Island prime-meridian τ prior | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | IERS Earth sidereal phase at prime meridian | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ISRIC SoilGrids v2 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Kittel / CRC | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | LIGO public GW150914 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | LIGO public summary 2024 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | LIGO/Virgo public GW170817 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | LIGO/Virgo public GW190521 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | LIGO_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | MAST_em | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | MATERIALS_SCIENCE_rules | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | MITRE_ATT&CK_shape | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | NULL Island 0N 0E UTC diurnal cycle | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Natural Earth | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Observer_Channel_Derivation | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | PB2002_tectonics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | PBDB | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | Physical Review Letters 2026 Zhang et al. QCE | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Poof-dominant molecular valve — unity τ recycle baseline | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Portable_Clone_Verify | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Preregistered_Predictions | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | QUANTUM_COMPUTING_rules | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | RELATED_EMBODIMENTS.md | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | RFC_IANA_anchors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Reichardt, Solvents 3rd ed (2003) | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | SHIP_BASELINE_MULTILANG | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | SMILES_activation | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | SMILES_particle | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | SMILES_quantum | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | S_sign_multi_scale_hierarchy | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Stumped_Observables_Panel | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | THERMODYNAMICS_ENGINEERING_rules | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | Time_Domain_Crosswalk | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Time_Emergence_Simulation | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | VizieR NVSS | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | WDS | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | WDS/literature sextuple | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | Warp_BH_WH_Portal_Panel | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | World_Athletics_records | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | adversarial_corpus | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | aerodynamics_motion_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | agriculture_agroecology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | airfoil_motion_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | airfoil_rmse | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | anthropology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ashrae_hvac_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | bh_wh_cycle_blueprint | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | biology_strict | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | biology_strict_lab | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | bubble_bleed_physics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | c_parity | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cache | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cardiology_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cardiology_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | circuit_component_emergence | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | civil_engineering_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | civil_engineering_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | climate_observed | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | clinical_medicine_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_crosswalk | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_depth_pass | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_holes | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_language_registry | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_lib | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | code_genome_structure_bridge | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | coding_structure | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | coding_structure_verifier | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | coffee_roast | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | cosmology_extended_benchmark.json — cosmological damping τ anchor | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | creep_fracture_materials_literature_anchors+materials_project | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cross_scale_motif | Named in panel source; add explicit public URL if this is an external authority | 3 |
| unresolved | crosswalk_modules | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | crosswalk_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cryosphere | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cryptography_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cryptography_technology_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | culinary_arts | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | culinary_process_bridge | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | cve_codon_hole_falsification | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | cwe_codon_map | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | derived from IERS sidereal period | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | derived lunar sidereal | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_bibliography | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_binary_decoder | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_canonical_oracle | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_certified_agent | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_dictionary | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_early_lean_mc | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_fuel_lab_engine_simulator | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_intrinsic_llm | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_knowledge_brain | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_living_fsot | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_machine_and_molecule_species_catalog | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_observer_loop_lib | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_omni_theory | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_physarum | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_project_crosswalk | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_rust_lean_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_scalar_solver | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_trinary_hardware | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | desktop_vl_distill | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | developmental_structural_biology_literature_anchors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | domain_orbital_predictions | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | econometrics | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | economics_gap_fill | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | economics_yoy_bridge | Named in panel source; add explicit public URL if this is an external authority | 3 |
| unresolved | entanglement_decoherence_literature_anchors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | epidemiology_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | epidemiology_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | esp32_platform | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | evolution_lab | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | evolution_operon | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | existence_simulation_lib | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | existence_simulation_refinement_lib | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | extension_benchmarks | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | external_oss_code_genome | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fermentation_browning_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fermentation_reference | Named in panel source; add explicit public URL if this is an external authority | 3 |
| unresolved | fic_sensitivity_sweep | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | finance_markets_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | finance_markets_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fluid_navigation_analogy | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fluid_phase_current_spine | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fluidlink_fpc_timing | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | food_microbiology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | formula_branching_fractal | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | founding_law:law_11 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_12 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_13 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_20 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_23 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_26 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | founding_law:law_34 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_biology_scalar | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_developmental_predict_lib | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_gpu_cuda | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | fsot_gpu_parity | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_gpu_parity_verify | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_hardware_kernel | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fsot_transporter_technology_stack | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | fusion_lab | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | gate=0.50 no_exp | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | geochemistry | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | geomagnetism_x_space_weather_x_magnetic_string | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | github_open_source | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | github_oss_code_genome_manifest | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | hardware_depth_bridge | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | immunology | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | immunology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | industry_x86_cache_classes | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | interconnect | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | intermediate_axis_theorem / tennis_racket / Dzhanibekov public literature | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | law_policy_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | law_policy_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_priors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:consciousness | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:energy | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:fusion | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:observer | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:perceived | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | lean_route_credibility_expansion:proton | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | linguistics_anthropology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | linguistics_corpus | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | linguistics_formal | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | linguistics_formal_benchmark | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | linguistics_lab | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | literature hierarchical | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | literature_Tc | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | magnetic_confinement | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | magnetosphere_cluster | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | malware_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | malware_threat_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | maps_to_lean | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | materials_engineering | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | math_first_qc_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_chem_eng | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_civil | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_fluid_mechanics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_mech | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_pure | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_quantum | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_rules | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | math_generator_rules_eval | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | math_physics_rules | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | mathematics_computational | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | mechanical_engineering_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | mechanical_engineering_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | multi_base_carry_analysis | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | multi_hero_benchmark | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | navigation sweep | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | network_internet_protocols_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | neuroeconomics_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | neuroeconomics_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | neuron_cohort | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | neuron_cohort_lab | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | neuron_cohort_per_stratum | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | open_literature_math_constants | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | paleoclimate_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | paleoclimate_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | particle_physics_benchmark | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | pbdb_age | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | pbdb_api | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | pharmacokinetics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | pharmacology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase1_formal_gpu/ | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase1_formal_gpu/isabelle/Trinary.thy | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase1_formal_gpu/lean/GpuMemory.lean | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase1_formal_gpu/lean/Trinary.lean | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | phase2_native_gpu/cuda/ | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase2_native_gpu/cuda/fsot_beat_cuda.cu | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | phase_shift_physics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | pk_reference | Named in panel source; add explicit public URL if this is an external authority | 3 |
| unresolved | planetary_structure | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | planetary_structure_lab | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | polymathic_ai_the_well | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | positional_carry_theory | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | processor | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | programming_language_crosswalk | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | psychology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | psychometrics_rct_literature_anchors | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | public 2022–2026 fusion/quantum breakthrough literature | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | public ELM literature + TechTimes/PRL summary | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | python_mathlib_identity | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | qce_elm | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | qemu_bios | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | quantum_computing_gap_fill | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | ram | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | raw_S | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | reality_folding_spine_metrics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | recent_breakthroughs | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | recipe_process | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | reference_circuits | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | robotics_control_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | robotics_control_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | robotics_control_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | rust_lean_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | rust_lean_genome | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | scaled_S | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | secure_software_engineering_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | seismology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | smiles_food_chemistry | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | smiles_immunology | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | smiles_lab | Named in panel source; add explicit public URL if this is an external authority | 5 |
| unresolved | species_catalog | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | speleology_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | speleology_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | stumped_observables_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | supply_chain_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | supply_chain_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term1.coherence_efficiency | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term1.growth_term | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term1.perceived_adjust | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term1.quirkMod | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term1.term1_base | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term2.amplitude | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term2.scale | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term2.trend_bias | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term3.acoustic_bleed | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term3.acoustic_inflow | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | term3.chaos_factor | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | the_well_hdf5_spot_chunks | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | theory_completeness_spine | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | thesis_wave | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | tier52-56_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier55-57_material_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier61_creative_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier64_neurolab_gap_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier66_neurolab_residual_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier67_formula_precision_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier68_live_ingest_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier69_unified_db_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier80_government_open_data_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier81_public_verifiable_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier82_scientific_expansion_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier84_scientific_expansion_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier85_scientific_expansion_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier86_depth_wave_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier87_depth_wave2_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier88_application_wiring_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier89_the_well_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier90_consciousness_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier90_observer_effect | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier91_foundational_ontology_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier92_alternate_base_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier92_base_analysis | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier93_dual_wave_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier94_longevity | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier94_longevity_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier95_predictive_crossval | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier95_zebrahub_panels | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier95_zebrahub_tracks | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier96_circuit | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier_h_child_rollup | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier_k_gap_closure_pillars | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier_l_orbital_gap_fill | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | tier_m_toe_unity | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | toe_gap_closure_spine | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | toe_unification_metrics | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_genome | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_os | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_os_ISA | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_os_control_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_os_oracle | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | trinary_os_tier_e | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\cybersecurity\samples\csp_safe_dom.js | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\cybersecurity\samples\secure_buffer.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\cybersecurity\samples\vulnerable_legacy.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\cybersecurity\samples\xss_sink_legacy.js | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\cpython_ceval.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\express_router.js | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\nodejs_buffer.js | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\python_dictobject.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\react_hooks.js | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\redis_sds.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | vendor\github_oss\snapshots\sqlite_mem.c | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | verification/esp32/fsot_esp32_observer | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | virology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | virology_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | virology_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | weather_observed | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | world_athletics_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | x.com/dr_logvinovich/status/2084655064602358240 | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | zebrahub.sf.czbiohub.org | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | zero_day_evaluator_reference_observables | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | zero_day_language_bridges | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | zero_day_reference | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | zero_day_risk_evaluator_cybersecurity_benchmark | Named in panel source; add explicit public URL if this is an external authority | 2 |
| unresolved | zoology_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| unresolved | zoology_insect_bridge | Named in panel source; add explicit public URL if this is an external authority | 1 |
| url | https://api.crossref.org/ | https://api.crossref.org/ | 1 |
| url | https://api.inaturalist.org/ | https://api.inaturalist.org/ | 1 |
| url | https://archive.stsci.edu/ | https://archive.stsci.edu/ | 1 |
| url | https://clinicaltrials.gov/api/v2/ | https://clinicaltrials.gov/api/v2/ | 1 |
| url | https://github.com/FloatingPragma/observer-patch-holography | https://github.com/FloatingPragma/observer-patch-holography | 1 |
| url | https://github.com/dappalumbo91/fsot-neuron-zig | https://github.com/dappalumbo91/fsot-neuron-zig | 1 |
| url | https://huggingface.co/collections/polymathic-ai/the-well | https://huggingface.co/collections/polymathic-ai/the-well | 1 |
| url | https://www.osti.gov/api/v1/records | https://www.osti.gov/api/v1/records | 1 |
| url | https://www.war.gov/UFO/ | https://www.war.gov/UFO/ | 1 |
| url | https://x.com/muellerberndt/status/2079877767416709231 | https://x.com/muellerberndt/status/2079877767416709231 | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\data\dark_energy_cpl_reference.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/dark_energy_cpl_reference.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\data\foundational_ontology_axioms.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/foundational_ontology_axioms.yaml | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\data\hardware_competitive_refine_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/hardware_competitive_refine_report.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\data\preregistered_predictions_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/preregistered_predictions_manifest.yaml | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\bibliography_corpus_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/bibliography_corpus_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\biological_cuda_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/biological_cuda_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\living_fsot_hardware_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/living_fsot_hardware_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\tokenization_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/tokenization_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\vl_agent_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/vl_agent_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\industry_component_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/industry_component_catalog.json | 3 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\tier96_cache\industry_component_catalog_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/tier96_cache/industry_component_catalog_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fluid_spacetime\cosmology_anomaly_deep_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fluid_spacetime/cosmology_anomaly_deep_anchors.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fusion\fusion_public_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fusion/fusion_public_anchors.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fusion\qce_elm_public_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fusion/qce_elm_public_anchors.json | 2 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\hardware\dzhanibekov_public_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/hardware/dzhanibekov_public_anchors.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\lab_synthesis\heavy_ion_reaction_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/lab_synthesis/heavy_ion_reaction_anchors.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\lab_synthesis\metamaterial_fluid_prereg_candidates.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/lab_synthesis/metamaterial_fluid_prereg_candidates.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier86_cache\culinary_fermentation_maillard_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier86_cache/culinary_fermentation_maillard_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\biology_developmental_structural_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/biology_developmental_structural_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\condensed_matter_superconductivity_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/condensed_matter_superconductivity_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\materials_creep_fracture_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/materials_creep_fracture_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\neuroscience_connectomics_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/neuroscience_connectomics_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\optics_interferometry_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/optics_interferometry_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\psychology_psychometrics_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/psychology_psychometrics_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\quantum_computing_math_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/quantum_computing_math_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\quantum_mechanics_entanglement_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/quantum_mechanics_entanglement_cache.json | 1 |
| vendor_cache | C:\Users\damia\Desktop\FSOT-Legacy-Physics-Connections\concept_refinement\warp_actuation_formula_fsot21.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-Legacy-Physics-Connections/concept_refinement/warp_actuation_formula_fsot21.json | 1 |
| vendor_cache | CRYPTOGRAPHY_RULES.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/CRYPTOGRAPHY_RULES.json | 1 |
| vendor_cache | FSOT_VERIFIED_SCOPE.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/FSOT_VERIFIED_SCOPE.yaml | 1 |
| vendor_cache | G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json | 1 |
| vendor_cache | G:\FSOT-PublicData\anomaly_observables\consciousness\tier90_microtubule_observer_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_microtubule_observer_cache.json | 1 |
| vendor_cache | G:\FSOT-PublicData\anomaly_observables\consciousness\tier90_species_panel_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_species_panel_cache.json | 1 |
| vendor_cache | G:\FSOT-PublicData\the_well\the_well_catalog_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/the_well/the_well_catalog_cache.json | 1 |
| vendor_cache | G:\FSOT-PublicData\the_well\the_well_spot_checks_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/the_well/the_well_spot_checks_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\arxiv_brain_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/arxiv_brain_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\arxiv_primitives_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/arxiv_primitives_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\binary_decoder_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/binary_decoder_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\blackhole_whitehole_cycle_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/blackhole_whitehole_cycle_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\canonical_oracle_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/canonical_oracle_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\certified_agent_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/certified_agent_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\early_lean_mc_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/early_lean_mc_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\fuel_lab_live_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/fuel_lab_live_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\machine_and_molecule_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/machine_and_molecule_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\omni_theory_humanities_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/omni_theory_humanities_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\rust_lean_bridge_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/rust_lean_bridge_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\scalar_solver_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/scalar_solver_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\star_trek_transporter_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/star_trek_transporter_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\trinary_hardware_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/trinary_hardware_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\validators_intrinsic_llm_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/validators_intrinsic_llm_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\materials_project_live_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/materials_project_live_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\openneuro_full_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/openneuro_full_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\pubchem_live_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/pubchem_live_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\vizier_wds_tap_live_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/vizier_wds_tap_live_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\scientific_expansion\tier85_cache\mechanical_engineering_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/scientific_expansion/tier85_cache/mechanical_engineering_cache.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\verified_desktop\legacy_physics\warp_actuation_formula_fsot21.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/verified_desktop/legacy_physics/warp_actuation_formula_fsot21.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\04_Genetics-Longevity\tier94_anage_longevity_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/04_Genetics-Longevity/tier94_anage_longevity_catalog.json | 1 |
| vendor_cache | I:\FSOT-Physical-Archive\08_Verified-Desktop-Projects\star_trek_transporter\pattern_buffer_scan_results.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/08_Verified-Desktop-Projects/star_trek_transporter/pattern_buffer_scan_results.json | 1 |
| vendor_cache | PROGRAMMING_LANGUAGE_RULES.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/PROGRAMMING_LANGUAGE_RULES.json | 1 |
| vendor_cache | acoustic_resonance_materials_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/acoustic_resonance_materials_benchmark.json | 3 |
| vendor_cache | actuarial_science_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/actuarial_science_panel_benchmark.json | 1 |
| vendor_cache | adjacent_rung_coupling_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/adjacent_rung_coupling_benchmark.json | 2 |
| vendor_cache | adversarial_fractal_break_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/adversarial_fractal_break_benchmark.json | 1 |
| vendor_cache | agriculture_agroecology_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/agriculture_agroecology_gap_fill_benchmark.json | 1 |
| vendor_cache | ai_galactic_orbital_bridge_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/ai_galactic_orbital_bridge_benchmark.json | 1 |
| vendor_cache | alternate_base_mathematics_explorer_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/alternate_base_mathematics_explorer_panel_benchmark.json | 1 |
| vendor_cache | alternate_base_mathematics_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/alternate_base_mathematics_spine_benchmark.json | 1 |
| vendor_cache | anthropology_extension_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/anthropology_extension_benchmark.json | 1 |
| vendor_cache | architecture_building_science_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/architecture_building_science_gap_fill_benchmark.json | 3 |
| vendor_cache | arxiv_brain_knowledge_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_brain_knowledge_panel_benchmark.json | 1 |
| vendor_cache | arxiv_gravitational_waves_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_gravitational_waves_panel_benchmark.json | 1 |
| vendor_cache | arxiv_primitives_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_primitives_panel_benchmark.json | 1 |
| vendor_cache | arxiv_primitives_v14_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_primitives_v14_benchmark.json | 1 |
| vendor_cache | astrophysical_structure_crosswalk_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/astrophysical_structure_crosswalk_benchmark.json | 1 |
| vendor_cache | atmospheric_physics_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/atmospheric_physics_gap_fill_benchmark.json | 1 |
| vendor_cache | atomic_physics_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/atomic_physics_gap_fill_benchmark.json | 1 |
| vendor_cache | bibliography_corpus_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/bibliography_corpus_panel_benchmark.json | 1 |
| vendor_cache | bibliography_lean_corpus_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/bibliography_lean_corpus_benchmark.json | 1 |
| vendor_cache | binary_decoder_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/binary_decoder_panel_benchmark.json | 1 |
| vendor_cache | binary_decoder_rendlesham_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/binary_decoder_rendlesham_benchmark.json | 1 |
| vendor_cache | biological_cuda_physarum_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/biological_cuda_physarum_benchmark.json | 1 |
| vendor_cache | biology_developmental_structural_depth_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/biology_developmental_structural_depth_panel_benchmark.json | 1 |
| vendor_cache | biophysics_public_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/biophysics_public_panel_benchmark.json | 1 |
| vendor_cache | blackhole_whitehole_cycle_live_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/blackhole_whitehole_cycle_live_panel_benchmark.json | 1 |
| vendor_cache | botany_extension_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/botany_extension_benchmark.json | 1 |
| vendor_cache | boundary_partition_tightening_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/boundary_partition_tightening_benchmark.json | 1 |
| vendor_cache | breakthrough_discoveries_2024_2026_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/breakthrough_discoveries_2024_2026_benchmark.json | 1 |
| vendor_cache | canonical_oracle_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/canonical_oracle_panel_benchmark.json | 1 |
| vendor_cache | cardiology_extension_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cardiology_extension_benchmark.json | 1 |
| vendor_cache | cardiology_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cardiology_panel_benchmark.json | 1 |
| vendor_cache | cartography_gis_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cartography_gis_panel_benchmark.json | 1 |
| vendor_cache | cern_open_data_lhc_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cern_open_data_lhc_benchmark.json | 1 |
| vendor_cache | certificate.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/certificate.json | 1 |
| vendor_cache | certified_agent_formal_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/certified_agent_formal_panel_benchmark.json | 1 |
| vendor_cache | certified_agent_qwen_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/certified_agent_qwen_benchmark.json | 1 |
| vendor_cache | chaos_mediated_phase_transitions_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/chaos_mediated_phase_transitions_benchmark.json | 1 |
| vendor_cache | chemical_engineering_extension_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/chemical_engineering_extension_benchmark.json | 1 |
| vendor_cache | cisa_kev_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cisa_kev_summary.json | 1 |
| vendor_cache | code_genome_structure_cybersecurity_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/code_genome_structure_cybersecurity_benchmark.json | 1 |
| vendor_cache | cold_fusion_candidate_prereg_scaffold_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cold_fusion_candidate_prereg_scaffold_benchmark.json | 1 |
| vendor_cache | cold_fusion_lab_synthesis_crosswalk_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cold_fusion_lab_synthesis_crosswalk_benchmark.json | 1 |
| vendor_cache | compactification_ladder_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_benchmark.json | 1 |
| vendor_cache | compactification_ladder_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_manifest.yaml | 3 |
| vendor_cache | compare_full_20260526.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compare_full_20260526.json | 1 |
| vendor_cache | compare_optimax_wave_20260715.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compare_optimax_wave_20260715.json | 1 |
| vendor_cache | computational_reasoning_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/computational_reasoning_benchmark.json | 1 |
| vendor_cache | consciousness_reference_observables.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/consciousness_reference_observables.json | 1 |
| vendor_cache | core_formula_fractal_branch_index.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/core_formula_fractal_branch_index.json | 1 |
| vendor_cache | cosmology_anomalies_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_anomalies_benchmark.json | 1 |
| vendor_cache | cosmology_anomaly_deep_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_anomaly_deep_panel_benchmark.json | 1 |
| vendor_cache | cosmology_extended_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_extended_benchmark.json | 1 |
| vendor_cache | cryptography_technology_cybersecurity_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cryptography_technology_cybersecurity_benchmark.json | 1 |
| vendor_cache | culinary_arts_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/culinary_arts_benchmark.json | 2 |
| vendor_cache | dark_sector_open_problems_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/dark_sector_open_problems_benchmark.json | 2 |
| vendor_cache | data/*_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/*_benchmark.json | 1 |
| vendor_cache | data/cosmology_extended_benchmark.json lambda_cdm H0 | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/cosmology_extended_benchmark.json lambda_cdm H0 | 1 |
| vendor_cache | data\living_fsot_hardware_verification_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/living_fsot_hardware_verification_report.json | 1 |
| vendor_cache | domain_coupling_simulation_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json | 10 |
| vendor_cache | domain_orbital_prediction_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_orbital_prediction_report.json | 1 |
| vendor_cache | electrical_power_systems_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/electrical_power_systems_benchmark.json | 1 |
| vendor_cache | existence_simulation_failure_clusters_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/existence_simulation_failure_clusters_manifest.yaml | 1 |
| vendor_cache | extension_domains_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/extension_domains_manifest.yaml | 3 |
| vendor_cache | external_data_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/external_data_manifest.yaml | 1 |
| vendor_cache | external_oss_code_genome_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/external_oss_code_genome_benchmark.json | 1 |
| vendor_cache | fluid_phase_current_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fluid_phase_current_spine_benchmark.json | 1 |
| vendor_cache | fluid_spacetime_observable_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fluid_spacetime_observable_spine_benchmark.json | 1 |
| vendor_cache | fold_depth_metrics_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fold_depth_metrics_benchmark.json | 1 |
| vendor_cache | food_microbiology_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/food_microbiology_gap_fill_benchmark.json | 1 |
| vendor_cache | fpc_fluidlink_timing_deep_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fpc_fluidlink_timing_deep_panel_benchmark.json | 1 |
| vendor_cache | fpc_temporal_coupling_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fpc_temporal_coupling_benchmark.json | 2 |
| vendor_cache | fractal_constant_recursion.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fractal_constant_recursion.yaml | 1 |
| vendor_cache | fsot_aggregate_unified_db_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_aggregate_unified_db_benchmark.json | 1 |
| vendor_cache | fsot_formula_spine.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_formula_spine.yaml | 3 |
| vendor_cache | fsot_species_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_species_catalog.json | 3 |
| vendor_cache | fsot_verification_progress.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_verification_progress.yaml | 2 |
| vendor_cache | fuel_thermochemistry_public_anchors_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fuel_thermochemistry_public_anchors_benchmark.json | 1 |
| vendor_cache | fusion_decay_chain_prereg_scaffold_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_decay_chain_prereg_scaffold_benchmark.json | 2 |
| vendor_cache | fusion_lab_certificate_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_lab_certificate_spine_benchmark.json | 1 |
| vendor_cache | fusion_physics_public_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_physics_public_panel_benchmark.json | 3 |
| vendor_cache | galactic_structure_sample.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/galactic_structure_sample.json | 1 |
| vendor_cache | galactic_structure_sample_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/galactic_structure_sample_benchmark.json | 1 |
| vendor_cache | geomagnetism_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/geomagnetism_benchmark.json | 1 |
| vendor_cache | github_oss_adversarial_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/github_oss_adversarial_manifest.yaml | 1 |
| vendor_cache | gwosc_live_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/gwosc_live_cache.json | 1 |
| vendor_cache | heavy_ion_lab_synthesis_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/heavy_ion_lab_synthesis_panel_benchmark.json | 1 |
| vendor_cache | higgs_branching_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/higgs_branching_benchmark.json | 1 |
| vendor_cache | https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json | 1 |
| vendor_cache | hubble_bubble_tension_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/hubble_bubble_tension_benchmark.json | 2 |
| vendor_cache | hubble_dark_sector_crosswalk_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/hubble_dark_sector_crosswalk_benchmark.json | 1 |
| vendor_cache | igem_live_fasta_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/igem_live_fasta_benchmark.json | 1 |
| vendor_cache | igem_synthetic_biology_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/igem_synthetic_biology_benchmark.json | 1 |
| vendor_cache | knowledge_base_formula_verification_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/knowledge_base_formula_verification_summary.json | 1 |
| vendor_cache | lab_synthesis_metamaterial_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/lab_synthesis_metamaterial_spine_benchmark.json | 1 |
| vendor_cache | linguistics_formal_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/linguistics_formal_benchmark.json | 1 |
| vendor_cache | longevity_telomere_repair_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/longevity_telomere_repair_anchors.json | 1 |
| vendor_cache | magnetosphere_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/magnetosphere_benchmark.json | 1 |
| vendor_cache | magnetosphere_extended_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/magnetosphere_extended_benchmark.json | 1 |
| vendor_cache | maillard_chemistry_gap_fill_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/maillard_chemistry_gap_fill_benchmark.json | 1 |
| vendor_cache | malware_threat_intelligence_cybersecurity_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/malware_threat_intelligence_cybersecurity_benchmark.json | 1 |
| vendor_cache | material_compatibility_comparison.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/material_compatibility_comparison.json | 1 |
| vendor_cache | materials_engineering_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/materials_engineering_benchmark.json | 1 |
| vendor_cache | materials_species_bridge_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/materials_species_bridge_benchmark.json | 1 |
| vendor_cache | math_generator_airfoil_rmse_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/math_generator_airfoil_rmse_benchmark.json | 1 |
| vendor_cache | mechanistic_coupling_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/mechanistic_coupling_manifest.yaml | 1 |
| vendor_cache | multi_hero_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/multi_hero_benchmark.json | 1 |
| vendor_cache | music_harmonics_public_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/music_harmonics_public_panel_benchmark.json | 1 |
| vendor_cache | network_internet_protocols_cybersecurity_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/network_internet_protocols_cybersecurity_benchmark.json | 1 |
| vendor_cache | nist_codata_constants_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/nist_codata_constants_benchmark.json | 1 |
| vendor_cache | openneuro_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/openneuro_summary.json | 1 |
| vendor_cache | orbital_predictions_registry.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/orbital_predictions_registry.yaml | 1 |
| vendor_cache | particle_physics_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/particle_physics_benchmark.json | 2 |
| vendor_cache | periodic_table_completion_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/periodic_table_completion_spine_benchmark.json | 2 |
| vendor_cache | pharmacology_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pharmacology_benchmark.json | 1 |
| vendor_cache | plasma_physics_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json | 6 |
| vendor_cache | prediction_rederivation_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/prediction_rederivation_benchmark.json | 1 |
| vendor_cache | preregistered_predictions_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_benchmark.json | 1 |
| vendor_cache | preregistered_predictions_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_manifest.yaml | 3 |
| vendor_cache | preregistered_predictions_verification_scaffold_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_verification_scaffold_benchmark.json | 1 |
| vendor_cache | proof_ledger.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/proof_ledger.yaml | 1 |
| vendor_cache | pubchem_compound_properties_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pubchem_compound_properties_benchmark.json | 2 |
| vendor_cache | pubchem_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pubchem_summary.json | 1 |
| vendor_cache | public_fuel_property_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/public_fuel_property_catalog.json | 1 |
| vendor_cache | quantum_materials_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/quantum_materials_benchmark.json | 1 |
| vendor_cache | rcsb_pdb_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/rcsb_pdb_summary.json | 1 |
| vendor_cache | reality_folding_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/reality_folding_spine_benchmark.json | 1 |
| vendor_cache | refined_grounded_hemp.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/refined_grounded_hemp.json | 1 |
| vendor_cache | results/competitive/beat_cuda.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/beat_cuda.json | 3 |
| vendor_cache | results/competitive/flash_attention_track.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/flash_attention_track.json | 1 |
| vendor_cache | results/competitive/long_seq_and_norm.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/long_seq_and_norm.json | 1 |
| vendor_cache | results/industry_lm/fsot21_verify.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/industry_lm/fsot21_verify.json | 1 |
| vendor_cache | results/parity/parity_ledger.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/parity/parity_ledger.json | 3 |
| vendor_cache | results/phase0/fsot_scalar_gpu.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/fsot_scalar_gpu.json | 2 |
| vendor_cache | results/phase0/gpu_probe.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/gpu_probe.json | 2 |
| vendor_cache | rust_lean_bridge_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/rust_lean_bridge_benchmark.json | 1 |
| vendor_cache | scientific_domain_expansion_map.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/scientific_domain_expansion_map.json | 1 |
| vendor_cache | secure_software_engineering_cybersecurity_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/secure_software_engineering_cybersecurity_benchmark.json | 1 |
| vendor_cache | space_weather_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/space_weather_benchmark.json | 1 |
| vendor_cache | stellar_multiplicity_catalog_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stellar_multiplicity_catalog_benchmark.json | 1 |
| vendor_cache | stumped_observables_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_panel_benchmark.json | 1 |
| vendor_cache | stumped_observables_reference.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_reference.json | 1 |
| vendor_cache | stumped_observables_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_spine_benchmark.json | 1 |
| vendor_cache | superheavy_element_stability_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/superheavy_element_stability_panel_benchmark.json | 1 |
| vendor_cache | superheavy_island_completion_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/superheavy_island_completion_spine_benchmark.json | 1 |
| vendor_cache | symbolic_archetype_panel_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/symbolic_archetype_panel_benchmark.json | 1 |
| vendor_cache | term3_acoustic_bleed_depth_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/term3_acoustic_bleed_depth_benchmark.json | 2 |
| vendor_cache | thermochemistry_public_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/thermochemistry_public_anchors.json | 1 |
| vendor_cache | tier65_prereg_channels_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier65_prereg_channels_manifest.yaml | 3 |
| vendor_cache | tier92_base_analysis_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier92_base_analysis_cache.json | 1 |
| vendor_cache | tier93_consciousness_genetics_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_consciousness_genetics_cache.json | 3 |
| vendor_cache | tier93_experimental_base_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_experimental_base_cache.json | 1 |
| vendor_cache | tier94_anage_longevity_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_anage_longevity_catalog.json | 1 |
| vendor_cache | tier94_extreme_species_ncbi_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_extreme_species_ncbi_cache.json | 1 |
| vendor_cache | tier94_megadeep_extreme_ncbi_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_megadeep_extreme_ncbi_cache.json | 2 |
| vendor_cache | tier94_telomere_repair_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_telomere_repair_cache.json | 1 |
| vendor_cache | tier95_zebrahub_gpu_imaging_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier95_zebrahub_gpu_imaging_cache.json | 1 |
| vendor_cache | tier95_zebrahub_tracks_cache.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier95_zebrahub_tracks_cache.json | 2 |
| vendor_cache | time_domain_crosswalk_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_domain_crosswalk_benchmark.json | 1 |
| vendor_cache | time_emergence_manifest.yaml | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_manifest.yaml | 2 |
| vendor_cache | time_emergence_simulation_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_simulation_benchmark.json | 2 |
| vendor_cache | toe_unification_spine_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/toe_unification_spine_benchmark.json | 1 |
| vendor_cache | undiscovered_element_candidate_prereg_scaffold_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/undiscovered_element_candidate_prereg_scaffold_benchmark.json | 1 |
| vendor_cache | unified_db_domain_index.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/unified_db_domain_index.json | 1 |
| vendor_cache | uniprot_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/uniprot_summary.json | 1 |
| vendor_cache | vendor/arxiv_primitives/v14_run_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/arxiv_primitives/v14_run_summary.json | 2 |
| vendor_cache | vendor/bibliography_corpus/bibliography_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/bibliography_corpus/bibliography_summary.json | 1 |
| vendor_cache | vendor/binary_decoder/rendlesham_page14_trace.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/binary_decoder/rendlesham_page14_trace.json | 2 |
| vendor_cache | vendor/certified_agent/certified_agent_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/certified_agent/certified_agent_summary.json | 1 |
| vendor_cache | vendor/certified_agent/fsot_workspace.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/certified_agent/fsot_workspace.json | 1 |
| vendor_cache | vendor/cosmology/database/FSOT_Mathematical_Database_Unified.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/cosmology/database/FSOT_Mathematical_Database_Unified.json | 1 |
| vendor_cache | vendor/cybersecurity/samples/secure_buffer.c | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/cybersecurity/samples/secure_buffer.c | 1 |
| vendor_cache | vendor/evolution/biological_mt_operons.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/evolution/biological_mt_operons.json | 1 |
| vendor_cache | vendor/fringe_desktop/intelligence_compressor_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/intelligence_compressor_summary.json | 1 |
| vendor_cache | vendor/fringe_desktop/soul_simulator_manifest_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/soul_simulator_manifest_summary.json | 1 |
| vendor_cache | vendor/fringe_desktop/symbolic_encoding_graph_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/symbolic_encoding_graph_summary.json | 1 |
| vendor_cache | vendor/fringe_desktop/vibrafsot_progress_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/vibrafsot_progress_summary.json | 1 |
| vendor_cache | vendor/fsot_aggregate/FSOT_Mathematical_Database_Unified.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/FSOT_Mathematical_Database_Unified.json | 2 |
| vendor_cache | vendor/fsot_aggregate/FSOT_UNIFIED.db | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/FSOT_UNIFIED.db | 1 |
| vendor_cache | vendor/fsot_aggregate/prediction_rederivation_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/prediction_rederivation_summary.json | 2 |
| vendor_cache | vendor/fuel/public_fuel_property_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fuel/public_fuel_property_catalog.json | 1 |
| vendor_cache | vendor/github_oss/adversarial/broken_memcpy_chain.c | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/broken_memcpy_chain.c | 1 |
| vendor_cache | vendor/github_oss/adversarial/double_free_pattern.c | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/double_free_pattern.c | 1 |
| vendor_cache | vendor/github_oss/adversarial/prototype_pollution.js | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/prototype_pollution.js | 1 |
| vendor_cache | vendor/github_oss/adversarial/race_unsafe.go | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/race_unsafe.go | 1 |
| vendor_cache | vendor/github_oss/adversarial/xss_eval_sink.js | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/xss_eval_sink.js | 1 |
| vendor_cache | vendor/igem/fastas | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/fastas | 2 |
| vendor_cache | vendor/igem/igem_parts_registry.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/igem_parts_registry.json | 3 |
| vendor_cache | vendor/intrinsic_llm/benchmark_results_final.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/intrinsic_llm/benchmark_results_final.json | 2 |
| vendor_cache | vendor/knowledge_base/kb_portable_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/knowledge_base/kb_portable_summary.json | 1 |
| vendor_cache | vendor/linguistics/data/LINGUISTIC_TARGETS.csv | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/linguistics/data/LINGUISTIC_TARGETS.csv | 1 |
| vendor_cache | vendor/linguistics/linguistics_derivations.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/linguistics/linguistics_derivations.json | 1 |
| vendor_cache | vendor/materials_live/materials_project_bundled.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/materials_live/materials_project_bundled.json | 1 |
| vendor_cache | vendor/math_generator/benchmark_reports | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports | 2 |
| vendor_cache | vendor/math_generator/benchmark_reports/airfoil_three_seed_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports/airfoil_three_seed_report.json | 1 |
| vendor_cache | vendor/math_generator/benchmark_reports/hubble_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports/hubble_report.json | 1 |
| vendor_cache | vendor/math_generator/datasets/airfoil_self_noise.csv | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/datasets/airfoil_self_noise.csv | 2 |
| vendor_cache | vendor/math_generator/generated_formula_comparison_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/generated_formula_comparison_report.json | 1 |
| vendor_cache | vendor/math_generator/rules | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/rules | 3 |
| vendor_cache | vendor/neuron_cohort/inconsistency_rerun_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/neuron_cohort/inconsistency_rerun_report.json | 1 |
| vendor_cache | vendor/omni_theory/analysis/genesis/genesis_per_verse_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/omni_theory/analysis/genesis/genesis_per_verse_summary.json | 2 |
| vendor_cache | vendor/physarum/genome_data/cuda_benchmark_results.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/cuda_benchmark_results.json | 1 |
| vendor_cache | vendor/physarum/genome_data/genomics_slime_mold_refined.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/genomics_slime_mold_refined.json | 1 |
| vendor_cache | vendor/physarum/genome_data/physarum_codon_weights.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/physarum_codon_weights.json | 1 |
| vendor_cache | vendor/physarum/physarum_v5_states.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/physarum_v5_states.json | 1 |
| vendor_cache | vendor/public_data/consciousness/openneuro_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/consciousness/openneuro_summary.json | 1 |
| vendor_cache | vendor/public_data/nasa_exoplanet/nasa_exoplanet_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/nasa_exoplanet/nasa_exoplanet_summary.json | 1 |
| vendor_cache | vendor/public_data/pubchem/pubchem_auto_expansion.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_auto_expansion.json | 1 |
| vendor_cache | vendor/public_data/pubchem/pubchem_auto_seed_manifest.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_auto_seed_manifest.json | 1 |
| vendor_cache | vendor/public_data/pubchem/pubchem_culinary_expansion.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_culinary_expansion.json | 1 |
| vendor_cache | vendor/public_data/pubchem/pubchem_preregistered_panel.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_preregistered_panel.json | 1 |
| vendor_cache | vendor/public_data/pubchem/pubchem_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_summary.json | 1 |
| vendor_cache | vendor/rust_lean_bridge/rust_lean_bridge_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/rust_lean_bridge/rust_lean_bridge_summary.json | 1 |
| vendor_cache | vendor/smiles/FSOT_SMILES_Lab_Dataset.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json | 5 |
| vendor_cache | vendor/species/fsot_species_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/species/fsot_species_catalog.json | 2 |
| vendor_cache | vendor/stellar_structures/galactic_structure_sample.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/galactic_structure_sample.json | 1 |
| vendor_cache | vendor/stellar_structures/gwosc_public_events.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/gwosc_public_events.json | 1 |
| vendor_cache | vendor/stellar_structures/public_multiplicity_catalog.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/public_multiplicity_catalog.json | 2 |
| vendor_cache | vendor/tokenization/smoke_cases.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/tokenization/smoke_cases.json | 1 |
| vendor_cache | vendor/tokenization/vocab.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/tokenization/vocab.json | 1 |
| vendor_cache | vendor/trinary_hardware/motif_influence_profile_stable.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_hardware/motif_influence_profile_stable.json | 2 |
| vendor_cache | vendor/trinary_os/fixtures | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/fixtures | 1 |
| vendor_cache | vendor/trinary_os/isa/fsotb_opcode_registry.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/isa/fsotb_opcode_registry.json | 4 |
| vendor_cache | vendor/trinary_os/round_trip | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/round_trip | 1 |
| vendor_cache | vendor/trinary_os/target | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/target | 1 |
| vendor_cache | vendor/trinary_os/target/ | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/target/ | 1 |
| vendor_cache | vendor/vl_distill/distill_dataset.meta.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/distill_dataset.meta.json | 1 |
| vendor_cache | vendor/vl_distill/fsot_atlas_summary.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_atlas_summary.json | 1 |
| vendor_cache | vendor/vl_distill/fsot_competitive_report.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_competitive_report.json | 1 |
| vendor_cache | vendor/vl_distill/fsot_domain_registry.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_domain_registry.json | 1 |
| vendor_cache | vendor\neuron_cohort\cells.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/neuron_cohort/cells.json | 2 |
| vendor_cache | vendor\public_data\oph_challenge_public_anchors.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/oph_challenge_public_anchors.json | 1 |
| vendor_cache | wds_live_multiplicity_deep_benchmark.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/wds_live_multiplicity_deep_benchmark.json | 1 |
| vendor_cache | wds_multiplicity_expanded.json | https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/wds_multiplicity_expanded.json | 1 |

## Unresolved source tokens (need explicit public URL)

These strings appear in panel `source` fields but were not mapped to a known public landing page. 
They remain listed for honesty; prefer promoting them into `PUBLIC_ANCHORS` or `api_requirements.yaml`.

| Token | Panels mentioning |
|-------|------------------:|
| `C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star` | 4 |
| `smiles_lab` | 4 |
| `cross_scale_motif` | 3 |
| `pk_reference` | 3 |
| `fermentation_reference` | 3 |
| `economics_yoy_bridge` | 3 |
| `formula_branching_fractal` | 2 |
| `linguistics_lab` | 2 |
| `weather_observed` | 2 |
| `public ELM literature + TechTimes/PRL summary` | 2 |
| `THERMODYNAMICS_ENGINEERING_rules` | 2 |
| `materials_engineering` | 2 |
| `paleoclimate_reference_observables` | 2 |
| `immunology` | 2 |
| `zero_day_evaluator_reference_observables` | 2 |
| `math_generator_rules_eval` | 2 |
| `smiles_food_chemistry` | 2 |
| `recipe_process` | 2 |
| `coffee_roast` | 2 |
| `fluidlink_fpc_timing` | 2 |
| `esp32_platform` | 2 |
| `fsot_gpu_cuda` | 2 |
| `code_genome_structure_bridge` | 2 |
| `zero_day_risk_evaluator_cybersecurity_benchmark` | 2 |
| `zero_day_language_bridges` | 2 |
| `econometrics` | 2 |
| `culinary_arts` | 2 |
| `culinary_process_bridge` | 2 |
| `hardware_depth_bridge` | 2 |
| `phase1_formal_gpu/lean/Trinary.lean` | 2 |
| `thesis_wave` | 2 |
| `virology_reference_observables` | 2 |
| `FSOT.Formal.Scalar.consciousness_factor` | 2 |
| `biology_strict_lab` | 2 |
| `PBDB` | 2 |
| `SMILES_quantum` | 2 |
| `adversarial_corpus` | 1 |
| `tier92_alternate_base_panels` | 1 |
| `linguistics_anthropology_bridge` | 1 |
| `ASHRAE_HVAC` | 1 |

## Per-panel anchors (compact)

Full machine detail: `data/benchmark_anchor_citation_ledger.json`.

### AI_Galactic_Orbital_Bridge

- Benchmark: `data/ai_galactic_orbital_bridge_benchmark.json` · records=48 · median%=0.005168558627176023
- Lean: `FSOT.Formal.AIGalacticOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/ai_galactic_orbital_bridge_benchmark.json — https://github.com/data/ai_galactic_orbital_bridge_benchmark.json
  - **dataset**: GitHub OSS corpus data/adversarial_fractal_break_benchmark.json — https://github.com/data/adversarial_fractal_break_benchmark.json
  - **dataset**: GitHub OSS corpus data/alternate_base_mathematics_explorer_panel_benchmark.json — https://github.com/data/alternate_base_mathematics_explorer_panel_benchmark.json
  - **dataset**: GitHub OSS corpus data/alternate_base_mathematics_spine_benchmark.json — https://github.com/data/alternate_base_mathematics_spine_benchmark.json
  - **unresolved**: cross_scale_motif — Named in panel source; add explicit public URL if this is an external authority

### Acoustic_Resonance_Materials

- Benchmark: `data/acoustic_resonance_materials_benchmark.json` · records=29 · median%=0.008381497018411083
- Lean: `FSOT.Formal.AcousticResonanceMaterialsPriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_species_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_species_catalog.json
  - **vendor_cache**: architecture_building_science_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/architecture_building_science_gap_fill_benchmark.json
  - **vendor_cache**: math_generator_airfoil_rmse_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/math_generator_airfoil_rmse_benchmark.json

### Actuarial_Science_Panel

- Benchmark: `data/actuarial_science_panel_benchmark.json` · records=60 · median%=0.02261
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.ActuarialSciencePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: SSA Office of the Chief Actuary life tables — https://www.ssa.gov/oact/STATS/table4c6.html
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Adjacent_Rung_Coupling

- Benchmark: `data/adjacent_rung_coupling_benchmark.json` · records=36 · median%=0.020098237848404983
- Lean: `FSOT.Formal.AdjacentRungCouplingPriors`
- Public / portable anchors:
  - **vendor_cache**: compactification_ladder_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_manifest.yaml

### Adversarial_Fractal_Break_Tests

- Benchmark: `data/adversarial_fractal_break_benchmark.json` · records=13 · median%=0.0
- Lean: `FSOT.Formal.AdversarialFractalBreakPriors`
- Public / portable anchors:
  - **vendor_cache**: github_oss_adversarial_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/github_oss_adversarial_manifest.yaml
  - **vendor_cache**: vendor/github_oss/adversarial/broken_memcpy_chain.c — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/broken_memcpy_chain.c
  - **unresolved**: formula_branching_fractal — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: vendor/github_oss/adversarial/double_free_pattern.c — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/double_free_pattern.c
  - **vendor_cache**: vendor/github_oss/adversarial/xss_eval_sink.js — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/xss_eval_sink.js
  - **vendor_cache**: vendor/github_oss/adversarial/prototype_pollution.js — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/prototype_pollution.js
  - **vendor_cache**: vendor/github_oss/adversarial/race_unsafe.go — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/github_oss/adversarial/race_unsafe.go
  - **vendor_cache**: vendor/cybersecurity/samples/secure_buffer.c — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/cybersecurity/samples/secure_buffer.c
  - **unresolved**: adversarial_corpus — Named in panel source; add explicit public URL if this is an external authority

### Agriculture_Agroecology

- Benchmark: `data/agriculture_agroecology_gap_fill_benchmark.json` · records=276 · median%=0.018019024892929635
- Lean: `FSOT.Formal.AgricultureAgroecologyGapFillPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/

### Alternate_Base_Mathematics_Explorer_Panel

- Benchmark: `data/alternate_base_mathematics_explorer_panel_benchmark.json` · records=56 · median%=0.009504
- Ingest: `scripts/ingest_tier92_alternate_base_mathematics.py`
- Lean: `FSOT.Formal.AlternateBaseMathematicsExplorerPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: tier92_base_analysis_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier92_base_analysis_cache.json
  - **ingest_script**: scripts/ingest_tier92_alternate_base_mathematics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier92_alternate_base_mathematics.py

### Alternate_Base_Mathematics_Spine

- Benchmark: `data/alternate_base_mathematics_spine_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.AlternateBaseMathematicsSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier92_alternate_base_panels — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/

### Anthropology

- Benchmark: `data/anthropology_extension_benchmark.json` · records=160 · median%=0.019504399572476606
- Lean: `FSOT.Formal.AnthropologyExtensionPriors`
- Public / portable anchors:
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **unresolved**: linguistics_lab — Named in panel source; add explicit public URL if this is an external authority
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **unresolved**: linguistics_anthropology_bridge — Named in panel source; add explicit public URL if this is an external authority

### Architecture_Building_Science

- Benchmark: `data/architecture_building_science_gap_fill_benchmark.json` · records=43 · median%=0.07869745016115058
- Lean: `FSOT.Formal.ArchitectureBuildingScienceGapFillPriors`
- Public / portable anchors:
  - **unresolved**: ASHRAE_HVAC — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: climate_observed — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: weather_observed — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: ashrae_hvac_reference — Named in panel source; add explicit public URL if this is an external authority

### Arxiv_Brain_Knowledge_Panel

- Benchmark: `data/arxiv_brain_knowledge_panel_benchmark.json` · records=20 · median%=0.018003
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.ArxivBrainKnowledgePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\arxiv_brain_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/arxiv_brain_cache.json
  - **unresolved**: desktop_knowledge_brain — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Arxiv_Gravitational_Waves_Panel

- Benchmark: `data/arxiv_gravitational_waves_panel_benchmark.json` · records=60 · median%=0.01748
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.ArxivGravitationalWavesPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: arXiv API / metadata — https://arxiv.org/help/api/
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Arxiv_Primitives_Panel

- Benchmark: `data/arxiv_primitives_panel_benchmark.json` · records=22 · median%=0.031506
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.ArxivPrimitivesPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\arxiv_primitives_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/arxiv_primitives_cache.json
  - **api**: arXiv API / metadata — https://arxiv.org/help/api/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Arxiv_Primitives_V14

- Benchmark: `data/arxiv_primitives_v14_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.ArxivPrimitivesV14Priors`
- Public / portable anchors:
  - **vendor_cache**: vendor/arxiv_primitives/v14_run_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/arxiv_primitives/v14_run_summary.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Astrophysical_Structure_Crosswalk

- Benchmark: `data/astrophysical_structure_crosswalk_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.AstrophysicalStructureCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/stellar_structures/public_multiplicity_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/public_multiplicity_catalog.json
  - **unresolved**: crosswalk_panels — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus WDS/literature — https://github.com/WDS/literature
  - **unresolved**: literature hierarchical — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: WDS — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: WDS/literature sextuple — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: LIGO public GW150914 — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: LIGO/Virgo public GW170817 — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: LIGO/Virgo public GW190521 — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: LIGO public summary 2024 — Named in panel source; add explicit public URL if this is an external authority

### Atmospheric_Physics

- Benchmark: `data/atmospheric_physics_gap_fill_benchmark.json` · records=47 · median%=0.0
- Public / portable anchors:
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/

### Atomic_Physics

- Benchmark: `data/atomic_physics_gap_fill_benchmark.json` · records=80 · median%=0.0009504134401195552
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: SMILES_particle — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Bibliography_Corpus_Panel

- Benchmark: `data/bibliography_corpus_panel_benchmark.json` · records=20 · median%=0.013294
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.BibliographyCorpusPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\bibliography_corpus_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/bibliography_corpus_cache.json
  - **unresolved**: desktop_bibliography — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Bibliography_Lean_Corpus

- Benchmark: `data/bibliography_lean_corpus_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.BibliographyLeanCorpusPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/bibliography_corpus/bibliography_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/bibliography_corpus/bibliography_summary.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Binary_Decoder_Panel

- Benchmark: `data/binary_decoder_panel_benchmark.json` · records=20 · median%=2.1766e-05
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.BinaryDecoderPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\binary_decoder_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/binary_decoder_cache.json
  - **unresolved**: desktop_binary_decoder — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Binary_Decoder_Rendlesham

- Benchmark: `data/binary_decoder_rendlesham_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.BinaryDecoderRendleshamPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/binary_decoder/rendlesham_page14_trace.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/binary_decoder/rendlesham_page14_trace.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Biology_Developmental_Structural_Depth_Panel

- Benchmark: `data/biology_developmental_structural_depth_panel_benchmark.json` · records=24 · median%=0.015311
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.BiologyDevelopmentalStructuralDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\biology_developmental_structural_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/biology_developmental_structural_cache.json
  - **unresolved**: developmental_structural_biology_literature_anchors — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Biophysics_Public_Panel

- Benchmark: `data/biophysics_public_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.BiophysicsPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### BlackHole_WhiteHole_Cycle_Live_Panel

- Benchmark: `data/blackhole_whitehole_cycle_live_panel_benchmark.json` · records=24 · median%=0.026472
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.BlackHoleWhiteholeCycleLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\blackhole_whitehole_cycle_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/blackhole_whitehole_cycle_cache.json
  - **unresolved**: bh_wh_cycle_blueprint — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Botany

- Benchmark: `data/botany_extension_benchmark.json` · records=426 · median%=0.022236250385193387
- Lean: `FSOT.Formal.BotanyExtensionPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/

### Boundary_Partition_Tightening

- Benchmark: `data/boundary_partition_tightening_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.BoundaryPartitionTighteningPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Breakthrough_Discoveries_2024_2026

- Benchmark: `data/breakthrough_discoveries_2024_2026_benchmark.json` · records=21 · median%=0.0
- Ingest: `scripts/ingest_tier39_propulsion_electrical.py`
- Lean: `FSOT.Formal.BreakthroughDiscoveries20242026Priors`
- Public / portable anchors:
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **ingest_script**: scripts/ingest_tier39_propulsion_electrical.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier39_propulsion_electrical.py

### Breakthrough_Fusion_Spine

- Benchmark: `data/breakthrough_fusion_spine_benchmark.json` · records=146 · median%=0.0
- Public / portable anchors:
  - **unresolved**: qce_elm — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: recent_breakthroughs — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: magnetic_confinement — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fusion_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: public ELM literature + TechTimes/PRL summary — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json

### CERN_Open_Data_LHC

- Benchmark: `data/cern_open_data_lhc_benchmark.json` · records=83 · median%=0.013294
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.CernOpenDataLhcPriors`
- Public / portable anchors:
  - **dataset**: CERN Open Data — https://opendata.cern.ch/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### CRC_Handbook_Properties

- Benchmark: `data/crc_handbook_properties_benchmark.json` · records=391 · median%=0.026922
- Lean: `FSOT.Formal.CrcHandbookPropertiesPriors`
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### CVE_Codon_Hole_Falsification

- Benchmark: `data/cve_codon_hole_falsification_benchmark.json` · records=29 · median%=0.009186636881580057
- Lean: `FSOT.Formal.CVECodonHoleFalsificationPriors`
- Public / portable anchors:
  - **vendor_cache**: cisa_kev_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cisa_kev_summary.json
  - **unresolved**: code_genome_lib — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: external_oss_code_genome — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\cybersecurity\samples\vulnerable_legacy.c — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\cybersecurity\samples\secure_buffer.c — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\cybersecurity\samples\xss_sink_legacy.js — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\cybersecurity\samples\csp_safe_dom.js — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\cpython_ceval.c — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: OpenSSL source corpus (GitHub OSS genome) — https://github.com/openssl/openssl
  - **unresolved**: vendor\github_oss\snapshots\python_dictobject.c — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\redis_sds.c — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\sqlite_mem.c — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\express_router.js — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\nodejs_buffer.js — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: vendor\github_oss\snapshots\react_hooks.js — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: cwe_codon_map — Named in panel source; add explicit public URL if this is an external authority

### Canonical_Oracle_Panel

- Benchmark: `data/canonical_oracle_panel_benchmark.json` · records=24 · median%=0.000561846
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.CanonicalOraclePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\canonical_oracle_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/canonical_oracle_cache.json
  - **unresolved**: desktop_canonical_oracle — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Cardiology

- Benchmark: `data/cardiology_extension_benchmark.json` · records=45 · median%=0.030622122938654326
- Lean: `FSOT.Formal.CardiologyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: cardiology_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: clinical_medicine_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: cardiology_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: pk_reference — Named in panel source; add explicit public URL if this is an external authority

### Cardiology_Panel

- Benchmark: `data/cardiology_panel_benchmark.json` · records=20 · median%=0.015311
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.CardiologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: AHA/ESC cardiology reference — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Cartography_GIS_Panel

- Benchmark: `data/cartography_gis_panel_benchmark.json` · records=48 · median%=0.018855999999999998
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.CartographyGisPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: Natural Earth — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Certified_Agent_Formal_Panel

- Benchmark: `data/certified_agent_formal_panel_benchmark.json` · records=21 · median%=0.014767
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.CertifiedAgentFormalPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\certified_agent_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/certified_agent_cache.json
  - **unresolved**: desktop_certified_agent — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Certified_Agent_Qwen

- Benchmark: `data/certified_agent_qwen_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.CertifiedAgentQwenPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/certified_agent/certified_agent_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/certified_agent/certified_agent_summary.json
  - **vendor_cache**: vendor/certified_agent/fsot_workspace.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/certified_agent/fsot_workspace.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Chaos_Mediated_Phase_Transitions

- Benchmark: `data/chaos_mediated_phase_transitions_benchmark.json` · records=21 · median%=0.03147898006445882
- Lean: `FSOT.Formal.ChaosMediatedPhaseTransitionsPriors`
- Public / portable anchors:
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json
  - **vendor_cache**: particle_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/particle_physics_benchmark.json
  - **vendor_cache**: higgs_branching_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/higgs_branching_benchmark.json

### Chemical_Engineering

- Benchmark: `data/chemical_engineering_extension_benchmark.json` · records=186 · median%=0.0010333425185953097
- Lean: `FSOT.Formal.ChemicalEngineeringExtensionPriors`
- Public / portable anchors:
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **api**: ChEMBL API — https://www.ebi.ac.uk/chembl/
  - **unresolved**: THERMODYNAMICS_ENGINEERING_rules — Named in panel source; add explicit public URL if this is an external authority
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **unresolved**: math_generator_chem_eng — Named in panel source; add explicit public URL if this is an external authority

### Chemical_Structure_Stability_Panel

- Benchmark: `data/chemical_structure_stability_panel_benchmark.json` · records=32 · median%=0.00206
- Lean: `FSOT.Formal.ChemicalStructureStabilityPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: pubchem_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pubchem_summary.json
  - **vendor_cache**: nist_codata_constants_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/nist_codata_constants_benchmark.json

### Circuit_Component_Emergence_Panel

- Benchmark: `data/circuit_component_emergence_panel_benchmark.json` · records=57 · median%=0.020755
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\industry_component_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/industry_component_catalog.json
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\tier96_cache\industry_component_catalog_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/tier96_cache/industry_component_catalog_cache.json

### Civil_Engineering

- Benchmark: `data/civil_engineering_extension_benchmark.json` · records=37 · median%=0.0335259880736416
- Lean: `FSOT.Formal.CivilEngineeringExtensionPriors`
- Public / portable anchors:
  - **unresolved**: civil_engineering_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: materials_engineering — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: MATERIALS_SCIENCE_rules — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: civil_engineering_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_generator_civil — Named in panel source; add explicit public URL if this is an external authority

### Civil_Engineering_Panel

- Benchmark: `data/civil_engineering_panel_benchmark.json` · records=20 · median%=0.01341
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.CivilEngineeringPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: ASCE/structural engineering reference — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### ClinicalTrials_Medical_Panel

- Benchmark: `data/clinicaltrials_medical_panel_benchmark.json` · records=394 · median%=0.0
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.ClinicaltrialsMedicalPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://clinicaltrials.gov/api/v2/ — https://clinicaltrials.gov/api/v2/
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### Clinical_Medicine

- Benchmark: `data/clinical_medicine_extension_benchmark.json` · records=260 · median%=0.002458296751538192
- Lean: `FSOT.Formal.ClinicalMedicineExtensionPriors`
- Public / portable anchors:
  - **unresolved**: pharmacokinetics — Named in panel source; add explicit public URL if this is an external authority
  - **api**: ChEMBL API — https://www.ebi.ac.uk/chembl/
  - **unresolved**: immunology — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: pk_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: pharmacology — Named in panel source; add explicit public URL if this is an external authority

### Code_Genome_Structure

- Benchmark: `data/code_genome_structure_cybersecurity_benchmark.json` · records=176 · median%=0.0
- Lean: `FSOT.Formal.CodeGenomeStructurePriors`
- Public / portable anchors:
  - **unresolved**: code_genome_depth_pass — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: 9_language_bridges — Named in panel source; add explicit public URL if this is an external authority
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: code_genome_language_registry — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_evaluator_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: rust_lean_genome — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: trinary_genome — Named in panel source; add explicit public URL if this is an external authority
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### Coding_Structure_Verifier_Panel

- Benchmark: `data/coding_structure_verifier_panel_benchmark.json` · records=43 · median%=0.0
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/programming_language_laws_benchmark.json — https://github.com/data/programming_language_laws_benchmark.json
  - **dataset**: GitHub OSS corpus data/external_oss_code_genome_benchmark.json — https://github.com/data/external_oss_code_genome_benchmark.json
  - **unresolved**: I:\Protofluid-Language-Translator-2.0-Zig — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: C:\Users\damia\Desktop\fsot code language — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: I:\fsot-neuron-zig — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus openssl/openssl — https://github.com/openssl/openssl
  - **dataset**: GitHub OSS corpus torvalds/linux — https://github.com/torvalds/linux
  - **dataset**: GitHub OSS corpus rust-lang/rust — https://github.com/rust-lang/rust
  - **dataset**: GitHub OSS corpus python/cpython — https://github.com/python/cpython
  - **dataset**: GitHub OSS corpus nodejs/node — https://github.com/nodejs/node
  - **unresolved**: SHIP_BASELINE_MULTILANG — Named in panel source; add explicit public URL if this is an external authority

### Cold_Fusion_Candidate_Prereg_Scaffold

- Benchmark: `data/cold_fusion_candidate_prereg_scaffold_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.ColdFusionCandidatePreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: term3_acoustic_bleed_depth_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/term3_acoustic_bleed_depth_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Cold_Fusion_Lab_Synthesis_Crosswalk

- Benchmark: `data/cold_fusion_lab_synthesis_crosswalk_benchmark.json` · records=49 · median%=7.9e-05
- Lean: `FSOT.Formal.ColdFusionLabSynthesisCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: cold_fusion_candidate_prereg_scaffold_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cold_fusion_candidate_prereg_scaffold_benchmark.json
  - **vendor_cache**: undiscovered_element_candidate_prereg_scaffold_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/undiscovered_element_candidate_prereg_scaffold_benchmark.json
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\lab_synthesis\heavy_ion_reaction_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/lab_synthesis/heavy_ion_reaction_anchors.json
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\lab_synthesis\metamaterial_fluid_prereg_candidates.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/lab_synthesis/metamaterial_fluid_prereg_candidates.json

### Compact_Object_Binary_Events

- Benchmark: `data/compact_object_binary_events_benchmark.json` · records=40 · median%=0.010049
- Lean: `FSOT.Formal.CompactObjectBinaryEventsPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/stellar_structures/gwosc_public_events.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/gwosc_public_events.json

### Compactification_Ladder

- Benchmark: `data/compactification_ladder_benchmark.json` · records=60 · median%=0.0220747159758794
- Lean: `FSOT.Formal.CompactificationLadderPriors`
- Public / portable anchors:
  - **vendor_cache**: compactification_ladder_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_manifest.yaml
  - **dataset**: GitHub OSS corpus data/higgs_mass_benchmark.json — https://github.com/data/higgs_mass_benchmark.json
  - **dataset**: GitHub OSS corpus data/particle_physics_gap_fill_benchmark.json — https://github.com/data/particle_physics_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/atomic_physics_gap_fill_benchmark.json — https://github.com/data/atomic_physics_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/materials_species_bridge_benchmark.json — https://github.com/data/materials_species_bridge_benchmark.json
  - **dataset**: GitHub OSS corpus data/synthetic_biology_benchmark.json — https://github.com/data/synthetic_biology_benchmark.json
  - **dataset**: GitHub OSS corpus data/immunology_benchmark.json — https://github.com/data/immunology_benchmark.json
  - **dataset**: GitHub OSS corpus data/planetary_structure_benchmark.json — https://github.com/data/planetary_structure_benchmark.json
  - **dataset**: GitHub OSS corpus data/breakthrough_discoveries_2024_2026_benchmark.json — https://github.com/data/breakthrough_discoveries_2024_2026_benchmark.json
  - **dataset**: GitHub OSS corpus data/climate_observed_benchmark.json — https://github.com/data/climate_observed_benchmark.json
  - **dataset**: GitHub OSS corpus data/cosmology_extended_benchmark.json — https://github.com/data/cosmology_extended_benchmark.json

### Complexity_Folding_Emergence_Panel

- Benchmark: `data/complexity_folding_emergence_panel_benchmark.json` · records=29 · median%=0.02658792169940266
- Lean: `FSOT.Formal.ComplexityFoldingEmergencePanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: core_formula_fractal_branch_index.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/core_formula_fractal_branch_index.json

### Condensed_Matter_Superconductivity_Depth_Panel

- Benchmark: `data/condensed_matter_superconductivity_depth_panel_benchmark.json` · records=24 · median%=0.033841
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.CondensedMatterSuperconductivityDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\condensed_matter_superconductivity_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/condensed_matter_superconductivity_cache.json
  - **unresolved**: literature_Tc — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Consciousness_Econ

- Benchmark: `data/consciousness_econ_benchmark.json` · records=32 · median%=0.020728
- Ingest: `scripts/ingest_anomaly_public_data.py`
- Lean: `FSOT.Formal.ConsciousnessEconPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/consciousness_reference_observables.json — https://github.com/data/consciousness_reference_observables.json
  - **dataset**: GitHub OSS corpus data/consciousness_resonance_reference.json — https://github.com/data/consciousness_resonance_reference.json
  - **api**: anage — https://genomics.senescence.info/species/dataset.zip
  - **dataset**: GitHub OSS corpus scripts/consciousness_econ_lib.py — https://github.com/scripts/consciousness_econ_lib.py
  - **ingest_script**: scripts/ingest_anomaly_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_anomaly_public_data.py

### Consciousness_Expansion_Spine

- Benchmark: `data/consciousness_expansion_spine_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.ConsciousnessExpansionSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier90_consciousness_panels — Named in panel source; add explicit public URL if this is an external authority
  - **api**: anage — https://genomics.senescence.info/species/dataset.zip
  - **api**: openneuro — https://openneuro.org/crn/graphql
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Consciousness_Galactic_Orbital_Bridge

- Benchmark: `data/consciousness_galactic_orbital_bridge_benchmark.json` · records=48 · median%=0.036757197413939124
- Lean: `FSOT.Formal.ConsciousnessGalacticOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/anthropology_extension_benchmark.json — https://github.com/data/anthropology_extension_benchmark.json
  - **dataset**: GitHub OSS corpus data/arxiv_primitives_v14_benchmark.json — https://github.com/data/arxiv_primitives_v14_benchmark.json
  - **dataset**: GitHub OSS corpus data/binary_decoder_rendlesham_benchmark.json — https://github.com/data/binary_decoder_rendlesham_benchmark.json
  - **dataset**: GitHub OSS corpus data/boundary_partition_tightening_benchmark.json — https://github.com/data/boundary_partition_tightening_benchmark.json

### Consciousness_Genetics_Coupling_Panel

- Benchmark: `data/consciousness_genetics_coupling_panel_benchmark.json` · records=24 · median%=0.031506
- Ingest: `scripts/ingest_tier93_dual_wave.py`
- Lean: `FSOT.Formal.ConsciousnessGeneticsCouplingPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier93_consciousness_genetics_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_consciousness_genetics_cache.json
  - **unresolved**: tier90_observer_effect — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier93_dual_wave.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier93_dual_wave.py

### Consciousness_Genetics_Species_Panel

- Benchmark: `data/consciousness_genetics_species_panel_benchmark.json` · records=27 · median%=0.022236
- Ingest: `scripts/ingest_tier93_dual_wave.py`
- Lean: `FSOT.Formal.ConsciousnessGeneticsSpeciesPanelPriors`
- Public / portable anchors:
  - **api**: NCBI E-utilities / Gene / datasets — https://www.ncbi.nlm.nih.gov/books/NBK25501/
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **ingest_script**: scripts/ingest_tier93_dual_wave.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier93_dual_wave.py

### Consciousness_Lean_Route_Credibility

- Benchmark: `data/consciousness_lean_route_credibility_benchmark.json` · records=101 · median%=0.018003
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:consciousness — Named in panel source; add explicit public URL if this is an external authority

### Consciousness_Soul_Bridge

- Benchmark: `data/consciousness_soul_bridge_benchmark.json` · records=24 · median%=0.0
- Ingest: `scripts/ingest_fringe_desktop_data.py`
- Lean: `FSOT.Formal.ConsciousnessSoulBridgePriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/consciousness_soul_bridge_reference.json — https://github.com/data/consciousness_soul_bridge_reference.json
  - **vendor_cache**: vendor/fringe_desktop/soul_simulator_manifest_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/soul_simulator_manifest_summary.json
  - **vendor_cache**: vendor/fringe_desktop/intelligence_compressor_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/intelligence_compressor_summary.json
  - **vendor_cache**: vendor/fringe_desktop/vibrafsot_progress_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/vibrafsot_progress_summary.json
  - **dataset**: GitHub OSS corpus scripts/consciousness_soul_bridge_lib.py — https://github.com/scripts/consciousness_soul_bridge_lib.py
  - **ingest_script**: scripts/ingest_fringe_desktop_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_fringe_desktop_data.py

### Consciousness_Species_Multi_Panel

- Benchmark: `data/consciousness_species_multi_panel_benchmark.json` · records=269 · median%=0.0201195
- Ingest: `scripts/ingest_tier90_consciousness_expansion.py`
- Lean: `FSOT.Formal.ConsciousnessSpeciesMultiPanelPriors`
- Public / portable anchors:
  - **url**: https://genomics.senescence.info/species/dataset.zip — https://genomics.senescence.info/species/dataset.zip
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: G:\FSOT-PublicData\anomaly_observables\consciousness\tier90_species_panel_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_species_panel_cache.json
  - **ingest_script**: scripts/ingest_tier90_consciousness_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier90_consciousness_expansion.py

### Cosmology_Anomaly_Deep_Panel

- Benchmark: `data/cosmology_anomaly_deep_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.CosmologyAnomalyDeepPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Cosmology_Extended

- Benchmark: `data/cosmology_extended_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.CosmologyExtendedPriors`
- Public / portable anchors:
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Creative_Arts_Math_Spine

- Benchmark: `data/creative_arts_math_spine_benchmark.json` · records=56 · median%=0.0
- Lean: `FSOT.Formal.CreativeArtsMathSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier61_creative_panels — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: culinary_arts_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/culinary_arts_benchmark.json
  - **vendor_cache**: linguistics_formal_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/linguistics_formal_benchmark.json

### Crossref_Scholarly_Panel

- Benchmark: `data/crossref_scholarly_panel_benchmark.json` · records=200 · median%=0.01382
- Ingest: `scripts/ingest_tier81_public_verifiable.py`
- Lean: `FSOT.Formal.CrossrefScholarlyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://api.crossref.org/ — https://api.crossref.org/
  - **ingest_script**: scripts/ingest_tier81_public_verifiable.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier81_public_verifiable.py

### Cryptography_Technology

- Benchmark: `data/cryptography_technology_cybersecurity_benchmark.json` · records=44 · median%=0.047520672006218234
- Lean: `FSOT.Formal.CryptographyTechnologyPriors`
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: CRYPTOGRAPHY_RULES — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: cryptography_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: cryptography_technology_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: CRYPTOGRAPHY_RULES.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/CRYPTOGRAPHY_RULES.json
  - **unresolved**: math_generator_rules_eval — Named in panel source; add explicit public URL if this is an external authority

### Culinary_Fermentation_Maillard_Panel

- Benchmark: `data/culinary_fermentation_maillard_panel_benchmark.json` · records=151 · median%=0.040788
- Ingest: `scripts/ingest_tier86_scientific_expansion.py`
- Lean: `FSOT.Formal.CulinaryFermentationMaillardPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier86_cache\culinary_fermentation_maillard_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier86_cache/culinary_fermentation_maillard_cache.json
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **unresolved**: fermentation_reference — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier86_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier86_scientific_expansion.py

### DESI_wa_Constraint

- Benchmark: `data/desi_wa_constraint_benchmark.json` · records=27 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\data\dark_energy_cpl_reference.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/dark_energy_cpl_reference.json
  - **dataset**: GitHub OSS corpus scripts/dark_energy_dual_readout_lib.py — https://github.com/scripts/dark_energy_dual_readout_lib.py

### Dark_Energy_CPL

- Benchmark: `data/dark_energy_cpl_benchmark.json` · records=14 · median%=0.280515
- Ingest: `scripts/ingest_anomaly_public_data.py`
- Lean: `FSOT.Formal.DarkEnergyCPLPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/dark_energy_cpl_reference.json — https://github.com/data/dark_energy_cpl_reference.json
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **dataset**: GitHub OSS corpus scripts/dark_energy_dual_readout_lib.py — https://github.com/scripts/dark_energy_dual_readout_lib.py
  - **ingest_script**: scripts/ingest_anomaly_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_anomaly_public_data.py

### Dark_Sector_Open_Problems

- Benchmark: `data/dark_sector_open_problems_benchmark.json` · records=24 · median%=0.000561846
- Lean: `FSOT.Formal.DarkSectorOpenProblemsPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **dataset**: GitHub OSS corpus data/stumped_observables_reference.json — https://github.com/data/stumped_observables_reference.json
  - **dataset**: GitHub OSS corpus scripts/dark_energy_dual_readout_lib.py — https://github.com/scripts/dark_energy_dual_readout_lib.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### Desktop_Application_Wiring_Spine

- Benchmark: `data/desktop_application_wiring_spine_benchmark.json` · records=81 · median%=0.0
- Lean: `FSOT.Formal.DesktopApplicationWiringSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier88_application_wiring_panels — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: desktop_project_crosswalk — Named in panel source; add explicit public URL if this is an external authority

### Desktop_Observer_Loop_Panel

- Benchmark: `data/desktop_observer_loop_panel_benchmark.json` · records=24 · median%=0.0010245
- Public / portable anchors:
  - **unresolved**: desktop_observer_loop_lib — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py

### Distant_Island_Emergence_Simulation

- Benchmark: `data/distant_island_emergence_simulation_benchmark.json` · records=26 · median%=0.0
- Lean: `FSOT.Formal.DistantIslandEmergenceSimulationPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Distant_Island_Z128_Z132_Deep_Panel

- Benchmark: `data/distant_island_z128_z132_deep_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.DistantIslandZ128Z132DeepPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Domain_Coupling_Simulation

- Benchmark: `data/domain_coupling_simulation_benchmark.json` · records=18617 · median%=0.0
- Lean: `FSOT.Formal.DomainCouplingSimulationPriors`
- Public / portable anchors:
  - **unresolved**: maps_to_lean — Named in panel source; add explicit public URL if this is an external authority
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: magnetosphere_cluster — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: crosswalk_modules — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fluidlink_fpc_timing — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Domain_Coupling_Simulation_Refresh_Panel

- Benchmark: `data/domain_coupling_simulation_refresh_panel_benchmark.json` · records=22 · median%=0.0
- Lean: `FSOT.Formal.DomainCouplingSimulationRefreshPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **vendor_cache**: fluid_spacetime_observable_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fluid_spacetime_observable_spine_benchmark.json

### Domain_Orbital_Predictions

- Benchmark: `data/domain_orbital_predictions_benchmark.json` · records=12 · median%=0.0
- Lean: `FSOT.Formal.DomainOrbitalPredictionsPriors`
- Public / portable anchors:
  - **vendor_cache**: orbital_predictions_registry.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/orbital_predictions_registry.yaml
  - **unresolved**: tier_l_orbital_gap_fill — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: tier_m_toe_unity — Named in panel source; add explicit public URL if this is an external authority

### Dzhanibekov_Intermediate_Axis_FSOT_Panel

- Benchmark: `data/dzhanibekov_intermediate_axis_fsot_panel_benchmark.json` · records=32 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\hardware\dzhanibekov_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/hardware/dzhanibekov_public_anchors.json
  - **unresolved**: intermediate_axis_theorem / tennis_racket / Dzhanibekov public literature — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: x.com/dr_logvinovich/status/2084655064602358240 — Named in panel source; add explicit public URL if this is an external authority

### ESP32_Platform_Engineering_Panel

- Benchmark: `data/esp32_platform_engineering_panel_benchmark.json` · records=34 · median%=0.020755
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\industry_component_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/industry_component_catalog.json
  - **unresolved**: verification/esp32/fsot_esp32_observer — Named in panel source; add explicit public URL if this is an external authority

### Early_Lean_MC_Panel

- Benchmark: `data/early_lean_mc_panel_benchmark.json` · records=21 · median%=2.1766e-05
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.EarlyLeanMcPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\early_lean_mc_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/early_lean_mc_cache.json
  - **unresolved**: desktop_early_lean_mc — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Ecology

- Benchmark: `data/ecology_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.EcologyPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/

### Ecology

- Benchmark: `data/ecology_gap_fill_benchmark.json` · records=627 · median%=0.017789000308164125
- Lean: `FSOT.Formal.EcologyPublicPanelPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **unresolved**: biology_strict — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: evolution_operon — Named in panel source; add explicit public URL if this is an external authority
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/

### Econometrics

- Benchmark: `data/econometrics_gap_fill_benchmark.json` · records=172 · median%=0.12920090413715177
- Lean: `FSOT.Formal.EconometricsGapFillPriors`
- Public / portable anchors:
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: economics_gap_fill — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: economics_yoy_bridge — Named in panel source; add explicit public URL if this is an external authority

### Economics

- Benchmark: `data/economics_gap_fill_benchmark.json` · records=157 · median%=0.1292009041371501
- Public / portable anchors:
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/

### Econophysics

- Benchmark: `data/econophysics_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.EconophysicsPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/

### Electrical_Power_Systems

- Benchmark: `data/electrical_power_systems_benchmark.json` · records=23 · median%=0.000561846
- Ingest: `scripts/ingest_tier39_propulsion_electrical.py`
- Lean: `FSOT.Formal.ElectricalPowerSystemsPriors`
- Public / portable anchors:
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **literature**: SH0ES / local distance ladder H0 (Riess et al. series) — https://ui.adsabs.harvard.edu/
  - **unresolved**: 4 — Named in panel source; add explicit public URL if this is an external authority
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **api**: arXiv API / metadata — https://arxiv.org/help/api/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Planck Collaboration cosmological parameters — https://www.cosmos.esa.int/web/planck
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - … +11 more in JSON

### Element_Synthesis_Condition_Scaffold

- Benchmark: `data/element_synthesis_condition_scaffold_benchmark.json` · records=45 · median%=0.000787
- Lean: `FSOT.Formal.ElementSynthesisConditionScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: superheavy_element_stability_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/superheavy_element_stability_panel_benchmark.json

### Energy_AI_Orbital_Bridge

- Benchmark: `data/energy_ai_orbital_bridge_benchmark.json` · records=48 · median%=0.027544107556407217
- Lean: `FSOT.Formal.EnergyAIOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/acoustic_resonance_materials_benchmark.json — https://github.com/data/acoustic_resonance_materials_benchmark.json
  - **dataset**: GitHub OSS corpus data/agriculture_agroecology_gap_fill_benchmark.json — https://github.com/data/agriculture_agroecology_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/architecture_building_science_gap_fill_benchmark.json — https://github.com/data/architecture_building_science_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/chaos_mediated_phase_transitions_benchmark.json — https://github.com/data/chaos_mediated_phase_transitions_benchmark.json

### Energy_Lean_Route_Credibility

- Benchmark: `data/energy_lean_route_credibility_benchmark.json` · records=40 · median%=0.039349
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:energy — Named in panel source; add explicit public URL if this is an external authority

### Energy_Neural_Orbital_Bridge

- Benchmark: `data/energy_neural_orbital_bridge_benchmark.json` · records=48 · median%=0.018002668701796887
- Lean: `FSOT.Formal.EnergyNeuralOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/acoustic_resonance_materials_benchmark.json — https://github.com/data/acoustic_resonance_materials_benchmark.json
  - **dataset**: GitHub OSS corpus data/agriculture_agroecology_gap_fill_benchmark.json — https://github.com/data/agriculture_agroecology_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/architecture_building_science_gap_fill_benchmark.json — https://github.com/data/architecture_building_science_gap_fill_benchmark.json
  - **dataset**: GitHub OSS corpus data/chaos_mediated_phase_transitions_benchmark.json — https://github.com/data/chaos_mediated_phase_transitions_benchmark.json

### Engineering_Hardware_Code_Spine

- Benchmark: `data/engineering_hardware_code_spine_benchmark.json` · records=93 · median%=0.0
- Public / portable anchors:
  - **unresolved**: esp32_platform — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: coding_structure_verifier — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: tier96_circuit — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_gpu_cuda — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_gpu_parity_verify — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus openssl/openssl — https://github.com/openssl/openssl
  - **dataset**: GitHub OSS corpus torvalds/linux — https://github.com/torvalds/linux
  - **dataset**: GitHub OSS corpus rust-lang/rust — https://github.com/rust-lang/rust
  - **dataset**: GitHub OSS corpus parity/golden.json — https://github.com/parity/golden.json
  - **vendor_cache**: results/competitive/beat_cuda.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/beat_cuda.json
  - **vendor_cache**: results/parity/parity_ledger.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/parity/parity_ledger.json

### Entomology

- Benchmark: `data/entomology_extension_benchmark.json` · records=430 · median%=0.022236250385189223
- Ingest: `scripts/build_tier_f_extension_benchmarks.py`
- Lean: `FSOT.Formal.EntomologyExtensionPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **unresolved**: zoology_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **unresolved**: zoology_insect_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/build_tier_f_extension_benchmarks.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/build_tier_f_extension_benchmarks.py

### Entomology_Panel

- Benchmark: `data/entomology_panel_benchmark.json` · records=90 · median%=0.006006
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.EntomologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Environmental_Engineering

- Benchmark: `data/environmental_engineering_extension_benchmark.json` · records=1117 · median%=0.009009512446467327
- Lean: `FSOT.Formal.EnvironmentalEngineeringExtensionPriors`
- Public / portable anchors:
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/

### Epidemiology

- Benchmark: `data/epidemiology_extension_benchmark.json` · records=20 · median%=0.03062212293865052
- Lean: `FSOT.Formal.EpidemiologyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: epidemiology_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: epidemiology_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Epidemiology_Panel

- Benchmark: `data/epidemiology_panel_benchmark.json` · records=24 · median%=0.015311
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.EpidemiologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Ethology_Panel

- Benchmark: `data/ethology_panel_benchmark.json` · records=100 · median%=0.006607
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.EthologyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Evolution_Operon

- Benchmark: `data/evolution_operon_benchmark.json` · records=20 · median%=0.0
- Public / portable anchors:
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **literature**: SH0ES / local distance ladder H0 (Riess et al. series) — https://ui.adsabs.harvard.edu/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/

### Existence_Simulation_Gap_Fill_Panel

- Benchmark: `data/existence_simulation_gap_fill_panel_benchmark.json` · records=20 · median%=3.8622500000000005e-05
- Public / portable anchors:
  - **unresolved**: existence_simulation_lib — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **vendor_cache**: stumped_observables_reference.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_reference.json
  - **vendor_cache**: domain_orbital_prediction_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_orbital_prediction_report.json
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Existence_Simulation_Refinement_Panel

- Benchmark: `data/existence_simulation_refinement_panel_benchmark.json` · records=26 · median%=0.0141195
- Public / portable anchors:
  - **unresolved**: existence_simulation_refinement_lib — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: vendor/smiles/FSOT_SMILES_Lab_Dataset.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json
  - **vendor_cache**: existence_simulation_failure_clusters_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/existence_simulation_failure_clusters_manifest.yaml

### Exogeology

- Benchmark: `data/exogeology_extension_benchmark.json` · records=316 · median%=0.0
- Lean: `FSOT.Formal.ExogeologyExtensionPriors`
- Public / portable anchors:
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **unresolved**: planetary_structure — Named in panel source; add explicit public URL if this is an external authority
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/

### Exogeology_Panel

- Benchmark: `data/exogeology_panel_benchmark.json` · records=100 · median%=0.026472
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.ExogeologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Exoplanet_System_Architecture

- Benchmark: `data/exoplanet_system_architecture_benchmark.json` · records=882 · median%=0.0
- Lean: `FSOT.Formal.ExoplanetSystemArchitecturePriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/public_data/nasa_exoplanet/nasa_exoplanet_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/nasa_exoplanet/nasa_exoplanet_summary.json

### Experimental_Base_Mathematics_Panel

- Benchmark: `data/experimental_base_mathematics_panel_benchmark.json` · records=36 · median%=0.009504
- Ingest: `scripts/ingest_tier93_dual_wave.py`
- Lean: `FSOT.Formal.ExperimentalBaseMathematicsPanelPriors`
- Public / portable anchors:
  - **unresolved**: tier92_base_analysis — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: tier93_experimental_base_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_experimental_base_cache.json
  - **ingest_script**: scripts/ingest_tier93_dual_wave.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier93_dual_wave.py

### External_OSS_Code_Genome

- Benchmark: `data/external_oss_code_genome_benchmark.json` · records=161 · median%=0.0
- Lean: `FSOT.Formal.ExternalOSSCodeGenomePriors`
- Public / portable anchors:
  - **unresolved**: github_open_source — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: code_genome_crosswalk — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: github_oss_code_genome_manifest — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus openssl/openssl — https://github.com/openssl/openssl
  - **dataset**: GitHub OSS corpus torvalds/linux — https://github.com/torvalds/linux
  - **dataset**: GitHub OSS corpus rust-lang/rust — https://github.com/rust-lang/rust
  - **dataset**: GitHub OSS corpus python/cpython — https://github.com/python/cpython
  - **dataset**: GitHub OSS corpus nodejs/node — https://github.com/nodejs/node
  - **dataset**: GitHub OSS corpus expressjs/express — https://github.com/expressjs/express
  - **dataset**: GitHub OSS corpus golang/go — https://github.com/golang/go
  - **dataset**: GitHub OSS corpus ziglang/zig — https://github.com/ziglang/zig
  - **dataset**: GitHub OSS corpus leanprover/lean4 — https://github.com/leanprover/lean4
  - **dataset**: GitHub OSS corpus sqlite/sqlite — https://github.com/sqlite/sqlite
  - **dataset**: GitHub OSS corpus redis/redis — https://github.com/redis/redis
  - **dataset**: GitHub OSS corpus pytorch/pytorch — https://github.com/pytorch/pytorch
  - **dataset**: GitHub OSS corpus kubernetes/client-go — https://github.com/kubernetes/client-go
  - **dataset**: GitHub OSS corpus facebook/react — https://github.com/facebook/react
  - **dataset**: GitHub OSS corpus openjdk/jdk — https://github.com/openjdk/jdk
  - **dataset**: GitHub OSS corpus JetBrains/kotlin — https://github.com/JetBrains/kotlin
  - **dataset**: GitHub OSS corpus apple/swift — https://github.com/apple/swift
  - **dataset**: GitHub OSS corpus haskell/bytestring — https://github.com/haskell/bytestring
  - **dataset**: GitHub OSS corpus simonmar/async — https://github.com/simonmar/async
  - **unresolved**: code_genome_structure_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_risk_evaluator_cybersecurity_benchmark — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_language_bridges — Named in panel source; add explicit public URL if this is an external authority

### FPC_Fluidlink_Timing_Deep_Panel

- Benchmark: `data/fpc_fluidlink_timing_deep_panel_benchmark.json` · records=24 · median%=1.0883e-05
- Lean: `FSOT.Formal.FpcFluidlinkTimingDeepPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fpc_temporal_coupling_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fpc_temporal_coupling_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### FPC_Temporal_Coupling

- Benchmark: `data/fpc_temporal_coupling_benchmark.json` · records=24 · median%=0.000637597
- Lean: `FSOT.Formal.FPCTemporalCouplingPriors`
- Public / portable anchors:
  - **vendor_cache**: time_emergence_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_manifest.yaml
  - **unresolved**: fluidlink_fpc_timing — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### FSOT_Aggregate_Organized_Panel

- Benchmark: `data/fsot_aggregate_organized_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.FsotAggregateOrganizedPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: unified_db_domain_index.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/unified_db_domain_index.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### FSOT_Aggregate_Unified_DB

- Benchmark: `data/fsot_aggregate_unified_db_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.FsotAggregateUnifiedDbPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/fsot_aggregate/FSOT_Mathematical_Database_Unified.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/FSOT_Mathematical_Database_Unified.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### FSOT_C_Pack_Parity_Panel

- Benchmark: `data/fsot_c_pack_parity_panel_benchmark.json` · records=24 · median%=0.0
- Public / portable anchors:
  - **unresolved**: C:\Users\damia\Desktop\FSOT-2.1-Lean\verification\c\fsot_pack_parity\fsot_pack_parity.c — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### FSOT_Cache_Hierarchy_Panel

- Benchmark: `data/fsot_cache_hierarchy_panel_benchmark.json` · records=61 · median%=0.0
- Public / portable anchors:
  - **unresolved**: hardware_depth_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: industry_x86_cache_classes — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\data\hardware_competitive_refine_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/hardware_competitive_refine_report.json

### FSOT_GPU_CUDA_Competitive_Panel

- Benchmark: `data/fsot_gpu_cuda_competitive_panel_benchmark.json` · records=27 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/competitive/beat_cuda.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/beat_cuda.json
  - **dataset**: GitHub OSS corpus parity/golden.json — https://github.com/parity/golden.json
  - **unresolved**: phase2_native_gpu/cuda/fsot_beat_cuda.cu — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: gate=0.50 no_exp — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/competitive/flash_attention_track.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/flash_attention_track.json
  - **vendor_cache**: results/competitive/long_seq_and_norm.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/long_seq_and_norm.json

### FSOT_GPU_Engineering_Spine

- Benchmark: `data/fsot_gpu_engineering_spine_benchmark.json` · records=40 · median%=0.0
- Public / portable anchors:
  - **unresolved**: fsot_gpu_cuda — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_gpu_parity — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: esp32_platform — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: coding_structure — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: GitHub OSS corpus parity/golden.json — https://github.com/parity/golden.json
  - **vendor_cache**: results/parity/parity_ledger.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/parity/parity_ledger.json
  - **dataset**: GitHub OSS corpus openssl/openssl — https://github.com/openssl/openssl
  - **dataset**: GitHub OSS corpus torvalds/linux — https://github.com/torvalds/linux

### FSOT_GPU_Parity_Verify_Panel

- Benchmark: `data/fsot_gpu_parity_verify_panel_benchmark.json` · records=48 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/parity/parity_ledger.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/parity/parity_ledger.json
  - **vendor_cache**: results/industry_lm/fsot21_verify.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/industry_lm/fsot21_verify.json
  - **unresolved**: phase1_formal_gpu/ — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: phase2_native_gpu/cuda/ — Named in panel source; add explicit public URL if this is an external authority

### FSOT_Hardware_Depth_Spine

- Benchmark: `data/fsot_hardware_depth_spine_benchmark.json` · records=170 · median%=0.0
- Public / portable anchors:
  - **unresolved**: cache — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: interconnect — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: processor — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: ram — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: c_parity — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/phase0/fsot_scalar_gpu.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/fsot_scalar_gpu.json
  - **dataset**: GitHub OSS corpus psutil/host — https://github.com/psutil/host

### FSOT_Interconnect_Coherence_Panel

- Benchmark: `data/fsot_interconnect_coherence_panel_benchmark.json` · records=62 · median%=0.0
- Public / portable anchors:
  - **unresolved**: hardware_depth_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_hardware_kernel — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: qemu_bios — Named in panel source; add explicit public URL if this is an external authority

### FSOT_Processor_Function_Panel

- Benchmark: `data/fsot_processor_function_panel_benchmark.json` · records=24 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: phase1_formal_gpu/lean/Trinary.lean — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: phase1_formal_gpu/isabelle/Trinary.thy — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/competitive/beat_cuda.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/competitive/beat_cuda.json
  - **vendor_cache**: results/phase0/gpu_probe.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/gpu_probe.json
  - **vendor_cache**: results/phase0/fsot_scalar_gpu.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/fsot_scalar_gpu.json
  - **dataset**: GitHub OSS corpus psutil/host — https://github.com/psutil/host
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### FSOT_RAM_Function_Panel

- Benchmark: `data/fsot_ram_function_panel_benchmark.json` · records=32 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: C:\Users\damia\Desktop\gpu exparment for lean coq isabell andf star — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: phase1_formal_gpu/lean/GpuMemory.lean — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: phase1_formal_gpu/lean/Trinary.lean — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: results/phase0/gpu_probe.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/results/phase0/gpu_probe.json
  - **dataset**: GitHub OSS corpus parity/golden.json — https://github.com/parity/golden.json

### Federal_Science_Registry_Panel

- Benchmark: `data/federal_science_registry_panel_benchmark.json` · records=24 · median%=0.013294
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.FederalScienceRegistryPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### Finance_Markets

- Benchmark: `data/finance_markets_extension_benchmark.json` · records=150 · median%=0.025840180827433133
- Lean: `FSOT.Formal.FinanceMarketsExtensionPriors`
- Public / portable anchors:
  - **unresolved**: finance_markets_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: econometrics — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: finance_markets_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: economics_yoy_bridge — Named in panel source; add explicit public URL if this is an external authority

### Finance_Markets_Panel

- Benchmark: `data/finance_markets_panel_benchmark.json` · records=36 · median%=0.02584
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.FinanceMarketsPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Fluid_Dynamics

- Benchmark: `data/fluid_dynamics_gap_fill_benchmark.json` · records=55 · median%=0.0
- Public / portable anchors:
  - **unresolved**: airfoil_rmse — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: FLUID_MECHANICS_rules — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_generator_fluid_mechanics — Named in panel source; add explicit public URL if this is an external authority

### Fluid_Phase_Current_Spine

- Benchmark: `data/fluid_phase_current_spine_benchmark.json` · records=24 · median%=3.8622500000000005e-05
- Lean: `FSOT.Formal.FluidPhaseCurrentSpinePriors`
- Public / portable anchors:
  - **vendor_cache**: time_emergence_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_simulation_benchmark.json
  - **vendor_cache**: time_domain_crosswalk_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_domain_crosswalk_benchmark.json
  - **vendor_cache**: fpc_temporal_coupling_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fpc_temporal_coupling_benchmark.json
  - **vendor_cache**: reality_folding_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/reality_folding_spine_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: Time_Emergence_Simulation — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Time_Domain_Crosswalk — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: FPC_Temporal_Coupling — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fluid_phase_current_spine — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Fluid_Spacetime_Observable_Spine

- Benchmark: `data/fluid_spacetime_observable_spine_benchmark.json` · records=29 · median%=0.0111155
- Lean: `FSOT.Formal.FluidSpacetimeObservableSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fluid_phase_current_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fluid_phase_current_spine_benchmark.json
  - **vendor_cache**: stumped_observables_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_spine_benchmark.json

### Fluid_Spacetime_Prereg_Validation_Panel

- Benchmark: `data/fluid_spacetime_prereg_validation_panel_benchmark.json` · records=20 · median%=0.0
- Lean: `FSOT.Formal.FluidSpacetimePreregValidationPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: preregistered_predictions_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_manifest.yaml
  - **vendor_cache**: hubble_dark_sector_crosswalk_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/hubble_dark_sector_crosswalk_benchmark.json
  - **vendor_cache**: fpc_fluidlink_timing_deep_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fpc_fluidlink_timing_deep_panel_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Fold_Depth_Metrics

- Benchmark: `data/fold_depth_metrics_benchmark.json` · records=51 · median%=0.025753835305195434
- Lean: `FSOT.Formal.FoldDepthMetricsPriors`
- Public / portable anchors:
  - **vendor_cache**: compactification_ladder_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_manifest.yaml
  - **vendor_cache**: fsot_formula_spine.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_formula_spine.yaml

### Food_Microbiology

- Benchmark: `data/food_microbiology_gap_fill_benchmark.json` · records=30 · median%=0.04447250077037743
- Lean: `FSOT.Formal.FoodMicrobiologyGapFillPriors`
- Public / portable anchors:
  - **unresolved**: fermentation_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: culinary_arts — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: culinary_process_bridge — Named in panel source; add explicit public URL if this is an external authority

### Formula_Branching_Fractal

- Benchmark: `data/formula_branching_fractal_benchmark.json` · records=380 · median%=0.038016537604979236
- Lean: `FSOT.Formal.FormulaBranchingFractalPriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_formula_spine.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_formula_spine.yaml
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: term1.quirkMod — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term3.chaos_factor — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term1.growth_term — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term3.acoustic_bleed — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term1.term1_base — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term3.acoustic_inflow — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term1.coherence_efficiency — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term1.perceived_adjust — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: scaled_S — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: raw_S — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term2.scale — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term2.amplitude — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: term2.trend_bias — Named in panel source; add explicit public URL if this is an external authority

### Formula_Corpus_CNC

- Benchmark: `data/formula_corpus_cnc_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.FormulaCorpusCncPriors`
- Public / portable anchors:
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Formula_Corpus_Closure

- Benchmark: `data/formula_corpus_closure_benchmark.json` · records=203 · median%=0.009504
- Lean: `FSOT.Formal.FormulaCorpusClosurePriors`
- Public / portable anchors:
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: extension_benchmarks — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: lean_priors — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: FSOT/Formal/*Priors.lean — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: data/*_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/*_benchmark.json
  - **vendor_cache**: acoustic_resonance_materials_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/acoustic_resonance_materials_benchmark.json
  - **vendor_cache**: actuarial_science_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/actuarial_science_panel_benchmark.json
  - **vendor_cache**: adjacent_rung_coupling_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/adjacent_rung_coupling_benchmark.json
  - **vendor_cache**: adversarial_fractal_break_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/adversarial_fractal_break_benchmark.json
  - **vendor_cache**: agriculture_agroecology_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/agriculture_agroecology_gap_fill_benchmark.json
  - **vendor_cache**: ai_galactic_orbital_bridge_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/ai_galactic_orbital_bridge_benchmark.json
  - **vendor_cache**: alternate_base_mathematics_explorer_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/alternate_base_mathematics_explorer_panel_benchmark.json
  - **vendor_cache**: alternate_base_mathematics_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/alternate_base_mathematics_spine_benchmark.json
  - **vendor_cache**: anthropology_extension_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/anthropology_extension_benchmark.json
  - **vendor_cache**: architecture_building_science_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/architecture_building_science_gap_fill_benchmark.json
  - **vendor_cache**: arxiv_brain_knowledge_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_brain_knowledge_panel_benchmark.json
  - **vendor_cache**: arxiv_gravitational_waves_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_gravitational_waves_panel_benchmark.json
  - **vendor_cache**: arxiv_primitives_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_primitives_panel_benchmark.json
  - **vendor_cache**: arxiv_primitives_v14_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/arxiv_primitives_v14_benchmark.json
  - **vendor_cache**: astrophysical_structure_crosswalk_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/astrophysical_structure_crosswalk_benchmark.json
  - **vendor_cache**: atmospheric_physics_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/atmospheric_physics_gap_fill_benchmark.json
  - **vendor_cache**: atomic_physics_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/atomic_physics_gap_fill_benchmark.json
  - **vendor_cache**: bibliography_corpus_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/bibliography_corpus_panel_benchmark.json
  - **vendor_cache**: bibliography_lean_corpus_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/bibliography_lean_corpus_benchmark.json
  - … +18 more in JSON

### Formula_Precision_Spine

- Benchmark: `data/formula_precision_spine_benchmark.json` · records=26 · median%=0.0
- Lean: `FSOT.Formal.FormulaPrecisionSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier67_formula_precision_panels — Named in panel source; add explicit public URL if this is an external authority

### Foundational_Ontology_Spine

- Benchmark: `data/foundational_ontology_spine_benchmark.json` · records=60 · median%=0.009504
- Lean: `FSOT.Formal.FoundationalOntologySpinePriors`
- Public / portable anchors:
  - **unresolved**: tier91_foundational_ontology_panels — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\data\foundational_ontology_axioms.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/foundational_ontology_axioms.yaml

### Founding_Atmospheric_Ozone_Panel

- Benchmark: `data/founding_atmospheric_ozone_panel_benchmark.json` · records=5 · median%=0.023822
- Lean: `FSOT.Formal.FoundingAtmosphericOzonePanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_26 — Named in panel source; add explicit public URL if this is an external authority

### Founding_Cosmic_Dust_Panel

- Benchmark: `data/founding_cosmic_dust_panel_benchmark.json` · records=5 · median%=0.044121
- Lean: `FSOT.Formal.FoundingCosmicDustPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_20 — Named in panel source; add explicit public URL if this is an external authority

### Founding_Cosmic_Ray_Panel

- Benchmark: `data/founding_cosmic_ray_panel_benchmark.json` · records=5 · median%=0.021221
- Lean: `FSOT.Formal.FoundingCosmicRayPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_12 — Named in panel source; add explicit public URL if this is an external authority

### Founding_Galactic_Halo_Rotation_Panel

- Benchmark: `data/founding_galactic_halo_rotation_panel_benchmark.json` · records=5 · median%=0.025123
- Lean: `FSOT.Formal.FoundingGalacticHaloRotationPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_13 — Named in panel source; add explicit public URL if this is an external authority

### Founding_Pulsar_Glitch_Panel

- Benchmark: `data/founding_pulsar_glitch_panel_benchmark.json` · records=5 · median%=0.044923
- Lean: `FSOT.Formal.FoundingPulsarGlitchPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_34 — Named in panel source; add explicit public URL if this is an external authority

### Founding_Quantum_Vacuum_Panel

- Benchmark: `data/founding_quantum_vacuum_panel_benchmark.json` · records=5 · median%=0.047775
- Lean: `FSOT.Formal.FoundingQuantumVacuumPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_11 — Named in panel source; add explicit public URL if this is an external authority

### Founding_White_Dwarf_Cooling_Panel

- Benchmark: `data/founding_white_dwarf_cooling_panel_benchmark.json` · records=5 · median%=0.044923
- Lean: `FSOT.Formal.FoundingWhiteDwarfCoolingPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/founding_unmapped_laws_reference.json — https://github.com/data/founding_unmapped_laws_reference.json
  - **unresolved**: founding_law:law_23 — Named in panel source; add explicit public URL if this is an external authority

### Fractal_Constant_Recursion

- Benchmark: `data/fractal_constant_recursion_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.FractalConstantRecursionPriors`
- Public / portable anchors:
  - **vendor_cache**: fractal_constant_recursion.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fractal_constant_recursion.yaml
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Fuel_Candidate_Prereg_Scaffold

- Benchmark: `data/fuel_candidate_prereg_scaffold_benchmark.json` · records=33 · median%=0.0
- Lean: `FSOT.Formal.FuelCandidatePreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: tier65_prereg_channels_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier65_prereg_channels_manifest.yaml

### Fuel_Lab_Live_Panel

- Benchmark: `data/fuel_lab_live_panel_benchmark.json` · records=366 · median%=0.039349
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.FuelLabLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\fuel_lab_live_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/fuel_lab_live_cache.json
  - **unresolved**: desktop_fuel_lab_engine_simulator — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: compare_full_20260526.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compare_full_20260526.json
  - **vendor_cache**: compare_optimax_wave_20260715.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compare_optimax_wave_20260715.json
  - **vendor_cache**: material_compatibility_comparison.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/material_compatibility_comparison.json
  - **vendor_cache**: refined_grounded_hemp.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/refined_grounded_hemp.json
  - **unresolved**: I:\FSOT-Physical-Archive\08_Verified-Desktop-Projects\fuel_lab\engine_simulator\REAL_DATA_PROVENANCE.md — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Fuel_Thermochemistry_Public_Anchors

- Benchmark: `data/fuel_thermochemistry_public_anchors_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.FuelThermochemistryPublicAnchorsPriors`
- Public / portable anchors:
  - **vendor_cache**: thermochemistry_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/thermochemistry_public_anchors.json
  - **vendor_cache**: public_fuel_property_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/public_fuel_property_catalog.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Fusion_Decay_Chain_Prereg_Scaffold

- Benchmark: `data/fusion_decay_chain_prereg_scaffold_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.FusionDecayChainPreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: cold_fusion_lab_synthesis_crosswalk_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cold_fusion_lab_synthesis_crosswalk_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Fusion_Lab_Certificate_Spine

- Benchmark: `data/fusion_lab_certificate_spine_benchmark.json` · records=50 · median%=0.0
- Lean: `FSOT.Formal.FusionLabCertificateSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json
  - **vendor_cache**: fuel_thermochemistry_public_anchors_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fuel_thermochemistry_public_anchors_benchmark.json

### Fusion_Lean_Route_Credibility

- Benchmark: `data/fusion_lean_route_credibility_benchmark.json` · records=81 · median%=0.009504
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:fusion — Named in panel source; add explicit public URL if this is an external authority

### Fusion_Physics_Public_Panel

- Benchmark: `data/fusion_physics_public_panel_benchmark.json` · records=24 · median%=9.5e-05
- Lean: `FSOT.Formal.FusionPhysicsPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### GBIF_Species_Occurrence

- Benchmark: `data/gbif_species_occurrence_benchmark.json` · records=240 · median%=0.006006
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.GbifSpeciesOccurrencePriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### GWOSC_Live_Event_Deep

- Benchmark: `data/gwosc_live_event_deep_benchmark.json` · records=185 · median%=0.008488
- Ingest: `scripts/ingest_tier58_live_catalogs.py`
- Lean: `FSOT.Formal.GWOSCLiveEventDeepPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **ingest_script**: scripts/ingest_tier58_live_catalogs.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier58_live_catalogs.py

### Gaia_Astrometry_Panel_Deep

- Benchmark: `data/gaia_astrometry_panel_deep_benchmark.json` · records=62 · median%=0.022461
- Lean: `FSOT.Formal.GaiaAstrometryPanelDeepPriors`
- Public / portable anchors:
  - **vendor_cache**: galactic_structure_sample.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/galactic_structure_sample.json
  - **vendor_cache**: galactic_structure_sample_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/galactic_structure_sample_benchmark.json

### Gaia_DR3_TAP_Deep

- Benchmark: `data/gaia_dr3_tap_deep_benchmark.json` · records=1826 · median%=0.022461
- Ingest: `scripts/ingest_tier62_live_astrometry.py`
- Lean: `FSOT.Formal.GaiaDR3TAPDeepPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **ingest_script**: scripts/ingest_tier62_live_astrometry.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier62_live_astrometry.py

### Galactic_Structure_Sample

- Benchmark: `data/galactic_structure_sample_benchmark.json` · records=101 · median%=0.0
- Lean: `FSOT.Formal.GalacticStructureSamplePriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/stellar_structures/galactic_structure_sample.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/galactic_structure_sample.json
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/

### Genomic_Sciences

- Benchmark: `data/genomic_sciences_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.GenomicSciencesPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Geology_Stratigraphy

- Benchmark: `data/geology_stratigraphy_extension_benchmark.json` · records=1957 · median%=0.0
- Lean: `FSOT.Formal.GeologyStratigraphyExtensionPriors`
- Public / portable anchors:
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **unresolved**: PB2002_tectonics — Named in panel source; add explicit public URL if this is an external authority
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **unresolved**: seismology — Named in panel source; add explicit public URL if this is an external authority

### Government_Open_Data_Spine

- Benchmark: `data/government_open_data_spine_benchmark.json` · records=28 · median%=0.0
- Lean: `FSOT.Formal.GovernmentOpenDataSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier80_government_open_data_panels — Named in panel source; add explicit public URL if this is an external authority

### H0_Planck_CMB_Sector

- Benchmark: `data/h0_planck_benchmark.json` · records=20 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/math_generator/benchmark_reports/hubble_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports/hubble_report.json
  - **dataset**: GitHub OSS corpus scripts/math_generator_benchmark_formula_eval.py — https://github.com/scripts/math_generator_benchmark_formula_eval.py

### HVAC_Thermal_Systems

- Benchmark: `data/hvac_thermal_systems_benchmark.json` · records=23 · median%=0.000561846
- Ingest: `scripts/ingest_tier39_propulsion_electrical.py`
- Lean: `FSOT.Formal.HvacThermalSystemsPriors`
- Public / portable anchors:
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: SH0ES / local distance ladder H0 (Riess et al. series) — https://ui.adsabs.harvard.edu/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - … +6 more in JSON

### Heavy_Ion_Lab_Synthesis_Panel

- Benchmark: `data/heavy_ion_lab_synthesis_panel_benchmark.json` · records=39 · median%=9.5e-05
- Lean: `FSOT.Formal.HeavyIonLabSynthesisPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_physics_public_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_physics_public_panel_benchmark.json

### Higgs_Branching

- Benchmark: `data/higgs_branching_benchmark.json` · records=27 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: thesis_wave — Named in panel source; add explicit public URL if this is an external authority

### History

- Benchmark: `data/history_extension_benchmark.json` · records=170 · median%=0.019504399572477397
- Lean: `FSOT.Formal.HistoryExtensionPriors`
- Public / portable anchors:
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **unresolved**: anthropology_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/

### History_Panel

- Benchmark: `data/history_panel_benchmark.json` · records=60 · median%=0.01382
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.HistoryPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: Crossref history corpus — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Hubble_Bubble_Tension

- Benchmark: `data/hubble_bubble_tension_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.HubbleBubbleTensionPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/sector_h0_seed.json — https://github.com/data/sector_h0_seed.json
  - **dataset**: GitHub OSS corpus scripts/build_cosmology_bubble_bleed_benchmark.py — https://github.com/scripts/build_cosmology_bubble_bleed_benchmark.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Hubble_Dark_Sector_Crosswalk

- Benchmark: `data/hubble_dark_sector_crosswalk_benchmark.json` · records=32 · median%=0.004252889935064887
- Lean: `FSOT.Formal.HubbleDarkSectorCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fluid_spacetime\cosmology_anomaly_deep_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fluid_spacetime/cosmology_anomaly_deep_anchors.json
  - **vendor_cache**: hubble_bubble_tension_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/hubble_bubble_tension_benchmark.json
  - **vendor_cache**: dark_sector_open_problems_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/dark_sector_open_problems_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Hybrid_FI_Sim_Multi_Hero_Panel

- Benchmark: `data/hybrid_fi_sim_multi_hero_panel_benchmark.json` · records=32 · median%=0.0
- Lean: `FSOT.Formal.HybridFiSimMultiHeroPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: multi_hero_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/multi_hero_benchmark.json
  - **vendor_cache**: vendor/neuron_cohort/inconsistency_rerun_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/neuron_cohort/inconsistency_rerun_report.json

### Hybrid_FI_Sim_Stratum_Deep_Panel

- Benchmark: `data/hybrid_fi_sim_stratum_deep_panel_benchmark.json` · records=24 · median%=0.015311
- Ingest: `scripts/ingest_tier86_scientific_expansion.py`
- Lean: `FSOT.Formal.HybridFiSimStratumDeepPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: neuron_cohort_per_stratum — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier86_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier86_scientific_expansion.py

### IGEM_Parts_Expanded

- Benchmark: `data/igem_parts_expanded_benchmark.json` · records=111 · median%=5.9357506661387664e-05
- Lean: `FSOT.Formal.IGEMPartsExpandedPriors`
- Public / portable anchors:
  - **vendor_cache**: igem_synthetic_biology_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/igem_synthetic_biology_benchmark.json
  - **vendor_cache**: igem_live_fasta_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/igem_live_fasta_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **api**: NCBI E-utilities / Gene / datasets — https://www.ncbi.nlm.nih.gov/books/NBK25501/

### Immunology_Panel

- Benchmark: `data/immunology_panel_benchmark.json` · records=24 · median%=0.040788
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.ImmunologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Inertial_Confinement_Fusion_Panel

- Benchmark: `data/inertial_confinement_fusion_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.InertialConfinementFusionPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Information_Theory_Public_Panel

- Benchmark: `data/information_theory_public_panel_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.InformationTheoryPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Initiation_Transformation_Archetype

- Benchmark: `data/initiation_transformation_archetype_benchmark.json` · records=23 · median%=0.0
- Lean: `FSOT.Formal.InitiationTransformationArchetypePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: symbolic_archetype_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/symbolic_archetype_panel_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### Interactive_Media_Prereg_Scaffold

- Benchmark: `data/interactive_media_prereg_scaffold_benchmark.json` · records=42 · median%=0.0
- Lean: `FSOT.Formal.InteractiveMediaPreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: tier65_prereg_channels_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier65_prereg_channels_manifest.yaml

### Interdisciplinary_Spine_Crosswalk

- Benchmark: `data/interdisciplinary_spine_crosswalk_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.InterdisciplinarySpineCrosswalkPriors`
- Public / portable anchors:
  - **unresolved**: tier52-56_panels — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Intrinsic_LLM_Validators

- Benchmark: `data/intrinsic_llm_validators_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.IntrinsicLLMValidatorsPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/intrinsic_llm/benchmark_results_final.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/intrinsic_llm/benchmark_results_final.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Intrinsic_LLM_Validators_Panel

- Benchmark: `data/validators_intrinsic_llm_panel_benchmark.json` · records=21 · median%=0.014767
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.IntrinsicLlmValidatorsPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\validators_intrinsic_llm_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/validators_intrinsic_llm_cache.json
  - **unresolved**: desktop_intrinsic_llm — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Ionospheric_Chemistry_Coupling

- Benchmark: `data/ionospheric_chemistry_coupling_benchmark.json` · records=85 · median%=0.0
- Lean: `FSOT.Formal.IonosphericChemistryCouplingPriors`
- Public / portable anchors:
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json
  - **vendor_cache**: geomagnetism_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/geomagnetism_benchmark.json
  - **vendor_cache**: magnetosphere_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/magnetosphere_benchmark.json
  - **vendor_cache**: space_weather_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/space_weather_benchmark.json
  - **vendor_cache**: magnetosphere_extended_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/magnetosphere_extended_benchmark.json

### Island_Of_Stability_Deep_Panel

- Benchmark: `data/island_of_stability_deep_panel_benchmark.json` · records=23 · median%=1e-06
- Lean: `FSOT.Formal.IslandOfStabilityDeepPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### Knowledge_Base_Portable_Bundle_Panel

- Benchmark: `data/knowledge_base_portable_bundle_panel_benchmark.json` · records=23 · median%=0.0
- Lean: `FSOT.Formal.KnowledgeBasePortableBundlePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: knowledge_base_formula_verification_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/knowledge_base_formula_verification_summary.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Lab_Synthesis_Metamaterial_Spine

- Benchmark: `data/lab_synthesis_metamaterial_spine_benchmark.json` · records=43 · median%=9.5e-05
- Lean: `FSOT.Formal.LabSynthesisMetamaterialSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_lab_certificate_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_lab_certificate_spine_benchmark.json
  - **vendor_cache**: periodic_table_completion_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/periodic_table_completion_spine_benchmark.json

### Law_Policy

- Benchmark: `data/law_policy_extension_benchmark.json` · records=180 · median%=0.019504399572479934
- Lean: `FSOT.Formal.LawPolicyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: law_policy_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: law_policy_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/

### Law_Policy_Panel

- Benchmark: `data/law_policy_panel_benchmark.json` · records=20 · median%=0.013003
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.LawPolicyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Limnology_Panel

- Benchmark: `data/limnology_panel_benchmark.json` · records=2010 · median%=0.030173
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.LimnologyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Linguistics_Formal

- Benchmark: `data/linguistics_formal_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.LinguisticsFormalPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Live_Ingest_Spine

- Benchmark: `data/live_ingest_spine_benchmark.json` · records=28 · median%=0.0
- Lean: `FSOT.Formal.LiveIngestSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier68_live_ingest_panels — Named in panel source; add explicit public URL if this is an external authority

### Living_FSOT_Hardware

- Benchmark: `data/living_fsot_hardware_benchmark.json` · records=4 · median%=None
- Public / portable anchors:
  - **vendor_cache**: data\living_fsot_hardware_verification_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/living_fsot_hardware_verification_report.json

### Living_FSOT_Hardware_Panel

- Benchmark: `data/living_fsot_hardware_panel_benchmark.json` · records=152 · median%=0.014767
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.LivingFsotHardwarePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\living_fsot_hardware_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/living_fsot_hardware_cache.json
  - **unresolved**: desktop_living_fsot — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Longevity_AnAge_Catalog_Panel

- Benchmark: `data/longevity_anage_catalog_panel_benchmark.json` · records=966 · median%=0.022236
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityAnAgeCatalogPanelPriors`
- Public / portable anchors:
  - **api**: anage — https://genomics.senescence.info/species/dataset.zip
  - **vendor_cache**: I:\FSOT-Physical-Archive\04_Genetics-Longevity\tier94_anage_longevity_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/04_Genetics-Longevity/tier94_anage_longevity_catalog.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### Longevity_Consciousness_Coupling_Panel

- Benchmark: `data/longevity_consciousness_coupling_panel_benchmark.json` · records=890 · median%=0.022424
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityConsciousnessCouplingPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier94_megadeep_extreme_ncbi_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_megadeep_extreme_ncbi_cache.json
  - **vendor_cache**: tier93_consciousness_genetics_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_consciousness_genetics_cache.json
  - **vendor_cache**: consciousness_reference_observables.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/consciousness_reference_observables.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### Longevity_Extreme_Species_Panel

- Benchmark: `data/longevity_extreme_species_panel_benchmark.json` · records=164 · median%=0.017789
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityExtremeSpeciesPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier94_extreme_species_ncbi_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_extreme_species_ncbi_cache.json
  - **vendor_cache**: tier93_consciousness_genetics_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier93_consciousness_genetics_cache.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### Longevity_Genetic_Mechanics_Panel

- Benchmark: `data/longevity_genetic_mechanics_panel_benchmark.json` · records=35 · median%=0.022236
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityGeneticMechanicsPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier94_anage_longevity_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_anage_longevity_catalog.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### Longevity_MegaDeep_NCBI_Panel

- Benchmark: `data/longevity_megadeep_ncbi_panel_benchmark.json` · records=1746 · median%=0.017789
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityMegaDeepNcbiPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier94_megadeep_extreme_ncbi_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_megadeep_extreme_ncbi_cache.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### Longevity_Telomere_Repair_Panel

- Benchmark: `data/longevity_telomere_repair_panel_benchmark.json` · records=60 · median%=0.022236
- Ingest: `scripts/ingest_tier94_longevity_genetics.py`
- Lean: `FSOT.Formal.LongevityTelomereRepairPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: longevity_telomere_repair_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/longevity_telomere_repair_anchors.json
  - **vendor_cache**: tier94_telomere_repair_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier94_telomere_repair_cache.json
  - **ingest_script**: scripts/ingest_tier94_longevity_genetics.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier94_longevity_genetics.py

### MPCORB_Minor_Planet_Catalog

- Benchmark: `data/mpcorb_fsot_benchmark.json` · records=1554101 · median%=0.023015
- Ingest: `scripts/ingest_mpcorb_catalog.py`
- Lean: `FSOT.Formal.MpcorbMinorPlanetCatalogPriors`
- Public / portable anchors:
  - **ingest_script**: scripts/ingest_mpcorb_catalog.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_mpcorb_catalog.py

### Machine_And_Molecule_Live_Panel

- Benchmark: `data/machine_and_molecule_live_panel_benchmark.json` · records=120 · median%=0.01341
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.MachineAndMoleculeLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\machine_and_molecule_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/machine_and_molecule_cache.json
  - **unresolved**: desktop_machine_and_molecule_species_catalog — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Magnetic_Confinement_Fusion_Panel

- Benchmark: `data/magnetic_confinement_fusion_panel_benchmark.json` · records=22 · median%=0.0
- Lean: `FSOT.Formal.MagneticConfinementFusionPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: plasma_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/plasma_physics_benchmark.json

### Magnetosphere_Extended

- Benchmark: `data/magnetosphere_extended_benchmark.json` · records=24 · median%=3.8622500000000005e-05
- Ingest: `scripts/ingest_kyoto_dst_historical.py`
- Lean: `FSOT.Formal.MagnetosphereExtendedPriors`
- Public / portable anchors:
  - **dataset**: Planck Collaboration cosmological parameters — https://www.cosmos.esa.int/web/planck
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **api**: JPL Horizons system — https://ssd.jpl.nasa.gov/horizons/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **ingest_script**: scripts/ingest_kyoto_dst_historical.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_kyoto_dst_historical.py

### Maillard_Chemistry

- Benchmark: `data/maillard_chemistry_gap_fill_benchmark.json` · records=30 · median%=0.09443694019339477
- Lean: `FSOT.Formal.MaillardChemistryGapFillPriors`
- Public / portable anchors:
  - **unresolved**: culinary_arts — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: SMILES_activation — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: smiles_food_chemistry — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: recipe_process — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: coffee_roast — Named in panel source; add explicit public URL if this is an external authority
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **unresolved**: fermentation_browning_bridge — Named in panel source; add explicit public URL if this is an external authority

### Malware_Threat_Intelligence

- Benchmark: `data/malware_threat_intelligence_cybersecurity_benchmark.json` · records=85 · median%=0.04593318440797134
- Lean: `FSOT.Formal.MalwareThreatIntelligencePriors`
- Public / portable anchors:
  - **unresolved**: malware_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: virology_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: immunology_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: malware_threat_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: virology_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Marine_Biology

- Benchmark: `data/marine_biology_extension_benchmark.json` · records=540 · median%=0.022236250385192644
- Ingest: `scripts/build_tier_f_extension_benchmarks.py`
- Lean: `FSOT.Formal.MarineBiologyExtensionPriors`
- Public / portable anchors:
  - **api**: obis — https://api.obis.org/v3/occurrence
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **api**: obis — https://api.obis.org/v3/occurrence
  - **api**: obis — https://api.obis.org/v3/occurrence
  - **ingest_script**: scripts/build_tier_f_extension_benchmarks.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/build_tier_f_extension_benchmarks.py

### Marine_Biology_Panel

- Benchmark: `data/marine_biology_panel_benchmark.json` · records=90 · median%=0.006006
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.MarineBiologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: obis — https://api.obis.org/v3/occurrence
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Material_In_Silico_Screening_Scaffold

- Benchmark: `data/material_in_silico_screening_scaffold_benchmark.json` · records=42 · median%=0.0
- Lean: `FSOT.Formal.MaterialInSilicoScreeningScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: tier65_prereg_channels_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier65_prereg_channels_manifest.yaml

### Material_Property_Verification_Scaffold

- Benchmark: `data/material_property_verification_scaffold_benchmark.json` · records=79 · median%=0.00206
- Lean: `FSOT.Formal.MaterialPropertyVerificationScaffoldPriors`
- Public / portable anchors:
  - **unresolved**: tier55-57_material_panels — Named in panel source; add explicit public URL if this is an external authority

### Materials_Creep_Fracture_Depth_Panel

- Benchmark: `data/materials_creep_fracture_depth_panel_benchmark.json` · records=47 · median%=0.01341
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.MaterialsCreepFractureDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\materials_creep_fracture_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/materials_creep_fracture_cache.json
  - **unresolved**: creep_fracture_materials_literature_anchors+materials_project — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Materials_Genome_Crosswalk

- Benchmark: `data/materials_genome_crosswalk_benchmark.json` · records=38 · median%=0.0
- Lean: `FSOT.Formal.MaterialsGenomeCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: materials_engineering_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/materials_engineering_benchmark.json
  - **vendor_cache**: quantum_materials_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/quantum_materials_benchmark.json
  - **vendor_cache**: materials_species_bridge_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/materials_species_bridge_benchmark.json

### Materials_Project_Live_Panel

- Benchmark: `data/materials_project_live_panel_benchmark.json` · records=141 · median%=0.011734
- Ingest: `scripts/ingest_tier68_live_ingest.py`
- Lean: `FSOT.Formal.MaterialsProjectLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\materials_project_live_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/materials_project_live_cache.json
  - **vendor_cache**: vendor/materials_live/materials_project_bundled.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/materials_live/materials_project_bundled.json
  - **ingest_script**: scripts/ingest_tier68_live_ingest.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier68_live_ingest.py

### Materials_Species_Bridge_Live_Panel

- Benchmark: `data/materials_species_bridge_live_panel_benchmark.json` · records=150 · median%=0.01341
- Ingest: `scripts/ingest_tier86_scientific_expansion.py`
- Lean: `FSOT.Formal.MaterialsSpeciesBridgeLivePanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: species_catalog — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: SMILES_lab — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier86_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier86_scientific_expansion.py

### Math_Generator_Airfoil_RMSE

- Benchmark: `data/math_generator_airfoil_rmse_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.MathGeneratorAirfoilRmsePriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/math_generator/datasets/airfoil_self_noise.csv — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/datasets/airfoil_self_noise.csv
  - **vendor_cache**: vendor/math_generator/benchmark_reports/airfoil_three_seed_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports/airfoil_three_seed_report.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Math_Generator_Benchmark_Formula_Eval

- Benchmark: `data/math_generator_benchmark_formula_eval_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.MathGeneratorBenchmarkFormulaEvalPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/math_generator/rules — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/rules
  - **vendor_cache**: vendor/math_generator/benchmark_reports — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Mechanical_Engineering

- Benchmark: `data/mechanical_engineering_extension_benchmark.json` · records=50 · median%=0.017310023021640548
- Lean: `FSOT.Formal.MechanicalEngineeringExtensionPriors`
- Public / portable anchors:
  - **unresolved**: mechanical_engineering_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: materials_engineering — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: THERMODYNAMICS_ENGINEERING_rules — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: mechanical_engineering_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_generator_mech — Named in panel source; add explicit public URL if this is an external authority

### Mechanical_Engineering_Panel

- Benchmark: `data/mechanical_engineering_panel_benchmark.json` · records=20 · median%=0.039349
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.MechanicalEngineeringPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\scientific_expansion\tier85_cache\mechanical_engineering_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/scientific_expansion/tier85_cache/mechanical_engineering_cache.json
  - **unresolved**: ASME mechanical engineering reference — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Mechanistic_Coupling

- Benchmark: `data/mechanistic_coupling_benchmark.json` · records=39 · median%=0.0073836551816993294
- Lean: `FSOT.Formal.MechanisticCouplingPriors`
- Public / portable anchors:
  - **vendor_cache**: mechanistic_coupling_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/mechanistic_coupling_manifest.yaml
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json

### Medical_Galactic_Orbital_Bridge

- Benchmark: `data/medical_galactic_orbital_bridge_benchmark.json` · records=48 · median%=0.010717743028516056
- Lean: `FSOT.Formal.MedicalGalacticOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/adjacent_rung_coupling_benchmark.json — https://github.com/data/adjacent_rung_coupling_benchmark.json
  - **dataset**: GitHub OSS corpus data/adversarial_fractal_break_benchmark.json — https://github.com/data/adversarial_fractal_break_benchmark.json
  - **dataset**: GitHub OSS corpus data/biological_cuda_physarum_benchmark.json — https://github.com/data/biological_cuda_physarum_benchmark.json
  - **dataset**: GitHub OSS corpus data/biology_developmental_structural_depth_panel_benchmark.json — https://github.com/data/biology_developmental_structural_depth_panel_benchmark.json
  - **unresolved**: cross_scale_motif — Named in panel source; add explicit public URL if this is an external authority

### Metamaterial_Fluid_Design_Prereg_Scaffold

- Benchmark: `data/metamaterial_fluid_design_prereg_scaffold_benchmark.json` · records=25 · median%=0.0
- Lean: `FSOT.Formal.MetamaterialFluidDesignPreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: term3_acoustic_bleed_depth_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/term3_acoustic_bleed_depth_benchmark.json

### Meteorology

- Benchmark: `data/meteorology_gap_fill_benchmark.json` · records=47 · median%=0.0
- Public / portable anchors:
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/

### Microtubule_Quantum_Consciousness_Panel

- Benchmark: `data/microtubule_quantum_consciousness_panel_benchmark.json` · records=21 · median%=0.0094425
- Ingest: `scripts/ingest_tier90_consciousness_expansion.py`
- Lean: `FSOT.Formal.MicrotubuleQuantumConsciousnessPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: G:\FSOT-PublicData\anomaly_observables\consciousness\tier90_microtubule_observer_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_microtubule_observer_cache.json
  - **dataset**: GitHub OSS corpus data/consciousness_econ_benchmark.json — https://github.com/data/consciousness_econ_benchmark.json
  - **dataset**: GitHub OSS corpus data/quantum_computing_math_depth_panel_benchmark.json — https://github.com/data/quantum_computing_math_depth_panel_benchmark.json
  - **dataset**: GitHub OSS corpus data/observer_channel_derivation_benchmark.json — https://github.com/data/observer_channel_derivation_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: GitHub OSS corpus data/canonical_constants.json — https://github.com/data/canonical_constants.json
  - **ingest_script**: scripts/ingest_tier90_consciousness_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier90_consciousness_expansion.py

### Music_Harmonics_Public_Panel

- Benchmark: `data/music_harmonics_public_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.MusicHarmonicsPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: acoustic_resonance_materials_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/acoustic_resonance_materials_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Mycology

- Benchmark: `data/mycology_extension_benchmark.json` · records=420 · median%=0.022236250385193498
- Ingest: `scripts/build_tier_f_extension_benchmarks.py`
- Lean: `FSOT.Formal.MycologyExtensionPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **unresolved**: food_microbiology_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **unresolved**: fermentation_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: culinary_process_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/build_tier_f_extension_benchmarks.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/build_tier_f_extension_benchmarks.py

### Mycology_Panel

- Benchmark: `data/mycology_panel_benchmark.json` · records=90 · median%=0.006006
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.MycologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### NASA_DONKI_Solar_Panel

- Benchmark: `data/nasa_donki_solar_panel_benchmark.json` · records=2148 · median%=0.020755
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.NasaDonkiSolarPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### NASA_Exoplanet_Archive

- Benchmark: `data/nasa_exoplanet_archive_benchmark.json` · records=158 · median%=0.023015
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.NasaExoplanetArchivePriors`
- Public / portable anchors:
  - **api**: NASA Exoplanet Archive TAP — https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### NASA_NEO_Feed_Panel

- Benchmark: `data/nasa_neo_feed_panel_benchmark.json` · records=56 · median%=0.021097
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.NasaNeoFeedPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### NCBI_Gene_Public_Panel

- Benchmark: `data/ncbi_gene_public_panel_benchmark.json` · records=48 · median%=0.025571999999999998
- Ingest: `scripts/ingest_tier81_public_verifiable.py`
- Lean: `FSOT.Formal.NcbiGenePublicPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: NCBI E-utilities / Gene / datasets — https://www.ncbi.nlm.nih.gov/books/NBK25501/
  - **ingest_script**: scripts/ingest_tier81_public_verifiable.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier81_public_verifiable.py

### NIST_CODATA_Constants

- Benchmark: `data/nist_codata_constants_benchmark.json` · records=6 · median%=0.0
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.NistCodataConstantsPriors`
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### NIST_DLMF_Special_Functions

- Benchmark: `data/nist_dlmf_special_functions_benchmark.json` · records=5 · median%=0.001661
- Lean: `FSOT.Formal.NistDlmfSpecialFunctionsPriors`
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### NOAA_Coastal_Tides

- Benchmark: `data/noaa_coastal_tides_benchmark.json` · records=20 · median%=0.030173
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.NoaaCoastalTidesPriors`
- Public / portable anchors:
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### NOAA_NDBC_Buoy_Panel

- Benchmark: `data/noaa_ndbc_buoy_panel_benchmark.json` · records=596 · median%=0.028287
- Ingest: `scripts/ingest_tier81_public_verifiable.py`
- Lean: `FSOT.Formal.NoaaNdbcBuoyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **ingest_script**: scripts/ingest_tier81_public_verifiable.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier81_public_verifiable.py

### Natural_Formation_Element_Simulation

- Benchmark: `data/natural_formation_element_simulation_benchmark.json` · records=32 · median%=0.0
- Lean: `FSOT.Formal.NaturalFormationElementSimulationPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_physics_public_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_physics_public_panel_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Network_Internet_Protocols

- Benchmark: `data/network_internet_protocols_cybersecurity_benchmark.json` · records=22 · median%=0.010337117254355377
- Lean: `FSOT.Formal.NetworkInternetProtocolsPriors`
- Public / portable anchors:
  - **unresolved**: RFC_IANA_anchors — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: MITRE_ATT&CK_shape — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: robotics_control_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: network_internet_protocols_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Network_Science_Public_Panel

- Benchmark: `data/network_science_public_panel_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.NetworkSciencePublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090

### Neural_Galactic_Orbital_Bridge

- Benchmark: `data/neural_galactic_orbital_bridge_benchmark.json` · records=49 · median%=0.018002668701796568
- Lean: `FSOT.Formal.NeuralGalacticOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/arxiv_brain_knowledge_panel_benchmark.json — https://github.com/data/arxiv_brain_knowledge_panel_benchmark.json
  - **dataset**: GitHub OSS corpus data/arxiv_primitives_panel_benchmark.json — https://github.com/data/arxiv_primitives_panel_benchmark.json
  - **dataset**: GitHub OSS corpus data/arxiv_primitives_v14_benchmark.json — https://github.com/data/arxiv_primitives_v14_benchmark.json
  - **dataset**: GitHub OSS corpus data/binary_decoder_rendlesham_benchmark.json — https://github.com/data/binary_decoder_rendlesham_benchmark.json
  - **unresolved**: cross_scale_motif — Named in panel source; add explicit public URL if this is an external authority

### Neuroeconomics

- Benchmark: `data/neuroeconomics_extension_benchmark.json` · records=65 · median%=0.10502056403980387
- Lean: `FSOT.Formal.NeuroeconomicsExtensionPriors`
- Public / portable anchors:
  - **unresolved**: neuroeconomics_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: psychology — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: econometrics — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: neuroeconomics_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: economics_yoy_bridge — Named in panel source; add explicit public URL if this is an external authority

### Neuroeconomics_Panel

- Benchmark: `data/neuroeconomics_panel_benchmark.json` · records=20 · median%=0.031506
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.NeuroeconomicsPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: Behavioral neuroeconomics reference — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Neurolab_Gaps_Math_Spine

- Benchmark: `data/neurolab_gaps_math_spine_benchmark.json` · records=35 · median%=0.0
- Lean: `FSOT.Formal.NeurolabGapsMathSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier64_neurolab_gap_panels — Named in panel source; add explicit public URL if this is an external authority

### Neurolab_Residual_Math_Spine

- Benchmark: `data/neurolab_residual_math_spine_benchmark.json` · records=28 · median%=0.0
- Lean: `FSOT.Formal.NeurolabResidualMathSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier66_neurolab_residual_panels — Named in panel source; add explicit public URL if this is an external authority

### Neuron_Zig_OS_Path_Panel

- Benchmark: `data/neuron_zig_os_path_panel_benchmark.json` · records=41 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/trinary_os/isa/fsotb_opcode_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/isa/fsotb_opcode_registry.json
  - **vendor_cache**: vendor/trinary_os/target/ — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/target/
  - **dataset**: GitHub OSS corpus docs/NEURON_ZIG_TO_OS_ROADMAP.md — https://github.com/docs/NEURON_ZIG_TO_OS_ROADMAP.md
  - **dataset**: GitHub OSS corpus docs/ENGINEERING_HARDWARE_CODE_DIRECTION.md — https://github.com/docs/ENGINEERING_HARDWARE_CODE_DIRECTION.md
  - **unresolved**: RELATED_EMBODIMENTS.md — Named in panel source; add explicit public URL if this is an external authority
  - **url**: https://github.com/dappalumbo91/fsot-neuron-zig — https://github.com/dappalumbo91/fsot-neuron-zig

### Neuroscience

- Benchmark: `data/neuroscience_fi_precision_benchmark.json` · records=20 · median%=0.0473
- Public / portable anchors:
  - **unresolved**: multi_hero_benchmark — Named in panel source; add explicit public URL if this is an external authority

### Neuroscience_Connectomics_Depth_Panel

- Benchmark: `data/neuroscience_connectomics_depth_panel_benchmark.json` · records=27 · median%=0.0201195
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.NeuroscienceConnectomicsDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\neuroscience_connectomics_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/neuroscience_connectomics_cache.json
  - **unresolved**: neuron_cohort — Named in panel source; add explicit public URL if this is an external authority
  - **api**: openneuro — https://openneuro.org/crn/graphql
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Neutrino_Physics_Panel

- Benchmark: `data/neutrino_physics_panel_benchmark.json` · records=20 · median%=0.009504
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.NeutrinoPhysicsPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Nothing_Perfection_Friction_Origin_Panel

- Benchmark: `data/nothing_perfection_friction_origin_panel_benchmark.json` · records=24 · median%=0.0
- Ingest: `scripts/ingest_tier91_foundational_ontology.py`
- Lean: `FSOT.Formal.NothingPerfectionFrictionOriginPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: phase_shift_physics — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: bubble_bleed_physics — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier91_foundational_ontology.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier91_foundational_ontology.py

### Nuclear_Lean_Route_Credibility

- Benchmark: `data/nuclear_lean_route_credibility_benchmark.json` · records=24 · median%=0.000637597
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **unresolved**: ASM International — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **unresolved**: CRC Handbook — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Reichardt, Solvents 3rd ed (2003) — Named in panel source; add explicit public URL if this is an external authority

### OPH_FSOT_Challenge_Panel

- Benchmark: `data/oph_fsot_challenge_panel_benchmark.json` · records=31 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor\public_data\oph_challenge_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/oph_challenge_public_anchors.json
  - **url**: https://x.com/muellerberndt/status/2079877767416709231 — https://x.com/muellerberndt/status/2079877767416709231
  - **url**: https://github.com/FloatingPragma/observer-patch-holography — https://github.com/FloatingPragma/observer-patch-holography
  - **dataset**: GitHub OSS corpus docs/OPH_FSOT_CHALLENGE_RESPONSE.md — https://github.com/docs/OPH_FSOT_CHALLENGE_RESPONSE.md
  - **dataset**: GitHub OSS corpus docs/T3_T4_GR_SM_DEEPENING.md — https://github.com/docs/T3_T4_GR_SM_DEEPENING.md
  - **dataset**: GitHub OSS corpus docs/CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md — https://github.com/docs/CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md
  - **dataset**: GitHub OSS corpus docs/TOE_CLAIM_BOUNDARIES.md — https://github.com/docs/TOE_CLAIM_BOUNDARIES.md
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/

### OSTI_DOE_Science_Panel

- Benchmark: `data/osti_doe_science_panel_benchmark.json` · records=100 · median%=0.01382
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.OstiDoeSciencePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://www.osti.gov/api/v1/records — https://www.osti.gov/api/v1/records
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### Observer_Channel_Derivation

- Benchmark: `data/observer_channel_derivation_benchmark.json` · records=372 · median%=0.052510282019890844
- Lean: `FSOT.Formal.ObserverChannelDerivationPriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_formula_spine.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_formula_spine.yaml
  - **vendor_cache**: extension_domains_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/extension_domains_manifest.yaml
  - **unresolved**: FSOT.Formal.Scalar.consciousness_factor — Named in panel source; add explicit public URL if this is an external authority

### Observer_Effect_Cross_Species_Panel

- Benchmark: `data/observer_effect_cross_species_panel_benchmark.json` · records=289 · median%=0.0
- Ingest: `scripts/ingest_tier90_consciousness_expansion.py`
- Lean: `FSOT.Formal.ObserverEffectCrossSpeciesPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/consciousness_reference_observables.json — https://github.com/data/consciousness_reference_observables.json
  - **dataset**: GitHub OSS corpus data/observer_channel_derivation_benchmark.json — https://github.com/data/observer_channel_derivation_benchmark.json
  - **unresolved**: FSOT.Formal.Scalar.consciousness_factor — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier90_consciousness_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier90_consciousness_expansion.py

### Observer_Lean_Route_Credibility

- Benchmark: `data/observer_lean_route_credibility_benchmark.json` · records=53 · median%=0.018003
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:observer — Named in panel source; add explicit public URL if this is an external authority

### Oceanography

- Benchmark: `data/oceanography_gap_fill_benchmark.json` · records=65 · median%=0.03017272606768673
- Public / portable anchors:
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **unresolved**: weather_observed — Named in panel source; add explicit public URL if this is an external authority
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/

### Omni_Theory_Humanities_Panel

- Benchmark: `data/omni_theory_humanities_panel_benchmark.json` · records=37 · median%=0.0222545
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.OmniTheoryHumanitiesPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\omni_theory_humanities_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/omni_theory_humanities_cache.json
  - **unresolved**: desktop_omni_theory — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### OpenAlex_Citation_Graph

- Benchmark: `data/openalex_citation_graph_benchmark.json` · records=80 · median%=0.031506
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.OpenalexCitationGraphPriors`
- Public / portable anchors:
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### OpenNeuro_Full_Panel

- Benchmark: `data/openneuro_full_panel_benchmark.json` · records=20 · median%=0.015431
- Ingest: `scripts/ingest_tier68_live_ingest.py`
- Lean: `FSOT.Formal.OpenNeuroFullPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\openneuro_full_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/openneuro_full_cache.json
  - **vendor_cache**: vendor/public_data/consciousness/openneuro_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/consciousness/openneuro_summary.json
  - **ingest_script**: scripts/ingest_tier68_live_ingest.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier68_live_ingest.py

### Open_Meteo_Live_Panel

- Benchmark: `data/open_meteo_live_panel_benchmark.json` · records=432 · median%=0.026204
- Ingest: `scripts/ingest_tier81_public_verifiable.py`
- Lean: `FSOT.Formal.OpenMeteoLivePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/
  - **ingest_script**: scripts/ingest_tier81_public_verifiable.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier81_public_verifiable.py

### Open_Science_Live_Concordance

- Benchmark: `data/open_science_live_concordance_benchmark.json` · records=24 · median%=0.0005550683289139394
- Public / portable anchors:
  - **api**: FDA open drug labeling records — https://api.fda.gov/drug/label.json?limit=5
  - **api**: Ensembl REST API — https://rest.ensembl.org/
  - **api**: GWAS Catalog studies (EBI) — https://www.ebi.ac.uk/gwas/rest/api/studies?size=5
  - **api**: ChEMBL API — https://www.ebi.ac.uk/chembl/
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **api**: Wikidata entity for π — https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q167&format=json
  - **api**: Our World in Data CO2 codebook (GitHub raw) — https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv
  - **api**: Zenodo open research records (physics) — https://zenodo.org/api/records/?q=subject:physics&size=3&sort=mostrecent
  - **api**: AlphaFold DB prediction metadata (P53) — https://alphafold.ebi.ac.uk/api/prediction/P04637
  - **api**: RCSB PDB REST API — https://data.rcsb.org/
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **api**: NCBI PubMed eSearch (open eutils) — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Hubble+tension&retmode=json&retmax=5
  - **api**: Crossref funders (open) — https://api.crossref.org/funders?query=national+science+foundation&rows=3
  - **api**: World Bank population indicator — https://api.worldbank.org/v2/country/USA/indicator/SP.POP.TOTL?format=json&per_page=5
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: STRING protein network API version — https://string-db.org/api/json/version
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: CERN Open Data — https://opendata.cern.ch/

### Open_Science_Seed_Constants

- Benchmark: `data/open_science_seed_constants_benchmark.json` · records=21 · median%=0.0
- Public / portable anchors:
  - **unresolved**: python_mathlib_identity — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: open_literature_math_constants — Named in panel source; add explicit public URL if this is an external authority

### Optics_Interferometry_Depth_Panel

- Benchmark: `data/optics_interferometry_depth_panel_benchmark.json` · records=82 · median%=0.026954
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.OpticsInterferometryDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\optics_interferometry_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/optics_interferometry_cache.json
  - **unresolved**: LIGO_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: MAST_em — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Overflow_Carry_Emergence_Panel

- Benchmark: `data/overflow_carry_emergence_panel_benchmark.json` · records=29 · median%=0.009504
- Lean: `FSOT.Formal.OverflowCarryEmergencePanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: multi_base_carry_analysis — Named in panel source; add explicit public URL if this is an external authority

### PDG_Particle_Properties

- Benchmark: `data/pdg_particle_properties_benchmark.json` · records=12 · median%=0.041994
- Lean: `FSOT.Formal.PdgParticlePropertiesPriors`
- Public / portable anchors:
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/

### Paleoclimate

- Benchmark: `data/paleoclimate_extension_benchmark.json` · records=40 · median%=0.015015854077432778
- Lean: `FSOT.Formal.PaleoclimateExtensionPriors`
- Public / portable anchors:
  - **unresolved**: paleoclimate_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/
  - **unresolved**: cryosphere — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: paleoclimate_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Paleoclimate_Panel

- Benchmark: `data/paleoclimate_panel_benchmark.json` · records=20 · median%=0.006006
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.PaleoclimatePanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Paleontology

- Benchmark: `data/paleontology_extension_benchmark.json` · records=630 · median%=0.017836062884406152
- Ingest: `scripts/build_tier_f_extension_benchmarks.py`
- Lean: `FSOT.Formal.PaleontologyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: PBDB — Named in panel source; add explicit public URL if this is an external authority
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **unresolved**: pbdb_api — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: pbdb_age — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/build_tier_f_extension_benchmarks.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/build_tier_f_extension_benchmarks.py

### Paleontology_Panel

- Benchmark: `data/paleontology_panel_benchmark.json` · records=120 · median%=0.0167305
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.PaleontologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: PBDB — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Particle_Neural_Orbital_Bridge

- Benchmark: `data/particle_neural_orbital_bridge_benchmark.json` · records=48 · median%=0.03326447040434832
- Lean: `FSOT.Formal.ParticleNeuralOrbitalBridgePriors`
- Public / portable anchors:
  - **vendor_cache**: domain_coupling_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/domain_coupling_simulation_benchmark.json
  - **dataset**: GitHub OSS corpus data/acoustic_resonance_materials_benchmark.json — https://github.com/data/acoustic_resonance_materials_benchmark.json
  - **dataset**: GitHub OSS corpus data/adjacent_rung_coupling_benchmark.json — https://github.com/data/adjacent_rung_coupling_benchmark.json
  - **dataset**: GitHub OSS corpus data/astrophysical_structure_crosswalk_benchmark.json — https://github.com/data/astrophysical_structure_crosswalk_benchmark.json
  - **dataset**: GitHub OSS corpus data/bibliography_lean_corpus_benchmark.json — https://github.com/data/bibliography_lean_corpus_benchmark.json

### Particle_Physics

- Benchmark: `data/particle_physics_gap_fill_benchmark.json` · records=98 · median%=0.0023222644988432507
- Lean: `FSOT.Formal.ParticlePhysicsPriors`
- Public / portable anchors:
  - **unresolved**: particle_physics_benchmark — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: smiles_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: thesis_wave — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_physics_rules — Named in panel source; add explicit public URL if this is an external authority

### Perceived_Lean_Route_Credibility

- Benchmark: `data/perceived_lean_route_credibility_benchmark.json` · records=58 · median%=0.018003
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:perceived — Named in panel source; add explicit public URL if this is an external authority

### Periodic_Extension_Decay_Topology_Scaffold

- Benchmark: `data/periodic_extension_decay_topology_scaffold_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.PeriodicExtensionDecayTopologyScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_decay_chain_prereg_scaffold_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_decay_chain_prereg_scaffold_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Periodic_Table_Completion_Spine

- Benchmark: `data/periodic_table_completion_spine_benchmark.json` · records=36 · median%=3.9999999999999996e-05
- Lean: `FSOT.Formal.PeriodicTableCompletionSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_physics_public_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_physics_public_panel_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Periodic_Table_Extension_Closure_Spine

- Benchmark: `data/periodic_table_extension_closure_spine_benchmark.json` · records=39 · median%=0.0
- Lean: `FSOT.Formal.PeriodicTableExtensionClosureSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: superheavy_island_completion_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/superheavy_island_completion_spine_benchmark.json
  - **vendor_cache**: periodic_table_completion_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/periodic_table_completion_spine_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Periodic_Table_Public_Panel

- Benchmark: `data/periodic_table_public_panel_benchmark.json` · records=52 · median%=9.5e-05
- Lean: `FSOT.Formal.PeriodicTablePublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### Petrology_Geochemistry_Panel

- Benchmark: `data/petrology_geochemistry_panel_benchmark.json` · records=80 · median%=0.030428
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.PetrologyGeochemistryPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: EarthChem subset — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Pharmacokinetics

- Benchmark: `data/pharmacokinetics_gap_fill_benchmark.json` · records=56 · median%=0.00241237063663613
- Lean: `FSOT.Formal.PharmacokineticsGapFillPriors`
- Public / portable anchors:
  - **unresolved**: pk_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: ChEMBL API — https://www.ebi.ac.uk/chembl/

### Phi_Morphogenetic_Scaling

- Benchmark: `data/phi_morphogenetic_scaling_benchmark.json` · records=289 · median%=0.01760779720633292
- Lean: `FSOT.Formal.PhiMorphogeneticScalingPriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_species_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_species_catalog.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Physarum_Biological_CUDA_Panel

- Benchmark: `data/physarum_biological_cuda_panel_benchmark.json` · records=24 · median%=0.0003086625
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.PhysarumBiologicalCudaPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\biological_cuda_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/biological_cuda_cache.json
  - **unresolved**: desktop_physarum — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Portable_Clone_Verify

- Benchmark: `data/portable_clone_verify_benchmark.json` · records=419 · median%=0.0
- Lean: `FSOT.Formal.PortableCloneVerifyPriors`
- Public / portable anchors:
  - **vendor_cache**: external_data_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/external_data_manifest.yaml
  - **vendor_cache**: extension_domains_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/extension_domains_manifest.yaml
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **vendor_cache**: vendor/smiles/FSOT_SMILES_Lab_Dataset.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json
  - **vendor_cache**: vendor/evolution/biological_mt_operons.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/evolution/biological_mt_operons.json
  - **vendor_cache**: vendor/linguistics/data/LINGUISTIC_TARGETS.csv — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/linguistics/data/LINGUISTIC_TARGETS.csv
  - **vendor_cache**: vendor/linguistics/linguistics_derivations.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/linguistics/linguistics_derivations.json
  - **vendor_cache**: vendor/math_generator/generated_formula_comparison_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/generated_formula_comparison_report.json
  - **vendor_cache**: vendor/math_generator/rules — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/rules
  - **vendor_cache**: vendor/trinary_os/target — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/target
  - **vendor_cache**: vendor/species/fsot_species_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/species/fsot_species_catalog.json
  - **vendor_cache**: vendor/igem/igem_parts_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/igem_parts_registry.json
  - **dataset**: GitHub OSS corpus vendor/reference_anchors — https://github.com/vendor/reference_anchors
  - **vendor_cache**: vendor/fsot_aggregate/FSOT_UNIFIED.db — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/FSOT_UNIFIED.db
  - **vendor_cache**: vendor/neuron_cohort/cells.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/neuron_cohort/cells.json
  - **vendor_cache**: vendor/knowledge_base/kb_portable_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/knowledge_base/kb_portable_summary.json
  - **vendor_cache**: vendor/math_generator/benchmark_reports — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/benchmark_reports
  - **vendor_cache**: vendor/trinary_os/isa/fsotb_opcode_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/isa/fsotb_opcode_registry.json
  - **vendor_cache**: vendor/igem/fastas — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/fastas
  - **vendor_cache**: vendor/math_generator/datasets/airfoil_self_noise.csv — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/datasets/airfoil_self_noise.csv
  - **vendor_cache**: vendor/trinary_os/fixtures — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/fixtures
  - **vendor_cache**: vendor/trinary_os/round_trip — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/round_trip
  - **dataset**: GitHub OSS corpus vendor/tokenization — https://github.com/vendor/tokenization
  - **vendor_cache**: vendor/trinary_hardware/motif_influence_profile_stable.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_hardware/motif_influence_profile_stable.json
  - **vendor_cache**: vendor/intrinsic_llm/benchmark_results_final.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/intrinsic_llm/benchmark_results_final.json
  - … +17 more in JSON

### Prediction_Rederivation

- Benchmark: `data/prediction_rederivation_benchmark.json` · records=23 · median%=0.000561846
- Lean: `FSOT.Formal.PredictionRederivationPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/fsot_aggregate/prediction_rederivation_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fsot_aggregate/prediction_rederivation_summary.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Preregistered_Outcome_Tracking

- Benchmark: `data/preregistered_outcome_tracking_benchmark.json` · records=72 · median%=0.0
- Lean: `FSOT.Formal.PreregisteredOutcomeTrackingPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\data\preregistered_predictions_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/data/preregistered_predictions_manifest.yaml
  - **vendor_cache**: preregistered_predictions_verification_scaffold_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_verification_scaffold_benchmark.json

### Preregistered_Predictions

- Benchmark: `data/preregistered_predictions_benchmark.json` · records=35 · median%=0.02009823784840936
- Lean: `FSOT.Formal.PreregisteredPredictionsPriors`
- Public / portable anchors:
  - **vendor_cache**: preregistered_predictions_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_manifest.yaml

### Preregistered_Predictions_Verification_Scaffold

- Benchmark: `data/preregistered_predictions_verification_scaffold_benchmark.json` · records=60 · median%=0.0
- Lean: `FSOT.Formal.PreregisteredPredictionsVerificationScaffoldPriors`
- Public / portable anchors:
  - **vendor_cache**: preregistered_predictions_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_manifest.yaml
  - **vendor_cache**: preregistered_predictions_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/preregistered_predictions_benchmark.json

### Programming_Language_Laws

- Benchmark: `data/programming_language_laws_benchmark.json` · records=105 · median%=0.0
- Lean: `FSOT.Formal.ProgrammingLanguageLawsPriors`
- Public / portable anchors:
  - **vendor_cache**: PROGRAMMING_LANGUAGE_RULES.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/PROGRAMMING_LANGUAGE_RULES.json
  - **unresolved**: math_generator_rules_eval — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: linguistics_formal — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: linguistics_formal_benchmark — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: programming_language_crosswalk — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: code_genome_structure_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_risk_evaluator_cybersecurity_benchmark — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_language_bridges — Named in panel source; add explicit public URL if this is an external authority

### Proof_Carrying_Code_Genome

- Benchmark: `data/proof_carrying_code_genome_benchmark.json` · records=25 · median%=0.0051685586271776884
- Lean: `FSOT.Formal.ProofCarryingCodeGenomePriors`
- Public / portable anchors:
  - **vendor_cache**: external_oss_code_genome_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/external_oss_code_genome_benchmark.json
  - **vendor_cache**: rust_lean_bridge_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/rust_lean_bridge_benchmark.json
  - **vendor_cache**: computational_reasoning_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/computational_reasoning_benchmark.json

### Proof_Ledger_Closure_Spine

- Benchmark: `data/proof_ledger_closure_spine_benchmark.json` · records=17 · median%=0.0
- Lean: `FSOT.Formal.ProofLedgerClosureSpinePriors`
- Public / portable anchors:
  - **vendor_cache**: proof_ledger.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/proof_ledger.yaml
  - **vendor_cache**: fsot_verification_progress.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_verification_progress.yaml
  - **vendor_cache**: certificate.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/certificate.json

### Proton_Lean_Route_Credibility

- Benchmark: `data/proton_lean_route_credibility_benchmark.json` · records=58 · median%=0.009504
- Public / portable anchors:
  - **unresolved**: lean_route_credibility_expansion:proton — Named in panel source; add explicit public URL if this is an external authority
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### Psychology

- Benchmark: `data/psychology_gap_fill_benchmark.json` · records=160 · median%=0.03150616921194649
- Public / portable anchors:
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **unresolved**: linguistics_lab — Named in panel source; add explicit public URL if this is an external authority
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **unresolved**: linguistics_corpus — Named in panel source; add explicit public URL if this is an external authority

### Psychology_Psychometrics_Depth_Panel

- Benchmark: `data/psychology_psychometrics_depth_panel_benchmark.json` · records=24 · median%=0.009282423000000001
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.PsychologyPsychometricsDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\psychology_psychometrics_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/psychology_psychometrics_cache.json
  - **unresolved**: psychometrics_rct_literature_anchors — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### PubChem_Compound_Properties

- Benchmark: `data/pubchem_compound_properties_benchmark.json` · records=500 · median%=0.002637
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.PubchemCompoundPropertiesPriors`
- Public / portable anchors:
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### PubChem_Live_Deep

- Benchmark: `data/pubchem_live_deep_benchmark.json` · records=5043 · median%=0.032631
- Ingest: `scripts/ingest_tier68_live_ingest.py`
- Lean: `FSOT.Formal.PubChemLiveDeepPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\pubchem_live_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/pubchem_live_cache.json
  - **vendor_cache**: vendor/public_data/pubchem/pubchem_preregistered_panel.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_preregistered_panel.json
  - **vendor_cache**: vendor/public_data/pubchem/pubchem_culinary_expansion.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_culinary_expansion.json
  - **vendor_cache**: vendor/public_data/pubchem/pubchem_auto_expansion.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_auto_expansion.json
  - **vendor_cache**: vendor/public_data/pubchem/pubchem_auto_seed_manifest.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_auto_seed_manifest.json
  - **vendor_cache**: pubchem_compound_properties_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pubchem_compound_properties_benchmark.json
  - **vendor_cache**: pharmacology_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pharmacology_benchmark.json
  - **vendor_cache**: culinary_arts_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/culinary_arts_benchmark.json
  - **vendor_cache**: maillard_chemistry_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/maillard_chemistry_gap_fill_benchmark.json
  - **vendor_cache**: food_microbiology_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/food_microbiology_gap_fill_benchmark.json
  - **ingest_script**: scripts/ingest_tier68_live_ingest.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier68_live_ingest.py

### PubChem_Stability_Panel

- Benchmark: `data/pubchem_stability_panel_benchmark.json` · records=59 · median%=0.0024239449292213135
- Lean: `FSOT.Formal.PubChemStabilityPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/public_data/pubchem/pubchem_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/public_data/pubchem/pubchem_summary.json
  - **vendor_cache**: pubchem_compound_properties_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/pubchem_compound_properties_benchmark.json

### Public_Verifiable_Spine

- Benchmark: `data/public_verifiable_spine_benchmark.json` · records=20 · median%=0.0
- Lean: `FSOT.Formal.PublicVerifiableSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier81_public_verifiable_panels — Named in panel source; add explicit public URL if this is an external authority

### Published_Fuel_Property_Panel

- Benchmark: `data/published_fuel_property_panel_benchmark.json` · records=31 · median%=0.0
- Lean: `FSOT.Formal.PublishedFuelPropertyPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/fuel/public_fuel_property_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fuel/public_fuel_property_catalog.json
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Pure_Mathematics

- Benchmark: `data/pure_mathematics_extension_benchmark.json` · records=1578 · median%=0.0
- Lean: `FSOT.Formal.PureMathematicsExtensionPriors`
- Public / portable anchors:
  - **unresolved**: mathematics_computational — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_generator_rules — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: math_generator_pure — Named in panel source; add explicit public URL if this is an external authority

### Pure_Mathematics_Panel

- Benchmark: `data/pure_mathematics_panel_benchmark.json` · records=44 · median%=0.02584
- Ingest: `scripts/ingest_tier86_scientific_expansion.py`
- Lean: `FSOT.Formal.PureMathematicsPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: math_generator — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier86_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier86_scientific_expansion.py

### QCE_ELM_Fusion_Edge_Panel

- Benchmark: `data/qce_elm_fusion_edge_panel_benchmark.json` · records=45 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fusion\qce_elm_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fusion/qce_elm_public_anchors.json
  - **unresolved**: Physical Review Letters 2026 Zhang et al. QCE — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: public ELM literature + TechTimes/PRL summary — Named in panel source; add explicit public URL if this is an external authority

### Quantum_Computing

- Benchmark: `data/quantum_computing_gap_fill_benchmark.json` · records=177 · median%=0.0002953462072651492
- Public / portable anchors:
  - **unresolved**: QUANTUM_COMPUTING_rules — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: trinary_os — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_generator_quantum — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CERN Open Data — https://opendata.cern.ch/
  - **unresolved**: trinary_os_oracle — Named in panel source; add explicit public URL if this is an external authority

### Quantum_Computing_Math_Depth_Panel

- Benchmark: `data/quantum_computing_math_depth_panel_benchmark.json` · records=77 · median%=0.014767
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.QuantumComputingMathDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\quantum_computing_math_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/quantum_computing_math_cache.json
  - **unresolved**: QUANTUM_COMPUTING_RULES — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: math_first_qc_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: quantum_computing_gap_fill — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Quantum_Information

- Benchmark: `data/quantum_information_benchmark.json` · records=21 · median%=0.0
- Lean: `FSOT.Formal.QuantumInformationPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Quantum_Mechanics

- Benchmark: `data/quantum_mechanics_gap_fill_benchmark.json` · records=50 · median%=9.52387420324368e-05
- Public / portable anchors:
  - **unresolved**: SMILES_quantum — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Quantum_Mechanics_Entanglement_Depth_Panel

- Benchmark: `data/quantum_mechanics_entanglement_depth_panel_benchmark.json` · records=21 · median%=0.014767
- Ingest: `scripts/ingest_tier87_scientific_expansion.py`
- Lean: `FSOT.Formal.QuantumMechanicsEntanglementDepthPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\scientific_expansion\tier87_cache\quantum_mechanics_entanglement_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/scientific_expansion/tier87_cache/quantum_mechanics_entanglement_cache.json
  - **unresolved**: entanglement_decoherence_literature_anchors — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier87_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier87_scientific_expansion.py

### Quantum_Optics

- Benchmark: `data/quantum_optics_gap_fill_benchmark.json` · records=50 · median%=9.52387420324368e-05
- Public / portable anchors:
  - **unresolved**: SMILES_quantum — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### RCSB_PDB_Structures

- Benchmark: `data/rcsb_pdb_structures_benchmark.json` · records=45 · median%=0.022236
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.RcsbPdbStructuresPriors`
- Public / portable anchors:
  - **api**: RCSB PDB REST API — https://data.rcsb.org/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### RD_Interval_Tightening_Panel

- Benchmark: `data/rd_interval_tightening_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.RdIntervalTighteningPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: cosmology_anomaly_deep_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_anomaly_deep_panel_benchmark.json
  - **unresolved**: FSOT.Formal.Cosmology — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/

### Radio_Astronomy_Panel

- Benchmark: `data/radio_astronomy_panel_benchmark.json` · records=30 · median%=0.022461
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.RadioAstronomyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: VizieR NVSS — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Reality_Folding_Spine

- Benchmark: `data/reality_folding_spine_benchmark.json` · records=24 · median%=0.000637597
- Lean: `FSOT.Formal.RealityFoldingSpinePriors`
- Public / portable anchors:
  - **vendor_cache**: compactification_ladder_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/compactification_ladder_benchmark.json
  - **vendor_cache**: adjacent_rung_coupling_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/adjacent_rung_coupling_benchmark.json
  - **vendor_cache**: fold_depth_metrics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fold_depth_metrics_benchmark.json
  - **vendor_cache**: toe_unification_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/toe_unification_spine_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: Compactification_Ladder — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Adjacent_Rung_Coupling — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Fold_Depth_Metrics — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: reality_folding_spine_metrics — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Recent_Breakthroughs_Expansion_Panel

- Benchmark: `data/recent_breakthroughs_expansion_panel_benchmark.json` · records=63 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fusion\qce_elm_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fusion/qce_elm_public_anchors.json
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\fusion\fusion_public_anchors.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/fusion/fusion_public_anchors.json
  - **unresolved**: public 2022–2026 fusion/quantum breakthrough literature — Named in panel source; add explicit public URL if this is an external authority

### Robotics_Control_Systems

- Benchmark: `data/robotics_control_systems_extension_benchmark.json` · records=44 · median%=0.0
- Lean: `FSOT.Formal.RoboticsControlSystemsExtensionPriors`
- Public / portable anchors:
  - **unresolved**: robotics_control_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: trinary_os_ISA — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: robotics_control_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: trinary_os_control_bridge — Named in panel source; add explicit public URL if this is an external authority

### Robotics_Control_Systems_Panel

- Benchmark: `data/robotics_control_systems_panel_benchmark.json` · records=24 · median%=0.01341
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.RoboticsControlSystemsPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: IEEE robotics reference — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### Rust_Lean_Bridge_Panel

- Benchmark: `data/rust_lean_bridge_panel_benchmark.json` · records=21 · median%=0.0
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.RustLeanBridgePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\rust_lean_bridge_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/rust_lean_bridge_cache.json
  - **unresolved**: desktop_rust_lean_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### SH0ES_Refined

- Benchmark: `data/sh0es_refined_benchmark.json` · records=7 · median%=0.0
- Ingest: `scripts/ingest_anomaly_public_data.py`
- Lean: `FSOT.Formal.SH0ESRefinedPriors`
- Public / portable anchors:
  - **literature**: SH0ES / local distance ladder H0 (Riess et al. series) — https://ui.adsabs.harvard.edu/
  - **dataset**: GitHub OSS corpus data/sh0es_host_coordinates.json — https://github.com/data/sh0es_host_coordinates.json
  - **dataset**: GitHub OSS corpus data/sector_h0_seed.json — https://github.com/data/sector_h0_seed.json
  - **ingest_script**: scripts/ingest_anomaly_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_anomaly_public_data.py

### SIMBAD_Stellar_Identity_Deep

- Benchmark: `data/simbad_stellar_identity_deep_benchmark.json` · records=520 · median%=0.022461
- Ingest: `scripts/ingest_tier60_live_astrometry.py`
- Lean: `FSOT.Formal.SIMBADStellarIdentityDeepPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **ingest_script**: scripts/ingest_tier60_live_astrometry.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier60_live_astrometry.py

### STScI_MAST_Telescope_Panel

- Benchmark: `data/stsci_mast_telescope_panel_benchmark.json` · records=377 · median%=0.022461
- Ingest: `scripts/ingest_stsci_mast.py`
- Lean: `FSOT.Formal.StsciMastTelescopePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://archive.stsci.edu/ — https://archive.stsci.edu/
  - **ingest_script**: scripts/ingest_stsci_mast.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_stsci_mast.py

### Scalar_Solver_35_Panel

- Benchmark: `data/scalar_solver_35_panel_benchmark.json` · records=21 · median%=0.007394383
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.ScalarSolver35PanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\scalar_solver_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/scalar_solver_cache.json
  - **unresolved**: desktop_scalar_solver — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Schematic_Netlist_Intrinsic_Panel

- Benchmark: `data/schematic_netlist_intrinsic_panel_benchmark.json` · records=27 · median%=0.020755
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\circuit_components\industry_component_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/circuit_components/industry_component_catalog.json
  - **unresolved**: reference_circuits — Named in panel source; add explicit public URL if this is an external authority

### Scientific_Expansion_Depth_Spine

- Benchmark: `data/scientific_expansion_depth_spine_benchmark.json` · records=72 · median%=0.033841
- Lean: `FSOT.Formal.ScientificExpansionDepthSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier86_depth_wave_panels — Named in panel source; add explicit public URL if this is an external authority

### Scientific_Expansion_Depth_Wave2_Spine

- Benchmark: `data/scientific_expansion_depth_wave2_spine_benchmark.json` · records=40 · median%=0.0
- Lean: `FSOT.Formal.ScientificExpansionDepthWave2SpinePriors`
- Public / portable anchors:
  - **unresolved**: tier87_depth_wave2_panels — Named in panel source; add explicit public URL if this is an external authority

### Scientific_Expansion_Spine

- Benchmark: `data/scientific_expansion_spine_benchmark.json` · records=40 · median%=0.0
- Lean: `FSOT.Formal.ScientificExpansionSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier82_scientific_expansion_panels — Named in panel source; add explicit public URL if this is an external authority

### Scientific_Expansion_Wave2_Spine

- Benchmark: `data/scientific_expansion_wave2_spine_benchmark.json` · records=40 · median%=0.0
- Lean: `FSOT.Formal.ScientificExpansionWave2SpinePriors`
- Public / portable anchors:
  - **unresolved**: tier84_scientific_expansion_panels — Named in panel source; add explicit public URL if this is an external authority

### Scientific_Expansion_Wave3_Spine

- Benchmark: `data/scientific_expansion_wave3_spine_benchmark.json` · records=40 · median%=0.0
- Lean: `FSOT.Formal.ScientificExpansionWave3SpinePriors`
- Public / portable anchors:
  - **unresolved**: tier85_scientific_expansion_panels — Named in panel source; add explicit public URL if this is an external authority

### Secure_Software_Engineering

- Benchmark: `data/secure_software_engineering_cybersecurity_benchmark.json` · records=59 · median%=0.0
- Lean: `FSOT.Formal.SecureSoftwareEngineeringPriors`
- Public / portable anchors:
  - **unresolved**: CVE_CWE_shape — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: rust_lean_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: trinary_os_tier_e — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: secure_software_engineering_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Semiconductor_Physics_Public_Panel

- Benchmark: `data/semiconductor_physics_public_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.SemiconductorPhysicsPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/

### Small_Body_Orbits

- Benchmark: `data/small_body_orbits_benchmark.json` · records=23 · median%=0.000561846
- Ingest: `scripts/ingest_small_body_jpl.py`
- Lean: `FSOT.Formal.SmallBodyOrbitsPriors`
- Public / portable anchors:
  - **api**: JPL Solar System Dynamics / Horizons — https://ssd.jpl.nasa.gov/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **api**: JPL Horizons system — https://ssd.jpl.nasa.gov/horizons/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - … +4 more in JSON

### Sociology

- Benchmark: `data/sociology_gap_fill_benchmark.json` · records=200 · median%=0.019504399572475274
- Public / portable anchors:
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **api**: OpenAlex scholarly graph API — https://api.openalex.org/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/

### Soil_Science_Panel

- Benchmark: `data/soil_science_panel_benchmark.json` · records=96 · median%=0.006006
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.SoilSciencePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: ISRIC SoilGrids v2 — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Solar_System_Structure_Deep

- Benchmark: `data/solar_system_structure_deep_benchmark.json` · records=48 · median%=0.0
- Ingest: `scripts/ingest_planetary_jpl.py`
- Lean: `FSOT.Formal.SolarSystemStructureDeepPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/planetary_jpl_cache.json — https://github.com/data/planetary_jpl_cache.json
  - **api**: JPL Solar System Dynamics / Horizons — https://ssd.jpl.nasa.gov/
  - **ingest_script**: scripts/ingest_planetary_jpl.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_planetary_jpl.py

### Space_Propulsion_Systems

- Benchmark: `data/space_propulsion_systems_benchmark.json` · records=21 · median%=0.0
- Ingest: `scripts/ingest_tier39_propulsion_electrical.py`
- Lean: `FSOT.Formal.SpacePropulsionSystemsPriors`
- Public / portable anchors:
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **ingest_script**: scripts/ingest_tier39_propulsion_electrical.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier39_propulsion_electrical.py

### Speleology

- Benchmark: `data/speleology_extension_benchmark.json` · records=65 · median%=0.0034072140135262413
- Lean: `FSOT.Formal.SpeleologyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: speleology_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **unresolved**: geochemistry — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: speleology_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: smiles_lab — Named in panel source; add explicit public URL if this is an external authority

### Speleology_Panel

- Benchmark: `data/speleology_panel_benchmark.json` · records=24 · median%=0.000637597
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.SpeleologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Sports_Biomechanics

- Benchmark: `data/sports_biomechanics_gap_fill_benchmark.json` · records=35 · median%=0.04447250077037523
- Lean: `FSOT.Formal.SportsBiomechanicsGapFillPriors`
- Public / portable anchors:
  - **unresolved**: World_Athletics_records — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: airfoil_motion_bridge — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: world_athletics_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: aerodynamics_motion_bridge — Named in panel source; add explicit public URL if this is an external authority

### Star_Trek_Transporter_Live_Panel

- Benchmark: `data/star_trek_transporter_live_panel_benchmark.json` · records=1575 · median%=0.031159
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.StarTrekTransporterLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\star_trek_transporter_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/star_trek_transporter_cache.json
  - **unresolved**: fsot_transporter_technology_stack — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\verified_desktop\legacy_physics\warp_actuation_formula_fsot21.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/verified_desktop/legacy_physics/warp_actuation_formula_fsot21.json
  - **vendor_cache**: I:\FSOT-Physical-Archive\08_Verified-Desktop-Projects\star_trek_transporter\pattern_buffer_scan_results.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/08_Verified-Desktop-Projects/star_trek_transporter/pattern_buffer_scan_results.json
  - **unresolved**: Warp_BH_WH_Portal_Panel — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Statistical_Mechanics_Public_Panel

- Benchmark: `data/statistical_mechanics_public_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.StatisticalMechanicsPublicPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### Stellar_Multiplicity_Catalog

- Benchmark: `data/stellar_multiplicity_catalog_benchmark.json` · records=68 · median%=0.0
- Lean: `FSOT.Formal.StellarMultiplicityCatalogPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/stellar_structures/public_multiplicity_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/stellar_structures/public_multiplicity_catalog.json
  - **vendor_cache**: wds_multiplicity_expanded.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/wds_multiplicity_expanded.json

### Stellar_Multiplicity_Live_Deep

- Benchmark: `data/stellar_multiplicity_live_deep_benchmark.json` · records=69 · median%=0.0
- Ingest: `scripts/ingest_tier58_live_catalogs.py`
- Lean: `FSOT.Formal.StellarMultiplicityLiveDeepPriors`
- Public / portable anchors:
  - **vendor_cache**: stellar_multiplicity_catalog_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stellar_multiplicity_catalog_benchmark.json
  - **vendor_cache**: gwosc_live_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/gwosc_live_cache.json
  - **ingest_script**: scripts/ingest_tier58_live_catalogs.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier58_live_catalogs.py

### Stumped_Observables_Panel

- Benchmark: `data/stumped_observables_panel_benchmark.json` · records=22 · median%=0.007871
- Lean: `FSOT.Formal.StumpedObservablesPanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/stumped_observables_reference.json — https://github.com/data/stumped_observables_reference.json
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **dataset**: GitHub OSS corpus scripts/higgs_mass_formula_eval.py — https://github.com/scripts/higgs_mass_formula_eval.py
  - **dataset**: GitHub OSS corpus data/sector_h0_seed.json — https://github.com/data/sector_h0_seed.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Stumped_Observables_Spine

- Benchmark: `data/stumped_observables_spine_benchmark.json` · records=24 · median%=3.8622500000000005e-05
- Lean: `FSOT.Formal.StumpedObservablesSpinePriors`
- Public / portable anchors:
  - **vendor_cache**: stumped_observables_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/stumped_observables_panel_benchmark.json
  - **vendor_cache**: hubble_bubble_tension_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/hubble_bubble_tension_benchmark.json
  - **vendor_cache**: dark_sector_open_problems_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/dark_sector_open_problems_benchmark.json
  - **vendor_cache**: cosmology_anomalies_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_anomalies_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: Stumped_Observables_Panel — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Hubble_Bubble_Tension — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Dark_Sector_Open_Problems — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Cosmology_Anomalies — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: stumped_observables_reference — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Superheavy_Element_Stability_Panel

- Benchmark: `data/superheavy_element_stability_panel_benchmark.json` · records=50 · median%=1e-06
- Lean: `FSOT.Formal.SuperheavyElementStabilityPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: particle_physics_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/particle_physics_benchmark.json

### Superheavy_Island_Completion_Spine

- Benchmark: `data/superheavy_island_completion_spine_benchmark.json` · records=41 · median%=0.0
- Lean: `FSOT.Formal.SuperheavyIslandCompletionSpinePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: lab_synthesis_metamaterial_spine_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/lab_synthesis_metamaterial_spine_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Superheavy_Island_Emergence_Simulation

- Benchmark: `data/superheavy_island_emergence_simulation_benchmark.json` · records=32 · median%=0.0
- Lean: `FSOT.Formal.SuperheavyIslandEmergenceSimulationPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: fusion_decay_chain_prereg_scaffold_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fusion_decay_chain_prereg_scaffold_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl

### Supply_Chain_Logistics

- Benchmark: `data/supply_chain_logistics_extension_benchmark.json` · records=40 · median%=0.03230022603427978
- Lean: `FSOT.Formal.SupplyChainLogisticsExtensionPriors`
- Public / portable anchors:
  - **unresolved**: supply_chain_reference — Named in panel source; add explicit public URL if this is an external authority
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **unresolved**: agriculture_agroecology — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: supply_chain_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/

### Supply_Chain_Logistics_Panel

- Benchmark: `data/supply_chain_logistics_panel_benchmark.json` · records=40 · median%=0.02584
- Ingest: `scripts/ingest_tier85_scientific_expansion.py`
- Lean: `FSOT.Formal.SupplyChainLogisticsPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **ingest_script**: scripts/ingest_tier85_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier85_scientific_expansion.py

### Symbolic_Archetype_Panel

- Benchmark: `data/symbolic_archetype_panel_benchmark.json` · records=22 · median%=0.0
- Ingest: `scripts/ingest_fringe_desktop_data.py`
- Lean: `FSOT.Formal.SymbolicArchetypePanelPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus data/symbolic_archetype_reference.json — https://github.com/data/symbolic_archetype_reference.json
  - **vendor_cache**: vendor/fringe_desktop/symbolic_encoding_graph_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/fringe_desktop/symbolic_encoding_graph_summary.json
  - **vendor_cache**: G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json
  - **dataset**: GitHub OSS corpus scripts/symbolic_archetype_lib.py — https://github.com/scripts/symbolic_archetype_lib.py
  - **ingest_script**: scripts/ingest_fringe_desktop_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_fringe_desktop_data.py

### Term3_Acoustic_Bleed_Depth

- Benchmark: `data/term3_acoustic_bleed_depth_benchmark.json` · records=23 · median%=0.008381497018408523
- Lean: `FSOT.Formal.Term3AcousticBleedDepthPriors`
- Public / portable anchors:
  - **vendor_cache**: acoustic_resonance_materials_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/acoustic_resonance_materials_benchmark.json
  - **vendor_cache**: music_harmonics_public_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/music_harmonics_public_panel_benchmark.json
  - **vendor_cache**: fsot_species_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_species_catalog.json
  - **vendor_cache**: architecture_building_science_gap_fill_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/architecture_building_science_gap_fill_benchmark.json

### The_Well_Outcomes_Verification_Panel

- Benchmark: `data/the_well_outcomes_verification_panel_benchmark.json` · records=246 · median%=0.031159
- Ingest: `scripts/ingest_tier89_the_well.py`
- Lean: `FSOT.Formal.TheWellOutcomesVerificationPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: G:\FSOT-PublicData\the_well\the_well_catalog_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/the_well/the_well_catalog_cache.json
  - **url**: https://huggingface.co/collections/polymathic-ai/the-well — https://huggingface.co/collections/polymathic-ai/the-well
  - **api**: arXiv API / metadata — https://arxiv.org/help/api/
  - **ingest_script**: scripts/ingest_tier89_the_well.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier89_the_well.py

### The_Well_Spot_Check_Panel

- Benchmark: `data/the_well_spot_check_panel_benchmark.json` · records=24 · median%=0.015860423
- Ingest: `scripts/ingest_tier89_the_well.py`
- Lean: `FSOT.Formal.TheWellSpotCheckPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: G:\FSOT-PublicData\the_well\the_well_spot_checks_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/G:/FSOT-PublicData/the_well/the_well_spot_checks_cache.json
  - **unresolved**: the_well_hdf5_spot_chunks — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **ingest_script**: scripts/ingest_tier89_the_well.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier89_the_well.py

### The_Well_Verification_Spine

- Benchmark: `data/the_well_verification_spine_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.TheWellVerificationSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier89_the_well_panels — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: polymathic_ai_the_well — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### Theory_Completeness_Spine

- Benchmark: `data/theory_completeness_spine_benchmark.json` · records=6 · median%=0.0
- Lean: `FSOT.Formal.TheoryCompletenessSpinePriors`
- Public / portable anchors:
  - **unresolved**: formula_branching_fractal — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: cve_codon_hole_falsification — Named in panel source; add explicit public URL if this is an external authority

### Tier_93_Dual_Wave_Spine

- Benchmark: `data/tier_93_dual_wave_spine_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.Tier93DualWaveSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier93_dual_wave_panels — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/

### Tier_94_Longevity_Spine

- Benchmark: `data/tier_94_longevity_spine_benchmark.json` · records=34 · median%=0.0
- Lean: `FSOT.Formal.Tier94LongevitySpinePriors`
- Public / portable anchors:
  - **unresolved**: tier94_longevity_panels — Named in panel source; add explicit public URL if this is an external authority

### Tier_95_Zebrafish_Spine

- Benchmark: `data/tier_95_zebrafish_spine_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.Tier95ZebrafishSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier95_zebrahub_panels — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Tier_96_Circuit_Spine

- Benchmark: `data/tier_96_circuit_spine_benchmark.json` · records=37 · median%=0.020755
- Public / portable anchors:
  - **unresolved**: circuit_component_emergence — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: electrical_power_systems_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/electrical_power_systems_benchmark.json

### Time_Domain_Crosswalk

- Benchmark: `data/time_domain_crosswalk_benchmark.json` · records=371 · median%=0.027551
- Lean: `FSOT.Formal.TimeDomainCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: extension_domains_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/extension_domains_manifest.yaml
  - **vendor_cache**: time_emergence_manifest.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_manifest.yaml
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py

### Time_Emergence_Deep_Panel

- Benchmark: `data/time_emergence_deep_panel_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.TimeEmergenceDeepPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: time_emergence_simulation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/time_emergence_simulation_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/

### Time_Emergence_Simulation

- Benchmark: `data/time_emergence_simulation_benchmark.json` · records=28 · median%=0.0
- Lean: `FSOT.Formal.TimeEmergenceSimulationPriors`
- Public / portable anchors:
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: IERS Earth sidereal — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: cosmology_extended_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cosmology_extended_benchmark.json
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py
  - **unresolved**: BlackHoleThesisPriors — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: derived from IERS sidereal period — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: derived lunar sidereal — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: data/cosmology_extended_benchmark.json lambda_cdm H0 — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/data/cosmology_extended_benchmark.json lambda_cdm H0
  - **unresolved**: GR dτ/dt at r=3M (photon sphere), M Schwarzschild mass — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **unresolved**: IERS Earth sidereal + NULL Island prime-meridian τ prior — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NASA Kepler / exoplanet archives (as cited per panel) — https://exoplanetarchive.ipac.caltech.edu/
  - **unresolved**: cosmology_extended_benchmark.json — cosmological damping τ anchor — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Poof-dominant molecular valve — unity τ recycle baseline — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: S_sign_multi_scale_hierarchy — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: GR Schwarzschild vs FPC whirlpool horizon stack — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: IERS Earth sidereal phase at prime meridian — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: NULL Island 0N 0E UTC diurnal cycle — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fluid_navigation_analogy — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: navigation sweep — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Greenwich τ anchor — longitude is θ phase label, not rate multiplier — Named in panel source; add explicit public URL if this is an external authority

### ToE_Claim_Certificate_Bundle

- Benchmark: `data/toe_claim_certificate_bundle_benchmark.json` · records=7 · median%=0.0
- Lean: `FSOT.Formal.ToEClaimCertificateBundlePriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_verification_progress.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_verification_progress.yaml
  - **vendor_cache**: FSOT_VERIFIED_SCOPE.yaml — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/FSOT_VERIFIED_SCOPE.yaml
  - **vendor_cache**: scientific_domain_expansion_map.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/scientific_domain_expansion_map.json

### ToE_Gap_Closure_Spine

- Benchmark: `data/toe_gap_closure_spine_benchmark.json` · records=7 · median%=0.0
- Lean: `FSOT.Formal.ToEGapClosureSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier_k_gap_closure_pillars — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Fractal_Constant_Recursion — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Preregistered_Predictions — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Portable_Clone_Verify — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Observer_Channel_Derivation — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Adversarial_Fractal_Break_Tests — Named in panel source; add explicit public URL if this is an external authority

### ToE_Unification_Spine

- Benchmark: `data/toe_unification_spine_benchmark.json` · records=8 · median%=0.0
- Lean: `FSOT.Formal.ToEUnificationSpinePriors`
- Public / portable anchors:
  - **unresolved**: toe_gap_closure_spine — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: theory_completeness_spine — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: domain_orbital_predictions — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: toe_unification_metrics — Named in panel source; add explicit public URL if this is an external authority

### Tokenization_Live_Panel

- Benchmark: `data/tokenization_live_panel_benchmark.json` · records=51 · median%=0.031506
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.TokenizationLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\tokenization_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/tokenization_cache.json
  - **unresolved**: desktop_dictionary — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Tokenization_Smoke

- Benchmark: `data/tokenization_smoke_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.TokenizationSmokePriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/tokenization/smoke_cases.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/tokenization/smoke_cases.json
  - **vendor_cache**: vendor/tokenization/vocab.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/tokenization/vocab.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Toxicology_Panel

- Benchmark: `data/toxicology_panel_benchmark.json` · records=21 · median%=0.033401
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.ToxicologyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### Trinary_Hardware_Live_Panel

- Benchmark: `data/trinary_hardware_live_panel_benchmark.json` · records=28 · median%=0.014767
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.TrinaryHardwareLivePanelPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\application_wiring\tier88_cache\trinary_hardware_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/application_wiring/tier88_cache/trinary_hardware_cache.json
  - **unresolved**: desktop_trinary_hardware — Named in panel source; add explicit public URL if this is an external authority
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### Trinary_Hardware_Motif

- Benchmark: `data/trinary_hardware_motif_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.TrinaryHardwareMotifPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/trinary_hardware/motif_influence_profile_stable.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_hardware/motif_influence_profile_stable.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Trinary_OS_Portable

- Benchmark: `data/trinary_os_portable_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.TrinaryOSPortablePriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus vendor/trinary_os — https://github.com/vendor/trinary_os
  - **dataset**: GitHub OSS corpus data/trinary_os_manifest.yaml — https://github.com/data/trinary_os_manifest.yaml
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Trinary_OS_Tier_E

- Benchmark: `data/trinary_os_tier_e_benchmark.json` · records=68 · median%=0.0
- Lean: `FSOT.Formal.TrinaryOSTierEPriors`
- Public / portable anchors:
  - **dataset**: GitHub OSS corpus vendor/trinary_os — https://github.com/vendor/trinary_os
  - **dataset**: GitHub OSS corpus data/trinary_os_portable_benchmark.json — https://github.com/data/trinary_os_portable_benchmark.json
  - **dataset**: GitHub OSS corpus data/trinary_os_isa_rebuild_benchmark.json — https://github.com/data/trinary_os_isa_rebuild_benchmark.json
  - **dataset**: GitHub OSS corpus data/trinary_os_round_trip_benchmark.json — https://github.com/data/trinary_os_round_trip_benchmark.json
  - **unresolved**: G:\FSOT-PublicData\trinary_os — Named in panel source; add explicit public URL if this is an external authority

### UAP_War_Gov_Release_Panel

- Benchmark: `data/uap_war_gov_release_panel_benchmark.json` · records=542 · median%=0.008488
- Ingest: `scripts/ingest_tier80_government_open_data.py`
- Lean: `FSOT.Formal.UapWarGovReleasePriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://www.war.gov/UFO/ — https://www.war.gov/UFO/
  - **ingest_script**: scripts/ingest_tier80_government_open_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier80_government_open_data.py

### Undiscovered_Element_Candidate_Prereg_Scaffold

- Benchmark: `data/undiscovered_element_candidate_prereg_scaffold_benchmark.json` · records=25 · median%=0.0
- Lean: `FSOT.Formal.UndiscoveredElementCandidatePreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### UniProt_Protein_Annotations

- Benchmark: `data/uniprot_protein_annotations_benchmark.json` · records=22 · median%=0.026684
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.UniprotProteinAnnotationsPriors`
- Public / portable anchors:
  - **api**: UniProt REST API — https://www.uniprot.org/help/api
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### UniProt_Structure_Annotations_Deep

- Benchmark: `data/uniprot_structure_annotations_deep_benchmark.json` · records=121 · median%=0.0
- Lean: `FSOT.Formal.UniProtStructureAnnotationsDeepPriors`
- Public / portable anchors:
  - **vendor_cache**: uniprot_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/uniprot_summary.json
  - **vendor_cache**: rcsb_pdb_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/rcsb_pdb_summary.json

### Unified_DB_Candidate_Crosswalk

- Benchmark: `data/unified_db_candidate_crosswalk_benchmark.json` · records=45 · median%=0.0
- Lean: `FSOT.Formal.UnifiedDBCandidateCrosswalkPriors`
- Public / portable anchors:
  - **vendor_cache**: fsot_aggregate_unified_db_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/fsot_aggregate_unified_db_benchmark.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **vendor_cache**: prediction_rederivation_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/prediction_rederivation_benchmark.json

### Unified_DB_Crosswalk_Spine

- Benchmark: `data/unified_db_crosswalk_spine_benchmark.json` · records=43 · median%=0.0
- Lean: `FSOT.Formal.UnifiedDBCrosswalkSpinePriors`
- Public / portable anchors:
  - **unresolved**: tier69_unified_db_panels — Named in panel source; add explicit public URL if this is an external authority

### VL_Agent_Distill_Panel

- Benchmark: `data/vl_agent_distill_panel_benchmark.json` · records=21 · median%=0.031506
- Ingest: `scripts/ingest_tier88_application_wiring.py`
- Lean: `FSOT.Formal.VlAgentDistillPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-2.1-Lean\vendor\application_wiring\tier88_cache\vl_agent_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-2.1-Lean/vendor/application_wiring/tier88_cache/vl_agent_cache.json
  - **unresolved**: desktop_vl_distill — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier88_application_wiring.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier88_application_wiring.py

### VL_Distill_Atlas

- Benchmark: `data/vl_distill_atlas_benchmark.json` · records=21 · median%=5.5479e-05
- Lean: `FSOT.Formal.VlDistillAtlasPriors`
- Public / portable anchors:
  - **vendor_cache**: vendor/vl_distill/fsot_atlas_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_atlas_summary.json
  - **vendor_cache**: vendor/vl_distill/fsot_domain_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_domain_registry.json
  - **vendor_cache**: vendor/vl_distill/distill_dataset.meta.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/distill_dataset.meta.json
  - **vendor_cache**: vendor/vl_distill/fsot_competitive_report.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/vl_distill/fsot_competitive_report.json
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: BRENDA enzyme database — https://www.brenda-enzymes.org/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: CRC / Riddick organic solvents handbook class — https://www.routledge.com/

### Virology

- Benchmark: `data/virology_extension_benchmark.json` · records=50 · median%=0.04593318440797614
- Lean: `FSOT.Formal.VirologyExtensionPriors`
- Public / portable anchors:
  - **unresolved**: virology_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: immunology — Named in panel source; add explicit public URL if this is an external authority
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **unresolved**: virology_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### Virology_Panel

- Benchmark: `data/virology_panel_benchmark.json` · records=24 · median%=0.000637597
- Ingest: `scripts/ingest_tier84_scientific_expansion.py`
- Lean: `FSOT.Formal.VirologyPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **api**: NCBI E-utilities / Gene / datasets — https://www.ncbi.nlm.nih.gov/books/NBK25501/
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier84_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier84_scientific_expansion.py

### VizieR_WDS_TAP_Live_Deep

- Benchmark: `data/vizier_wds_tap_live_deep_benchmark.json` · records=91 · median%=0.026954
- Ingest: `scripts/ingest_tier68_live_ingest.py`
- Lean: `FSOT.Formal.VizieRWdsTapLiveDeepPriors`
- Public / portable anchors:
  - **vendor_cache**: I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full\vendor\live_cache\tier68\vizier_wds_tap_live_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/vendor/live_cache/tier68/vizier_wds_tap_live_cache.json
  - **vendor_cache**: wds_live_multiplicity_deep_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/wds_live_multiplicity_deep_benchmark.json
  - **ingest_script**: scripts/ingest_tier68_live_ingest.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier68_live_ingest.py

### Volcanology_Panel

- Benchmark: `data/volcanology_panel_benchmark.json` · records=90 · median%=0.023502
- Ingest: `scripts/ingest_tier82_scientific_expansion.py`
- Lean: `FSOT.Formal.VolcanologyPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: GitHub OSS corpus USGS/GVP — https://github.com/USGS/GVP
  - **ingest_script**: scripts/ingest_tier82_scientific_expansion.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier82_scientific_expansion.py

### WDS_Live_Multiplicity_Deep

- Benchmark: `data/wds_live_multiplicity_deep_benchmark.json` · records=281 · median%=0.026954
- Ingest: `scripts/ingest_tier62_live_astrometry.py`
- Lean: `FSOT.Formal.WDSLiveMultiplicityDeepPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **ingest_script**: scripts/ingest_tier62_live_astrometry.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier62_live_astrometry.py

### Warp_BH_WH_Portal_Panel

- Benchmark: `data/warp_bh_wh_portal_benchmark.json` · records=23 · median%=0.0
- Lean: `FSOT.Formal.WarpBhWhPortalPriors`
- Public / portable anchors:
  - **vendor_cache**: C:\Users\damia\Desktop\FSOT-Legacy-Physics-Connections\concept_refinement\warp_actuation_formula_fsot21.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/C:/Users/damia/Desktop/FSOT-Legacy-Physics-Connections/concept_refinement/warp_actuation_formula_fsot21.json
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data

### World_Bank_Development

- Benchmark: `data/world_bank_development_benchmark.json` · records=395 · median%=0.02584
- Ingest: `scripts/ingest_tier38_public_data.py`
- Lean: `FSOT.Formal.WorldBankDevelopmentPriors`
- Public / portable anchors:
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **ingest_script**: scripts/ingest_tier38_public_data.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier38_public_data.py

### XR_Interactive_Media_Math_Scaffold

- Benchmark: `data/xr_interactive_media_math_scaffold_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.XRInteractiveMediaMathScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: openneuro_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/openneuro_summary.json

### Z120_Z126_Beam_Synthesis_Panel

- Benchmark: `data/z120_z126_beam_synthesis_panel_benchmark.json` · records=20 · median%=9.5e-05
- Lean: `FSOT.Formal.Z120Z126BeamSynthesisPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **vendor_cache**: heavy_ion_lab_synthesis_panel_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/heavy_ion_lab_synthesis_panel_benchmark.json

### Z164_Distant_Island_Prereg_Scaffold

- Benchmark: `data/z164_distant_island_prereg_scaffold_benchmark.json` · records=24 · median%=0.0
- Lean: `FSOT.Formal.Z164DistantIslandPreregScaffoldPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### Zebrafish_Cell_Tracking_Panel

- Benchmark: `data/zebrafish_cell_tracking_panel_benchmark.json` · records=20 · median%=0.022236
- Ingest: `scripts/ingest_tier95_zebrahub_development.py`
- Lean: `FSOT.Formal.ZebrafishCellTrackingPanelPriors`
- Public / portable anchors:
  - **unresolved**: zebrahub.sf.czbiohub.org — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: tier95_zebrahub_tracks_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier95_zebrahub_tracks_cache.json
  - **ingest_script**: scripts/ingest_tier95_zebrahub_development.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier95_zebrahub_development.py

### Zebrafish_Developmental_Mechanics_Panel

- Benchmark: `data/zebrafish_developmental_mechanics_panel_benchmark.json` · records=31 · median%=0.017789
- Ingest: `scripts/ingest_tier95_zebrahub_development.py`
- Lean: `FSOT.Formal.ZebrafishDevelopmentalMechanicsPanelPriors`
- Public / portable anchors:
  - **vendor_cache**: tier95_zebrahub_tracks_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier95_zebrahub_tracks_cache.json
  - **vendor_cache**: tier95_zebrahub_gpu_imaging_cache.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/tier95_zebrahub_gpu_imaging_cache.json
  - **ingest_script**: scripts/ingest_tier95_zebrahub_development.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier95_zebrahub_development.py

### Zebrafish_Longevity_Genetics_Coupling_Panel

- Benchmark: `data/zebrafish_longevity_genetics_coupling_panel_benchmark.json` · records=24 · median%=0.013342
- Ingest: `scripts/ingest_tier95_zebrahub_development.py`
- Lean: `FSOT.Formal.ZebrafishLongevityGeneticsCouplingPanelPriors`
- Public / portable anchors:
  - **unresolved**: tier94_longevity — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: tier95_zebrahub_tracks — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: Danio rerio — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **ingest_script**: scripts/ingest_tier95_zebrahub_development.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier95_zebrahub_development.py

### Zebrafish_Predictive_Validation_Panel

- Benchmark: `data/zebrafish_predictive_validation_panel_benchmark.json` · records=20 · median%=0.3579695
- Public / portable anchors:
  - **unresolved**: tier95_predictive_crossval — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_developmental_predict_lib — Named in panel source; add explicit public URL if this is an external authority

### Zero_Boundary_Not_Entity_Panel

- Benchmark: `data/zero_boundary_not_entity_panel_benchmark.json` · records=24 · median%=5.5479e-05
- Ingest: `scripts/ingest_tier91_foundational_ontology.py`
- Lean: `FSOT.Formal.ZeroBoundaryNotEntityPanelPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: positional_carry_theory — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution — https://www.routledge.com/
  - **literature**: Long & Greenwood (1997) — materials / thermoelectric class reference — https://ui.adsabs.harvard.edu/
  - **literature**: Snyder & Toberer, Nature Materials 7, 105 (2008) — https://doi.org/10.1038/nmat2090
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **literature**: Anderson (1966) — localization / condensed-matter classic — https://ui.adsabs.harvard.edu/
  - **literature**: Andersen et al., J. Phys. Chem. Ref. Data 28 (1999) — https://www.nist.gov/pml/journal-physical-and-chemical-reference-data
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **ingest_script**: scripts/ingest_tier91_foundational_ontology.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier91_foundational_ontology.py

### Zero_Day_Risk_Evaluator

- Benchmark: `data/zero_day_risk_evaluator_cybersecurity_benchmark.json` · records=25 · median%=0.010337117254355377
- Lean: `FSOT.Formal.ZeroDayRiskEvaluatorPriors`
- Public / portable anchors:
  - **unresolved**: zero_day_reference — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: tier_h_child_rollup — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: code_genome_holes — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: zero_day_evaluator_reference_observables — Named in panel source; add explicit public URL if this is an external authority
  - **vendor_cache**: cryptography_technology_cybersecurity_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/cryptography_technology_cybersecurity_benchmark.json
  - **vendor_cache**: network_internet_protocols_cybersecurity_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/network_internet_protocols_cybersecurity_benchmark.json
  - **vendor_cache**: malware_threat_intelligence_cybersecurity_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/malware_threat_intelligence_cybersecurity_benchmark.json
  - **vendor_cache**: secure_software_engineering_cybersecurity_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/secure_software_engineering_cybersecurity_benchmark.json
  - **vendor_cache**: code_genome_structure_cybersecurity_benchmark.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/code_genome_structure_cybersecurity_benchmark.json

### Zoology

- Benchmark: `data/zoology_extension_benchmark.json` · records=1000 · median%=0.01778900030815634
- Lean: `FSOT.Formal.ZoologyExtensionPriors`
- Public / portable anchors:
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/
  - **api**: GBIF Occurrence API — https://api.gbif.org/v1/

### biological_cuda_physarum_benchmark

- Benchmark: `data/biological_cuda_physarum_benchmark.json` · records=34 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/physarum/genome_data/cuda_benchmark_results.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/cuda_benchmark_results.json
  - **vendor_cache**: vendor/physarum/physarum_v5_states.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/physarum_v5_states.json
  - **vendor_cache**: vendor/physarum/genome_data/genomics_slime_mold_refined.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/genomics_slime_mold_refined.json
  - **vendor_cache**: vendor/physarum/genome_data/physarum_codon_weights.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/physarum/genome_data/physarum_codon_weights.json

### climate_observed_benchmark

- Benchmark: `data/climate_observed_benchmark.json` · records=17325 · median%=0.01201268326195996
- Public / portable anchors:
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: Planck Collaboration cosmological parameters — https://www.cosmos.esa.int/web/planck
  - **unresolved**: paleoclimate_reference_observables — Named in panel source; add explicit public URL if this is an external authority

### computational_reasoning_benchmark

- Benchmark: `data/computational_reasoning_benchmark.json` · records=577 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### cosmology_bubble_bleed_benchmark

- Benchmark: `data/cosmology_bubble_bleed_benchmark.json` · records=110 · median%=0.0
- Public / portable anchors:

### cryosphere_benchmark

- Benchmark: `data/cryosphere_benchmark.json` · records=2399 · median%=0.0
- Public / portable anchors:
  - **dataset**: NOAA NCEI climate data — https://www.ncei.noaa.gov/

### culinary_arts_benchmark

- Benchmark: `data/culinary_arts_benchmark.json` · records=52 · median%=0.047615187057821064
- Public / portable anchors:
  - **vendor_cache**: vendor/smiles/FSOT_SMILES_Lab_Dataset.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json
  - **dataset**: GitHub OSS corpus data/culinary_recipe_observables.json — https://github.com/data/culinary_recipe_observables.json
  - **unresolved**: smiles_food_chemistry — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: recipe_process — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: coffee_roast — Named in panel source; add explicit public URL if this is an external authority

### geochemistry_benchmark

- Benchmark: `data/geochemistry_benchmark.json` · records=153 · median%=0.006625234573930708
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: smiles_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: planetary_structure_lab — Named in panel source; add explicit public URL if this is an external authority

### geomagnetism_benchmark

- Benchmark: `data/geomagnetism_benchmark.json` · records=524 · median%=0.0
- Public / portable anchors:
  - **api**: NOAA tides, climate, space-weather open services — https://www.noaa.gov/

### grace_cryosphere_benchmark

- Benchmark: `data/grace_cryosphere_benchmark.json` · records=253 · median%=0.0
- Public / portable anchors:
  - **unresolved**: GFZ_GravIS_Greenland_total — Named in panel source; add explicit public URL if this is an external authority

### higgs_mass_benchmark

- Benchmark: `data/higgs_mass_benchmark.json` · records=9 · median%=0.018987449514135373
- Public / portable anchors:
  - **vendor_cache**: vendor/smiles/FSOT_SMILES_Lab_Dataset.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json
  - **dataset**: GitHub OSS corpus scripts/higgs_mass_formula_eval.py — https://github.com/scripts/higgs_mass_formula_eval.py
  - **dataset**: GitHub OSS corpus data/higgs_mass_reference_observables.json — https://github.com/data/higgs_mass_reference_observables.json
  - **dataset**: GitHub OSS corpus vendor/fsot_compute.py — https://github.com/vendor/fsot_compute.py

### hydrology_benchmark

- Benchmark: `data/hydrology_benchmark.json` · records=957 · median%=0.0
- Public / portable anchors:
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/
  - **dataset**: Particle Data Group Review of Particle Physics — https://pdg.lbl.gov/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **api**: World Bank Open Data Indicators API — https://api.worldbank.org/v2/
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/
  - **dataset**: NIST CODATA recommended values (ASCII table) — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
  - **api**: arXiv API / metadata — https://arxiv.org/help/api/
  - **dataset**: Minor Planet Center Orbit Database (MPCORB) — https://minorplanetcenter.net/data
  - **api**: PubChem PUG REST — https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
  - **dataset**: Planck Collaboration cosmological parameters — https://www.cosmos.esa.int/web/planck
  - **dataset**: Minor Planet Center data services — https://minorplanetcenter.net/

### iNaturalist_Observation_Panel

- Benchmark: `data/inaturalist_observation_panel_benchmark.json` · records=288 · median%=0.006006
- Ingest: `scripts/ingest_tier81_public_verifiable.py`
- Lean: `FSOT.Formal.InaturalistObservationPriors`
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **url**: https://api.inaturalist.org/ — https://api.inaturalist.org/
  - **ingest_script**: scripts/ingest_tier81_public_verifiable.py — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/ingest_tier81_public_verifiable.py

### igem_live_fasta_benchmark

- Benchmark: `data/igem_live_fasta_benchmark.json` · records=42 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/igem/igem_parts_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/igem_parts_registry.json
  - **vendor_cache**: vendor/igem/fastas — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/fastas

### igem_synthetic_biology_benchmark

- Benchmark: `data/igem_synthetic_biology_benchmark.json` · records=54 · median%=0.022236250385203583
- Public / portable anchors:
  - **vendor_cache**: vendor/igem/igem_parts_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/igem/igem_parts_registry.json
  - **dataset**: GitHub OSS corpus data/biology_strict_empirical.json — https://github.com/data/biology_strict_empirical.json
  - **api**: NCBI E-utilities / Gene / datasets — https://www.ncbi.nlm.nih.gov/books/NBK25501/

### immunology_benchmark

- Benchmark: `data/immunology_benchmark.json` · records=84 · median%=0.061205
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### intelligence_compression_benchmark

- Benchmark: `data/intelligence_compression_benchmark.json` · records=572 · median%=0.029066672228905688
- Public / portable anchors:
  - **unresolved**: fic_sensitivity_sweep — Named in panel source; add explicit public URL if this is an external authority

### magnetosphere_benchmark

- Benchmark: `data/magnetosphere_benchmark.json` · records=167 · median%=0.0
- Public / portable anchors:
  - **unresolved**: geomagnetism_x_space_weather_x_magnetic_string — Named in panel source; add explicit public URL if this is an external authority

### materials_engineering_benchmark

- Benchmark: `data/materials_engineering_benchmark.json` · records=87 · median%=0.027170334947435038
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### materials_species_bridge_benchmark

- Benchmark: `data/materials_species_bridge_benchmark.json` · records=34 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/smiles/FSOT_SMILES_Lab_Dataset.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/smiles/FSOT_SMILES_Lab_Dataset.json
  - **vendor_cache**: vendor/species/fsot_species_catalog.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/species/fsot_species_catalog.json

### math_generator_rules_eval_benchmark

- Benchmark: `data/math_generator_rules_eval_benchmark.json` · records=1552 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/math_generator/rules — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/math_generator/rules

### mathematics_computational_benchmark

- Benchmark: `data/mathematics_computational_benchmark.json` · records=20 · median%=1.4090183367935627e-14
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### multi_hero_benchmark

- Benchmark: `data/multi_hero_benchmark.json` · records=32 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor\neuron_cohort\cells.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/neuron_cohort/cells.json

### neuroimmunology_benchmark

- Benchmark: `data/neuroimmunology_benchmark.json` · records=92 · median%=0.05041956982053305
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **unresolved**: smiles_immunology — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: neuron_cohort_lab — Named in panel source; add explicit public URL if this is an external authority

### omni_theory_genesis_benchmark

- Benchmark: `data/omni_theory_genesis_benchmark.json` · records=26 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/omni_theory/analysis/genesis/genesis_per_verse_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/omni_theory/analysis/genesis/genesis_per_verse_summary.json

### oncology_benchmark

- Benchmark: `data/oncology_benchmark.json` · records=67 · median%=0.05041956982053305
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: smiles_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: biology_strict_lab — Named in panel source; add explicit public URL if this is an external authority

### orbital_mechanics_benchmark

- Benchmark: `data/orbital_mechanics_benchmark.json` · records=9 · median%=0.106141
- Public / portable anchors:
  - **api**: JPL Solar System Dynamics / Horizons — https://ssd.jpl.nasa.gov/

### pharmacology_benchmark

- Benchmark: `data/pharmacology_benchmark.json` · records=120 · median%=0.0011715432153059484
- Public / portable anchors:
  - **api**: ChEMBL API — https://www.ebi.ac.uk/chembl/

### planetary_atmospheres_benchmark

- Benchmark: `data/planetary_atmospheres_benchmark.json` · records=21 · median%=0.0
- Public / portable anchors:
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/
  - **api**: JPL Solar System Dynamics / Horizons — https://ssd.jpl.nasa.gov/
  - **api**: NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel) — https://api.nasa.gov/

### planetary_structure_benchmark

- Benchmark: `data/planetary_structure_benchmark.json` · records=20 · median%=0.0
- Public / portable anchors:
  - **api**: JPL Solar System Dynamics / Horizons — https://ssd.jpl.nasa.gov/

### quantum_materials_benchmark

- Benchmark: `data/quantum_materials_benchmark.json` · records=168 · median%=0.024318115591995593
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py

### rust_lean_bridge_benchmark

- Benchmark: `data/rust_lean_bridge_benchmark.json` · records=9 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/rust_lean_bridge/rust_lean_bridge_summary.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/rust_lean_bridge/rust_lean_bridge_summary.json

### seismology_benchmark

- Benchmark: `data/seismology_benchmark.json` · records=500 · median%=0.0
- Public / portable anchors:
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/

### seismology_deep_benchmark

- Benchmark: `data/seismology_deep_benchmark.json` · records=1000 · median%=0.0
- Public / portable anchors:
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/

### synthetic_biology_benchmark

- Benchmark: `data/synthetic_biology_benchmark.json` · records=20 · median%=0.0
- Public / portable anchors:
  - **software**: FSOT scalar authority (pin D1D38A) — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py
  - **dataset**: vendor/formula_corpus/by_domain/strict_empirical.jsonl — https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl
  - **unresolved**: evolution_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: biology_strict_lab — Named in panel source; add explicit public URL if this is an external authority
  - **unresolved**: fsot_biology_scalar — Named in panel source; add explicit public URL if this is an external authority
  - **dataset**: NIST CODATA / Constants — https://physics.nist.gov/cuu/Constants/

### tectonics_benchmark

- Benchmark: `data/tectonics_benchmark.json` · records=500 · median%=0.0
- Public / portable anchors:
  - **api**: USGS earthquake / water / hazards open APIs — https://earthquake.usgs.gov/fdsnws/event/1/

### trinary_os_isa_rebuild_benchmark

- Benchmark: `data/trinary_os_isa_rebuild_benchmark.json` · records=38 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/trinary_os/isa/fsotb_opcode_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/isa/fsotb_opcode_registry.json
  - **dataset**: GitHub OSS corpus vendor/trinary_os — https://github.com/vendor/trinary_os

### trinary_os_round_trip_benchmark

- Benchmark: `data/trinary_os_round_trip_benchmark.json` · records=22 · median%=0.0
- Public / portable anchors:
  - **vendor_cache**: vendor/trinary_os/isa/fsotb_opcode_registry.json — https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/trinary_os/isa/fsotb_opcode_registry.json
  - **dataset**: GitHub OSS corpus vendor/trinary_os — https://github.com/vendor/trinary_os

### weather_observed_benchmark

- Benchmark: `data/weather_observed_benchmark.json` · records=None · median%=0.0
- Public / portable anchors:
  - **api**: Open-Meteo weather API / archive — https://open-meteo.com/

## API registry (full list)

From `data/api_requirements.yaml` — live rebuild channels:

- `nist_codata` (tier38_public_apis): https://physics.nist.gov/cuu/Constants/Table/allascii.txt [auth=none]
- `gbif` (tier38_public_apis): https://api.gbif.org/v1/occurrence/search [auth=none]
- `noaa_tides` (tier38_public_apis): https://api.tidesandcurrents.noaa.gov/api/prod/datagetter [auth=none]
- `world_bank` (tier38_public_apis): https://api.worldbank.org/v2/country/{iso}/indicator/{id} [auth=none]
- `nasa_exoplanet` (tier38_public_apis): https://exoplanetarchive.ipac.caltech.edu/TAP/sync [auth=none]
- `rcsb_pdb` (tier38_public_apis): https://data.rcsb.org/rest/v1/core/entry/{pdb_id} [auth=none]
- `openalex` (tier38_public_apis): https://api.openalex.org/works [auth=none]
- `pubchem` (tier38_public_apis): https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight,CanonicalSMILES/JSON [auth=none]
- `cern_opendata` (tier38_public_apis): https://opendata.cern.ch/api/records/ [auth=none]
- `uniprot` (tier38_public_apis): https://rest.uniprot.org/uniprotkb/{accession}.json [auth=none]
- `jpl_horizons` (geophysics_space_weather): https://ssd.jpl.nasa.gov/api/horizons.api [auth=none]
- `gfz_kp` (geophysics_space_weather): https://www.gfz.de/en/sections/geomagnetism/data-products-and-services/indices/kp-index [auth=none]
- `kyoto_dst` (geophysics_space_weather): https://www.ngdc.noaa.gov/stp/space-weather/geomagnetic-data/INDICES/DST/ [auth=none]
- `swpc_geomagnetism` (geophysics_space_weather):  [auth=none]
- `usgs_earthquakes` (geophysics_space_weather): https://earthquake.usgs.gov/fdsnws/event/1/query [auth=none]
- `usgs_hydrology` (geophysics_space_weather):  [auth=none]
- `ncei_climate` (geophysics_space_weather): https://www.ncei.noaa.gov/cdo-web/api/v2/data [auth=API token via NCEI registration (optional for rebuild)]
- `ncbi_gene` (biology_genomics):  [auth=none]
- `igem_parts` (biology_genomics): https://parts.igem.org/fasta/parts/{part_id} [auth=none]
- `openneuro` (biology_genomics): https://openneuro.org/crn/graphql [auth=none]
- `anage` (biology_genomics): https://genomics.senescence.info/species/dataset.zip [auth=none]
- `paleobiodb` (tier_f_gaps): https://paleobiodb.org/data1.2/occs/list.json [auth=none]
- `obis` (tier_f_gaps): https://api.obis.org/v3/occurrence [auth=none]
- `gbif_tier_f` (tier_f_gaps): https://api.gbif.org/v1/occurrence/search [auth=none]
- `malwarebazaar` (cybersecurity): https://bazaar.abuse.ch/export/csv/recent/ [auth=none]
- `cisa_kev` (cybersecurity): https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json [auth=none]
- `simbad_tap` (astrophysics_catalogs): http://simbad.cds.unistra.fr/simbad/sim-tap/sync [auth=none]
- `vizier_wds` (astrophysics_catalogs): https://cdsarc.cds.unistra.fr/viz-bin/votable [auth=none]
- `gaia_dr3_tap` (astrophysics_catalogs): https://gea.esac.esa.int/tap-server/tap/sync [auth=none]
- `gwosc` (astrophysics_catalogs): https://www.gw-openscience.org/eventapi/json/ [auth=none]
- `nasa_exoplanet_tap` (astrophysics_catalogs): https://exoplanetarchive.ipac.caltech.edu/TAP/sync [auth=none]
- `stsci_mast` (astrophysics_catalogs): https://mast.stsci.edu/api/v0/invoke [auth=none]
- `open_meteo` (misc): https://archive-api.open-meteo.com/v1/archive [auth=none]
- `chime_frb` (misc):  [auth=none]
- `sh0es_github` (misc): https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main [auth=none]
- `github_raw_oss` (misc):  [auth=Optional GITHUB_TOKEN for rate limits]

## Open science no-key probes

From `scripts/open_science_sources_lib.py`:

- `openfda_drug_label`: FDA open drug labeling records — https://api.fda.gov/drug/label.json?limit=5
- `ensembl_brca2`: Ensembl gene lookup (BRCA2) — https://rest.ensembl.org/lookup/id/ENSG00000139618?content-type=application/json
- `gwas_catalog_studies`: GWAS Catalog studies (EBI) — https://www.ebi.ac.uk/gwas/rest/api/studies?size=5
- `chembl_aspirin`: ChEMBL molecule record (aspirin) — https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json
- `usgs_earthquakes_recent`: USGS FDSN recent M≥4.5 events — https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=20&orderby=time&minmagnitude=4.5
- `wikidata_pi`: Wikidata entity for π — https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q167&format=json
- `owid_co2_codebook`: Our World in Data CO2 codebook (GitHub raw) — https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv
- `zenodo_records_physics`: Zenodo open research records (physics) — https://zenodo.org/api/records/?q=subject:physics&size=3&sort=mostrecent
- `alphafold_p53`: AlphaFold DB prediction metadata (P53) — https://alphafold.ebi.ac.uk/api/prediction/P04637
- `rcsb_1crn`: RCSB PDB entry 1CRN — https://data.rcsb.org/rest/v1/core/entry/1CRN
- `nasa_donki_flares`: NASA DONKI solar flare events (no key) — https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=2024-06-01&endDate=2024-06-14
- `openalex_works_cosmology`: OpenAlex scholarly works (no key) — https://api.openalex.org/works?search=cosmology&per_page=3
- `pubmed_esearch_hubble`: NCBI PubMed eSearch (open eutils) — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Hubble+tension&retmode=json&retmax=5
- `crossref_funders`: Crossref funders (open) — https://api.crossref.org/funders?query=national+science+foundation&rows=3
- `worldbank_population`: World Bank population indicator — https://api.worldbank.org/v2/country/USA/indicator/SP.POP.TOTL?format=json&per_page=5
- `nist_codata_ascii`: NIST CODATA constants table — https://physics.nist.gov/cuu/Constants/Table/allascii.txt
- `gbif_occurrence_sample`: GBIF occurrence search sample — https://api.gbif.org/v1/occurrence/search?limit=5&hasCoordinate=true
- `stringdb_version`: STRING protein network API version — https://string-db.org/api/json/version
- `pubchem_cid_2244`: PubChem aspirin (CID 2244) properties — https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularWeight,IUPACName,CanonicalSMILES/JSON
- `cern_opendata_records`: CERN Open Data records search — https://opendata.cern.ch/api/records/?q=collision&size=3

## Regenerate

```powershell
python scripts/build_benchmark_anchor_citation_ledger.py
python scripts/run_cross_proof_verification.py
```

Machine JSON: [`data/benchmark_anchor_citation_ledger.json`](../data/benchmark_anchor_citation_ledger.json)  
BibTeX: [`data/domain_citations/benchmark_public_anchors.bib`](../data/domain_citations/benchmark_public_anchors.bib)
