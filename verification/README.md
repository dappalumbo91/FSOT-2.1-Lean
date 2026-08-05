# FSOT Cross-Proof Verification (Tiers 79–91 + scalar math core)

Independent re-proof of exported Lean numeric obligations — **and scientific catalog residual gates** — across **Python decimal**, **Coq**, **Isabelle**, **SMT (Z3/CVC5)**, **TLA+ routing flow**, **Rust f64**, **F\***, and **QEMU bare-metal** runtime.

Pipeline roles (Lean master · SMT bulk · TLA+ flow): `docs/FORMAL_PIPELINE_ROLES.md`.

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
| `ScientificCatalogSpine_*.thy` | **Scientific residual gates** (pooled median / max-scalar / green flags / seeds) — multi-prover catalog re-proof |
| `StructuralProofSpine.thy` | Bundle conjuncts with **real positive literals** (fixed: no longer collapses `pos` to `0 < 1`) |
| `TranscendentalBounds*.thy` | π/e interval lemmas (native Approximation + certified points) |

**Honest scope:** FullFormalSpine + ScientificCatalogSpine triangulate *exported numeric / residual-gate obligations*, not a full re-derivation of every Lean `FSOT.Formal.*Priors` proof term from raw telescope pixels. The scalar engine math lives in `FSOTScalarMath.thy` (Isabelle) and `FSOT/Formal/Scalar.lean` + `Bounds.lean` + `Theorems.lean` (Lean primary authority).

## Run (authoritative)

```powershell
cd <repo-root>
python scripts/run_cross_proof_verification.py
```

This regenerates:

- `data/cross_proof_verification_report.json` — single source of truth
- `data/cross_proof_verification_manifest.yaml` → `status_local` (fail-closed, no hand-edits)
- `data/cross_proof_verification_benchmark.json`

**Pass bar (repo):** `overall_ok: true` = seven-way bare-metal (Lean+Coq+Isabelle+Rust+F\*+QEMU serial+disk) · **ESP32** extends eight-way hardware when harness passes.

**ESP32 hardware** is optional unless you pass `--require-esp32` (needs CP210x COM port).

**Live multiprover + green counts:** [`docs/CURRENT_STATUS.md`](../docs/CURRENT_STATUS.md) · debt clarified: [`docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md`](../docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md).

## What is cross-verified (typical post–2026-08 multiprover)

| Layer | Count (order) | Frameworks |
|-------|---------------|------------|
| Connective spine | 24 obligations | Lean → Python → Coq → Isabelle |
| Full formal atomic | **~1,904** provable | same + Rust f64 replay |
| Structural `bundle_conj` | ~526 indices (54 unparsed-export excluded) | Lean indices; **not** residual fails |
| **Scientific catalog spine** | **~2,025** residual / seed gates | Python + Coq + Isabelle + Lean + **SMT bulk** |
| Transcendental bounds | **68** inventory lemmas (all multiprovered) | Coq/Isabelle/Rust; 2 π/e Mathlib-style in Lean |
| Domain-routing flow | finite TLA+ model | `verification/tla/FSOTDomainRouting.tla` |
| Boot scalar | 1 canonical value | Rust no_std ↔ Python ↔ F\* constants ↔ QEMU UART |
| True margin violations | **0** | `margin_violations.json` |

**Coverage honesty:** Cross-proof triangulates **exported numeric obligations**, not every `FSOT.Formal.*` module. Engine math is separately formalized in Lean `FSOT.Formal.*` and Isabelle `FSOTScalarMath.thy` (see `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`).

## Documented proof debt (honest)

- Structural bundles with unparsed conjuncts: export-index exclusion, **not** green residual fails.
- Optional: deeper non-numeric π/e proofs in Coq/Isabelle (Lean already proves intervals).
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
  obligations/          exported JSON (connective, full formal, scientific catalog, …)
  coq/                  generated .v chunks (incl. ScientificCatalogSpine_*)
  isabelle/             generated .thy chunks (incl. ScientificCatalogSpine_*)
  smt/                  SMT-LIB2 bulk residual bounds
  tla/                  FSOTDomainRouting.tla (preregistered-fold flow)
  rust/fsot_obligation_replay/
  fstar/                FSOTScalarKernel.fst, FSOTScalarBoot.fst
  qemu/                 golden_boot_serial.txt, golden_boot_disk.txt
  esp32/                golden_boot_serial.txt (optional hardware tier)
```

Promote to GitHub when `cross_proof_verification_report.json` shows `github_ready: true`.