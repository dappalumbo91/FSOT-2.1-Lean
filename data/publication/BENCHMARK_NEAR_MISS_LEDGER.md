# Benchmark Near-Miss Ledger

*Generated: 2026-07-16T13:43:07.429918+00:00*

Domains that pass the green gate but approach the ≤0.5% boundary — published for transparency, not hidden as post-hoc rescues.

| Gate | Value |
|------|------:|
| Green pass | 394/394 |
| Worst max scalar (any domain) | 0.4989% — `Phi_Morphogenetic_Scaling` |
| Tier-scalar max fails | 1 |

## Top 15 by max single-record error (still green)

| Domain | Records | Pooled median % | Max scalar % | Worst observable |
|--------|--------:|----------------:|-------------:|------------------|
| Phi_Morphogenetic_Scaling | 289 | 0.0176 | 0.4989 | `Hg` / speed_sound_m_s |
| CRC_Handbook_Properties | 391 | 0.0269 | 0.4989 | `Hg` / §39 Speed of Sound |
| geochemistry_benchmark.json | 153 | 0.0066 | 0.4984 | `Ni_EDTA` / §58 logβ Stability |
| Zebrafish_Predictive_Validation_Panel | 20 | 0.3580 | 0.4920 | `ZSNS003` / mean_displacement_um |
| materials_engineering_benchmark.json | 87 | 0.0272 | 0.4912 | `Fe` / §84 Poisson Ratio ν |
| quantum_materials_benchmark.json | 168 | 0.0243 | 0.4890 | `K` / §33 Debye Temps |
| Clinical_Medicine | 260 | 0.0025 | 0.4801 | `TA/AT` / §71 DNA Stacking ΔG |
| immunology_benchmark.json | 84 | 0.0612 | 0.4801 | `TA/AT` / §71 DNA Stacking ΔG |
| neuroimmunology_benchmark.json | 92 | 0.0504 | 0.4801 | `TA/AT` / §71 DNA Stacking ΔG |
| Creative_Arts_Math_Spine | 56 | 0.0000 | 0.4623 | `sucrose_hydrolysis` / §45 Activation Ea |
| culinary_arts_benchmark.json | 26 | 0.0476 | 0.4623 | `sucrose_hydrolysis` / §45 Activation Ea |
| Information_Theory_Public_Panel | 24 | 0.0000 | 0.4623 | `sucrose_hydrolysis` / §45 Activation Ea |
| Music_Harmonics_Public_Panel | 24 | 0.0000 | 0.4623 | `sucrose_hydrolysis` / §45 Activation Ea |
| Malware_Threat_Intelligence | 85 | 0.0459 | 0.4316 | `Asp_pKR` / §22 Amino Acid pKa |
| Virology | 50 | 0.0459 | 0.4316 | `Asp_pKR` / §22 Amino Acid pKa |

## Tier-scalar aspiration misses (extension gate unchanged)

- **Phi_Morphogenetic_Scaling**: tier_scalar_max_pass=false, pooled=0.01760779720633292%
- **CRC_Handbook_Properties**: tier_scalar_max_pass=false, pooled=0.026922%
- **geochemistry_benchmark.json**: tier_scalar_max_pass=false, pooled=0.006625234573930708%
- **Zebrafish_Predictive_Validation_Panel**: tier_scalar_max_pass=false, pooled=0.3579695%
- **materials_engineering_benchmark.json**: tier_scalar_max_pass=false, pooled=0.027170334947435038%
- **quantum_materials_benchmark.json**: tier_scalar_max_pass=false, pooled=0.024318115591995593%
- **Clinical_Medicine**: tier_scalar_max_pass=false, pooled=0.002458296751538192%
- **immunology_benchmark.json**: tier_scalar_max_pass=false, pooled=0.061205%
- **neuroimmunology_benchmark.json**: tier_scalar_max_pass=false, pooled=0.05041956982053305%
- **Creative_Arts_Math_Spine**: tier_scalar_max_pass=false, pooled=0.0%

## Top 15 by pooled median (highest among green domains)

| Domain | Pooled median % | Max scalar % |
|--------|----------------:|-------------:|
| Zebrafish_Predictive_Validation_Panel | 0.3580 | 0.4920 |
| h0_planck_benchmark.json | 0.1333 | 0.0000 |
| Econometrics | 0.1292 | 0.0000 |
| Economics | 0.1292 | 0.0000 |
| Neuroeconomics | 0.1050 | 0.1050 |
| Quantum_Mechanics_Entanglement_Depth_Panel | 0.0956 | 0.0956 |
| Maillard_Chemistry | 0.0944 | 0.0000 |
| higgs_branching_benchmark.json | 0.0881 | 0.0000 |
| Architecture_Building_Science | 0.0787 | 0.0000 |
| immunology_benchmark.json | 0.0612 | 0.4801 |
| Observer_Channel_Derivation | 0.0525 | 0.0525 |
| neuroimmunology_benchmark.json | 0.0504 | 0.4801 |
| oncology_benchmark.json | 0.0504 | 0.4289 |
| culinary_arts_benchmark.json | 0.0476 | 0.4623 |
| Cryptography_Technology | 0.0475 | 0.0570 |

Regenerate: `python scripts/build_benchmark_near_miss_ledger.py`
