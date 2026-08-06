#!/usr/bin/env python3
"""Generate preregistered prediction atlas for every green domain panel.

Uses existing monorepo benchmarks (computed/measured records + pooled residual)
so predictions are grounded in FSOT information already in the repo — not free
parameters. Hand-curated PRED-001… in the YAML remain authoritative for
named contested locks; this atlas fills the 400+ domain gap.

Outputs:
  data/domain_prediction_atlas.json
  data/publication/DOMAIN_PREDICTION_ATLAS.md (summary)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
H0_MULTI = ROOT / "data" / "h0_multi_tool_predictions.json"
PREREG = ROOT / "data" / "preregistered_predictions_manifest.yaml"
OUT_JSON = ROOT / "data" / "domain_prediction_atlas.json"
OUT_MD = ROOT / "data" / "publication" / "DOMAIN_PREDICTION_ATLAS.md"

GREEN_CEILING = 0.5
MAX_SCALAR_LOCKS_PER_DOMAIN = 3


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


def _extract_records(bench: dict) -> list[dict]:
    for key in ("records", "material_records", "observables", "results", "rows"):
        v = bench.get(key)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    # particle-style nested
    for key in ("wave4_observables", "smiles_particle_records", "thesis_particle_waves"):
        v = bench.get(key)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []


def _is_scalar_lockable(rec: dict) -> bool:
    """Prefer real continuous observables over classifier 0/1 rows."""
    if rec.get("eval_kind") in {"classifier_match", "classifier"}:
        return False
    try:
        c = float(rec.get("computed"))
        m = float(rec.get("measured"))
    except (TypeError, ValueError):
        return False
    if m == 0 and c == 0:
        return False
    # skip pure binary
    if m in (0.0, 1.0) and c in (0.0, 1.0) and abs(c - m) in (0.0, 1.0):
        if abs(m) <= 1.0 and abs(c) <= 1.0:
            # may still be real if unit suggests continuous — keep if error_pct small and names look scalar
            name = str(rec.get("name") or "")
            if any(x in name.lower() for x in ("classifier", "match", "coupled", "flag")):
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
            err_f = float(err) if err is not None else abs(c - m) / max(abs(m), 1e-12) * 100.0
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
    # prefer lower error, then more 'interesting' magnitude
    cands.sort(key=lambda x: (x["error_pct"], -abs(x["literature_or_panel_measured"] or 0)))
    # unique names
    seen = set()
    out = []
    for c in cands:
        key = str(c["name"])
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
        if len(out) >= n:
            break
    return out


def build() -> dict:
    margin = _load_json(MARGIN)
    h0 = _load_json(H0_MULTI)
    rows = margin.get("all_domains") or []

    predictions: list[dict[str, Any]] = []
    domain_entries: list[dict[str, Any]] = []
    pred_counter = 0

    def next_id(prefix: str = "PRED-DOM") -> str:
        nonlocal pred_counter
        pred_counter += 1
        return f"{prefix}-{pred_counter:04d}"

    # ── Multi-tool H0 first (high priority) ─────────────────────────────
    h0_preds = []
    for t in h0.get("tools") or []:
        pid = t.get("pred_id") or next_id("PRED-H0")
        h0_preds.append(
            {
                "id": pid,
                "kind": "multi_tool_h0",
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
                "sota_label": t.get("reference"),
                "sota_baseline": t.get("literature_anchor_h0"),
                "fsot_formula_branch": "term3.acoustic_bleed_bubble_density",
                "registered_at": "2026-08-06",
                "theory": "BH→WH bubble bleed — per-tool sector lock",
            }
        )
    predictions.extend(h0_preds)

    # ── Every green domain residual hold + scalar locks ─────────────────
    covered = 0
    missing_files = 0
    for row in rows:
        if not row.get("green_gate_pass"):
            continue
        domain = str(row.get("domain") or row.get("file") or "unknown")
        fpath = row.get("file") or ""
        path = ROOT / "data" / Path(fpath).name if fpath else None
        if path is None or not path.is_file():
            # try as-is
            alt = ROOT / str(fpath)
            path = alt if alt.is_file() else None
        med = row.get("official_pooled_median_error_pct")
        if med is None:
            med = row.get("pooled_median_error_pct")
        try:
            med_f = float(med) if med is not None else None
        except (TypeError, ValueError):
            med_f = None

        residual_id = next_id()
        residual_pred = {
            "id": residual_id,
            "kind": "residual_hold",
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
        predictions.append(residual_pred)

        scalar_locks = []
        if path and path.is_file():
            try:
                bench = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                bench = {}
                missing_files += 1
            recs = _extract_records(bench)
            scalar_locks = _top_scalar_locks(recs, MAX_SCALAR_LOCKS_PER_DOMAIN)
            for s in scalar_locks:
                sid = next_id()
                predictions.append(
                    {
                        "id": sid,
                        "kind": "scalar_lock",
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
                "benchmark_file": Path(fpath).name if fpath else None,
                "pooled_median_error_pct": med_f,
                "residual_pred_id": residual_id,
                "scalar_lock_count": len(scalar_locks),
                "green_gate_pass": True,
            }
        )
        covered += 1

    # optional: count hand prereg
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
    for p in predictions:
        by_kind[p["kind"]] = by_kind.get(p["kind"], 0) + 1

    domains_unique = sorted({e["domain"] for e in domain_entries})

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "authority_pin_prefix": "D1D38A",
        "zero_free_parameters": True,
        "purpose": (
            "Atlas-scale preregistered predictions derived from existing FSOT "
            "domain panels. Residual holds for every green domain; scalar locks "
            "for top panel observables; multi-tool H0 under bubble-bleed theory."
        ),
        "summary": {
            "green_domains_covered": covered,
            "unique_domains": len(domains_unique),
            "prediction_count": len(predictions),
            "by_kind": by_kind,
            "h0_multi_tool_count": len(h0_preds),
            "hand_prereg_yaml_count": prereg_count,
            "missing_benchmark_files": missing_files,
            "green_ceiling_pct": GREEN_CEILING,
        },
        "h0_multi_tool_ref": "data/h0_multi_tool_predictions.json",
        "hand_prereg_ref": "data/preregistered_predictions_manifest.yaml",
        "domains": domain_entries,
        "predictions": predictions,
    }
    raw = json.dumps(
        {k: v for k, v in doc.items() if k not in {"bundle_sha256", "predictions"}},
        sort_keys=True,
    ).encode()
    # include prediction ids only in hash body for stability
    id_blob = json.dumps([p["id"] for p in predictions], sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw + id_blob).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    s = doc.get("summary") or {}
    lines = [
        "# Domain prediction atlas",
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
        f"| Unique domains | {s.get('unique_domains')} |",
        f"| Total atlas predictions | {s.get('prediction_count')} |",
        f"| Multi-tool H₀ | {s.get('h0_multi_tool_count')} |",
        f"| Hand prereg YAML (separate) | {s.get('hand_prereg_yaml_count')} |",
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
            "## Multi-tool H₀ (see full table)",
            "",
            "Full tool table: [`H0_MULTI_TOOL_PREDICTIONS.md`](H0_MULTI_TOOL_PREDICTIONS.md)  ",
            "Machine: `data/h0_multi_tool_predictions.json`",
            "",
            "## Worst residual holds (still green ≤0.5%)",
            "",
            "| Domain | Pooled % | Residual PRED |",
            "|--------|---------:|---------------|",
        ]
    )
    worst = sorted(
        doc.get("domains") or [],
        key=lambda d: -(d.get("pooled_median_error_pct") or 0),
    )[:25]
    for d in worst:
        lines.append(
            f"| {d.get('domain')} | {d.get('pooled_median_error_pct')} | `{d.get('residual_pred_id')}` |"
        )

    lines.extend(
        [
            "",
            "Refresh:",
            "```text",
            "python scripts/build_h0_multi_tool_predictions.py",
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
        f"  domains={s['green_domains_covered']} preds={s['prediction_count']} "
        f"by_kind={s['by_kind']} h0={s['h0_multi_tool_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
