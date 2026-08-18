#!/usr/bin/env python3
"""Diagnose the SH0ES 1% leftover — no retune, no new coefficient.

Reads frozen multi-tool + sightline JSON and writes:
  results/sh0es_ladder_diagnosis.json
  docs/SH0ES_LADDER_DIAGNOSIS.md

Does **not** rewrite predictions/sector_h0_seed.json.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "predictions" / "h0_multi_tool_predictions.json"
SIGHT = ROOT / "predictions" / "h0_sightline_predictions.json"
OUT_JSON = ROOT / "results" / "sh0es_ladder_diagnosis.json"
OUT_MD = ROOT / "docs" / "SH0ES_LADDER_DIAGNOSIS.md"

H0_G = 68.44005682979427
EPS = 0.015431


def _implied_rho(h_lit: float) -> float:
    return (float(h_lit) / H0_G - 1.0) / EPS


def _h0_of_rho(rho: float) -> float:
    return H0_G * (1.0 + float(rho) * EPS)


def _err_pct(computed: float, measured: float) -> float:
    return abs(computed - measured) / abs(measured) * 100.0


def main() -> int:
    tools_doc = json.loads(TOOLS.read_text(encoding="utf-8"))
    sight = json.loads(SIGHT.read_text(encoding="utf-8"))

    rows = []
    for t in tools_doc.get("tools") or []:
        lit = float(t["literature_anchor_h0"])
        pred = float(t["fsot_predicted_h0"])
        rho = float(t["bubble_density_model"])
        implied = _implied_rho(lit)
        rows.append(
            {
                "name": t["name"],
                "tool_class": t["tool_class"],
                "literature": lit,
                "fsot": pred,
                "rho_assigned": rho,
                "rho_implied_by_literature": round(implied, 4),
                "rho_overshoot": round(rho - implied, 4),
                "error_pct": float(t["error_vs_literature_pct"]),
            }
        )

    cepheid = [r for r in rows if r["tool_class"] == "local_ladder_cepheid"]
    cmb = [r for r in rows if r["tool_class"] == "early_universe_cmb"]
    trgb = [r for r in rows if r["tool_class"] == "intermediate_ladder"]

    hosts = sight.get("hosts") or []
    anchors = [h for h in hosts if h.get("method") in {"TRGB_anchor", "Maser_anchor"}]
    cep_hosts = [h for h in hosts if h.get("method") == "SH0ES_Cepheid"]
    host_mean = float(sight.get("host_mean_fsot_h0") or 0.0)
    lit = float(sight.get("sh0es_literature_anchor") or 73.04)
    class_pred = next(r["fsot"] for r in rows if r["name"] == "sh0es_hst_cepheid")

    diagnosis = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "policy": "do_not_retune_rho_to_hit_73.04",
        "h0_global": H0_G,
        "epsilon": EPS,
        "class_bin": {
            "name": "sh0es_hst_cepheid",
            "rho_assigned": 5.05,
            "fsot": class_pred,
            "literature": 73.04,
            "error_pct": 1.004045,
            "rho_implied_by_73_04": round(_implied_rho(73.04), 4),
            "overshoot_km_s_mpc": round(class_pred - 73.04, 4),
        },
        "host_mixture_already_computed": {
            "host_count": len(hosts),
            "anchor_count": len(anchors),
            "cepheid_host_count": len(cep_hosts),
            "anchor_h0": [round(float(h["fsot_predicted_h0"]), 4) for h in anchors],
            "cepheid_host_span": [
                round(min(float(h["fsot_predicted_h0"]) for h in cep_hosts), 4),
                round(max(float(h["fsot_predicted_h0"]) for h in cep_hosts), 4),
            ],
            "host_mean_fsot_h0": host_mean,
            "error_vs_73_04_pct": round(_err_pct(host_mean, lit), 4),
        },
        "class_means_error_pct": {
            "early_universe_cmb": round(sum(r["error_pct"] for r in cmb) / max(len(cmb), 1), 4),
            "intermediate_ladder": round(sum(r["error_pct"] for r in trgb) / max(len(trgb), 1), 4),
            "local_ladder_cepheid": round(sum(r["error_pct"] for r in cepheid) / max(len(cepheid), 1), 4),
        },
        "tools": rows,
        "unsolved": [
            "no_per_host_published_H0_to_score_sightlines_individually",
            "NIR_wesenheit_W_H_primary_candle",
        ],
        "filled": [
            "ladder_chain_information_weighted_mixture",
            "host_local_angular_sky_density",
            "cepheid_PL_slope_gamma_intercept",
        ],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(diagnosis, indent=2), encoding="utf-8")
    OUT_MD.write_text(_md(diagnosis, anchors, cep_hosts, rows), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  class 73.773 vs 73.04 (1.00%) · host-mean {host_mean:.3f} vs 73.04 "
        f"({diagnosis['host_mixture_already_computed']['error_vs_73_04_pct']}%)"
    )
    return 0


def _md(doc: dict, anchors: list, cep_hosts: list, rows: list) -> str:
    cmb_e = doc["class_means_error_pct"]["early_universe_cmb"]
    trgb_e = doc["class_means_error_pct"]["intermediate_ladder"]
    cep_e = doc["class_means_error_pct"]["local_ladder_cepheid"]
    mix = doc["host_mixture_already_computed"]
    cls = doc["class_bin"]

    tool_lines = [
        "| Tool | Class | Lit | FSOT | ρ assigned | ρ implied | err % |",
        "|------|-------|----:|-----:|-----------:|----------:|------:|",
    ]
    for r in sorted(rows, key=lambda x: x["literature"]):
        tool_lines.append(
            f"| {r['name']} | {r['tool_class']} | {r['literature']:.2f} | "
            f"{r['fsot']:.3f} | {r['rho_assigned']:.2f} | {r['rho_implied_by_literature']:.2f} | "
            f"{r['error_pct']:.3f} |"
        )

    anchor_lines = "\n".join(
        f"| {h['host']} | {h['method']} | {h['sky_sector']} | **{h['fsot_predicted_h0']:.3f}** |"
        for h in anchors
    )

    return f"""# Why SH0ES is the 1% leftover

**Pin:** D1D38A · **policy:** do **not** retune ρ to hit 73.04  
**Regenerate:** `python scripts/diagnose_sh0es_ladder.py`  
**Machine:** [`../results/sh0es_ladder_diagnosis.json`](../results/sh0es_ladder_diagnosis.json)

This is a diagnosis, not a retune. The 1% class-bin leftover is real. Stuffing SH0ES into the 0.5% green gate by moving ρ from 5.05 → 4.36 is forbidden.

**Filled (2026-08-18):** the published 73.04 is now residual-gated as the information-weighted ladder chain — [`SH0ES_Ladder_Chain`](../data/sh0es_ladder_chain_benchmark.json) · **72.856 vs 73.04 (0.252%)**. Frozen class row stays at 73.773. See [`../results/sh0es_ladder_chain_outcome.json`](../results/sh0es_ladder_chain_outcome.json).

---

## Short answer

SH0ES is not a second cosmology, and we are not missing the Hubble tension.

Planck is **0.024%**. Freedman JWST TRGB is **0.005%**. JAGB/Miras is **0.03%**. Those instruments already sit on the BH→WH sector formula

\\[
H_0^{{\\mathrm{{tool}}}} = H_0^{{\\mathrm{{global}}}}\\,(1 + \\rho\\,\\varepsilon),
\\qquad H_0^{{\\mathrm{{global}}}} = 68.440,\\quad \\varepsilon = 0.015431.
\\]

The leftover is this: we scored the **published SH0ES central** as one **class bin** (ρ = 5.05 → **73.773**) while Riess publishes a **three-rung ladder average** (**73.04**). Those rungs do not all live at ρ = 5.05.

Implied ρ to hit 73.04 exactly: **{cls['rho_implied_by_73_04']}**. Assigned class ρ: **5.05**. Overshoot: **{cls['overshoot_km_s_mpc']} km/s/Mpc** (1.00%, 0.7σ of SH0ES ±1.04). Inside the **2.5%** contested band on purpose.

---

## What SH0ES is actually looking at

SH0ES is not “the local universe” as one number. It is three rungs averaged into one H₀:

| Rung | What it sees | FSOT already assigns |
|------|----------------|----------------------|
| Geometric anchors | NGC 4258 maser, LMC DEBs, MW parallax | LMC **70.215** · NGC 4258 **70.389** — TRGB/Freedman-like, ρ ~ 1.7 |
| Cepheid PL in SN Ia hosts | Young disk Cepheids in ~20 star-forming galaxies (crowding, metallicity) | **73.47–74.16** — inflated local ladder |
| SN Ia Hubble flow | SNe whose absolute magnitude was *set* by those Cepheids | inherits the host mix |

CMB sees the last-scattering sound horizon (depleted sector ρ = −1).  
Freedman JWST TRGB sees **old** halo/disk tip-of-RGB stars — a different stellar population, different galactic real estate, ρ = 1.85, **0.005%**.  
BAO sees a baryon-acoustic ruler between those walls.

SH0ES sees **young Cepheids in the same galaxies that hosted SN Ia**, then uses those SNe as the Hubble-flow candle. That is a different coupling to the fluid than TRGB or Planck. The sector model already says that. The 1% is not “we forgot Cepheids exist.”

---

## The 1% is a mixture error, not a missing H₀

Per-host sightlines are already computed (`predictions/h0_sightline_predictions.json`, 22 hosts):

| Host | Method | Sector | FSOT H₀ |
|------|--------|--------|--------:|
{anchor_lines}

Cepheid SN hosts span **{mix['cepheid_host_span'][0]:.2f}–{mix['cepheid_host_span'][1]:.2f}**.

| Readout | FSOT | vs 73.04 |
|---------|-----:|---------:|
| Class bin ρ = 5.05 (what the tool row uses) | **73.773** | **1.00%** |
| Equal-weight host mixture (already on disk) | **{mix['host_mean_fsot_h0']:.3f}** | **{mix['error_vs_73_04_pct']}%** |

The published 73.04 sits between the **mild anchors** (~70.3) and the **hot SN hosts** (~73.5–74.2). A single ρ = 5.05 pretends the whole experiment lives in the hottest bin. That is what we are not solving for: **the ladder average is not a single-sector readout.**

Mean error by tool class (25-tool table):

| Class | Mean err % |
|-------|-----------:|
| Early-universe CMB | {cmb_e:.3f} |
| Intermediate ladder (TRGB / JAGB / Carnegie) | {trgb_e:.3f} |
| Local Cepheid ladder (SH0ES family) | {cep_e:.3f} |

The Cepheid *family* is the outlier cluster (SH0ES HST 1.00%, SH0ES JWST 1.08%, JWST Cepheid Riess 1.18%). Things calibrated *to* that ladder (Pantheon+ SH0ES) inherit it. Freedman TRGB does not.

---

## What we are still not solving for

Filled this pass: ladder mixture, host-local sky, and Cepheid PL interconnects (`CEPHEID_PL_PHYSICS.md`). Still labeled:

1. **No per-host published H₀.** Riess publishes the ladder average.
2. **NIR Wesenheit \(W_H\)** — optical table only. Crowding stays T1.

---

## What we will not do

| Temptation | Why not |
|------------|---------|
| Set ρ = {cls['rho_implied_by_73_04']} to hit 73.04 | Forbidden LSQ. That is stuffing SH0ES into the 0.5% gate. |
| Average 67.4 and 73.04 and call it H₀ | Two sectors, one fluid. PRED-001 is the *bridge*, not a third cosmology. |
| Blame “SH0ES is wrong” | 0.73 km/s/Mpc is 0.7σ of ±1.04. The class bin is coarse, not a failed pin. |
| Invent a Cepheid metallicity knob | eta_eff/2 is seed-closed; do not LSQ Z_W on R22. |

---

## Full 25-tool inversion (frozen predictions)

ρ_implied = (H_lit / 68.440 − 1) / 0.015431. Freedman and Planck were placed on that inversion. SH0ES was placed in the “most inflated local ladder” class bin instead.

{chr(10).join(tool_lines)}

Kill: if someone changes `predictions/sector_h0_seed.json` ρ for `sh0es_hst_cepheid` to close the 1%, that commit is a policy fail. Score a *mixture* readout in `results/` when we promote the host-mean; do not rewrite the frozen class row.

Related: [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md) · [`CONCEPTS.md`](CONCEPTS.md) C3 · `predictions/h0_sightline_predictions.json`
"""


if __name__ == "__main__":
    raise SystemExit(main())
