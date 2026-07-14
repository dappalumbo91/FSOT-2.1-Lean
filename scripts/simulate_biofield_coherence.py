#!/usr/bin/env python3
"""FSOT biofield / coherent-observer simulation — grounded in verified scalar engine.

Maps meditative waveform parameters to scalar S and derived AC/CP/MDR metrics.
Anchors to published bio-EM and metabolic ranges (not fiction).
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_compute import C_FACTOR, K, ScalarInput, compute_scalar, mpf  # noqa: E402

# Published anchors (order-of-magnitude, for interpretation only)
BMR_W = 100.0  # adult resting metabolic power ~80–120 W
BRAIN_W = 20.0
HEART_MCG_PT = 50.0  # magnetocardiography pT-scale at chest (typical lab)


@dataclass(frozen=True)
class MindState:
    name: str
    delta_psi: float
    recent_hits: float
    delta_theta: float
    scale: float
    amplitude: float
    acoustic_bleed_mult: float = 1.0
    notes: str = ""


STATES = [
    MindState("waking_scattered", 0.30, 1.0, 1.0, 1.0, 1.0, 1.0,
              "Ordinary attention; high phase variance proxy"),
    MindState("alpha_relaxed", 0.15, 0.3, 0.6, 1.05, 1.02, 1.0,
              "~8–12 Hz relaxed awareness; HRV may begin to cohere"),
    MindState("theta_meditative", 0.10, 0.1, 0.4, 1.08, 1.05, 1.0,
              "~4–8 Hz deep meditative access"),
    MindState("gamma_phase_lock", 0.02, 0.0, 0.15, 1.12, 1.10, 1.0,
              "High synchrony / low Δψ; long-term meditator gamma reports"),
    MindState("synesthesia_bleed", 0.12, 0.2, 0.5, 1.06, 1.04, 1.5,
              "Elevated cross-domain acoustic_bleed (synesthesia analog)"),
    MindState("remote_viewing_proxy", 0.05, 0.0, 0.2, 1.15, 1.12, 1.2,
              "High coherence + constructive T3 coupling (Stargate-scale claim proxy)"),
]


def _scalar_for_state(st: MindState, *, d_eff: int = 14) -> float:
    from fsot_compute import A_BLEED, A_IN  # noqa: WPS433

    si = ScalarInput(
        N=mpf(1),
        P=mpf(1),
        D_eff=mpf(d_eff),
        delta_psi=mpf(st.delta_psi),
        recent_hits=mpf(st.recent_hits),
        delta_theta=mpf(st.delta_theta),
        scale=mpf(st.scale),
        amplitude=mpf(st.amplitude),
        observed=True,
        A_bleed=A_BLEED * mpf(st.acoustic_bleed_mult),
        A_in=A_IN * mpf(st.acoustic_bleed_mult),
    )
    return float(compute_scalar(si))


def _derived_metrics(s: float, st: MindState, baseline_s: float) -> dict:
    ac = s / baseline_s  # aura capacity ratio vs waking
    cp = (1.0 - st.delta_psi) * float(C_FACTOR)  # control precision proxy
    mdr = st.recent_hits + 0.5 * st.delta_psi  # metabolic debt rate proxy
    em_proxy_pt = HEART_MCG_PT * ac  # not a prediction — scaled interpretive anchor
    bmr_frac = min(0.35, 0.08 * ac)  # plausible upper fraction of BMR for neural/cardiac work
    return {
        "S": round(s, 6),
        "AC_ratio": round(ac, 4),
        "CP_proxy": round(cp, 4),
        "MDR_proxy": round(mdr, 4),
        "EM_field_scale_vs_rest_pT": round(em_proxy_pt, 2),
        "max_sustainable_BMR_fraction_est": round(bmr_frac, 4),
    }


def debt_accrual_sim(st: MindState, steps: int = 20, hit_per_step: float = 0.08) -> list[dict]:
    """Simulate sustained high-output: recent_hits accrue unless Δψ is very low."""
    rows = []
    hits = st.recent_hits
    for t in range(steps + 1):
        tmp = MindState(st.name, st.delta_psi, hits, st.delta_theta, st.scale, st.amplitude,
                        st.acoustic_bleed_mult, st.notes)
        s = _scalar_for_state(tmp)
        rows.append({"t": t, "recent_hits": round(hits, 3), "S": round(s, 6)})
        if st.delta_psi > 0.04:
            hits += hit_per_step
        else:
            hits += hit_per_step * 0.35
    return rows


def main() -> int:
    baseline = _scalar_for_state(STATES[0])
    em_domain = _scalar_for_state(
        MindState("EM_baseline", 0.7, 0, 1.0, 1.0, 1.0), d_eff=9
    )
    bio_domain = _scalar_for_state(
        MindState("bio_baseline", 0.35, 0, 1.0, 1.0, 1.0), d_eff=13
    )

    report = {
        "engine": "vendor/fsot_compute.py compute_scalar",
        "K": float(K),
        "C_FACTOR_consciousness": float(C_FACTOR),
        "anchors": {
            "BMR_W": BMR_W,
            "brain_W": BRAIN_W,
            "heart_MCG_pT_reference": HEART_MCG_PT,
            "stargate_program": "CIA/DIA remote viewing (1970s–1995); small contested effect sizes",
            "synesthesia": "documented cross-modal sensory coupling (neuroscience)",
        },
        "domain_baselines": {
            "electromagnetism_D9_S": round(em_domain, 6),
            "biology_D13_S": round(bio_domain, 6),
            "neural_waking_D14_S": round(baseline, 6),
        },
        "mind_states": [],
        "debt_simulation_gamma_lock": debt_accrual_sim(STATES[3]),
    }

    for st in STATES:
        s = _scalar_for_state(st)
        row = {"state": st.name, "notes": st.notes, **_derived_metrics(s, st, baseline)}
        report["mind_states"].append(row)

    out = ROOT / "data" / "biofield_coherence_simulation.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=== FSOT Biofield / Coherent Observer Simulation ===")
    print(f"Waking baseline S = {baseline:.6f}")
    print(f"EM domain (D=9) S = {em_domain:.6f}")
    for row in report["mind_states"]:
        print(
            f"  {row['state']:22s} S={row['S']:.4f}  AC={row['AC_ratio']:.2f}x  "
            f"CP={row['CP_proxy']:.3f}  MDR={row['MDR_proxy']:.3f}"
        )
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())