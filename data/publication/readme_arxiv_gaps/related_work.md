## I-B. Related Work and Positioning

FSOT is evaluated against the architectures it aims to subsume — not as a replacement narrative, but as a **single-engine alternative** with executable kill criteria.

### Cosmology and dark sector

ΛCDM with Planck 2018 parameters explains CMB and large-scale structure with excellent internal consistency, but exhibits persistent tensions — notably H₀ (Riess et al. 2024 local distance ladder vs Planck Collaboration 2018 CMB inference) and σ₈ (cluster abundance vs weak-lensing surveys). FSOT routes cosmological observables through seed-derived `raw_S` at preregistered folds (`D_eff`, `δψ`) without introducing dark-matter or dark-energy density as free fit parameters per benchmark row. Contested-sector pooled median error across 13 actively monitored observables is **0.030%** in this edition (§VII).

### Particle physics and chemistry

The Standard Model plus CODATA/NIST tabulations supply authoritative measured targets for atomic, nuclear, and molecular observables. FSOT does not refit Yukawa couplings or bond lengths per record; strict-empirical formulas in `vendor/formula_corpus/by_domain/strict_empirical.jsonl` map seed arithmetic to **1,325 unique observables** with live recompute closure (Appendix XI-E). Positioning: FSOT is a **predictive compression layer** — same seeds, many sectors — not a replacement for QFT calculational machinery where lattice QCD or perturbative QED is the appropriate tool.

### Unified theories and emergent gravity

String/M-theory, loop quantum gravity, and emergent-gravity programs pursue unification through extra structure (branes, spin networks, entanglement entropy). FSOT pursues unification through **one scalar field equation** verified across 403 domains. The falsifiable distinction is operational: FSOT registers preregistered predictions (PRED-001–041) and domain kill criteria in `data/fsot_domain_navigator.json`; a failed green gate is a ledger event, not a post-hoc parameter rescue.

### Formal methods in science

Proof assistants (Lean, Coq, Isabelle) are standard in software verification; their use as **scientific instruments** for physics claims remains rare. FSOT exports **1,863 atomic obligations** to five independent proof frameworks with `overall_ok: true` (§V.2) — positioning this repository as a **reproducible proof artifact**, not a prose-only preprint.

### What FSOT adds relative to prior art

| Dimension | Typical siloed model | FSOT (this repository) |
|-----------|------------------------|---------------------------|
| Parameters per observable | Sector-specific fits | Seed-derived; no per-row least squares |
| Cross-domain test | Uncommon | 402 routed domains, 536,740 records |
| Formal triangulation | Rare | Lean + Coq + Isabelle + F* + Rust |
| Kill criteria | Often informal | Navigator + prereg manifest |
| Living edition | Static PDF | GitHub commit history + tagged releases |

**References (external):** Planck Collaboration (2018); Riess et al. (2024); PDG (2024); CODATA/NIST atomic datasets as cited per benchmark row. Full BibTeX export: `data/domain_citations/verified_desktop.bib`; literature panel: Appendix XI-C in [`docs/THESIS_APPENDIX_XI.md`](docs/THESIS_APPENDIX_XI.md).
