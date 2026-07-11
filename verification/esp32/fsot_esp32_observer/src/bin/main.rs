//! FSOT Tier 93 — WiFi CSI + BLE fluid sonar + trinary LED + ESP-NOW gossip.

#![no_std]
#![no_main]
#![deny(clippy::mem_forget)]

extern crate alloc;

use alloc::vec::Vec;
use embassy_time::{Duration, Timer};
use esp_alloc as _;
use esp_backtrace as _;
use esp_hal::{
    clock::CpuClock,
    delay::Delay,
    gpio::{Level, Output, OutputConfig},
    interrupt::software::SoftwareInterruptControl,
    ram,
    timer::timg::TimerGroup,
};
use esp_println::println;
use esp_radio::{
    ble::controller::BleConnector,
    esp_now::BROADCAST_ADDRESS,
    wifi::{
        ap::AccessPointInfo,
        csi::CsiConfig,
        scan::ScanConfig,
        sta::StationConfig,
        Config, ControllerConfig, SecondaryChannel,
    },
};
use fsot_esp32_observer::{
    ble_scan::{self, BleHit},
    csi::{record_csi_buf, reset_csi_window, snapshot_csi_window},
    observer::{
        pack_enow_payload, trinary_collapse, ApRssi, FluidSonarSnapshot, ObserverSnapshot,
        TrinaryState,
    },
};
use fsot_scalar_kernel::{
    boot_scalar, compute_fsot_scalar, BOOT_DELTA_PSI, BOOT_D_EFF, BOOT_OBSERVED, BOOT_RECENT_HITS,
    BOOT_SCALAR,
};

esp_bootloader_esp_idf::esp_app_desc!();

struct ApWrap(i8);

impl ApRssi for ApWrap {
    fn rssi(&self) -> i8 {
        self.0
    }
}

const FLUID_CYCLE_INTERVAL_S: u64 = 5;
const CSI_LISTEN_MS: u64 = 2000;
const BLE_SCAN_MS: u64 = 1500;

fn sanitize_ssid(ssid: &str) -> alloc::string::String {
    ssid.chars()
        .map(|c| if c == '|' || c == '\n' || c == '\r' { '_' } else { c })
        .collect()
}

fn emit_fluid_frame(
    frame: u32,
    aps: &[AccessPointInfo],
    fluid: &FluidSonarSnapshot,
    ble_hits: &[BleHit],
    fluid_scalar: f64,
    trinary: TrinaryState,
) {
    println!("FSOT_ESP32_FLUID_FRAME_START frame={frame}");
    println!("FSOT_ESP32_FLUID_LEVEL=2");
    for (i, ap) in aps.iter().enumerate() {
        let ssid = sanitize_ssid(ap.ssid.as_str());
        println!(
            "FSOT_ESP32_AP|{i}|{}|{}|{ssid}",
            ap.channel,
            ap.signal_strength
        );
    }
    println!("FSOT_ESP32_CSI_PACKETS={}", fluid.csi.packets);
    println!("FSOT_ESP32_CSI_AMP_VAR={:.6}", fluid.csi.amp_var_mean);
    println!("FSOT_ESP32_CSI_CHANNEL={}", fluid.csi.last_channel);
    for hit in ble_hits {
        println!("FSOT_ESP32_BLE|{}|{}", hit.idx + 1, hit.rssi);
    }
    println!("FSOT_ESP32_BLE_DEVICE_COUNT={}", fluid.ble_count);
    println!("FSOT_ESP32_RF_SCALAR={:.17}", fluid.rf_scalar());
    println!("FSOT_ESP32_FLUID_SCALAR={fluid_scalar:.17}");
    println!("FSOT_ESP32_WIFI_AP_COUNT={}", fluid.wifi.ap_count);
    println!("FSOT_ESP32_RSSI_MEAN={:.3}", fluid.wifi.rssi_mean);
    println!("FSOT_ESP32_RSSI_VAR={:.6}", fluid.wifi.rssi_var);
    println!("FSOT_ESP32_TRINARY_STATE={}", trinary.label());
    println!("FSOT_ESP32_FLUID_FRAME_END frame={frame}");
}

fn tune_csi_listener(wifi_ctrl: &mut esp_radio::wifi::WifiController<'_>, channel: u8) -> bool {
    if wifi_ctrl
        .set_config(&Config::Station(StationConfig::default()))
        .is_err()
    {
        return false;
    }
    if wifi_ctrl
        .set_channel(channel, SecondaryChannel::None)
        .is_err()
    {
        return false;
    }
    reset_csi_window();
    wifi_ctrl
        .set_csi(CsiConfig::default(), |info| {
            record_csi_buf(
                info.buf(),
                info.first_word_invalid(),
                info.channel(),
                info.rssi(),
            );
        })
        .is_ok()
}

async fn wifi_scan_aps(
    wifi_ctrl: &mut esp_radio::wifi::WifiController<'_>,
    scan_config: &ScanConfig,
) -> Vec<AccessPointInfo> {
    wifi_ctrl
        .scan_async(scan_config)
        .await
        .unwrap_or_default()
}

async fn listen_csi_window(wifi_ctrl: &mut esp_radio::wifi::WifiController<'_>, channel: u8) {
    if tune_csi_listener(wifi_ctrl, channel) {
        Timer::after(Duration::from_millis(CSI_LISTEN_MS)).await;
    }
}

async fn scan_ble_devices(ble_connector: &mut Option<BleConnector<'_>>) -> Vec<BleHit> {
    if let Some(ble) = ble_connector.as_mut() {
        ble_scan::passive_scan(ble, BLE_SCAN_MS, 12).await
    } else {
        Vec::new()
    }
}

async fn sample_fluid_field(
    wifi_ctrl: &mut esp_radio::wifi::WifiController<'_>,
    ble_connector: &mut Option<BleConnector<'_>>,
    scan_config: &ScanConfig,
    temp_c: f32,
    ble_stack_ok: bool,
) -> (Vec<AccessPointInfo>, FluidSonarSnapshot, Vec<BleHit>) {
    let aps = wifi_scan_aps(wifi_ctrl, scan_config).await;
    let rssi_list: Vec<ApWrap> = aps.iter().map(|ap| ApWrap(ap.signal_strength)).collect();
    let wifi = ObserverSnapshot::from_wifi_aps(&rssi_list, temp_c, ble_stack_ok);
    let listen_ch = aps
        .iter()
        .max_by_key(|ap| ap.signal_strength)
        .map(|ap| ap.channel)
        .unwrap_or(1);
    listen_csi_window(wifi_ctrl, listen_ch).await;
    let csi = snapshot_csi_window();
    let ble_hits = scan_ble_devices(ble_connector).await;
    let fluid = FluidSonarSnapshot::from_layers(wifi, csi, &ble_hits);
    (aps, fluid, ble_hits)
}

async fn fluid_cycle_loop(
    wifi_ctrl: &mut esp_radio::wifi::WifiController<'_>,
    ble_connector: &mut Option<BleConnector<'_>>,
    scan_config: &ScanConfig,
    temp_c: f32,
    ble_stack_ok: bool,
    mut led: Output<'_>,
    mut blink_ms: u64,
) -> ! {
    let mut frame: u32 = 1;
    let mut last_cycle = embassy_time::Instant::now();
    loop {
        if blink_ms > 0 {
            led.toggle();
            Timer::after(Duration::from_millis(blink_ms)).await;
        } else {
            Timer::after(Duration::from_millis(200)).await;
        }
        if last_cycle.elapsed() >= Duration::from_secs(FLUID_CYCLE_INTERVAL_S) {
            let (fresh_aps, fresh_fluid, fresh_ble) = sample_fluid_field(
                wifi_ctrl,
                ble_connector,
                scan_config,
                temp_c,
                ble_stack_ok,
            )
            .await;
            let fresh_fluid_scalar = fresh_fluid.fluid_scalar();
            let fresh_trinary = trinary_collapse(fresh_fluid_scalar);
            emit_fluid_frame(
                frame,
                &fresh_aps,
                &fresh_fluid,
                &fresh_ble,
                fresh_fluid_scalar,
                fresh_trinary,
            );
            frame = frame.wrapping_add(1);
            blink_ms = match fresh_trinary {
                TrinaryState::Emergence => 0,
                TrinaryState::Stability => 800,
                TrinaryState::Damping => 150,
            };
            match fresh_trinary {
                TrinaryState::Emergence => led.set_high(),
                TrinaryState::Stability => led.set_low(),
                TrinaryState::Damping => {}
            }
            last_cycle = embassy_time::Instant::now();
        }
    }
}

#[esp_rtos::main]
async fn main(_spawner: embassy_executor::Spawner) -> ! {
    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let peripherals = esp_hal::init(config);

    esp_alloc::heap_allocator!(size: 64 * 1024);
    esp_alloc::heap_allocator!(#[ram(reclaimed)] size: 64 * 1024);

    let timg0 = TimerGroup::new(peripherals.TIMG0);
    let sw_int = SoftwareInterruptControl::new(peripherals.SW_INTERRUPT);
    esp_rtos::start(timg0.timer0, sw_int.software_interrupt0);

    let mut led = Output::new(peripherals.GPIO2, Level::Low, OutputConfig::default());
    let mut delay = Delay::new();
    for _ in 0..3 {
        led.toggle();
        delay.delay_millis(120);
    }

    let boot_s = boot_scalar();
    let dynamic = compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS);
    println!("FSOT 2.0 Bare-Metal Observer Kernel POC v0.1");
    println!("Tier 93 WiFi CSI + BLE fluid sonar active");
    println!("Computed FSOT Scalar S_D_chaotic = {boot_s:.6}");
    println!("FSOT_ESP32_BOOT_SCALAR={boot_s:.17}");
    println!("FSOT_ESP32_CANONICAL={BOOT_SCALAR:.17}");
    println!("FSOT_ESP32_DYNAMIC_CHECK={dynamic:.17}");
    println!("FSOT_ESP32_HARDWARE_BOOT=ok");

    let temp_c = 25.0_f32;
    let (mut wifi_ctrl, interfaces) =
        esp_radio::wifi::new(peripherals.WIFI, ControllerConfig::default()).expect("wifi init");
    let scan_config = ScanConfig::default().with_max(16);

    let ble_connector = BleConnector::new(peripherals.BT, Default::default());
    let ble_stack_ok = ble_connector.is_ok();
    let mut ble_connector = ble_connector.ok();

    let aps = wifi_scan_aps(&mut wifi_ctrl, &scan_config).await;
    let rssi_list: Vec<ApWrap> = aps.iter().map(|ap| ApWrap(ap.signal_strength)).collect();
    let wifi = ObserverSnapshot::from_wifi_aps(&rssi_list, temp_c, ble_stack_ok);
    let fluid = FluidSonarSnapshot::from_layers(wifi, snapshot_csi_window(), &[]);
    let ble_hits: Vec<BleHit> = Vec::new();
    let fluid_scalar = fluid.fluid_scalar();
    let trinary = trinary_collapse(fluid_scalar);

    match trinary {
        TrinaryState::Emergence => led.set_high(),
        TrinaryState::Stability => led.set_low(),
        TrinaryState::Damping => {
            for _ in 0..6 {
                led.toggle();
                Timer::after(Duration::from_millis(60)).await;
            }
        }
    }

    println!("FSOT_ESP32_RF_SCALAR={:.17}", fluid.rf_scalar());
    println!("FSOT_ESP32_FLUID_SCALAR={fluid_scalar:.17}");
    println!("FSOT_ESP32_CSI_PACKETS={}", fluid.csi.packets);
    println!("FSOT_ESP32_CSI_AMP_VAR={:.6}", fluid.csi.amp_var_mean);
    println!("FSOT_ESP32_WIFI_AP_COUNT={}", fluid.wifi.ap_count);
    println!("FSOT_ESP32_BLE_DEVICE_COUNT={}", fluid.ble_count);
    println!("FSOT_ESP32_TRINARY_STATE={}", trinary.label());
    println!(
        "FSOT_ESP32_BLE_STACK={}",
        if ble_stack_ok { "ok" } else { "fail" }
    );

    let mut esp_now = interfaces.esp_now;
    esp_now.set_channel(1).ok();
    let enow_ok = esp_now
        .send_async(
            &BROADCAST_ADDRESS,
            &pack_enow_payload(boot_s, fluid_scalar, trinary),
        )
        .await
        .is_ok();
    println!(
        "FSOT_ESP32_ENOW_SENT={}",
        if enow_ok { "ok" } else { "fail" }
    );
    println!("FSOT_ESP32_OBSERVER_TIER=93");
    println!("FSOT_ESP32_SONAR_VIZ=1");
    println!("FSOT_ESP32_FLUID_LEVEL=2");

    emit_fluid_frame(0, &aps, &fluid, &ble_hits, fluid_scalar, trinary);

    let blink_ms = match trinary {
        TrinaryState::Emergence => 0_u64,
        TrinaryState::Stability => 800,
        TrinaryState::Damping => 150,
    };
    fluid_cycle_loop(
        &mut wifi_ctrl,
        &mut ble_connector,
        &scan_config,
        temp_c,
        ble_stack_ok,
        led,
        blink_ms,
    )
    .await
}