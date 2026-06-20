# arXiv Paper Outline (Draft)

**Working title:** Machine-Checked Sign Certificates for the FSOT Domain Scalar and Wave-1 ΛCDM Observables

**Target:** cs.LO (Logic in Computer Science) primary; astro-ph.CO or physics.comp-ph cross-list if emphasizing cosmology certificates.

**Length:** ~12–18 pages + supplementary source zip (`dist/fsot-lean-source-*.zip`)

---

## Abstract (draft)

We present a Lean 4 formalization of the FSOT domain scalar `raw_S = term1 + term2 + term3` across a 35-domain ledger, with machine-checked **sign certificates** at canonical parameters and interval certificates for five Wave-1 ΛCDM observables derived from cached cosmology and quantum scalars. A Python oracle and SHA-256 hash gate tie the formalization to a single authoritative compute engine. We document a proof playbook linking physical reasoning (dispersal dominance, observer/quirk modulation, recent-hits growth) to bound strategies that closed all prior proof obligations. We explicitly separate proved statements, numerically verified caches, and physical interpretation.

---

## 1. Introduction

- FSOT as a cross-domain scalar framework (motivation, not proof obligation)
- Gap: numeric agreement ≠ machine-checked guarantee
- Contribution: zero-`sorry` sign certificates + reproducible pipeline
- Paper scope: **what Lean proves** vs what physics claims

## 2. The FSOT Scalar Formalism (operational)

- `FSOTParams`: N, P, D_eff, δψ, recent_hits, observed, …
- Definitions: `term1_base`, `term1`, `term2`, `term3`, `raw_S`, `scaled_S`
- Default ledger: term2 = 1, |term3| ≪ 1 (β tiny)
- 35-domain taxonomy (table: D_eff, δψ, observed flag)

## 3. Formalization in Lean 4

- Module map: `Scalar`, `Bounds`, `Theorems`, `Domains`, `Cosmology`, `Lab`
- Proof architecture: shared templates + per-domain certificates
- Key templates:
  - `raw_S_positive_of_term1_gt_neg_08`
  - `raw_S_negative_of_term1_overcomes_term3`
- Axiom audit: Mathlib only, no custom axioms
- Toolchain: Lean 4.31.0, Mathlib v4.31.0

## 4. Verification Pipeline

- `domain_scalar_oracle.py` — numeric mirror
- `sync_canonical_constants.py` — cache from authority
- `fsot_verification_runner.py` — hash gate + Wave-1 + `lake build`
- `export_certificate.py` → `data/certificate.json`
- `data/proof_ledger.yaml` — human/knowledge bridge
- `fill_smiles_catalog_gaps.py` — resolves 8 SMILES Tier-22 export gaps
- `align_neurolab_domains.py` — patches 17/35 NeuroLab domains to Lean ledger params
- `ingest_lab_data.py` / `verify_lab_registry.py` — SMILES + NeuroLab cross-validation

## 5. Results

### 5.1 Domain sign certificates

| Domain | Claim | Oracle raw_S | Lean theorem |
|--------|-------|--------------|--------------|
| cosmological | < 0 | −1.20 | `cosmological_raw_S_negative` |
| dark_energy | < 0 | −1.13 | `dark_energy_raw_S_negative` |
| cmb | < 0 | −1.01 | `cmb_raw_S_negative` |
| ai | ≤ 0 | −0.35 | `ai_raw_S_non_positive` |
| medical | > 0 | +0.73 | `medical_raw_S_positive` |
| chemical | > 0 | +0.80 | `chemical_raw_S_positive` |
| electron | > 0 | +0.97 | `electron_raw_S_positive` |
| neural | > 0 | +1.22 | `neural_raw_S_positive` |
| quantum | > 0 | +2.27 | `quantum_raw_S_positive` |
| … | … | … | … |

(Full table in supplementary ledger.)

### 5.2 Wave-1 interval certificates (cached scalars)

| Observable | FSOT formula | Formal bound | Planck-class reference |
|------------|--------------|--------------|------------------------|
| H₀ | `h0_fsot(S_cosm)` | ±1e−8 vs cache | 67.4 ± 0.5 km/s/Mpc |
| T_CMB | `t_cmb_fsot(S_cosm)` | ±1e−6 vs cache | 2.7255 ± 0.0006 K |
| n_s | `n_s_fsot(S_cosm)` | ±1e−4 vs cache | 0.9649 ± 0.0042 |
| Ω_b h² | `omega_b_h2_fsot(...)` | ±1e−5 vs cache | 0.02237 ± 0.00015 |
| α_s(M_Z) | `1/(eπ)` | ±1e−8 vs cache | 0.1179 ± 0.0010 |

**Important:** Formal proofs establish internal consistency at cached inputs; external comparison is empirical validation (§6).

### 5.3 Lab integration certificates

- **SMILES Lab:** 1470/1470 records mapped via `section_domain_map.json`; 8 catalog gaps filled (§90–§95, max error 2.78%)
- **NeuroLab:** thalamic gate K within 5×10⁻⁴ of formal `k`; 17 domains ledger-aligned; brain-fit mean_abs_gap &lt;0.15
- **Lean:** `FSOT.Formal.Lab` — `lab_smiles_domain_sign_bundle` (11 positive domain signs + Layer-2 alignment)

### 5.4 Baryon drag horizon

- `r_d = r★(1 + δλ)` with interval certificate |r_d − 147.52| < **0.05** Mpc
- DESI/BAO band discussion; ±0.01 tightening left as future work

## 6. External Validation and Limitations

- Compare Wave-1 to Planck 2018 / DESI 2024 (with uncertainties)
- Sign proofs do not certify full magnitude agreement across parameter sweeps
- Physical interpretation of terms is **conjectural** / heuristic
- Domains not in `Domains.lean` table may lack individual theorems
- Dependency on single authority `fsot_compute.py` digest

## 7. Proof Playbook (Methods contribution)

Physics-to-proof patterns from `proof_ledger.yaml`:

1. **Wrong bound direction** — lower-bound `term1 > −0.8` for weak dispersal + observer boost
2. **Wrong hits template** — `recent_hits` in growth_term / rexp
3. **Dominance ≠ sign** — need |term1| > 1 + |term3| when term2 = 1
4. **raw vs scaled** — prove on `raw_S`, scale by k > 0 separately

## 8. Related Work

- Formal proof in physics (Flyspeck, QED, cosmological constants in proof assistants)
- Interval arithmetic / numeric proof certificates
- ML + Lean (AlphaProof, etc.) — contrast: hand-crafted domain bounds here

## 9. Conclusion and Future Work

- Portable `certificate.json` for downstream FSOT projects
- Tighten r_d to ±0.01 Mpc
- Extend to remaining ledger domains
- Export interval certificates to runtime MPFR checker (no Lean at inference)

## Supplementary Material

- Source zip via `python scripts/make_source_release.py`
- `REPRODUCE.md` one-page build
- `data/proof_ledger.yaml` full entries

---

## Claim Taxonomy (required table for submission)

| Category | Definition | Examples in this work |
|----------|------------|------------------------|
| **Proved** | Lean QED, no `sorry` | `medical_raw_S_positive`, `r_d_approx_value` |
| **Numerically verified** | Oracle/hash gate match | Wave-1 cache, domain oracle rows |
| **Conjectured** | Stated, not formalized | FSOT as fundamental physical framework |
| **Interpretation** | Physics narrative | “dispersal dominance at high D_eff” |
| **Empirical** | External data agreement | H₀ vs Planck (not a Lean theorem) |

---

## Checklist before submission

- [ ] Author ORCID, affiliations
- [ ] Data availability: GitHub / Zenodo source-only archive
- [ ] Run `fsot_verification_runner.py` on clean machine; attach log
- [ ] Confirm `sorry_count_formal = 0` in `certificate.json`
- [ ] Bibliography: Planck 2018, DESI BAO, Lean 4, Mathlib
- [ ] Figure: pipeline diagram (oracle → Lean → certificate)
- [ ] Figure: term1/2/3 decomposition for 3 hard domains (medical, cmb, cosmological)
- [ ] Reviewer FAQ: “Does this prove FSOT is correct physics?” → No; sign certificates at canonical params