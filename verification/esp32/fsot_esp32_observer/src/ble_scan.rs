//! Tier 93 — BLE passive HCI scan (Level 2 RF fluid echo).

use alloc::vec::Vec;

use embassy_time::{Duration, Timer};
use esp_radio::ble::controller::BleConnector;

const HCI_CMD_SET_SCAN_PARAMS: &[u8] = &[0x01, 0x0B, 0x20, 0x07, 0x00, 0x40, 0x00, 0x40, 0x00, 0x00, 0x00];
const HCI_CMD_SCAN_ENABLE: &[u8] = &[0x01, 0x0C, 0x20, 0x02, 0x01, 0x00];
const HCI_CMD_SCAN_DISABLE: &[u8] = &[0x01, 0x0C, 0x20, 0x02, 0x00, 0x00];

#[derive(Debug, Clone, Copy)]
pub struct BleHit {
    pub idx: u8,
    pub rssi: i8,
}

pub async fn passive_scan(connector: &mut BleConnector<'_>, duration_ms: u64, max: usize) -> Vec<BleHit> {
    let _ = connector.write(HCI_CMD_SET_SCAN_PARAMS);
    let _ = connector.write(HCI_CMD_SCAN_ENABLE);

    let mut rx_buf = [0u8; 256];
    let mut stream: Vec<u8> = Vec::new();
    let mut hits: Vec<(i8, [u8; 6])> = Vec::new();
    let deadline = embassy_time::Instant::now() + Duration::from_millis(duration_ms);

    while embassy_time::Instant::now() < deadline {
        if let Ok(n) = connector.read_async(&mut rx_buf).await {
            if n > 0 {
                stream.extend_from_slice(&rx_buf[..n]);
                drain_hci_events(&mut stream, &mut hits, max);
            }
        }
        Timer::after(Duration::from_millis(20)).await;
    }

    let _ = connector.write(HCI_CMD_SCAN_DISABLE);

    hits.into_iter()
        .enumerate()
        .take(max)
        .map(|(i, (rssi, _addr))| BleHit {
            idx: i as u8,
            rssi,
        })
        .collect()
}

fn drain_hci_events(stream: &mut Vec<u8>, hits: &mut Vec<(i8, [u8; 6])>, max: usize) {
    while stream.len() >= 3 {
        if stream[0] != 0x04 {
            stream.remove(0);
            continue;
        }
        let param_len = stream[2] as usize;
        let frame_len = 3 + param_len;
        if stream.len() < frame_len {
            break;
        }
        let event_code = stream[1];
        let params = &stream[3..frame_len];
        if event_code == 0x3E {
            parse_le_meta(params, hits, max);
        }
        stream.drain(..frame_len);
    }
}

fn parse_le_meta(params: &[u8], hits: &mut Vec<(i8, [u8; 6])>, max: usize) {
    if params.is_empty() || params[0] != 0x02 || hits.len() >= max {
        return;
    }
    let mut i = 1usize;
    let num_reports = params[i];
    i += 1;
    for _ in 0..num_reports {
        if i + 10 > params.len() {
            break;
        }
        i += 1; // event type
        i += 1; // address type
        let mut addr = [0u8; 6];
        addr.copy_from_slice(&params[i..i + 6]);
        i += 6;
        let data_len = params[i] as usize;
        i += 1;
        if i + data_len + 1 > params.len() {
            break;
        }
        i += data_len;
        let rssi = params[i] as i8;
        i += 1;
        if rssi != 127 {
            hits.push((rssi, addr));
        }
    }
}