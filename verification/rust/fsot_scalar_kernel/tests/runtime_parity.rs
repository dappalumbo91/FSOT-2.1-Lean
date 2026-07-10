//! Tier 85 runtime parity — bare-metal kernel boot scenario + dynamic spot checks.

use fsot_scalar_kernel::{
    boot_scalar, compute_fsot_scalar, BOOT_DELTA_PSI, BOOT_D_EFF, BOOT_OBSERVED, BOOT_RECENT_HITS,
    BOOT_SCALAR, K,
};
#[test]
fn boot_scalar_matches_canonical() {
    let s = boot_scalar();
    assert!(
        (s - BOOT_SCALAR).abs() < 1e-14,
        "boot scalar {s} != canonical {BOOT_SCALAR}"
    );
    assert!(s > 0.0, "boot scalar must be positive (emergence)");
}

#[test]
fn boot_constants_match_summary() {
    assert_eq!(BOOT_D_EFF, 8.0);
    assert!((BOOT_DELTA_PSI - 0.7).abs() < 1e-14);
    assert!(BOOT_OBSERVED);
    assert_eq!(BOOT_RECENT_HITS, 0.0);
}

#[test]
fn k_matches_atlas() {
    assert!((K - 0.4202216641606967).abs() < 1e-15);
}

#[test]
fn dynamic_phase_spot_checks() {
    let d_eff = BOOT_D_EFF;
    let observed = BOOT_OBSERVED;
    let delta_psi = BOOT_DELTA_PSI;
    for phase_n in [0, 5, 10, 15, 19] {
        let phase = (phase_n as f64) * 0.05;
        let dynamic_delta_psi = delta_psi + 0.3 * phase.sin();
        let dynamic_hits = (phase * 0.1).abs().min(2.0);
        let s = compute_fsot_scalar(d_eff, dynamic_delta_psi, observed, dynamic_hits);
        assert!(s.is_finite(), "dynamic scalar must be finite at phase_n={phase_n}");
    }
}