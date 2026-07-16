## Government Registries, Open Data & Scholarly Graphs

**Panels:** 6 · **Records:** 720 · **Mean panel median error:** 0.013084%

#### Crossref Scholarly Panel

Extension panel **`Crossref_Scholarly_Panel`** (verification tier 81) evaluates **200** measured records at **0.01382%** pooled median error (A_strong). Formal module: `FSOT.Formal.CrossrefScholarlyPriors`. This panel extends the core spine into crossref scholarly panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/crossref_scholarly_panel_benchmark.json`](data/crossref_scholarly_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`
- **Panel tags:** Crossref, Scholarly, Panel
- **Data sources / cohorts:** Crossref public works API — citation counts, publication years

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| citation_count · 10.1007/978-0-387-30160-0_1141 | 0 | 0 | 0 |
| fsot_prediction · crossref | 0 | 0.01382 | 0.01382 |
| pooled_median · all_channels | 0 | 0.01382 | 0.01382 |
| publication_year · 10.1007/978-0-387-30160-0_1141 | 2007 | 2007.28 | 0.01382 |
| citation_count · 10.1007/978-0-387-74759-0_163 | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Crossref Scholarly Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Crossref Scholarly Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Crossref Scholarly Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Federal Science Registry Panel

Extension panel **`Federal_Science_Registry_Panel`** (verification tier 80) evaluates **24** measured records at **0.013352%** pooled median error (B_verified). Formal module: `FSOT.Formal.FederalScienceRegistryPriors`. This panel extends the core spine into federal science registry panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/federal_science_registry_panel_benchmark.json`](data/federal_science_registry_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `economic`, `particle`, `energy`
- **Panel tags:** Federal, Science, Registry, Panel
- **Data sources / cohorts:** NAIRR, Genesis Mission, Data.gov, OSTI bridge registry metadata (allocation portals documented)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |
| importance_score · 18-100754-general-1946-7-vol-2 | 6.4 | 6.40054 | 0.008488 |
| declassified_fraction_pct · osti_bridge | 8.2 | 8.20078 | 0.009504 |
| annual_record_ingest_rate · osti_bridge | 125000 | 125014 | 0.011056 |
| open_dataset_catalog_entries · nairr | 186 | 186.024 | 0.013003 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Federal Science Registry Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Federal Science Registry Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Federal Science Registry Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Government Open Data Spine

Extension panel **`Government_Open_Data_Spine`** (verification tier 80) evaluates **28** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.GovernmentOpenDataSpinePriors`. This panel extends the core spine into government open data spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/government_open_data_spine_benchmark.json`](data/government_open_data_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `medical`, `astronomical`, `economic`
- **Panel tags:** Government, Open, Data, Spine
- **Data sources / cohorts:** Tier 80 cross-panel spine — government open-data validation relay

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| panel_pooled_median · clinicaltrials_medical_panel | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| importance_score · 18-100754-general-1946-7-vol-2 | 6.4 | 6.40054 | 0.008488 |
| open_dataset_catalog_entries · nairr | 186 | 186.024 | 0.013003 |
| pilot_compute_hours · nairr | 250000 | 250033 | 0.013294 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Government Open Data Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Government Open Data Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Government Open Data Spine: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### OSTI DOE Science Panel

Extension panel **`OSTI_DOE_Science_Panel`** (verification tier 80) evaluates **100** measured records at **0.01382%** pooled median error (A_strong). Formal module: `FSOT.Formal.OstiDoeSciencePriors`. This panel extends the core spine into osti doe science panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/osti_doe_science_panel_benchmark.json`](data/osti_doe_science_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `energy`
- **Panel tags:** Osti, Doe, Science, Panel
- **Data sources / cohorts:** DOE OSTI open scientific corpus — publication year anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| fsot_prediction · osti_doe | 0 | 0.01382 | 0.01382 |
| pooled_median · all_channels | 0 | 0.01382 | 0.01382 |
| publication_year · 1961631 | 2026 | 2026.28 | 0.01382 |
| publication_year · 1961632 | 2026 | 2026.28 | 0.01382 |
| publication_year · 2352511 | 2024 | 2024.28 | 0.01382 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in OSTI DOE Science Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in OSTI DOE Science Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in OSTI DOE Science Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### OpenAlex Citation Graph

Extension panel **`OpenAlex_Citation_Graph`** (verification tier 38) evaluates **80** measured records at **0.031506%** pooled median error (B_verified). Formal module: `FSOT.Formal.OpenalexCitationGraphPriors`. This panel extends the core spine into openalex citation graph observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/openalex_citation_graph_benchmark.json`](data/openalex_citation_graph_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `linguistic`
- **Panel tags:** Openalex, Citation, Graph
- **Data sources / cohorts:** OpenAlex scholarly citation graph (150 works deep)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| cited_by_count · <i>Computational Methods for Fluid Dynamics</i> | 6038 | 6039.9 | 0.031506 |
| cited_by_count · A spectral element method for fluid dynamics: Laminar flow i | 2301 | 2301.72 | 0.031506 |
| cited_by_count · An Introduction to Computational Fluid Dynamics: The Finite  | 4480 | 4481.41 | 0.031506 |
| cited_by_count · An Introduction to Fluid Dynamics | 12370 | 12373.9 | 0.031506 |
| cited_by_count · An Introduction to Fluid Dynamics | 1073 | 1073.34 | 0.031506 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in OpenAlex Citation Graph: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in OpenAlex Citation Graph: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`C≡O`** in OpenAlex Citation Graph: measured **1076.5**, seed-derived **1076.5476215052706** via `E^7-E^3` (error **0.004424%**). Constants: seed constants. Authority: Luo, Compr. Handbook Chem. Bond Energies (2007).

#### iNaturalist Observation Panel

Extension panel **`iNaturalist_Observation_Panel`** (verification tier 81) evaluates **288** measured records at **0.006006%** pooled median error (A_strong). Formal module: `FSOT.Formal.InaturalistObservationPriors`. This panel extends the core spine into inaturalist observation panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/inaturalist_observation_panel_benchmark.json`](data/inaturalist_observation_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `ecological`
- **Panel tags:** Inaturalist, Observation, Panel
- **Data sources / cohorts:** iNaturalist public observations — geo ecology cross-check vs GBIF

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| fsot_prediction · inaturalist | 0 | 0.006006 | 0.006006 |
| latitude · 380617064 | 47.7058 | 47.7086 | 0.006006 |
| longitude · 380617064 | -3.38352 | -3.38373 | 0.006006 |
| pooled_median · all_channels | 0 | 0.006006 | 0.006006 |
| positional_accuracy · 380617064 | 3102 | 3102.23 | 0.007508 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in iNaturalist Observation Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in iNaturalist Observation Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in iNaturalist Observation Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
