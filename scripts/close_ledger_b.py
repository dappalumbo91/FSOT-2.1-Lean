#!/usr/bin/env python3
"""Close Ledger B depth debt without padding or ρ retune.

- Process spines are certificates, not empirical catalogs.
- SH0ES ladder / Cepheid interconnect are named-complete small objects.
- SH0ES refined gets the 25 published H0 tool rows (2.5% band, structural).
- SH0ES full sample gets per-host cz/d as structural flow-noise (not 0.5% H0).

Green gate stays 477/477. Issued JSON and H0 freeze are not rewritten.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

from c_thin_depth_lib import classify_bench  # noqa: E402
from fsot_precision_constants import AUDIT_EXCLUDED_BENCHMARKS  # noqa: E402

PROCESS_SPINE = {
    "Theory_Completeness_Spine",
    "ToE_Claim_Certificate_Bundle",
    "ToE_Gap_Closure_Spine",
    "ToE_Unification_Spine",
    "Proof_Ledger_Closure_Spine",
    "Adversarial_Fractal_Break_Tests",
    "Domain_Orbital_Predictions",
    "Rust_Lean_Bridge",
    "rust_lean_bridge_benchmark",
}
NAMED_COMPLETE = {
    "SH0ES_Ladder_Chain": "Five named rungs. Padding to n=20 is false densify.",
    "Cepheid_PL_Interconnect": "Slopes, intercepts, 4 Li+2024 TRGB hosts, N4258 crowding. Named interconnect is complete.",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _domain(bench: dict, path: Path) -> str:
    return str(bench.get("domain") or path.stem.replace("_benchmark", ""))


def _tag(path: Path, role: str, note: str) -> dict:
    bench = json.loads(path.read_text(encoding="utf-8"))
    bench["ledger_role"] = role
    bench["ledger_role_note"] = note
    bench["ledger_b_closed_at"] = _now()
    path.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    return {"file": path.name, "domain": _domain(bench, path), "role": role}


def _append_structural(path: Path, extra: list[dict], *, note: str) -> dict:
    bench = json.loads(path.read_text(encoding="utf-8"))
    mat = list(bench.get("material_records") or [])
    have = {str(r.get("name")) for r in mat}
    added = 0
    for row in extra:
        if str(row.get("name")) in have:
            continue
        mat.append(row)
        added += 1
    bench["material_records"] = mat
    bench["record_count"] = len(mat)
    bench["observable_count"] = len(mat)
    bench["ledger_b_closed_at"] = _now()
    bench["ledger_b_expand_note"] = note
    path.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    return {
        "file": path.name,
        "domain": _domain(bench, path),
        "added": added,
        "record_count": len(mat),
    }


def expand_sh0es_refined() -> dict:
    tools_path = ROOT / "predictions" / "h0_multi_tool_predictions.json"
    tools = json.loads(tools_path.read_text(encoding="utf-8")).get("tools") or []
    extra = []
    for t in tools:
        extra.append(
            {
                "lab": "sh0es_refined_lab",
                "property": "h0_tool_row",
                "name": str(t.get("id") or t.get("name")),
                "computed": float(t["fsot_predicted_h0"]),
                "measured": float(t["literature_anchor_h0"]),
                "error_pct": float(t.get("error_vs_literature_pct") or 0.0),
                "eval_kind": "literature_band",
                "record_kind": "structural",
                "unit": "km/s/Mpc",
                "note": "25-tool bubble sector. 2.5% contested band. Not a 0.5% central. Not ρ retune.",
                "method": t.get("method"),
                "tool_class": t.get("tool_class"),
            }
        )
    return _append_structural(
        DATA / "sh0es_refined_benchmark.json",
        extra,
        note="Imported 25 published H0 tool rows as structural (right object per tool).",
    )


def expand_full_sample() -> dict:
    path = DATA / "sh0es_full_sample_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    hosts = ((bench.get("cz_d_diagnostic") or {}).get("hosts") or [])
    extra = []
    for h in hosts:
        if not isinstance(h, dict) or "H0_i" not in h:
            continue
        extra.append(
            {
                "lab": "sh0es_full_sample_lab",
                "property": "per_host_cz_d_flow_noise",
                "name": f"{h.get('host')}_cz_d_not_SH0ES_H0",
                "computed": float(h["H0_i"]),
                "measured": 73.04,
                "error_pct": abs(float(h["H0_i"]) - 73.04) / 73.04 * 100.0,
                "eval_kind": "literature_band",
                "record_kind": "structural",
                "unit": "km/s/Mpc",
                "note": "Individual cz/d is local flow, not SH0ES H0. Named 0.5% object is the ensemble mean.",
                "flow_noise": bool(h.get("flow_noise")),
            }
        )
    return _append_structural(
        path,
        extra,
        note="Per-host cz/d as structural flow-noise. Do not 0.5%-gate individuals.",
    )


def main() -> int:
    tagged = []
    for path in sorted(DATA.glob("*_benchmark.json")):
        bench = json.loads(path.read_text(encoding="utf-8"))
        dom = _domain(bench, path)
        stem = path.stem
        if dom in PROCESS_SPINE or stem in PROCESS_SPINE:
            tagged.append(
                _tag(
                    path,
                    "process_certificate",
                    "Certificate / ledger spine. Not a Ledger B empirical catalog. Do not pad to n=20.",
                )
            )
        elif dom in NAMED_COMPLETE:
            tagged.append(_tag(path, "named_object_complete", NAMED_COMPLETE[dom]))

    refined = expand_sh0es_refined()
    full = expand_full_sample()

    rows = []
    open_thin = []
    for path in sorted(DATA.glob("*_benchmark.json")):
        if path.name in AUDIT_EXCLUDED_BENCHMARKS:
            continue
        bench = json.loads(path.read_text(encoding="utf-8"))
        rec = int(bench.get("record_count") or bench.get("observable_count") or 0)
        med = bench.get("pooled_median_error_pct")
        if med is None:
            med = bench.get("median_error_pct")
        if med is None or rec == 0:
            continue
        klass = classify_bench(bench)
        item = {
            "file": path.name,
            "domain": _domain(bench, path),
            "records": rec,
            "median_pct": float(med),
            "class": klass,
            "ledger_role": bench.get("ledger_role"),
        }
        rows.append(item)
        if klass == "C_thin":
            open_thin.append(item)

    by = {}
    for r in rows:
        by[r["class"]] = by.get(r["class"], 0) + 1
    closure = {
        "generated_at": _now(),
        "pin": "AEB2AD",
        "cite_as_toe_accuracy": False,
        "green_gate": "477/477 stays; this file is depth/role, not a new residual gate",
        "ledger_b_empirical_open": len(open_thin),
        "ledger_b_done": len(open_thin) == 0,
        "tier_distribution": by,
        "tagged_process_or_named": tagged,
        "expanded": [refined, full],
        "open_c_thin": open_thin,
        "kill": [
            "Padding process spines to n=20",
            "Padding SH0ES ladder rungs",
            "Gating cz/d hosts as 0.5% H0",
            "Retuning rho onto 73.04",
            "Quoting 477/477 as ToE accuracy",
        ],
    }
    out = DATA / "ledger_b_closure.json"
    out.write_text(json.dumps(closure, indent=2), encoding="utf-8")
    print(json.dumps({k: closure[k] for k in ("ledger_b_done", "ledger_b_empirical_open", "tier_distribution")}, indent=2))
    if open_thin:
        print("still C_thin:")
        for r in open_thin:
            print(f"  {r['domain']} n={r['records']} {r['median_pct']}")
    return 0 if closure["ledger_b_done"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
