# MPCORB raw observation O–C (MPC + JPL Horizons)

*Generated 2026-08-06T14:20:49.688717+00:00*

O–C in arcseconds between raw MPC optical observations we download and JPL Horizons predicted positions at those epochs — granular data, not a literature summary table.

**Ephemeris:** JPL Horizons geocentric OBSERVER (DE441-class)  
**Observations:** MPC Observations API ADES (optical RA/Dec)  
**Store:** `G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations`

Not a re-fit of orbits. Catalog rms remains the MPC's own orbit-fit residual; Horizons O–C is an independent industrial ephemeris check.

## Triple scoreboard (granular data)

| Layer | Value | Unit |
|-------|------:|------|
| **Raw obs vs Horizons O–C (median)** | **4.230223137111953** | arcsec |
| Catalog RMS on same sample | 0.65 | arcsec |
| Catalog RMS full MPCORB median | 0.76 | arcsec |
| FSOT pooled residual | 0.023015 | % |

Three layers on real data: (1) raw MPC obs vs Horizons O–C arcsec, (2) MPCORB catalog rms field arcsec, (3) FSOT seed residual %.

Objects scored: **19** (up to 40 obs each)

| Raw O–C summary | arcsec |
|-----------------|-------:|
| median of object medians | 4.230223137111953 |
| p95 of object medians | 384.2006289689805 |
| median of object RMS | 10.609007903549376 |

## By regime

| Regime | median O–C (arcsec) |
|--------|--------------------:|
| distant | 0.48288991906137585 |
| main_belt | 2.4360599249389043 |
| neo | 38.141965468172785 |
| other | 4.1609077054054735 |

## Per-object

| Desig | Regime | U | Catalog RMS | Horizons O–C med | O–C RMS | n |
|------:|--------|--:|------------:|-----------------:|--------:|--:|
| 15788 | distant | 1 | 0.84 | 0.2893 | 0.6662 | 40 |
| 15809 | distant | 5 | 0.65 | 0.4236 | 0.8492 | 40 |
| 15807 | distant | 4 | 0.58 | 0.4376 | 1.2973 | 40 |
| 15760 | distant | 2 | 0.91 | 0.5282 | 0.9766 | 40 |
| J95Y03Y | distant | None | 0.91 | 1.1743 | 17.6323 | 21 |
| J99A36C | main_belt | 6 | 0.24 | 1.4533 | 1.9486 | 22 |
| 944 | other | 0 | 0.68 | 1.7834 | 2.5821 | 40 |
| 2 | main_belt | 0 | 0.77 | 2.2941 | 8.5446 | 40 |
| 1 | main_belt | 0 | 0.83 | 2.5780 | 13.5539 | 40 |
| J96P00W | distant | None | 0.56 | 4.2302 | 4.2954 | 40 |
| 434 | other | 0 | 0.47 | 6.5385 | 147.6732 | 40 |
| 433 | neo | 0 | 0.61 | 8.2120 | 145.6500 | 40 |
| 719 | neo | 0 | 0.77 | 8.3830 | 10.6090 | 40 |
| J98A10K | main_belt | 6 | 0.35 | 8.9729 | 9.9703 | 26 |
| K02A01Z | neo | None | 0.65 | 12.7055 | 15.5381 | 40 |
| J90U00N | neo | 8 | 0.51 | 38.1420 | 62.9725 | 22 |
| J91J00R | neo | 7 | 0.55 | 70.9541 | 81.4549 | 20 |
| J92J00D | neo | 5 | 0.75 | 354.6381 | 326.2998 | 24 |
| J93K00A | neo | None | 0.9 | 650.2633 | 636.2380 | 38 |

```powershell
python scripts/ingest_mpcorb_raw_observations.py --max-objects 48
python scripts/build_mpcorb_raw_oc_residuals.py
python scripts/build_mpcorb_classical_metrics.py
```
