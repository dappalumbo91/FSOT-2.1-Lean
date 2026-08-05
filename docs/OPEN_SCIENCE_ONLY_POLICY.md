# Open science only — no credentials / no sign-on

**Policy for FSOT-2.1-Lean public verification and atlas expansion.**

---

## Hard rules

1. **No API keys** required to clone, rebuild atlas, or run green gates.  
2. **No sign-in / OAuth / institutional VPN** for public reproduction paths.  
3. Prefer **bundled vendor caches** + **documented public URLs**.  
4. Live fetch is optional; failures must not block portable green.  
5. If a dataset **requires** credentials (Materials Project key, FRED key, many clinical DBs), it is **out of band** unless a fully open mirror exists.

---

## Allowed sources (examples)

| Family | Open endpoints |
|--------|----------------|
| Constants | NIST CODATA ASCII, SI definitions |
| Particle | PDG public tables / reviews |
| Catalogs | MPCORB (MPC/CfA), Gaia archive TAP (public), SIMBAD |
| Chemistry | PubChem PUG REST, ChEMBL public API |
| Biology | UniProt REST, Ensembl REST, RCSB, AlphaFold DB public API, OpenFDA |
| Earth | USGS FDSN, NOAA open services, OWID GitHub raw |
| Scholarly | OpenAlex, arXiv API, Crossref, Zenodo API, PubMed eutils |
| Code | Public GitHub raw / no-auth APIs for OSS genome panels |

Registry files:

- `data/api_requirements.yaml` — mark `auth: none` only for default paths  
- `scripts/open_science_sources_lib.py` — no-key probe list  
- `docs/BENCHMARK_DATA_CITATIONS.md` — per-panel anchors  

---

## Disallowed for default pipeline

- Materials Project **with** `MP_API_KEY` (optional key path may exist for your machine; not required for green)  
- FRED API **with** key (optional on a private machine only)  
- Any service that returns 401 without an account  
- License-restricted clinical dumps (e.g. full MIMIC) without public subset  

### Open substitutes (default pipeline)

| Credential wall | Open replacement | Builder |
|-----------------|------------------|---------|
| Materials Project API key | **JARVIS-DFT OPTIMADE** (NIST) + **COD OPTIMADE** | `scripts/build_open_credential_replacements.py` |
| FRED API key | **World Bank Open Data** (GDP, unemployment, CPI, population) | same script + existing `world_bank_development` panel |

Bundled MP summary caches may remain for offline clones; live expansion uses open substitutes only.  

---

## ArXiv / papers

Manuscript depth and residual evidence can grow **without** endorsement.  
**Publication** on arXiv needs endorsement — that is social/process, separate from residual green and atlas organization.

---

## Expansion rule of thumb

When hitting high-value gaps:

1. Check open endpoint + citation  
2. Prefer cache under `vendor/public_data/`  
3. Residual-gate with **FSOT formula only** (pin + `fsot_scaled`)  
4. Rebuild atlas SQLite  
5. Never invent free-fit parameters  
