//! FSOT Tier 85 — host-runnable port of `vendor/rust_lean_bridge/main.rs` scalar engine.
//! Simplified S_D_chaotic POC (T2 = 0); must stay byte-stable with bare-metal kernel.

// Host std math (mirrors vendor no_std kernel which uses libm::{cos, exp, ln, sin, sqrt}).

pub const K: f64 = 0.4202216641606967;
pub const ALPHA: f64 = 0.0008082937414140405;
pub const PSI_CON: f64 = 0.6321205588285577;
pub const ETA_EFF: f64 = 0.46694220692425986;
pub const BETA: f64 = 2.620866911333223e-17;
pub const C_EFF: f64 = 0.9577022026205613;
pub const A_BLEED: f64 = 1.046973630587551;
pub const B_IN: f64 = 0.7879407922764435;
pub const A_IN: f64 = 1.6668538450045731;
pub const CHAOS: f64 = -0.33102418261048183;
pub const P_NEW: f64 = 0.30030227667037146;
pub const C_FACTOR: f64 = 0.28760015181918397;
pub const POOF: f64 = 0.1534822148944508;
pub const THETA_S: f64 = 0.29089654054517305;
pub const SUCTION: f64 = 0.14703398542810284;
pub const P_VAR: f64 = 0.9579871226722757;

pub const BOOT_D_EFF: f64 = 8.0;
pub const BOOT_DELTA_PSI: f64 = 0.7;
pub const BOOT_RECENT_HITS: f64 = 0.0;
pub const BOOT_OBSERVED: bool = true;
pub const BOOT_SCALAR: f64 = 0.09928895626861721;

const GAMMA_EULER: f64 = 0.5772156649;
const PHI: f64 = 1.6180339887;
const PI: f64 = core::f64::consts::PI;

/// Simplified FSOT scalar (no_std kernel port). T2 fixed at 0 for POC.
pub fn compute_fsot_scalar(d_eff: f64, delta_psi: f64, observed: bool, recent_hits: f64) -> f64 {
    let n = 1.0_f64;
    let p = 1.0_f64;
    let d = d_eff.max(1.0);
    let dp = delta_psi;
    let hits = recent_hits;

    let growth = (ALPHA * (1.0 - hits / n) * GAMMA_EULER / PHI).exp();
    let base = (n * p / d.sqrt())
        * ((PSI_CON + dp) / ETA_EFF).cos()
        * (-ALPHA * hits / n + 1.0 + B_IN * dp).exp()
        * (1.0 + growth * C_EFF);
    let mut t1 = base * (1.0 + P_NEW * (d / 25.0).ln());
    if observed {
        t1 = t1 * (C_FACTOR * P_VAR).exp() * (dp + P_VAR).cos();
    }

    let t2 = 0.0_f64;

    let valve = BETA * dp.cos() * (n * p / d.sqrt())
        * (1.0 + CHAOS * (d - 25.0) / 25.0)
        * (1.0 + POOF * (THETA_S + PI).cos() + SUCTION * THETA_S.sin());
    let acoustic = 1.0
        + (A_BLEED * 1.0_f64.sin().powi(2)) / PHI
        + (A_IN * 1.0_f64.cos().powi(2)) / PHI;
    let phase = 1.0 + B_IN * P_VAR;
    let t3 = valve * acoustic * phase;

    K * (t1 + t2 + t3)
}

pub fn boot_scalar() -> f64 {
    compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS)
}