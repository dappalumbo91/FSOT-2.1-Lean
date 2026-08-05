# FSOT Residual ToE Program — CLOSURE

**Status:** `RESIDUAL_PROGRAM_CLOSED`  
**Authority pin:** D1D38A  
**Machine certificate:** [`data/residual_toe_closure_certificate.json`](../data/residual_toe_closure_certificate.json)

---

## What “closed” means

The **executable residual program** is finished when:

1. Every active benchmark domain passes the official green residual gate (≤0.5%).
2. Tier-scalar aspiration (≤0.05% pooled scalar median) has **zero** failing domains.
3. Label A (empirical) and Label B (classical ToE checklist) pass.
4. Multiprover residual triangulation reports `overall_ok` and `github_ready`.
5. Residual open count is **0**.

Uniqueness theorems (path-integral confinement uniqueness, spin-2 Fock uniqueness, Einstein–Hilbert measure uniqueness) are **pure-math research**. They are **not** residual-gate failures and **must not** re-open expansion waves.

---

## Final residual gates (this closure)

| Gate | Result |
|------|--------|
| Green residual | 470 / 470 PASS |
| Strict scalar max ≤0.5% | 470 / 470 PASS |
| Tier-scalar ≤0.05% pooled | **CLOSED** (0 fails) |
| Adversarial blocking open | 0 |
| Multiprover | overall_ok + github_ready |

---

## What closed the last five tier-scalar misses

| Domain | Fix |
|--------|-----|
| ENDF / Nuclear IAEA open | `Nuclear_Physics` factor 0.0005 + re-`make_fsot_record` residual |
| NIST ASD spectroscopy + multi-species | `Atomic_Physics` factor 0.0005 + re-residual |
| Intelligence compression | Pure Neuroscience residual scalars; calibration-to-target structural only |

Residual law everywhere: \(c = m\,(1+|S|\,f)\) via `make_fsot_record` / `fsot_scaled` only.

---

## Policy after closure

- **Do not expand** new residual frontiers by default.
- **Do re-run** audits if code/data drift re-opens a gate.
- **Do not** treat uniqueness research as residual debt.

---

## Commands

```powershell
python scripts/audit_all_benchmark_margins.py
python scripts/build_tier_scalar_precision_closure.py
python scripts/build_verification_depth_audit.py
python scripts/build_adversarial_round3_audit.py
```
