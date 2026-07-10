# Quantum_Materials Domain — FSOT 2.1

**Created:** 2026-07-09
**Status:** Tier-27 extension domain (condensed-matter SMILES depth)
**Core Idea:** Zero-parameter FSOT scalar predictions for band gaps, superconducting Tc, lattice parameters, magnetic ordering, crystal-field splittings, and related condensed-matter observables via the SMILES lab dataset.

## Scalar Results (D_eff=16)
- D_eff: 16
- observed: true
- delta_psi: 0.7
- recent_hits: 2
- Sections: 13 condensed-matter SMILES property classes (168 observables)
- Precision tail: smiles_seed_precision_overrides.json (548 applied overrides)

## Maps To Lean
- material
- quantum

## Related Notes
- [[Materials_Science]]
- [[Condensed_Matter]]
- [[Quantum_Mechanics]]
- [[FSOT_Compute_Engine]]

## Predictions Tested
FSOT zero-parameter medians beat Materials Project DFT-class baselines (~5%) on pooled condensed-matter observables and on hardest sections (band gaps, crystal field, μeff, Tc).