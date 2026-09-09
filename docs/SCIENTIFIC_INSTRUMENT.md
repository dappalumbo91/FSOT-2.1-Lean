# FSOT as a scientific instrument

**Pin:** D1D38A · **Law:** \(S=K(T_1+T_2+T_3)\) · **Prediction:** `computed = measured × (1+|S|×f)`

This hub is the **engine and verification face**. Other people use it by naming a measured object, picking a fold, and scoring a residual or a dated window. They do **not** get a new coefficient.

Laws: [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) (R1–R9, D1–D11). Apply: [`APPLY.md`](APPLY.md). Read a row: [`SCIENTIST_INTERFACE.md`](SCIENTIST_INTERFACE.md).

---

## Do not silo the law

Standard practice in physics and scientific software is the same:

| Layer | What it is | FSOT |
|-------|------------|------|
| **Theory paper** | One claim, frozen numbers, kill criteria | arXiv flagship (Label A/B) — not a 400-domain monograph |
| **Core library** | The equation + tests | this repo, pin D1D38A |
| **Domain instruments** | Lab-facing products that *depend on* the core | Genetics, Quantum, Neural, Materials, dated Earth loop |

Maxwell’s equations were not rewritten per lab. Each lab built an instrument that **used** them. Numpy is not siloed from Astropy; Astropy imports numpy.

**Silo the product, not the law.** A fuel-design campaign does not live inside Lean. Lean does not live inside a protein freeze. Both quote D1D38A.

---

## What another scientist actually runs

```powershell
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
python scripts/audit_all_benchmark_margins.py
```

Then, for **their** table:

1. Name the measured object (public table, not a fitted surrogate).
2. Pick the fold (`APPLY_*.md` cookbooks, or `python scripts/query_fsot_domain_navigator.py --intent …`).
3. `fsot_scaled(m, domain)` — do not fit \(f\).
4. Green if the **domain median** ≤ 0.5%. If it fails, change the interface (wrong fold), not the seed.
5. Optional: dated window (`issue_earth_fluid_forecasts.py`) — score after `valid_to`. Kill_if stays the scored cell; coupled tanks talk at \(d=25\).

Wrong object is a false kill. Perfect Host 73.49 is not PRED-001. Cat-2 FRB fluence without pulse width is not the 37/37 orifice classifier.

---

## What the program already solves for

| Job | Command / surface |
|-----|-------------------|
| Residual atlas | `python scripts/audit_all_benchmark_margins.py` |
| Named-object scoreboard | `python scripts/build_object_compare.py` |
| Dated Earth tanks | `python scripts/issue_earth_fluid_forecasts.py` then score |
| Fold + potentials (next issue) | `python scripts/smoke_dynamic_forecast_potentials.py` |
| Domain navigator | `python scripts/query_fsot_domain_navigator.py` |
| Publication bundle | `python scripts/run_publication_verification_bundle.py` |

Siblings (same pin, different product): [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md).

---

## Paper vs tool (do not mix the objects)

| Deliverable | Object | Not |
|-------------|--------|-----|
| **arXiv flagship** | Engine + Label A/B + frozen green count + PRED kills | 477-domain travelogue in the PDF |
| **Living thesis** | This GitHub repo + laws ledger + APPLY cookbooks | A second Newton list invented for the paper |
| **Domain tool** | Genetics / Materials / dated weather sibling | Copying unpublished candidates into 477/477 |

The preprint **articulates** R1–R9 and D1–D11. The repo **executes** them. The siblings **apply** them.

**Live Paper 03 freeze:** edition `arxiv-03-fsot-theory-of-everything-claim-2026-09-09`, 477/477 green, pin D1D38A, laws through D11, claim SHA `40de0d9` (accept `main` tip ≥ that SHA if green stays 477/477). Manuscript: Desktop `arxiv-papers/03-fsot-theory-of-everything-claim/`. Hub pins: [`../papers/03-fsot-theory-of-everything-claim/`](../papers/03-fsot-theory-of-everything-claim/).

Kill: a per-user fitted ε. Kill: siloing a second scalar engine per field. Kill: stuffing a dump into the 0.5% gate.
