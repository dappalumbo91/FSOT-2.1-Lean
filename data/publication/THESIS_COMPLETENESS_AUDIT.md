# FSOT Thesis Completeness Audit

*Generated: 2026-07-16T13:17:42.099485+00:00*

Top-to-bottom comparison of **living thesis** (`README.md`) against **philosophy spine**, **monograph skeleton**, and **live verification artifacts**.

## Executive summary

| Check | Status |
|-------|--------|
| Verification bundle (`overall_ok`) | `True` |
| Benchmark green gate | `394/394` |
| Cross-proof atomic obligations | `1863` |
| Contested pooled median | `0.029748999999999998%` |
| Domain atlas rows (routed) | `402` (35 core + 367 extension = 402) |
| Preregistered predictions | `35` |
| Ideals in main README | `20/20` |

## Crucial FSOT ideals — coverage matrix

| Ideal / topic | README | Philosophy spine | Monograph skeleton |
|---------------|:------:|:----------------:|:------------------:|
| 25D fluid ontology | ✓ | ✓ | — |
| As Above So Below | ✓ | ✓ | ✓ |
| Zero free parameters | ✓ | ✓ | ✓ |
| Seed engine (π,e,φ,γ,G) | ✓ | ✓ | ✓ |
| raw_S emergence/dispersal | ✓ | ✓ | ✓ |
| quirk_mod / observation | ✓ | ✓ | — |
| Consciousness fundamental | ✓ | ✓ | — |
| Epistemology / truth criterion | ✓ | ✓ | — |
| Bubble-bleed cosmology | ✓ | — | — |
| Preregistered PRED manifest | ✓ | — | ✓ |
| Founding 35 laws | ✓ | — | — |
| Five-prover cross-proof | ✓ | ✓ | ✓ |
| Contested sectors (H₀, σ₈) | ✓ | ✓ | ✓ |
| Engineering demos (main thesis) | ✓ | — | ✓ |
| Transporter supplementary volume | ✓ | — | ✓ |
| Strict-empirical corpus | ✓ | ✓ | — |
| Domain atlas / coverage | ✓ | ✓ | ✓ |
| Derivation appendix | ✓ | — | — |
| Formal vs interpretive tiers | ✓ | ✓ | — |
| Soul-bridge / SR-ITE | ✓ | ✓ | — |

## Gaps still thin in main thesis (action list)

- No critical ideal gaps detected in README prose (audit patterns matched).

## Domain count reconciliation

Authoritative routed domain count: **402** = 35 NeuroLab core + 367 extension panels (`data/fsot_domain_navigator.json`, `domain_atlas.csv`). Prior editions cited **403** from `scientific_domain_expansion_map.yaml` summary rollup — reconciled in v2.1 to **402**.

## Regeneration chain (top to bottom)

```bash
python scripts/run_publication_verification_bundle.py
python scripts/build_mechanism_chain_derivation.py
python scripts/build_thesis_appendix_derivations.py
python scripts/build_readme_domain_chapters.py
python scripts/build_readme_thesis_expansion.py
python scripts/build_readme_arxiv_gaps.py
python scripts/merge_readme_arxiv_thesis.py
python scripts/build_thesis_completeness_audit.py
```

## Source files

| Artifact | Path |
|----------|------|
| readme | `README.md` (yes) |
| philosophy | `docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md` (yes) |
| monograph | `data/publication/fsot_monograph_skeleton.md` (yes) |
| derivations | `docs/THESIS_APPENDIX_DERIVATIONS.md` (yes) |
| claims | `data/publication_claims_manifest.json` (yes) |
| cross_proof | `data/cross_proof_verification_report.json` (yes) |
| margin | `data/benchmark_margin_audit.json` (yes) |
| atlas | `data/publication/domain_atlas.csv` (yes) |
| prereg | `data/preregistered_predictions_manifest.yaml` (yes) |
