#!/usr/bin/env python3
"""FSOT Star Trek Transporter technology stack — verification figure."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "vendor" / "application_wiring" / "tier88_cache" / "star_trek_transporter_cache.json"
BENCH = ROOT / "data" / "star_trek_transporter_live_panel_benchmark.json"
FIG_DIR = ROOT / "data" / "figures"

LAYER_ORDER = (
    ("quantum_channel", "Quantum teleportation", "#7c3aed"),
    ("information_theory", "Information theory", "#2563eb"),
    ("portal_proxies", "Poof / suction portal", "#059669"),
    ("transporter_engineering", "Transporter engineering", "#d97706"),
    ("warp_actuation", "Warp actuation", "#dc2626"),
    ("warp_portal_crosswalk", "Portal crosswalk", "#0891b2"),
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _layer_medians(bench: dict) -> dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    section_map = {
        "qubit_teleport": "quantum_channel",
        "entanglement": "quantum_channel",
        "landauer": "information_theory",
        "channel_capacity": "information_theory",
        "decoherence": "information_theory",
        "error_correction": "information_theory",
        "poof": "portal_proxies",
        "suction": "portal_proxies",
        "coherence_efficiency": "portal_proxies",
        "information_preservation": "portal_proxies",
        "k_coupling": "portal_proxies",
        "beam_resolution": "portal_proxies",
        "scan_time": "portal_proxies",
        "pattern_buffer": "transporter_engineering",
        "matter_scan": "transporter_engineering",
        "dematerialization": "transporter_engineering",
        "heisenberg": "transporter_engineering",
        "reassembly": "transporter_engineering",
        "transport_cycle": "transporter_engineering",
        "bio_pattern": "transporter_engineering",
        "portal_doorway": "warp_actuation",
        "entanglement_gate": "warp_actuation",
        "traverse": "warp_actuation",
        "tunneling_bridge": "warp_actuation",
        "stabilization_margin": "warp_actuation",
        "bh_inlet": "warp_actuation",
        "wh_outgassing": "warp_actuation",
        "micro_portal": "warp_portal_crosswalk",
        "quantum_entanglement_gate": "warp_portal_crosswalk",
        "entangled_gate_pair": "warp_portal_crosswalk",
        "doorway_traverse": "warp_portal_crosswalk",
    }
    for rec in bench.get("material_records") or []:
        name = str(rec.get("name") or "").lower()
        err = float(rec.get("error_pct") or 0)
        layer = "warp_portal_crosswalk"
        for key, lay in section_map.items():
            if key in name:
                layer = lay
                break
        if rec.get("extra", {}).get("channel"):
            layer = str(rec["extra"]["channel"])
        buckets[layer].append(err)
    return {k: sum(v) / len(v) for k, v in buckets.items() if v}


def figure_transporter_stack(out: Path) -> dict:
    import matplotlib.pyplot as plt
    import numpy as np

    cache = _load(CACHE)
    bench = _load(BENCH)
    medians = _layer_medians(bench)
    pooled = float(bench.get("pooled_median_error_pct") or 0)
    frame = cache.get("technology_frame") or {}

    labels = [t[1] for t in LAYER_ORDER]
    keys = [t[0] for t in LAYER_ORDER]
    colors = [t[2] for t in LAYER_ORDER]
    values = [medians.get(k, pooled) for k in keys]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")

    ax = axes[0]
    y = np.arange(len(labels))
    ax.barh(y, values, color=colors, alpha=0.9)
    ax.axvline(0.05, color="#f59e0b", linestyle=":", linewidth=1.2, label="0.05% tier aspiration")
    ax.axvline(0.5, color="#dc2626", linestyle="--", linewidth=1.2, label="0.5% verification gate")
    ax.axvline(pooled, color="#1e3a8a", linewidth=2.0, label=f"pooled {pooled:.4f}%")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("FSOT scalar error % (layer median)")
    ax.set_title("Transporter technology stack — per-layer precision")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_xlim(0, max(0.12, max(values) * 1.35))

    ax2 = axes[1]
    ax2.axis("off")
    stack_text = [
        frame.get("name", "FSOT Star Trek Transporter"),
        "",
        frame.get("mechanism", ""),
        "",
        f"Records verified: {bench.get('record_count', '?')}",
        f"Pooled median error: {pooled:.5f}%",
        "",
        "Stack layers:",
        "  1. Quantum teleportation channel (fidelity, entanglement, no-cloning)",
        "  2. Information theory (Landauer, decoherence, error correction)",
        "  3. Poof/suction portal proxies (matter-stream geometry)",
        "  4. Transporter engineering (scan, pattern buffer, reassembly)",
        "  5. Warp actuation (portal doorway, traverse, stabilization)",
        "  6. Warp BH/WH portal crosswalk (entanglement gate pairs)",
        "",
        frame.get("doorway_interpretation", ""),
        frame.get("entanglement_interpretation", ""),
    ]
    ax2.text(0.02, 0.98, "\n".join(stack_text), va="top", fontsize=9, family="monospace", wrap=True)

    fig.suptitle(
        "FSOT Transporter Technology — seed-scalar verified engineering stack",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)

    return {
        "record_count": bench.get("record_count"),
        "pooled_median_error_pct": pooled,
        "layer_medians": medians,
        "technology_frame": frame,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT transporter technology verification figure")
    parser.add_argument("--output", type=Path, default=FIG_DIR / "verified_desktop_transporter.png")
    args = parser.parse_args()

    if not BENCH.exists():
        raise SystemExit("Run ingest + build tier88 first")

    meta = figure_transporter_stack(args.output)
    manifest = args.output.parent / "verified_desktop_transporter_manifest.json"
    manifest.write_text(json.dumps({"figure": args.output.name, **meta}, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {meta.get('record_count')}  pooled: {meta.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())