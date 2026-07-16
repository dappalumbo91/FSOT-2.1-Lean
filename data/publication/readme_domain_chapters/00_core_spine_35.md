## Core NeuroLab Spine — 35 Scientific Domains

The core spine routes FSOT through 35 preregistered NeuroLab domains. Each domain selects a Lean ledger route (`lean_domain`), verification labs, and measured record cohort. All core domains pass the ≤0.5% green gate.

### Acoustics

**Lean route:** `material` — condensed-matter and materials properties.

| Metric | Value |
|--------|------:|
| Empirical records | 485 |
| Pooled median error | 0.032277% |
| Coverage tier | A_strong |
| Subfields touched | 2 / 7 studied |

**Verification labs:** `smiles_lab`

**Scientific coverage:** SMILES relay; thin on sonar, architectural acoustics

**FSOT readout:** The same seed engine evaluates acoustics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `material` routing.

### Astronomy

**Lean route:** `astronomical` — stellar and galactic catalog readouts through astronomical ledger routes.

| Metric | Value |
|--------|------:|
| Empirical records | 193 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 7 / 15 studied |

**Verification labs:** `cosmology_lambda_cdm;cosmology_wave4;cosmology_extended_lab;cosmology_bubble_bleed_lab`

**Scientific coverage:** Gaia/SIMBAD/MAST/WDS; thin on radio VLBI

**FSOT readout:** The same seed engine evaluates astronomy observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `astronomical` routing.

### Astrophysics

**Lean route:** `astronomical` — stellar and galactic catalog readouts through astronomical ledger routes.

| Metric | Value |
|--------|------:|
| Empirical records | 305 |
| Pooled median error | 0.000561056% |
| Coverage tier | A_strong |
| Subfields touched | 6 / 14 studied |

**Verification labs:** `cosmology_wave4;cosmology_extended_lab;cosmology_higher_waves_lab;cosmology_bubble_bleed_lab`

**Scientific coverage:** Stellar/galactic; thin on stellar evolution grids

**FSOT readout:** The same seed engine evaluates astrophysics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `astronomical` routing.

### Atmospheric_Physics

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 17414 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 10 studied |

**Verification labs:** `weather_lab;atmospheric_physics_gap_fill_lab`

**Scientific coverage:** Weather/climate; thin on aerosol microphysics

**FSOT readout:** The same seed engine evaluates atmospheric_physics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### Atomic_Physics

**Lean route:** `particle` — particle and atomic observables via high-energy scalar channels.

| Metric | Value |
|--------|------:|
| Empirical records | 116 |
| Pooled median error | 0.000950413% |
| Coverage tier | A_strong |
| Subfields touched | 3 / 8 studied |

**Verification labs:** `smiles_lab;nist_atomic_lab`

**Scientific coverage:** CODATA + periodic table; thin on Rydberg molecules, laser cooling

**FSOT readout:** The same seed engine evaluates atomic_physics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `particle` routing.

### Biochemistry

**Lean route:** `medical` — biochemical and medical SMILES-anchored properties.

| Metric | Value |
|--------|------:|
| Empirical records | 166 |
| Pooled median error | 0.0192011% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 12 studied |

**Verification labs:** `smiles_lab;neurolab_bio`

**Scientific coverage:** PDB/ChEMBL/ClinicalTrials; thin on metabolomics

**FSOT readout:** The same seed engine evaluates biochemistry observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `medical` routing.

### Biology

**Lean route:** `biological` — life-system emergence — positive raw_S at canonical biological folds.

| Metric | Value |
|--------|------:|
| Empirical records | 67 |
| Pooled median error | 0% |
| Coverage tier | B_verified |
| Subfields touched | 10 / 20 studied |

**Verification labs:** `evolution_lab;cellular_lab;neurolab_bio`

**Scientific coverage:** UniProt/GBIF/NCBI + developmental/structural/genomics depth panel

**FSOT readout:** The same seed engine evaluates biology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `biological` routing.

### Chemistry

**Lean route:** `electron` — electromagnetic and chemical electron-shell observables.

| Metric | Value |
|--------|------:|
| Empirical records | 99 |
| Pooled median error | 0.005707% |
| Coverage tier | B_verified |
| Subfields touched | 6 / 15 studied |

**Verification labs:** `smiles_lab`

**Scientific coverage:** PubChem/CRC; thin on organometallic, solid-state synth

**FSOT readout:** The same seed engine evaluates chemistry observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `electron` routing.

### Condensed_Matter

**Lean route:** `material` — condensed-matter and materials properties.

| Metric | Value |
|--------|------:|
| Empirical records | 1169 |
| Pooled median error | 0.0306032% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 14 studied |

**Verification labs:** `smiles_lab;species_catalog`

**Scientific coverage:** Superconductivity Tc depth — literature + breakthrough + quantum materials

**FSOT readout:** The same seed engine evaluates condensed_matter observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `material` routing.

### Cosmology

**Lean route:** `cosmological` — negative dispersal regime — structure bleeds at cosmic scales unless bubble-bleed dual anchors apply.

| Metric | Value |
|--------|------:|
| Empirical records | 347 |
| Pooled median error | 0.00073542% |
| Coverage tier | A_strong |
| Subfields touched | 7 / 12 studied |

**Verification labs:** `cosmology_lambda_cdm;cosmology_extended_lab;cosmology_higher_waves_lab;cosmology_bubble_bleed_lab`

**Scientific coverage:** CMB/bubble-bleed/H0; thin on BAO full survey ingest

**FSOT readout:** The same seed engine evaluates cosmology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `cosmological` routing.

### Ecology

**Lean route:** `biological` — life-system emergence — positive raw_S at canonical biological folds.

| Metric | Value |
|--------|------:|
| Empirical records | 654 |
| Pooled median error | 0.017789% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 12 studied |

**Verification labs:** `gbif_ecology_lab;evolution_lab`

**Scientific coverage:** GBIF/iNaturalist; thin on food-web, population dynamics

**FSOT readout:** The same seed engine evaluates ecology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `biological` routing.

### Economics

**Lean route:** `consciousness` — observer-coupled consciousness routes with quirk_mod active.

| Metric | Value |
|--------|------:|
| Empirical records | 167 |
| Pooled median error | 0.129201% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 10 studied |

**Verification labs:** `world_bank_economics_lab;linguistics_lab`

**Scientific coverage:** World Bank/Crossref; thin on macro VAR, trade gravity

**FSOT readout:** The same seed engine evaluates economics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `consciousness` routing.

### Electromagnetism

**Lean route:** `electron` — electromagnetic and chemical electron-shell observables.

| Metric | Value |
|--------|------:|
| Empirical records | 271912 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 9 studied |

**Verification labs:** `smiles_lab;geomagnetism_lab;space_weather_lab`

**Scientific coverage:** GOES x-ray, geomagnetism; thin on antenna theory, plasmonics

**FSOT readout:** The same seed engine evaluates electromagnetism observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `electron` routing.

### Fluid_Dynamics

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 56 |
| Pooled median error | 0% |
| Coverage tier | B_verified |
| Subfields touched | 4 / 10 studied |

**Verification labs:** `fluid_dynamics_lab;trinary_fluid_computer`

**Scientific coverage:** Fluid spacetime + HVAC; thin on turbulence DNS

**FSOT readout:** The same seed engine evaluates fluid_dynamics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### Geophysics

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 547 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 11 studied |

**Verification labs:** `weather_lab;tectonics_lab;geomagnetism_lab`

**Scientific coverage:** USGS/seismology/grace; thin on magnetotellurics

**FSOT readout:** The same seed engine evaluates geophysics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### High_Energy_Physics

**Lean route:** `higgs` — electroweak and Higgs-sector cached observables.

| Metric | Value |
|--------|------:|
| Empirical records | 151 |
| Pooled median error | 0.00355717% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 9 studied |

**Verification labs:** `higgs_branching_lab;higgs_mass_lab;cosmology_higher_waves_lab`

**Scientific coverage:** CERN/GWOSC/Higgs; thin on B-physics, jet substructure

**FSOT readout:** The same seed engine evaluates high_energy_physics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `higgs` routing.

### Materials_Science

**Lean route:** `material` — condensed-matter and materials properties.

| Metric | Value |
|--------|------:|
| Empirical records | 1169 |
| Pooled median error | 0.0306032% |
| Coverage tier | A_strong |
| Subfields touched | 9 / 14 studied |

**Verification labs:** `smiles_lab;species_catalog`

**Scientific coverage:** Materials Project + creep/fracture/mechanical depth panel

**FSOT readout:** The same seed engine evaluates materials_science observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `material` routing.

### Meteorology

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 17414 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 10 studied |

**Verification labs:** `weather_lab;meteorology_gap_fill_lab`

**Scientific coverage:** Open-Meteo/NDBC; thin on NWP ensemble verification

**FSOT readout:** The same seed engine evaluates meteorology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### Molecular_Chemistry

**Lean route:** `chemical` — molecular chemistry and bonding readouts.

| Metric | Value |
|--------|------:|
| Empirical records | 608 |
| Pooled median error | 0.0283895% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 8 studied |

**Verification labs:** `smiles_lab`

**Scientific coverage:** SMILES/PDB; thin on conformer ensembles

**FSOT readout:** The same seed engine evaluates molecular_chemistry observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `chemical` routing.

### Neuroscience

**Lean route:** `neural` — neuroscience and brain-component metabolic proxies.

| Metric | Value |
|--------|------:|
| Empirical records | 41 |
| Pooled median error | 0.0133828% |
| Coverage tier | B_verified |
| Subfields touched | 7 / 15 studied |

**Verification labs:** `smiles_lab;neuron_cohort_lab`

**Scientific coverage:** Connectomics depth panel — neuron cohort strata + catalog coverage + OpenNeuro

**FSOT readout:** The same seed engine evaluates neuroscience observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `neural` routing.

### Nuclear_Physics

**Lean route:** `nuclear` — nuclear structure and BBN-proxy channels.

| Metric | Value |
|--------|------:|
| Empirical records | 79 |
| Pooled median error | 0.00735713% |
| Coverage tier | B_verified |
| Subfields touched | 4 / 10 studied |

**Verification labs:** `smiles_lab;blackhole_thesis`

**Scientific coverage:** OSTI/HEP; thin on cross-section databases

**FSOT readout:** The same seed engine evaluates nuclear_physics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `nuclear` routing.

### Oceanography

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 112 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 11 studied |

**Verification labs:** `noaa_oceanography_lab;weather_lab`

**Scientific coverage:** NOAA tides/NDBC; thin on ARGO float profiles

**FSOT readout:** The same seed engine evaluates oceanography observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### Optics

**Lean route:** `material` — condensed-matter and materials properties.

| Metric | Value |
|--------|------:|
| Empirical records | 485 |
| Pooled median error | 0.032277% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 9 studied |

**Verification labs:** `smiles_lab`

**Scientific coverage:** Interferometry depth — LIGO/JWST reference + MAST em wavelengths

**FSOT readout:** The same seed engine evaluates optics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `material` routing.

### Particle_Astrophysics

**Lean route:** `cmb` — CMB and large-scale structure interval certificates.

| Metric | Value |
|--------|------:|
| Empirical records | 192 |
| Pooled median error | 0.00464371% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 10 studied |

**Verification labs:** `cosmology_wave4;cosmology_extended_lab;cosmology_higher_waves_lab`

**Scientific coverage:** GWOSC/UAP; thin on cosmic-ray spectrum

**FSOT readout:** The same seed engine evaluates particle_astrophysics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `cmb` routing.

### Particle_Physics

**Lean route:** `particle` — particle and atomic observables via high-energy scalar channels.

| Metric | Value |
|--------|------:|
| Empirical records | 98 |
| Pooled median error | 0.00232226% |
| Coverage tier | B_verified |
| Subfields touched | 4 / 12 studied |

**Verification labs:** `particle_physics_lab`

**Scientific coverage:** PDG/Higgs/CERN; thin on neutrino oscillation, lattice QCD

**FSOT readout:** The same seed engine evaluates particle_physics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `particle` routing.

### Physical_Chemistry

**Lean route:** `chemical` — molecular chemistry and bonding readouts.

| Metric | Value |
|--------|------:|
| Empirical records | 608 |
| Pooled median error | 0.0283895% |
| Coverage tier | A_strong |
| Subfields touched | 4 / 10 studied |

**Verification labs:** `smiles_lab`

**Scientific coverage:** PubChem thermochem; thin on kinetics, surface chem

**FSOT readout:** The same seed engine evaluates physical_chemistry observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `chemical` routing.

### Planetary_Science

**Lean route:** `galactic` — cross-domain scalar evaluation at canonical seed parameters.

| Metric | Value |
|--------|------:|
| Empirical records | 50 |
| Pooled median error | 0.0214774% |
| Coverage tier | B_verified |
| Subfields touched | 6 / 12 studied |

**Verification labs:** `cosmology_wave4;cosmology_extended_lab`

**Scientific coverage:** Exoplanet/JPL NEO/Horizons; thin on regolith, atm chemistry

**FSOT readout:** The same seed engine evaluates planetary_science observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `galactic` routing.

### Psychology

**Lean route:** `consciousness` — observer-coupled consciousness routes with quirk_mod active.

| Metric | Value |
|--------|------:|
| Empirical records | 170 |
| Pooled median error | 0.0315062% |
| Coverage tier | A_strong |
| Subfields touched | 7 / 12 studied |

**Verification labs:** `openalex_psychology_lab;linguistics_lab`

**Scientific coverage:** OpenAlex/citations + psychometrics/RCT/cognition depth panel

**FSOT readout:** The same seed engine evaluates psychology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `consciousness` routing.

### Quantum_Computing

**Lean route:** `ai` — computational and AI-oracle invariant panels.

| Metric | Value |
|--------|------:|
| Empirical records | 180 |
| Pooled median error | 0.000295346% |
| Coverage tier | A_strong |
| Subfields touched | 6 / 8 studied |

**Verification labs:** `quantum_computing_lab;trinary_os`

**Scientific coverage:** Math-first QC depth — gate fidelity, error correction, formal rules; physical QC verifies

**FSOT readout:** The same seed engine evaluates quantum_computing observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `ai` routing.

### Quantum_Gravity

**Lean route:** `blackhole` — cross-domain scalar evaluation at canonical seed parameters.

| Metric | Value |
|--------|------:|
| Empirical records | 141 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 2 / 6 studied |

**Verification labs:** `blackhole_thesis;cosmology_bubble_bleed_lab`

**Scientific coverage:** Scaffold/crosswalk; thin on LQG observables

**FSOT readout:** The same seed engine evaluates quantum_gravity observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `blackhole` routing.

### Quantum_Mechanics

**Lean route:** `quantum` — quantum mechanics and entanglement-channel readouts.

| Metric | Value |
|--------|------:|
| Empirical records | 74 |
| Pooled median error | 0.000950413% |
| Coverage tier | B_verified |
| Subfields touched | 7 / 10 studied |

**Verification labs:** `smiles_lab;nist_quantum_lab`

**Scientific coverage:** NIST constants + entanglement/decoherence/measurement depth panel

**FSOT readout:** The same seed engine evaluates quantum_mechanics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `quantum` routing.

### Quantum_Optics

**Lean route:** `quantum` — quantum mechanics and entanglement-channel readouts.

| Metric | Value |
|--------|------:|
| Empirical records | 74 |
| Pooled median error | 0.000950413% |
| Coverage tier | B_verified |
| Subfields touched | 2 / 7 studied |

**Verification labs:** `smiles_lab;nist_quantum_lab`

**Scientific coverage:** Cross-domain; thin on squeezed light, cavity QED

**FSOT readout:** The same seed engine evaluates quantum_optics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `quantum` routing.

### Seismology

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 1000 |
| Pooled median error | 0% |
| Coverage tier | A_strong |
| Subfields touched | 5 / 8 studied |

**Verification labs:** `seismology_lab;tectonics_lab`

**Scientific coverage:** USGS deep catalog; thin on full moment-tensor relay

**FSOT readout:** The same seed engine evaluates seismology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.

### Sociology

**Lean route:** `consciousness` — observer-coupled consciousness routes with quirk_mod active.

| Metric | Value |
|--------|------:|
| Empirical records | 410 |
| Pooled median error | 0.0195044% |
| Coverage tier | A_strong |
| Subfields touched | 3 / 10 studied |

**Verification labs:** `openalex_sociology_lab;world_bank_sociology_lab;linguistics_lab`

**Scientific coverage:** UAP years/registry; thin on survey panels, networks

**FSOT readout:** The same seed engine evaluates sociology observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `consciousness` routing.

### Thermodynamics

**Lean route:** `energy` — thermodynamic, atmospheric, and energy-sector observables.

| Metric | Value |
|--------|------:|
| Empirical records | 89 |
| Pooled median error | 0.022147% |
| Coverage tier | B_verified |
| Subfields touched | 4 / 8 studied |

**Verification labs:** `fuel_lab`

**Scientific coverage:** Fuel/NIST; thin on non-equilibrium, phase diagrams

**FSOT readout:** The same seed engine evaluates thermodynamics observables without per-record fitting. Measured values are drawn from public domain data (NIST, Planck-class surveys, SMILES/NCBI catalogs, NOAA/USGS archives as applicable) and compared to seed-derived predictions through `energy` routing.
