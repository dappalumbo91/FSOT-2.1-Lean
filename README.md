# FSOT 2.0 Lean Formalization

**Fluid Spacetime Omni-Theory (FSOT) 2.0**

This is the Lean 4 formalization of **Fluid Spacetime Omni-Theory (FSOT) 2.0**, created and architected by **Damian Arthur Palumbo**.

It was developed in close collaboration with the Python reference implementation.

## Structure

- `FSOT/Scalar.lean` — Executable `Float`-based core (for the Python verification runner and quick checks). Includes extracted internal terms (`growth_term`, `quirk_mod`, `perceived_adjust`, `term3` + sub-components).

- `FSOT/Theorems.lean` — Theorems and Examples section (Float layer). Includes scaling proofs, `quirk_mod` case analysis, emergence/damping interpretation, quantitative dominance theorems, and documented `#eval` examples.

- `FSOT/Formal/` — Heavier `Real`-based proof layer (aligned with the attached `FSOT.Formal.*` files).
  - `Formal/Scalar.lean` — `Real` version of the core scalar engine.
  - `Formal/Theorems.lean` — Rigorous theorems using Mathlib analysis, with references to MC evidence and combustion triangulation from the attached files.

- `FSOT2_0_Compute.lean` — Executable entry point (run with `lake env lean FSOT2_0_Compute.lean`).

## Key Features

- **Extracted internal terms** for clean, rigorous proofs (`quirk_mod`, `growth_term`, `term3` sub-components, etc.).
- **Observer effect** (`quirk_mod`) formalized with case analysis.
- **Emergence vs Damping** interpretation theorems.
- **Quantitative dominance theorems** (when `term3` dominates Term1 + `quirk_mod`).
- **Examples section** with domain sweeps, observer intervention comparisons, stability delta style, and trinary collapse demos.
- Strong alignment with the attached reference files (`VibRegister.lean`, `RealData.lean`, `Domains.lean`, etc.), including MC + combustion justification in comments.

## Verification status (2026-07-09 — Tier 41)

Full pipeline: `python scripts/fsot_verification_runner.py`

Public capability map: `data/FSOT_VERIFIED_SCOPE.yaml` | Progress: `data/fsot_verification_progress.yaml` | Domain map: `data/scientific_domain_expansion_map.json`

| Metric | Value |
|--------|-------|
| Verification tiers | **39/39 complete** (100%) |
| Scientific domains | **141** (35 NeuroLab + 105 extension + Intelligence Compression rollup) |
| Empirical records | **306,680** |
| Neurolab precision | **35/35** domains ≤2% median error |
| Coverage tiers | A_strong: 25 · B_verified: 10 · C_thin: **0** · D_needs_work: **0** · unverified: **0** |
| Lean formal modules | **175** |
| Proved claims | **65** · 0 active `sorry` |
| SOTA ledger | **54/54** observables beat or meet baselines |
| Expansion candidates | **0** (all identified science gaps filled) |

**External data cache** (bulk API ingest): `G:\FSOT-PublicData` — override with `FSOT_EXTERNAL_DATA_ROOT`. Tier F gap-fill cache: `G:\FSOT-PublicData\tier_f_gaps`.

**Self-contained clone-and-verify**: `strict_empirical.jsonl` (7,941 formulas) bundled under `vendor/formula_corpus/`.
- Genomic exact identities (`FSOT.Formal.Genomic`)
- Brain component priors (`FSOT.Formal.BrainPriors`) — 10 NeuroLab components
- 64-codon dual-axis map (`FSOT.Formal.CodonPriors`) — 8 primary + 27 secondary patterns
- Protein amino-acid trinary (`FSOT.Formal.ProteinPriors`) — 20 AAs, 10 distinct patterns ⊆ 27
- Protein formula closed forms (`FSOT.Formal.ProteinFormulas`) — 15 catalog + 3 proposed, φ⁶ disulfide certified
- ΛCDM cosmology observables (`FSOT.Formal.CosmologyLab`) — 30 observables (full Wave-3) within 2%
- Fuel Lab compound profiles (`FSOT.Formal.FuelPriors`) — 6 profiles, 34 resolved PubChem lookups
- Machine & Molecule catalog (`FSOT.Formal.SpeciesPriors`) — 141 species, 684 FSOT properties within 5%
- Genetics CAMEO symbolic folding (`FSOT.Formal.CameoPriors`) — 130 benchmarks, 8.85 Å MAE formula
- Fsot trinary OS (`FSOT.Formal.TrinaryOSPriors`) — FSOTB Tier-1/2/3 oracle invariants
- Photonic V2 virtual crystal (`FSOT.Formal.PhotonicForge`) — 180 voxels, POOF/P_new resonance map
- VibraFSOT register + MC alignment (`FSOT.Formal.VibRegisterPriors`) — D_eff=11, cp5 prob_non_decrease=1.0
- Magnetic string lattice (`FSOT.Formal.MagneticStringPriors`) — 250 strings, S_em≈0.519
- Evolution sim (`FSOT.Formal.EvolutionPriors`) — 13 mitochondrial operons, fitness 58.49
- Weather scalar sim (`FSOT.Formal.WeatherPriors`) — 24h at D_eff=15, all S>0
- Linguistics anchors (`FSOT.Formal.LinguisticsPriors`) — 10 targets within 5% FSOT derivations
- Unified DB inventory (`FSOT.Formal.UnifiedDBPriors`) — 30,984 indexed records, 26 projects (inventory tier)
- Cosmology Wave-4 (`FSOT.Formal.CosmologyWave4Priors`) — 16 observables (PMNS/CKM/nuclear/dark-energy); legacy `CosmologyWave4.lean` is a deprecation shim
- GFZ Kp historical arc (`FSOT.Formal.SpaceWeatherPriors`) — **271,813** Kp records (1932–2024), 100% stability match
- USGS hydrology (`FSOT.Formal.HydrologyPriors`) — monthly streamflow cohort with train/holdout gates
- Pharmacology ChEMBL (`FSOT.Formal.PharmacologyPriors`) — 120 approved-drug molecular weights, median err &lt;0.01%
- Cryosphere proxy (`FSOT.Formal.CryospherePriors`) — 1,919 northern freezing-month records, 99.3% classifier match
- Theory-of-Everything crosswalk (`data/fsot_theory_crosswalk.yaml`) — Aerospace, CS, Hearing + geophysics/planetary stack
- Seismology (`FSOT.Formal.SeismologyPriors`) — **500** USGS M4.5+ events, 98.6% shallow-depth classifier match
- Tectonics (`FSOT.Formal.TectonicsPriors`) — **241** PB2002 plate boundaries + crustal earthquake coupling
- Geomagnetism (`FSOT.Formal.GeomagnetismPriors`) — **525** NOAA Dst/GOES records, 100% storm-classifier match
- Planetary structure (`FSOT.Formal.PlanetaryStructurePriors`) — **8** JPL bodies, density median err 0.05%
- Orbital mechanics (`FSOT.Formal.OrbitalMechanicsPriors`) — **8** planets, Kepler T²/a³ median err 0.11%
- Small-body orbits (`FSOT.Formal.SmallBodyOrbitsPriors`) — Moon + Ceres/Vesta/Eros/Halley, 0.01% median perturbation err
- Magnetosphere (`FSOT.Formal.MagnetospherePriors`) — **167** coupled Dst×Kp hours (NOAA rolling window); timeline arc: daily-max **71%** → 3-hourly **96%** → hourly-interpolated **100%**
- Magnetosphere extended (`FSOT.Formal.MagnetosphereExtendedPriors`) — **120,877** historical Kyoto Dst×Kp hours (1998–2012) @ **99.79%**; **77,188** G-scale storm holdout hours @ **99.68%**; **1,416** RTSW 1-min Bz records @ **99.44%**
- GRACE cryosphere (`FSOT.Formal.GraceCryospherePriors`) — **253** GFZ GravIS Greenland months, 93.7% mass-decline classifier match
- Seismology deep (`FSOT.Formal.SeismologyDeepPriors`) — **1000** moment-tensor + plate-margin observables, 81% match (Pacific holdout 100%)
- Planetary atmospheres (`FSOT.Formal.PlanetaryAtmospheresPriors`) — Mars/Venus/Titan pressure &amp; temperature, 0.27% median error
- Geochemistry (`FSOT.Formal.GeochemistryPriors`) — SMILES mineral/geo sections + planetary bulk-density overlap
- Oncology (`FSOT.Formal.OncologyPriors`) — SMILES drug/enzyme affinity + biology strict operon bridge
- Neuroimmunology (`FSOT.Formal.NeuroimmunologyPriors`) — immunology SMILES + Allen neuron cohort strata crosswalk
- Synthetic biology (`FSOT.Formal.SyntheticBiologyPriors`) — evolution mt-operons + biology strict NCBI bridge
- Quantum materials (`FSOT.Formal.QuantumMaterialsPriors`) — condensed-matter SMILES (band gaps, Tc, lattice)
- Neuron multi-hero (`FSOT.Formal.NeuronMultiHeroPriors`) — 4 FI-proxy certified heroes per Allen class
- Climate scale-up (`FSOT.Formal.ClimateSciencePriors`) — **30 stations × 50 years** (24 train / 6 holdout gates)
- Linguistics formal (`FSOT.Formal.LinguisticsFormalPriors`) — 10 measured anchors, consciousness bridge
- Mathematics computational (`FSOT.Formal.MathematicsComputationalPriors`) — math-generator comparisons + constant alignment
- Materials engineering (`FSOT.Formal.MaterialsEngineeringPriors`) — Young's modulus, thermal, bulk/shear SMILES
- Computational reasoning (`FSOT.Formal.ComputationalReasoningPriors`) — FIC sweep + trinary-OS coding invariants
- Math generator rules eval (`FSOT.Formal.MathGeneratorRulesEvalPriors`) — **1520** per-rule schema/domain eval across 61 corpora
- Trinary OS portable (`FSOT.Formal.TrinaryOSPortablePriors`) — vendor FSOTB oracles + ISA constants for clone-and-rebuild
- Materials↔species bridge (`FSOT.Formal.MaterialsSpeciesBridgePriors`) — 12 overlapping engineering metals cross-validated
- iGEM synthetic biology (`FSOT.Formal.IGEMSyntheticBiologyPriors`) — 20 Registry parts strict-empirical + biology_strict operon bridge
- Math benchmark_formula eval (`FSOT.Formal.MathGeneratorBenchmarkFormulaEvalPriors`) — live FO-200/210/220 overlay rule eval
- Trinary OS ISA rebuild (`FSOT.Formal.TrinaryOSISARebuildPriors`) — 27-opcode FSOTB v1/v1.1/v1.2 registry + oracle invariants
- iGEM live FASTA ingest (`FSOT.Formal.IGEMLiveFastaPriors`) — parts.igem.org FASTA refresh with bundled fallback cache
- Airfoil RMSE recompute (`FSOT.Formal.MathGeneratorAirfoilRmsePriors`) — FO-210 full-dataset + held-out RMSE live eval
- Trinary OS round-trip (`FSOT.Formal.TrinaryOSRoundTripPriors`) — vendor FSOTB byte-identical asm→dis→asm smoke
- Tokenization smoke (`FSOT.Formal.TokenizationSmokePriors`) — Dictionary universal-tokenizer smoke + vocab registry
- Trinary hardware motif (`FSOT.Formal.TrinaryHardwareMotifPriors`) — cube-block motif tier/weight invariants
- Intrinsic LLM validators (`FSOT.Formal.IntrinsicLLMValidatorsPriors`) — multi-topic validator accuracy tiers
- Physarum CUDA bridge (`FSOT.Formal.BiologicalCudaPhysarumPriors`) — RTX 5070 nuclei scaling + plasmodium v5 state
- arXiv V14 primitives (`FSOT.Formal.ArxivPrimitivesV14Priors`) — 2.96M topic ingest, six cognitive primitive signatures
- Formula corpus CNC (`FSOT.Formal.FormulaCorpusCncPriors`) — 61-doc corpus, validator delta, 100% chem gauntlet pass rate
- Rendlesham decoder (`FSOT.Formal.BinaryDecoderRendleshamPriors`) — 52-step hidden-state trace, 17 branching events
- Qwen certified agent (`FSOT.Formal.CertifiedAgentQwenPriors`) — lean-bridge protocol v1.1 + 9-path workspace registry
- Genesis omni-theory (`FSOT.Formal.OmniTheoryGenesisPriors`) — 12 ch.1 verses, all S&gt;0 FSOT scalar crosswalk
- Aggregate unified DB (`FSOT.Formal.FsotAggregateUnifiedDbPriors`) — 1,532 mathematical rows, 107 SMILES derivation sections
- Prediction re-derivation (`FSOT.Formal.PredictionRederivationPriors`) — 66 predictions, zero free parameters, 72% stabilized improvement rate
- Kronos metrology (`FSOT.Formal.KronosPriors`) — 568 runs, best fractional error 1.64e-7
- Knowledge base (`FSOT.Formal.KnowledgeBasePriors`) — 19,213 catalog formulas; 7,941 strict-empirical bridge (6,921 within 2%); per-formula pass on full catalog
- Math generator (`FSOT.Formal.MathGeneratorPriors`) — 7 comparisons within 2%
- Trinary Fluid Computer v2 (`FSOT.Formal.TrinaryFluidPriors`) — 99.3% accuracy, 27 Metatron pathways
- Soul Sibling kernel (`FSOT.Formal.SoulSiblingPriors`) — D_compact=24.98, zero_free
- Lean proofs bridge (`FSOT.Formal.LeanProofsBridge`) — 28 formal constants, k aligned to SMILES
- Formula corpus (`FSOT.Formal.FormulaCorpusPriors`) — **7,941** strict-empirical observable checks (all matched, all within 5%)
- Cellular lab (`FSOT.Formal.CellularPriors`) — 234k Soul Simulator records + 13 mt operons; `cellular_raw_S_positive`
- BlackHole thesis (`FSOT.Formal.BlackHoleThesisPriors`) — 28/28 observables within 2% (max err 0.72%)
- Space propulsion (`FSOT.Formal.SpacePropulsionSystemsPriors`) — 12 systems (NEXT-C, AEPS, X3, DRACO, Pulsar Sunbird), 21 observables, 0% median err
- Electrical power (`FSOT.Formal.ElectricalPowerSystemsPriors`) — batteries, grid, solar, superconductors; 9 observables
- HVAC thermal (`FSOT.Formal.HvacThermalSystemsPriors`) — SEER/COP/Carnot heat-pump cohort; 7 observables
- Breakthroughs 2024–2026 (`FSOT.Formal.BreakthroughDiscoveries20242026Priors`) — 20 world-shaking discoveries (NIF, AEPS, Webb, Euclid, Starship)
- Trinary-OS Tier E (`FSOT.Formal.TrinaryOSTierEPriors`) — unified FSOTB + ISA rebuild + round-trip byte-identical oracle (68 records, 0% pooled)

### Tier A/B/C — NeuroLab gap-fill (20 domains)

Real API anchors + FSOT v1.1 benchmarks for thin neurolab domains. Scripts: `scripts/tier_gap_fill_lib.py`, `build_tier_gap_fill_benchmarks.py`, `gen_tier_gap_fill_lean.py`.

Ecology, Economics, Psychology, Sociology, Oceanography, Meteorology, Atmospheric_Physics, Fluid_Dynamics, Atomic_Physics, Quantum_Mechanics, Quantum_Optics, Quantum_Computing, Particle_Physics, Pharmacokinetics, Food_Microbiology, Agriculture_Agroecology, Maillard_Chemistry, Econometrics, Sports_Biomechanics, Architecture_Building_Science.

### Tier D — Extension wave (7 domains)

`scripts/tier_d_extension_lib.py` · GBIF Plantae/Animalia + clinical/engineering/social bridges.

Geology_Stratigraphy, Botany, Zoology, Clinical_Medicine, Chemical_Engineering, Environmental_Engineering, Anthropology.

### Tier F — Science-gap fill (19 domains, Tier 41)

Closes every remaining expansion candidate before cross-domain coupling simulation. Real APIs: **PBDB** (paleontology), **OBIS** (marine biology), **GBIF** Fungi/Insecta, plus published reference anchors for clinical, engineering, humanities, and industry verticals.

| Domain | Lean module | Primary sources |
|--------|-------------|-----------------|
| Paleontology | `PaleontologyExtensionPriors` | PBDB + USGS seismology bridge |
| Marine_Biology | `MarineBiologyExtensionPriors` | OBIS + NOAA tides |
| Mycology | `MycologyExtensionPriors` | GBIF Fungi + food microbiology |
| Entomology | `EntomologyExtensionPriors` | GBIF Insecta + zoology |
| Virology | `VirologyExtensionPriors` | Reference + immunology + PubChem antivirals |
| Epidemiology | `EpidemiologyExtensionPriors` | WHO/CDC reference + World Bank health |
| Cardiology | `CardiologyExtensionPriors` | AHA/ESC reference + clinical medicine |
| Civil_Engineering | `CivilEngineeringExtensionPriors` | ASCE reference + materials engineering |
| Mechanical_Engineering | `MechanicalEngineeringExtensionPriors` | ASME reference + thermodynamics rules |
| Robotics_Control_Systems | `RoboticsControlSystemsExtensionPriors` | IEEE reference + Trinary-OS ISA |
| Neuroeconomics | `NeuroeconomicsExtensionPriors` | Behavioral econ reference + psychology/econometrics |
| Paleoclimate | `PaleoclimateExtensionPriors` | Ice-core reference + NOAA NCEI/cryosphere |
| Speleology | `SpeleologyExtensionPriors` | UIS cave metrics + hydrology/geochemistry |
| Exogeology | `ExogeologyExtensionPriors` | NASA Exoplanet Archive + planetary structure |
| Pure_Mathematics | `PureMathematicsExtensionPriors` | Math-generator rules + NIST constants |
| History | `HistoryExtensionPriors` | OpenAlex historical corpus + anthropology |
| Law_Policy | `LawPolicyExtensionPriors` | WGI governance + World Bank |
| Finance_Markets | `FinanceMarketsExtensionPriors` | Market reference + econometrics |
| Supply_Chain_Logistics | `SupplyChainLogisticsExtensionPriors` | SCOR reference + World Bank trade |

```bash
# Tier F rebuild (ingest → benchmarks → Lean)
python scripts/build_tier_f_extension_benchmarks.py --ingest
python scripts/build_tier_f_extension_benchmarks.py
python scripts/gen_tier_f_extension_lean.py
python scripts/build_scientific_domain_expansion_map.py
python scripts/build_sota_observable_ledger.py
python scripts/build_fsot_verification_progress.py
python scripts/build_fsot_verified_scope.py
lake build
```

Registry: `data/extension_domains_manifest.yaml` (tier 41 entries) · Benchmarks: `data/*_extension_benchmark.json` · Reference anchors: `data/*_reference_observables.json`.

### Formula verification honesty (Tier 6)

Per-formula observable checks use `fsot_numeric_eval_v4` — not count-only meta-oracles. Policy: `data/formula_verification_policy.yaml`.

| Corpus | Records | Matched | Within 2% | Notes |
|--------|---------|---------|-----------|-------|
| strict_empirical.jsonl | 7,941 | 7,941 | 6,921 | Primary honest verification path |
| verification_numeric (DB) | 9,607 | 9,556 ok | 8,283 | **0** strict_empirical pending |
| KB catalog per-formula | 19,213 | 105 verified | 50 | Full catalog pass + strict-empirical bridge |

Numeric eval pipeline:

```bash
python scripts/run_numeric_eval_queue.py          # pipeline + CNC gap + outcome backfill
python scripts/resolve_strict_empirical_gap.py    # CNC turning MRR (54 runs)
python scripts/backfill_numeric_from_outcomes.py  # outcome_json → verification_numeric
python scripts/run_knowledge_base_formula_verify.py
```

- Domain coverage map: `data/domain_coverage_map.yaml` (26 ledger domains: 18 proved_sign / 9 partial / 0 gap)
- Certificate: `data/certificate.json` | Run log: `data/verification_runs.jsonl`
- Verified scope (GitHub consumers): `data/FSOT_VERIFIED_SCOPE.yaml` — full FSOT capability index

See `REPRODUCE.md` and `docs/genomic_brain_priors_verification.md` for details.

## Usage

```bash
pip install -r requirements.txt
lake build

# Portable verification (clone-and-verify; no author Desktop required)
python scripts/fsot_verification_runner.py --portable

# Full pipeline (author machine with optional Desktop lab mirrors)
python scripts/fsot_verification_runner.py
```

Bundled oracle and lab inputs live under `vendor/`. See `CONTRIBUTING.md` and `data/external_data_manifest.yaml` for path overrides and contributor workflow.

## Alignment with Reference Files

This project closely follows the structure and justification style of the attached reference files:
- Uses MC evidence and combustion triangulation anchors (from `VibRegister.lean`, `Domains.lean`, `RealData.lean`).
- Extracts internal terms for proof hygiene (similar to attached `Scalar.lean`).
- References `VibRegister` observer lemmas and stability proxies.
- Keeps a clean separation between executable (`Float`) and rigorous (`Real` + Mathlib analysis) layers.

## Roadmap

- **141-domain cross-domain coupling simulation** — nodes = all covered domains; edges = `maps_to_lean` overlaps + crosswalk modules + scalar coupling (`fsot_compute.predictions()` cross-ratios); hooks in `thesis_simulation` lab and magnetosphere Dst×Kp×Bz coupling
- Tighten r_d interval to ±0.01 Mpc
- Extension domain precision tightening (median error &lt; 1% wave)
- Extend `select_observable()` hooks for non-IE chemistry/cosmology rows in unified DB
- Energy / fusion domain dedicated lab certificates (currently partial via fuel_lab proxy)

## License

Apache 2.0 (consistent with the reference implementation).