//! Serial harness: mirrors vendor/rust_lean_bridge VGA boot output on stdout for QEMU capture.

use fsot_scalar_kernel::{
    boot_scalar, compute_fsot_scalar, BOOT_DELTA_PSI, BOOT_D_EFF, BOOT_OBSERVED, BOOT_RECENT_HITS,
    BOOT_SCALAR,
};

fn main() {
    println!("FSOT 2.0 Bare-Metal Observer Kernel POC v0.1");
    println!("Fluid Spacetime Omni-Theory - Parameter Free | QEMU x86_64");
    println!("Built with Rust no_std | FSOT Native Scalar Engine");
    println!();
    println!("Mapping boot to FSOT domain: KernelInit (D_eff=8, observed=True)");

    let s = boot_scalar();
    println!("Computed FSOT Scalar S_D_chaotic = {s:.6}");

    if s > 0.0 {
        println!("Interpretation: POSITIVE (Emergence) - New information flow detected.");
        println!("System entering high-coherence boot phase. Fluid spacetime active.");
    } else {
        println!("Interpretation: NEGATIVE / DAMPED (Stabilization) - Perturbations suppressed.");
        println!("System prioritizing stability during initialization.");
    }

    println!();
    println!("FSOT k-scaled output demonstrates ~99% domain fit principle in bare metal.");
    println!("This POC proves FSOT scalar computation is viable in no-OS environments.");
    println!();
    println!("FSOT_SERIAL_BOOT_SCALAR={s:.17}");
    println!("FSOT_SERIAL_CANONICAL={BOOT_SCALAR:.17}");

    // One dynamic spot-check (phase 0) for harness depth.
    let dynamic = compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS);
    println!("FSOT_SERIAL_DYNAMIC_CHECK={dynamic:.17}");
}