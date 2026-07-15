## Data Sources and API Resources (auto-generated)

Portable clone-and-verify uses bundled `vendor/` caches. Full live rebuild requires network.

### Software requirements

- **Lean:** `leanprover/lean4:v4.31.0` — verify with `lake build`
- **Python:** ≥3.10

### Bundled authority paths

- **fsot_compute:** `vendor/fsot_compute.py` — canonical numeric oracle for constants, wave1, and domain scalars
- **smiles_dataset:** `vendor/smiles/FSOT_SMILES_Lab_Dataset.json` — SMILES Lab catalog for chemical/medical domain benchmarks
- **evolution_operons:** `vendor/evolution/biological_mt_operons.json` — mitochondrial operon source for evolution and synthetic biology bridges
- **linguistics_targets:** `vendor/linguistics/data/LINGUISTIC_TARGETS.csv` — measured linguistic anchors for consciousness-domain bridge
- **linguistics_derivations:** `vendor/linguistics/linguistics_derivations.json` — portable FSOT derivation snapshot (replaces 400MB SQLite for GitHub)
- **math_generator_comparison:** `vendor/math_generator/generated_formula_comparison_report.json` — cross-domain FSOT formula comparisons for mathematics computational tier
- **math_generator_rules:** `vendor/math_generator/rules` — 61 corpora / 1520 formal rules for per-rule eval tier
- **trinary_os_oracles:** `vendor/trinary_os/target` — FSOTB regression oracles for portable Trinary-OS coding rebuild
- **species_catalog:** `vendor/species/fsot_species_catalog.json` — Machine & Molecule metals/molecules/polymers for species bridge
- **igem_parts_registry:** `vendor/igem/igem_parts_registry.json` — iGEM Registry standard parts for synthetic biology strict-empirical bridge
- **reference_anchors:** `vendor/reference_anchors` — PDG / CRC / NIST DLMF first-class benchmark source manifests
- **fsot_unified_db:** `vendor/fsot_aggregate/FSOT_UNIFIED.db` — SQLite strict-empirical / numeric eval queue (portable verification)
- **neuron_cohort_cells:** `vendor/neuron_cohort/cells.json` — Allen cell-types catalog for experiment synthesis / cohort verification
- **knowledge_base_portable:** `vendor/knowledge_base/kb_portable_summary.json` — Portable KB counts + strict-empirical bridge (full transfer on Desktop)
- **math_generator_benchmark_reports:** `vendor/math_generator/benchmark_reports` — FSOT overlay benchmark reports (H0, airfoil, chemistry) for live formula eval
- **trinary_os_isa_registry:** `vendor/trinary_os/isa/fsotb_opcode_registry.json` — FSOTB v1/v1.1/v1.2 opcode table for portable ISA rebuild verification
- **igem_fastas:** `vendor/igem/fastas` — bundled iGEM FASTA cache when parts.igem.org API is blocked
- **airfoil_dataset:** `vendor/math_generator/datasets/airfoil_self_noise.csv` — airfoil aeroacoustics CSV for FO-210 benchmark_formula RMSE recompute
- **trinary_os_fixtures:** `vendor/trinary_os/fixtures` — canonical hello/call_ret/spawn_join .fsa fixtures for round-trip smoke
- **trinary_os_round_trip:** `vendor/trinary_os/round_trip` — byte-identical FSOTB pass-1/pass-2 round-trip oracle pairs
- **linguistics_derivations_json:** `vendor/linguistics/linguistics_derivations.json` — portable linguistics derivation snapshot (replaces SQLite for GitHub)
- **tokenization_smoke:** `vendor/tokenization` — Dictionary universal-tokenizer smoke cases and vocab registry
- **trinary_hardware_motif:** `vendor/trinary_hardware/motif_influence_profile_stable.json` — cube-block trinary hardware motif tuning profile
- **intrinsic_llm_validators:** `vendor/intrinsic_llm/benchmark_results_final.json` — intrinsic LLM validator multi-topic accuracy tiers
- **biological_cuda_physarum:** `vendor/physarum` — Physarum CUDA benchmarks, v5 plasmodium state, genomics + codon weights
- **arxiv_primitives_v14:** `vendor/arxiv_primitives/v14_run_summary.json` — Loop V14 arXiv topic ingest and six-primitive signature summary
- **formula_corpus_cnc:** `vendor/formula_corpus_cnc` — compiled formula corpus stats, validator delta, chem gauntlet report
- **binary_decoder_rendlesham:** `vendor/binary_decoder/rendlesham_page14_trace.json` — Rendlesham hidden-state trace CORE/FRAGMENTED branching summary
- **certified_agent_qwen:** `vendor/certified_agent` — Qwen 3VL formal env workspace + certified protocol summary
- **omni_theory_genesis:** `vendor/omni_theory/analysis/genesis/genesis_per_verse_summary.json` — Genesis ch.1 per-verse FSOT scalar humanities crosswalk
- **formula_corpus_strict_empirical:** `vendor/formula_corpus/by_domain/strict_empirical.jsonl` — 7,941 strict-empirical per-formula observable verification corpus
- **fsot_aggregate_unified_db:** `vendor/fsot_aggregate/FSOT_Mathematical_Database_Unified.json` — portable aggregate unified mathematical database (1532 rows)
- **thesis_waves:** `vendor/thesis` — bundled wave7–10 observations + intrinsic screens for particle/cosmology thesis labs
- **cosmology_skeleton_database:** `vendor/cosmology/database/FSOT_Mathematical_Database_Unified.json` — Cosmic Skeleton Key DB with 24 cosmology derivations for extended cosmology tier
- **prediction_rederivation_summary:** `vendor/fsot_aggregate/prediction_rederivation_summary.json` — 66-prediction re-derivation arc summary (zero free parameters)
- **vl_distill_atlas:** `vendor/vl_distill` — VL distill atlas summary, domain registry, dataset meta, competitive report
- **rust_lean_bridge:** `vendor/rust_lean_bridge` — Rust no_std bare-metal kernel + Lean bridge summary
- **bibliography_corpus:** `vendor/bibliography_corpus` — FSOT Bibliography axiomatic Lean corpus + parsed summary
- **tier38_public_data:** `vendor/public_data` — Tier 38 public API summaries (NIST, GBIF, NOAA, World Bank, NASA, RCSB, OpenAlex, PubChem, CERN, UniProt)
- **tier39_propulsion_electrical:** `vendor/propulsion_electrical` — Tier 39 space propulsion, electrical power, HVAC thermal, 2024-2026 breakthroughs
- **cybersecurity_public_data:** `vendor/cybersecurity` — MalwareBazaar + CISA KEV portable summaries; full ingest on external cache
- **space_weather_full_arc:** `data/space_weather_summary_benchmark.json` — Portable Kp summary (501 records); full 271813-record arc on external cache
- **cross_scale_bridges:** `data/orbital_bridge_scientific_framing.yaml` — Cross-scale self-similarity index + NASA exoplanet sample on external cache only
- **compactification_ladder:** `data/compactification_ladder_manifest.yaml` — 10-rung folding ladder index + adjacent coupling + fold-depth summary on external cache
- **evolution_best_organism:** `vendor/evolution/best_evolved_organism.json` — best evolved organism metrics for evolution lab verification
- **stellar_structures_catalog:** `vendor/stellar_structures/public_multiplicity_catalog.json` — Tier 52 public binary/trinary star and GW event anchors (WDS/literature/LIGO public)

### External API tiers (sample)

#### tier38_public_apis
- Ingest: `scripts/ingest_tier38_public_data.py`
- Build: `scripts/build_tier38_public_data_benchmarks.py`
- `nist_codata`: https://physics.nist.gov/cuu/Constants/Table/allascii.txt
- `gbif`: https://api.gbif.org/v1/occurrence/search
- `noaa_tides`: https://api.tidesandcurrents.noaa.gov/api/prod/datagetter
- `world_bank`: https://api.worldbank.org/v2/country/{iso}/indicator/{id}
- `nasa_exoplanet`: https://exoplanetarchive.ipac.caltech.edu/TAP/sync
- `rcsb_pdb`: https://data.rcsb.org/rest/v1/core/entry/{pdb_id}

#### geophysics_space_weather
- `jpl_horizons`: https://ssd.jpl.nasa.gov/api/horizons.api
- `gfz_kp`: https://www.gfz.de/en/sections/geomagnetism/data-products-and-services/indices/kp-index
- `kyoto_dst`: https://www.ngdc.noaa.gov/stp/space-weather/geomagnetic-data/INDICES/DST/
- `swpc_geomagnetism`: 
- `usgs_earthquakes`: https://earthquake.usgs.gov/fdsnws/event/1/query
- `usgs_hydrology`: 

#### biology_genomics
- `ncbi_gene`: 
- `igem_parts`: https://parts.igem.org/fasta/parts/{part_id}
- `openneuro`: https://openneuro.org/crn/graphql
- `anage`: https://genomics.senescence.info/species/dataset.zip

#### tier_f_gaps
- `paleobiodb`: https://paleobiodb.org/data1.2/occs/list.json
- `obis`: https://api.obis.org/v3/occurrence
- `gbif_tier_f`: https://api.gbif.org/v1/occurrence/search

#### cybersecurity
- `malwarebazaar`: https://bazaar.abuse.ch/export/csv/recent/
- `cisa_kev`: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

#### tier53_56_expansion
- Build: `['scripts/build_tier53_stellar_galactic_benchmarks.py', 'scripts/build_tier54_planetary_solar_benchmarks.py', 'scripts/build_tier55_chemistry_materials_benchmarks.py', 'scripts/build_tier56_genetics_benchmarks.py']`

#### tier57_58_expansion
- Ingest: `scripts/ingest_tier58_live_catalogs.py`
- Build: `['scripts/build_tier57_interdisciplinary_benchmarks.py', 'scripts/build_tier58_live_catalog_benchmarks.py']`

#### tier59_60_expansion
- Ingest: `scripts/ingest_tier60_live_astrometry.py`
- Build: `['scripts/build_tier59_material_fuel_benchmarks.py', 'scripts/build_tier60_astrometry_benchmarks.py']`

Full registry: `data/api_requirements.yaml`, `data/external_data_manifest.yaml`
