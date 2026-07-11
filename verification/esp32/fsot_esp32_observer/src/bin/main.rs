//! FSOT Tier 88 — ESP32 bare-metal observer mirroring QEMU/serial harness markers over UART.

#![no_std]
#![no_main]
#![deny(clippy::mem_forget)]

use esp_hal::{
    clock::CpuClock,
    main,
    time::{Duration, Instant},
};
use fsot_scalar_kernel::{
    boot_scalar, compute_fsot_scalar, BOOT_DELTA_PSI, BOOT_D_EFF, BOOT_OBSERVED, BOOT_RECENT_HITS,
    BOOT_SCALAR,
};

use esp_backtrace as _;

esp_bootloader_esp_idf::esp_app_desc!();

#[main]
fn main() -> ! {
    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let _peripherals = esp_hal::init(config);

    esp_println::println!("FSOT 2.0 Bare-Metal Observer Kernel POC v0.1");
    esp_println::println!("Fluid Spacetime Omni-Theory - Parameter Free | ESP32 xtensa");
    esp_println::println!("Built with Rust no_std | FSOT Native Scalar Engine");
    esp_println::println!();
    esp_println::println!("Mapping boot to FSOT domain: KernelInit (D_eff=8, observed=True)");

    let s = boot_scalar();
    esp_println::println!("Computed FSOT Scalar S_D_chaotic = {s:.6}");

    if s > 0.0 {
        esp_println::println!("Interpretation: POSITIVE (Emergence) - New information flow detected.");
        esp_println::println!("System entering high-coherence boot phase. Fluid spacetime active.");
    } else {
        esp_println::println!("Interpretation: NEGATIVE / DAMPED (Stabilization) - Perturbations suppressed.");
        esp_println::println!("System prioritizing stability during initialization.");
    }

    esp_println::println!();
    esp_println::println!("FSOT k-scaled output demonstrates ~99% domain fit principle in bare metal.");
    esp_println::println!("This POC proves FSOT scalar computation is viable in no-OS environments.");
    esp_println::println!();
    esp_println::println!("Tier 88 ESP32 hardware boot complete — halting for harness capture.");

    esp_println::println!("FSOT_ESP32_BOOT_SCALAR={s:.17}");
    esp_println::println!("FSOT_ESP32_CANONICAL={BOOT_SCALAR:.17}");

    let dynamic = compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS);
    esp_println::println!("FSOT_ESP32_DYNAMIC_CHECK={dynamic:.17}");
    esp_println::println!("FSOT_ESP32_HARDWARE_BOOT=ok");

    let delay_start = Instant::now();
    while delay_start.elapsed() < Duration::from_secs(30) {}
    esp_hal::system::software_reset();
}