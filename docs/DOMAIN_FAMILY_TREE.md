# Domain family tree — folds, subdomains, between-scale gaps

**Generated:** `2026-08-24T23:35:38.830813+00:00` · pin **D1D38A**  
**Regenerate:** `python scripts/build_domain_family_tree.py`

This is a **directory of slices**, not 400 theories. Reality is one 25-D fluid
([`CONCEPTS.md`](CONCEPTS.md) C8). A domain is a `(D_eff, observed)` interface.
An extension is a subdomain of a slice. A gap is a **missing interconnect**
between slices (`κ_ij`), not a missing spring constant.

Core folds **35** · extension subdomains **375** · atlas named rows **403**.
Green-file count stays in [`CURRENT_STATUS.md`](CURRENT_STATUS.md) (do not mix ledgers:
[`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md)).

## How to read this

| You want… | Look at |
|-----------|---------|
| The engine | `vendor/fsot_compute.py` `DOMAINS` |
| Picture | [`CONCEPTS.md`](CONCEPTS.md) C1–C13 · [`FOUNDING_ARCHIVE_VIEW.md`](FOUNDING_ARCHIVE_VIEW.md) |
| Apply without LSQ | [`APPLY.md`](APPLY.md) |
| Hubble is not one number | C3 — structure + bubble, not a 60° RA silo |

## The tree (core folds by compactification depth)

Extension columns attach by **nearest \(D_{\mathrm{eff}}\)**, not by Lean name.
Machine map: `data/domain_family_tree.json`.

### D = 5–8 — micro / bond / observer-on

Particle, QM, chemistry — form at the small orifice.

| Core fold | D_eff | observed | Extension subdomains (nearest D) |
|-----------|------:|:--------:|----------------------------------|
| **Particle_Physics** | 5 | yes | — |
| **Quantum_Mechanics** | 6 | yes | — |
| **Atomic_Physics** | 7 | yes | NIST_CODATA_Constants, Neutrino_Physics_Panel |
| **High_Energy_Physics** | 7 | yes | — |
| **Chemistry** | 8 | yes | Rust_Lean_Bridge, PubChem_Compound_Properties, Information_Theory_Public_Panel, Founding_Quantum_Vacuum_Panel |
| **Physical_Chemistry** | 8 | yes | — |

### D = 9–11 — look / compute / sound

EM, optics, acoustics; QC stays dark on purpose.

| Core fold | D_eff | observed | Extension subdomains (nearest D) |
|-----------|------:|:--------:|----------------------------------|
| **Electromagnetism** | 9 | yes | Electrical_Power_Systems, Periodic_Table_Public_Panel, PDG_Particle_Properties |
| **Molecular_Chemistry** | 9 | yes | — |
| **Acoustics** | 10 | yes | Music_Harmonics_Public_Panel, Superheavy_Element_Stability_Panel, Undiscovered_Element_Candidate_Prereg_Scaffold, Founding_Cosmic_Ray_Panel |
| **Materials_Science** | 10 | yes | — |
| **Optics** | 10 | yes | — |
| **Quantum_Computing** | 11 | dark | Semiconductor_Physics_Public_Panel, Quantum_Information, Natural_Formation_Element_Simulation, CRC_Handbook_Properties, Early_Lean_MC_Panel |
| **Quantum_Optics** | 11 | yes | — |

### D = 12–16 — life / fluid / weather

Biology through meteorology — viscosity and C_factor.

| Core fold | D_eff | observed | Extension subdomains (nearest D) |
|-----------|------:|:--------:|----------------------------------|
| **Biology** | 12 | dark | Linguistics_Formal, Computational_Reasoning, Trinary_OS_Portable, Trinary_OS_ISA_Rebuild, Trinary_OS_Round_Trip, Tokenization_Smoke, Trinary_Hardware_Motif, Intrinsic_LLM_Validators, Arxiv_Primitives_V14, Binary_Decoder_Rendlesham, Certified_Agent_Qwen, VL_Distill_Atlas … +9 |
| **Biochemistry** | 13 | yes | Immunology, Geomagnetism, Bibliography_Lean_Corpus, RCSB_PDB_Structures, HVAC_Thermal_Systems, UniProt_Structure_Annotations_Deep, Heavy_Ion_Lab_Synthesis_Panel, ClinicalTrials_Medical_Panel, Toxicology_Panel, Immunology_Panel, Tokenization_Live_Panel, Founding_Cosmic_Dust_Panel … +2 |
| **Condensed_Matter** | 14 | yes | Plasma_Physics, Space_Weather, Pharmacology, Magnetosphere, Magnetosphere_Extended, Oncology, Neuroimmunology, Synthetic_Biology, Neuron_Multi_Hero, Materials_Engineering, Materials_Species_Bridge, IGEM_Synthetic_Biology … +35 |
| **Neuroscience** | 14 | yes | — |
| **Ecology** | 15 | dark | Hydrology, TOE_Dynamics, Geochemistry, Culinary_Arts, Maillard_Chemistry, Clinical_Medicine, GBIF_Species_Occurrence, Marine_Biology, Epidemiology, Cardiology, History, Network_Internet_Protocols … +24 |
| **Fluid_Dynamics** | 15 | dark | — |
| **Nuclear_Physics** | 15 | yes | — |
| **Thermodynamics** | 15 | yes | — |
| **Meteorology** | 16 | dark | Climate_Science, Cryosphere, Planetary_Structure, Grace_Cryosphere, Planetary_Atmospheres, Quantum_Materials, Agriculture_Agroecology, Architecture_Building_Science, Chemical_Engineering, Civil_Engineering, Mechanical_Engineering, Neuroeconomics … +32 |
| **Psychology** | 16 | yes | — |

### D = 17–21 — bulk / catalogs

Atmosphere, ocean, rock, planets, astronomy.

| Core fold | D_eff | observed | Extension subdomains (nearest D) |
|-----------|------:|:--------:|----------------------------------|
| **Atmospheric_Physics** | 17 | dark | Tectonics, Mathematics_Computational, Math_Generator_Rules_Eval, Environmental_Engineering, Anthropology, Math_Generator_Benchmark_Formula_Eval, Math_Generator_Airfoil_RMSE, Formula_Corpus_CNC, FSOT_Aggregate_Unified_DB, NOAA_Coastal_Tides, Paleoclimate, Law_Policy … +47 |
| **Oceanography** | 17 | dark | — |
| **Seismology** | 18 | dark | Particle_Physics, Seismology, Orbital_Mechanics, Small_Body_Orbits, Seismology_Deep, Geology_Stratigraphy, OpenAlex_Citation_Graph, Paleontology, Pure_Mathematics, Supply_Chain_Logistics, Zero_Day_Risk_Evaluator, Formula_Branching_Fractal … +28 |
| **Sociology** | 18 | yes | — |
| **Geophysics** | 19 | dark | Higgs_Mass, Econometrics, CERN_Open_Data_LHC, Finance_Markets, Theory_Completeness_Spine, ToE_Gap_Closure_Spine, Domain_Orbital_Predictions, Time_Domain_Crosswalk, Stellar_Multiplicity_Catalog, Stellar_Multiplicity_Live_Deep, WDS_Live_Multiplicity_Deep, Island_Of_Stability_Deep_Panel … +10 |
| **Astronomy** | 20 | yes | World_Bank_Development, Exogeology, ToE_Unification_Spine, Fold_Depth_Metrics, Fluid_Phase_Current_Spine, SH0ES_Ladder_Chain, Cepheid_PL_Interconnect, SH0ES_Full_Sample, Compact_Object_Binary_Events, Galactic_Structure_Sample, GWOSC_Live_Event_Deep, SIMBAD_Stellar_Identity_Deep … +15 |
| **Economics** | 20 | yes | — |
| **Planetary_Science** | 21 | yes | MPCORB_Minor_Planet_Catalog, NASA_Exoplanet_Archive, Reality_Folding_Spine, Exoplanet_System_Architecture, VizieR_WDS_TAP_Live_Deep, Superheavy_Island_Emergence_Simulation, STScI_MAST_Telescope_Panel, Arxiv_Gravitational_Waves_Panel, Complexity_Folding_Emergence_Panel, Longevity_Extreme_Species_Panel, Zebrafish_Developmental_Mechanics_Panel |

### D = 22–25 — deep / ceiling

QG, particle-astro, astrophysics, cosmology at D=25.

| Core fold | D_eff | observed | Extension subdomains (nearest D) |
|-----------|------:|:--------:|----------------------------------|
| **Quantum_Gravity** | 22 | dark | TOE_Limit_Recovery, Biological_CUDA_Physarum, Breakthrough_Discoveries_2024_2026, Stumped_Observables_Panel, Superheavy_Island_Completion_Spine, Distant_Island_Z128_Z132_Deep_Panel, Periodic_Extension_Decay_Topology_Scaffold, RD_Interval_Tightening_Panel, Nothing_Perfection_Friction_Origin_Panel, Foundational_Ontology_Spine, Longevity_MegaDeep_NCBI_Panel, Zebrafish_Longevity_Genetics_Coupling_Panel … +1 |
| **Astrophysics** | 24 | yes | Dark_Sector_Open_Problems, Dark_Energy_CPL, Z164_Distant_Island_Prereg_Scaffold, Cosmology_Anomaly_Deep_Panel, Domain_Coupling_Simulation_Refresh_Panel, Longevity_Consciousness_Coupling_Panel |
| **Particle_Astrophysics** | 24 | dark | — |
| **Cosmology** | 25 | dark | Cosmology_Extended, Cosmology_Bubble_Bleed, Cosmology_Anomalies, TOE_Contested_Sector_Refresh, Omni_Theory_Genesis, Hubble_Bubble_Tension, Stumped_Observables_Spine, SH0ES_Refined, Proof_Ledger_Closure_Spine, ToE_Claim_Certificate_Bundle, Distant_Island_Emergence_Simulation, Periodic_Table_Extension_Closure_Spine … +5 |

## Interconnects already gated (do not re-litigate)

| Interconnect | Cores | Status | Where |
|--------------|-------|--------|-------|
| Cepheid PL | Acoustics, Chemistry, Electromagnetism, Astronomy | filled | docs/CEPHEID_PL_PHYSICS.md |
| BH→WH bubble H0 | Cosmology, Astronomy, Astrophysics | filled | docs/CONCEPTS.md C3 / SH0ES_LADDER_DIAGNOSIS.md |
| Genetics ChemLink | Biology, Chemistry, Biochemistry | filled_sibling | docs/GENETICS_CLAIM_EVIDENCE.md |
| MPCORB planetary catalog | Planetary_Science, Astronomy | filled | docs/MPCORB_REFINEMENT_PROCESS.md |
| Observer / C_factor | Neuroscience, Quantum_Mechanics, Optics | filled | docs/CONSCIOUSNESS_CLAIM_EVIDENCE.md |
| Matter–antimatter conjugate | Particle_Physics, High_Energy_Physics, Quantum_Mechanics | filled | docs/MATTER_ANTIMATTER_CLAIM_EVIDENCE.md |
| Seed cross-ratios (engine §25) | Optics, Quantum_Optics, Materials_Science, Condensed_Matter, Astronomy, Planetary_Science | engine | vendor/fsot_compute.py §25 |
| Between-scale interconnects (5 gaps) | Acoustics, Seismology, Fluid_Dynamics, Oceanography, Atmospheric_Physics, Thermodynamics, Cosmology, Nuclear_Physics, Particle_Physics, Quantum_Gravity | filled | docs/SCALE_INTERCONNECT_PHYSICS.md |

## Between-scale gaps (physical conditions still siloed)

These are the next expansion targets. Fill with **measured public tables** and
the mismatch rule (wrong `D_eff` first). Forbidden: extra coefficient, stuffing
SH0ES class 1% into 0.5%, inventing unpublished tech numerics.

| Gap | Cores | Why it is one fluid | What “filled” looks like |
|-----|-------|---------------------|--------------------------|
| **Developmental mechanics (sibling-owned)** | Biology, Fluid_Dynamics, Neuroscience | Zebrafish 0.358% is inside 0.5%. Genetics repo is the live fold; migrate when that freeze lands. | Do not densify here. Wait for FSOT-Genetics product freeze, then hub residual. |
| **Social tanks at catalog scale** | Economics, Sociology, Psychology | As-above-so-below says a market is not a different medium from a neural net. Economics pooled 0.129%. | κ(Economics,Neuroscience) on World Bank series already ingested; no fitted β. |

## Largest empirical pooled residuals (still green)

Process/certificate C_thin spines (TOE ledgers, rust-lean bridge) are not these.
Push **measured** panels with APPLY. Zebrafish 0.358% was the worst; D_eff metadata
is now 12 (biology), matching the connective engine — not astrophysics 24.

| Domain | Records | Pooled % |
|--------|--------:|---------:|
| Zebrafish_Predictive_Validation_Panel | 20 | 0.3580 |
| Econometrics | 172 | 0.1292 |
| Economics | 157 | 0.1292 |
| Neuroeconomics | 65 | 0.1050 |
| Maillard_Chemistry | 30 | 0.0944 |
| Architecture_Building_Science | 43 | 0.0787 |
| CODATA_Full_Table_Open | 38 | 0.0736 |
| immunology_benchmark.json | 84 | 0.0612 |
| Observer_Channel_Derivation | 372 | 0.0525 |
| TOE_CKM_PMNS_Flavor | 40 | 0.0520 |
| neuroimmunology_benchmark.json | 92 | 0.0504 |
| oncology_benchmark.json | 67 | 0.0504 |

Kill: treating the family tree as a request for more free parameters.
More domains strengthen Label A only. Label B T1–T6 is frozen.

Related: [`HOLE_AUDIT.md`](HOLE_AUDIT.md) · [`SYSTEM_DIRECTORY.md`](SYSTEM_DIRECTORY.md) ·
[`APPLY.md`](APPLY.md)
