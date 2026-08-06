# Per-host / sightline H₀ predictions

*Generated 2026-08-06T13:12:34.184993+00:00 · pin D1D38A · 22 hosts*

SH0ES host galaxies lie on different sightlines through the BH→WH information-flow / nebula-bleed field. Each host gets its own FSOT H0 prediction; the ladder average is a mixture, not a single fundamental constant.

**Global FSOT H₀** = `68.44005682979427`  
**Host-mean FSOT H₀** = `73.302397`  
**Span** = `{'min_fsot': 70.214931, 'max_fsot': 74.164154}`  
**Nebulae / FRBs used for sky density** = 20 / 38

## Sky sectors

| Sector | Hosts | Mean FSOT H₀ | Min | Max |
|--------|------:|-------------:|----:|----:|
| `sector_0_planck_depleted` | 3 | **74.164154** | 74.164154 | 74.164154 |
| `sector_1_local_low` | 3 | **72.474173** | 70.214931 | 73.603794 |
| `sector_2_carnegie` | 5 | **73.470375** | 73.470375 | 73.470375 |
| `sector_3_fsot_document` | 10 | **73.186214** | 70.388608 | 73.497059 |
| `sector_5_sh0es_inflated` | 1 | **73.523742** | 73.523742 | 73.523742 |

## Hosts (sorted by FSOT H₀)

| Host | Method | RA° | Sector | Density sky | FSOT H₀ |
|------|--------|----:|--------|------------:|--------:|
| LMC | TRGB_anchor | 80.894 | `sector_1_local_low` | -0.431034 | **70.214931** |
| NGC4258 | Maser_anchor | 184.740 | `sector_3_fsot_document` | -0.637931 | **70.388608** |
| NGC3021 | SH0ES_Cepheid | 147.371 | `sector_2_carnegie` | -0.689655 | **73.470375** |
| NGC3370 | SH0ES_Cepheid | 161.132 | `sector_2_carnegie` | -0.689655 | **73.470375** |
| NGC3627 | SH0ES_Cepheid | 170.062 | `sector_2_carnegie` | -0.689655 | **73.470375** |
| NGC3982 | SH0ES_Cepheid | 179.075 | `sector_2_carnegie` | -0.689655 | **73.470375** |
| UGC9391 | SH0ES_Cepheid | 175.628 | `sector_2_carnegie` | -0.689655 | **73.470375** |
| M101 | SH0ES_Cepheid | 210.802 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC4038 | SH0ES_Cepheid | 180.466 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC4254 | SH0ES_Cepheid | 184.674 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC4321 | SH0ES_Cepheid | 185.899 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC4536 | SH0ES_Cepheid | 188.614 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC4639 | SH0ES_Cepheid | 190.677 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC5584 | SH0ES_Cepheid | 215.289 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC5643 | SH0ES_Cepheid | 219.059 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC5917 | SH0ES_Cepheid | 232.288 | `sector_3_fsot_document` | -0.637931 | **73.497059** |
| NGC7250 | SH0ES_Cepheid | 334.215 | `sector_5_sh0es_inflated` | -0.586207 | **73.523742** |
| NGC1559 | SH0ES_Cepheid | 67.767 | `sector_1_local_low` | -0.431034 | **73.603794** |
| NGC2442 | SH0ES_Cepheid | 111.108 | `sector_1_local_low` | -0.431034 | **73.603794** |
| NGC1309 | SH0ES_Cepheid | 50.423 | `sector_0_planck_depleted` | 0.655172 | **74.164154** |
| NGC1365 | SH0ES_Cepheid | 53.401 | `sector_0_planck_depleted` | 0.655172 | **74.164154** |
| NGC1448 | SH0ES_Cepheid | 56.138 | `sector_0_planck_depleted` | 0.655172 | **74.164154** |

Bundle SHA-256: `081d8faa0a186d4ceda2bb975696c6f2895c19e885d05cbf233a7449d0ee0c91`

Refresh: `python scripts/build_h0_sightline_predictions.py`

Related: multi-tool table `H0_MULTI_TOOL_PREDICTIONS.md` · seed `data/sector_h0_seed.json`
