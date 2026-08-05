# Reality OS sibling repository

The **standalone Reality OS** lives in a separate project so it can become a real operating system without carrying the full multiprover atlas.

| | |
|--|--|
| **GitHub** | https://github.com/dappalumbo91/FSOT-Reality-OS |
| **Sibling path (local)** | `C:\Users\damia\Desktop\FSOT-Reality-OS` |
| **Role** | Formula shell (Python) + **must drive monorepo Rust/QEMU OS spine** |
| **This monorepo** | Formula authority, residual atlas, multiprover, **and** the real OS spine |

**OS spine lives here, not in Python:**

| Spine | Path |
|-------|------|
| Scalar kernel | `verification/rust/fsot_scalar_kernel` |
| Hardware kernel | `verification/rust/fsot_hardware_kernel` |
| Boot bridge | `vendor/rust_lean_bridge` |
| QEMU | `verification/qemu` + `scripts/run_rust_lean_bridge_qemu_harness.py` |
| Bare metal runner | `scripts/run_fsot_hardware_bare_metal.py` |
| Reality OS execute | `python scripts/run_fsot_reality_os.py hardware --run` |

Upstream pin and `vendor/fsot_compute.py` remain formula authority.  
Sibling repo runs the same spine via `scripts/run_hardware_spine.py` (env `FSOT_MONOREPO_ROOT`).  
Do **not** scaffold a second Python “kernel.”
