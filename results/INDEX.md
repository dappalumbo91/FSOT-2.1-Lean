# FSOT results index

**Last literature pack:** 2026-08-17  
**Prediction freeze SHA:** `aeb0679eaec722108759589591129fe24f0a77c6` (2026-08-07)  
**Pin:** D1D38A

Predictions live in [`../predictions/`](../predictions/). This page is **outcomes only**.

## Latest verdicts (literature window 2026-08-17)

| PRED | Frozen lock | Latest measured | Verdict |
|------|-------------|-----------------|---------|
| PRED-001 | H0 = 70.75 | CCHP TRGB 70.39 ± 1.22; SH0ES-class ~73; Planck-class 67.4 | **hold** |
| PRED-024 | H0 = 72.1 (local-ladder sector) | SH0ES ~73 / Cepheid-class ~72 | **hold** |
| PRED-002 / 042 | S8 = 0.805 | Euclid DR1 not released | **awaiting** |
| PRED-043 | wₐ = −1.018 | DES+DESI+CMB −0.63^{+0.21}_{−0.18} | **hold** (not 3σ excluded) |
| PRED-004 | Δa_μ = 2.49×10⁻⁹ | Fermilab final confirms high a_μ; WP25 lattice rebase | **partial** |
| PRED-049 | m_H = 125.25 GeV | CMS 2026 γγ 125.14 ± 0.15 | **hold** (0.088%) |
| PRED-017 | Z119 viability | No confirmed atom; JINR run live | **awaiting** |
| PRED-048 | GWTC residual | GWTC-5.0 public | **awaiting** panel refresh |

Full write-up: [`literature/2026-08-17_crossref.md`](literature/2026-08-17_crossref.md)  
Append-only log: [`outcomes/prediction_outcome_log.jsonl`](outcomes/prediction_outcome_log.jsonl)

## Local empirical gate (in-repo panels)

These are **already-measured** domain residuals, not future predictions. Official source: `data/benchmark_margin_audit.json`.

| Item | Value (2026-08-06 snapshot; re-run audit to refresh) |
|------|------------------------------------------------------|
| Green pass | **472 / 472** |
| Fail | **0** |
| Gate | pooled median ≤ 0.5% |
| Median-of-medians | 0.006607% |
| Atlas predictions covering those domains | 1445 |

Re-run: `python scripts/audit_all_benchmark_margins.py`

## Monitor (ran 2026-08-18T01:30Z, `--online`)

| Outcome | Count |
|---------|------:|
| local_green_hold | 8 |
| source_reachable_awaiting_release | 2 |
| open_predata | 3 |
| data_available | 1 |
| local_gate_fail | **0** |

Snapshot: [`monitor/PREDICTION_MONITOR.md`](monitor/PREDICTION_MONITOR.md)

## Next calendar kills

| When | What | PRED |
|------|------|------|
| **12 Nov 2026** | Euclid DR1-Foundation | S8 / catalog locks |
| Sep–Oct 2026 | JINR Z=119 first results | PRED-017 / 012 |
| Oct–Dec 2026 | Rubin EDP2 / early S8 pathfinder | PRED-044 |
| Rolling | DESI / JWST H0 papers | PRED-001 / 024 / 046 |
| Rolling | PDG Higgs combination | PRED-049 |
