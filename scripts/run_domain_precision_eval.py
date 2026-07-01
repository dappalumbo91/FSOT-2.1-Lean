#!/usr/bin/env python3
"""Tier 10: per-record numeric precision across all 35 NeuroLab domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_YAML = ROOT / "data" / "fsot_35_domain_registry.yaml"
LAB_REGISTRY = ROOT / "data" / "lab_registry.json"
OUTPUT = ROOT / "data" / "domain_precision_report.json"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_precision_labs import LAB_EXTRACTORS, merge_lab_summaries  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402


HUGE_GAP_PCT = 25.0
SIGN_MISMATCH_NOTE = (
    "NeuroLab authority scalar sign disagrees with Lean rollup domain; "
    "likely observed=false/CHAOS params — weather sim uses observed=true D_eff=15."
)


def _precision_status(
    median: float | None,
    record_count: int,
    sign_mismatch: bool,
    huge_gap: bool,
) -> str:
    if sign_mismatch:
        return "sign_mismatch"
    if record_count == 0:
        return "no_numeric_records"
    if huge_gap:
        return "huge_gap"
    if median is None:
        return "structural_only"
    if median <= 2.0:
        return "target_band"
    if median <= 5.0:
        return "tolerable_band"
    return "unacceptable"


def evaluate() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
    precision_cfg = spec.get("precision_verification") or {}
    huge_gap_pct = float(precision_cfg.get("huge_gap_pct", HUGE_GAP_PCT))

    registry = json.loads(LAB_REGISTRY.read_text(encoding="utf-8")) if LAB_REGISTRY.exists() else {}
    mod, authority_path = load_fsot_compute()
    empirical_sources = spec.get("empirical_sources", {})
    lean_overrides = spec.get("lean_overrides", {})

    domains_out = []
    for name in sorted(mod.DOMAINS.keys()):
        cfg = mod.DOMAINS[name]
        S = float(mod.domain_scalar(name))
        neurolab_sign = "negative" if S < -1e-12 else ("positive" if S > 1e-12 else "zero")
        lean_domain = lean_overrides.get(name) or empirical_sources.get(name, {}).get("lean_domain")

        lab_summaries = []
        lab_breakdown = []
        src_cfg = empirical_sources.get(name, {})
        smiles_lean = lean_domain
        if lab_key_hint := src_cfg.get("smiles_lean_fallback"):
            smiles_lean = src_cfg.get("smiles_lean_fallback") or lean_domain
        for lab_key in (src_cfg.get("labs") or []):
            extractor = LAB_EXTRACTORS.get(lab_key)
            if extractor is None:
                continue
            summary = extractor(
                registry,
                smiles_lean if lab_key == "smiles_lab" else None,
            )
            lab_breakdown.append(
                {
                    "lab": lab_key,
                    "record_count": summary["record_count"],
                    "median_error_pct": summary["median_error_pct"],
                    "p90_error_pct": summary["p90_error_pct"],
                    "max_error_pct": summary["max_error_pct"],
                    "within_2pct": summary["within_2pct"],
                    "within_5pct": summary["within_5pct"],
                }
            )
            lab_summaries.append(summary)

        merged = merge_lab_summaries(lab_summaries)
        median = merged["median_error_pct"]
        huge_gap = median is not None and median > huge_gap_pct

        lean_sign_positive = None
        if lean_domain:
            sys.path.insert(0, str(ROOT / "scripts"))
            from domain_scalar_oracle import DOMAINS as LEAN_DOMAINS, raw_S  # noqa: E402

            if lean_domain in LEAN_DOMAINS:
                lean_raw = raw_S(LEAN_DOMAINS[lean_domain])
                lean_sign_positive = lean_raw > 0

        sign_mismatch = (
            lean_sign_positive is not None
            and ((neurolab_sign == "negative" and lean_sign_positive)
                 or (neurolab_sign == "positive" and not lean_sign_positive))
        )

        # Property grain from SMILES sections when present
        properties: dict[str, list[float]] = {}
        for s in lab_summaries:
            for rec in s.get("records") or []:
                prop = rec.get("property") or "unknown"
                err = rec.get("error_pct")
                if err is not None:
                    properties.setdefault(str(prop), []).append(float(err))
        property_stats = [
            {
                "property": k,
                "records": len(v),
                "median_error_pct": sorted(v)[len(v) // 2],
            }
            for k, v in sorted(properties.items())
        ]

        status = _precision_status(median, merged["record_count"], sign_mismatch, huge_gap)

        domains_out.append(
            {
                "neurolab_domain": name,
                "lean_domain": lean_domain,
                "domain_scalar_S": S,
                "neurolab_scalar_sign": neurolab_sign,
                "lean_sign_positive": lean_sign_positive,
                "sign_mismatch": sign_mismatch,
                "record_count": merged["record_count"],
                "median_error_pct": median,
                "p90_error_pct": merged["p90_error_pct"],
                "max_error_pct": merged["max_error_pct"],
                "within_2pct": merged["within_2pct"],
                "within_5pct": merged["within_5pct"],
                "precision_status": status,
                "huge_gap": huge_gap,
                "labs": lab_breakdown,
                "top_properties": property_stats[:8],
                "diagnostic": SIGN_MISMATCH_NOTE if sign_mismatch else None,
            }
        )

    target_band = [d for d in domains_out if d["precision_status"] == "target_band"]
    tolerable = [d for d in domains_out if d["precision_status"] == "tolerable_band"]
    huge = [d for d in domains_out if d["precision_status"] == "huge_gap"]
    mismatch = [d for d in domains_out if d["precision_status"] == "sign_mismatch"]
    unacceptable = [d for d in domains_out if d["precision_status"] == "unacceptable"]

    return {
        "authority_path": str(authority_path),
        "domain_count": len(domains_out),
        "domains_with_numeric_precision": sum(
            1 for d in domains_out if d["median_error_pct"] is not None
        ),
        "domains_target_band_2pct": len(target_band),
        "domains_tolerable_band_5pct": len(tolerable),
        "domains_unacceptable": len(unacceptable),
        "domains_huge_gap": len(huge),
        "domains_sign_mismatch": len(mismatch),
        "huge_gap_domains": [d["neurolab_domain"] for d in huge],
        "sign_mismatch_domains": [d["neurolab_domain"] for d in mismatch],
        "domains": domains_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Tier-10 domain precision evaluation")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    report = evaluate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  numeric precision: {report['domains_with_numeric_precision']}/{report['domain_count']}")
    print(f"  target ≤2%: {report['domains_target_band_2pct']}")
    print(f"  tolerable ≤5%: {report['domains_tolerable_band_5pct']}")
    print(f"  huge gap: {report['domains_huge_gap']} {report.get('huge_gap_domains')}")
    print(f"  sign mismatch: {report['domains_sign_mismatch']} {report.get('sign_mismatch_domains')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())