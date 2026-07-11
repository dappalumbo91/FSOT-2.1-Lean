//! Tier 93 — Wi-Fi CSI multipath density accumulator (Level 2 fluid sensor).

use core::cell::RefCell;

use critical_section::Mutex;

#[derive(Debug, Clone, Copy, Default)]
pub struct CsiSnapshot {
    pub packets: u32,
    pub amp_var_mean: f64,
    pub buf_len_mean: f64,
    pub last_channel: u8,
    pub last_rssi: i8,
}

#[derive(Default)]
struct CsiAccumulator {
    packets: u32,
    sum_amp_var: f64,
    sum_buf_len: f64,
    last_channel: u8,
    last_rssi: i8,
}

static CSI_ACC: Mutex<RefCell<CsiAccumulator>> = Mutex::new(RefCell::new(CsiAccumulator {
    packets: 0,
    sum_amp_var: 0.0,
    sum_buf_len: 0.0,
    last_channel: 0,
    last_rssi: 0,
}));

pub fn reset_csi_window() {
    critical_section::with(|cs| {
        *CSI_ACC.borrow(cs).borrow_mut() = CsiAccumulator::default();
    });
}

pub fn record_csi_buf(buf: &[i8], first_word_invalid: bool, channel: u8, rssi: i8) {
    if buf.is_empty() {
        return;
    }
    let amp_var = subcarrier_amp_variance(buf, first_word_invalid);
    critical_section::with(|cs| {
        let mut acc = CSI_ACC.borrow(cs).borrow_mut();
        acc.packets = acc.packets.saturating_add(1);
        acc.sum_amp_var += amp_var;
        acc.sum_buf_len += buf.len() as f64;
        acc.last_channel = channel;
        acc.last_rssi = rssi;
    });
}

pub fn snapshot_csi_window() -> CsiSnapshot {
    critical_section::with(|cs| {
        let acc = CSI_ACC.borrow(cs).borrow();
        let packets = acc.packets;
        if packets == 0 {
            return CsiSnapshot::default();
        }
        let n = packets as f64;
        CsiSnapshot {
            packets,
            amp_var_mean: acc.sum_amp_var / n,
            buf_len_mean: acc.sum_buf_len / n,
            last_channel: acc.last_channel,
            last_rssi: acc.last_rssi,
        }
    })
}

/// Per-packet variance of subcarrier amplitudes — multipath spread proxy.
pub fn subcarrier_amp_variance(buf: &[i8], first_word_invalid: bool) -> f64 {
    let skip = if first_word_invalid { 4 } else { 0 };
    if buf.len() <= skip + 1 {
        return 0.0;
    }
    let mut amps: [f64; 64] = [0.0; 64];
    let mut count = 0usize;
    let mut i = skip;
    while i + 1 < buf.len() && count < 64 {
        let im = buf[i] as f64;
        let re = buf[i + 1] as f64;
        amps[count] = libm::sqrt(im * im + re * re);
        count += 1;
        i += 2;
    }
    if count == 0 {
        return 0.0;
    }
    let n = count as f64;
    let mean = amps[..count].iter().sum::<f64>() / n;
    amps[..count]
        .iter()
        .map(|a| {
            let d = *a - mean;
            d * d
        })
        .sum::<f64>()
        / n
}