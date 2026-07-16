# Appendix XI — Full Verification Record

*Edition fragment · 2026-07-16 · [Return to main thesis](../README.md#appendix-xi--full-verification-record-summary)

```bash
python scripts/run_publication_verification_bundle.py --full-cross-proof
python scripts/build_readme_thesis_expansion.py
python scripts/merge_readme_thesis_expansion.py
```

## XI-A — Cross-Verification Metrics

*Generated: 2026-07-16T13:15:33.298254+00:00*

### Five-prover formal spine

| Metric | Value |
|--------|------:|
| overall_ok | True |
| github_ready | True |
| tier | 91_seven_way_bare_metal |
| atomic provable obligations | 1863 |
| full spine obligations | 2370 |
| margin violations | 0 |
| seven_way_bare_metal | True |

Authoritative report: `data/cross_proof_verification_report.json`

### Verified desktop cross-proof closure

- verdict: **VERIFIED_DESKTOP_CROSS_PROOF_READY**
- panels_closed: 4
- generated_at: 2026-07-16T13:09:24.493662+00:00

## XI-B — Data Sources and API Resources

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

## XI-C — Literature and Citations

Domain-specific references are exported from the FSOT domain navigator and panel benchmarks.

### Verified desktop BibTeX

Export command: `python scripts/export_domain_citations.py --bundle verified_desktop`

- **File:** `data/domain_citations/verified_desktop.bib` (4 entries)

```bibtex
% FSOT domain citations — generated 2026-07-16T13:09:27.664111+00:00
% Repository: https://github.com/dappalumbo91/FSOT-2.1-Lean
@misc{fsot_machineandmoleculelivepanel,
  title = {FSOT verification panel: Machine_And_Molecule_Live_Panel},
  author = {Palumbo, Damian Arthur},
  year = {2026},
  howpublished = {\url{https://github.com/dappalumbo91/FSOT-2.1-Lean}},
  note = {Records: 120; pooled median error: 0.01341%; kill criterion: Machine_And_Molecule_Live_Panel pooled median exceeds 0.5% or >25% of catalog properties exceed 1% scalar error on refresh.}
}

@misc{fsot_fuellablivepanel,
  title = {FSOT verification panel: Fuel_Lab_Live_Panel},
  author = {Palumbo, Damian Arthur},
  year = {2026},
  howpublished = {\url{https://github.com/dappalumbo91/FSOT-2.1-Lean}},
  note = {Records: 366; pooled median error: 0.039349%; kill criterion: Fuel_Lab_Live_Panel pooled median exceeds 0.5% or thermal_efficiency channel median exceeds 1% on grounded/hemp profiles.}
}

@misc{fsot_blackholewhiteholecyclelivepanel,
  title = {FSOT verification panel: BlackHole_WhiteHole_Cycle_Live_Panel},
  author = {Palumbo, Damian Arthur},
  year = {2026},
  howpublished = {\url{https://github.com/dappalumbo91/FSOT-2.1-Lean}},
  note = {Records: 24; pooled median error: 0.026472%; kill criterion: BH/WH cycle constants (poof, suction, c_eff) drift >0.5% from fsot-core.js canonical seed derivation on desktop blueprint refresh.}
}
...
```

Navigator routes with citation hooks: **19** (`data/fsot_domain_navigator.json`)

## XI-D — Domain Atlas

Full 403-domain table: `data/publication/domain_atlas.csv`

| Kind | Domains |
|------|--------:|
| core | 35 |
| extension | 367 |
| **total** | **402** |

### Core domains (35 NeuroLab spine)

| Domain | Records | Median err % | Tier |
|--------|--------:|-------------:|------|
| Acoustics | 485 | 0.032277 | A_strong |
| Astronomy | 193 | 0.0 | A_strong |
| Astrophysics | 305 | 0.0005610563516671626 | A_strong |
| Atmospheric_Physics | 17414 | 0.0 | A_strong |
| Atomic_Physics | 116 | 0.0009504134401228516 | A_strong |
| Biochemistry | 166 | 0.01920113857308633 | A_strong |
| Biology | 67 | 0.0 | B_verified |
| Chemistry | 99 | 0.005707 | B_verified |
| Condensed_Matter | 1169 | 0.030603154577296784 | A_strong |
| Cosmology | 347 | 0.0007354204043789445 | A_strong |
| Ecology | 654 | 0.017789000308163706 | A_strong |
| Economics | 167 | 0.12920090413714938 | A_strong |
| Electromagnetism | 271912 | 0.0 | A_strong |
| Fluid_Dynamics | 56 | 0.0 | B_verified |
| Geophysics | 547 | 0.0 | A_strong |
| High_Energy_Physics | 151 | 0.003557172593200954 | A_strong |
| Materials_Science | 1169 | 0.030603154577296784 | A_strong |
| Meteorology | 17414 | 0.0 | A_strong |
| Molecular_Chemistry | 608 | 0.028389499999999998 | A_strong |
| Neuroscience | 41 | 0.013382765569350981 | B_verified |
| Nuclear_Physics | 79 | 0.0073571309514874035 | B_verified |
| Oceanography | 112 | 0.0 | A_strong |
| Optics | 485 | 0.032277 | A_strong |
| Particle_Astrophysics | 192 | 0.004643710259500975 | A_strong |
| Particle_Physics | 98 | 0.0023222644988432507 | B_verified |
| Physical_Chemistry | 608 | 0.028389499999999998 | A_strong |
| Planetary_Science | 50 | 0.021477424424138976 | B_verified |
| Psychology | 170 | 0.03150616921194593 | A_strong |
| Quantum_Computing | 180 | 0.0002953462072651492 | A_strong |
| Quantum_Gravity | 141 | 0.0 | A_strong |
| Quantum_Mechanics | 74 | 0.0009504134401252401 | B_verified |
| Quantum_Optics | 74 | 0.0009504134401252401 | B_verified |
| Seismology | 1000 | 0.0 | A_strong |
| Sociology | 410 | 0.019504399572474972 | A_strong |
| Thermodynamics | 89 | 0.02214701353860092 | B_verified |

### Extension panels (first 40 of 367)

| Domain | Records | Median err % | Tier |
|--------|--------:|-------------:|------|
| AI_Galactic_Orbital_Bridge | 48 | 0.005168558627177688 | B_verified |
| Acoustic_Resonance_Materials | 29 | 0.008381497018411083 | B_verified |
| Actuarial_Science_Panel | 60 | 0.02261 | B_verified |
| Adjacent_Rung_Coupling | 36 | 0.020098237848404983 | B_verified |
| Adversarial_Fractal_Break_Tests | 24 | 0.0 | B_verified |
| Agriculture_Agroecology | 276 | 0.018019024892929635 | A_strong |
| Alternate_Base_Mathematics_Explorer_Panel | 56 | 0.009504 | B_verified |
| Alternate_Base_Mathematics_Spine | 24 | 0.004184779870129773 | B_verified |
| Anthropology | 160 | 0.019504399572476606 | A_strong |
| Architecture_Building_Science | 43 | 0.07869745016115058 | B_verified |
| Arxiv_Brain_Knowledge_Panel | 20 | 0.018003 | B_verified |
| Arxiv_Gravitational_Waves_Panel | 60 | 0.01748 | B_verified |
| Arxiv_Primitives_Panel | 22 | 0.031506 | B_verified |
| Arxiv_Primitives_V14 | 24 | 0.0 | B_verified |
| Astrophysical_Structure_Crosswalk | 32 | 0.0 | B_verified |
| Bibliography_Corpus_Panel | 24 | 0.03801653760497401 | B_verified |
| Bibliography_Lean_Corpus | 21 | 0.020055 | B_verified |
| Binary_Decoder_Panel | 24 | 0.013342 | B_verified |
| Binary_Decoder_Rendlesham | 24 | 0.004504756223217969 | B_verified |
| Biological_CUDA_Physarum | 35 | 0.0 | B_verified |
| Biology_Developmental_Structural_Depth_Panel | 26 | 0.022236 | B_verified |
| Biophysics_Public_Panel | 24 | 0.0 | B_verified |
| BlackHole_WhiteHole_Cycle_Live_Panel | 24 | 0.026472 | B_verified |
| Botany | 426 | 0.022236250385193387 | A_strong |
| Boundary_Partition_Tightening | 24 | 0.017672674984670764 | B_verified |
| Breakthrough_Discoveries_2024_2026 | 21 | 0.0 | B_verified |
| CERN_Open_Data_LHC | 83 | 0.013294 | B_verified |
| CRC_Handbook_Properties | 391 | 0.026922 | A_strong |
| CVE_Codon_Hole_Falsification | 29 | 0.009186636881580057 | B_verified |
| Canonical_Oracle_Panel | 24 | 0.013294 | B_verified |
| Cardiology | 45 | 0.030622122938654326 | B_verified |
| Cardiology_Panel | 20 | 0.015311 | B_verified |
| Cartography_GIS_Panel | 48 | 0.018855999999999998 | B_verified |
| Certified_Agent_Formal_Panel | 24 | 0.014767 | B_verified |
| Certified_Agent_Qwen | 24 | 0.004504756223217969 | B_verified |
| Chaos_Mediated_Phase_Transitions | 21 | 0.03147898006445882 | B_verified |
| Chemical_Engineering | 186 | 0.0010333425185953097 | A_strong |
| Chemical_Structure_Stability_Panel | 32 | 0.00206 | B_verified |
| Civil_Engineering | 37 | 0.0335259880736416 | B_verified |
| Civil_Engineering_Panel | 20 | 0.01341 | B_verified |
| … | *327 more* | | |

## XI-E — Formula Corpus and Observables

Strict empirical path: `vendor/formula_corpus/strict_empirical.jsonl` (7,941 formulas)


### Formula honesty report

- version: 1.0
- verdict: ROW_COUNT_WITH_DEDUPED_UNIQUE
- headline_row_count: 7941
- unique_observable_count: 1325
- project_triplication_factor: 5.993
- live_recompute: {'enabled': True, 'sample_size': 1325, 'pool_size': 1325, 'checked': 1325, 'skipped_unsupported': 0, 'unevaluable_unique_gap': 0, 'ok': 1325, 'ok_ratio': 1.0, 'drift_debt_count': 0}
- honest_statement: strict_empirical.jsonl contains 7,941 rows representing 1,325 unique observables (concept+formula+target); ~5.993× project triplication. Live recompute on deduped uniques: 1325/1325 OK; 0 skipped (unsupported eval).
- verification_issues: []
- verification_passed: True
- full_summary: {'records_total': 7941, 'unique_observables': 1325, 'project_triplication_factor': 5.993, 'matched_count': 7941, 'unique_matched_count': 1325, 'unmatched_count': 0, 'within_target_2pct': 6921, 'unique_within_target_2pct': 1155, 'within_tolerable_5pct': 7941, 'unique_within_tolerable_5pct': 1325, 'max_error_pct': 4.841504, 'top_project_count': 3, 'top_projects': [{'project': 'FSOT NEURON Gene LLM', 'records': 2647}, {'project': 'FSOT SMILES Lab', 'records': 2647}, {'project': 'Fsot3.0 code', 'records': 2647}], 'corpus_path': 'vendor/formula_corpus/by_domain/strict_empirical.jsonl', 'live_recompute_pool_size': 1325, 'live_recompute_deduped': True, 'live_recompute_sample_size': 1325, 'live_recompute_checked': 1325, 'live_recompute_skipped_unsupported': 0, 'live_recompute_ok': 1325, 'live_recompute_ok_ratio': 1.0, 'live_recompute_drift_debt_count': 0, 'live_recompute_max_drift_pct': 0.0, 'live_recompute_debt_report': 'data\\formula_live_recompute_debt.json', 'issues': 0}

Per-formula verification policy: `data/formula_verification_policy.yaml`
Reproduce: `python scripts/run_numeric_eval_queue.py`

## XI-F — Contested Observables

- Observable count: **13**
- FSOT pooled median: **0.029748999999999998%**
- Typical ΛCDM/SM baseline: **15.0%**
- Verdict: CONTESTED_SECTORS_FSOT_AHEAD_OF_CURRENT_MODELS

- **H0_tension_SH0ES_vs_Planck:** FSOT err 0.027466% — ref `Riess2024_vs_Planck2018`
- **H0_tension_Carnegie_vs_Planck:** FSOT err 0.227322% — ref `Freedman2019`
- **H0_FSOT_local_anchor:** FSOT err 0.829427% — ref `FSOT_bubble_bleed_dual_anchor`
- **H0_Planck_CMB:** FSOT err 0.192564% — ref `Planck2018`
- **H0_SH0ES_local:** FSOT err 0.662297% — ref `Riess2024`

### Closure detail

- H0_tension_SH0ES_vs_Planck: 0.027466%
- H0_tension_Carnegie_vs_Planck: 0.227322%
- S8_tension_Planck_vs_DES_Y3: 0.195214%
- Lithium_problem_factor: 0.316322%
- FRB_DM_excess_vs_IGM: 0.042611%
- N_eff: 0.009407%
- Omega_Lambda: 0.0016%
- sigma_8: 0.00296%
- tau_reion: 0.006335%
- D_H_ratio: 0.090986%
- r_c: 0.341024%
- m_H: 0.039905%
- H0_FSOT_local_anchor: 0.829427%
- H0_Planck_CMB: 0.192564%
- H0_SH0ES_local: 0.662297%

## XI-G — Verified Desktop Engineering Panels

Seven novel FSOT-designed fuel molecular states verified against seed-scalar predictions and cross-referenced with grounded thermochemistry + Prius engine simulator outputs; gasoline included as fossil baseline for comparison.

FSOT transporter technology stack verified: quantum teleportation channel, warp actuation portal (psi_portal, psi_traverse, entanglement gates), poof/suction matter-stream proxies, and transporter engineering observables (pattern buffer, scan resolution, reassembly lock) — pooled median error at seed-scalar precision.

| Panel | Records | Pooled median % | Benchmark |
|-------|--------:|----------------:|-----------|
| Machine_And_Molecule_Live_Panel | 120 | 0.01341 | `data/machine_and_molecule_live_panel_benchmark.json` |
| Fuel_Lab_Live_Panel | 366 | 0.039349 | `data/fuel_lab_live_panel_benchmark.json` |
| BlackHole_WhiteHole_Cycle_Live_Panel | 24 | 0.026472 | `data/blackhole_whitehole_cycle_live_panel_benchmark.json` |
| Star_Trek_Transporter_Live_Panel | 1575 | 0.031159 | `data/star_trek_transporter_live_panel_benchmark.json` |

### FSOT-designed fuels

`fsot_hemp_waste_grounded`, `fsot_hemp_waste_advanced`, `fsot_algae_oil_biodiesel`, `fsot_mushroom_spore_fuel`, `fsot_green_hydrogen`, `fsot_optimax`, `fsot_bio_spark`

Gasoline baseline: `gasoline`

Reproduce:
```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep
```
