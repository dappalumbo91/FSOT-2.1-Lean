# Research standpoint — what the hub is, what still has to hold

*Generated 2026-09-09T18:55:07.283046+00:00 · pin D1D38A*

This is the step-back. **Not** another prediction wave and **not** another
domain count. Label A is the empirical framework. Label B T1–T6 is the
frozen ToE checklist. More green files strengthen A only.

**Refresh:** `python scripts/build_research_standpoint.py`

## 1. Coverage (do not mix ledgers)

| Ledger | Live | Meaning |
|--------|-----:|---------|
| Core folds | **35** | `DOMAINS` in `vendor/fsot_compute.py` — the 25-D slices |
| Extension subdomains | **375** | nearest-D attachments, not other ontologies |
| Atlas named rows | **403** | coverage map |
| Green residual files | **477 / 477** | ≤0.5% pooled median |
| A_strong / B_verified / C_thin | 117 / 338 / 13 | record-depth tiers (C_thin measured **3**) |
| Gated tissues | **86** | same physics, two zooms, residual-checked |
| Adjacent cores still siloed | **0** | 0 = gated; next work is objects/C_thin/dated, not new domains |

Counts authority: [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md) · [`CURRENT_STATUS.md`](CURRENT_STATUS.md).
Tree: [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md).
How a scientist reads a row: [`SCIENTIST_INTERFACE.md`](SCIENTIST_INTERFACE.md).

## 2. Architecture (one law, four layers)

```text
seeds {π,e,φ,γ,G}  →  S = K(T1+T2+T3)     vendor/fsot_compute.py  pin D1D38A
                 →  dynamics / GR-SM       vendor/fsot_dynamics.py · fsot_gr_sm.py
                 →  κ_ij tanks             vendor/fsot_complex_interaction.py
                 →  domain fold            (D_eff, observed) preregistered
                 →  APPLY residual         computed = measured·(1+|S|·f)
```

| Layer | What it is | Where |
|-------|------------|-------|
| Engine | identities, seeds, 35 routes | `vendor/fsot_compute.py` · `FSOT/Formal/` |
| Empirical | measured vs computed | `data/*benchmark*.json` · margin audit |
| Formal | Lean/Coq/Isabelle/F*/Rust/SMT/TLA+/QEMU/ESP32 | `data/cross_proof_verification_report.json` |
| Predictions | frozen locks + dated windows | `predictions/` vs `results/` |
| Siblings | Genetics product · Quantum fold | `results/siblings/` |

Apply without fitting: [`APPLY.md`](APPLY.md). Picture: [`CONCEPTS.md`](CONCEPTS.md).

## 3. What a ToE needs besides more domains

Label B is already a frozen checklist (T1–T6). The work that actually
**holds ground** for a scientist using this as a tool is:

| Need | Why | Status |
|------|-----|--------|
| **Named objects** | A paper number is not automatically the lock | [`OBJECT_SCORING.md`](OBJECT_SCORING.md) shipped |
| **Laws ledger** | Verification without stated rules is a scoreboard | this file + [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) |
| **Connective tissue** | Same physics at two scales is the ToE signature | 86 gated · adjacent ungated **0** |
| **APPLY cookbooks** | Worked example per high-value core; general protocol in APPLY.md | Materials · Acoustics · Fluid · Nuclear · Thermo · Chemistry · Neuro · Astronomy · Optics · Seismology · Atomic · EM · HEP · Bio · QC · Ecology · Psychology |
| **Science vs FSOT** | arXiv/PDG/survey scored on the *named* object | [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) living scoreboard; append via record_prediction_outcome.py |
| **C_thin measured** | Green-and-thin is not depth | queue below |
| **Honest refusals** | Clock-time, S2S, prices, diagnoses, CLOE-as-measured | already labeled |
| **Open uniqueness** | Path-integral / T3–T4 uniqueness | stay open. Do not pretend. |

More extension files do **not** complete T1–T6. They only thicken Label A.

## 4. Core folds (the 35 slices)

| D | observed | Core |
|--:|:--------:|------|
| 5 | yes | **Particle_Physics** |
| 6 | yes | **Quantum_Mechanics** |
| 7 | yes | **Atomic_Physics** |
| 7 | yes | **High_Energy_Physics** |
| 8 | yes | **Chemistry** |
| 8 | yes | **Physical_Chemistry** |
| 9 | yes | **Electromagnetism** |
| 9 | yes | **Molecular_Chemistry** |
| 10 | yes | **Acoustics** |
| 10 | yes | **Materials_Science** |
| 10 | yes | **Optics** |
| 11 | dark | **Quantum_Computing** |
| 11 | yes | **Quantum_Optics** |
| 12 | dark | **Biology** |
| 13 | yes | **Biochemistry** |
| 14 | yes | **Condensed_Matter** |
| 14 | yes | **Neuroscience** |
| 15 | dark | **Ecology** |
| 15 | dark | **Fluid_Dynamics** |
| 15 | yes | **Nuclear_Physics** |
| 15 | yes | **Thermodynamics** |
| 16 | dark | **Meteorology** |
| 16 | yes | **Psychology** |
| 17 | dark | **Atmospheric_Physics** |
| 17 | dark | **Oceanography** |
| 18 | dark | **Seismology** |
| 18 | yes | **Sociology** |
| 19 | dark | **Geophysics** |
| 20 | yes | **Astronomy** |
| 20 | yes | **Economics** |
| 21 | yes | **Planetary_Science** |
| 22 | dark | **Quantum_Gravity** |
| 24 | yes | **Astrophysics** |
| 24 | dark | **Particle_Astrophysics** |
| 25 | dark | **Cosmology** |

Dark on purpose: Biology, Ecology, Fluid, Meteorology, Atmosphere, Ocean,
Seismology, Geophysics, QC, QG, Particle_Astrophysics, Cosmology — look
flips identity (QC→QO is the Hilbert move). Do not 'fix' dark by setting
`observed=true`.

## 5. Gated tissues (already the same physics at two scales)

| ID | Cores | What it says | Live |
|----|-------|--------------|------|
| `TISSUE-H0` | Cosmology, Astronomy, Astrophysics | H0 is sectors of one fluid, not two cosmologies | Planck 0.024%; chain 72.856 vs 73.04 (0.252%); class bin 1% frozen |
| `TISSUE-WAVE` | Acoustics, Seismology | Lab sound and crustal PREM are one T3 standing wave | lithosphere median 0.069% |
| `TISSUE-FLUID` | Fluid_Dynamics, Oceanography, Atmospheric_Physics | One NDBC neighborhood, three tanks | pres/SST/wind 0.026–0.030% |
| `TISSUE-FRIDGE` | Thermodynamics, Cosmology | BH→WH is a heat/information pump (same fridge cycle) | |S_thermo|/|S_cosm| vs π/2 0.289% |
| `TISSUE-ORIFICE` | Nuclear_Physics, Particle_Physics | ENDF levels are two zooms of one orifice | nuclear 0.046% · particle 0.010% |
| `TISSUE-CEILING` | Quantum_Gravity, Cosmology | Compactification remainder → 1 as D→25 | |S_QG|/|S_cosm| vs A_bleed 0.088% |
| `TISSUE-SOCIAL` | Economics, Neuroscience | A market is not a different medium from a neural net | same World Bank YoY on both folds; siloed 0.129% not retuned |
| `TISSUE-CEPHEID` | Acoustics, Chemistry, Electromagnetism, Astronomy | Cepheid PL is acoustic + chemistry + light, not a fitted b | R_H = POOF·e·C_eff vs 0.4 at 0.110% |
| `TISSUE-CHEMLINK` | Biology, Chemistry, Biochemistry | Protein product is residual at named ChemLink interfaces | sibling freeze 0.13 Å vs AF 0.47 Å (10/10) |
| `TISSUE-OBSERVER` | Neuroscience, Quantum_Mechanics, Optics | Consciousness is C_factor on the observer string, not a bolt-on | 20.003601 vs 20.0 W (0.018%) |
| `TISSUE-CONJUGATE` | Particle_Physics, High_Energy_Physics, Quantum_Mechanics | Matter–antimatter is the other face of the same valve | C13 conjugate; not a second ontology |
| `TISSUE-VALVE-EQ` | Seismology, Fluid_Dynamics | Slow slip and fast rupture are SUCTION vs POOF of one valve | dated cells 39.1 km / φ^4 days; not a clock-time hypocenter |
| `TISSUE-SEIS-GEO` | Seismology, Geophysics | Wave fold vs bulk-earth fold on adjacent D=18/19; same PREM density | |S_seis|/|S_geo| vs φ/2; PREM lithosphere density dual-routed |
| `TISSUE-FRB-ORIFICE` | Particle_Astrophysics, Cosmology | FRB is BH→WH orifice outgassing; repeaters are saloon-door post-POOF, one-shots a paper-rip | E=width×fluence vs e·POOF 37/37; width class vs D=5 at 0%; 16.35 d = 5π+1/φ; 200·(1+dens) REMEDIED_WRONG_APPLY |
| `TISSUE-MAT-OPT` | Materials_Science, Optics | Same D=10 rung: CRC n_D on Optics, density on Materials; ice n vs φ²/2 | n/ρ dual-fold APPLY; |S_mat|/|S_opt| vs PhysChem/Chem look-split 0.329%; vs 1 REMEDIED_WRONG_APPLY |
| `TISSUE-OPT-QO` | Optics, Quantum_Optics | Wave and photon are adjacent D=10/11 of one light; same C=π/e | |S_opt|/|S_qo| vs 1 at 0.0265%; CRC n_D photon fold 0.016% |
| `TISSUE-QM-ATOMIC` | Quantum_Mechanics, Atomic_Physics | Orbit and bound well are adjacent D=6/7 of one hydrogen; equalize the look | same-look D=6/7 vs 1 at 0.046%; IE_H seed 0.070%; NIST H–Ca IE/a0/R∞ dual-routed; mixed vs 1 retired |
| `TISSUE-EM-OPT` | Electromagnetism, Optics | Source and readout are adjacent D=9/10 of one light; ε_opt=n²; inverse C | same-look D=9/10 vs 1 at 0.024%; CRC n² on EM 0.021%; ice ε vs (φ²/2)² 0.0026%; mixed vs 1 retired |
| `TISSUE-BIO-BIOCHEM` | Biology, Biochemistry | Organism and molecule are adjacent D=12/13 of one life; Biology stays dark | dark same-look D=12/13 vs 1 at 0.053%; NCBI mt-operon + AA MW 0.015–0.022%; not Genetics 0.13 Å; mixed vs 1 retired |
| `TISSUE-ATOMIC-HEP` | Atomic_Physics, High_Energy_Physics | Bound well and collision are two looks at D=7; fold 0.85/0.95 onto QM | look-split vs QM rung 0.042%; CODATA m_e/m_p + IE_H dual-route; vs 1 retired |
| `TISSUE-CHEM-PC` | Chemistry, Physical_Chemistry | Composition and thermo are two looks at D=8; 0.5/0.6 is the mat-opt look-split | S-ratio vs mat-opt look-split 0.328%; CRC rho/MW vs Tm/Tb 0.017–0.041%; vs 1 retired |
| `TISSUE-CHEM-MOL` | Chemistry, Molecular_Chemistry | Composition and molecule are adjacent D=8/9; equalize the chemistry look | same-look D=8/9 vs 1 at 0.020%; CRC MW dual-routed; mixed vs 1 retired |
| `TISSUE-PC-MOL` | Physical_Chemistry, Molecular_Chemistry | Thermo and molecule already share δψ=0.5 on adjacent D=8/9 | live |S| vs 1 at 0.167% (looks matched); CRC Tm vs MW dual-routed |
| `TISSUE-AC-OPT` | Acoustics, Optics | Lab sound and light are two looks at D=10; fold 0.3/0.6 onto D=9 | look-split vs D=9 at 0.258%; CRC c vs n 0.013–0.016%; vs 1 retired |
| `TISSUE-AC-MAT` | Acoustics, Materials_Science | Lab sound and bulk density are two looks at D=10; fold 0.3/0.5 onto D=9 | look-split vs D=9 at 0.077%; CRC c vs ρ; vs 1 retired |
| `TISSUE-MOL-AC` | Molecular_Chemistry, Acoustics | Molecule and lab sound are adjacent D=9/10; equalize δψ=0.5 | same-look D=9/10 vs 1 at 0.205%; CRC MW vs c; mixed vs 1 retired |
| `TISSUE-CM-THERMO` | Condensed_Matter, Thermodynamics | Solid and heat are adjacent D=14/15; equalize the CM look | same-look D=14/15 vs 1 at 0.233%; CRC metal ρ vs Tm; mixed vs 1 retired |
| `TISSUE-EM-MAT` | Electromagnetism, Materials_Science | Field and bulk are adjacent D=9/10; equalize the materials look | same-look D=9/10 vs 1 at 0.205%; CRC n² vs ρ; mixed vs 1 retired |
| `TISSUE-BIOCHEM-NEURO` | Biochemistry, Neuroscience | Molecule and signaling are adjacent D=13/14; not the social-tank GDP route | same-look D=13/14 vs 1 at 0.179%; transmitter AA MW; mixed vs 1 retired |
| `TISSUE-ATOMIC-CHEM` | Atomic_Physics, Chemistry | Bound well and composition are adjacent D=7/8; equalize the chemistry look | same-look D=7/8 at δψ=0.6; NIST IE + CRC MW |
| `TISSUE-ATOMIC-PC` | Atomic_Physics, Physical_Chemistry | Bound well and thermo are adjacent D=7/8; equalize δψ=0.5 | same-look D=7/8 at δψ=0.5; NIST IE + CRC Tm |
| `TISSUE-HEP-CHEM` | High_Energy_Physics, Chemistry | Collision and composition are adjacent D=7/8; equalize δψ=0.6 | same-look D=7/8 at δψ=0.6; NIST IE on HEP + CRC MW |
| `TISSUE-HEP-PC` | High_Energy_Physics, Physical_Chemistry | Collision and thermo are adjacent D=7/8; equalize δψ=0.5 | same-look D=7/8 at δψ=0.5; NIST IE on HEP + CRC Tm |
| `TISSUE-PC-EM` | Physical_Chemistry, Electromagnetism | Thermo and field are adjacent D=8/9; equalize δψ=0.5 | same-look D=8/9 at δψ=0.5; CRC Tm + n² |
| `TISSUE-EM-MOL` | Electromagnetism, Molecular_Chemistry | Field and molecule are two looks at D=9; fold 0.7/0.5 onto D=8 | look-split vs D=8; CRC n² vs MW; vs 1 retired |
| `TISSUE-MOL-MAT` | Molecular_Chemistry, Materials_Science | Molecule and bulk are adjacent D=9/10 already sharing δψ=0.5 | matched-look live |S| vs 1; CRC MW vs density |
| `TISSUE-MOL-OPT` | Molecular_Chemistry, Optics | Molecule and light are adjacent D=9/10; equalize δψ=0.5 | same-look D=9/10 at δψ=0.5; CRC MW vs n; mixed vs 1 retired |
| `TISSUE-AC-QO` | Acoustics, Quantum_Optics | Lab sound and photon are adjacent D=10/11; equalize the light look | same-look D=10/11 at δψ=0.6; CRC c vs n |
| `TISSUE-MAT-QO` | Materials_Science, Quantum_Optics | Bulk and photon are adjacent D=10/11; equalize δψ=0.5 | same-look D=10/11 at δψ=0.5; CRC ρ vs n |
| `TISSUE-NUC-THERMO` | Nuclear_Physics, Thermodynamics | Orifice and heat are two looks at D=15; fold 1/0.9 onto D=14 | look-split vs D=14; ENDF keV + Carnot dual-route |
| `TISSUE-FLUID-THERMO` | Fluid_Dynamics, Thermodynamics | Tank and heat share D=15; Fluid stays dark | Carnot COP dual-route; live vs 1 is observed mix |
| `TISSUE-METEO-ATM` | Meteorology, Atmospheric_Physics | Weather and air tank are adjacent dark CHAOS rungs D=16/17 | dark same-look δψ=0.8; NDBC pressure; do not flip dark |
| `TISSUE-BIOCHEM-CM` | Biochemistry, Condensed_Matter | Molecule and solid are adjacent D=13/14; equalize the CM look | same-look D=13/14 at δψ=0.5; CRC AA MW vs metal ρ |
| `TISSUE-CM-NEURO` | Condensed_Matter, Neuroscience | Solid and signaling are two looks at D=14; fold onto D=13 | look-split 0.5/0.7 onto D=13; CRC ρ vs transmitter AA; vs 1 retired |
| `TISSUE-CM-FLUID` | Condensed_Matter, Fluid_Dynamics | Ice and water are one H2O, solid vs tank; Fluid stays dark | CRC ice ρ on CM, water ρ on Fluid; live vs 1 is observed mix |
| `TISSUE-CM-NUC` | Condensed_Matter, Nuclear_Physics | Lattice and orifice are adjacent D=14/15; Fe is the shared class | same-look D=14/15 at δψ=0.5; CRC ρ + ENDF keV dual-route |
| `TISSUE-NEURO-THERMO` | Neuroscience, Thermodynamics | Signaling and heat are adjacent D=14/15; not the social-tank GDP route | same-look D=14/15 at δψ=0.7 hits=1; transmitter AA vs Carnot |
| `TISSUE-FLUID-NUC` | Fluid_Dynamics, Nuclear_Physics | Tank and orifice share D=15; Fluid stays dark | Carnot + ENDF dual-route; live vs 1 is observed mix |
| `TISSUE-FLUID-METEO` | Fluid_Dynamics, Meteorology | Lab tank and weather are adjacent dark rungs D=15/16 | dark same-look δψ=0.8 hits=2; NDBC pressure; do not flip dark |
| `TISSUE-NEURO-FLUID` | Neuroscience, Fluid_Dynamics | Signaling and tank are adjacent D=14/15; Fluid stays dark | transmitter AA vs CRC water ρ; live vs 1 is observed mix |
| `TISSUE-NEURO-NUC` | Neuroscience, Nuclear_Physics | Signaling and orifice are adjacent D=14/15; equalize the neural look | same-look D=14/15 at δψ=0.7 hits=1; AA vs ENDF keV |
| `TISSUE-THERMO-METEO` | Thermodynamics, Meteorology | Heat and weather are adjacent D=15/16; Meteo stays dark | Carnot + NDBC pressure; live vs 1 is observed mix |
| `TISSUE-NUC-METEO` | Nuclear_Physics, Meteorology | Orifice and weather are adjacent D=15/16; Meteo stays dark | ENDF keV + NDBC pressure; do not flip dark |
| `TISSUE-METEO-OCEAN` | Meteorology, Oceanography | Weather and ocean tank are adjacent dark rungs D=16/17 | dark same-look δψ=0.8 hits=2; NDBC pressure; do not flip dark |
| `TISSUE-ATM-SEIS` | Atmospheric_Physics, Seismology | Air tank and crust are adjacent dark rungs D=17/18 | NDBC pressure + PREM lithosphere density; both stay dark |
| `TISSUE-OCEAN-SEIS` | Oceanography, Seismology | Ocean tank and crust are adjacent dark rungs D=17/18 | NDBC SST + PREM lithosphere density; both stay dark |
| `TISSUE-ASTRO-PLANET` | Astronomy, Planetary_Science | Sky and body are adjacent D=20/21; equalize the astronomy look | same-look D=20/21 at δψ=1; JPL densities via APPLY not identity pad |
| `TISSUE-QO-BIO` | Quantum_Optics, Biology | Photon and organism are adjacent D=11/12; Biology stays dark | dark same-look δψ=0.08; CRC n vs NCBI mt-operon; do not flip dark |
| `TISSUE-ATM-SOC` | Atmospheric_Physics, Sociology | Air tank and catalog tank are adjacent D=17/18; Atm stays dark | NDBC pressure + World Bank YoY; do not flip dark |
| `TISSUE-OCEAN-SOC` | Oceanography, Sociology | Ocean tank and catalog tank are adjacent D=17/18; Ocean stays dark | NDBC SST + World Bank YoY; do not flip dark |
| `TISSUE-SEIS-SOC` | Seismology, Sociology | Crust and catalog share D=18; Seismology stays dark | PREM lithosphere + World Bank YoY; live vs 1 is observed mix |
| `TISSUE-SOC-GEO` | Sociology, Geophysics | Catalog and bulk-earth are adjacent D=18/19; Geo stays dark | World Bank YoY + PREM lithosphere density |
| `TISSUE-GEO-ASTRO` | Geophysics, Astronomy | Bulk-earth and sky are adjacent D=19/20; Geo stays dark | PREM lithosphere + JPL densities |
| `TISSUE-GEO-ECON` | Geophysics, Economics | Bulk-earth and market are adjacent D=19/20; Geo stays dark | PREM lithosphere + World Bank YoY |
| `TISSUE-ASTRO-ECON` | Astronomy, Economics | Sky and market are two looks at D=20; fold onto D=19 | look-split 1.0/1.5 onto D=19; JPL + World Bank; vs 1 retired |
| `TISSUE-ECON-PLANET` | Economics, Planetary_Science | Market and body are adjacent D=20/21; equalize the astronomy look | same-look D=20/21 at δψ=1; World Bank YoY + JPL densities |
| `TISSUE-PLANET-QG` | Planetary_Science, Quantum_Gravity | Body and ceiling are adjacent D=21/22; QG stays dark | JPL densities + compact remainder; do not flip QG |
| `TISSUE-ASTROPHYS-PA` | Astrophysics, Particle_Astrophysics | Star and cosmic-ray share D=24; PA stays dark | PDG 2024 measured masses via APPLY; live vs 1 is observed mix |
| `TISSUE-QC-AC` | Acoustics, Quantum_Computing | Lab sound and Hilbert are adjacent D=10/11; QC stays dark | dark same-look δψ=0.5; CRC c vs n; do not flip Hilbert |
| `TISSUE-QC-MAT` | Materials_Science, Quantum_Computing | Bulk and Hilbert are adjacent D=10/11; QC stays dark | CRC ρ vs n; do not flip Hilbert |
| `TISSUE-QC-OPT` | Optics, Quantum_Computing | Wave and Hilbert are adjacent D=10/11; QC stays dark | CRC n dual-route; do not flip Hilbert |
| `TISSUE-QC-QO` | Quantum_Computing, Quantum_Optics | Hilbert and photon share D=11; QC stays dark | CRC n dual-route; live vs 1 is observed mix |
| `TISSUE-QC-BIO` | Quantum_Computing, Biology | Hilbert and organism are adjacent D=11/12; both stay dark | dark same-look δψ=0.08; CRC n vs NCBI mt-operon |
| `TISSUE-CM-ECO` | Condensed_Matter, Ecology | Solid and habitat are adjacent D=14/15; Ecology stays dark | CRC metal ρ + GBIF decimalLatitude; no invented watts |
| `TISSUE-NEURO-ECO` | Neuroscience, Ecology | Signaling and habitat are adjacent D=14/15; Ecology stays dark | transmitter AA + GBIF latitude |
| `TISSUE-ECO-FLUID` | Ecology, Fluid_Dynamics | Habitat and tank share D=15; both stay dark | GBIF latitude + CRC water ρ |
| `TISSUE-ECO-NUC` | Ecology, Nuclear_Physics | Habitat and orifice share D=15; Ecology stays dark | GBIF latitude + ENDF keV |
| `TISSUE-ECO-THERMO` | Ecology, Thermodynamics | Habitat and heat share D=15; Ecology stays dark | GBIF latitude + Carnot COP |
| `TISSUE-ECO-METEO` | Ecology, Meteorology | Habitat and weather are adjacent dark rungs D=15/16 | GBIF latitude + NDBC pressure; both stay dark |
| `TISSUE-ECO-PSYCH` | Ecology, Psychology | Habitat and psychometric scale are adjacent D=15/16; Ecology stays dark | GBIF latitude + Nunnally/Cohen anchors; not watts |
| `TISSUE-FLUID-PSYCH` | Fluid_Dynamics, Psychology | Tank and psychometric scale are adjacent D=15/16; Fluid stays dark | CRC water ρ + Nunnally/Cohen; not watts |
| `TISSUE-NUC-PSYCH` | Nuclear_Physics, Psychology | Orifice and psychometric scale are adjacent D=15/16 | ENDF keV + Nunnally/Cohen; not watts |
| `TISSUE-THERMO-PSYCH` | Thermodynamics, Psychology | Heat and psychometric scale are adjacent D=15/16 | Carnot COP + Nunnally/Cohen; not watts |
| `TISSUE-METEO-PSYCH` | Meteorology, Psychology | Weather and psychometric scale share D=16; Meteo stays dark | NDBC pressure + Nunnally/Cohen; not watts |
| `TISSUE-PSYCH-ATM` | Psychology, Atmospheric_Physics | Psychometric scale and air tank are adjacent D=16/17; Atm stays dark | Nunnally/Cohen + NDBC pressure; not watts |
| `TISSUE-PSYCH-OCEAN` | Psychology, Oceanography | Psychometric scale and ocean tank are adjacent D=16/17; Ocean stays dark | Nunnally/Cohen + NDBC SST; not watts |

Between-scale panel pooled **0.027% GREEN** (7520 tight). D9: live |S| vs 1 is T1 view (T3 leftover 0.000%). Kill: fit Q/γ/Poisson, stuff deep-PREM, or gate live vs 1 at 0.5%.

## 6. Ungated adjacent cores (connective simulation queue)

**0 ungated.** Every adjacent core pair with a public table is a gated tissue (86). Refresh `python scripts/build_scale_interconnect_benchmark.py`.
Do not invent watts or flip dark folds to manufacture a new pair.

## 7. Scientific depth still thin (measured C_thin)

Process/certificate spines are omitted. These are the panels that are green
but have fewer than 20 records — APPLY + public table, not a new domain.

| Domain | Records | Pooled % |
|--------|--------:|---------:|
| SH0ES_Ladder_Chain | 5 | 0.3284 |
| SH0ES_Full_Sample | 11 | 0.1410 |
| Cepheid_PL_Interconnect | 12 | 0.1350 |

## 8. Largest green residuals (honest, not stuffed)

| Domain | Records | Pooled % |
|--------|--------:|---------:|
| Zebrafish_Predictive_Validation_Panel | 20 | 0.3580 |
| SH0ES_Ladder_Chain | 5 | 0.3284 |
| SH0ES_Full_Sample | 11 | 0.1410 |
| Cepheid_PL_Interconnect | 12 | 0.1350 |
| Econometrics | 172 | 0.1292 |
| Economics | 157 | 0.1292 |
| Neuroeconomics | 65 | 0.1050 |
| Maillard_Chemistry | 30 | 0.0944 |
| Architecture_Building_Science | 43 | 0.0787 |
| CODATA_Full_Table_Open | 38 | 0.0736 |
| immunology_benchmark | 84 | 0.0612 |
| Observer_Channel_Derivation | 372 | 0.0525 |

## 9. Science vs FSOT (how to use this as a tool)

You were reaching for this loop:

1. **Name the object** science published (Perfect Host 73.49, DES-alone S8,
   cryo-EM FSC Å, DESI wa combination, …).
2. **Map it to the FSOT lock** (bridge / dual-anchor / class / product /
   no-map). Wrong object = false kill. [`OBJECT_SCORING.md`](OBJECT_SCORING.md).
3. **If the physical outcome agrees** (same H0 sector, same b≈1, same 20 W,
   same 0.5% residual) — that is a **hold**, then cross-check a *second*
   public table (CCHP vs SH0ES, joint S8 vs DES-alone, Genetics product vs AF).
4. **If FSOT explains better with the same outcome** (one valve not two
   cosmologies; homolog product not sequence-only AF; quiet/storm as sectors)
   — that is the distinctive claim. Keep the outcome; do not retune the central.
5. **If science has no date/place and FSOT issues a window** — score after
`valid_to`. Never rewrite the issue.

Standing compare: [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) · `results/literature/` ·
`predictions/reports/SCIENTIST_OPEN_QUESTIONS.md`. Do not ingest arXiv as a residual.

## 10. Next work (ranked)

| ID | Do this | Do not |
|----|---------|--------|
| `NW-LAWS` | Keep this laws ledger live. Do not add a law that is not engine or a named solve. | 35 founding discrepancy names as if they were Newton's laws. |
| `NW-TISSUE` | Adjacent ungated cores are 0. Keep κ_ij dual-route residuals live on interconnect refresh. Do not hunt a new pair for its own sake. | A free coupling coefficient. More isolated green files. |
| `NW-APPLY` | Worked APPLY cookbooks cover the remaining high-value cores (Materials, Acoustics, Fluid, Nuclear, Thermo, Chemistry ladder, Neuroscience, Astronomy). Satellite folds use the neighbor page. Keep each cookbook honest to the named public table. | A second math key. |
| `NW-OBJECT` | Keep OBJECT_COMPARE live: arXiv/PDG/survey papers scored against the named lock. Append via record_prediction_outcome.py. Refresh python scripts/build_object_compare.py. | Retuning fsot_predicted when a paper lands. |
| `NW-CTHIN` | Remaining measured C_thin are SH0ES/Cepheid headline objects (chain, full NIR sample, PL interconnect). Densify only with the next published named table (more JWST TRGB hosts / host-mean mixture). Do not pad with identical-fraction APPLY copies. | Process/certificate spines counted as scientific depth. Per-star photometry as a median pad. |
| `NW-DATED` | Dated windows: public scoreboard hold 65 / kill 45 / awaiting 4 (missing NDBC 45144/45145/46208/62146). 2026-09-09 issue uses corrected hydro IDs (06934500 Hermann). Honchō/Kermadec loading misses stay honest. Score after valid_to. | Rewriting issued JSON. Clock-time hypocenter. |
| `NW-CASP` | Genetics CASP/CAMEO blind protocol (Grok Build owns the run). | Quoting 0.13 Å as sequence-only. Cross-citing FSC Å. |
| `NW-OPEN` | T3/T4 uniqueness / path-integral confinement stays open research. Euclid DR1 12 Nov 2026 is a watch. | Pretending Label B uniqueness is proved. Euclid CLOE as measured. |

Adjacent cores with public tables are gated. Remaining policy holds:
QC stays dark (Hilbert). Ecology/Psychology use GBIF and Nunnally/Cohen,
not invented watts. ISO-SHOES-CLASS-BIN 1% stays frozen — work the chain
and next published mixture, do not retune ρ. Not a new theory.

Related: [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) · [`HOLE_AUDIT.md`](HOLE_AUDIT.md) ·
[`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md) · [`APPLY.md`](APPLY.md) ·
[`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md)
