# Open science expansion (no credentials)

**Workspace:** `C:\Users\damia\Desktop\FSOT-2.1-Lean`  
**Policy:** every stream is **public**, **no signup**, **no API keys**.

## Commands

```powershell
cd C:\Users\damia\Desktop\FSOT-2.1-Lean
python scripts/ingest_open_science_expansion.py
python scripts/build_open_science_expansion_benchmarks.py
python scripts/evaluate_open_science_holdouts.py
python scripts/audit_margin_and_scientific_metrics.py
python scripts/live_api_health_check.py
# optional full publication path with live open ingest:
python scripts/run_publication_verification_bundle.py --with-open-science-ingest
```

## What was added

| Piece | Path |
|-------|------|
| Source registry | `scripts/open_science_sources_lib.py` |
| Ingest | `scripts/ingest_open_science_expansion.py` |
| Benchmarks | `scripts/build_open_science_expansion_benchmarks.py` |
| Holdouts | `data/preregistered_open_science_holdouts.yaml` |
| Holdout eval | `scripts/evaluate_open_science_holdouts.py` |
| Caches | `vendor/open_science/*/live.json` |
| API registry | `data/api_requirements.yaml` → `open_science_expansion` |

## Streams (examples, all auth:none)

OpenFDA · Ensembl · GWAS Catalog · ChEMBL · USGS earthquakes · Wikidata · OWID CO₂ · Zenodo · AlphaFold DB · RCSB PDB · NASA DONKI · OpenAlex · PubMed eutils · Crossref · World Bank · NIST CODATA · GBIF · STRING · PubChem · CERN Open Data

## Honesty model

1. **Seed math identities** (φ, e, π, η_eff, ψ_con) — definitional residuals ≈ 0.  
2. **γ / Catalan** — open literature multiprecision anchors (not in NIST fundamental allascii).  
3. **Live NIST CODATA** — parses c, h, k_B, fine-structure, electron mass vs accepted SI/CODATA.  
4. **Catalog integrity** — PubChem/ChEMBL aspirin MW vs literature.  
5. **Stream evidence** — live connectivity counts; not fake sub-% fits to force green.

## Publication bundle

`run_publication_verification_bundle.py` now always runs:

- `audit_margin_and_scientific_metrics.py`
- `evaluate_open_science_holdouts.py`

Optional: `--with-open-science-ingest` to refresh streams first.
