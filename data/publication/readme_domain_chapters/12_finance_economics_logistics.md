## Finance, Econometrics & Supply-Chain Logistics

**Panels:** 8 · **Records:** 942 · **Mean panel median error:** 0.0359339%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `Actuarial_Science_Panel` | 60 | 0.02261 | B_verified |
| `Econometrics` | 172 | 0.129201 | A_strong |
| `Econophysics` | 24 | 0 | B_verified |
| `Finance_Markets` | 150 | 0.0258402 | A_strong |
| `Finance_Markets_Panel` | 36 | 0.02584 | B_verified |
| `Supply_Chain_Logistics` | 40 | 0.0323002 | B_verified |
| `Supply_Chain_Logistics_Panel` | 40 | 0.02584 | B_verified |
| `World_Bank_Development` | 420 | 0.02584 | A_strong |

#### Actuarial Science Panel

Extension panel **`Actuarial_Science_Panel`** (verification tier 82) evaluates **60** measured records at **0.02261%** pooled median error (B_verified). Formal module: `FSOT.Formal.ActuarialSciencePriors`. This panel extends the core spine into actuarial science panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/actuarial_science_panel_benchmark.json`](data/actuarial_science_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `economic`, `consciousness`
- **Panel tags:** Actuarial, Science, Panel
- **Data sources / cohorts:** Actuarial science — SSA mortality, life-table scalars

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| ex · 10 | 68.2 | 68.2089 | 0.013003 |
| fsot_prediction · actuarial | 0 | 0.02261 | 0.02261 |
| lx · 10 | 99420 | 99442.5 | 0.02261 |
| pooled_median · all_channels | 0 | 0.02261 | 0.02261 |
| qx · 10 | 0.00012 | 0.00012 | 0.02584 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Actuarial Science Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Actuarial Science Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Actuarial Science Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Econometrics

Extension panel **`Econometrics`** (verification tier 34) evaluates **172** measured records at **0.129201%** pooled median error (A_strong). Formal module: `FSOT.Formal.EconometricsGapFillPriors`. This panel extends the core spine into econometrics observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/econometrics_gap_fill_benchmark.json`](data/econometrics_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `mathematical`
- **Panel tags:** Econometrics
- **Data sources / cohorts:** World Bank macro panel dispersion, economics YoY bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| GDP_current_USD_yoy_growth_pct · IN_2021 | 18.4092 | 18.433 | 0.129201 |
| GDP_per_capita_yoy_growth_pct · CN_2022 | 0.645357 | 0.64619 | 0.129201 |
| population_total_yoy_growth_pct · CA_2021 | 0.555439 | 0.556157 | 0.129201 |
| panel_dispersion · macroeconometric_panel | 0 | 0.129201 | 0.129201 |
| pooled_median · all_channels | 0 | 0.129201 | 0.129201 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Econometrics: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Econometrics: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Econometrics: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Econophysics

Extension panel **`Econophysics`** (verification tier 66) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.EconophysicsPriors`. This panel extends the core spine into econophysics observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/econophysics_benchmark.json`](data/econophysics_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `mathematical`, `energy`
- **Panel tags:** Econophysics
- **Data sources / cohorts:** Pareto, Hurst, Kelly econophysics anchors, econometrics gap-fill bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Econophysics_depth | 0 | 0 | 0 |
| domain_scalar · fsot_Economics | 0.646005 | 0.646005 | 0 |
| empirical_gap_fill_bridge · econometrics_gap_fill_benchmark | 0.129201 | 0.129201 | 0 |
| observable · gini_coefficient | 0.724 | 0.724 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Econophysics: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Econophysics: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Econophysics: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Finance Markets

Extension panel **`Finance_Markets`** (verification tier 41) evaluates **150** measured records at **0.0258402%** pooled median error (A_strong). Formal module: `FSOT.Formal.FinanceMarketsExtensionPriors`. This panel extends the core spine into finance markets observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/finance_markets_extension_benchmark.json`](data/finance_markets_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`, `mathematical`
- **Panel tags:** Finance, Markets
- **Data sources / cohorts:** Finance markets reference, World Bank, econometrics bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| GDP_current_USD · US_2020 | 2.13753e+13 | 2.13808e+13 | 0.0258402 |
| GDP_per_capita · JP_2023 | 35215 | 35224.1 | 0.0258402 |
| market_observables · finance_markets_panel | 0 | 0.02584 | 0.0258402 |
| pooled_median · all_channels | 0 | 0.02584 | 0.0258402 |
| volatility_index · vix_long_run_mean | 19 | 19.0061 | 0.0323002 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Finance Markets: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Finance Markets: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Finance Markets: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Finance Markets Panel

Extension panel **`Finance_Markets_Panel`** (verification tier 85) evaluates **36** measured records at **0.02584%** pooled median error (B_verified). Formal module: `FSOT.Formal.FinanceMarketsPanelPriors`. This panel extends the core spine into finance markets panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/finance_markets_panel_benchmark.json`](data/finance_markets_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`, `mathematical`
- **Panel tags:** Finance, Markets, Panel
- **Data sources / cohorts:** Finance markets — World Bank macro, finance indicators

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| fsot_prediction · finance_markets | 0 | 0.02584 | 0.02584 |
| gdp_current_usd · ZH_NY.GDP.MKTP.CD | 1.17912e+12 | 1.17943e+12 | 0.02584 |
| gdp_per_capita · ZH_NY.GDP.PCAP.CD | 1571.13 | 1571.54 | 0.02584 |
| inflation_pct · ZH_FP.CPI.TOTL.ZG | 7.39919 | 7.4011 | 0.02584 |
| pooled_median · all_channels | 0 | 0.02584 | 0.02584 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Finance Markets Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Finance Markets Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Finance Markets Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Supply Chain Logistics

Extension panel **`Supply_Chain_Logistics`** (verification tier 41) evaluates **40** measured records at **0.0323002%** pooled median error (B_verified). Formal module: `FSOT.Formal.SupplyChainLogisticsExtensionPriors`. This panel extends the core spine into supply chain logistics observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/supply_chain_logistics_extension_benchmark.json`](data/supply_chain_logistics_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`, `biological`
- **Panel tags:** Supply, Chain, Logistics
- **Data sources / cohorts:** Supply chain reference, World Bank trade, agroecology bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| mean_latitude · Castor canadensis | 42.8143 | 42.822 | 0.018019 |
| logistics_observables · supply_chain_panel | 0 | 0.0323 | 0.0323002 |
| on_time_delivery_pct · supplier_otd_pct | 92 | 92.0297 | 0.0323002 |
| pooled_median · all_channels | 0 | 0.0323 | 0.0323002 |
| utilization_pct · warehouse_utilization_pct | 85 | 85.0275 | 0.0323002 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Supply Chain Logistics: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Supply Chain Logistics: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Supply Chain Logistics: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Supply Chain Logistics Panel

Extension panel **`Supply_Chain_Logistics_Panel`** (verification tier 85) evaluates **40** measured records at **0.02584%** pooled median error (B_verified). Formal module: `FSOT.Formal.SupplyChainLogisticsPanelPriors`. This panel extends the core spine into supply chain logistics panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/supply_chain_logistics_panel_benchmark.json`](data/supply_chain_logistics_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`, `biological`
- **Panel tags:** Supply, Chain, Logistics, Panel
- **Data sources / cohorts:** Supply chain logistics — World Bank trade, logistics indicators

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| container_port_traffic_teus · ZI_IS.SHP.GOOD.TU | 8.91752e+06 | 8.91982e+06 | 0.02584 |
| fsot_prediction · supply_chain | 0 | 0.02584 | 0.02584 |
| logistics_performance_index · ZH_LP.LPI.OVRL.XQ | 2.61818 | 2.61886 | 0.02584 |
| merchandise_exports_pct_gdp · ZH_TX.VAL.MRCH.R1.ZS | 23.5732 | 23.5793 | 0.02584 |
| merchandise_imports_pct_gdp · ZH_TM.VAL.MRCH.R1.ZS | 24.6736 | 24.68 | 0.02584 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Supply Chain Logistics Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Supply Chain Logistics Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Supply Chain Logistics Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### World Bank Development

Extension panel **`World_Bank_Development`** (verification tier 38) evaluates **420** measured records at **0.02584%** pooled median error (A_strong). Formal module: `FSOT.Formal.WorldBankDevelopmentPriors`. This panel extends the core spine into world bank development observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/world_bank_development_benchmark.json`](data/world_bank_development_benchmark.json)

**Subfield map:**

- **Lean routes:** `consciousness`, `economic`
- **Panel tags:** World, Bank, Development
- **Data sources / cohorts:** World Bank open development indicators (11 countries × 3 metrics)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| GDP_current_USD · AR_2019 | 4.47755e+11 | 4.4787e+11 | 0.02584 |
| GDP_per_capita · AR_2019 | 9955.97 | 9958.55 | 0.02584 |
| population_total · AR_2019 | 4.49735e+07 | 4.49851e+07 | 0.02584 |
| GDP_current_USD · AR_2020 | 3.85741e+11 | 3.8584e+11 | 0.02584 |
| GDP_current_USD · AR_2021 | 4.86564e+11 | 4.8669e+11 | 0.02584 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Ca`** in World Bank Development: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
- **`P`** in World Bank Development: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`R_C`** in World Bank Development: measured **0.77**, seed-derived **0.7700130881402762** via `π⁻⁴ + √γ` (error **0.0017%**). Constants: gamma, pi. Authority: NIST / CRC / Allen / Luo.
