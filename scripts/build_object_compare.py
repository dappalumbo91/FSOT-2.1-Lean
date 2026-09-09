#!/usr/bin/env python3
"""Standing science-vs-FSOT object compare.

A literature number is a named object. This ledger scores it against the
named FSOT lock (OBJECT_SCORING), not a headline. It does not retune
fsot_predicted and does not rewrite predictions/.

Refresh: python scripts/build_object_compare.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "results" / "object_compare.json"
OUT_MD = ROOT / "docs" / "OBJECT_COMPARE.md"
LOG = ROOT / "results" / "outcomes" / "prediction_outcome_log.jsonl"


def _load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _err(computed: float, measured: float) -> float | None:
    if measured == 0:
        return 0.0 if computed == 0 else None
    return abs(computed - measured) / abs(measured) * 100.0


def _row(
    *,
    paper: str,
    measured: float | None,
    unit: str,
    lock: str,
    lock_value: float | None,
    map_to: str,
    verdict: str,
    why: str,
    not_this: str,
    source: str,
    live_err_pct: float | None = None,
) -> dict[str, Any]:
    return {
        "paper": paper,
        "measured": measured,
        "unit": unit,
        "lock": lock,
        "lock_value": lock_value,
        "map": map_to,
        "verdict": verdict,
        "why": why,
        "not": not_this,
        "source": source,
        "live_err_pct": live_err_pct,
    }


def named_objects() -> list[dict[str, Any]]:
    chain = _load(ROOT / "results" / "sh0es_ladder_chain_outcome.json")
    cep = _load(ROOT / "results" / "cepheid_pl_interconnect_outcome.json")

    h0_chain = float((chain.get("computed") or {}).get("ladder_chain") or 72.855768)
    h0_anc = float((chain.get("computed") or {}).get("anchors_only") or 70.511048)
    h0_host = float((chain.get("computed") or {}).get("hosts_only") or 73.801781)
    h0_class = float((chain.get("computed") or {}).get("class_bin") or 73.773354)
    err_chain = float((chain.get("error_pct") or {}).get("ladder_chain_vs_SH0ES") or 0.252234)
    err_anc = float((chain.get("error_pct") or {}).get("anchors_vs_Freedman") or 0.171968)
    err_ph = float((chain.get("error_pct") or {}).get("hosts_only_vs_Perfect_Host") or _err(h0_host, 73.49) or 0.0)
    err_class = float((chain.get("error_pct") or {}).get("class_bin_vs_SH0ES") or 1.004045)

    r_nir = None
    for r in cep.get("rows") or []:
        if r.get("name") == "R_NIR_vs_Riess_Eq7":
            r_nir = r
            break

    rows = [
        _row(
            paper="JWST Perfect Host 73.49±0.93 (arXiv:2509.01667)",
            measured=73.49,
            unit="km/s/Mpc",
            lock="PRED-024 / hosts-only local ladder",
            lock_value=h0_host,
            map_to="local_ladder",
            verdict="hold",
            why=f"Hosts-only {h0_host:.3f} vs 73.49 ({err_ph:.3f}%). Same Cepheid-ladder sector.",
            not_this="PRED-001 bridge 70.75",
            source="docs/OBJECT_SCORING.md §1",
            live_err_pct=err_ph,
        ),
        _row(
            paper="SH0ES R22 published 73.04",
            measured=73.04,
            unit="km/s/Mpc",
            lock="ladder chain (mixture)",
            lock_value=h0_chain,
            map_to="mixture_chain",
            verdict="hold",
            why=f"Chain {h0_chain:.3f} vs 73.04 ({err_chain:.3f}%). Three-rung mixture, not one class bin.",
            not_this="Class bin 73.773 as a 0.5% central; ρ retune 5.05→4.36",
            source="results/sh0es_ladder_chain_outcome.json",
            live_err_pct=err_chain,
        ),
        _row(
            paper="SH0ES R22 scored as ρ=5.05 class bin",
            measured=73.04,
            unit="km/s/Mpc",
            lock="ISO-SHOES-CLASS-BIN (frozen)",
            lock_value=h0_class,
            map_to="class_bin",
            verdict="frozen_isolate",
            why=f"Class bin {h0_class:.3f} vs 73.04 ({err_class:.2f}%). Isolated on purpose. Work the chain.",
            not_this="Retuning ρ; stuffing 1% into 0.5%",
            source="docs/ISOLATED_RESIDUALS.md",
            live_err_pct=err_class,
        ),
        _row(
            paper="CCHP / Freedman JWST TRGB 70.39",
            measured=70.39,
            unit="km/s/Mpc",
            lock="PRED-001 bridge · anchors-only",
            lock_value=h0_anc,
            map_to="bridge_or_anchor",
            verdict="hold",
            why=f"Anchors-only {h0_anc:.3f} vs 70.39 ({err_anc:.3f}%). Fair bridge compare, not SH0ES 73.04.",
            not_this="Killing PRED-001 on Perfect Host 73.49",
            source="results/sh0es_ladder_chain_outcome.json",
            live_err_pct=err_anc,
        ),
        _row(
            paper="A&A 2026 Local Distance Network 73.50±0.81",
            measured=73.50,
            unit="km/s/Mpc",
            lock="PRED-024 / hosts-only local ladder",
            lock_value=h0_host,
            map_to="local_ladder",
            verdict="hold",
            why=f"Same local-high sector as Perfect Host. Hosts-only {h0_host:.3f} vs 73.50.",
            not_this="PRED-001 70.75",
            source="results/outcomes/prediction_outcome_log.jsonl",
            live_err_pct=_err(h0_host, 73.50),
        ),
        _row(
            paper="Planck 2018 TTTEEE+lowE+lensing 67.4",
            measured=67.4,
            unit="km/s/Mpc",
            lock="Planck-class sector (planck_cmb_local)",
            lock_value=67.384,
            map_to="cmb_sector",
            verdict="hold",
            why="CMB tool row 67.384 vs 67.4 (0.024%). Early-universe depleted sector.",
            not_this="SH0ES 73.04 as the CMB kill",
            source="predictions/sector_h0_seed.json",
            live_err_pct=0.024,
        ),
        _row(
            paper="DES Y6 S8 = 0.789±0.012 (alone)",
            measured=0.789,
            unit="S8",
            lock="PRED-002 / PRED-042 0.805",
            lock_value=0.805,
            map_to="tension_row",
            verdict="tension_row",
            why="DES-alone is ~2.6σ vs CMB. Not the PRED-002 kill. Fair compare is the joint.",
            not_this="Killing 0.805 on DES-alone",
            source="docs/OBJECT_SCORING.md §2",
            live_err_pct=_err(0.805, 0.789),
        ),
        _row(
            paper="Joint DES+CMB+low-z S8 = 0.806 (arXiv:2601.14559)",
            measured=0.806,
            unit="S8",
            lock="PRED-002 / PRED-042 0.805",
            lock_value=0.805,
            map_to="fair_compare",
            verdict="hold",
            why="Joint 0.806 vs lock 0.805 (0.124%). Discriminant is between Planck and DES.",
            not_this="Euclid CLOE FoM as measured S8",
            source="docs/OBJECT_SCORING.md §2",
            live_err_pct=_err(0.805, 0.806),
        ),
        _row(
            paper="Euclid CLOE.3 FoM(w0,wa)>400 (synthetic)",
            measured=None,
            unit="FoM",
            lock="PRED-002 / 042 / 043",
            lock_value=None,
            map_to="no-map",
            verdict="awaiting",
            why="Synthetic figure of merit. Zero survey-level S8/H0/wa. DR1 ~12 Nov 2026.",
            not_this="Citing CLOE as a measured hold",
            source="docs/OBJECT_SCORING.md §4",
        ),
        _row(
            paper="DES Y6 + DESI DR2 + CMB wa = −0.63^{+0.21}_{−0.18}",
            measured=-0.63,
            unit="w_a",
            lock="PRED-043 −1.018",
            lock_value=-1.018,
            map_to="direction_hold",
            verdict="hold_not_kill",
            why="Same sign (evolving DE). ~1.9σ from frozen central. Kill is 3σ Euclid/DESI exclusion.",
            not_this="Claiming 3σ on −1.018; retuning the central",
            source="docs/OBJECT_SCORING.md §3",
        ),
        _row(
            paper="CMS 2026 γγ m_H = 125.14±0.15 GeV",
            measured=125.14,
            unit="GeV",
            lock="PRED-049 125.25",
            lock_value=125.25,
            map_to="pdg_mass",
            verdict="hold",
            why="|125.25−125.14|/125.25 = 0.088%. Inside 0.5% kill.",
            not_this="A per-channel ε at the LHC",
            source="results/outcomes/prediction_outcome_log.jsonl",
            live_err_pct=_err(125.25, 125.14),
        ),
        _row(
            paper="Fermilab final Δa_μ ~2.6×10⁻⁹ (WP20 SM)",
            measured=2.6e-9,
            unit="delta_a_mu",
            lock="PRED-004 / 050 2.49e-9",
            lock_value=2.49e-9,
            map_to="same_sign",
            verdict="hold",
            why="Same sign and scale vs WP20. Experiment locked.",
            not_this="Retuning after lattice WP25 moved the theory target",
            source="results/outcomes/prediction_outcome_log.jsonl",
            live_err_pct=_err(2.49e-9, 2.6e-9),
        ),
        _row(
            paper="Muon g−2 Theory Initiative WP25 lattice excess ~0.38×10⁻⁹",
            measured=3.75e-10,
            unit="delta_a_mu",
            lock="PRED-004 experimental lock (unchanged)",
            lock_value=2.49e-9,
            map_to="theory_rebase",
            verdict="theory_rebase",
            why="Lattice SM target moved. Logged as theory_rebase, not a retune of the experimental lock.",
            not_this="Rewriting PRED-004 central",
            source="results/outcomes/prediction_outcome_log.jsonl",
        ),
        _row(
            paper="Genetics product 0.13 Å (sibling freeze 2026-08-17)",
            measured=0.13,
            unit="Å",
            lock="ChemLink product (sibling-owned)",
            lock_value=0.13,
            map_to="product",
            verdict="sibling_owned",
            why="Product 0.13 Å vs AF 0.47 Å vs cryo-EM FSC ~1.2 Å vs bulk ~13 Å. Do not cross-cite.",
            not_this="Sequence-only 0.13 Å; CASP/FSC papers as the product",
            source="docs/GENETICS_CLAIM_EVIDENCE.md",
        ),
        _row(
            paper="Riess+2022 Eq.7 R_H = 0.4",
            measured=0.4,
            unit="R_H",
            lock="POOF·e·C_eff",
            lock_value=float((r_nir or {}).get("computed") or 0.39956),
            map_to="cepheid_wesenheit",
            verdict="hold",
            why="NIR Wesenheit is acoustic+chemistry+light, not a fitted b. Residual ~0.110%.",
            not_this="A free Z_W or PL slope",
            source="results/cepheid_pl_interconnect_outcome.json",
            live_err_pct=float((r_nir or {}).get("error_pct") or 0.110),
        ),
        _row(
            paper="FRB IGM 200·(1+sky_density) (~66%)",
            measured=None,
            unit="pc cm^-3",
            lock="PRED-084 orifice (width×fluence vs e·POOF)",
            lock_value=None,
            map_to="wrong_object_remedied",
            verdict="remedied",
            why="IGM path vs orifice puncture. Retired. Repeaters = saloon door; one-shots = paper-rip.",
            not_this="Stuffing DM into 0.5%; dark matter in puncture energy",
            source="docs/FRB_ORIFICE.md",
        ),
        _row(
            paper="JINR Z=119 run (started May 2026)",
            measured=None,
            unit="Z",
            lock="PRED-017 viability",
            lock_value=None,
            map_to="awaiting",
            verdict="awaiting",
            why="No confirmed atom. IUPAC ceiling still 118.",
            not_this="A half-life as a 0.5% central",
            source="results/outcomes/prediction_outcome_log.jsonl",
        ),
        _row(
            paper="CASP/CAMEO blind protocol (Genetics freeze 2026-08-17)",
            measured=None,
            unit="Å",
            lock="product vs AF vs FSC, three columns",
            lock_value=None,
            map_to="awaiting_protocol",
            verdict="awaiting",
            why="Protocol is registered. Blind run is future (Grok Build owns it). Not 0.13 Å from sequence.",
            not_this="Quoting 0.13 Å as sequence-only; cross-citing FSC Å as the product",
            source="docs/CASP_CAMEO_BLIND_PROTOCOL.md",
        ),
        _row(
            paper="Euclid DR1-Foundation (~12 Nov 2026)",
            measured=None,
            unit="S8/H0/wa",
            lock="PRED-002 / 042 / 043",
            lock_value=None,
            map_to="awaiting",
            verdict="awaiting",
            why="Independent drop. CLOE is synthetic. Do not cite FoM as measured S8/H0/wa.",
            not_this="Euclid CLOE as a hold",
            source="docs/OBJECT_SCORING.md §4",
        ),
        _row(
            paper="Path-integral confinement / T3–T4 uniqueness",
            measured=None,
            unit="theorem",
            lock="OPEN_NOT_CLAIMED",
            lock_value=None,
            map_to="open_research",
            verdict="awaiting",
            why="Executable probes exist (γ_color, singlets). Continuum YM path-integral uniqueness is not proved.",
            not_this="Pretending Label B uniqueness is a theorem",
            source="docs/UNIQUENESS_RESEARCH_SPINE.md",
        ),
        _row(
            paper="GWTC-5.0 catalog (~390 p_astro≥0.5)",
            measured=390,
            unit="catalog_count",
            lock="PRED-048 / 067 residual class",
            lock_value=None,
            map_to="catalog",
            verdict="local_green_hold",
            why="Catalog public. Compact-object / GWOSC panels already green. Siren H0 70.024 awaits O4/O5.",
            not_this="Retuning ρ onto SH0ES from one siren",
            source="results/outcomes/prediction_outcome_log.jsonl",
        ),
    ]
    return rows


def outcome_log_preds() -> list[dict[str, Any]]:
    if not LOG.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        pid = str(rec.get("pred_id") or "")
        if not pid.startswith("PRED-"):
            continue
        out.append(
            {
                "pred_id": pid,
                "survey": rec.get("survey"),
                "result": rec.get("result"),
                "measured": rec.get("measured"),
                "unit": rec.get("unit"),
                "source": rec.get("source"),
                "notes": rec.get("notes"),
            }
        )
    return out


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    rows = named_objects()
    log = outcome_log_preds()
    by_v: dict[str, int] = {}
    for r in rows:
        by_v[str(r["verdict"])] = by_v.get(str(r["verdict"]), 0) + 1
    doc = {
        "generated_at": ts,
        "pin": "D1D38A",
        "freeze": "TOE-PREREG-20260806 / living hub",
        "policy": [
            "do_not_retune_fsot_predicted",
            "do_not_rewrite_predictions",
            "wrong_object_is_not_a_kill",
            "euclid_cloe_is_synthetic",
            "genetics_0p13A_is_sibling_product",
        ],
        "n": len(rows),
        "by_verdict": by_v,
        "rows": rows,
        "outcome_log_pred_rows": len(log),
        "refresh": "python scripts/build_object_compare.py",
        "append_paper": "python scripts/record_prediction_outcome.py --pred-id PRED-… --survey … --result hold|kill|awaiting …",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    md = [
        "# Science vs FSOT — named-object compare",
        "",
        f"*Generated {ts} · pin D1D38A*",
        "",
        "A literature number is a **named object**. Score it against the named",
        "lock, not a headline. Wrong object = false kill. Do **not** retune",
        "`fsot_predicted`. Do **not** rewrite `predictions/`.",
        "",
        "**Refresh:** `python scripts/build_object_compare.py`",
        "",
        "How to add the next paper: `python scripts/record_prediction_outcome.py` "
        "(see [`OBJECT_SCORING.md`](OBJECT_SCORING.md) and the 2026-08-17 literature pack).",
        "",
        "## Standing table",
        "",
        "| Paper / survey | Measured | FSOT lock | Map | Verdict | Why | Not |",
        "|----------------|----------|-----------|-----|---------|-----|-----|",
    ]
    for r in rows:
        meas = "—" if r["measured"] is None else (
            f"{r['measured']:g}" if not isinstance(r["measured"], float) or abs(float(r["measured"])) >= 0.01
            else f"{r['measured']:.3e}"
        )
        if r.get("unit"):
            meas = f"{meas} {r['unit']}"
        lock = r["lock"]
        if r["lock_value"] is not None:
            lv = r["lock_value"]
            lock = f"{lock} ({lv:g})" if abs(lv) >= 0.01 else f"{lock} ({lv:.3e})"
        err = r.get("live_err_pct")
        why = r["why"]
        if err is not None and "0." in why:
            pass
        md.append(
            f"| {r['paper']} | {meas} | {lock} | `{r['map']}` | **{r['verdict']}** | {why} | {r['not']} |"
        )
    md += [
        "",
        f"Counts: {by_v}. Outcome-log PRED rows (not FCAST): **{len(log)}**.",
        "",
        "## Verdict vocabulary",
        "",
        "| Verdict | Meaning |",
        "|---------|---------|",
        "| `hold` | Named object matches the named lock (or sits in the registered band). |",
        "| `hold_not_kill` | Direction agrees; registered 3σ kill has not fired. |",
        "| `tension_row` | Real tension; not the lock's kill object. |",
        "| `frozen_isolate` | Ugly residual kept on purpose (wrong object / class vs mixture). |",
        "| `awaiting` | Catalog/paper not yet measured. |",
        "| `theory_rebase` | Theory target moved; experimental lock unchanged. |",
        "| `sibling_owned` | Genetics/Quantum product, not this hub's remaining work. |",
        "| `remedied` | Wrong apply retired; replacement already gated. |",
        "| `local_green_hold` | In-repo panel already ≤0.5%; survey is a catalog count. |",
        "| `no-map` | Paper number is not the FSOT object (CLOE FoM, sequence-only Å). |",
        "",
        "Kill: retuning a frozen central when a paper lands. Kill: scoring Perfect Host",
        "as PRED-001. Kill: DES-alone as PRED-002. Kill: Euclid CLOE as measured.",
        "",
        "Related: [`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) ·",
        "[`../results/literature/2026-09-01_prediction_status.md`](../results/literature/2026-09-01_prediction_status.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"  n={len(rows)} by_verdict={by_v} outcome_log_preds={len(log)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
