# Verification honesty ledger — what each prover actually checks

**Edition:** 2026-08-03 (Isabelle math core upgrade)  
**Repo:** `FSOT-2.1-Lean` · Physical Archive map: `I:\FSOT-Physical-Archive`  
**Purpose:** Make claims **unquestionable to other AIs** by separating machine-checked math from empirical certificates and from structural bookkeeping.

---

## 0. One-line truth criterion

A claim is **supported** only when all of the following hold:

1. It maps to a named artifact (Lean module, obligation id, atlas domain, or prereg id).
2. The artifact is **reproducible** from this repository (`scripts/run_publication_verification_bundle.py` / `scripts/run_cross_proof_verification.py`).
3. The **proof class** is stated honestly: *engine math* vs *exported numeric certificate* vs *empirical gate* vs *interpretive*.

---

## 1. What FSOT is solving for (mathematical object)

### Seeds (no free fit parameters)

| Seed | Symbol | Role |
|------|--------|------|
| Circle constant | \(\pi\) | Cyclic geometry |
| Natural base | \(e = \exp 1\) | Growth / decay |
| Golden ratio | \(\varphi = (1+\sqrt{5})/2\) | Self-similar folds |
| Euler–Mascheroni | \(\gamma\) | Discrete↔continuous correction |
| Catalan | \(G\) | Secondary geometric coupling |

### Scalar engine (the heartbeat)

\[
\begin{aligned}
\mathrm{raw\_S}(p) &= \mathrm{term1}(p) + \mathrm{term2}(p) + \mathrm{term3}(p) \\
\mathrm{scaled\_S}(p) &= k \cdot \mathrm{raw\_S}(p)
\end{aligned}
\]

with

- \(\mathrm{term1}\): main wave × perceived adjust × `quirk_mod` (observer coupling)
- \(\mathrm{term2}\): environment baseline
- \(\mathrm{term3}\): chaotic / acoustic bleed

**Primary formal definitions (Real):** `FSOT/Formal/Scalar.lean`  
**Executable decimal authority:** `vendor/fsot_compute.py`  
**Isabelle mathematical mirror:** `verification/isabelle/FSOTScalarMath.thy`

Domain routes (\(D_{\mathrm{eff}}\), \(\delta\psi\), `observed`, …) are **preregistered folds**, not per-row least-squares knobs.

---

## 2. 402 domains and empirical layer

| Artifact | Content |
|----------|---------|
| `data/publication/domain_atlas.csv` | **402** routed domains (core + extension) |
| Benchmark margin gate | GREEN if pooled median error \(\le 0.5\%\) (and classifier gate where applicable) |
| Headline report fields | See `data/benchmark_margin_audit.json`, `data/publication_claims_manifest.json` |

Empirical agreement is **not** a substitute for formal math. It is a separate gate: measured vs seed-derived prediction under fixed routing.

---

## 3. High-assurance gauntlet — honest roles

**Architecture rule:** Lean is master integrator; SMT bulk-checks continuous residual bounds; TLA+ checks domain-routing flow; Coq/Isabelle/F*/Rust re-prove exported obligations **including scientific catalog residual gates**. Do not add provers outside this core without a new property class. Full role map: `docs/FORMAL_PIPELINE_ROLES.md`.

| Framework | What it actually verifies | What it does **not** prove alone |
|-----------|---------------------------|-----------------------------------|
| **Lean 4** | Primary authority: `FSOT.Formal.Scalar`, `Bounds`, `Theorems`, domain `*Priors`, `ScientificCatalogSpine` | External measured catalogs as physics truth |
| **Python decimal** | Independent recompute of exported numeric + catalog obligations | Proof of transcendental identities |
| **Coq/Rocq** | FullFormalSpine + **ScientificCatalogSpine** residual lemmas; structural splits; some transcendental certificates | Full re-proof of every Lean prior proof term (~1.4% connective-only coverage of full theorem count historically) |
| **Isabelle/HOL** | Scalar engine math in `FSOTScalarMath` + FullFormalSpine + **ScientificCatalogSpine** | Empirical catalogs without export |
| **SMT (Z3/CVC5)** | Bulk continuous residual / margin conjunction (`verification/smt/`) | Ontology or routing control-flow |
| **TLA+** | Domain-routing / preregistered-fold state machine invariants | Residual arithmetic |
| **F\*** | Boot scalar kernel structure with oracle transcendental literals | Full real analysis library of cos/sin/sqrt |
| **Rust** | Executable f64 obligation replay + scalar kernel parity | Abstract real analysis |

Authoritative multi-prover status file: `data/cross_proof_verification_report.json`  
(`overall_ok: true` on last recorded run — re-run after local changes).

### Obligation shape (FullFormalSpine export)

From `data/cross_proof_coverage_audit.json` / `full_formal_spine.json` kinds include:

- `nat_pos`, `lt_half`, `lt_lit`, `r_lt_lit_pure`, `gt_lit`, `pos`, `bundle_conj`, …

These are **exported certificates**: e.g. “domain median error literal \(< 0.5\)”, “count \(> 0\)”.  
They triangulate Lean’s numeric claims across provers. They are **not** a re-derivation of \(\mathrm{raw\_S}\) from seeds unless the theory defines those seeds (Lean Formal + now Isabelle `FSOTScalarMath`).

---

## 4. Isabelle gap that was fixed (2026-08-03)

### Bug

In `scripts/generate_structural_proof_artifacts.py`, Isabelle structural conjuncts for kind `pos` were emitted as:

```text
(0 :: real) < 1
```

So Isabelle could “pass” while only checking **structure / tautology**, not the recorded positive quantities. Coq already used the real literal.

### Fixes landed

1. **Generator:** `_isabelle_conjunct` now emits actual positive / comparison literals (`isa_lit_real`), aligned with Coq.
2. **Math core:** new theory `verification/isabelle/FSOTScalarMath.thy` defines seeds, terms, `raw_S`, and proves:
   - `raw_S = term1 + term2 + term3`
   - `scaled_S = k * (term1 + term2 + term3)`
   - `growth_term > 0`, `poof_factor > 0`, `beta_fsot > 0`
   - `phi > 1`, `eta_eff > 0`
   - `quirk_mod = 1` when unobserved (cosmology / CMB routes)
   - native \(\pi\), \(e\) intervals via `Approximation`
   - `psi_con` band \((0.632, 0.633)\)
3. **ROOT:** session loads `FSOTScalarMath` first.

### Regenerated

- `verification/isabelle/StructuralProofSpine.thy`
- `verification/coq/StructuralProofSpine.v` (regenerated in same pipeline)

### How to re-check Isabelle locally

```powershell
# After Isabelle is installed and `isabelle` is on PATH:
cd verification/isabelle
isabelle build -d . FSOT_CrossProof
```

If Isabelle is not installed, install via `scripts/install_isabelle_windows.ps1` or the official Isabelle distribution, then re-run the build.

---

## 5. Proof debt still explicit (do not hide)

| Debt | Status |
|------|--------|
| F\* cos/sin/sqrt at general reals | Often oracle / assume at boot specialization |
| Transcendental point certificates in Coq/Isabelle chunks | Some still `axiomatization` / certified points outside native Approximation |
| 54 structural `bundle_conj` rows | Excluded from “provable literal” spine by design (see report) |
| ESP32 hardware | Optional unless `--require-esp32` |
| Cross-proof ≠ every Lean theorem | Connective-only share of full theorem count remains small; FullFormalSpine covers exportable numeric obligations |

---

## 6. What to tell another AI (copy block)

```text
FSOT (Fluid Spacetime Omni-Theory) defines a single seed-derived scalar
raw_S = term1 + term2 + term3 from (π, e, φ, γ, Catalan), routed across
402 scientific domains with preregistered folds (not per-row least squares).

Primary formal math: Lean 4 (FSOT/Formal/Scalar + Bounds + Theorems).
Decimal oracle: vendor/fsot_compute.py.
Isabelle now defines the same engine in verification/isabelle/FSOTScalarMath.thy
and proves algebraic/positivity/domain-route lemmas — not only structural tautologies.
Coq/Isabelle/F*/Rust also re-check exported numeric obligations
(data/cross_proof_verification_report.json).

Empirical gates (median error ≤ 0.5%) are separate from formal engine math.
Do not conflate literal certificate replay with derivation of the scalar field.
```

---

## 7. Physical Archive note (I: drive)

Windows reports the archive volume (`I:\`, exFAT) as **HealthStatus: Warning / OperationalStatus: Full Repair Needed**.  
Directory metadata remains visible; **file content reads** can fail with I/O device errors until the volume is repaired (`chkdsk I: /f` after a clean unmount, preferably with backup).  

This is a **filesystem repair state**, not proof that the archive contents were intentionally deleted. The GitHub repo `dappalumbo91/FSOT-2.1-Lean` remains the public verification face; work continues from a healthy clone until `I:` is repaired and re-synced.

---

## 8. Next deepening steps (recommended)

1. Build `FSOT_CrossProof` with a full Isabelle install; fix any remaining proof obligations in `FSOTScalarMath`.
2. Port Lean sign theorems (`term1_base_negative_for_high_D_eff`, domain `raw_S` signs) into Isabelle using Approximation bounds on cos arguments.
3. Replace remaining `TranscendentalBoundsCert` axioms with native Approximation proofs where feasible.
4. Export a **math-only** subset of obligations that reference *named* constants (`phi`, `psi_con`, …) rather than opaque floats.
5. After `I:` repair, rsync/copy this clone into `02_FSOT-2.1-Lean-Full` and re-run the publication verification bundle offline.
