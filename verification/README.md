# FSOT Cross-Proof Verification (Tiers 79–91 + scalar math core)

Independent re-proof of exported Lean numeric obligations across **Python decimal**, **Coq**, **Isabelle**, **Rust f64**, **F\***, and **QEMU bare-metal** runtime.

## Live APIs (stream; bulk download optional)

Architecture: `data/api_requirements.yaml`, health probe `scripts/live_api_health_check.py`.  
Status write-up: `docs/LIVE_API_AND_MATH_VERIFICATION_STATUS.md`.  
Portable verify uses `vendor/` caches; live refresh **streams** public APIs.

## Isabelle mathematical engine (required reading)

Isabelle is **not** limited to structure-of-the-rest checks. The session now includes:

| Theory | Role |
|--------|------|
| **`FSOTScalarMath.thy`** | Seed constants, `term1/term2/term3`, `raw_S` / `scaled_S`, proved identities (`raw_S = t1+t2+t3`, `growth_term > 0`, `quirk_mod = 1` when unobserved, domain routes, native π/e intervals) |
| `FullFormalSpine_*.thy` | Exported numeric certificates (literal inequalities / counts) — triangulation of Lean export |
| `StructuralProofSpine.thy` | Bundle conjuncts with **real positive literals** (fixed: no longer collapses `pos` to `0 < 1`) |
| `TranscendentalBounds*.thy` | π/e interval lemmas (native Approximation + certified points) |

**Honest scope:** FullFormalSpine still triangulates *exported numeric obligations*, not a full re-derivation of every Lean `FSOT.Formal.*Priors` proof term. The scalar engine math lives in `FSOTScalarMath.thy` (Isabelle) and `FSOT/Formal/Scalar.lean` + `Bounds.lean` + `Theorems.lean` (Lean primary authority).

## Run (authoritative)

```powershell
cd <repo-root>
python scripts/run_cross_proof_verification.py
```

This regenerates:

- `data/cross_proof_verification_report.json` — single source of truth
- `data/cross_proof_verification_manifest.yaml` → `status_local` (fail-closed, no hand-edits)
- `data/cross_proof_verification_benchmark.json`

**Pass bar (repo):** `overall_ok: true` = seven-way bare-metal (Lean+Coq+Isabelle+Rust+F\*+QEMU serial+disk).

**ESP32 hardware** is optional unless you pass `--require-esp32` (needs CP210x COM port).

## What is cross-verified

| Layer | Count | Frameworks |
|-------|-------|------------|
| Connective spine | 24 obligations | Lean → Python → Coq → Isabelle |
| Full formal spine | 1,241 provable obligations | same + Rust f64 replay |
| Transcendental bounds | 68 lemmas | Coq/Isabelle with **certified π/e axioms** (2 intervals deferred) |
| Boot scalar | 1 canonical value | Rust no_std ↔ Python ↔ F\* constants ↔ QEMU UART |

**Coverage honesty:** Coq connective spine = **~1.43%** of Lean theorem count. Cross-proof triangulates **exported numeric obligations**, not every `FSOT.Formal.*` module. Engine math is separately formalized in Lean `FSOT.Formal.*` and Isabelle `FSOTScalarMath.thy` (see `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`).

## Documented proof debt (`proof_debt` in report)

- F\*: `boot_scalar_positive` / `boot_scalar_matches_canonical` are explicit **assume** lemmas (transcendental shell).
- F\*: `cos`, `sin`, `sqrt` primitives assumed on reals.
- Coq/Isabelle: `certified_*` axioms for π/e intervals (see `audit_transcendental_bounds_gap.py`).

Numeric truth for boot scalar is triangulated via **Tier 85 Rust/Python f64** — not hidden `admit()`.

## Install optional frameworks

```powershell
winget install Coq.CoqPlatform
powershell -File scripts/setup_rocq_path.ps1
powershell -ExecutionPolicy Bypass -File scripts/install_isabelle_windows.ps1
```

## Layout

```
verification/
  obligations/          exported JSON from Lean
  coq/                  generated .v chunks
  isabelle/             generated .thy chunks
  rust/fsot_obligation_replay/
  fstar/                FSOTScalarKernel.fst, FSOTScalarBoot.fst
  qemu/                 golden_boot_serial.txt, golden_boot_disk.txt
  esp32/                golden_boot_serial.txt (optional hardware tier)
```

Promote to GitHub when `cross_proof_verification_report.json` shows `github_ready: true`.