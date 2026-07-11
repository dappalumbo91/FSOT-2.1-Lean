//! Tier 89–93 — RF/sensor observer mapping into FSOT scalar + trinary collapse.

use fsot_scalar_kernel::{
    compute_fsot_scalar, BOOT_D_EFF, BOOT_DELTA_PSI, C_EFF, P_VAR,
};

use crate::ble_scan::BleHit;
use crate::csi::CsiSnapshot;

pub const COLLAPSE_THRESHOLD: f64 = C_EFF * P_VAR;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TrinaryState {
    Emergence,
    Stability,
    Damping,
}

impl TrinaryState {
    pub fn as_i8(self) -> i8 {
        match self {
            TrinaryState::Emergence => 1,
            TrinaryState::Stability => 0,
            TrinaryState::Damping => -1,
        }
    }

    pub fn label(self) -> &'static str {
        match self {
            TrinaryState::Emergence => "+1",
            TrinaryState::Stability => "0",
            TrinaryState::Damping => "-1",
        }
    }
}

#[derive(Debug, Clone, Copy, Default)]
pub struct ObserverSnapshot {
    pub ap_count: u32,
    pub rssi_mean: f64,
    pub rssi_var: f64,
    pub temp_c: f32,
    pub ble_stack_ok: bool,
}

impl ObserverSnapshot {
    pub fn from_wifi_aps(aps: &[impl ApRssi], temp_c: f32, ble_stack_ok: bool) -> Self {
        let ap_count = aps.len() as u32;
        if ap_count == 0 {
            return Self {
                ap_count: 0,
                rssi_mean: 0.0,
                rssi_var: 0.0,
                temp_c,
                ble_stack_ok,
            };
        }
        let mut sum = 0.0_f64;
        for ap in aps {
            sum += ap.rssi() as f64;
        }
        let mean = sum / ap_count as f64;
        let mut var = 0.0_f64;
        for ap in aps {
            let d = ap.rssi() as f64 - mean;
            var += d * d;
        }
        var /= ap_count as f64;
        Self {
            ap_count,
            rssi_mean: mean,
            rssi_var: var,
            temp_c,
            ble_stack_ok,
        }
    }

    pub fn scalar_inputs(&self) -> (f64, f64, bool, f64) {
        let delta_psi = BOOT_DELTA_PSI
            + (self.temp_c as f64 - 25.0) * 0.01
            + self.rssi_var * 0.0001
            + (self.ap_count as f64) * 0.002;
        let recent_hits = (self.ap_count.min(8) as f64)
            + if self.ble_stack_ok { 1.0 } else { 0.0 };
        let observed = self.ap_count > 0 || self.ble_stack_ok;
        (BOOT_D_EFF, delta_psi, observed, recent_hits)
    }

    pub fn rf_scalar(&self) -> f64 {
        let (d, dp, obs, hits) = self.scalar_inputs();
        compute_fsot_scalar(d, dp, obs, hits)
    }
}

pub trait ApRssi {
    fn rssi(&self) -> i8;
}

#[derive(Debug, Clone, Copy, Default)]
pub struct FluidSonarSnapshot {
    pub wifi: ObserverSnapshot,
    pub csi: CsiSnapshot,
    pub ble_count: u32,
    pub ble_rssi_mean: f64,
    pub ble_rssi_var: f64,
}

impl FluidSonarSnapshot {
    pub fn from_layers(
        wifi: ObserverSnapshot,
        csi: CsiSnapshot,
        ble_hits: &[BleHit],
    ) -> Self {
        let ble_count = ble_hits.len() as u32;
        let (ble_rssi_mean, ble_rssi_var) = if ble_count == 0 {
            (0.0, 0.0)
        } else {
            let mut sum = 0.0_f64;
            for hit in ble_hits {
                sum += hit.rssi as f64;
            }
            let mean = sum / ble_count as f64;
            let mut var = 0.0_f64;
            for hit in ble_hits {
                let d = hit.rssi as f64 - mean;
                var += d * d;
            }
            var /= ble_count as f64;
            (mean, var)
        };
        Self {
            wifi,
            csi,
            ble_count,
            ble_rssi_mean,
            ble_rssi_var,
        }
    }

    pub fn fluid_scalar(&self) -> f64 {
        let (d, mut dp, mut observed, mut hits) = self.wifi.scalar_inputs();
        dp += self.csi.amp_var_mean * 0.00005;
        dp += self.ble_rssi_var * 0.00008;
        dp += (self.csi.packets as f64) * 0.0002;
        hits += self.ble_count.min(8) as f64;
        hits += (self.csi.packets.min(32) as f64) * 0.15;
        observed |= self.csi.packets > 0 || self.ble_count > 0;
        compute_fsot_scalar(d, dp, observed, hits)
    }

    pub fn rf_scalar(&self) -> f64 {
        self.wifi.rf_scalar()
    }
}

pub fn trinary_collapse(s: f64) -> TrinaryState {
    if s.abs() < COLLAPSE_THRESHOLD {
        TrinaryState::Stability
    } else if s > 0.0 {
        TrinaryState::Emergence
    } else {
        TrinaryState::Damping
    }
}

pub fn pack_enow_payload(boot_scalar: f64, rf_scalar: f64, trinary: TrinaryState) -> [u8; 12] {
    let mut out = [0u8; 12];
    out[0] = 0xF5;
    out[1] = 0x07;
    out[2] = trinary.as_i8() as u8;
    out[3] = 0;
    out[4..8].copy_from_slice(&(boot_scalar as f32).to_le_bytes());
    out[8..12].copy_from_slice(&(rf_scalar as f32).to_le_bytes());
    out
}