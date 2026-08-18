# START HERE — FSOT-2.1-Lean

**Who this is for:** anyone opening the repo for the first time (human or AI).  
**Authority pin:** `vendor/fsot_compute.py` → **D1D38A** (zero free fit parameters).  
**Live status:** [`CURRENT_STATUS.md`](CURRENT_STATUS.md) (regenerate with `python scripts/build_repo_status_snapshot.py`).

---

## What this repository is

One seed-derived scalar law

\[
S = K\,(T_1 + T_2 + T_3)
\]

with **preregistered domain routes** (not per-row least squares), residual-gated across a multi-domain atlas (green if pooled median error ≤ **0.5%**), and cross-checked by an independent multiprover gauntlet (Lean master + Coq / Isabelle / F\* / Rust / SMT / TLA+ + hardware harnesses).

It is the **public formal face** of FSOT. Related embodiments (Zig mind, neural monorepo, GPU operators) share the same pin — see [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md).

---

## Pick your audience first

Full map: [`DOCUMENTATION_MAP.md`](DOCUMENTATION_MAP.md)

| You are… | Start with |
|----------|------------|
| Curious lay reader | [`FSOT_EXPLAINED_LAYMAN.md`](FSOT_EXPLAINED_LAYMAN.md) |
| Working scientist / engineer | [`FSOT_MATH_KEY_ONEPAGER.md`](FSOT_MATH_KEY_ONEPAGER.md) → [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) |
| PhD / formal methods | Math key §14 + [`VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`](VERIFICATION_HONESTY_AND_ISABELLE_MATH.md) |
| Here to break it | [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md) · [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |

## 10-minute path (any technical reader)

| Step | Do this | Why |
|------|---------|-----|
| 1 | Open [`CURRENT_STATUS.md`](CURRENT_STATUS.md) | Live pin, green count, multiprover |
| 2 | Read [`FSOT_MATH_KEY_ONEPAGER.md`](FSOT_MATH_KEY_ONEPAGER.md) | Seeds + scalar in one page |
| 3 | Skim [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md) | What we may claim (Label A vs B) |
| 4 | Run `python scripts/audit_all_benchmark_margins.py` | Empirical green gate |
| 5 | Optional formal: `python scripts/run_cross_proof_verification.py` | Multi-prover report (long) |
| 6 | Atlas: `python scripts/query_fsot_atlas.py --stats` | Organized inventory of all green solves |

Human reproduction guide: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).  
**Open science only (no keys):** [`OPEN_SCIENCE_ONLY_POLICY.md`](OPEN_SCIENCE_ONLY_POLICY.md) · Atlas design: [`ATLAS_DATABASE_DESIGN.md`](ATLAS_DATABASE_DESIGN.md)

---

## Map of the repo (not a mystery tour)

| Area | Path | Role |
|------|------|------|
| Scalar authority | `vendor/fsot_compute.py` | Executable law + pin |
| Lean formal | `FSOT/Formal/` | Master integrator |
| Multiprover | `verification/{coq,isabelle,fstar,rust,smt,tla,qemu,esp32}/` | Independent residual / structure checks |
| Domain data | `data/*_benchmark.json` | Residual panels |
| Predictions (frozen) | `predictions/` | Timestamped / SHA-locked forecasts |
| Results (outcomes) | `results/` | Literature + API outcomes after data lands |
| Docs | `docs/` | Human claims and runbooks |
| Hardware / OS path | this file § Machine stack + [`NEURON_ZIG_TO_OS_ROADMAP.md`](NEURON_ZIG_TO_OS_ROADMAP.md) | Embodiment → OS |

---

## Machine stack (where expansion is going)

Order of embodiment (honest — not all are “done OS”):

1. **Scalar kernel (Rust)** — `verification/rust/fsot_scalar_kernel/`  
2. **Hardware laws (pack, cache, interconnect)** — `verification/rust/fsot_hardware_kernel/` + panels in `data/fsot_*`  
3. **Bare metal / QEMU** — `verification/qemu/`, `python scripts/run_fsot_hardware_bare_metal.py`  
4. **Trinary OS ABI (FSOTB)** — `vendor/trinary_os/` (opcodes, call/ret, spawn/join oracles)  
5. **Neuron-zig mind** — sibling repo [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) (fixed-lattice neural engine under D1D38A)  
6. **Target:** mind + trinary ISA + scheduler/syscalls → **FSOT-native OS-class runtime** (roadmap doc)

Engineering direction: [`ENGINEERING_HARDWARE_CODE_DIRECTION.md`](ENGINEERING_HARDWARE_CODE_DIRECTION.md).

---

## Documentation debt (we own this)

Other open programs sometimes **write more clearly** than we do. That does not change math residual or pin integrity. It **does** mean we should keep improving:

- entry docs (this file)  
- claim boundaries and honesty ledgers  
- hardware / OS roadmap prose  
- fewer “only the author knows where X lives” gaps  

Prefer **complete sentences and named artifacts** over slogans.

---

## Commands cheat sheet

```powershell
# Status
python scripts/build_repo_status_snapshot.py

# Empirical green
python scripts/audit_all_benchmark_margins.py

# Hardware bare metal
python scripts/run_fsot_hardware_bare_metal.py

# Trinary OS oracles
python scripts/verify_trinary_os.py
python scripts/build_trinary_os_isa_rebuild_benchmark.py

# Neuron → OS residual panel
python scripts/build_neuron_zig_os_path_panel.py

# Proper densify only (formula + real measured)
# see docs/FSOT_PROPER_DENSIFY_POLICY.md
```

---

## Do / don’t

| Do | Don’t |
|----|--------|
| Cite pin D1D38A and green ≤0.5% | Invent free-fit constants |
| Use proper densify (formula + real data) | Seed-identity / process densify padding |
| Keep multiprover and empirical gates separate | Treat one green JSON as “proved physics” |
| Improve our own docs and hardware | Hijack or “fix” someone else’s open theory repo |
