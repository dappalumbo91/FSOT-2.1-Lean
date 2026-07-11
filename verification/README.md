# FSOT Cross-Proof Verification (Tiers 79–91)

Independent re-proof of exported Lean numeric obligations across **Python decimal**, **Coq**, **Isabelle**, **Rust f64**, **F\***, and **QEMU bare-metal** runtime.

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

**Coverage honesty:** Coq connective spine = **~1.43%** of Lean theorem count. Cross-proof triangulates **exported numeric obligations**, not every `FSOT.Formal.*` module.

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