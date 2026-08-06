# MPCORB raw observation O–C (MPC + JPL Horizons)

*Generated 2026-08-06T14:49:43.927362+00:00*

O–C in arcseconds between raw MPC optical observations we download and JPL Horizons predicted positions at those epochs — granular data, not a literature summary table.

**Ephemeris:** JPL Horizons geocentric OBSERVER (DE441-class)  
**Observations:** MPC Observations API ADES (optical RA/Dec)  
**Store:** `G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations`

Not a re-fit of orbits. Catalog rms remains the MPC's own orbit-fit residual; Horizons O–C is an independent industrial ephemeris check.

## Triple scoreboard (granular data)

| Layer | Value | Unit |
|-------|------:|------|
| **Raw obs vs Horizons O–C (median)** | **3.443217189679257** | arcsec |
| Catalog RMS on same sample | 0.65 | arcsec |
| Catalog RMS full MPCORB median | 0.76 | arcsec |
| FSOT pooled residual | 0.023015 | % |

Three layers on real data: (1) raw MPC obs vs Horizons O–C arcsec, (2) MPCORB catalog rms field arcsec, (3) FSOT seed residual %.

Objects scored: **35** (up to 40 obs each)

| Raw O–C summary | arcsec |
|-----------------|-------:|
| median of object medians | 3.443217189679257 |
| p95 of object medians | 82.24726881824313 |
| median of object RMS | 23.615871243424195 |

## By regime

| Regime | median O–C (arcsec) |
|--------|--------------------:|
| distant | 0.5282110850687085 |
| main_belt | 3.2067654829618024 |
| neo | 7.132918089467298 |
| other | 4.296637047345211 |
| outer_belt | 1.8062889256807266 |

## Per-object

| Desig | Regime | U | Catalog RMS | Horizons O–C med | O–C RMS | n |
|------:|--------|--:|------------:|-----------------:|--------:|--:|
| 15760 | distant | 2 | 0.91 | 0.5282 | 0.9766 | 40 |
| 10370 | other | 3 | 0.31 | 0.7447 | 1.1978 | 40 |
| 279 | outer_belt | 0 | 0.62 | 1.5851 | 60.3003 | 40 |
| 522 | outer_belt | 0 | 0.74 | 1.6346 | 1.9287 | 40 |
| 361 | outer_belt | 0 | 0.72 | 1.6492 | 1.8597 | 40 |
| 334 | outer_belt | 0 | 0.74 | 1.7093 | 1.9634 | 40 |
| 944 | other | 0 | 0.68 | 1.7834 | 2.5821 | 40 |
| 414 | outer_belt | 0 | 0.64 | 1.9032 | 55.5199 | 40 |
| 499 | outer_belt | 0 | 0.61 | 1.9254 | 55.0713 | 40 |
| 2 | main_belt | 0 | 0.77 | 2.2941 | 8.5446 | 40 |
| 1 | main_belt | 0 | 0.83 | 2.5780 | 13.5539 | 40 |
| 5 | main_belt | 0 | 0.85 | 2.9119 | 19.4486 | 40 |
| 5335 | other | 4 | 0.51 | 2.9502 | 3.2360 | 40 |
| 153 | outer_belt | 0 | 0.53 | 3.1036 | 70.8427 | 40 |
| 8 | main_belt | 0 | 0.85 | 3.1827 | 24.6060 | 40 |
| 6 | main_belt | 0 | 0.77 | 3.2308 | 4.0268 | 40 |
| 1036 | neo | 0 | 0.62 | 3.2457 | 42.3476 | 40 |
| 3 | main_belt | 0 | 0.84 | 3.4432 | 7.8604 | 40 |
| 1139 | other | 0 | 0.66 | 3.4710 | 5.8690 | 40 |
| 4 | main_belt | 0 | 0.69 | 3.7405 | 16.3968 | 40 |
| 7 | main_belt | 0 | 0.83 | 3.7650 | 11.1417 | 40 |
| 1580 | neo | 0 | 0.72 | 4.0504 | 13.4108 | 40 |
| 1025 | other | 0 | 0.65 | 4.1188 | 127.3221 | 40 |
| 1103 | other | 0 | 0.56 | 4.4745 | 169.5881 | 40 |
| 1355 | other | 0 | 0.55 | 4.7260 | 158.8278 | 40 |
| 887 | neo | 0 | 0.54 | 6.1230 | 121.5280 | 40 |
| 434 | other | 0 | 0.47 | 6.5385 | 147.6732 | 40 |
| 1221 | neo | 0 | 0.93 | 7.0063 | 23.6159 | 40 |
| 1620 | neo | 0 | 0.58 | 7.2595 | 198.2865 | 40 |
| 433 | neo | 0 | 0.61 | 8.2120 | 145.6500 | 40 |
| 719 | neo | 0 | 0.77 | 8.3830 | 10.6090 | 40 |
| 190 | outer_belt | 0 | 0.51 | 11.9148 | 88.3378 | 40 |
| 1566 | neo | 0 | 0.63 | 51.4579 | 193.7497 | 40 |
| 1019 | other | 0 | 0.4 | 154.0892 | 230.6204 | 40 |
| 1235 | other | 0 | 0.53 | 194.7188 | 323.8719 | 40 |

```powershell
python scripts/ingest_mpcorb_raw_observations.py --max-objects 48
python scripts/build_mpcorb_raw_oc_residuals.py
python scripts/build_mpcorb_classical_metrics.py
```
