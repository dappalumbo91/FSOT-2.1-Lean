# Desktop workspace status — `C:\Users\damia\Desktop\FSOT-2.1-Lean`

**Canonical working root while `I:\` is under repair.**  
**Reviewed:** 2026-08-05  
**Remote:** `https://github.com/dappalumbo91/FSOT-2.1-Lean`  
**Live stamp:** [`docs/CURRENT_STATUS.md`](docs/CURRENT_STATUS.md) · sync: [`docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md)

---

## 1. What this folder is

| Property | Value |
|----------|--------|
| Role | Full **GitHub-scale** FSOT-2.1-Lean tree (math, proofs, portable vendor caches, benchmarks) |
| Size on disk | **~425 MB** / ~3,421 files |
| Authority pin | **D1D38A** — `vendor/fsot_compute.py` SHA-256 matches pin |
| Not included | Full Physical Archive offline mass (~17–39+ GB: `.lake`, bulk API dumps, SR-ITE runtime, genetics blobs, etc.) |

This is the **verification + mathematics** face of the project. It is **not** a byte-for-byte restore of the entire `I:\FSOT-Physical-Archive` tree. Catalog **results** and portable caches are here; multi-GB raw downloads often lived only on `I:`.

---

## 2. Mathematics — present and verified

| Layer | Path | Status |
|-------|------|--------|
| Seed + scalar (Float) | `FSOT/Scalar.lean` | OK |
| Seed + scalar (Real) | `FSOT/Formal/Scalar.lean` | OK |
| Interval bounds | `FSOT/Formal/Bounds.lean` (~129 KB) | OK |
| Engine theorems | `FSOT/Formal/Theorems.lean` (~106 KB) | OK |
| Domain table | `FSOT/Formal/Domains.lean` | OK |
| Domain priors | `FSOT/Formal/*Priors.lean` | **~492** modules / **506** Lean files total |
| Decimal oracle | `vendor/fsot_compute.py` | OK, pin **D1D38A** match |
| Authority pin file | `vendor/fsot_compute_AUTHORITY_PIN.json` | OK |

**Engine equation (what is being solved):**

\[
S = K \cdot (T_1 + T_2 + T_3)
\]

from seeds \((\pi, e, \varphi, \gamma, G)\). Smoke values from oracle: \(\varphi \approx 1.61803\), \(K \approx 0.42022\), \(S_{\mathrm{cosm}} \approx -0.50246\), \(S_{\mathrm{quant}} \approx 0.95551\).

---

## 3. Cross-prover verification — present

| Framework | Location | Status in last report |
|-----------|----------|------------------------|
| Lean | `FSOT/` | primary authority |
| Coq | `verification/coq/` | passed (exported spine) |
| Isabelle | `verification/isabelle/` | passed + **math core** |
| F\* | `verification/fstar/` | passed |
| Rust replay | `verification/rust/` | passed |
| QEMU boot | `verification/qemu/` | passed |
| Obligations | `verification/obligations/` | 2370 full / 1863 atomic |

**Isabelle math upgrade (local, uncommitted or pending commit):**

- `verification/isabelle/FSOTScalarMath.thy` — definitions + proved identities  
- Structural spine no longer collapses `pos` to tautology `0 < 1`  
- `ROOT` loads `FSOTScalarMath` first  
- Doc: `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`

Report snapshot: `data/cross_proof_verification_report.json` → `overall_ok: true`, `github_ready: true`.

---

## 4. Scientific / domain cross-check resources — present

### Empirical gates

| Artifact | Status |
|----------|--------|
| Domain atlas 402 rows | `data/publication/domain_atlas.csv` — **402** (35 core + 367 extension) |
| Benchmark margin | **405/405 green**, 0 fails (`data/benchmark_margin_audit.json`) |
| Navigator | `data/fsot_domain_navigator.json` + `.db` |
| Prereg predictions | `data/preregistered_predictions_manifest.yaml` |
| Formula corpus | `vendor/formula_corpus/by_domain/strict_empirical.jsonl` (~8.3 MB) |
| Unified math DB | `vendor/fsot_aggregate/FSOT_UNIFIED.db` (~43 MB) |

### Public API portable summaries (`vendor/public_data/`)

Bundled (offline-capable summaries — full live re-ingest needs network):

- NIST CODATA, GBIF, NOAA tides, World Bank, NASA exoplanet  
- RCSB PDB, OpenAlex, PubChem, CERN Open Data, UniProt  
- SH0ES, consciousness, cybersecurity, dark-energy CPL, OBIS, PBDB  

### Other scientific vendor packs (checklist **29/29** critical paths OK)

Includes: SMILES lab, evolution operons, linguistics targets, math_generator rules, species catalog, iGEM, neuron cohort cells, longevity AnAge, cosmology skeleton DB, space-weather summary, government open data, etc.  
Full path list: `data/publication/readme_sections/api_resources.md`.

### What the lost ~39 GB on `I:` likely was

Not the Lean math definitions (those are here). Typically:

- `.lake` / Mathlib build artifacts  
- Full live API caches (space weather multi-100k rows, bulk genetics, The Well blobs)  
- SR-ITE runtime, large Desktop lab mirrors under Physical Archive folders  
- Coq `.vo` / Isabelle heaps if stored offline  

**Cross-verification can continue** from this Desktop tree using bundled caches + recompute scripts. Live API refresh is optional when network + restored external cache are available.

---

## 5. Gaps vs full Physical Archive (honest)

| Item | Desktop | Typical full `I:` archive |
|------|---------|---------------------------|
| Formal math + proofs | Yes | Yes |
| Portable vendor + benchmarks | Yes | Yes + larger caches |
| `.lake` build cache | No | Often yes |
| `03_FSOT-PublicData` bulk | Partial summaries only | Full downloads |
| SR-ITE / Zig mind / Kronos trees | Not this repo root | Sibling folders on `I:` |
| Workspace size | ~0.4 GB | Multi-GB to tens of GB |

---

## 6. How to work from here

```powershell
cd C:\Users\damia\Desktop\FSOT-2.1-Lean

# Numeric / publication verification (Python)
pip install -r requirements.txt
python scripts/run_publication_verification_bundle.py

# Cross-proof re-run (when provers installed)
python scripts/run_cross_proof_verification.py

# Lean (when elan/lake ready)
lake build
```

**Do not** treat `C:\Users\damia\fsot_work\` as authority if it still exists — use **this Desktop path**.

---

## 7. Local git status (math/verification work)

As of review:

- Modified: structural generator, Isabelle ROOT / StructuralProofSpine, verification README  
- Added: `FSOTScalarMath.thy`, `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`, this status file  

Commit/push when you want GitHub to match Desktop.

---

## 8. Next math/verification priorities

1. Keep deepening `FSOTScalarMath.thy` (sign theorems, term1 negativity at high \(D_{\mathrm{eff}}\), matching Lean `Theorems.lean`).  
2. Re-run cross-proof bundle after Isabelle install.  
3. When `I:` is stable, **copy from Desktop → archive** (not the reverse thin-clone pattern).  
4. Optional: live API refresh scripts into a new cache root on a healthy disk if bulk data is unrecoverable.
