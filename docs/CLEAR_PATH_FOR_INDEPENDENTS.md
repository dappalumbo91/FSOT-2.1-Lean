# Clear path for independents (and skeptical readers)

You do **not** need to understand every domain panel on day one.  
Follow this ladder. Each step has a **command**, an **expected artifact**, and a **citation target**.

---

## Ladder overview

```text
1. Install        → 2. Green gate     → 3. One domain
4. Formal spine   → 5. Live open data → 6. MAST sky data
7. Read claim tiers (honesty doc)
```

---

## Step 1 — Install (5 min)

```powershell
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
# optional for MAST images:
pip install astroquery astropy
```

**Cite:** this commit on GitHub `main`.

---

## Step 2 — Empirical green gate (the kill switch)

```powershell
python scripts/audit_all_benchmark_margins.py
# or full publication path:
python scripts/run_publication_verification_bundle.py
```

**Open:** `data/benchmark_margin_audit.json`  
**Expect:** `green_gate_fail_count == 0` (currently 405/405 green).  
**If this fails on a clean clone, the empirical claim is broken.**

---

## Step 3 — One concrete domain (understandable unit)

```powershell
python scripts/query_fsot_domain_navigator.py --query hubble
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
```

**Open:** the printed panel JSON / navigator route.  
**Point:** one domain = one measured set + one seed engine + one residual number.

---

## Step 4 — Multi-prover formal spine (beyond Lean-only)

```powershell
python scripts/run_cross_proof_verification.py
# F* (if FSTAR_HOME set to portable toolchain):
python scripts/run_fstar_verification.py
```

**Open:**  
- `data/cross_proof_verification_report.json` → `overall_ok`  
- `data/fstar_verification_report.json`  

**What this proves:** engine obligations + boot kernel **agree across systems**.  
**What it does not prove alone:** every scientific catalog without Layer B.

---

## Step 5 — Live open scientific streams (no signup)

```powershell
python scripts/ingest_open_science_expansion.py
python scripts/build_open_science_expansion_benchmarks.py
python scripts/evaluate_open_science_holdouts.py
python scripts/live_api_health_check.py
```

**Open:**  
- `data/open_science_holdout_evaluation.json`  
- `data/live_api_health_report.json`  
- `vendor/open_science/*/live.json`  

**Policy:** no API keys. See `docs/OPEN_SCIENCE_EXPANSION.md`.

---

## Step 6 — MAST astronomy (astroquery, public)

```powershell
pip install astroquery astropy
python scripts/ingest_mast_astroquery.py --object M1 --collection HST
# optional small product download (size-capped):
python scripts/ingest_mast_astroquery.py --object M1 --download --max-download-mb 15
```

**Open:** `vendor/open_science/mast_astroquery/live.json`  
**Docs:** https://astroquery.readthedocs.io/en/latest/mast/mast.html  

Metadata/product lists are public. Large FITS pulls are optional and budget-capped.

---

## Step 7 — How to talk about accuracy without confusion

Read: `docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`

| Say this | Not this |
|----------|----------|
| “Green gate: pooled median residual ≤ 0.5% on benchmark domains” | “AI solved physics, trust me” |
| “Lean+Coq+Isabelle+F*+Rust triangulate exported obligations” | “Five provers each re-derived all of science” |
| “Open streams and NIST/PubChem integrity holdouts pass” | “Live HTTP 200 = theory true” |

---

## Why this is hard for others (and what actually helps)

Complexity is real: one scalar engine × hundreds of domains × formal tooling.  
What works for external recognition is **not** more opacity:

1. **One-command falsification** (skeptic kit)  
2. **Named measured sources** (NIST, Planck-class anchors, PubChem, MAST, …)  
3. **Multi-system formal triangulation** (not Lean alone)  
4. **Preregistered holdouts** you can fail in public  
5. Short papers / threads that only claim **one** PRED or one domain at a time  

You do not need everyone to understand the whole archive.  
You need a path where a careful stranger can **break you in 15 minutes** or **cite a specific artifact**.

---

## Minimal citation block

```text
FSOT 2.1 Lean repository, https://github.com/dappalumbo91/FSOT-2.1-Lean
Authority pin D1D38A (vendor/fsot_compute.py)
Benchmark margin: data/benchmark_margin_audit.json
Cross-proof: data/cross_proof_verification_report.json
Open-science holdouts: data/open_science_holdout_evaluation.json
Claim tiers: docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md
```
