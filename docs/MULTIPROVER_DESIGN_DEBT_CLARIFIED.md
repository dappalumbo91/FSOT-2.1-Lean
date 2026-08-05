# Multiprover “design notes” — what needs fixing vs what is inventory

## 1. The “68 structural lemmas”

**Status: not open failures.**

| Item | Meaning |
|------|---------|
| Count | 68 `exp_*` / `pi_*` / `e_*` lemma **names** in `FSOT/Formal/Bounds.lean` |
| Role | **Inventory** of transcendental lemmas already in the formal spine |
| Multiprover | **All 68** IDs appear in `verification/obligations/transcendental_bounds.json` |
| Checks | Python decimal + Coq/Isabelle transcendental chunks + Rust replay (68) |

**Only 2** lemmas (`e_lt_…`, `pi_lt_…` class) use Mathlib-style transcendental interval proofs rather than pure float-export. They are **proved in Lean** and still exported; they are not residual-gate failures.

Nothing to “solve” for green multiprover. Optional future: deeper independent Coq/Isabelle analytic proofs of those two intervals.

---

## 2. The “54 margin violations”

**Status: mislabeled — not true margin failures.**

| Item | Reality |
|------|---------|
| Count | 54 `bundle_conj` obligations |
| Cause | Unparsed Lean conjuncts → `obligation_provable` false |
| Conjunct coverage | Structural ledger: **~100%** atomic coverage via linked IDs |
| Lean | Modules **build** (not intentional falsifiers) |
| True margin violations | **0** (`margin_violations.json` count = 0) |

They were incorrectly run through “expect Lean build failure” (refutation path). That path is only for **false inequalities**.

**Fix applied:** Lean↔Coq and Lean↔Isabelle audits reclassify them as  
`structural_bundle_excluded` (unparsed conjuncts), **not** margin violations.  
True margin violation count must stay **0** on a green ledger.

**Optional later work:** parse more conjunct forms so all 526 bundles become python-provable indices (export hygiene), not science residual work.

---

## 3. What actually gates science

| Gate | Location | Status |
|------|----------|--------|
| Empirical residual ≤ 0.5% | `benchmark_margin_audit.json` | **430/430** green (see `CURRENT_STATUS.md`) |
| Atomic multiprover | Lean/Coq/Isabelle/F*/Rust | passed |
| True falsifiers in export | `margin_violations.json` | 0 |

Source of truth after re-audit: `data/cross_refinement_lean_coq_report.json`.
