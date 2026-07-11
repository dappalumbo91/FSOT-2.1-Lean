#!/usr/bin/env python3
"""Live RF sonar visualizer for FSOT ESP32 observer (Tier 92 viz telemetry)."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from esp32_fsot_serial_lib import (  # noqa: E402
    DEFAULT_BAUD,
    _parse_esp32_markers,
    detect_cp210x_port,
    mask_sonar_frame,
    parse_sonar_frames,
)

OUT_DIR = ROOT / "data"
SNAPSHOT_JSON = OUT_DIR / "esp32_rf_sonar_snapshot.json"
SNAPSHOT_PNG = OUT_DIR / "esp32_rf_sonar_snapshot.png"

TRINARY_COLORS = {"+1": "#22c55e", "0": "#eab308", "-1": "#ef4444"}
RSSI_MIN = -90
RSSI_MAX = -30


def rssi_to_radius(rssi: int) -> float:
    clamped = max(RSSI_MIN, min(RSSI_MAX, rssi))
    return (clamped - RSSI_MIN) / (RSSI_MAX - RSSI_MIN)


def read_serial_stream(port: str, seconds: float | None = None):
    import serial

    buffer = ""
    deadline = None if seconds is None else time.time() + seconds
    with serial.Serial(port, DEFAULT_BAUD, timeout=0.3) as ser:
        while deadline is None or time.time() < deadline:
            raw = ser.read(4096)
            if raw:
                buffer += raw.decode("utf-8", errors="replace")
                yield buffer
            else:
                yield buffer
            time.sleep(0.05)


def latest_complete_frame(text: str) -> dict | None:
    frames = parse_sonar_frames(text)
    if frames:
        return frames[-1]
    markers = _parse_esp32_markers(text)
    if markers.get("wifi_ap_count") is not None and "FSOT_ESP32_OBSERVER_TIER=91" in text:
        return {
            "frame": 0,
            "aps": [],
            "markers": markers,
            "legacy_summary_only": True,
        }
    return None


def publish_snapshot_doc(frame: dict, boot_markers: dict, port: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "port": port,
        "frame": mask_sonar_frame(frame),
        "boot_markers": boot_markers,
        "ssid_masking": "Network1..N replaces real SSIDs in committed artifacts",
    }


def draw_sonar_dashboard(
    frame: dict,
    boot_markers: dict,
    save_path: Path | None = None,
    show: bool = True,
    mask_ssids: bool = False,
):
    if mask_ssids:
        frame = mask_sonar_frame(frame)
    import matplotlib.pyplot as plt
    import numpy as np

    aps = frame.get("aps") or []
    markers = frame.get("markers") or {}
    frame_id = frame.get("frame", 0)

    fig = plt.figure(figsize=(12, 8), facecolor="#0f172a")
    fig.suptitle(
        f"ESP32 RF Sonar — frame {frame_id}  |  {len(aps)} access points detected",
        color="#e2e8f0",
        fontsize=14,
        fontweight="bold",
    )

    ax_radar = fig.add_subplot(2, 2, 1, projection="polar", facecolor="#1e293b")
    ax_channel = fig.add_subplot(2, 2, 2, facecolor="#1e293b")
    ax_scalar = fig.add_subplot(2, 2, 3, facecolor="#1e293b")
    ax_info = fig.add_subplot(2, 2, 4, facecolor="#1e293b")

    for ax in (ax_channel, ax_scalar, ax_info):
        ax.tick_params(colors="#94a3b8")
        for spine in ax.spines.values():
            spine.set_color("#334155")

    # Polar "sonar" — each AP is an echo at a compass slot; radius = signal strength.
    ax_radar.set_facecolor("#1e293b")
    ax_radar.set_theta_zero_location("N")
    ax_radar.set_theta_direction(-1)
    ax_radar.set_ylim(0, 1.05)
    ax_radar.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax_radar.set_yticklabels(["weak", "", "", "strong"], color="#64748b", fontsize=8)
    ax_radar.set_xticks(np.linspace(0, 2 * math.pi, 8, endpoint=False))
    ax_radar.set_xticklabels([f"{i * 45}°" for i in range(8)], color="#94a3b8", fontsize=8)
    ax_radar.grid(color="#334155", alpha=0.6)
    ax_radar.set_title("WiFi echo map (RSSI → range)", color="#e2e8f0", pad=12)

    if aps:
        n = len(aps)
        for i, ap in enumerate(aps):
            angle = (2 * math.pi * i / n) - math.pi / 2
            radius = rssi_to_radius(ap["rssi"])
            ax_radar.scatter(
                [angle],
                [radius],
                s=120 + radius * 80,
                c="#38bdf8",
                edgecolors="#0ea5e9",
                linewidths=1.2,
                alpha=0.9,
                zorder=3,
            )
            label = ap["ssid"][:12] + ("…" if len(ap["ssid"]) > 12 else "")
            ax_radar.annotate(
                f"{label}\n{ap['rssi']} dBm",
                xy=(angle, radius),
                xytext=(angle, min(1.08, radius + 0.12)),
                color="#cbd5e1",
                fontsize=7,
                ha="center",
                va="bottom",
            )
    else:
        ax_radar.text(
            0.5,
            0.5,
            "No APs detected",
            transform=ax_radar.transAxes,
            ha="center",
            va="center",
            color="#94a3b8",
        )

    # Channel occupancy bar chart.
    by_channel: dict[int, list[int]] = defaultdict(list)
    for ap in aps:
        by_channel[ap["channel"]].append(ap["rssi"])
    channels = list(range(1, 14))
    counts = [len(by_channel[ch]) for ch in channels]
    best_rssi = [max(by_channel[ch]) if by_channel[ch] else RSSI_MIN for ch in channels]
    colors = [
        "#38bdf8" if c > 0 else "#334155" for c in counts
    ]
    bars = ax_channel.bar(channels, counts, color=colors, edgecolor="#0f172a")
    ax_channel.set_xlabel("Wi-Fi channel", color="#94a3b8")
    ax_channel.set_ylabel("AP count", color="#94a3b8")
    ax_channel.set_title("Channel occupancy", color="#e2e8f0")
    ax_channel.set_xticks(channels)
    for bar, ch, rssi in zip(bars, channels, best_rssi):
        if bar.get_height() > 0:
            ax_channel.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                f"{rssi} dBm",
                ha="center",
                va="bottom",
                color="#cbd5e1",
                fontsize=7,
            )

    # Scalar gauges.
    boot_scalar = boot_markers.get("boot_scalar")
    rf_scalar = markers.get("rf_scalar")
    scalars = []
    labels = []
    bar_colors = []
    if isinstance(boot_scalar, float):
        scalars.append(boot_scalar)
        labels.append("Boot scalar")
        bar_colors.append("#a78bfa")
    if isinstance(rf_scalar, float):
        scalars.append(rf_scalar)
        labels.append("RF scalar")
        bar_colors.append("#38bdf8")
    if scalars:
        y_pos = range(len(scalars))
        ax_scalar.barh(list(y_pos), scalars, color=bar_colors, height=0.5)
        ax_scalar.set_yticks(list(y_pos), labels)
        ax_scalar.set_xlim(0, max(0.2, max(scalars) * 1.2))
        for i, val in enumerate(scalars):
            ax_scalar.text(val + 0.002, i, f"{val:.6f}", va="center", color="#e2e8f0", fontsize=9)
    ax_scalar.set_xlabel("FSOT scalar magnitude", color="#94a3b8")
    ax_scalar.set_title("Multi-level scalar stack", color="#e2e8f0")

    # Info panel.
    trinary = markers.get("trinary_state", "?")
    trinary_color = TRINARY_COLORS.get(str(trinary), "#94a3b8")
    lines = [
        "What the ESP32 sees:",
        "",
        f"  Trinary collapse:  {trinary}",
        f"  AP count:          {markers.get('wifi_ap_count', len(aps))}",
        f"  RSSI mean:         {markers.get('rssi_mean', 'n/a')}",
        f"  RSSI variance:     {markers.get('rssi_var', 'n/a')}",
        "",
        "Detected networks:",
    ]
    if aps:
        for ap in sorted(aps, key=lambda a: a["rssi"], reverse=True):
            lines.append(
                f"  ch {ap['channel']:2d}  {ap['rssi']:4d} dBm  {ap['ssid']}"
            )
    else:
        lines.append("  (none)")
    if frame.get("legacy_summary_only"):
        lines.extend(
            [
                "",
                "Note: summary-only firmware (no per-AP lines).",
                "Re-flash to enable live sonar map:",
                "  python scripts/flash_esp32_fsot_observer.py",
            ]
        )
    lines.extend(
        [
            "",
            "Legend:",
            "  Radar blip radius = stronger signal (closer/louder echo)",
            "  LED on GPIO2 mirrors trinary: solid=+1, slow blink=0, fast=-1",
        ]
    )
    ax_info.axis("off")
    ax_info.text(
        0.02,
        0.98,
        "\n".join(lines),
        transform=ax_info.transAxes,
        va="top",
        ha="left",
        color="#e2e8f0",
        fontsize=9,
        family="monospace",
    )
    ax_info.add_patch(
        plt.Rectangle(
            (0.0, 0.92),
            0.04,
            0.04,
            transform=ax_info.transAxes,
            facecolor=trinary_color,
            clip_on=False,
        )
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor())
        print(f"Saved snapshot: {save_path}")
    if show:
        plt.show(block=False)
        plt.pause(0.05)
    else:
        plt.close(fig)


def run_live(port: str, snapshot: bool = False) -> int:
    import matplotlib.pyplot as plt

    print(f"Opening {port} @ {DEFAULT_BAUD} — waiting for sonar frames...")
    print("Press Ctrl+C to stop.")
    print()
    print("What you are seeing:")
    print("  • The ESP32 passively listens for Wi-Fi beacon frames (like a submarine ping).")
    print("  • Each network becomes a 'blip' — stronger RSSI = closer/brighter echo.")
    print("  • The scalar stack maps RF chaos into the FSOT boot + RF layers.")
    print()

    buffer = ""
    boot_markers: dict = {}
    fig_open = False

    try:
        import serial

        with serial.Serial(port, DEFAULT_BAUD, timeout=0.3) as ser:
            while True:
                raw = ser.read(4096)
                if raw:
                    buffer += raw.decode("utf-8", errors="replace")
                    if not boot_markers and "FSOT_ESP32_OBSERVER_TIER=91" in buffer:
                        boot_markers = _parse_esp32_markers(buffer)
                    frame = latest_complete_frame(buffer)
                    if frame:
                        if not fig_open:
                            plt.ion()
                            fig_open = True
                        draw_sonar_dashboard(
                            frame,
                            boot_markers,
                            save_path=SNAPSHOT_PNG if snapshot else None,
                            show=True,
                        )
                        if snapshot:
                            doc = publish_snapshot_doc(frame, boot_markers, port)
                            OUT_DIR.mkdir(parents=True, exist_ok=True)
                            SNAPSHOT_JSON.write_text(
                                json.dumps(doc, indent=2), encoding="utf-8"
                            )
                            print(f"Wrote {SNAPSHOT_JSON}")
                            return 0
                plt.pause(0.05)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run_capture_once(port: str, seconds: float = 45.0) -> int:
    buffer = ""
    for chunk in read_serial_stream(port, seconds=seconds):
        buffer = chunk
        if latest_complete_frame(buffer):
            break
    boot_markers = _parse_esp32_markers(buffer)
    frame = latest_complete_frame(buffer)
    if not frame:
        print("No complete sonar frame captured. Is the ESP32 flashed with SONAR_VIZ firmware?")
        print("Run: python scripts/build_esp32_fsot_observer.py")
        print("     python scripts/flash_esp32_fsot_observer.py")
        return 1
    draw_sonar_dashboard(
        frame,
        boot_markers,
        save_path=SNAPSHOT_PNG,
        show=True,
        mask_ssids=True,
    )
    doc = publish_snapshot_doc(frame, boot_markers, port)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {SNAPSHOT_JSON}")
    import matplotlib.pyplot as plt

    plt.show()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Visualize ESP32 multi-level RF sonar (WiFi scan → FSOT scalar)"
    )
    parser.add_argument("--port", help="COM port (default: auto-detect CP210x)")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Capture one frame then save PNG/JSON and exit",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="In live mode, save first frame to data/ and exit",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=45.0,
        help="Seconds to wait for a frame in --once mode (default: 45)",
    )
    args = parser.parse_args()

    port = args.port or detect_cp210x_port()
    if not port:
        print("No CP210x COM port found. Plug in the ESP32 or pass --port COM3")
        return 1

    if args.once:
        return run_capture_once(port, seconds=args.wait)
    return run_live(port, snapshot=args.snapshot)


if __name__ == "__main__":
    raise SystemExit(main())