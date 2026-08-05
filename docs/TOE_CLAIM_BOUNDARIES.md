# TOE claim boundaries — frozen criteria (do not renegotiate mid-work)

**Locked:** 2026-08-03  
**Repo:** FSOT-2.1-Lean  
**Purpose:** Stop the moving bar. Two labels, two checklists. Domain count and prover count strengthen **Label A**, they do **not** redefine **Label B**.

---

## Label A — claimable **now** (empirical multi-domain framework)

> A single seed-derived constant spine with **preregistered** domain routes reproduces a multi-domain measurement atlas at **sub-0.5% pooled median residual**, under multi-prover residual triangulation and registered falsification criteria.

**Fixed pass checklist (Label A):**

| ID | Criterion | Evidence |
|----|-----------|----------|
| A1 | Seed-locked engine (π,e,φ,γ,G) | `vendor/fsot_compute.py` pin D1D38A |
| A2 | Preregistered routes, not per-row LS fits | `parameter_honesty_closure.json` |
| A3 | Multi-domain residual gate ≤ 0.5% | `benchmark_margin_audit.json` (live N/N in `docs/CURRENT_STATUS.md`) |
| A4 | Multi-prover residual triangulation | `cross_proof_verification_report.json` overall_ok |
| A5 | Falsification registry | `falsification_registry_closure.json` |
| A6 | Public reproduce path | `docs/SKEPTIC_REPLICATION_KIT.md` |

If A1–A6 hold → **Label A is satisfied.** Adding domains/provers can only strengthen A.

---

## Label B — “Theory of Everything” (classical technical meaning)

A candidate is Label B **only if** all of the following are **true with named artifacts**.  
This list is **frozen**. Peer acknowledgment is **not** on this list.

| ID | Criterion | What “done” looks like | Artifact path |
|----|-----------|------------------------|---------------|
| **T1** | One ontology written as axioms | Finite axiom list + maps to engine | `data/foundational_ontology_axioms.yaml` + this doc |
| **T2** | Dynamics (evolution laws) | Continuum / fluid / scalar field equations + numerical checks | `vendor/fsot_dynamics.py`, `data/toe_dynamics_benchmark.json` |
| **T3** | Limit recovery | Explicit GR / QM / SM (or replacement) limit checks | `data/toe_limit_recovery_benchmark.json` + `vendor/fsot_gr_sm.py` (deep GR map) |
| **T4** | Force/matter package **or** explicit scope change | Interaction package (gauge/masses/charges) **or** written scope retirement | `vendor/fsot_gr_sm.py` + `data/toe_force_package_manifest.json` (v1); see `docs/T3_T4_GR_SM_DEEPENING.md` |
| **T5** | Pre-data risky predictions | Frozen slate + SHA-256 **before** decisive surveys | `data/toe_prereg_freeze.json` |
| **T6** | Falsifiability | Kill criteria for global + contested sectors | `data/falsification_registry_closure.json` |

**Label B status is computed by** `python scripts/build_toe_gap_closure.py` → `data/toe_gap_closure_report.json`.

---

## What does **not** count as completing Label B

- More extension domains alone  
- More provers alone  
- Smaller residual alone  
- “Another human agreed” alone  

Those strengthen **Label A** or social process, not T1–T6.

---

## Social / process (separate bar — never mixed into T1–T6)

| Process item | Role |
|--------------|------|
| arXiv / peer review | Acceptance path |
| Independent clean-clone | Trust path |
| Specialist domain papers | Communication path |

Process can lag technical Label A forever; that does not erase A1–A6.

---

## Required public language

**When A1–A6 hold:** Label A statement; multi-domain seed-locked framework.  
**When T1–T6 all green (as of gap report):** Explicit **Theory of Everything candidate under frozen Label B checklist** — **allowed and not hidden**.  
**Still not allowed:** “Proved beyond peer review,” “full Einstein–Hilbert / full SM Lagrangian derived,” or “all 13 contested problems finished” unless those specific deeper claims have their own green artifacts.

**Process language (always honest):** peer review and independent clean-clone remain open; they are **not** T1–T6.

Machine Key: `docs/FSOT_MATH_KEY.md`  
Gap closure runbook: `docs/TOE_GAP_CLOSURE.md`
