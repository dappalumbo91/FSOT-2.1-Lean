# Three ledgers — never mixed in a headline

**Pin:** D1D38A · **Peer review:** out of scope  
A hostile reader treats one green paragraph as a first-principles hit. These ledgers cannot share a headline.

| Ledger | What is allowed in the formula | Pass metric | Forbidden |
|--------|--------------------------------|-------------|-----------|
| **A. Closed-form** | seeds + derived constants + frozen \(D_{\mathrm{eff}}\) only | \(\hat{m}\) vs held-out \(m\) in physical units | \(m\) inside the formula |
| **B. Catalog residual** | \(c=m(1+\|S\|f)\) allowed, labeled **correction**, not discovery | beat nulls \(c=\bar{m}\) and random-domain fold | quoting B as ToE accuracy |
| **C. Live integrity** | API/catalog identity checks | stream + holdout hash/value match | promoting C into A or B |

**Verbs:** Ledger A **predicts**. Ledger B **corrects**. Ledger C **checks**.

- 477/477 is Ledger **B** (catalog residual files).
- \(T_{\mathrm{CMB}}\), H₀, first Riemann zero are Ledger **A** only when emitted with no measured input.
- Multiprover / pin match is Ledger **C**.

Do not write “477/477” next to \(T_{\mathrm{CMB}}\) or H₀.

Predict vs correct: `python scripts/predict_closed_form.py --observable T_CMB` then `python scripts/compare_to_anchor.py --observable T_CMB`.

Knobs: [`FROZEN_KNOBS.md`](FROZEN_KNOBS.md). Misses: [`../results/MISSES.md`](../results/MISSES.md). What we do not claim: [`WHAT_WE_DO_NOT_CLAIM.md`](WHAT_WE_DO_NOT_CLAIM.md).
