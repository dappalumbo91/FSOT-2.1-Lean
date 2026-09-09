#!/usr/bin/env python3
"""Ledger of residuals we will not stuff into the 0.5% gate.

Ugly residuals are APPLY diagnoses: wrong object or wrong D_eff.
They stay isolated until the interface is named. No new coefficient.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "docs" / "ISOLATED_RESIDUALS.md"
OUT_JSON = ROOT / "data" / "isolated_residuals.json"
PIN = "D1D38A"


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _mat_opt_s_ratio_err() -> float | None:
    try:
        import sys

        sys.path.insert(0, str(ROOT / "vendor"))
        from fsot_compute import domain_scalar  # noqa: E402

        sm = abs(float(domain_scalar("Materials_Science")))
        so = abs(float(domain_scalar("Optics")))
        return abs(sm / so - 1.0) * 100.0
    except Exception:
        return None


def _phi6_wrong_object_err() -> tuple[float, float]:
    """Retired φ⁶ vs 16.35 d residual (measured denom), plus live T_activity."""
    orifice = _load(ROOT / "results" / "frb_orifice_outgassing_outcome.json")
    phi6_err = orifice.get("rejected_phi6_error_pct")
    t_err = orifice.get("activity_season_error_pct")
    return (
        None if phi6_err is None else float(phi6_err),
        None if t_err is None else float(t_err),
    )


def main() -> int:
    frb = _load(ROOT / "results" / "frb_interface_diagnosis.json")
    mat_s = _mat_opt_s_ratio_err()
    phi6_err, t_act_err = _phi6_wrong_object_err()
    open_items = [
        {
            "id": "ISO-SHOES-CLASS-BIN",
            "error_pct": 1.00,
            "verdict": "WRONG_OBJECT_ISOLATED",
            "applied": "SH0ES published 73.04 as the ρ=5.05 class bin (73.773)",
            "why": "73.04 is a three-rung mixture, not the class bin. Chain 72.856 vs 73.04 is 0.252%.",
            "correct": "Kill the class row on the 2.5% band; score the chain; do not retune ρ",
            "not": "Move ρ 5.05→4.36 to swallow 1%.",
            "doc": "docs/SH0ES_LADDER_DIAGNOSIS.md",
        },
    ]
    interconnect = _load(ROOT / "results" / "between_scale_interconnect_outcome.json")
    look_err = (interconnect.get("channel_median_error_pct") or {}).get("mat_opt_S_ratio")
    remedied = [
        {
            "id": "ISO-FRB-200x1pdens",
            "error_pct": frb.get("median_error_pct_200x1pdens"),
            "verdict": "REMEDIED_WRONG_APPLY",
            "applied": "DM_excess ≈ 200·(1+local_sky_density)",
            "why": (
                "IGM path (Cosmology D=25) vs H0 angular kernel (±0.2). "
                "Formula trapped in ~160–240 pc; measured excess 15–580. Sign wrong. "
                "Orifice replaced it — not an open isolate."
            ),
            "correct": "PRED-084 orifice (width×fluence vs e·POOF). PRED-052 200 class. PRED-076 kernel is angular grammar only.",
            "not": "Keep 66% on the open isolate list. Stuff 66% into 0.5%. Fit β. Retune 200. Reuse the formula.",
            "doc": "docs/FRB_INTERFACE_DIAGNOSIS.md",
        },
        {
            "id": "ISO-FRB-PHI6-DAYS",
            "error_pct": phi6_err,
            "verdict": "REMEDIED_WRONG_OBJECT",
            "applied": "FRB20180916B 16.35 d vs φ⁶ d (compactification count)",
            "why": (
                "16.35 d is the saloon-door activity season, not a compactification "
                "tick. φ⁶ is the wrong object. Live handle is T=5π+1/φ days"
                + (f" ({t_act_err:.3f}%)." if t_act_err is not None else ".")
            ),
            "correct": "T_activity = D_particle·π + 1/φ days (Particle orifice cycle + Omori c rest)",
            "not": "0.5%-gate φ⁶. Stuff 2πφ² (~0.61%). Keep 8.9% as an open isolate.",
            "doc": "docs/FRB_ORIFICE.md",
        },
        {
            "id": "ISO-MAT-OPT-S-RATIO",
            "error_pct": mat_s,
            "verdict": "REMEDIED_WRONG_APPLY",
            "applied": "|S_Materials|/|S_Optics| vs 1 (engine §25 Cross_Opt_QO test)",
            "why": (
                "vs 1 is the same-C same-δψ test. Materials δψ=1/2 is the body/mass look; "
                "Optics δψ=3/5 is the light look. C does not enter S. The 18% is that "
                "observer-phase fold (T1 perception, D9), not a failed n/ρ tissue. "
                "Closed form |1+T1_mat|/|1+T1_opt| matches live |S| (T3 leftover 0%)."
                + (
                    f" Live handle vs PhysChem/Chem is {float(look_err):.3f}%."
                    if look_err is not None
                    else ""
                )
            ),
            "correct": (
                "T1 view (D9): |S_i|/|S_j|=|1+T1_i|/|1+T1_j|. "
                "Fold the look-split onto Physical_Chemistry/Chemistry (same 0.5/0.6 at D=8). "
                "CRC n/ρ dual-route. Ice n vs φ²/2."
            ),
            "not": "Stuff ~18% into 0.5%. Keep vs 1 as an open isolate. A new C or δψ. Pad the pooled median with the T1 identity.",
            "doc": "docs/SCALE_INTERCONNECT_PHYSICS.md §8",
        },
    ]
    ts = datetime.now(timezone.utc).isoformat()
    payload = {
        "generated_at": ts,
        "pin": PIN,
        "policy": [
            "do_not_stuff_ugly_into_0_5pct",
            "diagnose_interface_first",
            "no_new_coefficient",
            "remedied_wrong_apply_is_not_an_open_isolate",
        ],
        "items": open_items,
        "remedied": remedied,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Isolated residuals — do not stuff",
        "",
        f"*Generated {ts} · pin {PIN}*",
        "",
        "If a residual is huge and everything else is sub-percent, the mathematics",
        "is usually **applied to the wrong object** (wrong \(D_{\mathrm{eff}}\), wrong",
        "split, class vs chain). Isolate it. Name the interface. Do **not** add a",
        "coefficient so the 0.5% gate looks pretty.",
        "",
        "Once the right object is named and gated, the ugly number is **remedied** —",
        "retired formula, do-not-use note — **not** an open isolate.",
        "",
        "**Refresh:** `python scripts/diagnose_frb_dm_interface.py` then",
        "`python scripts/build_frb_orifice_benchmark.py` then this script.",
        "",
        "## Open isolates",
        "",
        "| ID | Error | Verdict | Why | Next apply |",
        "|----|------:|---------|-----|------------|",
    ]
    for it in open_items:
        e = it.get("error_pct")
        e_s = "—" if e is None else f"**{float(e):.2f}%**"
        lines.append(
            f"| `{it['id']}` | {e_s} | {it['verdict']} | {it['why']} | {it['correct']} |"
        )
    lines += [
        "",
        "## Remedied — retired formulas (do not reuse, do not keep open)",
        "",
        "| ID | Retired error | Verdict | Why | What replaced it |",
        "|----|--------------:|---------|-----|------------------|",
    ]
    for it in remedied:
        e = it.get("error_pct")
        e_s = "—" if e is None else f"**{float(e):.2f}%**"
        lines.append(
            f"| `{it['id']}` | {e_s} | {it['verdict']} | {it['why']} | {it['correct']} |"
        )
    lines += [
        "",
        "## Rules",
        "",
        "1. Report the ugly number in `results/`.",
        "2. Name the object that was applied vs the object science measured.",
        "3. If they differ, the residual is not a failed 0.5% central.",
        "4. When the right object is gated, move the ugly number to **remedied**.",
        "5. Forbidden: β-fit, ρ-retune, identity pads, moving the green gate,",
        "   keeping a remedied wrong-apply on the open isolate list.",
        "",
        "Related: [`APPLY.md`](APPLY.md) · [`OBJECT_SCORING.md`](OBJECT_SCORING.md) ·",
        "[`FRB_INTERFACE_DIAGNOSIS.md`](FRB_INTERFACE_DIAGNOSIS.md) ·",
        "[`FRB_ORIFICE.md`](FRB_ORIFICE.md) ·",
        "[`SH0ES_LADDER_DIAGNOSIS.md`](SH0ES_LADDER_DIAGNOSIS.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    for it in open_items:
        print(f"  OPEN {it['id']} err={it.get('error_pct')} {it['verdict']}")
    for it in remedied:
        print(f"  REMEDIED {it['id']} err={it.get('error_pct')} {it['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
