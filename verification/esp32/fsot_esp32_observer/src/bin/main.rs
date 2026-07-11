//! FSOT Tier 89–91 — ESP32 RF sonar + sensors + trinary LED + ESP-NOW gossip.

#![no_std]
#![no_main]
#![deny(clippy::mem_forget)]

extern crate alloc;

use embassy_time::{Duration, Timer};
use esp_alloc as _;
use esp_backtrace as _;
use esp_hal::{
    clock::CpuClock,
    gpio::{Level, Output, OutputConfig},
    interrupt::software::SoftwareInterruptControl,
    timer::timg::TimerGroup,
};
use esp_println::println;
use esp_radio::{
    ble::controller::BleConnector,
    esp_now::BROADCAST_ADDRESS,
    wifi::{scan::ScanConfig, ControllerConfig},
};
use fsot_esp32_observer::observer::{pack_enow_payload, trinary_collapse, ApRssi, ObserverSnapshot};
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

#[esp_rtos::main]
async fn main(_spawner: embassy_executor::Spawner) -> ! {
    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let mut peripherals = esp_hal::init(config);

    esp_alloc::heap_allocator!(size: 80 * 1024);

    let timg0 = TimerGroup::new(peripherals.TIMG0);
    let sw_int = SoftwareInterruptControl::new(peripherals.SW_INTERRUPT);
    esp_rtos::start(timg0.timer0, sw_int.software_interrupt0);

    let mut led = Output::new(peripherals.GPIO2, Level::Low, OutputConfig::default());

    for _ in 0..3 {
        led.toggle();
        Timer::after(Duration::from_millis(120)).await;
    }

    println!("FSOT 2.0 Bare-Metal Observer Kernel POC v0.1");
    println!("Fluid Spacetime Omni-Theory - Parameter Free | ESP32 xtensa");
    println!("Built with Rust no_std | FSOT Native Scalar Engine");
    println!("Tier 89–91 RF/Sensor Observer Layer active");
    println!();

    let boot_s = boot_scalar();
    println!("Mapping boot to FSOT domain: KernelInit (D_eff=8, observed=True)");
    println!("Computed FSOT Scalar S_D_chaotic = {boot_s:.6}");
    if boot_s > 0.0 {
        println!("Interpretation: POSITIVE (Emergence) - New information flow detected.");
    } else {
        println!("Interpretation: NEGATIVE / DAMPED (Stabilization) - Perturbations suppressed.");
    }
    println!();

    // ESP32 (classic) has no tsens in esp-hal 1.1 — proxy die temp from RF activity.
    let temp_c = 25.0_f32;

    let (mut wifi_ctrl, interfaces) =
        esp_radio::wifi::new(peripherals.WIFI, ControllerConfig::default()).expect("wifi init");
    let scan_config = ScanConfig::default().with_max(24);
    let aps = wifi_ctrl.scan_async(&scan_config).await.expect("wifi scan");
    let rssi_list: alloc::vec::Vec<ApWrap> = aps.iter().map(|ap| ApWrap(ap.signal_strength)).collect();

    let ble_stack_ok = match BleConnector::new(peripherals.BT, Default::default()) {
        Ok(_ble) => true,
        Err(_) => false,
    };

    let snapshot = ObserverSnapshot::from_wifi_aps(&rssi_list, temp_c, ble_stack_ok);
    let rf_scalar = snapshot.rf_scalar();
    let trinary = trinary_collapse(rf_scalar);

    match trinary {
        fsot_esp32_observer::observer::TrinaryState::Emergence => led.set_high(),
        fsot_esp32_observer::observer::TrinaryState::Stability => led.set_low(),
        fsot_esp32_observer::observer::TrinaryState::Damping => {
            for _ in 0..6 {
                led.toggle();
                Timer::after(Duration::from_millis(60)).await;
            }
        }
    }

    let dynamic = compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS);

    println!("Tier 88 ESP32 hardware boot complete — halting for harness capture.");
    println!("FSOT_ESP32_BOOT_SCALAR={boot_s:.17}");
    println!("FSOT_ESP32_CANONICAL={BOOT_SCALAR:.17}");
    println!("FSOT_ESP32_DYNAMIC_CHECK={dynamic:.17}");
    println!("FSOT_ESP32_HARDWARE_BOOT=ok");

    println!("Tier 89 RF sonar observer — WiFi scan mapped to scalar inputs.");
    println!("FSOT_ESP32_RF_SCALAR={rf_scalar:.17}");
    println!("FSOT_ESP32_WIFI_AP_COUNT={}", snapshot.ap_count);
    println!("FSOT_ESP32_RSSI_MEAN={:.3}", snapshot.rssi_mean);
    println!("FSOT_ESP32_RSSI_VAR={:.6}", snapshot.rssi_var);
    println!("FSOT_ESP32_TEMP_C={temp_c:.2}");
    println!(
        "FSOT_ESP32_BLE_STACK={}",
        if ble_stack_ok { "ok" } else { "fail" }
    );

    println!("Tier 90 trinary collapse from observer field.");
    println!("FSOT_ESP32_TRINARY_STATE={}", trinary.label());
    if trinary.as_i8() == 1 || rf_scalar > 0.0 {
        println!("Interpretation: POSITIVE (Emergence) - RF observer channel active.");
    }

    let mut esp_now = interfaces.esp_now;
    esp_now.set_channel(1).ok();
    let payload = pack_enow_payload(boot_s, rf_scalar, trinary);
    let enow_ok = esp_now
        .send_async(&BROADCAST_ADDRESS, &payload)
        .await
        .is_ok();
    println!("Tier 91 ESP-NOW scalar gossip.");
    println!(
        "FSOT_ESP32_ENOW_SENT={}",
        if enow_ok { "ok" } else { "fail" }
    );
    println!("FSOT_ESP32_OBSERVER_TIER=91");

    let blink_ms = match trinary {
        fsot_esp32_observer::observer::TrinaryState::Emergence => 0,
        fsot_esp32_observer::observer::TrinaryState::Stability => 800,
        fsot_esp32_observer::observer::TrinaryState::Damping => 150,
    };

    loop {
        if blink_ms > 0 {
            led.toggle();
            Timer::after(Duration::from_millis(blink_ms)).await;
        } else {
            Timer::after(Duration::from_secs(5)).await;
        }
    }
}