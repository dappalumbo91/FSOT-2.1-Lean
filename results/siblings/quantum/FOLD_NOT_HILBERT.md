# Fold-not-Hilbert suite

**overall_ok:** `True`
**pass:** `27/27`
**wall_s:** `1.368`

## Thesis

QC jobs via FSOT domain folds / modular algebra / collapse — not Hilbert 2^n expansion

## The bottleneck (correct term)

Hilbert-space dimension / degrees of freedom — amplitudes in C^{2^n}; cost explodes with qubit count

## FSOT scaling

Complexity as domain folds (D_eff routes) + modular/algebraic structure + collapse/consensus — poly probes, not 2^n amplitudes

## Cost contrast examples

- n=20 Hilbert amps `1048576` vs fold budget `398` (ratio ~2635×)
- n=32 Hilbert amps `4294967296` vs fold budget `621` (ratio ~6916211×)

## Job families

| Job | Pass | OK |
|-----|------|----|
| oracle_class_DJ | 4/4 | True |
| secret_parity_BV | 2/2 | True |
| marked_search_Grover | 3/3 | True |
| period_order_Shor | 6/6 | True |
| factor_Shor_end | 8/8 | True |
| ising_optimize_QAOA_role | 3/3 | True |
| phase_class_QPE | 1/1 | True |

## Nested D_eff folds

- fold 0: **Quantum_Mechanics** D_eff=6 S=0.9555 (emergence) — measurement / spin resolve
- fold 1: **Quantum_Computing** D_eff=11 S=-0.1477 (damping) — compute substrate
- fold 2: **Quantum_Optics** D_eff=11 S=0.4082 (emergence) — phase / optics class

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_suite
```

## Note

Hilbert fragments (climb v1/v2) remain available as optional bridges; fold path is the scaling law for competitor jobs
