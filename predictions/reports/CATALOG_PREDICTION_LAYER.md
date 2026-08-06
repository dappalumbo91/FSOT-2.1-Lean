# Catalog prediction layer

*Generated 2026-08-06T13:50:32.094497+00:00 · pin D1D38A*

Catalog-native predictions from open panels already residual-gated in the monorepo (MPCORB, Gaia, DESI, GWTC, PubChem, exoplanets, climate).

**Framework gate (unchanged):** ≤ **0.5%** pooled residual.

Global residual framework gate remains ≤0.5%. This layer does not replace or relax that gate. Domain-specific tighter kills (e.g. Higgs) are a separate follow-on program — see predictions/HIGGS_TIGHTEN_PLAN.md.

Catalogs: **8** · Predictions: **35**

| Catalog | Tier | Records | Pooled % | Residual PRED | Survey |
|---------|------|--------:|---------:|---------------|--------|
| CAT-MPCORB | C | 1554101 | 0.023015 | `PRED-CAT-MPCORB-RESIDUAL` | MPC / IAU minor-planet catalog refreshes |
| CAT-GAIA-DR3 | A | 3459 | 0.022461 | `PRED-CAT-GAIA-DR3-RESIDUAL` | Gaia DR4 / DR3 reprocess public samples |
| CAT-DESI-PUBLIC | A | 10 | 0.010049 | `PRED-CAT-DESI-PUBLIC-RESIDUAL` | DESI public BAO / spectroscopy catalog refreshes |
| CAT-DESI-EDR-FITS | A | 97144 | 0.022461489204152866 | `PRED-CAT-DESI-EDR-FITS-RESIDUAL` | DESI EDR/DR table residual refreshes |
| CAT-GWTC | A | 1972 | 0.008488 | `PRED-CAT-GWTC-RESIDUAL` | GWOSC / GWTC catalog updates (O4 remainder, O5) |
| CAT-PUBCHEM | C | 500 | 0.002637 | `PRED-CAT-PUBCHEM-RESIDUAL` | PubChem compound property dumps |
| CAT-EXO | A | 1976 | 0.023015 | `PRED-CAT-EXO-RESIDUAL` | NASA Exoplanet Archive continuous updates |
| CAT-CLIMATE | C | 17325 | 0.01201268326195996 | `PRED-CAT-CLIMATE-RESIDUAL` | NOAA NCEI / open climate station refreshes |

## Sample scalar locks

| ID | Domain | Observable | FSOT | Err % |
|----|--------|------------|-----:|------:|
| `PRED-CAT-MPCORB-S01` | MPCORB_Minor_Planet_Catalog | catalog_kepler_median | 1.5876e-06 | 1.5876e-06 |
| `PRED-CAT-MPCORB-S02` | MPCORB_Minor_Planet_Catalog | catalog_kepler_p95 | 4.1106e-06 | 4.1106e-06 |
| `PRED-CAT-MPCORB-S03` | MPCORB_Minor_Planet_Catalog | K global scale | 0.4202616 | 0.009504 |
| `PRED-CAT-MPCORB-S04` | MPCORB_Minor_Planet_Catalog | S_abs_Cosmology_D25 | 0.50250644 | 0.010049 |
| `PRED-CAT-MPCORB-S05` | MPCORB_Minor_Planet_Catalog | θ_S acoustic phase | 0.2909328 | 0.012464 |
| `PRED-CAT-MPCORB-S06` | MPCORB_Minor_Planet_Catalog | A_bleed yin–yang bleed | 1.04710412 | 0.012464 |
| `PRED-CAT-MPCORB-S07` | MPCORB_Minor_Planet_Catalog | POOF valve (T3) | 0.15350421 | 0.014333 |
| `PRED-CAT-MPCORB-S08` | MPCORB_Minor_Planet_Catalog | SUCTION = POOF·(−cos(θ_S−π)) | 0.14705506 | 0.014333 |
| `PRED-CAT-GAIA-DR3-S02` | Gaia_DR3_Source_Sample_Open | gaia_depth | 0.022461 | 0.022461 |
| `PRED-CAT-DESI-PUBLIC-S02` | DESI_Public_Depth_Open | desi | 0.010049 | 0.010049 |
| `PRED-CAT-DESI-EDR-FITS-S01` | DESI_EDR_FITS_Residual | delta_chi2 | 0.010049 | 0.010049118924193572 |
| `PRED-CAT-DESI-EDR-FITS-S02` | DESI_EDR_FITS_Residual | redshift_zerr | 0.010049 | 0.010049118924193573 |
| `PRED-CAT-DESI-EDR-FITS-S03` | DESI_EDR_FITS_Residual | redshift_z | 0.010049 | 0.01004911892419358 |
| `PRED-CAT-DESI-EDR-FITS-S04` | DESI_EDR_FITS_Residual | chi2 | 0.010049 | 0.010049118924193584 |
| `PRED-CAT-DESI-EDR-FITS-S06` | DESI_EDR_FITS_Residual | plx_mas | 0.022461 | 0.02246148920415079 |
| `PRED-CAT-DESI-EDR-FITS-S07` | DESI_EDR_FITS_Residual | dec_abs_deg | 0.022461 | 0.022461489204150805 |
| `PRED-CAT-DESI-EDR-FITS-S08` | DESI_EDR_FITS_Residual | ebv | 0.022461 | 0.022461489204150812 |
| `PRED-CAT-GWTC-S02` | GWTC_Catalog_Open | gwtc | 0.008488 | 0.008488 |
| `PRED-CAT-PUBCHEM-S01` | PubChem_Compound_Properties | 962 | 18.015 | 0.0 |
| `PRED-CAT-PUBCHEM-S02` | PubChem_Compound_Properties | 1054 | 169.18 | 0.0 |
| `PRED-CAT-PUBCHEM-S03` | PubChem_Compound_Properties | 1176 | 60.056 | 0.0 |
| `PRED-CAT-PUBCHEM-S04` | PubChem_Compound_Properties | 588 | 113.12 | 0.0 |
| `PRED-CAT-PUBCHEM-S05` | PubChem_Compound_Properties | 190 | 135.13 | 0.0 |
| `PRED-CAT-PUBCHEM-S06` | PubChem_Compound_Properties | 5962 | 146.19 | 0.0 |
| `PRED-CAT-PUBCHEM-S07` | PubChem_Compound_Properties | 33032 | 147.13 | 0.0 |
| `PRED-CAT-PUBCHEM-S08` | PubChem_Compound_Properties | 5280961 | 270.24 | 0.0 |
| `PRED-CAT-EXO-S02` | Exoplanet_Archive_Depth_Open | exoplanet_tap | 0.023015 | 0.023015 |

Refresh: `python scripts/build_catalog_prediction_layer.py`
