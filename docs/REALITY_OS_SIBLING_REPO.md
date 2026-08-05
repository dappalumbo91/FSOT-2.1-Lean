# Reality OS sibling repository

The **standalone Reality OS** lives in a separate project so it can become a real operating system without carrying the full multiprover atlas.

| | |
|--|--|
| **GitHub** | https://github.com/dappalumbo91/FSOT-Reality-OS |
| **Sibling path (local)** | `C:\Users\damia\Desktop\FSOT-Reality-OS` |
| **Role** | **Real OS:** Rust `no_std` kernel + QEMU in `kernel/` (v0.1 booting) |
| **This monorepo** | Formula authority, residual atlas, multiprover, reference crates |

**Sibling Reality OS (independent kernel tree):**

| Component | Path in FSOT-Reality-OS |
|-----------|-------------------------|
| Scalar lib | `kernel/crates/reality_os_scalar` |
| Hardware lib | `kernel/crates/reality_os_hw` |
| Kernel binary | `kernel/crates/reality_os_kernel` |
| Boot image | `data/reality_os_kernel.img` |
| Build | `cd kernel && cargo bootimage -p reality_os_kernel --release` |

Reference implementations in this monorepo (`verification/rust/*`, `vendor/rust_lean_bridge`) remain the multiprover hardware path.  
**Python residual CLI is not the OS** in either tree.
