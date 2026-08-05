# Neuron-zig → FSOT OS-class runtime — roadmap

**Date:** 2026-08-05  
**Status:** active expansion path  
**Pin:** D1D38A on all layers  
**Panel:** [`data/neuron_zig_os_path_panel_benchmark.json`](../data/neuron_zig_os_path_panel_benchmark.json)

---

## Intent

Grow the **machine side** so the Zig neural mind is not a lone binary, but sits inside a **seed-closed runtime** with:

- trinary instruction ABI (FSOTB)  
- tasks / spawn-join  
- syscalls  
- packing / cache / interconnect laws  
- QEMU bare-metal proof of execution  
- residual gates into this Lean hub  

End state (aspirational, not claimed done): an **FSOT-native OS-class environment** where “process,” “mind lattice,” and “scalar law” share one pin.

---

## Layers (bottom → top)

```
Seeds (π,e,φ,γ,G) + compute_scalar          vendor/fsot_compute.py
        ↓
Rust scalar kernel parity                   verification/rust/fsot_scalar_kernel/
        ↓
Hardware laws (pack, θ, cache, bus)         verification/rust/fsot_hardware_kernel/
        ↓
QEMU / bare-metal harness                   verification/qemu/ + run_fsot_hardware_bare_metal.py
        ↓
Trinary OS ABI (FSOTB opcodes)              vendor/trinary_os/  (HALT…JOIN, SYSCALL, SPAWN)
        ↓
Neuron-zig fixed lattice mind               github.com/dappalumbo91/fsot-neuron-zig
        ↓
OS-class services (scheduler, IPC, store)   *next builds — residual-gated as we add them*
```

| Layer | In-repo now | Still open |
|-------|-------------|------------|
| Scalar pin | Yes | Keep pin frozen |
| Pack / trit / cache | Panels + Rust kernel | Deeper competitive benches |
| Trinary ISA v1.0–v1.2 | Oracles hello / call_ret / spawn_join | More programs, richer syscalls |
| Bare metal | QEMU path | ESP32 UART convenience deferred |
| Neuron-zig | Sibling repo under same pin | Tighter hub bridge when disk available |
| Full OS | **Not claimed** | Filesystem, drivers, multi-user — only when residual-gated |

---

## Trinary OS ABI snapshot (vendor truth)

From `vendor/trinary_os/isa/fsotb_opcode_registry.json`:

| ABI | Opcodes | Programs |
|-----|---------|----------|
| v1.0 | 0–19 (HALT…MEASURE) | hello.fsotb |
| v1.1 | 20–24 (+ CALL/RET/PUSH/POP/SYSCALL) | call_ret.fsotb |
| v1.2 | 25–26 (+ SPAWN/JOIN) | spawn_join.fsotb |

Structural constants residual-gated:

- word width **27** trits  
- **25** registers  
- **8** task slots  
- **6** cortical layers (mind-aligned layout hint)  
- instruction size **6** bytes  
- magic `FSOTB\x01`  

Rebuild: `python scripts/build_trinary_os_isa_rebuild_benchmark.py`  
Verify: `python scripts/verify_trinary_os.py`

---

## Neuron-zig role

[fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) is the **neuroscience-domain fixed-lattice mind** under D1D38A — not a free-param LLM.

In the OS path it becomes:

1. a **workload** that the trinary runtime schedules (spawn/join class)  
2. a **scalar client** that must stay pin-identical to this hub  
3. later: a **system service** (sensory / observer loop) on top of FSOTB syscalls  

Hub map: [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md).  
Engineering note: [`ENGINEERING_HARDWARE_CODE_DIRECTION.md`](ENGINEERING_HARDWARE_CODE_DIRECTION.md).

When the local archive path (`I:\fsot-neuron-zig`) is online, prefer live stamp ingest; when offline, residual-gate public ABI + hub panels only.

---

## Near-term expansion checklist

- [x] Document stack + residual panel (`build_neuron_zig_os_path_panel.py`)  
- [x] Keep trinary OS oracles and ISA rebuild green  
- [ ] Expand FSOTB programs (more syscall surface, not vanity opcodes)  
- [ ] Wire neuron-zig CI pin check against hub D1D38A when both repos available  
- [ ] Scheduler residual: task slots × φ-locality (active fraction ≤ φ⁻⁴ class)  
- [ ] Store / VRAM crystal sector laws already in hardware panels — reuse, don’t re-fit  
- [ ] OS “shell” = evaluator of FSOTB + mind panel, not a Unix clone for ego  

---

## Commands

```powershell
python scripts/build_neuron_zig_os_path_panel.py
python scripts/build_trinary_os_isa_rebuild_benchmark.py
python scripts/verify_trinary_os.py
python scripts/run_fsot_hardware_bare_metal.py
python scripts/audit_all_benchmark_margins.py
python scripts/build_repo_status_snapshot.py
```

## Honesty

Calling this an **OS roadmap** is a **direction**, not a claim that a full multi-user operating system ships today.  
Every new layer must enter the green residual gate and the multiprover path like everything else.
