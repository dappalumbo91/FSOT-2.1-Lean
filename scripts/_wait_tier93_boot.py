import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from esp32_fsot_serial_lib import _parse_esp32_markers, parse_sonar_frames

import serial

print("Waiting for Tier 93 boot (release BOOT + tap EN if stuck in download)...")
chunks: list[str] = []
with serial.Serial("COM3", 115200, timeout=0.5) as ser:
    deadline = time.time() + 90
    last_hint = 0.0
    while time.time() < deadline:
        raw = ser.read(4096)
        if raw:
            chunks.append(raw.decode("utf-8", errors="replace"))
        text = "".join(chunks)
        if "waiting for download" in text and "FSOT 2.0" not in text:
            if time.time() - last_hint > 5:
                print("  still in download mode — release BOOT and tap EN")
                last_hint = time.time()
        if "FSOT_ESP32_OBSERVER_TIER=93" in text:
            break
        time.sleep(0.05)

text = "".join(chunks)
markers = _parse_esp32_markers(text)
frames = parse_sonar_frames(text)
print("tier=", markers.get("observer_tier"))
print("fluid_scalar=", markers.get("fluid_scalar"))
print("csi_packets=", markers.get("csi_packets"))
print("csi_amp_var=", markers.get("csi_amp_var"))
print("ble_devices=", markers.get("ble_device_count"))
print("fluid_level=", markers.get("fluid_level"))
print("fluid_frames=", len(frames))
if frames:
    f = frames[-1]
    print("last_frame_ble=", len(f.get("ble") or []))
    print("last_frame_csi_packets=", f.get("markers", {}).get("csi_packets"))
for line in text.splitlines():
    if line.startswith("FSOT_ESP32_"):
        print(line)