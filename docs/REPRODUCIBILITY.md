# Reproducibility guide (human-first)

**Edition:** 2026-08-05  
**Repo:** https://github.com/dappalumbo91/FSOT-2.1-Lean  
**Authority pin:** first 6 hex of SHA-256(`vendor/fsot_compute.py`) = **D1D38A** when `pin_match` is true  
**Live numbers:** always refresh with `python scripts/build_repo_status_snapshot.py` → [`CURRENT_STATUS.md`](CURRENT_STATUS.md)

This document is the **primary** reproduction path for scientists and independents.  
Lean-centric details also live in [`../REPRODUCE.md`](../REPRODUCE.md).  
Fast falsification: [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md).

---

## What “reproduced” means here

A clean clone is successful when **all** of the following hold:

| # | Criterion | How you check |
|---|-----------|----------------|
| 1 | Authority pin matches D1D38A | Status snapshot or SHA-256 of `vendor/fsot_compute.py` |
| 2 | Empirical green gate: all active benchmarks ≤ **0.5%** pooled median residual | `python scripts/audit_all_benchmark_margins.py` → `data/benchmark_margin_audit.json` |
| 3 | Zero free-parameter audit | `python scripts/audit_parameter_count.py` → **ZERO_FREE** |
| 4 | Multiprover triangulation `overall_ok` | `python scripts/run_cross_proof_verification.py` (toolchains required) |
| 5 | Label A / Label B flags match frozen checklist | `python scripts/build_toe_gap_closure.py` → `data/toe_gap_closure_report.json` |

If (1)–(3) pass and (4) fails only for missing Coq/Isabelle/etc., report **partial formal** honestly — do not invent prover success.

---

## Prerequisites

| Tool | Required for | Notes |
|------|--------------|--------|
| Python 3.11+ | Empirical + generators | `pip install -r requirements.txt` |
| Git | Clone | — |
| Lean 4 via elan | Full formal | Toolchain file: `lean-toolchain` (currently `leanprover/lean4:v4.31.0`) |
| Rocq/Coq 9 + Interval | Coq transcendental native | Optional on portable machines |
| Isabelle | Isabelle scalar + spine | Optional |
| Rust + cargo | Obligation replay, hardware kernel | Optional for full multiprover |
| QEMU | Bare-metal disk path | Optional |
| ESP32 COM port | Hardware UART | Optional; not a math gap if skipped |

---

## Path A — Minimal empirical (laptop, ~10–20 min)

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt

python scripts/build_repo_status_snapshot.py
python scripts/audit_all_benchmark_margins.py
python scripts/audit_parameter_count.py
```

**Expect:**

- `docs/CURRENT_STATUS.md`: pin **D1D38A**, green **N/N** fail 0 (N is live; do not hard-code from memory)  
- `data/benchmark_margin_audit.json`: `green_gate_fail_count == 0`  
- Parameter audit: **ZERO_FREE**

Optional spot-check:

```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
```

---

## Path B — Publication verification bundle (~8–30 min)

```bash
python scripts/run_publication_verification_bundle.py
```

Regenerates contested closures, figures, and claims manifest from on-disk benchmarks (no bulk live download required for the portable path).

**Expect:** bundle completes without hard failures.  
Add `--full-cross-proof` only if multiprover toolchains are installed.

Outputs (representative):

- `data/publication_claims_manifest.json`  
- `data/publication_spine_walkthrough.json`  
- `data/figures/` (when figure scripts succeed)

---

## Path C — Full multiprover (~tens of minutes to hours)

```bash
python scripts/run_cross_proof_verification.py
```

**Expect when toolchains present:**

- `data/cross_proof_verification_report.json` → `overall_ok: true`  
- `github_ready: true` when CI-class gates pass  

**Honesty:** multiprover re-checks **exported residual gates and identities**, not a re-proof of every laboratory catalog from raw bytes. See [`VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`](VERIFICATION_HONESTY_AND_ISABELLE_MATH.md).

Lean-only sample:

```bash
lake exe cache get
lake build FSOT.Formal.Scalar FSOT.Formal.Bounds
```

---

## Path D — Hardware / OS stack (optional)

```bash
python scripts/verify_trinary_os.py
python scripts/run_fsot_hardware_bare_metal.py
python scripts/build_neuron_zig_os_path_panel.py
```

Roadmap prose: [`NEURON_ZIG_TO_OS_ROADMAP.md`](NEURON_ZIG_TO_OS_ROADMAP.md).  
This is **not** a claim that a full multi-user OS ships in-tree.

---

## Falsification (kill criteria)

1. Green-gate failure on a clean clone (no local patches).  
2. `overall_ok: false` with all listed provers installed.  
3. Authority pin no longer D1D38A without a documented pin migration.  
4. Parameter audit finds per-observable least-squares free parameters.  
5. Preregistered PRED rows violated under locked freeze rules.

---

## What we do **not** require for basic trust

- Physical Archive bulk store (~tens of GB) — portable path uses `vendor/` caches  
- ESP32 on the desk — deferred convenience, not a math gap  
- Cloning third-party theory repos — FSOT is self-contained under D1D38A  

---

## Cite these artifacts

| Artifact | Role |
|----------|------|
| `docs/CURRENT_STATUS.md` | Live pin / green / multiprover snapshot |
| `data/benchmark_margin_audit.json` | Empirical green ledger |
| `data/cross_proof_verification_report.json` | Multiprover |
| `data/toe_gap_closure_report.json` | Label A / B |
| **`docs/BENCHMARK_DATA_CITATIONS.md`** | **Public datasets / APIs / literature for every green panel** |
| `data/benchmark_anchor_citation_ledger.json` | Machine citation ledger |
| `data/domain_citations/benchmark_public_anchors.bib` | BibTeX public anchors |
| `data/api_requirements.yaml` | Live API rebuild registry |
| `docs/FSOT_MATH_KEY.md` | Mathematical key |
| `vendor/fsot_compute.py` | Executable authority |

### Public anchors (how to re-fetch measured targets)

```powershell
python scripts/build_benchmark_anchor_citation_ledger.py
# Human table:
#   docs/BENCHMARK_DATA_CITATIONS.md
# Full catalog example: MPCORB → Harvard/CfA MPC (one dataset cite)
# Individual literature rows: listed per panel in the ledger
# APIs: data/api_requirements.yaml + open_science_sources_lib.py
```

---

## Document hygiene after any change

```bash
python scripts/build_repo_status_snapshot.py
python scripts/build_fsot_math_key_onepager.py
python scripts/build_skeptic_replication_kit.py
python scripts/audit_all_benchmark_margins.py
```

See [`DOCUMENTATION_MAP.md`](DOCUMENTATION_MAP.md) and [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md).
