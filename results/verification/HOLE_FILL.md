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

## Remaining 19 empirical C_thin

Founding laws (5–6 literature anchors each), Higgs (10 channels), PDG (12), DESI slices (10–18), NuFIT (10), Dark Energy CPL (14), orbital (9), NIST CODATA (8), cosmology anomalies (12), Matter/Antimatter (17), SH0ES refined hosts (7), NIST ASD (13).

Fill these **only** when another **on-topic** public table exists. Then:

```powershell
python scripts/add_ontopic_c_thin_anchors.py
python scripts/audit_all_benchmark_margins.py
```

Then cross-proof.
