# Frozen knobs — honest, not “zero integers”

**Pin:** D1D38A · **Freeze date:** 2026-09-09 · **Never moved after lock without a new pin**

“Zero free parameters” here means: **no post-hoc dial when a row misses**. It does **not** mean the domain table was derived from \(\pi,e,\varphi,\gamma,G\) by a published \(\mathcal{F}\).

## Assigned folds (admitted)

The public `DomainConfig` table assigns \(D_{\mathrm{eff}}\), \(\delta\psi\), hits, and `observed` per domain. **35 assigned folds**, frozen on **2026-09-09**, never moved after lock.

There is **no** identity

\[
D_{\mathrm{eff}}(\mathrm{domain})=\mathcal{F}(\pi,e,\varphi,\gamma,G,\mathrm{name})
\]

in this edition. If that \(\mathcal{F}\) is written later, it is a **new pin**.

Hash: `data/domain_table_freeze.json` (`domain_table_sha256`).  
`python scripts/audit_parameter_count.py` **fails** if the table or the `K` line changes while the pin is still D1D38A.

## \(K\) contains 0.99

```text
K = PHI * (GAMMA / E) * sqrt(2) / ln(PI) * 0.99
```

`0.99` is a **frozen seed factor**, not a derived identity in this edition. Deleting it would republish every Ledger A number under a new pin. We do **not** retune it to chase a residual.

## `observed`

Frozen as an **experiment-class** tag on the domain row (spectroscopy-like domains observed; dark folds such as Fluid/Biology/QC stay `observed=False`). Not a per-catalog-row switch.

## \(f_{\mathrm{domain}}\)

Ledger B modulation factors live in `scripts/fsot_api_predict_lib.py` (`DOMAIN_FACTORS`). Changing a factor is a **new edition**, not a silent densify.

## What a miss may not do

After lock \(T_0\): a miss goes to [`../results/MISSES.md`](../results/MISSES.md). A domain-integer change is a new pin plus a diff of every old Ledger A number. Fold edits are not residual repair ([`FSOT_PROPER_DENSIFY_POLICY.md`](FSOT_PROPER_DENSIFY_POLICY.md)).
