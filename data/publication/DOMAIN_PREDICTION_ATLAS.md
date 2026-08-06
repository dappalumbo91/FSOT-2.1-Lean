# Domain prediction atlas

*Generated 2026-08-06T13:06:58.970297+00:00 · pin D1D38A*

Atlas-scale preregistered predictions derived from existing FSOT domain panels. Residual holds for every green domain; scalar locks for top panel observables; multi-tool H0 under bubble-bleed theory.

## Summary

| Metric | Value |
|--------|------:|
| Green domains covered | 472 |
| Unique domains | 470 |
| Total atlas predictions | 1219 |
| Multi-tool H₀ | 25 |
| Hand prereg YAML (separate) | 48 |
| Bundle SHA | `e93f66e26a86f2f4…` |

### By kind

| Kind | Count |
|------|------:|
| multi_tool_h0 | 25 |
| residual_hold | 472 |
| scalar_lock | 722 |

## Multi-tool H₀ (see full table)

Full tool table: [`H0_MULTI_TOOL_PREDICTIONS.md`](H0_MULTI_TOOL_PREDICTIONS.md)  
Machine: `data/h0_multi_tool_predictions.json`

## Worst residual holds (still green ≤0.5%)

| Domain | Pooled % | Residual PRED |
|--------|---------:|---------------|
| Zebrafish_Predictive_Validation_Panel | 0.3579695 | `PRED-DOM-0013` |
| Dark_Energy_CPL | 0.280515 | `PRED-DOM-0067` |
| Econometrics | 0.12920090413715177 | `PRED-DOM-1013` |
| Economics | 0.1292009041371501 | `PRED-DOM-1016` |
| orbital_mechanics_benchmark.json | 0.106141 | `PRED-DOM-1091` |
| Neuroeconomics | 0.10502056403980387 | `PRED-DOM-0203` |
| cosmology_anomalies_benchmark.json | 0.096204 | `PRED-DOM-0997` |
| Maillard_Chemistry | 0.09443694019339477 | `PRED-DOM-1057` |
| Architecture_Building_Science | 0.07869745016115058 | `PRED-DOM-0976` |
| CODATA_Full_Table_Open | 0.073582 | `PRED-DOM-0234` |
| immunology_benchmark.json | 0.060853500000000005 | `PRED-DOM-0030` |
| Observer_Channel_Derivation | 0.052510282019890844 | `PRED-DOM-0244` |
| TOE_CKM_PMNS_Flavor | 0.05235314586422479 | `PRED-DOM-0063` |
| neuroimmunology_benchmark.json | 0.05041956982053305 | `PRED-DOM-0034` |
| oncology_benchmark.json | 0.05041956982053305 | `PRED-DOM-0053` |
| Founding_Quantum_Vacuum_Panel | 0.047775 | `PRED-DOM-0261` |
| culinary_arts_benchmark.json | 0.04761518705782039 | `PRED-DOM-0043` |
| ENDF_IAEA_Nuclear_Open | 0.046065 | `PRED-DOM-0267` |
| Nuclear_IAEA_Open | 0.046065 | `PRED-DOM-0270` |
| Virology | 0.04593318440797596 | `PRED-DOM-0050` |
| Malware_Threat_Intelligence | 0.04593318440797134 | `PRED-DOM-0047` |
| Founding_Pulsar_Glitch_Panel | 0.044923 | `PRED-DOM-0276` |
| Founding_White_Dwarf_Cooling_Panel | 0.044923 | `PRED-DOM-0279` |
| Speleology | 0.04459015721103052 | `PRED-DOM-0060` |
| Food_Microbiology | 0.04447250077037743 | `PRED-DOM-1027` |

Refresh:
```text
python scripts/build_h0_multi_tool_predictions.py
python scripts/build_domain_prediction_atlas.py
python scripts/run_prediction_monitor.py
```
