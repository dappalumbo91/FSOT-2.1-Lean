# FSOT Atlas SQLite — design (math unchanged)

**Purpose:** Professional, queryable index of what FSOT has already residual-gated — domains, records, formulas, open-science citations — **without** a second compute engine or free parameters.

**Authority remains:** `vendor/fsot_compute.py` pin **D1D38A** + green JSON benchmarks.  
**DB is a view** rebuilt from those artifacts.

---

## Policy

| Rule | Detail |
|------|--------|
| Open science only | No API keys, sign-in, or paid portals for *atlas rebuild* or *gap ingest* |
| Regenerable | `python scripts/build_fsot_atlas_sqlite.py` |
| Offline portable | Ship `data/fsot_atlas.sqlite` in clone; optional live open probes |
| No math rewrite | No re-derivation of seeds; no least-squares |

Full credential policy: [`OPEN_SCIENCE_ONLY_POLICY.md`](OPEN_SCIENCE_ONLY_POLICY.md).

---

## Schema

| Table | Role |
|-------|------|
| `meta` | build time, pin, green counts |
| `domains` | one row per green residual panel |
| `records` | material_records (sampled for huge catalogs) |
| `formulas` | unique formula strings + use counts |
| `citations` | public dataset/API/literature anchors |
| `open_sources` | no-key open science endpoints (registry) |
| `high_value_gaps` | curated untouched frontiers (open data only) |
| `fts_domains` | FTS5 search over domain names / files |

### Large catalogs

Panels with `record_count ≥ 10_000` (e.g. MPCORB):

- Domain row always full stats  
- Records table stores **up to 5_000** sample rows  
- `domains.full_json_path` points at the full benchmark JSON  

---

## Commands

```powershell
# Build / rebuild atlas (offline; uses existing JSON)
python scripts/build_fsot_atlas_sqlite.py

# Query examples
python scripts/query_fsot_atlas.py --stats
python scripts/query_fsot_atlas.py --search higgs
python scripts/query_fsot_atlas.py --family physics
python scripts/query_fsot_atlas.py --gaps
python scripts/query_fsot_atlas.py --domain Particle_Physics --limit 20
```

**Outputs:**

- `data/fsot_atlas.sqlite`  
- `data/fsot_atlas_build_report.json`  

---

## Relation to other DBs

| Artifact | Role |
|----------|------|
| `data/fsot_atlas.sqlite` | **This** — residual atlas + open gaps + citations |
| `data/fsot_domain_navigator.db` | Intent/routing discovery (kept) |
| `vendor/fsot_aggregate/FSOT_UNIFIED.db` | Formula corpus aggregate (kept) |
| `vendor/knowledge_base/` | Formula verification corpus (kept) |

Do not merge blindly; atlas is the **professional inventory layer** for green solves.

---

## After atlas is up

Hit **high-value gaps** with open public data only (Materials Project *only if no key*; prefer COD/NOMAD/PubChem open; ENDF public, GWTC, NuFIT public tables, FRED *requires key → skip*, etc.). Prefer:

- NIST, PDG public HTML/tables  
- GBIF, USGS, OpenAlex, PubChem, UniProt, RCSB, Ensembl, ChEMBL, Zenodo, arXiv API (no key)  
- MPCORB / Harvard–CfA public catalogs  
- Bundled `vendor/public_data/*`  

ArXiv paper depth can proceed in parallel; **endorsement is process**, not residual math.
