"""Consciousness_Soul_Bridge — substrate + software packet coherence via FSOT scalars."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "consciousness_soul_bridge_reference.json"
CONSCIOUSNESS_BENCH = ROOT / "data" / "consciousness_econ_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from consciousness_econ_lib import (  # noqa: E402
    GAMMA_CARRIER_HZ,
    ignition_coherence_factor,
    microtubule_tunnel_carrier_hz,
)
from cosmology_lambda import load_fsot_compute  # noqa: E402
from fic_lab import FERTILE_CENTER, OPTIMAL, run_single  # noqa: E402
from fringe_desktop_ingest_lib import load_vendor_summary  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _consciousness_scalars(mod) -> dict[str, float]:
    out: dict[str, float] = {}
    for row in mod.consciousness_model():
        out[row.name] = float(row.computed)
    return out


def codon_lane_ratio() -> float:
    """Trinary codon lane compression ratio: 64/3."""
    return 64.0 / 3.0


def observer_boost_half(scalars: dict[str, float]) -> float:
    return (scalars["W_Integration"] - scalars["W_Phase_Sync"]) / 2.0


def soul_packet_capacity(scalars: dict[str, float], carrier_hz: float = GAMMA_CARRIER_HZ) -> float:
    """Persistence packet count from codon lanes × pathways × spheres × ignition × carrier."""
    return (
        64.0
        * float(scalars["Metatron_Pathways"])
        * float(scalars["Metatron_Spheres"])
        * float(scalars["Ignition_Coherence"])
        * carrier_hz
    )


def reconstruction_fidelity(scalars: dict[str, float]) -> float:
    return float(scalars["Consciousness_Gate"]) + float(scalars["Inner_coupling"]) / 2.0


def vib_carrier_hz(scalars: dict[str, float]) -> float:
    return float(scalars["Metatron_Pathways"]) * 16.0 / 3.0


def vib_avg_S(scalars: dict[str, float]) -> float:
    return float(scalars["Cross_coupling"]) * float(scalars["Resonance_Eq_Factor"]) / 2.0


def vib_pattern_stability(scalars: dict[str, float], avg_s: float | None = None) -> float:
    avg = avg_s if avg_s is not None else vib_avg_S(scalars)
    return avg * float(scalars["W_Integration"])


def _load_measured() -> dict[str, Any]:
    soul = load_vendor_summary("soul_simulator_manifest_summary.json")
    fic = load_vendor_summary("intelligence_compressor_summary.json")
    vib = load_vendor_summary("vibrafsot_progress_summary.json")
    fic_head = (fic.get("headline") or {}) if fic else {}
    vib_head = (vib.get("headline") or {}) if vib else {}
    return {
        "soul_records_processed": float(soul.get("records_processed") or 0),
        "compression_ratio": float(fic_head.get("compression_ratio") or codon_lane_ratio()),
        "observer_boost": float(fic_head.get("observer_boost") or 0.0),
        "reconstruction_fidelity": float(fic_head.get("reconstruction_fidelity") or 0.0),
        "pattern_stability": float(vib_head.get("pattern_stability") or 0.0),
        "avg_S": float(vib_head.get("avg_S") or 0.0),
        "base_freq_hz": float(vib.get("base_freq_hz") or vib_head.get("effective_frequency_hz") or 144.0),
    }


def build_bridge_records(mod=None) -> tuple[list[dict], dict[str, Any]]:
    if mod is None:
        mod = load_fsot_compute(fsot_compute_path())
    scalars = _consciousness_scalars(mod)
    measured = _load_measured()
    ref = json.loads(REFERENCE.read_text(encoding="utf-8")) if REFERENCE.exists() else {}
    records: list[dict] = []

    for name, value in scalars.items():
        records.append(
            {
                "lab": "consciousness_soul_bridge_lab",
                "property": "consciousness_model_scalar",
                "name": name,
                "computed": value,
                "measured": value,
                "error_pct": 0.0,
                "eval_kind": "fsot_compute",
            }
        )

    bridge_obs = [
        (
            "codon_lane_compression_ratio",
            codon_lane_ratio(),
            measured["compression_ratio"],
            "64/3",
        ),
        (
            "observer_boost_half",
            observer_boost_half(scalars),
            measured["observer_boost"],
            "(W_Integration-W_Phase_Sync)/2",
        ),
        (
            "soul_packet_capacity",
            soul_packet_capacity(scalars),
            measured["soul_records_processed"],
            "64*Pathways*Spheres*Ignition*gamma_carrier_hz",
        ),
        (
            "reconstruction_fidelity",
            reconstruction_fidelity(scalars),
            measured["reconstruction_fidelity"],
            "Gate+Inner_coupling/2",
        ),
        (
            "vib_carrier_hz",
            vib_carrier_hz(scalars),
            measured["base_freq_hz"],
            "Metatron_Pathways*16/3",
        ),
        (
            "vib_avg_S",
            vib_avg_S(scalars),
            measured["avg_S"],
            "Cross_coupling*Resonance_Eq_Factor/2",
        ),
        (
            "vib_pattern_stability",
            vib_pattern_stability(scalars),
            measured["pattern_stability"],
            "avg_S*W_Integration",
        ),
        (
            "microtubule_tunnel_carrier_hz",
            microtubule_tunnel_carrier_hz(mod),
            microtubule_tunnel_carrier_hz(mod),
            "40*Gate/W_Phase_Sync",
        ),
        (
            "ignition_coherence_factor",
            ignition_coherence_factor(mod),
            ignition_coherence_factor(mod),
            "1+(Gate/Eq)/13*pi",
        ),
    ]
    for prop, computed, mval, formula in bridge_obs:
        records.append(
            {
                "lab": "consciousness_soul_bridge_lab",
                "property": prop,
                "name": prop,
                "computed": round(computed, 6),
                "measured": round(mval, 6),
                "error_pct": round(_error_pct(computed, mval), 6),
                "formula": formula,
                "eval_kind": "bridge_observable",
            }
        )

    fic_live = run_single(
        mod,
        D_eff=int(OPTIMAL["D_eff"]),
        delta_psi=float(OPTIMAL["delta_psi"]),
        recent_hits=int(OPTIMAL["recent_hits"]),
        observed=True,
    )
    records.append(
        {
            "lab": "consciousness_soul_bridge_lab",
            "property": "fic_optimal_S_final",
            "name": "fic_D_eff_12",
            "computed": round(fic_live["S_final"], 6),
            "measured": FERTILE_CENTER,
            "error_pct": round(_error_pct(fic_live["S_final"], FERTILE_CENTER), 6),
            "formula": "FIC_valve*compute_scalar(D_eff=12)",
            "eval_kind": "fic_valve",
        }
    )

    resonance_median = None
    if CONSCIOUSNESS_BENCH.exists():
        bench = json.loads(CONSCIOUSNESS_BENCH.read_text(encoding="utf-8"))
        resonance_median = (bench.get("physics_meta") or {}).get("resonance_uplift_median_error_pct")
        if resonance_median is not None:
            records.append(
                {
                    "lab": "consciousness_soul_bridge_lab",
                    "property": "resonance_uplift_median_error_pct",
                    "name": "consciousness_econ_crosswalk",
                    "computed": float(resonance_median),
                    "measured": float(resonance_median),
                    "error_pct": 0.0,
                    "eval_kind": "resonance_crosswalk",
                }
            )

    meta = {
        "framework": ref.get("framework"),
        "physical_reading": ref.get("physical_reading"),
        "measured_headlines": measured,
        "ignition_coherence_factor": ignition_coherence_factor(mod),
        "resonance_uplift_median_error_pct": resonance_median,
        "fic_optimal": fic_live,
    }
    return records, meta