# FSOT system math audit — summary

**Generated:** 2026-08-05T20:57:01.045588+00:00  
**Authority pin file:** `vendor/fsot_compute_AUTHORITY_PIN.json`  
**Consistency:** PASS (16/16)

## Scope (not core-only)

| Layer | Count |
|-------|------:|
| Core domain interfaces | 35 |
| Extension domain interfaces | 371 |
| **Total formula interfaces** | **406** |
| Publication atlas rows | 403 |
| Green residual benchmark panels | 470 |
| Benchmark files (margin audit) | 470 |

Machine dump: [`data/fsot_system_math_audit.json`](../data/fsot_system_math_audit.json)  
Hierarchy: [`data/fsot_building_block_hierarchy.json`](../data/fsot_building_block_hierarchy.json)  
Network + green panels: [`data/fsot_domain_formula_network.json`](../data/fsot_domain_formula_network.json)  
Extensions source: [`data/extension_domains_manifest.yaml`](../data/extension_domains_manifest.yaml)  
Atlas: [`data/publication/domain_atlas.csv`](../data/publication/domain_atlas.csv)  
Guide: [`FSOT_MATHEMATICIAN_HOWTO.md`](FSOT_MATHEMATICIAN_HOWTO.md) · Key: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)

## Ontology

FSOT is **fluid spacetime omni-theory** with compactification ceiling \(D_{\mathrm{eff}}=25\). **All** domains (core + expansion) are dimensional interfaces into one medium and one \(S=K(T_1+T_2+T_3)\).

## Master formula

```
S = K · (T1 + T2 + T3)
c = m · (1 + |S(interface)| · f)
# extensions: same law; f inherited from core / nearest-core DOMAIN_FACTORS
```

## 35 core domains (live S)

| D_eff | Domain | obs | S | sign | f | floor % |
|------:|--------|:---:|-----:|:----:|------:|--------:|
| 5 | `Particle_Physics` | True | +0.950413 | emergence | 0.0001 | 0.009504 |
| 6 | `Quantum_Mechanics` | True | +0.955506 | emergence | 0.001 | 0.095551 |
| 7 | `Atomic_Physics` | True | +0.735824 | emergence | 0.0005 | 0.036791 |
| 7 | `High_Energy_Physics` | True | +0.886264 | emergence | 0.00015 | 0.013294 |
| 8 | `Chemistry` | True | +0.407884 | emergence | 0.001 | 0.040788 |
| 8 | `Physical_Chemistry` | True | +0.334013 | emergence | 0.0005 | 0.016701 |
| 9 | `Electromagnetism` | True | +0.518866 | emergence | 0.0004 | 0.020755 |
| 9 | `Molecular_Chemistry` | True | +0.334573 | emergence | 0.001 | 0.033457 |
| 10 | `Acoustics` | True | +0.311591 | emergence | 0.0004 | 0.012464 |
| 10 | `Materials_Science` | True | +0.335260 | emergence | 0.0004 | 0.013410 |
| 10 | `Optics` | True | +0.408062 | emergence | 0.0004 | 0.016322 |
| 11 | `Quantum_Computing` | False | -0.147673 | damping | 0.0004 | 0.005907 |
| 11 | `Quantum_Optics` | True | +0.408171 | emergence | 0.0004 | 0.016327 |
| 12 | `Biology` | False | +0.444725 | emergence | 0.0005 | 0.022236 |
| 13 | `Biochemistry` | True | +0.306221 | emergence | 0.0005 | 0.015311 |
| 14 | `Condensed_Matter` | True | +0.338406 | emergence | 0.0004 | 0.013536 |
| 14 | `Neuroscience` | True | +0.514362 | emergence | 0.00035 | 0.018003 |
| 15 | `Ecology` | False | +0.300317 | emergence | 0.0002 | 0.006006 |
| 15 | `Fluid_Dynamics` | False | -0.562734 | damping | 0.0005 | 0.028137 |
| 15 | `Nuclear_Physics` | True | +0.921309 | emergence | 0.0005 | 0.046065 |
| 15 | `Thermodynamics` | True | +0.786975 | emergence | 0.0005 | 0.039349 |
| 16 | `Meteorology` | False | -0.484997 | damping | 0.0006 | 0.029100 |
| 16 | `Psychology` | True | +1.050206 | emergence | 0.0003 | 0.031506 |
| 17 | `Atmospheric_Physics` | False | -0.476432 | damping | 0.00055 | 0.026204 |
| 17 | `Oceanography` | False | -0.377159 | damping | 0.0008 | 0.030173 |
| 18 | `Seismology` | False | -0.445902 | damping | 0.0005 | 0.022295 |
| 18 | `Sociology` | True | +0.650147 | emergence | 0.0002 | 0.013003 |
| 19 | `Geophysics` | False | -0.549094 | damping | 0.0005 | 0.027455 |
| 20 | `Astronomy` | True | +0.898460 | emergence | 0.00025 | 0.022461 |
| 20 | `Economics` | True | +0.646005 | emergence | 0.0004 | 0.025840 |
| 21 | `Planetary_Science` | True | +0.767179 | emergence | 0.0003 | 0.023015 |
| 22 | `Quantum_Gravity` | False | -0.525598 | damping | 0.0002 | 0.010512 |
| 24 | `Astrophysics` | True | +0.882411 | emergence | 0.0003 | 0.026472 |
| 24 | `Particle_Astrophysics` | False | -0.424412 | damping | 0.0002 | 0.008488 |
| 25 | `Cosmology` | False | -0.502456 | damping | 0.0002 | 0.010049 |

## Extension expansion (371 domains)

Full per-domain \(S\) lives in the JSON (`extension_domains` array). Summary:

- By band: {'micro': 9, 'meso': 127, 'geo_climate': 164, 'astro': 71}
- By sign: {'emergence': 361, 'damping': 10}
- Sample: `NIST_CODATA_Constants`(D=7,S=+0.955), `Neutrino_Physics_Panel`(D=7,S=+0.886), `Founding_Quantum_Vacuum_Panel`(D=8,S=+0.734), `Information_Theory_Public_Panel`(D=8,S=+0.408), `PubChem_Compound_Properties`(D=8,S=+0.334), `Rust_Lean_Bridge`(D=8,S=+0.520), `Electrical_Power_Systems`(D=9,S=+0.303), `PDG_Particle_Properties`(D=9,S=+0.657)

## Consistency checks

- **PASS** `n_core_domains_35` — n_core=35
- **PASS** `n_extension_domains_ge_300` — n_ext=371
- **PASS** `n_total_interfaces_ge_400` — n_total=406
- **PASS** `cosmology_D25` — D=25
- **PASS** `cosmology_damping` — S=-0.5024559462100433
- **PASS** `nuclear_emergence` — S=0.9213094330291355
- **PASS** `particle_emergence` — S=0.9504134401245242
- **PASS** `core_factors_present` — missing=[]
- **PASS** `S_recompute_all_cores` — all 35 cores match
- **PASS** `S_recompute_extension_sample` — NIST_CODATA_Constants: 0.9554372598111504 vs 0.9554372598111504
- **PASS** `residual_floor_consistent_all` — floor=|S|f*100 for 406 interfaces
- **PASS** `K_pos` — K=0.4202216641606967
- **PASS** `C_EFF_pos` — C_EFF=0.9577022026205613
- **PASS** `POOF_pos` — POOF=0.1534822148944508
- **PASS** `authority_pin_file` — {'repinned_at': '2026-07-18T17:29:54.179057+00:00', 'authority_sha256': 'D1D38A1
- **PASS** `atlas_rows_ge_400` — atlas=403

## Benchmark envelope

- Green panels: 470 / 470
- Tier-scalar fails: 0
- Unmapped green (name heuristic): 117

Regenerate:

```powershell
python scripts/build_fsot_system_math_audit.py
```
