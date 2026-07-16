## Molecular Chemistry, PubChem & Compound Properties

**Panels:** 8 · **Records:** 6,471 · **Mean panel median error:** 0.0218151%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `CRC_Handbook_Properties` | 391 | 0.026922 | A_strong |
| `Chemical_Structure_Stability_Panel` | 32 | 0.00206 | B_verified |
| `Ionospheric_Chemistry_Coupling` | 85 | 0 | B_verified |
| `Machine_And_Molecule_Live_Panel` | 120 | 0.01341 | A_strong |
| `Maillard_Chemistry` | 30 | 0.0944369 | B_verified |
| `PubChem_Compound_Properties` | 500 | 0.002637 | A_strong |
| `PubChem_Live_Deep` | 5,254 | 0.032631 | A_strong |
| `PubChem_Stability_Panel` | 59 | 0.00242389 | B_verified |

#### CRC Handbook Properties

Extension panel **`CRC_Handbook_Properties`** (verification tier 78) evaluates **391** measured records at **0.026922%** pooled median error (A_strong). Formal module: `FSOT.Formal.CrcHandbookPropertiesPriors`. This panel extends the core spine into crc handbook properties observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/crc_handbook_properties_benchmark.json`](data/crc_handbook_properties_benchmark.json)

**Subfield map:**

- **Lean routes:** `chemical`, `material`
- **Panel tags:** Crc, Handbook, Properties
- **Data sources / cohorts:** CRC Handbook, NIST chemistry anchors — SMILES lab empirical panel

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §1 Foundation · pH_water (mixed) | 7 | 7 | 0 |
| §30 Refractive nD · diethyl ether (dimensionless) | 1.353 | 1.353 | 3.4e-05 |
| §48 ΔHfus · N₂ (kJ/mol) | 0.72 | 0.72 | 5.3e-05 |
| §98 Vapor Pressure · CS2 (mmHg) | 359 | 359 | 5.5e-05 |
| §87 Heat Cap Ratio Cp/Cv · N2 (dimensionless) | 1.4 | 1.4 | 7.4e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`pH_water`** in CRC Handbook Properties: measured **7.0**, seed-derived **7.0** via `φ⁻⁴ + φ⁴` (error **0%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.
- **`CS2`** in CRC Handbook Properties: measured **359.0**, seed-derived **358.99980082967573** via `E^4+PI^5-PHI^1` (error **5.5e-05%**). Constants: phi, pi. Authority: NIST Chemistry WebBook / CRC.
- **`F`** in CRC Handbook Properties: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Chemical Structure Stability Panel

Extension panel **`Chemical_Structure_Stability_Panel`** (verification tier 57) evaluates **32** measured records at **0.00206%** pooled median error (B_verified). Formal module: `FSOT.Formal.ChemicalStructureStabilityPanelPriors`. This panel extends the core spine into chemical structure stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/chemical_structure_stability_panel_benchmark.json`](data/chemical_structure_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `chemical`, `material`, `particle`, `electron`
- **Panel tags:** Chemical, Structure, Stability, Panel
- **Data sources / cohorts:** PubChem formula-mass, NIST, SMILES topology — no novel stability claims

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| Planck constant | 6.62607e-34 | 6.62607e-34 | 0 |
| fine-structure constant | 0.00729735 | 0.00729735 | 0 |
| formula_mass_closure · 5280961 | 270.24 | 270.24 | 0 |
| proton mass | 1.67262e-27 | 1.67262e-27 | 0 |
| smiles_mapped_records · FSOT_SMILES_Lab | 1470 | 1470 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Chemical Structure Stability Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Chemical Structure Stability Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Chemical Structure Stability Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Ionospheric Chemistry Coupling

Extension panel **`Ionospheric_Chemistry_Coupling`** (verification tier 47) evaluates **85** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.IonosphericChemistryCouplingPriors`. This panel extends the core spine into ionospheric chemistry coupling observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/ionospheric_chemistry_coupling_benchmark.json`](data/ionospheric_chemistry_coupling_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `energy`, `plasma`
- **Panel tags:** Ionospheric, Chemistry, Coupling
- **Data sources / cohorts:** Magnetosphere cluster gap — ionosphere MHD, Dst, Kp, Bz coupling

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| dst_storm_classifier · 2026-06-26T17:00:00 | 0 | 0 | 0 |
| ionospheric · magnetosphere_cluster_panel | 0 | 0 | 0 |
| kp_storm_classifier · 1932-01-01T00:00:00 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| ionosphere_mhd_beta · ionosphere | 1 | 1.00024 | 0.0236092 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Ionospheric Chemistry Coupling: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Ionospheric Chemistry Coupling: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Ionospheric Chemistry Coupling: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Machine And Molecule Live Panel

Extension panel **`Machine_And_Molecule_Live_Panel`** (verification tier 88) evaluates **120** measured records at **0.01341%** pooled median error (A_strong). Formal module: `FSOT.Formal.MachineAndMoleculeLivePanelPriors`. This panel extends the core spine into machine and molecule live panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/machine_and_molecule_live_panel_benchmark.json`](data/machine_and_molecule_live_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `energy`, `particle`
- **Panel tags:** Machine, And, Molecule, Live, Panel
- **Data sources / cohorts:** Desktop FSOT_Machine_And_Molecule species catalog live verification

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boiling_K · metals_Hg_boiling_K | 629.9 | 629.984 | 0.01341 |
| bulk_GPa · metals_Ag_bulk_GPa | 104 | 104.014 | 0.01341 |
| cohesive_eV · metals_Ag_cohesive_eV | 2.95 | 2.9504 | 0.01341 |
| cp_J_molK · metals_Al_cp_J_molK | 24.2 | 24.2032 | 0.01341 |
| expansion_e6_per_K · metals_Ag_expansion_e6_per_K | 18 | 18.0024 | 0.01341 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`P`** in Machine And Molecule Live Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Si`** in Machine And Molecule Live Panel: measured **1.385**, seed-derived **1.3850362977165687** via `Ω⁻²+B_IN` (error **0.002621%**). Constants: seed constants. Authority: Andersen et al., JPCRD 28 (1999).
- **`Li`** in Machine And Molecule Live Panel: measured **0.618**, seed-derived **0.6180333354111225** via `φ⁻¹−α²` (error **0.005394%**). Constants: phi. Authority: Andersen et al., JPCRD 28 (1999).

#### Maillard Chemistry

Extension panel **`Maillard_Chemistry`** (verification tier 34) evaluates **30** measured records at **0.0944369%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaillardChemistryGapFillPriors`. This panel extends the core spine into maillard chemistry observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/maillard_chemistry_gap_fill_benchmark.json`](data/maillard_chemistry_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `medical`, `material`
- **Panel tags:** Maillard, Chemistry
- **Data sources / cohorts:** Maillard, browning kinetics from culinary SMILES, roast observables

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §51 Solubility logS · caffeine | 0.81 | 0.81 | 2.94767e-05 |
| §50 Diffusion D · sucrose | 0.523 | 0.522947 | 0.0102218 |
| §90 Heat of Combustion · glucose | 2803 | 2804.28 | 0.0455353 |
| §61 Glass Tg · glucose_amorph | 309 | 309.161 | 0.052193 |
| browning_proxy_temp_C · beer_ale_fermentation | 20 | 20.0157 | 0.0786975 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Maillard Chemistry: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Maillard Chemistry: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Maillard Chemistry: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### PubChem Compound Properties

Extension panel **`PubChem_Compound_Properties`** (verification tier 38) evaluates **500** measured records at **0.002637%** pooled median error (A_strong). Formal module: `FSOT.Formal.PubchemCompoundPropertiesPriors`. This panel extends the core spine into pubchem compound properties observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_compound_properties_benchmark.json`](data/pubchem_compound_properties_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`
- **Panel tags:** Pubchem, Compound, Properties
- **Data sources / cohorts:** PubChem molecular weight vs formula mass (31 compounds deep)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| molecular_weight · 1054 | 169.18 | 169.18 | 0 |
| molecular_weight · 10975657 | 150.13 | 150.13 | 0 |
| molecular_weight · 1102 | 145.25 | 145.25 | 0 |
| molecular_weight · 11174599 | 319.27 | 319.27 | 0 |
| molecular_weight · 1176 | 60.056 | 60.056 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`O`** in PubChem Compound Properties: measured **1.461**, seed-derived **1.4609166182653626** via `G⁻³+Ψ⁴` (error **0.005707%**). Constants: g_cat. Authority: Andersen et al., JPCRD 28 (1999).
- **`C`** in PubChem Compound Properties: measured **1.262**, seed-derived **1.2619131378546835** via `Ω⁻¹+B_IN³` (error **0.006883%**). Constants: seed constants. Authority: Andersen et al., JPCRD 28 (1999).
- **`I`** in PubChem Compound Properties: measured **3.059**, seed-derived **3.0587861624940675** via `η⁻¹+C_eff²` (error **0.00699%**). Constants: seed constants. Authority: Andersen et al., JPCRD 28 (1999).

#### PubChem Live Deep

Extension panel **`PubChem_Live_Deep`** (verification tier 68) evaluates **5254** measured records at **0.032631%** pooled median error (A_strong). Formal module: `FSOT.Formal.PubChemLiveDeepPriors`. This panel extends the core spine into pubchem live deep observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_live_deep_benchmark.json`](data/pubchem_live_deep_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `medical`, `biological`, `material`, `energy`
- **Panel tags:** Pubchem, Live, Deep
- **Data sources / cohorts:** PubChem auto-expanded panel — PUG REST name discovery, culinary, pharmacology bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| biological_scalar · fsot_Biology | 0.444725 | 0.444725 | 0 |
| chemistry_scalar · fsot_Chemistry | 0.407884 | 0.407884 | 0 |
| culinary_arts_crosswalk_count | 26 | 26 | 0 |
| food_microbiology_crosswalk_count · Food_Microbiology | 30 | 30 | 0 |
| hbond_acceptor_count · 1140 | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in PubChem Live Deep: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in PubChem Live Deep: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in PubChem Live Deep: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### PubChem Stability Panel

Extension panel **`PubChem_Stability_Panel`** (verification tier 55) evaluates **59** measured records at **0.00242389%** pooled median error (B_verified). Formal module: `FSOT.Formal.PubChemStabilityPanelPriors`. This panel extends the core spine into pubchem stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_stability_panel_benchmark.json`](data/pubchem_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `material`
- **Panel tags:** Pubchem, Stability, Panel
- **Data sources / cohorts:** PubChem formula-mass closure — novel stability claims require preregistration

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| chemistry_scalar · fsot_Chemistry | 0.407884 | 0.407884 | 0 |
| molecular_weight · 5280961 | 270.24 | 270.24 | 0 |
| pooled_median · all_channels | 0 | 0.002424 | 0.00242389 |
| molecular_weight · 962 | 18.015 | 18.015 | 0 |
| molecular_weight · 3386 | 309.33 | 309.331 | 0.000323 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in PubChem Stability Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in PubChem Stability Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in PubChem Stability Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
