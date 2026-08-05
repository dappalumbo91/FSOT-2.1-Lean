# Open science — next frontiers (beyond original high-value gaps)

**Policy:** auth=none only. No API keys, no sign-on for default residual path.  
**Status of original curated gaps:** all **covered** (see atlas `--gaps`).  
**This list:** next expansion candidates after depth polish.

Rebuild inventory: `python scripts/query_fsot_atlas.py --gaps`  
Depth pass: `python scripts/build_open_depth_expansion.py`

---

## Math policy (non-negotiable)

All frontier residual panels use **FSOT mathematics only**:

- `make_fsot_record` → `fsot_scaled` (seed-locked domain scalar)
- **No** free-fit parameters
- **No** ad-hoc physics formulas
- **No** `formula_mass` short-circuit (`formula=None` always in frontier builders)
- Builders: `scripts/build_open_frontier_wave1.py`, `wave2.py`

## Multiprover re-proof (same stack as historical green domains)

After residual panels are green, they enter the multiprover spine:

```text
python scripts/gen_open_frontier_priors_lean.py
python scripts/export_scientific_catalog_obligations.py
python scripts/generate_scientific_catalog_artifacts.py
python scripts/export_full_priors_obligations.py
python scripts/run_cross_proof_verification.py
```

| Layer | Role |
|-------|------|
| Lean 4 | `*OpenPriors.lean` + `ScientificCatalogSpine.lean` |
| Coq | `ScientificCatalogSpine_*.v`, `FullFormalSpine_*.v` |
| Isabelle | `ScientificCatalogSpine_*.thy`, `FullFormalSpine_*.thy` |
| Python Decimal | obligation triangulation |
| Z3 SMT | bulk catalog bounds |
| Rust / F* / QEMU / ESP32 | executable + hardware parity |

Latest multiprover report: `data/open_frontier_multiprover_report.json`  
Cross-proof master: `data/cross_proof_verification_report.json` (`overall_ok: true`)

---

## Frontier wave 1 — COVERED (2026-08-05)

| ID | Panel artifact | Records | Pooled residual |
|----|----------------|---------|-----------------|
| `pdg_live_depth` | `pdg_live_depth_open_benchmark.json` | 33 | ~0.010% |
| `gaia_source_sample` | `gaia_dr3_source_sample_open_benchmark.json` | ~610 | ~0.022% |
| `simbad_identity_depth` | `simbad_identity_depth_open_benchmark.json` | ~328 | ~0.022% |
| `lmfdb_elliptic_curves` | `lmfdb_elliptic_curves_open_benchmark.json` | ~1116 | ~0.015% |
| `gwas_catalog_depth` | `gwas_catalog_depth_open_benchmark.json` | ~81 | green |
| `pubchem_assay_depth` | `pubchem_depth_open_benchmark.json` | ~149 | ~0.041% |
| `openalex_citation_depth` | `openalex_citation_depth_open_benchmark.json` | ~150 | ~0.009% |

Rebuild: `python scripts/build_open_frontier_wave1.py`

---

## Frontier wave 2 — COVERED

Builder: `scripts/build_open_frontier_wave2.py` (FSOT residual only)

| ID | Artifact | Notes |
|----|----------|-------|
| `uniprot_proteome_slice` | `uniprot_proteome_slice_open_benchmark.json` | UniProt REST |
| `alphafold_batch_meta` | `alphafold_batch_meta_open_benchmark.json` | AlphaFold DB API |
| `rcsb_structure_batch` | `rcsb_structure_batch_open_benchmark.json` | RCSB open entries |
| `oeis_family_sweep` | `oeis_family_sweep_open_benchmark.json` | OEIS families |
| `usgs_seismic_history` | `usgs_seismic_history_open_benchmark.json` | USGS M≥6 |
| `noaa_tides_multi_station` | `noaa_tides_multi_station_open_benchmark.json` | CO-OPS levels |
| `gbif_taxon_depth` | `gbif_taxon_depth_open_benchmark.json` | GBIF occurrences |
| `zenodo_records_depth` | `zenodo_records_depth_open_benchmark.json` | Zenodo records |

---

## Frontier wave 3 — COVERED

Builder: `scripts/build_open_frontier_wave3.py` (FSOT residual only)

| ID | Artifact | Notes |
|----|----------|-------|
| `endf_reaction_subset` | `endf_iaea_nuclear_open_benchmark.json` | IAEA levels/gammas open nuclear |
| `nist_asd_multi_species` | `nist_asd_multi_species_open_benchmark.json` | Multi-species line anchors |
| `desi_edr_table_slice` | `desi_edr_table_slice_open_benchmark.json` | Public portal + BAO anchors (no multi-GB FITS) |
| `gwosc_strain_metadata` | `gwosc_strain_metadata_open_benchmark.json` | Open strain archive JSON metadata |
| `codata_full_table` | `codata_full_table_open_benchmark.json` | NIST CODATA allascii residual sweep |

---

## Explicitly out of default path

| Resource | Reason | Open substitute |
|----------|--------|-----------------|
| Materials Project live key | API key | JARVIS OPTIMADE + COD |
| FRED live key | API key | World Bank Open Data |
| CDS ERA5 (account) | free account wall | NCEI Climate-at-a-Glance open CSVs |
| Clinical restricted dumps | license | public subsets only |

---

## Working rule

1. Prefer endpoint with `auth: none` already in `data/api_requirements.yaml` or `open_science_sources_lib.py`.  
2. Cache under `vendor/open_science/<id>/`.  
3. Residual only via `make_fsot_record`.  
4. Rebuild margin audit + atlas SQLite.  
5. Mark frontier `covered` in atlas gap table when panel is green.

---

## Multi-drive bulk data

External root resolver: `scripts/fsot_external_data_root.py`  
Preference: `FSOT_EXTERNAL_DATA_ROOT` → `G:\FSOT-PublicData` → `I:\FSOT-PublicData` → repo cache.

Large open downloads land under:
`{external}/open_science_large/{codata,gaia,simbad,lmfdb,climate_ncei,desi}/`

Wave 4 large builder: `scripts/build_open_frontier_wave4_large.py`

## Wave 4 large depth — COVERED (FSOT residual)

| Panel | Scale | Notes |
|-------|-------|-------|
| CODATA full | 38 constants | Ellipsis + alias parse fixed |
| Gaia DR3 TAP | ~3459 residual rows | TOP 400 sources cached on G: |
| SIMBAD TAP | ~1365 rows | TOP 250 cached on G: |
| LMFDB nf+ec | ~3918 / ~1016 | degrees 2–5 + EC 150 |
| NCEI multivar climate | ~607 | land/ocean/NHem/SHem series |
| DESI bulk | portal + anchors | full zall FITS → G:\…\desi\ |

## DESI FITS residual attach — COVERED

Builder: `scripts/build_desi_fits_residual_panel.py`

| Item | Value |
|------|-------|
| FITS | `G:\FSOT-PublicData\open_science_large\desi\zall-pix-fuji.fits` (~2.1 GB) |
| Catalog rows | **2,847,435** |
| Quality sample | ZWARN=0 · **2500** objects |
| Residual records | **~37,080** (Z, ZERR, fluxes, χ², Δχ², mags, TSNR…) |
| Pooled residual | **~0.026%** green |
| Benchmark | `data/desi_edr_fits_residual_benchmark.json` |
| Lean | `FSOT/Formal/DesiEdrFitsResidualPriors.lean` |

Math: `make_fsot_record` → `fsot_scaled` only.

## Suggested order (next waves)

1. ChEMBL activity assays + deeper PubChem  
2. LMFDB modular forms / more number-field degrees  
3. More GWOSC strain windows on external disk  
4. Optional: larger DESI residual sample / DR1 products on I:
