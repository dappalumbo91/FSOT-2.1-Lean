# FSOT Monograph Verification Bundle v1

**Tag:** `fsot-monograph-v1`  
**Commit:** `50b6d4d5ef3a`  
**Date:** 2026-07-15

## Fluid Spacetime Omni-Theory (FSOT)

Cross-domain empirical and formal verification of a seed-derived scalar engine.

| Metric | Value |
|--------|------:|
| Scientific domains | 403 |
| Empirical records | 536,740 |
| Benchmark domains green (≤0.5%) | 394/394 |
| Cross-domain pooled median | 0.013003% |
| Five-prover cross-proof | overall_ok=True |
| Atomic formal obligations | 1863 |

Formal verification: Lean 4 → Coq → Isabelle → F* → Rust executable replay.

## Bundle contents

- `fsot_monograph_skeleton.md` — full ToE paper structure
- `domain_atlas.csv` — 403-domain verification table
- Figures, cross-proof report, publication claims manifest
- Preregistered predictions, BibTeX citations

## Reproduce

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
python scripts/run_publication_verification_bundle.py
```

## Author note

Verification runs through independent proof frameworks (Lean, Coq, Isabelle, F*,
Rust) against 536,740 measured records across 403 domains. AI tools assisted
assembly; all claims reproduce from this repository. Author retains scientific
responsibility.

## Cite

```
dappalumbo91/FSOT-2.1-Lean (fsot-monograph-v1). GitHub Release.
https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/tag/fsot-monograph-v1
```
