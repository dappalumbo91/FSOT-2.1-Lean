# Count vocabulary (do not mix these)

**Authority:** The 17 September 2026 snapshot is [`CURRENT_STATUS.md`](CURRENT_STATUS.md) and `data/repo_status_snapshot.json`. The 29 September 2026 scoreboard is the README, `data/empirical_accuracy_closure.json`, and `data/cross_proof_verification_report.json`.  
**Regenerate the snapshot:** `python scripts/build_repo_status_snapshot.py`

These are **different ledgers**. Using one number for all of them is the discrepancy.

**A / B / C split (hostile-reader):** [`LEDGERS.md`](LEDGERS.md). 477/477 is Ledger **B**. Closed-form \(T_{\mathrm{CMB}}\) / H₀ is Ledger **A** only via `predict_closed_form.py`. Pin match is Ledger **C**. Never put 477/477 next to \(T_{\mathrm{CMB}}\).

| Name | Recorded value | What it counts | Source |
|------|------------------------:|----------------|--------|
| **Green residual benchmarks** | **477 / 477** | Benchmark **files** that pass ≤0.5% pooled median (live tiers in CURRENT_STATUS) | `data/benchmark_margin_audit.json` |
| **Hand PREDs** | **77** | PRED-001–084 in the prereg manifest | `predictions/preregistered_predictions_manifest.yaml` |
| **Median-of-medians** | **0.005537779313588844%** | Median of the 414 prediction-domain medians | `data/empirical_accuracy_closure.json` (2026-09-29) |
| **Scalar-record envelope** | **183,196** | Individual scalar rows inside those panels | same closure |
| **Atlas CSV rows** | **~403–404** | Named rows in `data/publication/domain_atlas.csv` | atlas file (coverage map, not the green-file count) |
| **Coverage-map scientific domains** | **~407** | 35 core + extensions + intelligence compression | navigator / coverage prose |
| **Atomic obligations** | **2030** | Exportable atomic multiprover obligations | `data/cross_proof_verification_report.json` (2026-09-29) |
| **Full formal obligations** | **2594** | Full formal spine | same |
| **Catalog obligations** | **2205** | Scientific-catalog spine | same |
| **Mathlib theorems** | **5248 / 5248 (100%, L1=0)** | Formal corpus depth campaign | status snapshot |

## Stale phrases — ignore if you still see them

| Phrase | Why it is stale |
|--------|-----------------|
| 394/394 green | older public-panel subset |
| 405/405 green | mid-2026 snapshot |
| 430/432 or 432/432 or 433/433 green | pre-472 envelope |
| 476/476 green | previous file envelope; live is **477/477** |
| 5229/5229 or 5232/5232 or 5240/5240 Mathlib | previous corpus stamps; live is **5248/5248** L1=0 |
| 1,863 atomic | older export; 17 September snapshot said **2024**; 29 September cross-proof is **2030** |
| 61,445 scalar records | older envelope; 17 September snapshot said **181,477**; 29 September closure is **183,196** |
| 0.006625% median-of-medians | 17 September snapshot; 29 September prediction median is **0.005537779313588844%** over 414 |
| 2024 atomic obligations | 17 September snapshot; 29 September cross-proof is **2030** |
| 2587 full formal obligations | 17 September snapshot; 29 September cross-proof is **2594** |
| 2256 catalog obligations | 17 September snapshot; 29 September cross-proof is **2205** |
| eight-way hardware true | 17 September snapshot; 29 September cross-proof has eight-way hardware false |
| 536,740 records as the green envelope | older rollup; do not use as the 472-file gate |
| 15 Å / ~13.6 Å as the Genetics **product** or a live fold | 2026-08-07 retired MDS (`--force-bulk`). Live freeze **2026-08-17**: product **0.13 Å** vs AF **0.47 Å**. No-map path does **not** emit 3-D MDS. |
| `E_con` ≈ 21.79 W / 8.95% | Retired Cosmology Lab / aggregate P21 draft; live Homo sapiens is **20.003601 vs 20.0 W (0.018%)** |

## Rule for writers and generators

- Green-gate headlines use **477 / 477** from the margin audit.
- Atlas / coverage-map headlines must say **atlas rows** or **named domains**, not “green.”
- Atomic-obligation headlines use **2030** from the 29 September cross-proof.
- Median-of-medians headlines use **0.005537779313588844%** over 414 prediction medians.
- A generator that rewrites the 17 September snapshot reads `repo_status_snapshot.json` for that snapshot's tables.
