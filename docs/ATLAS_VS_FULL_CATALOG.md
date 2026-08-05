# Atlas ~90k rows vs million-row catalogs — what is actually solved

## Short answer

**~92k is not “how much FSOT can residual-gate.”**  
It is how many **individual residual rows are copied into the portable Atlas SQLite** for browsing.

Large catalogs are residual-gated in their **benchmark authority files** (and external full products). The atlas **samples** huge panels so the SQLite stays queryable.

You are right about the math: **the same FSOT residual law** (`make_fsot_record` → `fsot_scaled`, pin D1D38A, zero free fits) is applied to every row we choose to evaluate. Expanding coverage is “apply the same math to more of the set,” not inventing new formulas.

---

## Two layers

| Layer | What it stores | Purpose |
|-------|----------------|---------|
| **Authority residual solve** | Full (or quality-full) stats in `data/*_benchmark.json` + optional external arrays on `G:\FSOT-PublicData\...` | Green gate: pooled median ≤ 0.5% under FSOT law |
| **Atlas SQLite view** | Domain metadata + **sampled** `material_records` (cap **5,000** rows when panel ≥ 10k) | Inventory / search / open-science map |

Atlas builder rule (`scripts/build_fsot_atlas_sqlite.py`):

```text
if record_count ≥ 10_000 → store only first 5_000 material_records in SQLite
```

Domain row still has **full** `record_count` / pooled median from the benchmark.

---

## Real scale examples (authority, not atlas sample)

| Catalog | What is residual-gated | Approx scale |
|---------|------------------------|--------------|
| **MPCORB** | Full minor-planet panel | **1,554,101** records in `mpcorb_fsot_benchmark.json` |
| **DESI EDR zall FITS** | All **ZWARN==0 & Z>0** quality objects, multi-property channels | Catalog **2,847,435** rows; quality ~**1.4M** objects; full residual obs in millions (see full residual script) |
| **GWTC** | Open event catalog properties | ~thousands of property rows |
| **Gaia / SIMBAD TAP** | Public TAP samples (expandable) | thousands+ of residual rows |

Atlas then shows ~90k **stored sample rows across all 470 domains**, not “only 90k objects exist in science.”

---

## Multiprover (Lean / Coq / Isabelle / …)

Provers re-check **gate claims**, not one theorem per catalog object:

- `record_count > 0`
- `pooled_median_error_pct < 0.5`
- green flag / max-scalar bounds

So full-catalog residual accuracy **strengthens the empirical claim** that the multiprover certificates. More rows residual-gated → harder to dismiss as “toy sample,” while formal stack still certifies the **inequalities** honestly.

---

## Commands

```text
# Full DESI quality residual (writes external full stats + portable sample)
python scripts/build_desi_fits_full_residual.py

# Atlas rebuild (sampled view)
python scripts/build_fsot_atlas_sqlite.py
python scripts/query_fsot_atlas.py --stats

# Multiprover gate re-proof
python scripts/export_scientific_catalog_obligations.py
python scripts/run_cross_proof_verification.py
```

External full DESI product (after full residual run):

```text
G:\FSOT-PublicData\open_science_large\desi\full_quality_residual_summary.json
G:\FSOT-PublicData\open_science_large\desi\full_quality_error_pct.npz
```

---

## Policy

- Same math everywhere: FSOT seed-locked residual only  
- No free-fit parameters  
- Open data only for default path  
- Multi-drive bulk files via `scripts/fsot_external_data_root.py`  
