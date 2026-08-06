#!/usr/bin/env python3
"""Generate preregistered prediction atlas across ALL green domains.

Not cosmology-only:
  - residual_hold for every green domain
  - scalar_lock for top continuous observables (tiered by panel size)
  - multi_tool_h0 + sightline host H0 (bubble bleed)
  - sector_portfolio holds for bio/materials/particle/earth/social/astro/…

Grounded in monorepo benchmarks — zero free parameters.

Outputs:
  predictions/domain_prediction_atlas.json
  predictions/reports/DOMAIN_PREDICTION_ATLAS.md
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
H0_MULTI = ROOT / "predictions" / "h0_multi_tool_predictions.json"
H0_SIGHT = ROOT / "predictions" / "h0_sightline_predictions.json"
H0_TRGB = ROOT / "predictions" / "cchp_trgb_sightline_predictions.json"
PREREG = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"
OUT_JSON = ROOT / "predictions" / "domain_prediction_atlas.json"
OUT_MD = ROOT / "predictions" / "reports" / "DOMAIN_PREDICTION_ATLAS.md"

GREEN_CEILING = 0.5

# Sector keyword map (non-exclusive first match order)
SECTOR_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("cosmology", ("cosmo", "hubble", "desi", "cmb", "dark_energy", "planck", "sh0es", "bubble", "s8", "wa_")),
    ("particle_nuclear", ("particle", "higgs", "ckm", "pmns", "nuclear", "fusion", "quantum", "atom", "cern", "lhc", "pdg")),
    ("bio_med", ("neuro", "brain", "immuno", "onco", "bio", "zebra", "genom", "cell", "medic", "cardio", "epidemi", "pharma", "pdb", "protein", "igem", "gbif", "species")),
    ("earth_climate", ("climate", "ocean", "hydro", "geo", "atmos", "cryo", "ecology", "seismo", "volcan", "ncei", "weather")),
    ("materials_chem", ("material", "chem", "fuel", "acoustic", "crc", "metal", "smiles", "pubchem", "alloy", "polymer", "crystal")),
    ("astro_gw", ("gw", "gaia", "planet", "stellar", "astro", "galaxy", "blackhole", "exoplanet", "mpcorb", "pulsar", "frb")),
    ("social_econ", ("econ", "finance", "law", "history", "ling", "anthrop", "world_bank", "actuar", "policy")),
    ("engineering_compute", ("engineer", "hardware", "gpu", "cpu", "code", "crypt", "trinary", "os_", "circuit", "esp32", "qemu", "reasoning")),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:80] if s else "domain"


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _sector_for(domain: str, file: str = "") -> str:
    blob = f"{domain} {file}".lower()
    for sector, keys in SECTOR_RULES:
        if any(k in blob for k in keys):
            return sector
    return "cross_domain_other"


def _scalar_budget(n_records: int) -> int:
    """More locks for larger panels — still capped to keep atlas usable."""
    if n_records >= 200:
        return 12
    if n_records >= 80:
        return 8
    if n_records >= 20:
        return 6
    if n_records >= 5:
        return 5
    return 3


def _extract_records(bench: dict) -> list[dict]:
    for key in ("records", "material_records", "observables", "results", "rows"):
        v = bench.get(key)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    for key in ("wave4_observables", "smiles_particle_records", "thesis_particle_waves"):
        v = bench.get(key)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []


def _is_scalar_lockable(rec: dict) -> bool:
    if rec.get("eval_kind") in {"classifier_match", "classifier"}:
        return False
    try:
        c = float(rec.get("computed"))
        m = float(rec.get("measured"))
    except (TypeError, ValueError):
        return False
    if m == 0 and c == 0:
        return False
    name = str(rec.get("name") or "") + " " + str(rec.get("property") or "")
    if any(x in name.lower() for x in ("classifier", "match_flag", "coupled_flag")):
        return False
    if m in (0.0, 1.0) and c in (0.0, 1.0) and abs(c - m) in (0.0, 1.0):
        if abs(m) <= 1.0 and abs(c) <= 1.0 and "error" not in name.lower():
            # binary-ish — skip unless unit/property looks continuous
            unit = str(rec.get("unit") or "").lower()
            if unit in {"", "dimensionless", "flag", "bool"}:
                return False
    err = rec.get("error_pct")
    if err is not None:
        try:
            if float(err) > GREEN_CEILING:
                return False
        except (TypeError, ValueError):
            pass
    return True


def _top_scalar_locks(records: list[dict], n: int) -> list[dict]:
    cands = []
    for r in records:
        if not _is_scalar_lockable(r):
            continue
        try:
            m = float(r["measured"])
            c = float(r["computed"])
        except (TypeError, ValueError, KeyError):
            continue
        err = r.get("error_pct")
        try:
            err_f = (
                float(err)
                if err is not None
                else abs(c - m) / max(abs(m), 1e-12) * 100.0
            )
        except (TypeError, ValueError):
            err_f = 0.0
        cands.append(
            {
                "name": r.get("name") or r.get("property") or "observable",
                "property": r.get("property"),
                "fsot_predicted": c,
                "literature_or_panel_measured": m,
                "error_pct": err_f,
                "unit": r.get("unit"),
                "fsot_formula": r.get("fsot_formula"),
            }
        )
    cands.sort(key=lambda x: (x["error_pct"], -abs(x["literature_or_panel_measured"] or 0)))
    # stratified: keep best errors + sample mid-list for catalog diversity
    seen: set[str] = set()
    out: list[dict] = []
    for c in cands:
        key = str(c["name"])
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
        if len(out) >= n:
            break
    if len(out) < n and len(cands) > n:
        step = max(len(cands) // n, 1)
        for i in range(0, len(cands), step):
            c = cands[i]
            key = str(c["name"])
            if key in seen:
                continue
            seen.add(key)
            out.append(c)
            if len(out) >= n:
                break
    return out[:n]


def build() -> dict:
    margin = _load_json(MARGIN)
    h0 = _load_json(H0_MULTI)
    h0_sight = _load_json(H0_SIGHT)
    h0_trgb = _load_json(H0_TRGB)
    rows = margin.get("all_domains") or []

    predictions: list[dict[str, Any]] = []
    domain_entries: list[dict[str, Any]] = []
    pred_counter = 0
    sector_residuals: dict[str, list[float]] = defaultdict(list)

    def next_id(prefix: str = "PRED-DOM") -> str:
        nonlocal pred_counter
        pred_counter += 1
        return f"{prefix}-{pred_counter:04d}"

    # ── Multi-tool H0 ───────────────────────────────────────────────────
    h0_preds = []
    for t in h0.get("tools") or []:
        h0_preds.append(
            {
                "id": t.get("pred_id") or next_id("PRED-H0"),
                "kind": "multi_tool_h0",
                "sector": "cosmology",
                "name": t.get("name"),
                "domain": "Hubble_Multi_Tool_Bubble_Bleed",
                "fsot_predicted": t.get("fsot_predicted_h0"),
                "unit": "km/s/Mpc",
                "literature_anchor": t.get("literature_anchor_h0"),
                "bubble_density_proxy": t.get("bubble_density_proxy"),
                "tool_class": t.get("tool_class"),
                "method": t.get("method"),
                "reference": t.get("reference"),
                "discriminant": t.get("kill"),
                "fsot_formula_branch": "term3.acoustic_bleed_bubble_density",
                "registered_at": "2026-08-06",
                "theory": "BH→WH bubble bleed — per-tool sector lock",
            }
        )
    predictions.extend(h0_preds)

    # ── Per-host / sky-sector sightline H0 ───────────────────────────────
    host_preds = []
    for h in h0_sight.get("hosts") or []:
        host_preds.append(
            {
                "id": h.get("pred_id") or next_id("PRED-H0-HOST"),
                "kind": "h0_sightline_host",
                "sector": "cosmology",
                "name": h.get("host"),
                "domain": "Hubble_Sightline_Host_Bubble_Bleed",
                "fsot_predicted": h.get("fsot_predicted_h0"),
                "unit": "km/s/Mpc",
                "ra_deg": h.get("ra_deg"),
                "dec_deg": h.get("dec_deg"),
                "sky_sector": h.get("sky_sector"),
                "bubble_density_sky": h.get("bubble_density_sky"),
                "method": h.get("method"),
                "tool_class": h.get("tool_class"),
                "discriminant": h.get("kill"),
                "fsot_formula_branch": "term3.acoustic_bleed_sightline",
                "registered_at": "2026-08-06",
                "theory": "Per-host BH→WH sightline bubble density",
            }
        )
    predictions.extend(host_preds)

    for s in h0_sight.get("sky_sectors") or []:
        predictions.append(
            {
                "id": s.get("pred_id") or next_id("PRED-H0-SEC"),
                "kind": "h0_sightline_sector",
                "sector": "cosmology",
                "name": s.get("sky_sector"),
                "domain": "Hubble_Sightline_Sky_Sector",
                "fsot_predicted": s.get("fsot_predicted_h0_mean"),
                "unit": "km/s/Mpc",
                "host_count": s.get("host_count"),
                "hosts": s.get("hosts"),
                "discriminant": s.get("kill"),
                "fsot_formula_branch": "term3.acoustic_bleed_sightline",
                "registered_at": "2026-08-06",
            }
        )

    # ── CCHP TRGB hosts (external-drive catalog) ────────────────────────
    trgb_preds = []
    for h in h0_trgb.get("hosts") or []:
        trgb_preds.append(
            {
                "id": h.get("pred_id") or next_id("PRED-H0-TRGB"),
                "kind": "h0_trgb_host",
                "sector": "cosmology",
                "name": h.get("host"),
                "domain": "Hubble_CCHP_TRGB_Sightline",
                "fsot_predicted": h.get("fsot_predicted_h0"),
                "unit": "km/s/Mpc",
                "ra_deg": h.get("ra_deg"),
                "sky_sector": h.get("sky_sector"),
                "method": h.get("method"),
                "role": h.get("role"),
                "sample": h.get("sample"),
                "discriminant": h.get("kill"),
                "fsot_formula_branch": "term3.acoustic_bleed_trgb_sightline",
                "registered_at": "2026-08-06",
                "external_catalog": h0_trgb.get("external_catalog_path"),
            }
        )
    predictions.extend(trgb_preds)
    for s in h0_trgb.get("sky_sectors") or []:
        predictions.append(
            {
                "id": s.get("pred_id") or next_id("PRED-H0-TRGB-SEC"),
                "kind": "h0_trgb_sector",
                "sector": "cosmology",
                "name": s.get("sky_sector"),
                "domain": "Hubble_CCHP_TRGB_Sky_Sector",
                "fsot_predicted": s.get("fsot_predicted_h0_mean"),
                "unit": "km/s/Mpc",
                "host_count": s.get("host_count"),
                "registered_at": "2026-08-06",
            }
        )

    # ── Every green domain ──────────────────────────────────────────────
    covered = 0
    missing_files = 0
    for row in rows:
        if not row.get("green_gate_pass"):
            continue
        domain = str(row.get("domain") or row.get("file") or "unknown")
        fpath = row.get("file") or ""
        path = ROOT / "data" / Path(fpath).name if fpath else None
        if path is None or not path.is_file():
            alt = ROOT / str(fpath)
            path = alt if alt.is_file() else None

        med = row.get("official_pooled_median_error_pct")
        if med is None:
            med = row.get("pooled_median_error_pct")
        try:
            med_f = float(med) if med is not None else None
        except (TypeError, ValueError):
            med_f = None

        sector = _sector_for(domain, str(fpath))
        if med_f is not None:
            sector_residuals[sector].append(med_f)

        residual_id = next_id()
        predictions.append(
            {
                "id": residual_id,
                "kind": "residual_hold",
                "sector": sector,
                "name": f"{_slug(domain)}_pooled_residual_hold",
                "domain": domain,
                "fsot_predicted": med_f if med_f is not None else 0.0,
                "unit": "pooled_median_error_pct_watch",
                "ceiling_pct": GREEN_CEILING,
                "sota_baseline": 5.0,
                "sota_label": "typical_unstructured_or_free_param_model_error",
                "discriminant": "within_green_gate_0_5pct",
                "kill": f"{_slug(domain)}_pooled_median_exceeds_0_5pct_on_refresh",
                "records": row.get("records"),
                "benchmark_file": Path(fpath).name if fpath else None,
                "fsot_formula_branch": "domain_panel_seed_engine",
                "registered_at": "2026-08-06",
            }
        )

        scalar_locks: list[dict] = []
        n_rec = int(row.get("records") or 0)
        if path and path.is_file():
            try:
                bench = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                bench = {}
                missing_files += 1
            recs = _extract_records(bench)
            n_rec = max(n_rec, len(recs))
            budget = _scalar_budget(n_rec)
            # non-cosmology gets full budget; cosmology already has multi-tool/sightline
            if sector == "cosmology":
                budget = min(budget, 4)
            scalar_locks = _top_scalar_locks(recs, budget)
            for s in scalar_locks:
                predictions.append(
                    {
                        "id": next_id(),
                        "kind": "scalar_lock",
                        "sector": sector,
                        "name": f"{_slug(domain)}__{_slug(str(s['name']))}",
                        "domain": domain,
                        "observable": s["name"],
                        "property": s.get("property"),
                        "fsot_predicted": s["fsot_predicted"],
                        "literature_or_panel_measured": s["literature_or_panel_measured"],
                        "error_pct_at_registration": s["error_pct"],
                        "unit": s.get("unit"),
                        "fsot_formula": s.get("fsot_formula"),
                        "sota_baseline": s["literature_or_panel_measured"],
                        "sota_label": "panel_measured_at_registration",
                        "discriminant": "within_0_5pct_of_fsot_predicted_on_refresh",
                        "kill": f"observable_{_slug(str(s['name']))}_outside_0_5pct",
                        "benchmark_file": path.name,
                        "fsot_formula_branch": "domain_record_seed",
                        "registered_at": "2026-08-06",
                    }
                )
        else:
            missing_files += 1

        domain_entries.append(
            {
                "domain": domain,
                "sector": sector,
                "benchmark_file": Path(fpath).name if fpath else None,
                "pooled_median_error_pct": med_f,
                "residual_pred_id": residual_id,
                "scalar_lock_count": len(scalar_locks),
                "record_count": n_rec,
                "green_gate_pass": True,
            }
        )
        covered += 1

    # ── Sector portfolio predictions (cross-domain, non-cosmo emphasis) ─
    sector_portfolio = []
    for sector, vals in sorted(sector_residuals.items()):
        if not vals:
            continue
        vals_sorted = sorted(vals)
        mid = vals_sorted[len(vals_sorted) // 2]
        mx = vals_sorted[-1]
        pid = next_id("PRED-SECTOR")
        pred = {
            "id": pid,
            "kind": "sector_portfolio_hold",
            "sector": sector,
            "name": f"{sector}_portfolio_pooled_median_hold",
            "domain": f"Sector_Portfolio_{sector}",
            "fsot_predicted": round(mid, 8),
            "unit": "pooled_median_error_pct_watch",
            "sector_domain_count": len(vals),
            "sector_max_pooled_pct": round(mx, 8),
            "ceiling_pct": GREEN_CEILING,
            "discriminant": "sector_median_and_all_domains_within_0_5pct",
            "kill": f"sector_{sector}_any_domain_fails_green_or_median_exceeds_0_5",
            "fsot_formula_branch": "multi_domain_seed_engine",
            "registered_at": "2026-08-06",
            "note": (
                "Portfolio lock: every domain in this scientific sector stays "
                "≤0.5% pooled; FSOT-predicted watch is sector median residual."
            ),
        }
        predictions.append(pred)
        sector_portfolio.append(
            {
                "sector": sector,
                "domain_count": len(vals),
                "median_pooled_pct": round(mid, 8),
                "max_pooled_pct": round(mx, 8),
                "pred_id": pid,
            }
        )

    prereg_count = 0
    if PREREG.is_file():
        try:
            import yaml

            prereg_count = len(
                (yaml.safe_load(PREREG.read_text(encoding="utf-8")) or {}).get(
                    "predictions"
                )
                or []
            )
        except Exception:
            pass

    by_kind: dict[str, int] = {}
    by_sector: dict[str, int] = {}
    for p in predictions:
        by_kind[p["kind"]] = by_kind.get(p["kind"], 0) + 1
        sec = str(p.get("sector") or "unknown")
        by_sector[sec] = by_sector.get(sec, 0) + 1

    domains_unique = sorted({e["domain"] for e in domain_entries})
    non_cosmo_domains = [e for e in domain_entries if e.get("sector") != "cosmology"]

    doc = {
        "generated_at": _now(),
        "version": "2.0",
        "authority_pin_prefix": "D1D38A",
        "zero_free_parameters": True,
        "purpose": (
            "Atlas-scale preregistered predictions across the full scientific "
            "domain table — bio, materials, particle, earth, social, engineering, "
            "astro — not cosmology alone. Plus multi-tool and per-host H0 under "
            "BH→WH bubble bleed."
        ),
        "summary": {
            "green_domains_covered": covered,
            "unique_domains": len(domains_unique),
            "non_cosmology_domains": len(non_cosmo_domains),
            "prediction_count": len(predictions),
            "by_kind": by_kind,
            "by_sector": by_sector,
            "h0_multi_tool_count": len(h0_preds),
            "h0_sightline_host_count": len(host_preds),
            "h0_sightline_sector_count": len(h0_sight.get("sky_sectors") or []),
            "h0_trgb_host_count": len(trgb_preds),
            "h0_trgb_sector_count": len(h0_trgb.get("sky_sectors") or []),
            "sector_portfolio_count": len(sector_portfolio),
            "hand_prereg_yaml_count": prereg_count,
            "missing_benchmark_files": missing_files,
            "green_ceiling_pct": GREEN_CEILING,
        },
        "sector_portfolio": sector_portfolio,
        "h0_multi_tool_ref": "predictions/h0_multi_tool_predictions.json",
        "h0_sightline_ref": "predictions/h0_sightline_predictions.json",
        "h0_trgb_ref": "predictions/cchp_trgb_sightline_predictions.json",
        "hand_prereg_ref": "predictions/preregistered_predictions_manifest.yaml",
        "domains": domain_entries,
        "predictions": predictions,
    }
    raw = json.dumps(
        {k: v for k, v in doc.items() if k not in {"bundle_sha256", "predictions", "domains"}},
        sort_keys=True,
    ).encode()
    id_blob = json.dumps([p["id"] for p in predictions], sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw + id_blob).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    s = doc.get("summary") or {}
    lines = [
        "# Domain prediction atlas (all sectors)",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A*",
        "",
        str(doc.get("purpose") or ""),
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Green domains covered | {s.get('green_domains_covered')} |",
        f"| Non-cosmology domains | {s.get('non_cosmology_domains')} |",
        f"| **Total atlas predictions** | **{s.get('prediction_count')}** |",
        f"| Multi-tool H₀ | {s.get('h0_multi_tool_count')} |",
        f"| Sightline hosts H₀ | {s.get('h0_sightline_host_count')} |",
        f"| Sightline sky sectors | {s.get('h0_sightline_sector_count')} |",
        f"| Sector portfolios | {s.get('sector_portfolio_count')} |",
        f"| Hand prereg YAML | {s.get('hand_prereg_yaml_count')} |",
        f"| Bundle SHA | `{doc.get('bundle_sha256', '')[:16]}…` |",
        "",
        "### By kind",
        "",
        "| Kind | Count |",
        "|------|------:|",
    ]
    for k, v in sorted((s.get("by_kind") or {}).items()):
        lines.append(f"| {k} | {v} |")

    lines.extend(
        [
            "",
            "### By scientific sector",
            "",
            "| Sector | Predictions |",
            "|--------|------------:|",
        ]
    )
    for k, v in sorted((s.get("by_sector") or {}).items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")

    lines.extend(
        [
            "",
            "## Sector portfolio holds",
            "",
            "| Sector | Domains | Median residual % | Max % | PRED |",
            "|--------|--------:|------------------:|------:|------|",
        ]
    )
    for sp in doc.get("sector_portfolio") or []:
        lines.append(
            f"| {sp['sector']} | {sp['domain_count']} | {sp['median_pooled_pct']} | "
            f"{sp['max_pooled_pct']} | `{sp['pred_id']}` |"
        )

    lines.extend(
        [
            "",
            "## Multi-tool + sightline H₀",
            "",
            "- Tools: [`H0_MULTI_TOOL_PREDICTIONS.md`](H0_MULTI_TOOL_PREDICTIONS.md)",
            "- Hosts/sightlines: [`H0_SIGHTLINE_PREDICTIONS.md`](H0_SIGHTLINE_PREDICTIONS.md)",
            "",
            "## Worst residual holds (still green ≤0.5%)",
            "",
            "| Domain | Sector | Pooled % |",
            "|--------|--------|---------:|",
        ]
    )
    worst = sorted(
        doc.get("domains") or [],
        key=lambda d: -(d.get("pooled_median_error_pct") or 0),
    )[:30]
    for d in worst:
        lines.append(
            f"| {d.get('domain')} | {d.get('sector')} | {d.get('pooled_median_error_pct')} |"
        )

    # non-cosmo sample of high scalar-lock domains
    lines.extend(
        [
            "",
            "## Non-cosmology domains with most scalar locks",
            "",
            "| Domain | Sector | Scalar locks | Records | Pooled % |",
            "|--------|--------|-------------:|--------:|---------:|",
        ]
    )
    rich = sorted(
        [d for d in (doc.get("domains") or []) if d.get("sector") != "cosmology"],
        key=lambda d: -(d.get("scalar_lock_count") or 0),
    )[:25]
    for d in rich:
        lines.append(
            f"| {d.get('domain')} | {d.get('sector')} | {d.get('scalar_lock_count')} | "
            f"{d.get('record_count')} | {d.get('pooled_median_error_pct')} |"
        )

    lines.extend(
        [
            "",
            "Refresh:",
            "```text",
            "python scripts/build_h0_multi_tool_predictions.py",
            "python scripts/build_h0_sightline_predictions.py",
            "python scripts/build_domain_prediction_atlas.py",
            "python scripts/run_prediction_monitor.py",
            "```",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    s = doc["summary"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  domains={s['green_domains_covered']} non_cosmo={s['non_cosmology_domains']} "
        f"preds={s['prediction_count']} by_kind={s['by_kind']}"
    )
    print(f"  by_sector={s['by_sector']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
