# Count vocabulary (do not mix these)

**Authority:** [`CURRENT_STATUS.md`](CURRENT_STATUS.md) · `data/repo_status_snapshot.json`  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

These are **different ledgers**. Using one number for all of them is the discrepancy.

| Name | Live value (2026-08-18) | What it counts | Source |
|------|------------------------:|----------------|--------|
| **Green residual benchmarks** | **472 / 472** | Benchmark **files** that pass ≤0.5% pooled median | `data/benchmark_margin_audit.json` |
| **Median-of-medians** | **0.006607%** | Median of those domain medians | same + status snapshot |
| **Scalar-record envelope** | **179,914** | Individual scalar rows inside those panels | status snapshot |
| **Atlas CSV rows** | **~403–404** | Named rows in `data/publication/domain_atlas.csv` | atlas file (coverage map, not the green-file count) |
| **Coverage-map scientific domains** | **~407** | 35 core + extensions + intelligence compression | navigator / coverage prose |
| **Atomic obligations** | **2022** | Exportable atomic multiprover obligations | `data/cross_proof_verification_report.json` |
| **Full formal obligations** | **2585** | Full formal spine | same |
| **Catalog obligations** | **2222** | Scientific-catalog spine (472 domains) | same |
| **Mathlib theorems** | **5182 / 5182** | Formal corpus depth campaign | status snapshot |

## Stale phrases — ignore if you still see them

| Phrase | Why it is stale |
|--------|-----------------|
| 394/394 green | older public-panel subset |
| 405/405 green | mid-2026 snapshot |
| 430/432 or 432/432 or 433/433 green | pre-472 envelope |
| 1,863 atomic | older export; live is **2022** |
| 61,445 scalar records | older envelope; live is **179,914** |
| 536,740 records as the green envelope | older rollup; do not use as the 472-file gate |
| 15 Å AlphaFold median as the Genetics **product** | 2026-08-07 **bulk** snapshot; product freeze is in FSOT-Genetics |

## Rule for writers and generators

- Green-gate headlines use **472 / 472** from the margin audit.
- Atlas / coverage-map headlines must say **atlas rows** or **named domains**, not “green.”
- Atomic-obligation headlines use **2022**, not 1,863.
- If a generator would write an old green count, it must read `repo_status_snapshot.json` instead.
