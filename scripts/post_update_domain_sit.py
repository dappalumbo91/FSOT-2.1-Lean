#!/usr/bin/env python3
"""Where every nest core sits after π-identity + derived D/look/observed.

Read-only vs Ledger A freeze. Samples Ledger B drift without rewriting catalogs.
Does not retune. Does not rewrite dated forecasts.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import (  # noqa: E402
    DOMAINS,
    K,
    C_COSM,
    C_EFF,
    ALPHA,
    MEDIUM_ORIFICES,
    derived_D_eff,
    domain_scalar,
    _fold_look,
    _fold_hits,
    _fold_observed,
)
from fsot_api_predict_lib import fsot_correct  # noqa: E402
from fsot_ledger_a_lib import LEDGER_A, compare_anchor, engine_pin  # noqa: E402
from benchmark_margin_lib import STRUCTURAL_EVAL_KINDS  # noqa: E402

OUT = ROOT / "results" / "post_update_domain_sit.json"

PAIRS = [
    ("Quantum_Mechanics", "Atomic_Physics"),
    ("Atomic_Physics", "High_Energy_Physics"),
    ("Chemistry", "Physical_Chemistry"),
    ("Chemistry", "Molecular_Chemistry"),
    ("Electromagnetism", "Optics"),
    ("Optics", "Materials_Science"),
    ("Optics", "Acoustics"),
    ("Biology", "Biochemistry"),
    ("Biochemistry", "Neuroscience"),
    ("Condensed_Matter", "Thermodynamics"),
    ("Fluid_Dynamics", "Thermodynamics"),
    ("Fluid_Dynamics", "Nuclear_Physics"),
    ("Meteorology", "Atmospheric_Physics"),
    ("Seismology", "Geophysics"),
    ("Astronomy", "Economics"),
    ("Quantum_Gravity", "Cosmology"),
    ("Thermodynamics", "Cosmology"),
]


def _f(x) -> float:
    return float(x)


def main() -> int:
    pin = engine_pin()
    cores = []
    for name in sorted(DOMAINS):
        cfg = DOMAINS[name]
        s = _f(domain_scalar(name))
        cores.append(
            {
                "name": name,
                "D_eff": int(cfg.D_eff),
                "D_nest": int(derived_D_eff(name)),
                "look": str(cfg.delta_psi),
                "look_law": str(_fold_look(name)),
                "hits": int(cfg.hits),
                "hits_law": int(_fold_hits(name)),
                "observed": bool(cfg.observed),
                "observed_law": bool(_fold_observed(name)),
                "medium": name in MEDIUM_ORIFICES,
                "S": s,
                "abs_S": abs(s),
                "sign": "emergence" if s > 0 else "damping",
            }
        )

    ledger_a = []
    n_miss = 0
    for oid in sorted(LEDGER_A):
        rec = compare_anchor(oid)
        err = float(rec["error_pct"])
        kind = LEDGER_A[oid]["kind"]
        miss = kind == "FORECAST" and err > 0.5
        if miss:
            n_miss += 1
        ledger_a.append(
            {
                "id": oid,
                "kind": kind,
                "value": rec["value"],
                "anchor": LEDGER_A[oid]["anchor"],
                "error_pct": err,
                "outside_half_pct": miss,
            }
        )

    pairs = []
    for a, b in PAIRS:
        sa, sb = abs(_f(domain_scalar(a))), abs(_f(domain_scalar(b)))
        ratio = sa / sb if sb else None
        vs1 = abs(ratio - 1.0) * 100.0 if ratio is not None else None
        same_look = str(DOMAINS[a].delta_psi) == str(DOMAINS[b].delta_psi)
        same_d = int(DOMAINS[a].D_eff) == int(DOMAINS[b].D_eff)
        same_obs = bool(DOMAINS[a].observed) == bool(DOMAINS[b].observed)
        identity = same_look and same_d and same_obs
        pairs.append(
            {
                "pair": f"{a}/{b}",
                "D": [int(DOMAINS[a].D_eff), int(DOMAINS[b].D_eff)],
                "look_same": same_look,
                "observed_same": same_obs,
                "identity_same_fold": identity,
                "abs_S_ratio": ratio,
                "live_vs_1_pct": vs1,
            }
        )

    # Sample Ledger B drift on a handful of catalog files (no rewrite).
    sample_files = [
        "chemistry_ionization_benchmark.json",
        "optics_crc_n_d_benchmark.json",
        "materials_crc_density_benchmark.json",
        "seismology_prem_benchmark.json",
        "mpcorb_fsot_benchmark.json",
        "biology_strict_empirical.json",
        "endf_iaea_nuclear_open_benchmark.json",
        "noaa_ndbc_buoy_panel_benchmark.json",
    ]
    b_sample = []
    skip = set(STRUCTURAL_EVAL_KINDS)
    for fname in sample_files:
        path = ROOT / "data" / fname
        if not path.is_file():
            b_sample.append({"file": fname, "present": False})
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        recs = doc.get("records") or doc.get("material_records") or []
        drifts = []
        n = 0
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            kind = str(rec.get("eval_kind") or rec.get("kind") or "")
            if kind in skip:
                continue
            m = rec.get("measured")
            old = rec.get("computed")
            domain = str(rec.get("fsot_domain") or rec.get("domain") or doc.get("domain") or "")
            if not isinstance(m, (int, float)) or not isinstance(old, (int, float)) or not domain:
                continue
            if float(m) == 0.0:
                continue
            try:
                new, _err = fsot_correct(float(m), domain)
            except Exception:
                continue
            n += 1
            rel = abs(float(new) - float(old)) / max(abs(float(old)), 1e-30)
            if rel > 1e-12:
                drifts.append(rel)
        b_sample.append(
            {
                "file": fname,
                "present": True,
                "rescored_n": n,
                "drift_n": len(drifts),
                "max_rel_drift": max(drifts) if drifts else 0.0,
            }
        )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": pin,
        "K": _f(K),
        "C_EFF": _f(C_EFF),
        "C_COSM": _f(C_COSM),
        "ALPHA": _f(ALPHA),
        "cores": cores,
        "n_medium": sum(1 for c in cores if c["medium"]),
        "n_specimen": sum(1 for c in cores if not c["medium"]),
        "n_emergence": sum(1 for c in cores if c["sign"] == "emergence"),
        "n_damping": sum(1 for c in cores if c["sign"] == "damping"),
        "ledger_a": ledger_a,
        "n_forecast_outside_half_pct": n_miss,
        "pairs": pairs,
        "ledger_b_sample": b_sample,
        "note": "Live nest + π identities. Ledger A freeze not rewritten. Catalog files not rewritten.",
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"pin={pin} K={_f(K):.9f} cores={len(cores)} miss>0.5%={n_miss}")
    print(f"emergence={doc['n_emergence']} damping={doc['n_damping']} medium={doc['n_medium']}")
    for p in pairs:
        flag = "IDENTITY" if p["identity_same_fold"] else f"{p['live_vs_1_pct']:.3f}%"
        print(f"  {p['pair']:42s} vs1={flag}")
    for s in b_sample:
        if not s.get("present"):
            print(f"  B missing {s['file']}")
            continue
        print(
            f"  B {s['file']:42s} n={s['rescored_n']} drift_n={s['drift_n']} "
            f"max_rel={s['max_rel_drift']:.3e}"
        )
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
