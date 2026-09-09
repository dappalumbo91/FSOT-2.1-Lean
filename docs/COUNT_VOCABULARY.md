# Count vocabulary (do not mix these)

**Authority:** [`CURRENT_STATUS.md`](CURRENT_STATUS.md) · `data/repo_status_snapshot.json`  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

These are **different ledgers**. Using one number for all of them is the discrepancy.

| Name | Live value (2026-09-09) | What it counts | Source |
|------|------------------------:|----------------|--------|
| **Green residual benchmarks** | **477 / 477** | Benchmark **files** that pass ≤0.5% pooled median (live tiers in CURRENT_STATUS) | `data/benchmark_margin_audit.json` |
| **Hand PREDs** | **77** | PRED-001–084 in the prereg manifest | `predictions/preregistered_predictions_manifest.yaml` |
| **Median-of-medians** | **0.006625%** | Median of those domain medians | same + status snapshot |
| **Scalar-record envelope** | **181,477** | Individual scalar rows inside those panels | status snapshot |
| **Atlas CSV rows** | **~403–404** | Named rows in `data/publication/domain_atlas.csv` | atlas file (coverage map, not the green-file count) |
| **Coverage-map scientific domains** | **~407** | 35 core + extensions + intelligence compression | navigator / coverage prose |
| **Atomic obligations** | **2024** | Exportable atomic multiprover obligations | `data/cross_proof_verification_report.json` |
| **Full formal obligations** | **2587** | Full formal spine | same |
| **Catalog obligations** | **2256** | Scientific-catalog spine (477 domains) | same |
| **Mathlib theorems** | **5229 / 5229 (100%, L1=0)** | Formal corpus depth campaign | status snapshot |

## Stale phrases — ignore if you still see them

| Phrase | Why it is stale |
|--------|-----------------|
| 394/394 green | older public-panel subset |
| 405/405 green | mid-2026 snapshot |
| 430/432 or 432/432 or 433/433 green | pre-472 envelope |
| 476/476 green | previous file envelope; live is **477/477** |
| 1,863 atomic | older export; live is **2024** |
| 61,445 scalar records | older envelope; live is **181,477** |
| 536,740 records as the green envelope | older rollup; do not use as the 472-file gate |
| 15 Å / ~13.6 Å as the Genetics **product** or a live fold | 2026-08-07 retired MDS (`--force-bulk`). Live freeze **2026-08-17**: product **0.13 Å** vs AF **0.47 Å**. No-map path does **not** emit 3-D MDS. |
| `E_con` ≈ 21.79 W / 8.95% | Retired Cosmology Lab / aggregate P21 draft; live Homo sapiens is **20.003601 vs 20.0 W (0.018%)** |

## Rule for writers and generators

- Green-gate headlines use **477 / 477** from the margin audit.
- Atlas / coverage-map headlines must say **atlas rows** or **named domains**, not “green.”
- Atomic-obligation headlines use **2024**, not 1,863.
- If a generator would write an old green count, it must read `repo_status_snapshot.json` instead.
