# Formal pipeline roles — Lean master · SMT bulk · TLA+ flow

**Edition:** 2026-08-03  
**Repo:** `FSOT-2.1-Lean`  
**Principle:** With ~402 domains and 500k+ empirical records, the ceiling is open-source formal methods **used correctly**, not a longer tool list.

---

## 1. Core tool group (do not expand casually)

| Tool | Role |
|------|------|
| **Lean 4** | Master integrator — definitions, large structures, domain certificates |
| **Coq / Rocq** | Independent re-proof of exported obligations + catalog residual lemmas |
| **Isabelle/HOL** | Independent re-proof + scalar math mirror (`FSOTScalarMath`) |
| **F\*** | Boot / kernel scalar parity path |
| **Z3 / CVC5** | SMT bulk numerical bounds on continuous residuals / margins |
| **TLA+** | Model-check domain-routing / preregistered-fold **execution flow** |
| **Rust** | Executable obligation replay |

Adding frameworks outside this set is presumed **redundant overhead** unless a new *class* of property appears (not already covered by math / bounds / flow).

---

## 2. How the pieces fit (translation layer)

```text
Seeds + pin D1D38A (Python oracle)
        │
        ▼
Lean 4  ──────── master Real definitions + domain Priors
        │
        ├─ export obligations ──► Coq / Isabelle / F* / Rust   (interactive + replay triangulation)
        │
        ├─ scientific_catalog_spine.json ──► ScientificCatalogSpine_*.v/.thy + Lean module
        │         │
        │         └─► SMT-LIB2 bulk (Z3/CVC5 or python_decimal fallback)
        │
        └─ domain routing scripts ──► TLA+ FSOTDomainRouting (TLC or Python explorer)
```

**Bottleneck:** translating one obligation set into many backends without drift — not inventing a sixth interactive prover.

---

## 3. What each layer is *for*

### Lean 4 — master integrator

- Own `FSOT/Formal/Scalar.lean`, bounds, theorems, domain `*Priors`.
- Scale with Mathlib-style project structure.
- Human-readable theorem statements reviewers open first.

### SMT (Z3 / CVC5) — bulk numerical bounds

- Target: residual inequalities, margin gates, continuous domain constraints across the catalog.
- Artifact: `verification/smt/scientific_catalog_bounds.smt2`
- Runner: `python scripts/run_smt_catalog_bounds.py`
- Report: `data/smt_catalog_bounds_report.json`
- If Z3/CVC5 are missing, the same obligations are still checked via Python decimal (honest fallback, not a silent skip).

### TLA+ — system state flow

- Target: preregistered folds / domain-routing scripts — load → fold → residual → green gate → certify.
- Spec: `verification/tla/FSOTDomainRouting.tla`
- Runner: `python scripts/run_tla_domain_routing_check.py`
- Report: `data/tla_domain_routing_report.json`
- Invariants: no stuck states, no certify-without-measure path, Done iff all domains certified.

### Coq / Isabelle / F* / Rust — multi-prover scientific re-proof

- **Not** structure-only caveats.
- Scientific catalog residual gates are first-class: `verification/obligations/scientific_catalog_spine.json` (~1980 obligations).
- Generated lemmas: `verification/coq/ScientificCatalogSpine_*.v`, `verification/isabelle/ScientificCatalogSpine_*.thy`, `FSOT/Formal/ScientificCatalogSpine.lean`.
- Wired into `scripts/run_cross_proof_verification.py`.

---

## 4. Honesty boundaries

| Layer proves | Layer does **not** prove |
|--------------|---------------------------|
| Exported residual gate literals hold | That Hubble/JWST raw pixels were re-derived from axioms alone |
| Routing cannot skip green gate | That a physical ontology is “true” in the metaphysical sense |
| Multi-prover agreement on obligations | That every field theory community has endorsed FSOT |

See also: `docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`, `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`, `docs/FSOT_NARRATIVE_CORE.md` §7.

---

## 5. Commands

```bash
# Catalog obligations + multi-prover artifacts
python scripts/export_scientific_catalog_obligations.py
python scripts/generate_scientific_catalog_artifacts.py

# SMT bulk bounds
python scripts/run_smt_catalog_bounds.py

# TLA+ routing flow
python scripts/run_tla_domain_routing_check.py

# Full cross-proof (includes catalog + SMT + TLA in pipeline)
python scripts/run_cross_proof_verification.py
```

Authoritative rollup: `data/cross_proof_verification_report.json`  
(`scientific_catalog_spine`, `pipeline_roles`, `frameworks.smt_catalog_bounds`, `frameworks.tla_domain_routing`).
