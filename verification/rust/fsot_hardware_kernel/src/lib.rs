//! FSOT processor + RAM hardware functions (seed-closed).
//!
//! Portable between host `std` tests and `no_std` bare-metal kernels.
//! Mirrors Desktop FSOT-GPU + Lean residual panels:
//!   collapse θ = C_eff · P_var
//!   warp / pack = 32 trits per u64 (2 bits each)
//!   usable VRAM = C_eff · formal crystal boundary
//!   work law W = H·S·A·D with A ≪ S

#![cfg_attr(not(feature = "std"), no_std)]

/// Archive seeds (vendor/fsot_compute / fsot_scalar_kernel).
pub const C_EFF: f64 = 0.9577022026205613;
pub const P_VAR: f64 = 0.9579871226722757;
pub const PHI: f64 = 1.618033988749895;
pub const PSI_CON: f64 = 0.6321205588285577;
pub const K: f64 = 0.4202216641606967;

/// Collapse threshold θ = C_eff · P_var (measurement law).
pub const COLLAPSE_THETA: f64 = C_EFF * P_VAR; // 0.9174663774653723

/// Coherence gate half-plane.
pub const COHERENCE_GATE: f64 = 0.5;

/// Trinary packing: 2 bits/state → 32 states / u64 (warp-aligned).
pub const BITS_PER_TRIT: u32 = 2;
pub const WORD_BITS: u32 = 64;
pub const STATES_PER_U64: u32 = WORD_BITS / BITS_PER_TRIT; // 32
pub const WARP_SIZE: u32 = 32;
pub const TRINARY_ARITY: u32 = 3;
pub const DENSITY_GAIN_VS_U8: u32 = 8 / BITS_PER_TRIT; // 4

/// GpuMemory.lean crystal sector count.
pub const CRYSTAL_SECTOR_COUNT: u32 = 6;

/// Formal RTX 5070-class crystal boundary (MiB) from GpuMemory.lean.
pub const FORMAL_VRAM_BOUNDARY_MIB: f64 = 12800.0;

/// Lab probe (RTX 5070) total memory MiB — residual vs C_eff · formal.
pub const MEASURED_VRAM_MIB_RTX5070: f64 = 12226.56;

/// Lab SM count (RTX 5070).
pub const MEASURED_SM_COUNT_RTX5070: u32 = 48;

/// Mean A_frac from beat_cuda suite (process ledger).
pub const MEAN_A_FRAC_BEAT_CUDA: f64 = 0.017955555555555558;

#[inline]
pub fn collapse_theta() -> f64 {
    COLLAPSE_THETA
}

/// φ⁻⁴ active-work ceiling.
#[inline]
pub fn active_work_ceiling() -> f64 {
    // PHI^{-4}
    let inv = 1.0 / PHI;
    inv * inv * inv * inv
}

/// usable_mib = C_eff · formal_crystal_boundary_mib
#[inline]
pub fn vram_usable_mib(formal_boundary_mib: f64) -> f64 {
    C_EFF * formal_boundary_mib
}

/// fits(alloc) ⇔ alloc_bytes ≤ formal_bytes
#[inline]
pub fn vram_fits(alloc_bytes: u64, formal_bytes: u64) -> bool {
    alloc_bytes <= formal_bytes
}

#[inline]
pub fn formal_vram_bytes() -> u64 {
    // 12800 * 1024 * 1024
    (FORMAL_VRAM_BOUNDARY_MIB as u64) * 1024 * 1024
}

/// SM class residual: 3 · 2⁴ (trinary arity × nibble).
#[inline]
pub fn sm_count_trinary_times_16() -> u32 {
    TRINARY_ARITY * 16
}

/// SM class residual: φ⁸ + 1
#[inline]
pub fn sm_count_phi8_plus_1() -> f64 {
    let p2 = PHI * PHI;
    let p4 = p2 * p2;
    let p8 = p4 * p4;
    p8 + 1.0
}

/// Relative residual percent |c - m| / |m| * 100.
#[inline]
pub fn rel_err_pct(computed: f64, measured: f64) -> f64 {
    if measured == 0.0 && computed == 0.0 {
        return 0.0;
    }
    let denom = if measured.abs() > 1e-30 {
        measured.abs()
    } else {
        computed.abs()
    };
    if denom < 1e-30 {
        return if (computed - measured).abs() < 1e-12 {
            0.0
        } else {
            100.0
        };
    }
    (computed - measured).abs() / denom * 100.0
}

/// Pack 32 trit codes (0/1/2) into one u64 (2 bits each, low to high).
pub fn pack_trits32(codes: &[u8; 32]) -> u64 {
    let mut word: u64 = 0;
    for (i, &c) in codes.iter().enumerate() {
        let c = (c % 3) as u64;
        word |= c << (2 * i);
    }
    word
}

/// Unpack 32 trit codes from u64.
pub fn unpack_trits32(word: u64) -> [u8; 32] {
    let mut codes = [0u8; 32];
    for i in 0..32 {
        codes[i] = ((word >> (2 * i)) & 0b11) as u8;
    }
    codes
}

/// Collapse continuous value to trit: -1 / 0 / +1.
#[inline]
pub fn collapse_trit(x: f64, theta: f64) -> i8 {
    if x > theta {
        1
    } else if x < -theta {
        -1
    } else {
        0
    }
}

/// Coherence gate: true if |x| exceeds half-plane after collapse domain.
#[inline]
pub fn coherence_active(coh: f64) -> bool {
    coh > COHERENCE_GATE
}

/// Work efficiency η = speedup · A_frac must be ≤ 1 (theory upper O(S/A)).
#[inline]
pub fn work_efficiency_ok(speedup: f64, a_frac: f64) -> bool {
    speedup * a_frac <= 1.0 + 1e-12
}

/// Full hardware self-check used by host serial harness and unit tests.
#[derive(Clone, Copy, Debug)]
pub struct HardwareGateReport {
    pub collapse_theta: f64,
    pub collapse_theta_err_pct: f64,
    pub states_per_u64: u32,
    pub warp_divides: bool,
    pub pack_roundtrip_ok: bool,
    pub pack_word: u64,
    pub vram_usable_mib: f64,
    pub vram_usable_err_pct: f64,
    pub vram_fits: bool,
    pub sm_trinary_ok: bool,
    pub sm_phi8_err_pct: f64,
    pub active_frac_under_ceiling: bool,
    pub density_gain: u32,
    pub sector_count: u32,
    pub overall_ok: bool,
}

pub fn run_hardware_gates() -> HardwareGateReport {
    let theta = collapse_theta();
    let theta_err = rel_err_pct(theta, 0.9174663774653723);

    let codes: [u8; 32] = {
        let mut c = [0u8; 32];
        for i in 0..32 {
            c[i] = (i % 3) as u8;
        }
        c
    };
    let word = pack_trits32(&codes);
    let back = unpack_trits32(word);
    let pack_ok = back == codes;

    let usable = vram_usable_mib(FORMAL_VRAM_BOUNDARY_MIB);
    let vram_err = rel_err_pct(usable, MEASURED_VRAM_MIB_RTX5070);
    // measured bytes from probe total_memory_bytes ≈ 12820480000
    let measured_bytes: u64 = 12_820_480_000;
    let fits = vram_fits(measured_bytes, formal_vram_bytes());

    let sm_tri = sm_count_trinary_times_16() == MEASURED_SM_COUNT_RTX5070;
    let sm_phi_err = rel_err_pct(sm_count_phi8_plus_1(), MEASURED_SM_COUNT_RTX5070 as f64);

    let ceiling = active_work_ceiling();
    let active_ok = MEAN_A_FRAC_BEAT_CUDA <= ceiling;

    let warp_ok = STATES_PER_U64 % WARP_SIZE == 0 && STATES_PER_U64 == 32;

    let overall = theta_err < 0.5
        && warp_ok
        && pack_ok
        && vram_err < 0.5
        && fits
        && sm_tri
        && sm_phi_err < 0.5
        && active_ok
        && DENSITY_GAIN_VS_U8 == 4
        && CRYSTAL_SECTOR_COUNT == 6;

    HardwareGateReport {
        collapse_theta: theta,
        collapse_theta_err_pct: theta_err,
        states_per_u64: STATES_PER_U64,
        warp_divides: warp_ok,
        pack_roundtrip_ok: pack_ok,
        pack_word: word,
        vram_usable_mib: usable,
        vram_usable_err_pct: vram_err,
        vram_fits: fits,
        sm_trinary_ok: sm_tri,
        sm_phi8_err_pct: sm_phi_err,
        active_frac_under_ceiling: active_ok,
        density_gain: DENSITY_GAIN_VS_U8,
        sector_count: CRYSTAL_SECTOR_COUNT,
        overall_ok: overall,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn collapse_theta_matches_archive() {
        let err = rel_err_pct(collapse_theta(), 0.9174663774653723);
        assert!(err < 1e-9, "theta err {err}");
    }

    #[test]
    fn packing_roundtrip_and_warp() {
        assert_eq!(STATES_PER_U64, 32);
        assert_eq!(STATES_PER_U64 % WARP_SIZE, 0);
        let mut codes = [0u8; 32];
        for i in 0..32 {
            codes[i] = (i % 3) as u8;
        }
        let w = pack_trits32(&codes);
        assert_eq!(unpack_trits32(w), codes);
    }

    #[test]
    fn vram_usable_under_half_pct() {
        let usable = vram_usable_mib(FORMAL_VRAM_BOUNDARY_MIB);
        let err = rel_err_pct(usable, MEASURED_VRAM_MIB_RTX5070);
        assert!(err < 0.5, "vram err {err}% usable={usable}");
        assert!(vram_fits(12_820_480_000, formal_vram_bytes()));
    }

    #[test]
    fn processor_sm_and_active_work() {
        assert_eq!(sm_count_trinary_times_16(), 48);
        let err = rel_err_pct(sm_count_phi8_plus_1(), 48.0);
        assert!(err < 0.5, "sm phi8 err {err}");
        assert!(MEAN_A_FRAC_BEAT_CUDA <= active_work_ceiling());
        assert!(work_efficiency_ok(89.49, 0.0072));
    }

    #[test]
    fn hardware_gates_overall() {
        let r = run_hardware_gates();
        assert!(r.overall_ok, "gates failed: theta_err={} vram_err={} sm_phi={}",
            r.collapse_theta_err_pct, r.vram_usable_err_pct, r.sm_phi8_err_pct);
    }
}
