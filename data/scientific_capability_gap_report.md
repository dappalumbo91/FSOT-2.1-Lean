# Scientific capability & accuracy gap report

Generated: `2026-08-04T02:56:39.139409+00:00`

## Goal

Beat or exceed scientific SOTA / literature capability on measured observables

## Live atlas (green gate)

- Green: **414** pass / 0 fail
- Worst max residual: **0.4989%** (Phi_Morphogenetic_Scaling)
- Domains with max > 0.05% aspiration: **102**

## SOTA competitiveness (registered comparisons)

- Domains beating SOTA median: **35/35** (100.0%)
- Average margin vs SOTA: **5.82 pp**
- Observables beats/meets: **58/65**
- Below SOTA IDs: none
- SOTA free parameters replaced (aggregate): **782**

### Thinnest leads (refine to lock *exceed*)

| ID | FSOT err% | SOTA typ% | Margin pp | Tier | SOTA model |
|----|-----------|-----------|-----------|------|------------|
| higgs_mass | 0.01100190161397048 | 0.14 | 0.129 | THIN_LEAD — refine to lock exceed | SM fits (PDG) |
| higgs_branching | 0.03711124585172393 | 0.5 | 0.463 | THIN_LEAD — refine to lock exceed | PDG SM branching fits |
| H0_planck | 0.08243667961587486 | 0.8 | 0.718 | MODERATE_LEAD — optional polish | Planck 2018 TT,TE,EE+lowE |
| airfoil_held_out_rmse | 4.598501331670039 | 5.412721340832612 | 0.814 | MODERATE_LEAD — optional polish | Chosen-feature quadratic regression |
| Omega_Lambda | 0.05 | 1.1 | 1.050 | MODERATE_LEAD — optional polish | Planck 2018 Lambda-CDM |
| N_eff | 0.01 | 4.0 | 3.990 | STRONG_LEAD — maintain | Planck 2018 |
| phobos_density | 0.0 | 4.0 | 4.000 | STRONG_LEAD — maintain | JPL Horizons GM/MR |
| pa_temperature_channel | 0.1764512018643632 | 5.0 | 4.824 | STRONG_LEAD — maintain | JPL Horizons vs NASA fact-sheet temperatures |
| culinary_coffee_roast | 0.0786974501611598 | 5.0 | 4.921 | STRONG_LEAD — maintain | SCA roast curve profiling |
| fic_best_intelligence_score | 0.029066672228905688 | 5.0 | 4.971 | STRONG_LEAD — maintain | INT8 LLM quantization fidelity drift |
| fic_optimal_S_final | 0.04959966617804441 | 8.0 | 7.950 | STRONG_LEAD — maintain | Neural knowledge distillation scalar calibration |
| onco_biology_strict | 0.0 | 8.0 | 8.000 | STRONG_LEAD — maintain | Comparative genomics operon regression |

### How much refinement is needed?

| Tier | Meaning | Action |
|------|---------|--------|
| BEHIND_SOTA | FSOT error > SOTA typical | Must improve formula/mechanism |
| THIN_LEAD (<0.5 pp) | Barely ahead | Highest-value refine for confident exceed |
| MODERATE_LEAD (0.5–2 pp) | Solid lead | Optional polish |
| STRONG_LEAD (>2 pp) | Comfortably ahead | Maintain; expand coverage |

FSOT already beats registered SOTA typical error on headline observables with 0 free fit coefficients. To *exceed more confidently*, refine THIN_LEAD items (margin < 0.5 pp) first: higgs_mass, airfoil RMSE, higgs_branching, H0_planck — without adding free parameters.

## Near-gate atlas (max residual)

- **Phi_Morphogenetic_Scaling**: max 0.4989% med 0.0176% n=289 worst=`Hg`
- **CRC_Handbook_Properties**: max 0.4989% med 0.0269% n=391 worst=`Hg`
- **geochemistry_benchmark.json**: max 0.4984% med 0.0066% n=153 worst=`Ni_EDTA`
- **Zebrafish_Predictive_Validation_Panel**: max 0.4920% med 0.3580% n=20 worst=`ZSNS003`
- **materials_engineering_benchmark.json**: max 0.4912% med 0.0272% n=87 worst=`Fe`
- **quantum_materials_benchmark.json**: max 0.4890% med 0.0243% n=168 worst=`K`
- **Clinical_Medicine**: max 0.4801% med 0.0025% n=260 worst=`TA/AT`
- **immunology_benchmark.json**: max 0.4801% med 0.0612% n=84 worst=`TA/AT`
- **neuroimmunology_benchmark.json**: max 0.4801% med 0.0504% n=92 worst=`TA/AT`
- **Creative_Arts_Math_Spine**: max 0.4623% med 0.0000% n=54 worst=`sucrose_hydrolysis`

## Thin panels (coverage debt)

- n=1 max=0.05092740813165782  math_generator_benchmark_formula_eval_benchmark.json
- n=2 max=3.862903827310908e-14  math_generator_airfoil_rmse_benchmark.json
- n=3 max=0.0  Tier_96_Circuit_Spine
- n=4 max=0.08243667961587486  h0_planck_benchmark.json
- n=4 max=0.031506  VL_Agent_Distill_Panel
- n=4 max=1.3209968920124464e-14  Living_FSOT_Hardware
- n=4 max=0.0  Astrophysical_Structure_Crosswalk
- n=4 max=0.0  Compact_Object_Binary_Events
- n=4 max=0.0  Interactive_Media_Prereg_Scaffold
- n=4 max=0.0  Scientific_Expansion_Depth_Spine
- n=5 max=0.051887  Schematic_Netlist_Intrinsic_Panel
- n=5 max=0.023609235048340338  Ionospheric_Chemistry_Coupling

## Priority queue

- 1. THIN_LEAD SOTA observables (higgs_mass, airfoil, H0_planck)
- 2. Near-gate formula-class only if definitional (not fishing)
- 3. Thin-panel thickening (lean routes, multi-hero strata)
- 4. TOE research spine (path-integral theorem, spin-2 Fock uniqueness)
- 5. Registered expansion waves (culinary Maillard, materials bridge, KB)

## TOE depth track

- Label B: True
- GR/SM/CKM multiprover ok: True
- Next research: ['Full non-abelian path-integral confinement *theorem* (probe layer closed; uniqueness proof open)', 'Spin-2 Fock *uniqueness* from fluid action (probe layer closed; uniqueness proof open)', 'Einstein–Hilbert measure uniqueness theorem (open)']

