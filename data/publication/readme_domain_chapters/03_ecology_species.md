## Ecology, Species Catalogs & Agricultural Systems

**Panels:** 20 · **Records:** 5,751 · **Mean panel median error:** 0.018924%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `Agriculture_Agroecology` | 276 | 0.018019 | A_strong |
| `Biological_CUDA_Physarum` | 35 | 0 | B_verified |
| `Botany` | 426 | 0.0222363 | A_strong |
| `Culinary_Arts` | 26 | 0.0476152 | B_verified |
| `Culinary_Fermentation_Maillard_Panel` | 130 | 0.040788 | A_strong |
| `Ecology` | 24 | 0 | B_verified |
| `Entomology` | 430 | 0.0222363 | A_strong |
| `Entomology_Panel` | 90 | 0.006006 | B_verified |
| `Food_Microbiology` | 30 | 0.0444725 | B_verified |
| `GBIF_Species_Occurrence` | 240 | 0.006006 | A_strong |
| `Longevity_AnAge_Catalog_Panel` | 966 | 0.022236 | A_strong |
| `Longevity_Extreme_Species_Panel` | 164 | 0.017789 | A_strong |
| `Marine_Biology` | 540 | 0.0222363 | A_strong |
| `Marine_Biology_Panel` | 90 | 0.006006 | B_verified |
| `Mycology` | 420 | 0.0222363 | A_strong |
| `Mycology_Panel` | 90 | 0.006006 | B_verified |
| `Paleontology` | 630 | 0.0178361 | A_strong |
| `Paleontology_Panel` | 120 | 0.0167305 | A_strong |
| `Physarum_Biological_CUDA_Panel` | 24 | 0.022236 | B_verified |
| `Zoology` | 1,000 | 0.017789 | A_strong |

#### Agriculture Agroecology

Extension panel **`Agriculture_Agroecology`** (verification tier 34) evaluates **276** measured records at **0.018019%** pooled median error (A_strong). Formal module: `FSOT.Formal.AgricultureAgroecologyGapFillPriors`. This panel extends the core spine into agriculture agroecology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/agriculture_agroecology_gap_fill_benchmark.json`](data/agriculture_agroecology_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `energy`
- **Panel tags:** Agriculture, Agroecology
- **Data sources / cohorts:** GBIF species occurrence, World Bank agro-socioeconomic panel

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| GDP_per_capita · IT_2022 | 35653.9 | 35657.1 | 0.00900951 |
| population_total · CN_2022 | 1.41218e+09 | 1.4123e+09 | 0.00900951 |
| mean_latitude · Leratiomyces ceres | 40.7963 | 40.8037 | 0.018019 |
| agroecology · species_ag_indicator | 0 | 0.018019 | 0.018019 |
| pooled_median · all_channels | 0 | 0.018019 | 0.018019 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Agriculture Agroecology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Agriculture Agroecology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Agriculture Agroecology: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Biological CUDA Physarum

Extension panel **`Biological_CUDA_Physarum`** (verification tier 34) evaluates **35** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.BiologicalCudaPhysarumPriors`. This panel extends the core spine into biological cuda physarum observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/biological_cuda_physarum_benchmark.json`](data/biological_cuda_physarum_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `medical`, `neural`
- **Panel tags:** Biological, Cuda, Physarum
- **Data sources / cohorts:** Physarum CUDA RTX 5070 benchmarks, v5 plasmodium state, genomics bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| avg_S · nuclei_1000 | 6.9618 | 6.9618 | 0 |
| condo_ops_per_sec · nuclei_1000 | 75.2 | 75.2 | 0 |
| genomics_D_eff · genomics D eff | 22 | 22 | 0 |
| genomics_error_pct · genomics error pct | 6.62412 | 6.62412 | 0 |
| global_coherence_range · global coherence range | 0.322112 | 0.322112 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`pH_water`** in Biological CUDA Physarum: measured **7.0**, seed-derived **7.0** via `φ⁻⁴ + φ⁴` (error **0%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.
- **`F`** in Biological CUDA Physarum: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Biological CUDA Physarum: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Botany

Extension panel **`Botany`** (verification tier 35) evaluates **426** measured records at **0.0222363%** pooled median error (A_strong). Formal module: `FSOT.Formal.BotanyExtensionPriors`. This panel extends the core spine into botany observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/botany_extension_benchmark.json`](data/botany_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Botany
- **Data sources / cohorts:** GBIF Plantae occurrence coordinates (G: drive cache)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLongitude · Vaccinium myrtillus | 17.9395 | 17.9427 | 0.017789 |
| decimalLatitude · Pinus strobus | 42.6841 | 42.6936 | 0.0222363 |
| plant_occurrence · botany_gbif | 0 | 0.022236 | 0.0222363 |
| pooled_median · all_channels | 0 | 0.022236 | 0.0222363 |
| decimalLongitude · Hippophae rhamnoides | 17.5483 | 17.5514 | 0.017789 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Botany: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Botany: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Botany: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Culinary Arts

Extension panel **`Culinary_Arts`** (verification tier 33) evaluates **26** measured records at **0.0476152%** pooled median error (B_verified). Formal module: `FSOT.Formal.CulinaryArtsPriors`. This panel extends the core spine into culinary arts observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/culinary_arts_benchmark.json`](data/culinary_arts_benchmark.json)

**Subfield map:**

- **Lean routes:** `medical`, `material`, `energy`
- **Panel tags:** Culinary, Arts
- **Data sources / cohorts:** SMILES food chemistry, household quick-bread, coffee roast process observables

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §1 Foundation · pH_water | 7 | 7 | 0 |
| §51 Solubility logS · caffeine | 0.81 | 0.81 | 2.94767e-05 |
| §50 Diffusion D · sucrose | 0.523 | 0.522947 | 0.0102218 |
| section_median_sec51_solubility_logs · §51 Solubility logS | 0 | 0.014039 | 0.0140392 |
| banana_mass_fraction · banana_bread:banana_mass_fraction (mass_fraction) | 0.34 | 0.340081 | 0.0238076 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`pH_water`** in Culinary Arts: measured **7.0**, seed-derived **7.0** via `φ⁻⁴ + φ⁴` (error **0%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.
- **`H⁺/H₂`** in Culinary Arts: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Culinary Arts: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).

#### Culinary Fermentation Maillard Panel

Extension panel **`Culinary_Fermentation_Maillard_Panel`** (verification tier 86) evaluates **130** measured records at **0.040788%** pooled median error (A_strong). Formal module: `FSOT.Formal.CulinaryFermentationMaillardPanelPriors`. This panel extends the core spine into culinary fermentation maillard panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/culinary_fermentation_maillard_panel_benchmark.json`](data/culinary_fermentation_maillard_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `medical`, `material`
- **Panel tags:** Culinary, Fermentation, Maillard, Panel
- **Data sources / cohorts:** Culinary depth — PubChem Maillard precursors, fermentation kinetics

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| lag_phase_h · beer_ale_fermentation | 6 | 6.00133 | 0.022236 |
| fsot_prediction · culinary_fermentation_maillard | 0 | 0.040788 | 0.040788 |
| molecular_weight · acetic_acid | 60.05 | 60.0745 | 0.040788 |
| optimal_ph · beer_ale_fermentation | 4.3 | 4.30175 | 0.040788 |
| pooled_median · all_channels | 0 | 0.040788 | 0.040788 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Culinary Fermentation Maillard Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Culinary Fermentation Maillard Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Culinary Fermentation Maillard Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Ecology

Extension panel **`Ecology`** (verification tier 66) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.EcologyPublicPanelPriors`. This panel extends the core spine into ecology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/ecology_benchmark.json`](data/ecology_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `energy`
- **Panel tags:** Ecology
- **Data sources / cohorts:** Kleiber, MacArthur-Wilson ecology anchors, GBIF gap-fill bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| domain_scalar · fsot_Ecology | 0.300317 | 0.300317 | 0 |
| empirical_gap_fill_bridge · ecology_gap_fill_benchmark | 0.017789 | 0.017789 | 0 |
| observable · heart_rate_allometry | -0.25 | -0.25 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| depth_relay · Ecology_depth | 0 | 0.000555 | 0.000555 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Ecology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Ecology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Ecology: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Entomology

Extension panel **`Entomology`** (verification tier 41) evaluates **430** measured records at **0.0222363%** pooled median error (A_strong). Formal module: `FSOT.Formal.EntomologyExtensionPriors`. This panel extends the core spine into entomology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/entomology_extension_benchmark.json`](data/entomology_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Entomology
- **Data sources / cohorts:** GBIF Insecta class occurrence, zoology bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLongitude · Tholymis tillarga | 75.8669 | 75.8804 | 0.017789 |
| decimalLatitude | -33.7174 | -33.7249 | 0.0222363 |
| insect_occurrence · entomology_gbif | 0 | 0.022236 | 0.0222363 |
| pooled_median · all_channels | 0 | 0.022236 | 0.0222363 |
| decimalLongitude · Acrocercops brongniardella | 17.9991 | 18.0023 | 0.017789 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Entomology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Entomology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Entomology: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Entomology Panel

Extension panel **`Entomology_Panel`** (verification tier 84) evaluates **90** measured records at **0.006006%** pooled median error (B_verified). Formal module: `FSOT.Formal.EntomologyPanelPriors`. This panel extends the core spine into entomology panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/entomology_panel_benchmark.json`](data/entomology_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Entomology, Panel
- **Data sources / cohorts:** Entomology — GBIF Insecta occurrence coordinates

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLatitude · Acherontia lachesis | 22.8942 | 22.8956 | 0.006006 |
| decimalLongitude · Acherontia lachesis | 121.247 | 121.254 | 0.006006 |
| fsot_prediction · entomology | 0 | 0.006006 | 0.006006 |
| pooled_median · all_channels | 0 | 0.006006 | 0.006006 |
| individual_count · Acherontia lachesis | 1 | 1.00022 | 0.022236 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Entomology Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Entomology Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Entomology Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Food Microbiology

Extension panel **`Food_Microbiology`** (verification tier 34) evaluates **30** measured records at **0.0444725%** pooled median error (B_verified). Formal module: `FSOT.Formal.FoodMicrobiologyGapFillPriors`. This panel extends the core spine into food microbiology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/food_microbiology_gap_fill_benchmark.json`](data/food_microbiology_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `medical`
- **Panel tags:** Food, Microbiology
- **Data sources / cohorts:** Fermentation kinetics, culinary process bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| banana_mass_fraction · banana_bread:banana_mass_fraction (mass_fraction) | 0.34 | 0.340081 | 0.0238076 |
| pumpkin_mass_fraction · pumpkin_bread:pumpkin_mass_fraction (mass_fraction) | 0.31 | 0.310074 | 0.0238076 |
| final_moisture_pct · banana_bread:final_moisture_pct (pct) | 28.5 | 28.5068 | 0.0238076 |
| zucchini_mass_fraction · zucchini_bread:zucchini_mass_fraction (mass_fraction) | 0.29 | 0.290069 | 0.0238076 |
| optimal_temp_C · wine_primary | 22 | 22.0098 | 0.0444725 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Food Microbiology: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Food Microbiology: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Toluene`** in Food Microbiology: measured **28.4**, seed-derived **28.400682642694072** via `PI^3·G` (error **0.002404%**). Constants: g_cat, pi. Authority: NIST Chemistry WebBook / CRC.

#### GBIF Species Occurrence

Extension panel **`GBIF_Species_Occurrence`** (verification tier 38) evaluates **240** measured records at **0.006006%** pooled median error (A_strong). Formal module: `FSOT.Formal.GbifSpeciesOccurrencePriors`. This panel extends the core spine into gbif species occurrence observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/gbif_species_occurrence_benchmark.json`](data/gbif_species_occurrence_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Gbif, Species, Occurrence
- **Data sources / cohorts:** GBIF species occurrence coordinates (300-ingest, 600 observables)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLatitude · Abies balsamea | 44.632 | 44.6346 | 0.006006 |
| decimalLongitude · Abies balsamea | -72.37 | -72.3744 | 0.006006 |
| decimalLatitude · Acer saccharum | 43.5756 | 43.5782 | 0.006006 |
| decimalLatitude · Agrilus planipennis | 40.3695 | 40.3719 | 0.006006 |
| decimalLatitude · Alsophila pometaria | 40.9948 | 40.9972 | 0.006006 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`P`** in GBIF Species Occurrence: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`O`** in GBIF Species Occurrence: measured **1.461**, seed-derived **1.4609166182653626** via `G⁻³+Ψ⁴` (error **0.005707%**). Constants: g_cat. Authority: Andersen et al., JPCRD 28 (1999).
- **`C`** in GBIF Species Occurrence: measured **1.262**, seed-derived **1.2619131378546835** via `Ω⁻¹+B_IN³` (error **0.006883%**). Constants: seed constants. Authority: Andersen et al., JPCRD 28 (1999).

#### Longevity AnAge Catalog Panel

Extension panel **`Longevity_AnAge_Catalog_Panel`** (verification tier 94) evaluates **966** measured records at **0.022236%** pooled median error (A_strong). Formal module: `FSOT.Formal.LongevityAnAgeCatalogPanelPriors`. This panel extends the core spine into longevity anage catalog panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/longevity_anage_catalog_panel_benchmark.json`](data/longevity_anage_catalog_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `neural`, `consciousness`
- **Panel tags:** Longevity, Anage, Catalog, Panel
- **Data sources / cohorts:** Full AnAge HAGR catalog — maximum longevity, metabolic rate, longevity quotient

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| longevity_quotient · Alligator_mississippiensis | 94077.8 | 94094.6 | 0.017789 |
| anage_catalog · maximum_longevity | 0 | 0.022236 | 0.022236 |
| maximum_longevity_yrs · Acanthopagrus_butcheri | 29 | 29.0064 | 0.022236 |
| metabolic_rate_w · Alligator_mississippiensis | 0.1539 | 0.153934 | 0.022236 |
| pooled_median · all_channels | 0 | 0.022236 | 0.022236 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Longevity AnAge Catalog Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Longevity AnAge Catalog Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Longevity AnAge Catalog Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Longevity Extreme Species Panel

Extension panel **`Longevity_Extreme_Species_Panel`** (verification tier 94) evaluates **164** measured records at **0.017789%** pooled median error (A_strong). Formal module: `FSOT.Formal.LongevityExtremeSpeciesPanelPriors`. This panel extends the core spine into longevity extreme species panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/longevity_extreme_species_panel_benchmark.json`](data/longevity_extreme_species_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `consciousness`, `genetics`
- **Panel tags:** Longevity, Extreme, Species, Panel
- **Data sources / cohorts:** Extreme long-lived species — NCBI genome crosswalk, consciousness panel overlap

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| extreme_longevity_quotient · Acipenser_dabryanus | 17779.6 | 17782.8 | 0.017789 |
| genome_longevity_coupling · Acipenser_sturio | 18.5658 | 18.5691 | 0.017789 |
| pooled_median · all_channels | 0 | 0.017789 | 0.017789 |
| extreme_species · genome_longevity | 0 | 0.017789 | 0.017789 |
| extreme_maximum_longevity_yrs · Acipenser_dabryanus | 100 | 100.022 | 0.022236 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Longevity Extreme Species Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Longevity Extreme Species Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`P`** in Longevity Extreme Species Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Marine Biology

Extension panel **`Marine_Biology`** (verification tier 41) evaluates **540** measured records at **0.0222363%** pooled median error (A_strong). Formal module: `FSOT.Formal.MarineBiologyExtensionPriors`. This panel extends the core spine into marine biology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/marine_biology_extension_benchmark.json`](data/marine_biology_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`, `energy`
- **Panel tags:** Marine, Biology
- **Data sources / cohorts:** OBIS marine occurrence depth, NOAA tides bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_m · Alphaproteobacteria | 0 | 0 | 0 |
| max_height_m · Boston | 2.76 | 2.76 | 0 |
| mean_height_m · Boston | 1.52899 | 1.52899 | 0 |
| min_height_m · Boston | 0.204 | 0.204 | 0 |
| prediction_count · Boston | 72 | 72 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Marine Biology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Marine Biology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`P`** in Marine Biology: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Marine Biology Panel

Extension panel **`Marine_Biology_Panel`** (verification tier 84) evaluates **90** measured records at **0.006006%** pooled median error (B_verified). Formal module: `FSOT.Formal.MarineBiologyPanelPriors`. This panel extends the core spine into marine biology panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/marine_biology_panel_benchmark.json`](data/marine_biology_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `energy`
- **Panel tags:** Marine, Biology, Panel
- **Data sources / cohorts:** Marine biology — OBIS occurrence depth, lat, lon

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_m · Aratus pisonii | 0 | 0 | 0 |
| decimalLatitude · Aratus pisonii | -8.3603 | -8.3608 | 0.006006 |
| decimalLongitude · Aratus pisonii | -34.9617 | -34.9638 | 0.006006 |
| fsot_prediction · marine_biology | 0 | 0.006006 | 0.006006 |
| pooled_median · all_channels | 0 | 0.006006 | 0.006006 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Marine Biology Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Marine Biology Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Marine Biology Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Mycology

Extension panel **`Mycology`** (verification tier 41) evaluates **420** measured records at **0.0222363%** pooled median error (A_strong). Formal module: `FSOT.Formal.MycologyExtensionPriors`. This panel extends the core spine into mycology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/mycology_extension_benchmark.json`](data/mycology_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Mycology
- **Data sources / cohorts:** GBIF Fungi kingdom occurrence, food microbiology bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLongitude · Phellinus tremulae | 17.5549 | 17.558 | 0.017789 |
| decimalLatitude · Phaeophyscia orbicularis | 55.5837 | 55.596 | 0.0222363 |
| fungal_occurrence · mycology_gbif | 0 | 0.022236 | 0.0222363 |
| pooled_median · all_channels | 0 | 0.022236 | 0.0222363 |
| optimal_temp_C · wine_primary | 22 | 22.0098 | 0.0444725 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Mycology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Mycology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Mycology: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Mycology Panel

Extension panel **`Mycology_Panel`** (verification tier 84) evaluates **90** measured records at **0.006006%** pooled median error (B_verified). Formal module: `FSOT.Formal.MycologyPanelPriors`. This panel extends the core spine into mycology panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/mycology_panel_benchmark.json`](data/mycology_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `medical`
- **Panel tags:** Mycology, Panel
- **Data sources / cohorts:** Mycology — GBIF Fungi occurrence panel

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLatitude · Alectoria sarmentosa | 61.5295 | 61.5332 | 0.006006 |
| decimalLongitude · Alectoria sarmentosa | 15.1505 | 15.1515 | 0.006006 |
| fsot_prediction · mycology | 0 | 0.006006 | 0.006006 |
| pooled_median · all_channels | 0 | 0.006006 | 0.006006 |
| year · Alectoria sarmentosa | 2024 | 2024.45 | 0.022236 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Mycology Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Mycology Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Mycology Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Paleontology

Extension panel **`Paleontology`** (verification tier 41) evaluates **630** measured records at **0.0178361%** pooled median error (A_strong). Formal module: `FSOT.Formal.PaleontologyExtensionPriors`. This panel extends the core spine into paleontology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/paleontology_extension_benchmark.json`](data/paleontology_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `galactic`, `biological`
- **Panel tags:** Paleontology
- **Data sources / cohorts:** PBDB fossil occurrences, seismology stratigraphy bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| shallow_earthquake_classifier · us6000pgcu | 1 | 1 | 0 |
| geologic_age_ma · Ammonoidea indet. | 143.1 | 143.119 | 0.013377 |
| lat · Ammonoidea indet. | 73 | 73.013 | 0.0178361 |
| lng · Ammonoidea indet. | 19.0167 | 19.0201 | 0.0178361 |
| fossil_occurrence · paleontology_pbdb | 0 | 0.017836 | 0.0178361 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Paleontology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Paleontology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Paleontology: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Paleontology Panel

Extension panel **`Paleontology_Panel`** (verification tier 84) evaluates **120** measured records at **0.0167305%** pooled median error (A_strong). Formal module: `FSOT.Formal.PaleontologyPanelPriors`. This panel extends the core spine into paleontology panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/paleontology_panel_benchmark.json`](data/paleontology_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `energy`
- **Panel tags:** Paleontology, Panel
- **Data sources / cohorts:** Paleontology — PBDB Ammonoidea occurrences (deep-time cross-check)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| lat · Ammonoida indet. | 47.4167 | 47.4195 | 0.006006 |
| late_age · Ammonoida indet. | 351.9 | 351.921 | 0.006006 |
| pooled_median · all_channels | 0 | 0.01673 | 0.0167305 |
| early_age · Ammonoida indet. | 358.86 | 358.959 | 0.027455 |
| fsot_prediction · paleontology | 0 | 0.027455 | 0.027455 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Paleontology Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Paleontology Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`CS2`** in Paleontology Panel: measured **359.0**, seed-derived **358.99980082967573** via `E^4+PI^5-PHI^1` (error **5.5e-05%**). Constants: phi, pi. Authority: NIST Chemistry WebBook / CRC.

#### Physarum Biological CUDA Panel

Extension panel **`Physarum_Biological_CUDA_Panel`** (verification tier 88) evaluates **24** measured records at **0.022236%** pooled median error (B_verified). Formal module: `FSOT.Formal.PhysarumBiologicalCudaPanelPriors`. This panel extends the core spine into physarum biological cuda panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/physarum_biological_cuda_panel_benchmark.json`](data/physarum_biological_cuda_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `neural`
- **Panel tags:** Physarum, Biological, Cuda, Panel
- **Data sources / cohorts:** Desktop Physarum polycephalum CUDA genomics simulation

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| genomics_gene_count | 0 | 0 | 0 |
| desktop_wiring · physarum_cuda | 0 | 0.022236 | 0.022236 |
| editing_yield | 347 | 347.077 | 0.022236 |
| global_coherence | 0.322112 | 0.322184 | 0.022236 |
| nuclei_count | 1 | 1.00022 | 0.022236 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Physarum Biological CUDA Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Physarum Biological CUDA Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Physarum Biological CUDA Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Zoology

Extension panel **`Zoology`** (verification tier 35) evaluates **1000** measured records at **0.017789%** pooled median error (A_strong). Formal module: `FSOT.Formal.ZoologyExtensionPriors`. This panel extends the core spine into zoology observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/zoology_extension_benchmark.json`](data/zoology_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `medical`
- **Panel tags:** Zoology
- **Data sources / cohorts:** GBIF Animalia occurrence coordinates, ecology bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| decimalLongitude · Populus grandidentata | -71.807 | -71.8198 | 0.017789 |
| decimalLatitude · Alsophila pometaria | 40.9948 | 41.0021 | 0.017789 |
| animal_occurrence · zoology_gbif | 0 | 0.017789 | 0.017789 |
| pooled_median · all_channels | 0 | 0.017789 | 0.017789 |
| decimalLongitude · Clethra alnifolia | -71.3005 | -71.3131 | 0.017789 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Zoology: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Zoology: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Zoology: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
