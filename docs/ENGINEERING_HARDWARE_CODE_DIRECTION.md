# Engineering, hardware, code — direction note

**Date:** 2026-08-03  
**Status:** active build path (Living FSOT hardware + VL-agent distill **parked**)

---

## What we are building toward

1. **Circuit / ESP32 engineering** — absolute rails (3.3 V, current, clocks, pull-ups, RC, LDO/buck) so BOM and bring-up are seed-grounded, not wall-banging.
2. **Coding structure verifier** — same *class* of panel as linguistics / Protofluid / code-genome: structure, parity, genome stats — **not** importing transformer weights into the seed spine.
3. **Neuron-zig → OS path** — fixed-lattice mind ([fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig)) under D1D38A, sitting on **trinary FSOTB ABI** (`vendor/trinary_os/`) + QEMU bare metal + hardware laws. Roadmap: [`NEURON_ZIG_TO_OS_ROADMAP.md`](NEURON_ZIG_TO_OS_ROADMAP.md) · panel: `python scripts/build_neuron_zig_os_path_panel.py`. Not a Unix clone claim — OS-class runtime direction.
4. **FSOT-GPU CUDA system** — same pattern as your Desktop FSOT-GPU lab: own collapse θ / coherence gate / consensus (no softmax exp) / sparse active-key CUDA vs industry dense-SDPA, multi-lang parity, FSOT 2.1 verify bridge. Residual-gated into Lean as competitive + parity panels — **operators and seeds**, not weight import.
5. **Processor function + RAM function** — map silicon work and memory as FSOT law (not opaque FLOPS/allocator bags): warp/pack (32 trits/u64), collapse work \(W=H\cdot S\cdot A\cdot D\), VRAM crystal sectors, usable capacity \(C_\mathrm{eff}\cdot\) formal boundary.
6. **Cache hierarchy + interconnect** — line/trit packing, L1&lt;L2&lt;L3 order, working-set \(A_\mathrm{frac}\le\phi^{-4}\); bus “who may speak” = coherence gate (same connective law as attention).
7. **Thin C pack parity** — optional portable evidence (`verification/c/fsot_pack_parity/`); not theory authority.

---

## Parked / redirected

| Old panel | Status | Redirect |
|-----------|--------|----------|
| Living FSOT hardware | Parked | **fsot-neuron-zig** (running mind + Lean stamps) |
| VL agent distill | Parked | LLM architecture is free-param opposite of seed-closed FSOT |

---

## LLM architecture — honest cognitive map

Large language models are **large free-parameter function approximators**. FSOT’s core law is **zero free fit parameters** on the seed spine.

That is a real architectural opposition, not a temporary bug:

| | FSOT seed spine | Autoregressive LLM |
|--|-----------------|---------------------|
| Parameters | Closed seeds (π,e,φ,…) | 10⁹–10¹² fitted weights |
| Goal | Derive / residual-gate | Fit next-token distribution |
| Failure mode | Wrong *comparison object* | Shortcut / hallucination / brittleness |

### Approaches that stay honest

1. **Do not absorb weights into the seed spine.** That would break the zero-free-param claim.
2. **Optional secondary “potential / interface” layer** (your idea): connective tissue *between* systems — routing, attention *gates*, or interface indices derived from multi-sector coupling — **not** a replacement for seeds. Weights live only in that secondary layer, clearly labeled.
3. **Use FSOT where it is native:** verify structure of *code*, languages, hardware rails, biology (neuron-zig), and *steer* tools with seed metrics — without claiming the LLM *is* FSOT.
4. **Code verifier path** already half-built: `fsot code language` multi-lang parity, Protofluid densify exact rates, Tier I programming laws + OSS code-genome.

### What “solving LLM problems” might mean without free params in the core

- Seed-derived **kill criteria** for when a generation is out of band  
- **Structure** of token/operator maps (you already have language operator maps)  
- **Hardware** that runs fixed-point / trinary / Zig minds (neuron-zig), not GPU weight farms  
- Interface layer for *routing* among tools — potential between systems, not a third Yukawa fit

---

## Commands

```powershell
python scripts/build_fsot_gpu_cuda_bridge.py
python scripts/build_engineering_code_bridge.py
python scripts/gen_fsot_gpu_cuda_bridge_lean.py
python scripts/gen_engineering_code_bridge_lean.py
python scripts/audit_all_benchmark_margins.py
# same multiprover path as the rest of the theory:
python scripts/export_scientific_catalog_obligations.py
python scripts/generate_scientific_catalog_artifacts.py
python scripts/run_smt_catalog_bounds.py
# full seven-way (when you want the whole report):
# python scripts/run_cross_proof_verification.py
```

GPU-only (when Desktop FSOT-GPU ledgers are present):

```powershell
python scripts/build_fsot_gpu_cuda_bridge.py
python scripts/gen_fsot_gpu_cuda_bridge_lean.py
```

## Cross-verification (same system as the rest of FSOT)

These panels are **not** a side ledger. They enter the standard pipeline:

| Step | Artifact |
|------|----------|
| Residual benches | `data/*_benchmark.json` |
| Margin audit (green ≤0.5%) | `data/benchmark_margin_audit.json` |
| Scientific catalog obligations | `verification/obligations/scientific_catalog_spine.json` |
| Coq / Isabelle / Lean re-proof | `ScientificCatalogSpine_*` + `FSOT/Formal/*Priors.lean` |
| SMT bulk residual bounds | `python scripts/run_smt_catalog_bounds.py` |
| Full multi-prover report | `python scripts/run_cross_proof_verification.py` → `data/cross_proof_verification_report.json` |

Lean prior modules (0.5% gate):  
`FsotGpuCudaCompetitivePanelPriors`, `FsotGpuParityVerifyPanelPriors`,  
`FsotProcessorFunctionPanelPriors`, `FsotRamFunctionPanelPriors`,  
`FsotGpuEngineeringSpinePriors`, `Esp32PlatformEngineeringPanelPriors`,  
`CodingStructureVerifierPanelPriors`, `EngineeringHardwareCodeSpinePriors`.

### Bare-metal (Rust + QEMU) — hardware must execute

Processor/RAM are not JSON-only. Executable path:

| Layer | Artifact |
|-------|----------|
| no_std / host Rust laws | `verification/rust/fsot_hardware_kernel/` |
| Host serial markers `FSOT_HW_*` | `cargo run --bin fsot_hardware_serial` |
| QEMU disk kernel | `vendor/rust_lean_bridge` + `verification/qemu/fsot-kernel-bios.bin` |
| Harness report | `python scripts/run_fsot_hardware_bare_metal.py` → `data/fsot_hardware_bare_metal_report.json` |

```powershell
python scripts/build_rust_lean_bridge_bootimage.py   # after kernel source changes
python scripts/run_fsot_hardware_bare_metal.py
lake build FSOT.Formal.FsotProcessorFunctionPanelPriors FSOT.Formal.FsotRamFunctionPanelPriors
python scripts/run_cross_proof_verification.py
```

---

## FSOT-GPU pattern (what the CUDA system already does)

Your FSOT-GPU repo (`Desktop\gpu exparment for lean coq isabell andf star`) is the silicon twin of the theory hub:

| Layer | GPU repo | Lean bridge |
|-------|----------|-------------|
| Seeds / collapse θ = `C_eff·P_var` | `fsot_lib/seeds.py`, golden, beat_cuda | residual vs `vendor/fsot_compute` |
| Formal contracts | Lean/Coq/Isabelle/F\* trinary + GpuMemory | device-file + parity layer gates |
| CUDA kernels | sparse consensus, beat_cuda, attn DLL | competitive win-fraction process gates |
| Industry host | SmolLM2 pure-FSOT attention (optional) | **not** absorbed into seed spine |
| Verify | `industry_lm/fsot21_verify.py` PASS | parity/verify panel |

**Claim class:** beat industry *CUDA algorithm stack* with FSOT structure (A ≪ S), not “import free-param weights as physics.”

Panels:

- `data/fsot_gpu_cuda_competitive_panel_benchmark.json`
- `data/fsot_gpu_parity_verify_panel_benchmark.json`
- `data/fsot_processor_function_panel_benchmark.json` — warp, collapse work, SM class, host CPU
- `data/fsot_ram_function_panel_benchmark.json` — packing density, crystal sectors, VRAM usable, host RAM
- `data/fsot_gpu_engineering_spine_benchmark.json` (GPU + processor/RAM + ESP32 + coding rollup)

### Processor function (closed form)

```
F_proc(x) = residual( consensus( active_keys after collapse(θ=C_eff·P_var), gate=½, no_exp ) )
W = H·S·A·D    with A = |active| ≪ S
warp = states_per_u64 = 64/2 = 32
```

### RAM function (closed form)

```
pack: trit → 2 bits → 32 states / u64  (×4 denser than u8)
sectors: header | boot | trinary | Φ | LTM | interop
usable_mib = C_eff · formal_crystal_boundary_mib   (RTX 5070 formal 12800 MiB)
fits(alloc) ⇔ alloc ≤ formal_boundary
```

---

## External paths referenced

- `I:\fsot-neuron-zig` — live bio mind + Lean wet-lab certificate  
- `I:\Protofluid-Language-Translator-2.0-Zig` — multi-lang densify ship baseline  
- `Desktop\fsot code language` — multi-implementation FSOT language parity  
- `Desktop\gpu exparment for lean coq isabell andf star` — **FSOT-GPU** (CUDA consensus stack)  
- `verification/esp32/fsot_esp32_observer` — existing ESP32 Rust observer firmware  
