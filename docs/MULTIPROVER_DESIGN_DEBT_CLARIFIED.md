# Multiprover “design notes” — what needs fixing vs what is inventory

## 1. The “68 structural lemmas”

**Status: not open failures.**

| Item | Meaning |
|------|---------|
| Count | 68 `exp_*` / `pi_*` / `e_*` lemma **names** in `FSOT/Formal/Bounds.lean` |
| Role | **Inventory** of transcendental lemmas already in the formal spine |
| Multiprover | **All 68** IDs appear in `verification/obligations/transcendental_bounds.json` |
| Checks | Python decimal + Coq/Isabelle transcendental chunks + Rust replay (68) |

**Only 2** lemmas (`pi_gt_314159265358979323846`, `pi_lt_314159265358979323847`) use Mathlib-style tight digit intervals rather than coarse float-export. They are **proved in Lean** (via `pi_gt_d20` / `pi_lt_d20`) and still exported; they are not residual-gate failures.

**Python oracle solidification (2026-08-05):** float64 cannot distinguish those digit strings from `math.pi` (IEEE π sits *between* the two certified bounds in a way that broke naive `Decimal(str(math.pi))` comparisons). `scripts/transcendental_bounds_lib.py` now evaluates with **≥50-digit `Decimal` `PI_REF` / `E_REF`**, so all **68/68** inventory rows report `python_decimal_verified: true` in `verification/obligations/transcendental_bounds.json`.

**Coq native depth (2026-08-05):** `verification/coq/TranscendentalBoundsNative.v` proves the four base intervals with the Rocq Platform **Interval** tactic (`interval with (i_prec …)`). `TranscendentalBoundsCert.v` **Require Export**s Native and proves the remaining pointwise exp/π certificates as **Lemmas** (Interval) — **0 Axioms** on the transcendental cert path. Chunks `TranscendentalBounds_00..02.v` compile against that stack. Isabelle already used `approximation` natively.

Nothing open for green multiprover on the π/e ladder. Remaining optional: F\* oracle-literal reduction; deeper Machin-series *hand* proofs without Interval (not required).

**Not a formal path:** Lissajous figures (two orthogonal sines; frequency ratios ≈ rational approximations involving π harmonics) are good *intuition* for circular/periodicity geometry. They do **not** replace Mathlib digit bounds, Interval, or the Decimal multiprover oracle.

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
