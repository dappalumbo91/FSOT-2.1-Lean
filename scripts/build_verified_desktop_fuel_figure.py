#!/usr/bin/env python3
"""Verified desktop fuel evidence figure — FSOT-designed fuels vs gasoline baseline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier88_verified_desktop_lib import FSOT_DESIGNED_FUEL_IDS, GASOLINE_BASELINE_ID  # noqa: E402

CACHE = ROOT / "vendor" / "application_wiring" / "tier88_cache" / "fuel_lab_live_cache.json"
BENCH = ROOT / "data" / "fuel_lab_live_panel_benchmark.json"
FIG_DIR = ROOT / "data" / "figures"

DISPLAY_NAMES = {
    "fsot_hemp_waste_grounded": "Hemp grounded",
    "fsot_hemp_waste_advanced": "Hemp advanced",
    "fsot_algae_oil_biodiesel": "Algae biodiesel",
    "fsot_mushroom_spore_fuel": "Mushroom ester",
    "fsot_green_hydrogen": "Green H₂",
    "fsot_optimax": "FSOT Optimax",
    "fsot_bio_spark": "Bio Spark",
    "gasoline": "Gasoline (baseline)",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _sim_by_fuel(cache: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in cache.get("simulation_records") or []:
        pid = str(row.get("fuel_profile_id") or "")
        if pid and pid not in out:
            out[pid] = row
    return out


def _median_error_by_fuel(bench: dict) -> dict[str, float]:
    from collections import defaultdict

    buckets: dict[str, list[float]] = defaultdict(list)
    for rec in bench.get("material_records") or []:
        name = str(rec.get("name") or "")
        err = float(rec.get("error_pct") or 0)
        for pid in FSOT_DESIGNED_FUEL_IDS:
            if name == pid or name.startswith(f"compare_{pid}") or name.startswith(f"hemp_refined_{pid}"):
                buckets[pid].append(err)
                break
    return {pid: (sum(v) / len(v) if v else 0.0) for pid, v in buckets.items()}


def figure_verified_desktop_fuels(out: Path) -> dict:
    import matplotlib.pyplot as plt
    import numpy as np

    cache = _load(CACHE)
    bench = _load(BENCH)
    sim = _sim_by_fuel(cache)
    medians = _median_error_by_fuel(bench)

    fuel_order = list(FSOT_DESIGNED_FUEL_IDS) + [GASOLINE_BASELINE_ID]
    labels = [DISPLAY_NAMES.get(pid, pid) for pid in fuel_order]

    renewable = [float((sim.get(pid) or {}).get("renewable_rank") or 0) for pid in fuel_order]
    efficiency = [float((sim.get(pid) or {}).get("thermal_efficiency") or 0) for pid in fuel_order]
    fsot_score = [float((sim.get(pid) or {}).get("fsot_score") or 0) for pid in fuel_order]
    verify_med = [medians.get(pid, bench.get("pooled_median_error_pct") or 0) if pid != GASOLINE_BASELINE_ID else 0 for pid in fuel_order]

    x = np.arange(len(fuel_order))
    width = 0.2
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")

    ax = axes[0]
    ax.bar(x - width, renewable, width, label="Renewable rank", color="#059669")
    ax.bar(x, efficiency, width, label="Thermal efficiency", color="#2563eb")
    ax.bar(x + width, fsot_score, width, label="FSOT score", color="#7c3aed")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Normalized metric (engine simulator)")
    ax.set_title("FSOT-designed fuels vs gasoline — Prius 1.8L Atkinson")
    ax.legend(fontsize=8, loc="upper left")
    ax.axvline(len(FSOT_DESIGNED_FUEL_IDS) - 0.5, color="#94a3b8", linestyle="--", linewidth=1)
    ax.text(len(FSOT_DESIGNED_FUEL_IDS) - 0.45, 1.02, "baseline →", fontsize=7, color="#64748b")

    ax2 = axes[1]
    designed = [medians.get(pid, 0) for pid in FSOT_DESIGNED_FUEL_IDS]
    ax2.barh(
        [DISPLAY_NAMES.get(pid, pid) for pid in FSOT_DESIGNED_FUEL_IDS],
        designed,
        color="#1d4ed8",
        alpha=0.85,
    )
    ax2.axvline(0.5, color="#dc2626", linestyle="--", linewidth=1.2, label="0.5% verification gate")
    ax2.axvline(0.05, color="#f59e0b", linestyle=":", linewidth=1.0, label="0.05% tier aspiration")
    pooled = float(bench.get("pooled_median_error_pct") or 0)
    ax2.axvline(pooled, color="#059669", linestyle="-", linewidth=1.5, label=f"panel pooled {pooled:.3f}%")
    ax2.set_xlabel("FSOT scalar error % (median per fuel)")
    ax2.set_title("Per-fuel verification precision (novel molecular states)")
    ax2.legend(fontsize=7, loc="lower right")
    ax2.set_xlim(0, max(0.06, max(designed + [pooled]) * 1.4))

    fig.suptitle(
        f"Fuel Lab verified desktop evidence — {bench.get('record_count', '?')} records, "
        f"pooled {pooled:.3f}%",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)

    return {
        "fuels": fuel_order,
        "record_count": bench.get("record_count"),
        "pooled_median_error_pct": pooled,
        "per_fuel_median_error_pct": medians,
        "engine_sim": {pid: sim.get(pid) for pid in fuel_order if pid in sim},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build verified desktop fuel comparison figure")
    parser.add_argument("--output", type=Path, default=FIG_DIR / "verified_desktop_fuels.png")
    args = parser.parse_args()

    if not CACHE.exists():
        raise SystemExit(f"Missing cache — run ingest_tier88_application_wiring.py --deep first: {CACHE}")

    meta = figure_verified_desktop_fuels(args.output)
    manifest_path = args.output.parent / "verified_desktop_fuel_figure_manifest.json"
    manifest_path.write_text(json.dumps({"figure": str(args.output.name), **meta}, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  fuels: {len(FSOT_DESIGNED_FUEL_IDS)} designed + gasoline baseline")
    print(f"  records: {meta.get('record_count')}  pooled: {meta.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())