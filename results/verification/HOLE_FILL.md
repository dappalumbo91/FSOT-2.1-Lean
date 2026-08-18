# Hole fill — 2026-08-18

Green gate after this pass: **472 / 472**. Pin D1D38A. No free parameters.

## Falsification registry

Rebuilt from the living YAML (`predictions/preregistered_predictions_manifest.yaml`).

| Item | Value |
|------|------:|
| Prereg PREDs | **48** |
| Stumped / contested | 13 |
| Status overlay | `results/outcomes/prediction_outcome_log.jsonl` |
| Flagship envelope | `472_file_green_gate` (was 272) |

`python scripts/build_falsification_registry_closure.py`

## C_thin (29 → honest split)

| Class | n | What we did |
|-------|--:|-------------|
| Process / certificate ledgers | 9 | Tagged `coverage_role: process_ledger`. Not densified. |
| Science, on-topic fill | 1 | **NIST_DLMF** 5 → **21** seed-closed identities (Γ, ζ, erf, J0…). B_verified. |
| Science, still thin | 19 | Off-topic formula-corpus rows **removed**. Literature anchors kept. |

We tried dumping the seed-formula corpus into every thin panel. That put pH of water on a cosmology panel. That is forbidden. Those rows are gone.

SH0ES 25-tool H₀ was **not** stuffed into `sh0es_refined_benchmark.json`. Those 1% residuals are the contested bubble-bleed band. They live in `predictions/h0_multi_tool_predictions.json`. Putting them in the 0.5% gate would have failed the panel for the wrong reason.

## FSOT-Quantum Higgs import (this pass)

Quantum solves the mass as

`(θ_S + e³)/C_factor⁷ / 1000` = **125.200 GeV** vs PDG **125.25** (0.0399%).

That is the High_Energy_Physics fold — not the FO-213 NLO overlay (125.264). Branching ratios from the same pin (YR4 literature for H→gg, not the stale vendor 0.0785).

| Panel | Before | After | Tier |
|-------|-------:|------:|------|
| higgs_mass | 10 | **23** | **B_verified** |
| PDG_Particle_Properties | 12 | **27** | **B_verified** |
| Dark_Energy_CPL | 14 | **20** | **B_verified** |
| NuFIT_Neutrino_Open | 10 | 12 | still C_thin |
| Matter_Antimatter | 17 | 18 | still C_thin |

Green after import: **472 / 472**.

`python scripts/import_fsot_quantum_ontopic.py`

## Continue fill (this pass)

On-topic only: Quantum folds, JPL Kepler caches + SBDB dwarfs, NIST ASD handbook lines. No formula-corpus dump. No SH0ES 1% tools.

`python scripts/continue_c_thin_fill.py`

| Panel | Before | After | Tier |
|-------|-------:|------:|------|
| Matter_Antimatter | 18 | **27** | **B_verified** |
| NuFIT_Neutrino_Open | 12 | **20** | **B_verified** |
| cosmology_anomalies | 12 | **28** | **B_verified** |
| NIST_CODATA_Constants | 8 | **20** | **B_verified** |
| DESI_Public_Depth_Open | 10 | **20** | **B_verified** |
| DESI_EDR_Table_Slice_Open | 18 | **22** | **B_verified** |
| orbital_mechanics | 9 | **21** | **B_verified** |
| NIST_ASD_Spectroscopy_Open | 13 | **24** | **B_verified** |

Green after continue fill: **472 / 472**.

## Remaining empirical C_thin

| Class | n | Why still thin |
|-------|--:|----------------|
| Founding laws (7 panels) | 5–6 | Only the public literature anchors in `founding_unmapped_laws_reference.json`. No extra table. |
| SH0ES_Refined | 7 | 1% bubble-bleed tools stay in `predictions/h0_multi_tool_predictions.json`. |

Process / certificate ledgers: **9** (still tagged, not densified).

Then:

```powershell
python scripts/audit_all_benchmark_margins.py
python scripts/run_cross_proof_verification.py
```
