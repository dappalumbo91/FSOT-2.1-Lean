#!/usr/bin/env python3
"""Build contested-sector future-observation ledger (pre-data differentiators).

Locks FSOT vs baseline discriminants for surveys that have not yet closed the
measurement. Anonymous: no personal names. Does not retune engine constants.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTESTED = ROOT / "data" / "contested_observables_closure.json"
PREREG_FREEZE = ROOT / "predictions" / "toe_prereg_freeze.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
OUT_JSON = ROOT / "predictions" / "contested_future_observation_ledger.json"
OUT_MD = ROOT / "predictions" / "reports" / "CONTESTED_FUTURE_OBSERVATION_LEDGER.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _worst_green(margin: dict, n: int = 8) -> list[dict]:
    rows = margin.get("all_domains") or []
    green = [r for r in rows if r.get("green_gate_pass")]
    green.sort(
        key=lambda r: -(
            r.get("official_pooled_median_error_pct")
            or r.get("pooled_median_error_pct")
            or 0.0
        )
    )
    out = []
    for r in green[:n]:
        out.append(
            {
                "domain": r.get("domain") or r.get("file"),
                "pooled_median_error_pct": r.get("official_pooled_median_error_pct")
                or r.get("pooled_median_error_pct"),
                "file": r.get("file"),
            }
        )
    return out


# Future surveys where FSOT and baseline models can diverge on published posteriors.
FUTURE_ROWS = [
    {
        "id": "FO-H0-ladder",
        "observable": "H0_local_vs_CMB",
        "fsot_lock": "bridge_scalar_70.75_between_67.4_and_73.04",
        "baseline_default": "separate_Planck_and_SH0ES_posteriors",
        "future_observation": "JWST/HST local ladder + CMB-S4 early-universe H0",
        "kill_if": "FSOT bridge not strictly between next local and CMB centrals",
        "related_pred": "PRED-H0-bridge",
        "status": "open_predata",
    },
    {
        "id": "FO-S8-lensing",
        "observable": "S8_effective",
        "fsot_lock": "0.805_between_Planck_and_DES",
        "baseline_default": "Planck_high_S8_vs_DES_low_S8_tension",
        "future_observation": "Euclid + LSST year-1 weak lensing S8",
        "kill_if": "FSOT S8 outside next Planck–DES-class band",
        "related_pred": "PRED-S8",
        "status": "open_predata",
    },
    {
        "id": "FO-wa-desi-euclid",
        "observable": "w_a_CPL",
        "fsot_lock": "wa_approx_-1.018",
        "baseline_default": "LCDM_wa_equals_0",
        "future_observation": "DESI DR2+/DR3 + Euclid BAO joint CPL (w0, wa)",
        "kill_if": "desi_3sigma_exclusion of frozen wa or sign flip vs lock",
        "related_pred": "PRED-wa",
        "status": "open_predata",
    },
    {
        "id": "FO-Neff-cmb",
        "observable": "N_eff",
        "fsot_lock": "3.046",
        "baseline_default": "SM_Neff_3.044_to_3.046",
        "future_observation": "Simons Observatory / CMB-S4 N_eff",
        "kill_if": "cmb_3sigma_exclusion of frozen N_eff",
        "related_pred": "PRED-Neffective",
        "status": "open_predata",
    },
    {
        "id": "FO-mH-pdg",
        "observable": "m_H",
        "fsot_lock": "125.25_GeV",
        "baseline_default": "SM_input_not_prediction",
        "future_observation": "next PDG Higgs mass combination",
        "kill_if": "pdg_update_outside_0_5pct of freeze",
        "related_pred": "PRED-mH",
        "status": "open_predata",
    },
    {
        "id": "FO-cusp-core",
        "observable": "dwarf_core_radius_rc",
        "fsot_lock": "0.6_kpc_Fornax_class",
        "baseline_default": "CDM_cusp_vs_cored_baryon_feedback_models",
        "future_observation": "dwarf spheroidal kinematic campaigns",
        "kill_if": "core radius outside 0.5% band of freeze when consensus forms",
        "related_pred": "PRED-cusp-core-rc",
        "status": "open_predata",
    },
    {
        "id": "FO-lithium-bbn",
        "observable": "lithium_underproduction_factor",
        "fsot_lock": "factor_approx_3",
        "baseline_default": "BBN_theory_vs_halo_star_gap",
        "future_observation": "metal-poor star Li + BBN nuclear rate updates",
        "kill_if": "gap factor outside 10% of frozen 3.0",
        "related_pred": "PRED-lithium-factor",
        "status": "open_predata",
    },
    {
        "id": "FO-frb-dm",
        "observable": "FRB_DM_excess_vs_IGM",
        "fsot_lock": "200_pc_cm3_excess_class",
        "baseline_default": "IGM_only_DM_models",
        "future_observation": "CHIME/FRB high-DM catalog refresh",
        "kill_if": "excess outside 0.5% of frozen central on panel refresh",
        "related_pred": "PRED-FRB-DM-excess",
        "status": "open_predata",
    },
    {
        "id": "FO-sigma8-central",
        "observable": "sigma_8",
        "fsot_lock": "0.8111",
        "baseline_default": "LCDM_sigma8_from_Planck_primary",
        "future_observation": "Euclid + LSST combined sigma8",
        "kill_if": "outside_0_5pct_of_frozen_central",
        "related_pred": "PRED-sigma8-central",
        "status": "open_predata",
    },
    {
        "id": "FO-omega-lambda",
        "observable": "Omega_Lambda",
        "fsot_lock": "0.6847",
        "baseline_default": "LCDM_OmegaL_fit_parameter",
        "future_observation": "combined BAO+CMB Omega_Lambda posterior",
        "kill_if": "outside_0_5pct_of_frozen_central",
        "related_pred": "PRED-Omega-Lambda",
        "status": "open_predata",
    },
]


def main() -> int:
    contested = _load(CONTESTED)
    freeze = _load(PREREG_FREEZE)
    margin = _load(MARGIN)
    panel = contested.get("panel_summary") or {}
    worst = _worst_green(margin)

    body = {
        "generated_at": _now(),
        "version": "1.0",
        "purpose": (
            "Future-observation differentiators for contested sectors. "
            "FSOT locks are pre-data; baseline defaults are current-model practice. "
            "No personal names. Pin D1D38A."
        ),
        "authority_pin_prefix": "D1D38A",
        "linked_freeze_id": freeze.get("freeze_id"),
        "linked_freeze_sha256": freeze.get("bundle_sha256"),
        "contested_panel": {
            "observable_count": panel.get("observable_count"),
            "fsot_pooled_median_error_pct": panel.get("pooled_median_error_pct"),
            "current_model_baseline_pct": panel.get("current_model_baseline_pct"),
            "verdict": contested.get("verdict"),
        },
        "future_observations": FUTURE_ROWS,
        "worst_green_empirical_watch": worst,
        "refresh_commands": [
            "python scripts/build_contested_observables_closure.py",
            "python scripts/build_contested_sector_watch.py",
            "python scripts/build_contested_future_observation_ledger.py",
            "python scripts/build_toe_gap_closure.py",
        ],
    }
    raw = json.dumps(body, sort_keys=True).encode()
    body["ledger_sha256"] = hashlib.sha256(raw).hexdigest()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(body, indent=2), encoding="utf-8")

    lines = [
        "# Contested Future-Observation Ledger",
        "",
        f"*Generated {_now()} · pin D1D38A · freeze `{body.get('linked_freeze_id')}`*",
        "",
        body["purpose"],
        "",
        "## Contested panel (current)",
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Observables | {panel.get('observable_count', '?')} |",
        f"| FSOT pooled median % | {panel.get('pooled_median_error_pct', '?')} |",
        f"| Typical baseline % | {panel.get('current_model_baseline_pct', 15)} |",
        f"| Verdict | {contested.get('verdict', '?')} |",
        "",
        "## Future differentiators (pre-data)",
        "",
        "| ID | Observable | FSOT lock | Baseline default | Future observation | Kill if |",
        "|----|------------|-----------|------------------|--------------------|---------|",
    ]
    for row in FUTURE_ROWS:
        lines.append(
            f"| {row['id']} | {row['observable']} | `{row['fsot_lock']}` | "
            f"{row['baseline_default']} | {row['future_observation']} | {row['kill_if']} |"
        )

    lines.extend(
        [
            "",
            "## Worst-green empirical watch (≤0.5% gate still holding)",
            "",
            "| Domain | Pooled median % |",
            "|--------|----------------:|",
        ]
    )
    for w in worst:
        lines.append(f"| {w['domain']} | {w['pooled_median_error_pct']} |")

    lines.extend(
        [
            "",
            f"Ledger SHA-256: `{body['ledger_sha256']}`",
            "",
            "Refresh: `python scripts/build_contested_future_observation_ledger.py`",
            "",
            "Related: `docs/PREDATA_RISK.md` · `predictions/toe_prereg_freeze.json` · "
            "`predictions/reports/CONTESTED_SECTOR_WATCH.md`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"  rows={len(FUTURE_ROWS)} ledger_sha={body['ledger_sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
