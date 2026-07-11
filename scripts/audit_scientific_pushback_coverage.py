#!/usr/bin/env python3
"""
Major scientific pushback audit — literature backing, contested sectors, σ coverage.

Surfaces avenues that could challenge FSOT at current precision:
  - Stumped/contested observables without benchmark representation
  - Scalar records missing literature uncertainty metadata
  - Domains failing hard or aspiration gates
  - Records where raw vs literature-aware effective error diverges
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
DEBT = ROOT / "data" / "extension_scalar_precision_debt.json"
STUMPED = ROOT / "data" / "stumped_observables_reference.json"
OUT = ROOT / "data" / "scientific_pushback_audit.json"

# Stumped reference property → benchmark property aliases / panel ids
STUMPED_PROPERTY_ALIASES: dict[str, set[str]] = {
    "brain_power": {"brain_power", "brain_power_w", "E_con", "e_con", "E_con_manifest"},
    "dark_energy_eos_evolution": {"dark_energy_eos_evolution", "w_a", "wa_evolution"},
    "hubble_constant": {"hubble_constant", "hubble_constant_km_s_mpc", "sector_h0_overlay"},
    "matter_clustering": {"matter_clustering", "sigma_8", "external_planck_sigma8"},
    "higgs_mass": {"higgs_mass", "higgs_mass_GeV"},
}

sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import analyze_benchmark, classify_record  # noqa: E402
from literature_uncertainty_lib import (  # noqa: E402
    is_contested_record,
    load_stumped_ids,
    resolve_reference_uncertainty_pct,
)
from scientific_measurement_lib import literature_aware_error_pct  # noqa: E402


def _yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _iter_scalar_records(doc: dict) -> list[dict]:
    recs = doc.get("material_records") or doc.get("records") or []
    return [r for r in recs if classify_record(r) == "scalar"]


def _scan_domain(name: str, path: Path) -> dict:
    if not path.exists():
        return {"domain": name, "missing_benchmark": True}
    doc = json.loads(path.read_text(encoding="utf-8"))
    margin = analyze_benchmark(doc, file_name=path.name)
    scalars = _iter_scalar_records(doc)

    missing_unc = 0
    missing_envelope = 0
    contested_untagged = 0
    raw_eff_divergence: list[dict] = []
    max_pushback: dict | None = None

    for r in scalars:
        prop = str(r.get("property") or "")
        if r.get("scientific_measurement") is None:
            missing_envelope += 1

        stumped = load_stumped_ids().get(prop)
        if stumped and not is_contested_record(r) and resolve_reference_uncertainty_pct(r) is None:
            missing_unc += 1
        elif stumped is None and resolve_reference_uncertainty_pct(r) is None and prop in load_stumped_ids():
            missing_unc += 1

        if prop in load_stumped_ids() and not is_contested_record(r):
            contested_untagged += 1

        comp = r.get("computed")
        meas = r.get("measured")
        if comp is None or meas is None:
            continue
        try:
            raw = float(r.get("error_pct") or 0)
            aware = literature_aware_error_pct(float(comp), float(meas), r)
            eff = float(aware.get("effective_error_pct") or raw)
        except (TypeError, ValueError):
            continue

        if abs(eff - raw) > 0.5 and max(raw, eff) > 0.5:
            raw_eff_divergence.append(
                {
                    "property": prop,
                    "name": r.get("name"),
                    "raw_pct": raw,
                    "effective_pct": eff,
                    "comparison_kind": aware.get("comparison_kind"),
                }
            )

        push = eff if not is_contested_record(r) else 0.0
        if max_pushback is None or push > float(max_pushback.get("effective_pct") or 0):
            max_pushback = {
                "property": prop,
                "name": r.get("name"),
                "raw_pct": raw,
                "effective_pct": eff,
                "contested": is_contested_record(r),
            }

    return {
        "domain": name,
        "scalar_count": len(scalars),
        "missing_scientific_measurement": missing_envelope,
        "stumped_missing_uncertainty": missing_unc,
        "stumped_untagged_contested": contested_untagged,
        "max_scalar_error_pct": margin.get("max_scalar_error_pct"),
        "max_effective_scalar_error_pct": margin.get("max_effective_scalar_error_pct"),
        "pooled_median_error_pct": margin.get("official_pooled_median_error_pct"),
        "green_gate_pass": margin.get("green_gate_pass"),
        "raw_eff_divergence_count": len(raw_eff_divergence),
        "top_raw_eff_divergence": sorted(raw_eff_divergence, key=lambda x: -x["effective_pct"])[:3],
        "max_pushback_scalar": max_pushback,
    }


def _collect_benchmark_properties() -> set[str]:
    spec = _yaml(MANIFEST)
    props: set[str] = set()
    for _name, cfg in (spec.get("extension_domains") or {}).items():
        rel = cfg.get("benchmark_data")
        if not rel:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for r in doc.get("material_records") or doc.get("records") or []:
            p = str(r.get("property") or "")
            if p:
                props.add(p)
            sid = str(r.get("id") or r.get("name") or "")
            if sid:
                props.add(sid)
        for r in doc.get("open_predictions") or []:
            sid = str(r.get("id") or r.get("name") or "")
            if sid:
                props.add(sid)
    return props


def _property_covered(prop: str, covered: set[str]) -> bool:
    if prop in covered:
        return True
    for alias in STUMPED_PROPERTY_ALIASES.get(prop, {prop}):
        if alias in covered:
            return True
    return False


def _stumped_coverage(covered_props: set[str]) -> list[dict]:
    stumped_doc = json.loads(STUMPED.read_text(encoding="utf-8")) if STUMPED.exists() else {}
    out: list[dict] = []
    for obs in stumped_doc.get("observables") or []:
        prop = str(obs.get("property") or "")
        out.append(
            {
                "id": obs.get("id"),
                "property": prop,
                "status": obs.get("status"),
                "reference": obs.get("reference"),
                "measured": obs.get("measured"),
                "in_extension_benchmarks": _property_covered(prop, covered_props),
                "pushback_risk": obs.get("status"),
            }
        )
    return out


def build() -> dict:
    spec = _yaml(MANIFEST)
    domain_rows: list[dict] = []
    for name, cfg in (spec.get("extension_domains") or {}).items():
        rel = cfg.get("benchmark_data")
        if not rel:
            continue
        domain_rows.append(_scan_domain(name, ROOT / rel))

    debt = json.loads(DEBT.read_text(encoding="utf-8")) if DEBT.exists() else {}
    aspiration_debt = debt.get("aspiration_debt") or []

    failing_green = [r for r in domain_rows if r.get("green_gate_pass") is False]
    missing_unc_domains = sorted(
        [r for r in domain_rows if (r.get("stumped_missing_uncertainty") or 0) > 0],
        key=lambda x: -(x.get("stumped_missing_uncertainty") or 0),
    )
    high_pushback = sorted(
        [
            r
            for r in domain_rows
            if (r.get("max_effective_scalar_error_pct") or 0) > 0.5
            and not (r.get("max_pushback_scalar") or {}).get("contested")
        ],
        key=lambda x: -(x.get("max_effective_scalar_error_pct") or 0),
    )[:20]
    raw_eff_domains = sorted(
        [r for r in domain_rows if (r.get("raw_eff_divergence_count") or 0) > 0],
        key=lambda x: -(x.get("raw_eff_divergence_count") or 0),
    )[:25]

    covered_props = _collect_benchmark_properties()
    stumped = _stumped_coverage(covered_props)
    stumped_gaps = [
        s
        for s in stumped
        if not s.get("in_extension_benchmarks")
        and s.get("status") != "unconfirmed_prediction"
    ]
    prereg_tracked = [s for s in stumped if s.get("status") == "unconfirmed_prediction"]

    pushback_avenues: list[dict] = []
    for s in stumped:
        if s.get("status") in {
            "hubble_tension_cmb",
            "hubble_tension_local",
            "dark_energy_open",
            "s8_tension",
            "cmb_open",
            "bbn_open",
            "hierarchy_problem",
            "cusp_core_problem",
            "consciousness_open",
            "unconfirmed_prediction",
        }:
            pushback_avenues.append(
                {
                    "avenue": s.get("id"),
                    "status": s.get("status"),
                    "reference": s.get("reference"),
                    "benchmark_coverage": s.get("in_extension_benchmarks"),
                    "severity": "high" if not s.get("in_extension_benchmarks") else "monitored",
                    "mitigation": (
                        "contested_observable eval_kind + literature_uncertainty_anchors"
                        if s.get("in_extension_benchmarks")
                        else "add benchmark panel row with σ metadata"
                    ),
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "summary": {
            "extension_domain_count": len(domain_rows),
            "green_gate_pass_count": sum(1 for r in domain_rows if r.get("green_gate_pass")),
            "green_gate_fail_count": len(failing_green),
            "aspiration_scalar_debt_count": debt.get("aspiration_debt_count", len(aspiration_debt)),
            "stumped_observable_count": len(stumped),
            "stumped_without_benchmark_row": len(stumped_gaps),
            "preregistered_predictions_tracked": len(prereg_tracked),
            "domains_missing_uncertainty_metadata": len(missing_unc_domains),
            "domains_raw_eff_divergence": sum(1 for r in domain_rows if (r.get("raw_eff_divergence_count") or 0) > 0),
        },
        "aspiration_debt": aspiration_debt,
        "pushback_avenues": pushback_avenues,
        "stumped_observables": stumped,
        "stumped_gaps": stumped_gaps,
        "preregistered_predictions": prereg_tracked,
        "high_pushback_domains": high_pushback,
        "missing_uncertainty_domains": missing_unc_domains[:25],
        "raw_eff_divergence_domains": [
            {
                "domain": r.get("domain"),
                "count": r.get("raw_eff_divergence_count"),
                "top": (r.get("top_raw_eff_divergence") or [None])[0],
                "green_gate_pass": r.get("green_gate_pass"),
            }
            for r in raw_eff_domains
        ],
        "failing_green_gate_domains": failing_green[:25],
        "remediation_priority": [
            "Propagate literature_uncertainty_anchors to stumped-property rows via enrich_benchmark_scientific_metadata.py",
            "Tag H0 / dark-sector rows with contested_observable where literature spans >5%",
            "Use sigma_distance rows for DESI w0 (not raw relative %)",
            "Close stumped_gaps: benchmark panel for observables not yet in extension domains",
            "Re-run verification_depth_audit after each remediation batch",
        ],
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    s = doc["summary"]
    print("=== Scientific pushback audit ===")
    print(f"  domains: {s['extension_domain_count']} green={s['green_gate_pass_count']} fail={s['green_gate_fail_count']}")
    print(f"  aspiration_debt: {s['aspiration_scalar_debt_count']}")
    print(f"  stumped_observables: {s['stumped_observable_count']} gaps={s['stumped_without_benchmark_row']}")
    print(f"  pushback_avenues: {len(doc['pushback_avenues'])}")
    print(f"  wrote: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())