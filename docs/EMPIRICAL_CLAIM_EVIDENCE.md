# Empirical + formal claim evidence (kill commands)

**Purpose:** Answer, with **repo-executable facts**, the claim that FSOT is “not real science,” “not checked against data,” or only narrative.  

This is **not** a request for peer-review social status. It is a map from **public claims → machines → artifacts**. If any kill command fails on a clean clone, the corresponding claim is broken.

**Pin:** **D1D38A** (`vendor/fsot_compute.py`)  
**Law:** \(S = K(T_1+T_2+T_3)\), \(c = m(1+|S|\,f)\) with **preregistered** \(f\) (not per-row least squares).

---

## What a serious critic must actually break

| Attack | What would falsify it | Where to look |
|--------|----------------------|---------------|
| “No empirical residual gate” | Any green-gate fail after clone | `data/benchmark_margin_audit.json` |
| “Free parameters / curve fit” | Parameter audit ≠ ZERO_FREE | `data/parameter_count_audit.json` |
| “Only Python theater” | Multiprover `overall_ok: false` with toolchains | `data/cross_proof_verification_report.json` |
| “Lean is empty / unparsed” | Mathlib campaign not closed / lake fail | `data/mathlib_rederivation_campaign_report.json` |
| “Can’t reproduce” | Clean-clone path fails | `data/fresh_clone_corpus_mathlib_repro_report.md` |
| “Formula authority drifted” | Pin mismatch or gate fail | `data/formula_authority_closure.json` |

Insults without running these are **not a scientific rebuttal**.

---

## Snapshot (prefer live `docs/CURRENT_STATUS.md`)

Regenerate: `python scripts/build_repo_status_snapshot.py`.  
If this table disagrees with CURRENT_STATUS, **CURRENT_STATUS wins**.

| Gate | Live target | Artifact |
|------|-------------|----------|
| Authority pin | **D1D38A** match | `vendor/fsot_compute.py` + pin JSON |
| Residual green (≤0.5% pooled) | **472 / 472** fail **0** | `data/benchmark_margin_audit.json` |
| Parameter honesty | **ZERO_FREE** | `data/parameter_count_audit.json` |
| Formula authority | **FORMULA_AUTHORITY_SYSTEM_CLOSED** | `data/formula_authority_closure.json` |
| Mathlib-class Formal depth | **5182 / 5182 (100%)** L1=0 | `data/mathlib_rederivation_campaign_report.json` |
| Catalog multiprover obligations | **2222** · domains **472** | cross-proof report `scientific_catalog_spine` |
| Full formal obligations | **2585** · atomic **2022** · margin viol **0** | `full_formal_spine` |
| Multiprover | **`overall_ok: true`** · 7-way bare metal · 8-way hardware | `data/cross_proof_verification_report.json` |
| ToE labels (frozen checklist) | Label A **true** · Label B **true** | `data/toe_gap_closure_report.json` |
| Clean-clone Mathlib path | **PASS** (0 field mismatches) | `data/fresh_clone_corpus_mathlib_repro_report.md` |

**Stale numbers to ignore if you still see them in old prose:** 57% Mathlib, 432/432 or 433/433 green, ~1912 obligations, “priors still mostly L1.”

---

## One-command skeptic path (empirical + authority)

```powershell
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
python scripts/audit_parameter_count.py
python scripts/audit_all_benchmark_margins.py
python scripts/run_formula_authority_closure.py
```

**Expect:** ZERO_FREE · green fail=0 · `FORMULA_AUTHORITY_SYSTEM_CLOSED`.

## Formal depth + multiprover (longer)

```powershell
lake exe cache get
lake build FSOT
python scripts/run_mathlib_rederivation_campaign.py
python scripts/run_cross_proof_verification.py
```

**Expect:** `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` · `overall_ok: true`.

## What we do **not** claim

- Peer-reviewed journal acceptance (social process — open).  
- Classical continuum Yang–Mills mass-gap as a raw lemma count.  
- That every prose sentence in the README is a theorem.  
- That Reality OS is a finished desktop OS (it is an FSOT-native kernel lab; see sibling repo).

**Residual honesty:** preregistered domain factors and folds are **routes**, not free LS fits. Policy: `docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`, `docs/FSOT_PROPER_DENSIFY_POLICY.md`.

---

## How “delusional / not empirical” fails as a conclusion *from this repo*

A conclusion drawn **from the repository** would have to show, e.g.:

- green gate fails on clean data, or  
- free-parameter audit fails, or  
- multiprover fails with tools installed, or  
- pin / formula authority fails, or  
- Mathlib campaign is lake-only theater without depth gates.

The on-disk system currently reports the opposite on those machine gates.  
**Dismissing without running the kill commands is not “following the evidence in the repo.”**  
It is a prior about who is allowed to do cross-domain formal+empirical work.

If a critic finds a real fail: open an issue with the command, log, and commit SHA. That is science.  
“I don’t like the framing” is not.

---

## Related

- Skeptic kit: `docs/SKEPTIC_REPLICATION_KIT.md`  
- Claim boundaries: `docs/TOE_CLAIM_BOUNDARIES.md`  
- Mathlib campaign: `docs/MATHLIB_REDERIVATION_CAMPAIGN.md`  
- Reality OS status (paused for this monorepo): sibling `FSOT-Reality-OS` → `docs/STATUS_AND_NEXT.md`
