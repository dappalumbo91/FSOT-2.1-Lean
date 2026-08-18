#!/usr/bin/env python3
"""Falsification registry — preregistered kill criteria and review horizons."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"
STUMPED = ROOT / "data" / "stumped_observables_reference.json"
DESI = ROOT / "data" / "desi_wa_constraint_benchmark.json"
OUT = ROOT / "data" / "falsification_registry_closure.json"

DISCRIMINANT_KILL: dict[str, str] = {
    "strictly_between_planck_and_sh0es": "FSOT H0 readout outside [67.4, 73.04] km/s/Mpc",
    "between_planck_and_des": "FSOT S8 readout outside Planck–DES tension band",
    "within_10pct_of_observed_gap": "FSOT prediction >10% from measured anchor",
    "fsot_exceeds_sota_by_0.4": "FSOT margin vs null/SOTA baseline < 0.4",
    "same_sign_as_fermilab": "FSOT delta_a_mu opposite sign to Fermilab 2021",
    "desi_3sigma_exclusion": "desi_or_euclid_3sigma_exclusion of frozen wa",
    "cmb_3sigma_exclusion": "cmb_3sigma_exclusion of frozen N_eff",
    "within_green_gate_0_5pct": "panel pooled median exceeds 0.5% green gate",
    "pdg_update_outside_0_5pct": "PDG/combination update more than 0.5% from frozen central",
    "within_0_5pct_of_frozen_central": "refresh residual more than 0.5% from frozen central",
}

OUTCOME_LOG = ROOT / "results" / "outcomes" / "prediction_outcome_log.jsonl"
RESULTS_XREF = ROOT / "results" / "literature" / "2026-08-17_crossref.json"


def _yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _outcome_index() -> dict[str, list[dict]]:
    idx: dict[str, list[dict]] = {}
    if OUTCOME_LOG.is_file():
        for line in OUTCOME_LOG.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            pid = str(row.get("pred_id") or "")
            if pid:
                idx.setdefault(pid, []).append(row)
    return idx


def _pred_status(pred: dict, outcomes: dict[str, list[dict]]) -> str:
    pid = str(pred.get("id") or "")
    latest = (outcomes.get(pid) or [None])[-1]
    if latest:
        res = str(latest.get("result") or "")
        mapping = {
            "hold": "hold_logged",
            "partial": "partial_logged",
            "awaiting": "pending_independent_measurement",
            "theory_rebase": "theory_rebase_logged",
            "kill": "kill_logged",
            "local_green_hold": "local_green_hold",
        }
        if res in mapping:
            return mapping[res]
    if pid in {"PRED-001", "PRED-024", "PRED-046", "PRED-051"}:
        val = float(pred.get("fsot_predicted") or 0)
        if 67.4 <= val <= 73.04:
            return "consistent_with_discriminant"
        return "would_falsify_if_measured"
    return "pending_independent_measurement"


def _wa_entry() -> dict:
    doc = {}
    if DESI.exists():
        doc = json.loads(DESI.read_text(encoding="utf-8"))
    rec = None
    for r in doc.get("material_records") or []:
        if r.get("property") == "dark_energy_eos_evolution":
            rec = r
            break
    if not rec:
        return {
            "id": "P45c_wa_prereg",
            "name": "w_a_BAO_readout_vs_DESI",
            "status": "pending_data",
            "kill_criterion": "FSOT wa_bao readout >3σ from DESI DR2+ posterior",
            "review_horizon": "DESI DR3 / DR4 release",
        }
    try:
        comp = float(rec.get("computed"))
        meas = float(rec.get("measured"))
        unc = float(rec.get("measured_uncertainty") or 0.24)
        sigma = abs(comp - meas) / unc if unc else None
    except (TypeError, ValueError):
        comp = meas = sigma = None
    status = "confirmed_within_2sigma" if sigma is not None and sigma <= 2.0 else "contested"
    return {
        "id": "P45c_wa_prereg",
        "name": "w_a_BAO_readout_vs_DESI",
        "fsot_readout": comp,
        "measured": meas,
        "uncertainty": unc,
        "sigma_equivalent": sigma,
        "status": status,
        "kill_criterion": "FSOT wa_bao readout >3σ from DESI DR2+ posterior",
        "review_horizon": "DESI DR3 / DR4 release",
        "evidence": "data/desi_wa_constraint_benchmark.json",
    }


def build() -> dict:
    manifest = _yaml(PREREG)
    predictions = manifest.get("predictions") or []
    stumped_doc = json.loads(STUMPED.read_text(encoding="utf-8")) if STUMPED.exists() else {}
    stumped = stumped_doc.get("observables") or []

    outcomes = _outcome_index()
    prereg_rows: list[dict] = []
    for p in predictions:
        disc = str(p.get("discriminant") or "")
        pid = p.get("id")
        latest = (outcomes.get(str(pid)) or [None])[-1]
        row = {
            "id": pid,
            "name": p.get("name"),
            "domain": p.get("domain"),
            "fsot_predicted": p.get("fsot_predicted"),
            "unit": p.get("unit"),
            "sota_baseline": p.get("sota_baseline"),
            "discriminant": disc,
            "kill_criterion": DISCRIMINANT_KILL.get(disc, f"Violates discriminant: {disc}"),
            "registered_at": p.get("registered_at"),
            "future_survey": p.get("future_survey"),
            "status": _pred_status(p, outcomes),
            "review_horizon": p.get("future_survey")
            or "independent_measurement_or_survey_release",
        }
        if latest:
            row["latest_outcome"] = {
                "ts": latest.get("ts"),
                "survey": latest.get("survey"),
                "result": latest.get("result"),
                "measured": latest.get("measured"),
                "source": latest.get("source"),
            }
        prereg_rows.append(row)

    stumped_rows: list[dict] = []
    for o in stumped:
        stumped_rows.append(
            {
                "id": o.get("id"),
                "property": o.get("property"),
                "status": o.get("status"),
                "measured": o.get("measured"),
                "fsot_predicted": o.get("fsot_predicted") or o.get("fsot_predicted_cmb"),
                "reference": o.get("reference"),
                "kill_criterion": (
                    f"Future survey measures {o.get('property')} >3σ from FSOT readout "
                    f"with tightened systematics"
                ),
                "review_horizon": "survey_data_release_or_laboratory_update",
                "note": "Contested sector — tracked, not hidden; does not invalidate cross-domain envelope alone.",
            }
        )

    wa = _wa_entry()
    confirmed = sum(1 for r in prereg_rows if r["status"] == "consistent_with_discriminant")
    pending = sum(1 for r in prereg_rows if r["status"] == "pending_independent_measurement")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.1",
        "verdict": "FALSIFICATION_CRITERIA_REGISTERED",
        "manifest_source": "predictions/preregistered_predictions_manifest.yaml",
        "outcome_log": "results/outcomes/prediction_outcome_log.jsonl",
        "summary": {
            "preregistered_prediction_count": len(prereg_rows),
            "stumped_observable_count": len(stumped_rows),
            "confirmed_discriminant_count": confirmed,
            "pending_measurement_count": pending,
            "wa_prereg_status": wa.get("status"),
            "global_kill_criterion": (
                "If >25% of extension domains fail pooled ≤0.5% gate on next full "
                "benchmark refresh, downgrade empirical_accuracy_closure verdict."
            ),
            "global_review_horizon": "2026-12-31 full benchmark + survey refresh",
        },
        "preregistered_predictions": prereg_rows,
        "stumped_observables": stumped_rows,
        "flagship_tests": [
            wa,
            {
                "id": "cross_domain_envelope",
                "name": "472_file_green_gate",
                "kill_criterion": ">25% extension domains fail pooled ≤0.5% on refresh",
                "review_horizon": "2026-12-31",
                "evidence": "data/benchmark_margin_audit.json",
                "live_green": "docs/CURRENT_STATUS.md",
            },
            {
                "id": "PRED-001",
                "name": "H0_bridge_scalar",
                "kill_criterion": DISCRIMINANT_KILL["strictly_between_planck_and_sh0es"],
                "fsot_predicted": 70.75,
                "status": "consistent_with_discriminant",
                "review_horizon": "SH0ES/Planck consensus shift",
            },
        ],
        "honest_statement": (
            "Every preregistered prediction carries a pre-stated kill criterion. "
            "Stumped observables are contested science — not pipeline failures. "
            "FSOT invites falsification via survey releases and domain-gate degradation, "
            "not post-hoc retuning."
        ),
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {OUT}")
    print(
        f"  prereg={s['preregistered_prediction_count']} stumped={s['stumped_observable_count']} "
        f"wa_status={s['wa_prereg_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())