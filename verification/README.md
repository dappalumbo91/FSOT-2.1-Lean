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

Isabelle (no sign-in, ~600 MB):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_isabelle_windows.ps1
```

If auto-download fails, use your browser: https://isabelle.in.tum.de/ → save `Isabelle2024-1_windows.exe` to Downloads → re-run the script.

Delete any corrupt tiny file in Downloads (281 bytes) before retrying.

## Coverage vs full FSOT corpus

```powershell
python scripts/audit_cross_proof_coverage.py
```

Tier 79 Coq proves the **connective spine** (24 obligations, 3 modules) — not all 245 domains yet.

Tier 80 exports **1081** obligations from **301** priors modules via `export_full_priors_obligations.py`.

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