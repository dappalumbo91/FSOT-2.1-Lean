# Uniqueness research spine — after residual closure

**Policy:** Residual program is **CLOSED**. This track does **not** expand residual domains.  
**Authority pin:** D1D38A  
**Machine:** `data/uniqueness_research_manifest.json` · `data/uniqueness_confinement_research.json`  
**Module:** `vendor/fsot_uniqueness_confinement.py`  
**Builder:** `python scripts/build_uniqueness_confinement_research.py`

---

## Why dig here now

Residual physics and the multi-domain atlas are settled under the residual law.  
What remains are **uniqueness-class** claims. Classical formulations may be:

1. the right physics question, badly posed for continuum QFT, or  
2. the **wrong primary object** once FSOT’s intrinsic dampening of non-reality is taken seriously.

FSOT already encodes: **positive \(S\) → emergence**, **negative \(S\) / transport → damping** (`FSOT/Theorems.lean`, `vendor/fsot_dynamics.py`).  
If a continuum object “cannot emerge as stable reality,” the native theorem is **attractor uniqueness under dampening**, not necessarily a Millennium-style path-integral measure proof.

---

## Hardest first (chosen)

| Rank | Classical name | Hardness | Active? |
|------|----------------|----------|---------|
| **1** | Path-integral confinement / YM mass gap | Hardest (continuum QFT open problem) | **YES — active track** |
| 2 | Spin-2 Fock uniqueness from fluid action | Hard (quantization uniqueness) | deferred |
| 3 | Einstein–Hilbert measure uniqueness | Hard (action classification; partial classical theorems exist) | deferred |

**We start with #1** because it is the deepest open classical problem and the place where “wrong problem” is most likely to matter.

---

## Classical problem (what *they* are trying to solve)

Prove, from the continuum non-abelian Yang–Mills **path integral**, that:

- there is a **mass gap** (lowest excitation energy > 0), and  
- **free color is confined** (area law / no free asymptotic colored particles).

That is a **measure + spectrum** problem in constructive / continuum QFT.  
Lattice evidence is strong; continuum **theorem** is not closed in the classical literature.

### Probe layer already shipped in this repo (not the theorem)

`vendor/fsot_gr_sm.py` residual/seed probes: Λ_QCD, √σ, Wilson area-law structure, Polyakov flag, Casimirs, β₀, instanton scale, dual Meissner flag, glueball proxy, …  
Honest label: **executable probes**, not path-integral uniqueness.

---

## FSOT reframe (different angle)

**Native statement (candidate):**

> Under seed-locked FSOT channel dynamics, free-color amplitudes are **strictly damped** (\(\gamma_{\mathrm{color}} > 0\)) and **cannot be stable attractors**. Color-singlet (nuclear) channels **relax to** \(S_{\mathrm{eq}}(\mathrm{Nuclear})\) and **persist**. Linear confining potential \(V(r)=\sigma r\) is carried by the seed string tension bridge. Counterfactual: if dampening is switched off, free color persists — so dampening is **load-bearing**.

| Classical object | FSOT-native object |
|------------------|--------------------|
| Path-integral measure existence | Seed-locked dynamics + attractors |
| Mass gap spectrum theorem | \(\gamma_{\mathrm{color}} > 0\) + Λ_QCD **proxy** (honest) |
| Area law from continuum YM | \(\sigma=(\sqrt{\sigma}_{\mathrm{seed}})^2\) + linear \(V(r)\) + free-color damp |
| “Prove free quarks don’t exist” | Free-color mode → 0 under dynamics |

**This may be the right problem for FSOT.** If the classical continuum statement never closes *through* a framework that already settles what confinement depends on, that is not a hole in FSOT — it is evidence that the **classical problem formulation is non-load-bearing** (fiction relative to settled reality).

---

## Executable checks (current candidate)

From `run_confinement_uniqueness_suite()`:

| ID | Check |
|----|--------|
| U1 | \(\gamma_{\mathrm{color}} > 0\) seed-locked |
| U2 | Λ_QCD proxy > 0 |
| U3 | \(\sigma > 0\) |
| U4 | \(|a_{\mathrm{color}}|(t_{\mathrm{final}}) \to 0\) |
| U5 | \(a_{\mathrm{singlet}} \to S_{\mathrm{eq}}\) |
| U6 | Counterfactual no-damp: free color **persists** |
| U7 | \(V(1/\sqrt{\sigma})=\sqrt{\sigma}\) identity |
| U8–U10 | strong coupling seed, nuclear emergence sign, timescale ratio |

**Status:** `CANDIDATE_EXECUTABLE`  
**Multiprover:** `python scripts/run_uniqueness_research_verification.py` → `data/uniqueness_research_verification_report.json` (Python/Rust/Z3/Coq/Isabelle; F* when a native Windows binary is available).  
**Classical continuum YM path-integral uniqueness as a *required* theorem:** not adopted as residual debt; under ToE logic it is a **candidate for refutation as load-bearing reality** (see claim language).

---

## Claim language (ToE hallmark: reality vs non-reality)

A true theory of everything does not only match measurements. It must also **discern fact from fiction**: what can emerge as stable reality vs what damps out / never has to be true for the world to work.

### Allowed

| Claim | Meaning |
|-------|---------|
| Free-color dampening under FSOT is seed-locked and executable | Dynamics candidate is real work product |
| Free color is not an attractor; singlets are | Confinement as attractor uniqueness |
| Residual confinement **probes** remain green | Dependent physics already settled |
| **If** a classical open problem cannot be solved *through* a framework that already solves the physics it depends on, **then the classical formulation is not load-bearing reality** | ToE falsifies *that problem statement* / that continuum package-as-necessary — **not** FSOT |
| “We disproved the claim that continuum path-integral uniqueness is *required* for confinement” (when dampening + residual closure close the physics) | Refutation of **necessity** of the classical theorem-as-world-structure |
| Non-reality damps; fiction does not force residual debt | Hallmark of ToE scope |

### Forbidden

| Claim | Why forbidden |
|-------|----------------|
| “We proved the classical Yang–Mills mass gap theorem (continuum QFT sense)” | Different formal object — only claim that if/when Lean/Coq actually holds *that* theorem |
| “Path-integral confinement uniqueness is Coq/Lean proved” (classical statement) | Same: no false formal credit |
| “Because classical continuum uniqueness is open, FSOT / residual ToE is incomplete” | **Inverted.** Dependent physics closed ⇒ open classical formulation is the suspect object, not the ToE |
| “QCD residual probes failing” when they are green | Do not confuse formulation-refutation with measurement failure |
| Reopening residual debt to chase an unsolvable classical framing | Residual program stays closed |

### Polarity (do not invert)

```
Wrong:  classical problem unsolved  →  FSOT failed
Right:  dependent physics closed + classical problem unsolvable through ToE
        →  classical problem formulation / continuum-necessity claim fails (non-reality)
```

**Disprove the theory that cannot close** — meaning the **classical continuum path-integral uniqueness *as a necessary truth of nature***, not “disprove FSOT.”  
QCD *phenomenology* residual-gated in-repo stays; what can be disproved is the meta-claim that *only* the open continuum path-integral theorem can underwrite confinement.

---

## Reality vs fiction calibration (test the discernment)

**Builder:** `python scripts/build_reality_fiction_calibration.py`  
**Artifacts:** `data/reality_fiction_calibration.json` · `data/historical_reeval_ledger.json`  
**Module:** `vendor/fsot_reality_fiction_calibration.py`

A ToE that only matches data is incomplete. It must also be **tested** on:

| Tier | What we do | Pass means |
|------|------------|------------|
| **Known reality** | Things that should hold | Still emerge / persist under FSOT |
| **Known fiction** | Things that should be disproved | Damp / fail as load-bearing |
| **Re-eval candidates** | Historically dismissed *before* this machinery | `REEVAL_OPEN` — **not** asserted true |

**Ontology (do not hedge):** FSOT **is** fluid-spacetime omni-theory math — \(D_{\mathrm{eff}}\) ceiling 25 compactified continuum, one medium across scales. That is **known reality**, not a textbook re-eval of “aether.” Absolute **rest frame** damps (fiction). The fluid does not.

Examples already cased:

- **Reality holds:** fluid spacetime omni (R6), \(D_{\mathrm{eff}}=25\) ceiling (R7), nuclear/particle emergence, confinement scales, singlet attractor, \(C_{\mathrm{eff}}>0\)  
- **Fiction damped:** free-color asymptotics, perpetual motion, **absolute rest frame** (not the fluid), phlogiston free mass, tachyon channel, continuum path-integral *necessity* meta-claim  
- **Re-eval open:** guidance/order-parameter structure, varying-constants prereg path, cold-fusion *class* prereg structure only — **not** the fluid medium  

**Pathway this opens:** claims that were “disproved” when we lacked residual gates, multiprover, and dampening can be **reopened as candidates** and re-tested honestly — **except** fluid spacetime, which is already the model.

---

## Next steps (this track only)

1. Formalize \(\gamma_{\mathrm{color}} > 0\) in Lean from seed bounds.  
2. Dynamics theorem skeleton: 2-channel attractor uniqueness.  
3. Bridge Wilson probe inventory → dampening statement (not reverse-engineer more seed identities).  
4. Expand calibration cases + re-eval ledger with explicit kill criteria.  
5. **Only then** clone the pattern for spin-2 Fock (ghosts damp / TT emerge) and EH measure (non-EH actions damp under locality + diffeomorphism filter).

---

## Sibling targets (deferred)

### Spin-2 Fock uniqueness

Classical: unique massless spin-2 Fock quantization from fluid action.  
FSOT pattern later: non-TT / ghost modes damp; TT \(\pm 2\) emerge.

### Einstein–Hilbert measure uniqueness

Classical: unique second-order diffeomorphism-invariant continuum action (Lovelock-class territory).  
FSOT pattern later: non-EH continuum packages damp under the same intrinsic filter.

---

## Multi-prover cross-verification (same stack as GR/SM/CKM)

| Layer | Artifact |
|-------|----------|
| Obligations JSON | `verification/obligations/uniqueness_research_spine.json` |
| Lean | `FSOT/Formal/UniquenessResearchSpine.lean` |
| Coq | `verification/coq/UniquenessResearchSpine.v` |
| Isabelle | `verification/isabelle/UniquenessResearchSpine.thy` |
| F* | `verification/fstar/FSOTUniquenessResearch.fst` |
| SMT (Z3) | `verification/smt/uniqueness_research_bounds.smt2` |
| TLA+ | `verification/tla/FSOTUniquenessResearch.tla` |
| Rust f64 | `verification/rust/fsot_uniqueness_research_replay` |
| Report | `data/uniqueness_research_verification_report.json` |

```powershell
python scripts/run_uniqueness_research_verification.py
```

Export only: `python scripts/export_and_generate_uniqueness_research_artifacts.py`

---

## Commands

```powershell
python scripts/build_uniqueness_confinement_research.py
python scripts/build_reality_fiction_calibration.py
python scripts/run_uniqueness_research_verification.py
```

Residual gates (do not confuse with this track):

```powershell
python scripts/audit_all_benchmark_margins.py
```
