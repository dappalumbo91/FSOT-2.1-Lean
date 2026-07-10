# FSOT Tier 79 — Cross-Proof Verification

Independent re-proof of Lean connective obligations in **Coq** and **Isabelle**, plus a **Python decimal** structural layer.

## No gatekeeping

| Tool | Cost | Account required | Typical disk |
|------|------|------------------|--------------|
| Lean 4 | Free | No | (already installed) |
| Coq / Rocq Platform | Free | No | ~4 GB |
| Isabelle | Free | No | ~5 GB |
| This tree | Free | No | ~50 MB |

## Run locally

```powershell
cd FSOT-2.1-Lean-main
python scripts/run_cross_proof_verification.py
python scripts/build_cross_proof_benchmark.py
```

## Install optional frameworks

```powershell
winget install Coq.CoqPlatform
powershell -File scripts/setup_rocq_path.ps1   # if coqc not found after install
```

Default install path: `C:\Rocq-Platform~9.0~2025.08\bin`

Isabelle: download Windows installer from https://isabelle.in.tum.de/ (no sign-in).
After install, re-run `python scripts/run_cross_proof_verification.py` for `full_triangulation: true`.

## Current status (local)

Run `python scripts/run_cross_proof_verification.py` — expect:

- `python_decimal`: passed
- `lean`: passed
- `coq`: passed (+ `coqchk` when available)
- `github_ready`: true when Coq passes

## Layout

```
verification/
  obligations/connective_spine.json   ← exported from Lean
  coq/ConnectiveSpine.v               ← generated proofs (lra)
  isabelle/ConnectiveSpine.thy        ← generated proofs (eval)
```

Lean authority modules:

- `FSOT.Formal.WarpActuationDevelopmentPriors`
- `FSOT.Formal.FusionGridConnectivePriors`
- `FSOT.Formal.E10dWdConnectivePriors`

Promote to GitHub when `data/cross_proof_verification_report.json` shows `github_ready: true`.