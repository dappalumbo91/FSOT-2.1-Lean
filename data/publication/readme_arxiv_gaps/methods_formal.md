### 5.5 Statistical error definitions

For each domain or panel benchmark, let \(n\) measured records produce pairs \((m_i, c_i)\) where \(m_i\) is the authoritative measured value and \(c_i\) is the seed-derived FSOT prediction at canonical parameters (no per-record fitting).

**Per-record error (percent):**

\[
\varepsilon_i = 100 \times \frac{|c_i - m_i|}{\max(|m_i|, \epsilon_{\mathrm{floor}})}
\]

where \(\epsilon_{\mathrm{floor}}\) guards division near zero for classifier-valued observables.

**Pooled median error (domain gate metric):**

\[
\tilde{\varepsilon} = \mathrm{median}(\varepsilon_1, \ldots, \varepsilon_n)
\]

**GREEN gate (benchmark margin):** \(\tilde{\varepsilon} \leq 0.5\%\) and stability classifier agreement \(\geq 99.5\%\) where applicable (`data/benchmark_margin_audit.json`).

**Cross-domain headline:** median of per-domain \(\tilde{\varepsilon}\) over the 403-domain atlas (not a global re-fit across all 536,740 rows).

### 5.6 Preregistration and kill criteria

- **Preregistered predictions:** `data/preregistered_predictions_manifest.yaml` (PRED-001–041) — outcomes declared before panel refresh.
- **Per-domain kill criteria:** `data/fsot_domain_navigator.json` — extension panels and core routes register failure thresholds.
- **Parameter honesty:** `data/honest_claims_manifest.yaml` — routing coordinates are seed-derived folds, not fitted observational knobs (audit: `scripts/audit_parameter_count.py` → `ZERO_FREE`).

### 5.7 Data availability and reproduction

All headline claims in §VI–VIII reproduce from:

```bash
python scripts/run_publication_verification_bundle.py
```

Machine-readable claim ledger: `data/publication_claims_manifest.json`. Domain atlas: `data/publication/domain_atlas.csv`. Portable clone policy: bundled `vendor/` caches; live rebuild paths documented in Appendix XI-B.
