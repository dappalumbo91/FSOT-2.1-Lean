# Live APIs + multi-prover mathematics — status

> **Historical session note (2026-08-03).** Live green / obligation counts below are **stale**. Use [`CURRENT_STATUS.md`](CURRENT_STATUS.md) and [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md): **472/472** green, **2022** atomic, **2585** full formal. Latest API probe: `data/live_api_health_report.json` (2026-08-18).

**Workspace:** `C:\Users\damia\Desktop\FSOT-2.1-Lean`  
**Date:** 2026-08-03 (session); counts superseded 2026-08-18  
**Policy:** Stream/live probe preferred; full bulk re-download not required for verification.

---

## 1. Architecture: are live APIs listed and appropriate?

**Yes.** They are first-class in the architecture:

| Artifact | Role |
|----------|------|
| `data/api_requirements.yaml` | Full external API registry (tier38, geophysics, genomics, cybersecurity, …) |
| `data/external_data_manifest.yaml` | External cache layout / portable vs live |
| `data/publication/readme_sections/api_resources.md` | Human-readable authority + API map |
| `data/publication/live_ingest_schedule.yaml` | Weekly refresh command + scheduler |
| `scripts/live_api_health_check.py` | Live stream probes (no bulk archive needed) |
| `scripts/live_api_fetch_lib.py` | Shared fetch helpers |
| `scripts/ingest_*.py` / `build_*_benchmarks.py` | Per-tier ingest + benchmark rebuild |
| `vendor/public_data/*` | Portable **summaries** for offline verify |
| `vendor/live_cache/` | Live catalog scratch |

**Design intent (correct for recovery):**  
Portable clone uses **bundled vendor caches**. Full credibility refresh **streams** from public APIs. You do **not** need the lost ~39 GB to re-validate sources — you re-stream.

Scheduler path updated to Desktop while `I:` is under repair.

---

## 2. Live API health (streamed probes, this machine)

Command: `python scripts/live_api_health_check.py`  
Report: `data/live_api_health_report.json`

| Result | Count |
|--------|------:|
| **OK** | **27** |
| **FAIL** | **4** |

### Working (examples)

GBIF, GWOSC, SIMBAD TAP, Gaia DR3 TAP, OpenNeuro, PubChem, JPL SSD CAD, NOAA GOES X-ray, OSTI DOE, UAP WAR.gov HF, NCBI Gene, Crossref, iNaturalist, NDBC buoy, Open-Meteo forecast, USGS NWIS, SoilGrids, Natural Earth, arXiv, PBDB, OBIS, NIST CODATA, The Well stats, …

Materials Project: **OK skipped** (no `MP_API_KEY` — uses bundled panel; appropriate).

### Failures (not architecture death)

| Channel | Issue | Impact |
|---------|--------|--------|
| `vizier_wds` | HTTP 404 (endpoint drift) | WDS live path; stellar catalog has bundled fallback |
| `clinicaltrials_v2` | HTTP 403 | Optional clinical panel |
| `tier84_world_bank` | Timeout | Retry; bundled `world_bank_summary.json` exists |
| `tier85_open_meteo_archive` | HTTP 400 | Query params / API change; forecast channel still OK |

**Verdict:** Live API architecture is **sound and mostly functioning**. Failures are endpoint/policy drift on a minority of channels — fixable without the Physical Archive bulk store.

---

## 3. Mathematics across verification systems (re-run today)

### Engine under formalization

\[
S = K\cdot(T_1 + T_2 + T_3)
\]

Seeds \((\pi,e,\varphi,\gamma,G)\). Authority pin **D1D38A** (`vendor/fsot_compute.py`).

### Results (this machine)

| System | Math role | Status today |
|--------|-----------|--------------|
| **Python decimal / oracle** | Authority constants + 1863 exportable obligations | **PASS** — `ok=1863 fail=0` (507 bundle_conj skipped by design) |
| **Rust `fsot_scalar_kernel`** | Executable scalar kernel parity | **PASS** — 4/4 tests |
| **Rust `fsot_obligation_replay`** | Full obligation replay | **PASS** |
| **Coq/Rocq `FSOTScalarMath.v`** | Engine identities (raw_S, scaled_S, growth_term>0, φ>1, …) | **PASS** — compiles |
| **Coq ConnectiveSpine** | Numeric connective inequalities | **PASS** |
| **Coq FullFormalSpine_00–18** | Exported domain certificates | **PASS** (00–05 + 06–18 batch) |
| **Coq StructuralProofSpine** | Bundle conjuncts | **PASS** (compiles; large-nat warnings only) |
| **Isabelle `FSOTScalarMath.thy`** | Same engine math in HOL | **Present** — needs `isabelle build` (binary not on PATH this session) |
| **Isabelle FullFormalSpine / Structural** | Export + fixed non-tautology spine | **Present** on disk |
| **F\*** `FSOTScalarKernel.fst` | Boot scalar spec | **Present** — `fstar` not on PATH this session |
| **Lean 4 Formal** | Primary Real math (`Scalar`/`Bounds`/`Theorems` + 492 priors) | **Sources present**; full `lake build` needs Mathlib cache (not re-run bulk here) |

### New / deepened formal math (Desktop)

- `verification/coq/FSOTScalarMath.v` — **new**, compiles under Rocq 9  
- `verification/isabelle/FSOTScalarMath.thy` — engine math (not structure-only)  
- Structural Isabelle generator fix (real literals, not `0 < 1` tautology)  
- `_CoqProject` lists `FSOTScalarMath.v` first  

---

## 4. Empirical spine still on Desktop (not “down the drain”)

| Ledger | Value |
|--------|------:|
| Routed / coverage-map domains | **~407** named (atlas CSV ~403 rows) — not the green-file count |
| Benchmark green gates | **472/472** (live `docs/CURRENT_STATUS.md`) |
| Scalar-record envelope | **179,914** |
| Formal atomic obligations | **2022** (full formal **2585**) |
| Strict-empirical formulas | **7941** |

---

## 5. Recoverability — honest answer

| Layer | Recoverable without `I:`? |
|-------|---------------------------|
| Math definitions + formal spines | **Yes** — Desktop/GitHub |
| Cross-prover obligations | **Yes** — re-run Python/Rust/Coq now |
| Live scientific sources | **Yes** — stream via listed APIs (27/31 live today) |
| Bulk offline multi-GB caches | **Nice-to-have**; rebuild by streaming over time |
| Physical Archive SR-ITE / extra trees | Only if `I:` repair succeeds |

You are **not** blocked on formal mathematics or on re-touching scientific APIs. You are blocked only on multi-GB offline convenience caches and non-repo archive trees until disk repair or re-stream rebuilds them.

---

## 6. Commands to re-verify anytime

```powershell
cd C:\Users\damia\Desktop\FSOT-2.1-Lean

# Live APIs (stream probes)
python scripts/live_api_health_check.py

# Math oracle + exportable obligations
python -c "..."  # or: python scripts/run_cross_proof_verification.py

# Rust scalar + obligations
cd verification\rust\fsot_scalar_kernel; cargo test
cd ..\fsot_obligation_replay; cargo test

# Coq math + spines
cd ..\..\coq
coqc -R . "" FSOTScalarMath.v
coqc -R . "" ConnectiveSpine.v
# … FullFormalSpine_*.v

# Isabelle (when installed on PATH)
cd ..\isabelle
isabelle build -d . FSOT_CrossProof
```

---

## 7. Next fixes (optional, prioritized)

1. Patch `vizier_wds` URL in fetch lib (404).  
2. Soft-fail / retry World Bank timeout; keep bundled summary as fallback.  
3. Install/link Isabelle; build `FSOT_CrossProof` including `FSOTScalarMath`.  
4. Full `lake build` when Mathlib cache available.  
5. Port more Lean sign theorems into Coq/Isabelle `FSOTScalarMath` (term1 sign at high \(D_{\mathrm{eff}}\)).  
