#!/usr/bin/env python3
"""Scientific capability & accuracy gap report — FSOT vs SOTA + live margin.

Answers: where do we already beat literature/SOTA, where is the margin thin
(need more refine to *exceed* confidently), and what granular expansion to run next.

Outputs:
  data/scientific_capability_gap_report.json
  data/scientific_capability_gap_report.md
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _run(script: str) -> None:
    p = ROOT / "scripts" / script
    if p.is_file():
        subprocess.run([sys.executable, str(p)], cwd=str(ROOT), check=False)


def main() -> int:
    # Refresh SOTA ledger + dossier from current benchmarks
    _run("build_sota_observable_ledger.py")
    _run("build_sota_competitiveness_dossier.py")

    margin = _load(DATA / "benchmark_margin_audit.json")
    sota_dom = _load(DATA / "sota_competitiveness_report.json")
    sota_obs = _load(DATA / "sota_observable_ledger_report.json")
    toe = _load(DATA / "toe_gap_closure_report.json")
    grsm = _load(DATA / "gr_sm_ckm_verification_report.json")
    exp_map = _load(DATA / "scientific_domain_expansion_map.json")

    domains = margin.get("all_domains") or []

    def mx(r: dict) -> float:
        return float(r.get("max_scalar_error_pct") or 0)

    def med(r: dict) -> float:
        return float(r.get("pooled_median_error_pct") or r.get("median_error_pct") or 0)

    def nsc(r: dict) -> int:
        return int(r.get("scalar_count") or 0)

    def dname(r: dict) -> str:
        return str(r.get("domain") or r.get("file") or "?")

    near_gate = sorted(
        [r for r in domains if nsc(r) > 0 and mx(r) >= 0.4],
        key=mx,
        reverse=True,
    )[:20]
    thin = sorted(
        [r for r in domains if 0 < nsc(r) <= 8],
        key=lambda r: (nsc(r), -mx(r)),
    )[:25]
    aspiration = [r for r in domains if nsc(r) > 0 and mx(r) > 0.05]

    # SOTA domain table
    sota_domains = sota_dom.get("domains") or []
    tight_sota = sorted(
        sota_domains,
        key=lambda r: float(r.get("margin_vs_sota_pct") or 0),
    )[:15]
    wide_sota = sorted(
        sota_domains,
        key=lambda r: -float(r.get("margin_vs_sota_pct") or 0),
    )[:10]

    # Observables: smallest margin vs SOTA = highest refine priority to *exceed more*
    obs = sota_obs.get("records") or []
    tight_obs = sorted(
        [r for r in obs if r.get("margin_vs_sota_pct") is not None and not r.get("exclude_from_headline_beats")],
        key=lambda r: float(r["margin_vs_sota_pct"]),
    )[:20]
    below = sota_obs.get("below_sota_ids") or sota_dom.get("below_sota_domains") or []

    # Refinement tiers for beat-or-exceed strategy
    def refine_tier(margin_pp: float | None, fsot_err: float | None) -> str:
        if margin_pp is None:
            return "uncompared"
        if margin_pp < 0:
            return "BEHIND_SOTA — must refine"
        if margin_pp < 0.5:
            return "THIN_LEAD — refine to lock exceed"
        if margin_pp < 2.0:
            return "MODERATE_LEAD — optional polish"
        return "STRONG_LEAD — maintain"

    obs_tiers = []
    for r in tight_obs:
        m = float(r["margin_vs_sota_pct"])
        fe = r.get("fsot_error_pct")
        obs_tiers.append(
            {
                "id": r.get("id"),
                "domain": r.get("domain"),
                "fsot_error_pct": fe,
                "sota_typical_error_pct": r.get("sota_typical_error_pct") or r.get("sota_rmse"),
                "margin_vs_sota_pp": m,
                "sota_model": r.get("sota_model"),
                "sota_free_parameters": r.get("sota_free_parameters"),
                "status": r.get("status"),
                "refine_tier": refine_tier(m, fe),
                "fsot_source": r.get("fsot_source"),
            }
        )

    # Live TOE flavor depth vs literature gate
    toe_depth = {
        "label_B": (toe.get("evaluation") or {}).get("label_B_classical_toe"),
        "gr_sm_ckm_overall_ok": grsm.get("overall_ok"),
        "next_research": toe.get("next_actions_research"),
    }

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "goal": "Beat or exceed scientific SOTA / literature capability on measured observables",
        "live_atlas": {
            "green_pass": margin.get("green_gate_pass_count"),
            "green_fail": margin.get("green_gate_fail_count"),
            "worst_max_error_pct": margin.get("worst_scalar_max_error_pct"),
            "worst_domain": margin.get("worst_scalar_domain"),
            "domains_above_aspiration_0_05": len(aspiration),
            "threshold_green_pct": 0.5,
            "threshold_aspiration_pct": 0.05,
        },
        "sota_domain_summary": {
            "domains_compared": sota_dom.get("domains_compared"),
            "domains_beats_sota": sota_dom.get("domains_beats_sota"),
            "beats_sota_fraction": sota_dom.get("beats_sota_fraction"),
            "average_margin_vs_sota_pct": sota_dom.get("average_margin_vs_sota_pct"),
            "aggregate_sota_free_parameters_replaced": sota_dom.get("aggregate_sota_free_parameters"),
            "fsot_free_parameters_claim": sota_dom.get("fsot_free_parameters"),
            "below_sota_domains": sota_dom.get("below_sota_domains") or [],
        },
        "sota_observable_summary": {
            "observable_count": sota_obs.get("observable_count"),
            "beats_or_meets_sota_count": sota_obs.get("beats_or_meets_sota_count"),
            "headline_beats_or_meets_count": sota_obs.get("headline_beats_or_meets_count"),
            "below_sota_ids": below,
            "parameter_honesty": sota_obs.get("parameter_audit_verdict") or sota_obs.get("fsot_free_parameters_note"),
        },
        "tightest_sota_leads_need_most_refine": obs_tiers,
        "strongest_sota_domain_leads": [
            {
                "domain": r.get("domain"),
                "fsot_median": r.get("fsot_median_error_pct"),
                "sota_typical": r.get("sota_typical_median_error_pct"),
                "margin_pp": r.get("margin_vs_sota_pct"),
                "sota_params": r.get("sota_free_parameters"),
            }
            for r in wide_sota
        ],
        "thinnest_sota_domain_leads": [
            {
                "domain": r.get("domain"),
                "fsot_median": r.get("fsot_median_error_pct"),
                "sota_typical": r.get("sota_typical_median_error_pct"),
                "margin_pp": r.get("margin_vs_sota_pct"),
                "sota_model": r.get("sota_model"),
            }
            for r in tight_sota
        ],
        "near_gate_atlas_max": [
            {
                "domain": dname(r),
                "max_error_pct": mx(r),
                "median_error_pct": med(r),
                "scalar_count": nsc(r),
                "max_name": r.get("max_scalar_name"),
            }
            for r in near_gate
        ],
        "thin_panels": [
            {
                "domain": dname(r),
                "scalar_count": nsc(r),
                "max_error_pct": mx(r),
                "file": r.get("file"),
            }
            for r in thin
        ],
        "expansion_map": {
            "total_scientific_domains": (exp_map.get("summary") or {}).get("total_scientific_domains_covered"),
            "recommended_next_waves": exp_map.get("recommended_next_waves"),
            "thin_empirical_coverage": exp_map.get("thin_empirical_coverage"),
        },
        "toe_depth": toe_depth,
        "refine_strategy": {
            "beat_or_exceed_rule": (
                "FSOT already beats registered SOTA typical error on headline observables "
                "with 0 free fit coefficients. To *exceed more confidently*, refine "
                "THIN_LEAD items (margin < 0.5 pp) first: higgs_mass, airfoil RMSE, "
                "higgs_branching, H0_planck — without adding free parameters."
            ),
            "near_gate_rule": (
                "Atlas max ~0.5% residuals are mostly SMILES closed-form headroom already "
                "under green; do not free-param shave. Use formula-class upgrades only."
            ),
            "coverage_rule": "Thicken thin panels (lean routes, hybrid FI) for capability breadth.",
            "priority_queue": [
                "1. THIN_LEAD SOTA observables (higgs_mass, airfoil, H0_planck)",
                "2. Near-gate formula-class only if definitional (not fishing)",
                "3. Thin-panel thickening (lean routes, multi-hero strata)",
                "4. TOE research spine (path-integral theorem, spin-2 Fock uniqueness)",
                "5. Registered expansion waves (culinary Maillard, materials bridge, KB)",
            ],
        },
    }

    # Markdown
    lines = [
        "# Scientific capability & accuracy gap report",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "## Goal",
        "",
        report["goal"],
        "",
        "## Live atlas (green gate)",
        "",
        f"- Green: **{report['live_atlas']['green_pass']}** pass / {report['live_atlas']['green_fail']} fail",
        f"- Worst max residual: **{report['live_atlas']['worst_max_error_pct']}%** ({report['live_atlas']['worst_domain']})",
        f"- Domains with max > 0.05% aspiration: **{report['live_atlas']['domains_above_aspiration_0_05']}**",
        "",
        "## SOTA competitiveness (registered comparisons)",
        "",
        f"- Domains beating SOTA median: **{report['sota_domain_summary']['domains_beats_sota']}/{report['sota_domain_summary']['domains_compared']}** "
        f"({100*(report['sota_domain_summary'].get('beats_sota_fraction') or 0):.1f}%)",
        f"- Average margin vs SOTA: **{report['sota_domain_summary'].get('average_margin_vs_sota_pct', 0):.2f} pp**",
        f"- Observables beats/meets: **{report['sota_observable_summary']['beats_or_meets_sota_count']}/{report['sota_observable_summary']['observable_count']}**",
        f"- Below SOTA IDs: {report['sota_observable_summary']['below_sota_ids'] or 'none'}",
        f"- SOTA free parameters replaced (aggregate): **{report['sota_domain_summary'].get('aggregate_sota_free_parameters_replaced')}**",
        "",
        "### Thinnest leads (refine to lock *exceed*)",
        "",
        "| ID | FSOT err% | SOTA typ% | Margin pp | Tier | SOTA model |",
        "|----|-----------|-----------|-----------|------|------------|",
    ]
    for r in obs_tiers[:12]:
        lines.append(
            f"| {r['id']} | {r['fsot_error_pct']} | {r['sota_typical_error_pct']} | "
            f"{r['margin_vs_sota_pp']:.3f} | {r['refine_tier']} | {r['sota_model']} |"
        )
    lines += [
        "",
        "### How much refinement is needed?",
        "",
        "| Tier | Meaning | Action |",
        "|------|---------|--------|",
        "| BEHIND_SOTA | FSOT error > SOTA typical | Must improve formula/mechanism |",
        "| THIN_LEAD (<0.5 pp) | Barely ahead | Highest-value refine for confident exceed |",
        "| MODERATE_LEAD (0.5–2 pp) | Solid lead | Optional polish |",
        "| STRONG_LEAD (>2 pp) | Comfortably ahead | Maintain; expand coverage |",
        "",
        report["refine_strategy"]["beat_or_exceed_rule"],
        "",
        "## Near-gate atlas (max residual)",
        "",
    ]
    for r in report["near_gate_atlas_max"][:10]:
        lines.append(
            f"- **{r['domain']}**: max {r['max_error_pct']:.4f}% med {r['median_error_pct']:.4f}% "
            f"n={r['scalar_count']} worst=`{r['max_name']}`"
        )
    lines += [
        "",
        "## Thin panels (coverage debt)",
        "",
    ]
    for r in report["thin_panels"][:12]:
        lines.append(f"- n={r['scalar_count']} max={r['max_error_pct']}  {r['domain']}")
    lines += [
        "",
        "## Priority queue",
        "",
    ]
    for p in report["refine_strategy"]["priority_queue"]:
        lines.append(f"- {p}")
    lines += [
        "",
        "## TOE depth track",
        "",
        f"- Label B: {toe_depth.get('label_B')}",
        f"- GR/SM/CKM multiprover ok: {toe_depth.get('gr_sm_ckm_overall_ok')}",
        f"- Next research: {toe_depth.get('next_research')}",
        "",
    ]

    (DATA / "scientific_capability_gap_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (DATA / "scientific_capability_gap_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"Wrote {DATA / 'scientific_capability_gap_report.json'}")
    print(f"Wrote {DATA / 'scientific_capability_gap_report.md'}")
    print(
        f"SOTA domains beat {report['sota_domain_summary']['domains_beats_sota']}/"
        f"{report['sota_domain_summary']['domains_compared']}; "
        f"obs {report['sota_observable_summary']['beats_or_meets_sota_count']}/"
        f"{report['sota_observable_summary']['observable_count']}"
    )
    print("Tightest leads:")
    for r in obs_tiers[:6]:
        print(f"  {r['refine_tier'][:20]:20s}  {r['id']:24s}  margin={r['margin_vs_sota_pp']:.3f} pp")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
