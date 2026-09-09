#!/usr/bin/env python3
"""Scale triangulation + frozen-state potentials for dynamic Earth tanks.

The 39 km vs 978 km miss is not a kernel retune. It is scoring fold d=1 of a
d=25 valve. orifice_scale(L, d) = L · POOF · d / 25. κ_ij names which tanks
can take the dump. Frozen valve_state splits into discrete potentials
(cell POOF, transfer, quiet hold) — seed-split, not a fitted probability.

Does not rewrite issued JSON. Does not retune kernel km, POOF, or ρ.
Public cell kill_if stays the score object.

Refresh: python scripts/build_dynamic_system_triangulation.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_earth_fluid_forecast import (  # noqa: E402
    CEILING_D,
    POOF,
    R_EARTH_KM,
    SUCTION,
    TANK_DOMAIN,
    apply_dynamic_fields,
    cycle_km,
    f,
    fold_from_orifice_km,
    kappa_named,
    kernel_km,
    orifice_scale_km,
    tank_kinds,
    valve_split,
)

ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
SCORE_DIR = ROOT / "results" / "dated_forecast_scores"
DIAG_JSON = ROOT / "results" / "planetary_cycle_kill_diagnosis.json"
OUT_JSON = ROOT / "results" / "dynamic_system_triangulation.json"
OUT_MD = ROOT / "docs" / "DYNAMIC_SYSTEM_TRIANGULATION.md"

VERDICT_TO_BRANCH = {
    "transferred_poof": "transferred_poof",
    "transferred_weather": "transferred_poof",
    "already_poofed": "quiet_hold",
    "fluid_released": "quiet_hold",
    "issue_bar": "quiet_hold",
    "playbook_bar": "cell_poof",
    "honest_quiet": "quiet_hold",
    "fluid_loaded": "unexpected_poof",
    "honest_quiet_load": "unexpected_poof",
    "wrong_gage": None,
    "solar_coupled": "transferred_poof",
}


def _assert_identities() -> dict[str, float]:
    k = kernel_km()
    c = cycle_km()
    o1 = orifice_scale_km(R_EARTH_KM, 1.0)
    o25 = orifice_scale_km(R_EARTH_KM, CEILING_D)
    d1 = fold_from_orifice_km(k)
    d25 = fold_from_orifice_km(c)
    assert abs(o1 - k) < 1e-12, (o1, k)
    assert abs(o25 - c) < 1e-12, (o25, c)
    assert abs(c - 25.0 * k) < 1e-9, (c, 25.0 * k)
    assert abs(d1 - 1.0) < 1e-9, d1
    assert abs(d25 - 25.0) < 1e-9, d25
    return {
        "kernel_km": k,
        "cycle_km": c,
        "ratio": c / k,
        "fold_from_kernel": d1,
        "fold_from_cycle": d25,
        "poof": f(POOF),
        "suction": f(SUCTION),
    }


def kappa_matrix() -> dict[str, Any]:
    kinds = tank_kinds()
    rows = []
    for a in kinds:
        da = TANK_DOMAIN[a]
        rec = {"kind": a, "domain": da, "couplings": []}
        for b in kinds:
            db = TANK_DOMAIN[b]
            rec["couplings"].append(
                {
                    "kind": b,
                    "domain": db,
                    "kappa": round(kappa_named(da, db), 8),
                    "same": a == b,
                }
            )
        rec["couplings"].sort(key=lambda x: -float(x["kappa"]))
        rows.append(rec)
    return {"kinds": kinds, "rows": rows}


def load_issues() -> list[dict[str, Any]]:
    out = []
    for p in sorted(ISSUE_DIR.glob("*_issue.json")):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for fc in doc.get("forecasts") or []:
            row = dict(fc)
            row["_issue_file"] = p.name
            out.append(row)
    return out


def load_scores() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in SCORE_DIR.glob("*_score.json"):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for r in doc.get("rows") or []:
            fid = str(r.get("id") or "")
            res = str(r.get("result") or "")
            if fid and res:
                out[fid] = res
    return out


def load_diagnosis() -> dict[str, dict[str, Any]]:
    if not DIAG_JSON.is_file():
        return {}
    doc = json.loads(DIAG_JSON.read_text(encoding="utf-8"))
    by_id: dict[str, dict[str, Any]] = {}
    for r in (doc.get("rows") or []) + (doc.get("other_tanks") or []):
        fid = str(r.get("id") or "")
        if fid:
            by_id[fid] = r
    return by_id


def triangulate_one(
    fc: dict[str, Any],
    diag: dict[str, dict[str, Any]],
    scores: dict[str, str],
) -> dict[str, Any]:
    """Forward potentials from the issued freeze. Does not rewrite the issue."""
    kind = str(fc.get("kind") or "")
    loc = fc.get("location") or {}
    pred = fc.get("predicted") or {}
    attached = apply_dynamic_fields(
        {
            "kind": kind,
            "location": loc,
            "predicted": dict(pred),
            "kill_if": fc.get("kill_if"),
        }
    )
    ap = attached.get("predicted") or {}
    fid = str(fc.get("id") or "")
    drow = diag.get(fid) or {}
    verdict = str(drow.get("verdict") or "")
    branch = VERDICT_TO_BRANCH.get(verdict)
    score = scores.get(fid)
    closed = bool(verdict)
    awaiting = score in {None, "", "awaiting"}
    return {
        "id": fid,
        "issue_file": fc.get("_issue_file"),
        "kind": kind,
        "place": (loc.get("name") or ""),
        "valve_state": pred.get("valve_state"),
        "expect_event": pred.get("expect_event"),
        "score_radius_km": loc.get("radius_km"),
        "fold_score_d": ap.get("fold_score_d"),
        "fold_valve_d": ap.get("fold_valve_d"),
        "orifice_score_km": ap.get("orifice_score_km"),
        "orifice_valve_km": ap.get("orifice_valve_km"),
        "neighbor_kinds": ap.get("neighbor_kinds"),
        "potentials": ap.get("potentials"),
        "score": score,
        "closed": closed,
        "diagnosis_verdict": verdict or None,
        "branch_fired": branch,
        "forward": awaiting,
    }


def build() -> dict[str, Any]:
    ident = _assert_identities()
    p_fire, p_hold = valve_split()
    ident["p_fire"] = p_fire
    ident["p_hold"] = p_hold
    matrix = kappa_matrix()
    diag = load_diagnosis()
    scores = load_scores()
    rows = [triangulate_one(fc, diag, scores) for fc in load_issues()]
    closed = [r for r in rows if r["closed"]]
    forward = [r for r in rows if r["forward"]]
    fired = Counter(str(r["branch_fired"]) for r in closed if r["branch_fired"])
    by_kind = Counter(str(r["kind"]) for r in rows)
    by_score = Counter(str(r.get("score") or "unscored") for r in rows)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "policy": [
            "do_not_rewrite_issued_json",
            "do_not_retune_kernel_or_POOF",
            "orifice_scale_L_d_eq_L_POOF_d_over_25",
            "potentials_are_seed_splits_not_calibrated_probabilities",
            "public_kill_stays_on_the_score_object",
        ],
        "identities": ident,
        "kappa": matrix,
        "n": len(rows),
        "n_closed": len(closed),
        "n_forward": len(forward),
        "by_kind": dict(by_kind),
        "by_score": dict(by_score),
        "closed_branch_fired": dict(fired),
        "rows": rows,
        "kill": (
            "a fitted radius to swallow transferred_poof; "
            "calling potential weights a calibrated probability; "
            "rewriting kill_if onto cycle_km; a many-worlds claim"
        ),
    }


def _md(doc: dict[str, Any]) -> str:
    ident = doc["identities"]
    k = ident["kernel_km"]
    c = ident["cycle_km"]
    p_fire = ident["p_fire"]
    p_hold = ident["p_hold"]
    fired = doc["closed_branch_fired"]
    lines = [
        "# Dynamic-system triangulation — fold, tanks, frozen potentials",
        "",
        f"*Generated {doc['generated_at']} · pin D1D38A*",
        "",
        "Matching known tables is already green. Dated misses were **wrong fold**,",
        "not a broken kernel. Normalize the prediction to the area you are scoring,",
        "then emit the tanks that talk at the unfolded valve. That is the n-body",
        "analog: **25 compactified tanks coupled by κ**, not Newton's gravity N-body.",
        "",
        "**Refresh:** `python scripts/build_dynamic_system_triangulation.py`",
        "",
        "Lean: `orifice_scale` · `kernel_km_eq_orifice_scale_one` ·",
        "`cycle_km_eq_orifice_scale_ceiling` in `FSOT/Formal/ScalarEngineStructure.lean`.",
        "Law **D11**. Picture **C14**.",
        "",
        "## Closed form",
        "",
        r"\[",
        r"\mathrm{orifice\_scale}(L,d)=L\cdot\mathrm{POOF}\cdot d/25",
        r"\]",
        "",
        "| Fold | Object | km | Job |",
        "|-----:|--------|---:|-----|",
        f"| 1 | dated cell (score / kill_if) | **{k:.1f}** | one compactified slice |",
        f"| 25 | planetary cycle (coupled tanks) | **{c:.1f}** | arc / trench / basin / solar |",
        "",
        f"Identity: cycle / cell = **{ident['ratio']:.6f}** (must be 25).",
        "Invert: \(d = 25\cdot L_\\mathrm{orifice}/(L_\\mathrm{body}\\cdot\\mathrm{POOF})\).",
        "Solar Kp is issued on the body — that is the planetary tank, not an orifice length.",
        "",
        "## How to normalize to the area you are predicting",
        "",
        "1. Name the **score object** (cell, buoy, gage, Kp). That radius is `kill_if`.",
        "2. Recover its fold \(d_\\mathrm{score}=25\cdot r/(R_\\oplus\\cdot\\mathrm{POOF})\).",
        "3. Coupled tanks always talk at \(d=25\). If \(d_\\mathrm{score}\\ll 25\), the load can dump next door.",
        "4. κ_ij says **which** tanks can take it. Dark folds still couple; silos are institutional.",
        "5. Frozen `valve_state` splits into discrete **potentials**. Weights are",
        f"   POOF/(POOF+SUCTION)=**{p_fire:.4f}** fire and",
        f"   SUCTION/(POOF+SUCTION)=**{p_hold:.4f}** hold, then split across tanks by κ.",
        "   That is valve geometry, **not** a calibrated event probability.",
        "",
        "Do not retune the 39 km kernel to swallow a 978 km dump. Record the transfer.",
        "",
        "## Where tanks interact",
        "",
        "| Kind | Core fold | Strongest other tank (κ) |",
        "|------|-----------|--------------------------|",
    ]
    for rec in doc["kappa"]["rows"]:
        others = [x for x in rec["couplings"] if not x["same"]]
        top = others[0] if others else {}
        lines.append(
            f"| {rec['kind']} | {rec['domain']} | "
            f"{top.get('kind')} ({top.get('kappa')}) |"
        )
    lines += [
        "",
        "Self-κ is always the largest (ΔD=0). Interaction is the off-diagonal.",
        "A tank that does not take the dump is not a failed planet — the attractor",
        "was the coupled tank. Same dampening grammar as uniqueness (free color is",
        "not an attractor). Uniqueness of continuum YM stays `OPEN_NOT_CLAIMED`.",
        "",
        "## Frozen-state potentials (the branches)",
        "",
        "| Valve at issue | Live branches |",
        "|----------------|---------------|",
        "| `loading_suction` | cell_poof · transferred_poof · quiet_hold |",
        "| `post_poof_aftershock` | quiet_hold · omori_aftershock · transferred_poof. **Not** a new mainshock. |",
        "| `released` / `steady` | quiet_hold · unexpected_poof · transferred_poof |",
        "",
        "New issues carry these on `predicted.potentials`. Issued JSON is not rewritten.",
        "",
        "## Closed kills → which branch fired",
        "",
        "Diagnosis already named the why. This table is the same why as a **scored branch**.",
        "",
        "| Branch | Closed kills |",
        "|--------|-------------:|",
    ]
    for name, n in sorted(fired.items(), key=lambda kv: -kv[1]):
        lines.append(f"| `{name}` | {n} |")
    if not fired:
        lines.append("| — | 0 |")
    n_fwd = int(doc["n_forward"])
    n_closed = int(doc["n_closed"])
    lines += [
        "",
        f"Closed kills with a mapped diagnosis: **{n_closed}**. "
        f"Still-open / awaiting (forward potentials): **{n_fwd}**.",
        "2026-09-09 stays frozen; score after `valid_to`. These rows are the live",
        "potentials from that freeze, not a rewrite.",
        "",
        "## Forward sample (open windows)",
        "",
        "| ID | Kind | Valve | Hold | Fire here | Transfer |",
        "|----|------|-------|-----:|----------:|---------:|",
    ]
    fwd = [r for r in doc["rows"] if r.get("forward")]
    shown = 0
    for r in fwd:
        pots = {str(p.get("id")): p for p in (r.get("potentials") or [])}
        hold = float((pots.get("quiet_hold") or {}).get("weight") or 0)
        here = pots.get("cell_poof") or pots.get("omori_aftershock") or pots.get("unexpected_poof") or {}
        tr = pots.get("transferred_poof") or {}
        lines.append(
            f"| `{r['id']}` | {r['kind']} | {r.get('valve_state')} | "
            f"{hold:.3f} | {float(here.get('weight') or 0):.3f} | "
            f"{float(tr.get('weight') or 0):.3f} |"
        )
        shown += 1
        if shown >= 12:
            break
    if shown == 0:
        lines.append("| — | — | — | — | — | — |")
    lines += [
        "",
        "## What this is not",
        "",
        "- A fitted 150 km or 1000 km spring.",
        "- A calibrated probability of the next earthquake.",
        "- Many-worlds / a second H0.",
        "- Rewriting `kill_if` onto `cycle_km`.",
        "- Clock-time hypocenter. S2S vs ECMWF. Prices. Diagnoses.",
        "",
        "Related: [`PLANETARY_CYCLE_CONNECTIVE.md`](PLANETARY_CYCLE_CONNECTIVE.md) ·",
        "[`CONCEPTS.md`](CONCEPTS.md) C14 · [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) D11 ·",
        "[`UNIQUENESS_RESEARCH_SPINE.md`](UNIQUENESS_RESEARCH_SPINE.md).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    doc = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.write_text(_md(doc), encoding="utf-8")
    ident = doc["identities"]
    print(
        f"triangulation n={doc['n']} closed={doc['n_closed']} "
        f"forward={doc['n_forward']} cell={ident['kernel_km']:.1f} "
        f"cycle={ident['cycle_km']:.1f} ratio={ident['ratio']:.6f}"
    )
    print(f"  wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"  wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
