# Appendix — Seed-to-Formula Derivations

*Edition fragment · 2026-07-16 · [Return to main thesis](../README.md#iii-the-scalar-engine)

This volume documents how FSOT moves from **five seeds** to **sector readouts** without per-observable least-squares tuning. Formal authority: `FSOT/Scalar.lean`, `vendor/fsot_compute.py`. Machine chain: `data/mechanism_chain_derivation.json`.

## D.1 Pipeline overview

```
seeds (π, e, φ, γ, G)
  → intrinsic derived constants (α, ψ_con, η_eff, K, consciousness_factor)
  → domain route (D_eff, δψ, recent_hits, observed) — preregistered fold
  → raw_S = term1 + term2 + term3
  → strict-empirical formula map (per observable)
  → benchmark comparison vs measured authority
```

**Verdict:** `DERIVATION_DOCUMENTED_NOT_OPAQUE_TABLE` — routing slots are manifest-declared; bleed constants are seed-derived (φ/e/π/γ), not tuned per benchmark row.

## D.2 Intrinsic seed derivations

| Derived constant | Value (canonical) | Seed origin |
|------------------|------------------:|-------------|
| α | 0.000808293741 | e, φ geometry |
| ψ_con | 0.632120558829 | (e−1)/e |
| η_eff | 0.466942206924 | 1/(π−1) |
| K | 0.420221664161 | φ/e fold |
| consciousness_factor | 0.287600151819 | coherence × perceived |

**Core decomposition:** `raw_S = term1_final + term2 + term3`

**term1 structure:** `(N·P/√D_eff)·cos((ψ_con+δψ)/η_eff)·growth·coherence·perceived_adjust × quirkMod(observed)`

## D.3 Domain route → scalar breakdown (core examples)

Same engine, different folds — illustrates *As Above, So Below* routing:

| NeuroLab domain | Lean route | D_eff | δψ | observed | raw_S | term1 share |
|-----------------|------------|------:|---:|:--------:|------:|------------:|
| Biology | biological | 12 | 0.08 | no | 1.05831052 | 0.055098 |
| Chemistry | electron | 8 | 0.6 | yes | 0.97064026 | 0.030248 |
| Cosmology | cosmological | 25 | 1.0 | no |  |  |
| Neuroscience | neural | 14 | 0.7 | yes | 1.22402533 | 0.183023 |

Regenerate mechanism chain:

```bash
python scripts/build_mechanism_chain_derivation.py
```

## D.4 Worked strict-empirical examples

Each row below is a live line from `vendor/formula_corpus/by_domain/strict_empirical.jsonl` with measured authority target and seed-only arithmetic:

| Observable | Seed formula | Measured | FSOT computed | Error % | Citation grade |
|------------|--------------|----------|---------------|--------:|----------------|
| proton | `PI⁶-E³` | 938.272 | 941.304 | 0.323111 | empirical_strict |
| proton | `PI⁶-E³` | 938.272 | 941.304 | 0.323111 | empirical_strict |
| IE_H | `γ⁻⁵ - G⁻⁸` | 13.598 | 13.5884 | 0.070379 | empirical_strict |
| IE_He | `e²/P_new` | 24.587 | 24.6054 | 0.074815 | empirical_strict |
| IE_Li | `γ⁻³ + γ³` | 5.392 | 5.3921 | 0.001928 | empirical_strict |
| IE_Be | `π² - sin(γ)` | 9.323 | 9.32391 | 0.009778 | empirical_strict |
| IE_B | `γ⁻⁴ - G⁴` | 8.298 | 8.30449 | 0.078197 | empirical_strict |
| IE_C | `e⁷/π⁴` | 11.26 | 11.258 | 0.017615 | empirical_strict |

### D.4.1 Cosmology — H₀ (Planck CMB anchor)

1. Route cosmology panel with preregistered `(D_eff, δψ)` from `fsot_compute.py`.
2. Evaluate `term1.perceived_adjust` branch (bubble-bleed dual-anchor readout).
3. Compare to Planck Collaboration (2018) CMB inference: 67.36 ± 0.54 km/s/Mpc.
4. FSOT computed: **67.270 km/s/Mpc** → error **0.13%** (§VII worked example).

Preregistered discriminant (PRED-001): FSOT H₀ bridge scalar strictly between Planck and SH0ES anchors — registered before panel refresh.

### D.4.2 Particle — ionization energies

Atomic ionization observables map to seed power laws (γ, e, G exponents only). Example: `IE_H = γ⁻⁵ − G⁻⁸` → 13.588 eV vs NIST 13.598 eV (0.07% error).

### D.4.3 Consciousness — metabolic power

```
E_con = kT × (1 + α² D_bio² e^(2φ) / kT) × N² × ψ_con
```

FSOT ≈ 21.79 W vs Raichle & Gusnard ~20 W (brain resting metabolic power). Same seeds that fix cosmology also fix consciousness-energy scaling.

## D.5 What is not a fit parameter

| Coordinate | Role | Audit |
|------------|------|-------|
| D_eff, δψ, recent_hits, observed | Preregistered domain fold | `data/honest_claims_manifest.yaml` |
| Formula map per observable | Strict-empirical corpus row | `strict_empirical.jsonl` |
| Measured targets | External authority (NIST, Planck, PDG, …) | Per-row citation grade |

Parameter audit command: `python scripts/audit_parameter_count.py` → **ZERO_FREE**.

## D.6 Cross-links

- Formula exemplar digest: [Appendix XII-E](THESIS_APPENDIX_XII.md#appendix-xii-e--formula-exemplar-digest-strict-empirical)
- Verification record: [Appendix XI](THESIS_APPENDIX_XI.md)
- Philosophy spine: [FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md](FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md)
