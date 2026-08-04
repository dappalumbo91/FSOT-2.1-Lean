//! Host serial harness for processor/RAM hardware functions.
//! Prints FSOT_HW_* markers for parity with Lean residual panels and QEMU path.

use fsot_hardware_kernel::{
    active_work_ceiling, run_hardware_gates, sm_count_phi8_plus_1, sm_count_trinary_times_16,
    vram_usable_mib, C_EFF, COLLAPSE_THETA, CRYSTAL_SECTOR_COUNT, DENSITY_GAIN_VS_U8,
    FORMAL_VRAM_BOUNDARY_MIB, MEAN_A_FRAC_BEAT_CUDA, MEASURED_VRAM_MIB_RTX5070, STATES_PER_U64,
    WARP_SIZE,
};

fn main() {
    println!("FSOT Hardware Kernel — Processor + RAM (seed-closed)");
    println!("Fluid Spacetime Omni-Theory | host serial / bare-metal parity");
    println!();

    let g = run_hardware_gates();

    println!("Processor function:");
    println!("  collapse_theta = C_eff·P_var = {:.17}", g.collapse_theta);
    println!("  warp_size = states_per_u64 = {}", g.states_per_u64);
    println!("  sm_trinary_times_16 = {}", sm_count_trinary_times_16());
    println!("  sm_phi8_plus_1 = {:.6}", sm_count_phi8_plus_1());
    println!(
        "  mean_A_frac = {:.6} ≤ φ⁻⁴ = {:.6} → {}",
        MEAN_A_FRAC_BEAT_CUDA,
        active_work_ceiling(),
        if g.active_frac_under_ceiling {
            "PASS"
        } else {
            "FAIL"
        }
    );
    println!();
    println!("RAM function:");
    println!(
        "  usable_mib = C_eff·{} = {:.6} (measured {:.2}, err {:.6}%)",
        FORMAL_VRAM_BOUNDARY_MIB, g.vram_usable_mib, MEASURED_VRAM_MIB_RTX5070, g.vram_usable_err_pct
    );
    println!(
        "  density_gain_vs_u8 = {}  sectors = {}  pack_ok = {}",
        g.density_gain, g.sector_count, g.pack_roundtrip_ok
    );
    println!();
    if g.overall_ok {
        println!("Interpretation: POSITIVE (Hardware gates green) — processor/RAM laws hold.");
    } else {
        println!("Interpretation: FAIL — hardware residual gate exceeded.");
    }
    println!();

    // Machine-readable markers (Tier 91 hardware extension)
    println!("FSOT_HW_COLLAPSE_THETA={:.17}", COLLAPSE_THETA);
    println!("FSOT_HW_C_EFF={:.17}", C_EFF);
    println!("FSOT_HW_STATES_PER_U64={}", STATES_PER_U64);
    println!("FSOT_HW_WARP_SIZE={}", WARP_SIZE);
    println!("FSOT_HW_VRAM_USABLE_MIB={:.17}", vram_usable_mib(FORMAL_VRAM_BOUNDARY_MIB));
    println!("FSOT_HW_VRAM_MEASURED_MIB={:.17}", MEASURED_VRAM_MIB_RTX5070);
    println!("FSOT_HW_VRAM_ERR_PCT={:.17}", g.vram_usable_err_pct);
    println!("FSOT_HW_SM_COUNT={}", sm_count_trinary_times_16());
    println!("FSOT_HW_DENSITY_GAIN={}", DENSITY_GAIN_VS_U8);
    println!("FSOT_HW_SECTORS={}", CRYSTAL_SECTOR_COUNT);
    println!("FSOT_HW_PACK_WORD={}", g.pack_word);
    println!(
        "FSOT_HW_OVERALL={}",
        if g.overall_ok { "ok" } else { "fail" }
    );

    if !g.overall_ok {
        std::process::exit(1);
    }
}
