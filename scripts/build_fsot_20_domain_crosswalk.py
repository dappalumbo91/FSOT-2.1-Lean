#!/usr/bin/env python3
"""Build crosswalk: FSOT-2.0-code (35 domains) ↔ NeuroLab authority ↔ Lean ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
FSOT_20_REPO = Path(r"C:\Users\damia\Desktop\FSOT-2.0-code")
EXPANSION_DOC = FSOT_20_REPO / "continued domain expansion"
PRECISION_REPORT = ROOT / "data" / "domain_precision_report.json"
REGISTRY_35 = ROOT / "data" / "fsot_35_domain_registry.yaml"
DRIFT_RESOLUTION = ROOT / "data" / "param_drift_resolution.yaml"
OUTPUT_JSON = ROOT / "data" / "fsot_20_domain_crosswalk.json"
OUTPUT_YAML = ROOT / "data" / "fsot_20_domain_crosswalk.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

# FSOT 2.0 README / continued-domain-expansion canonical names → NeuroLab names
NAME_MAP = {
    "Particle Physics": "Particle_Physics",
    "Physical Chemistry": "Physical_Chemistry",
    "Quantum Computing": "Quantum_Computing",
    "High-Energy Physics": "High_Energy_Physics",
    "Condensed Matter Physics": "Condensed_Matter",
    "Particle Astrophysics": "Particle_Astrophysics",
    "Quantum Mechanics": "Quantum_Mechanics",
    "Atomic Physics": "Atomic_Physics",
    "Molecular Chemistry": "Molecular_Chemistry",
    "Materials Science": "Materials_Science",
    "Atmospheric Physics": "Atmospheric_Physics",
    "Fluid Dynamics": "Fluid_Dynamics",
    "Nuclear Physics": "Nuclear_Physics",
    "Quantum Gravity": "Quantum_Gravity",
    "Quantum Optics": "Quantum_Optics",
    "Planetary Science": "Planetary_Science",
}


def _parse_expansion_doc(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict] = {}
    blocks = re.split(r"\n(?=\d+\.\s)", text)
    for block in blocks:
        m = re.match(r"(\d+)\.\s+([^\n]+)", block)
        if not m:
            continue
        name = m.group(2).strip()
        d_eff = re.search(r"D_\{eff\}=(\d+)", block) or re.search(r"D_eff[=:]\s*(\d+)", block)
        hits = re.search(r"recent_hits=(\d+)", block)
        dpsi = re.search(r"\\Delta\\psi=([\d.]+)", block) or re.search(r"delta_psi=([\d.]+)", block)
        obs = re.search(r"observed=(True|False)", block)
        s_val = re.search(r"Computed\s*\(\s*S\s*=\s*([-0-9.]+)", block)
        entries[name] = {
            "fsot20_name": name,
            "D_eff": int(d_eff.group(1)) if d_eff else None,
            "recent_hits": int(hits.group(1)) if hits else None,
            "delta_psi": float(dpsi.group(1)) if dpsi else None,
            "observed": obs.group(1) == "True" if obs else None,
            "canonical_S": float(s_val.group(1)) if s_val else None,
        }
    return entries


def build_crosswalk() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    mod, authority_path = load_fsot_compute()
    reg35 = yaml.safe_load(REGISTRY_35.read_text(encoding="utf-8"))
    drift_doc = (
        yaml.safe_load(DRIFT_RESOLUTION.read_text(encoding="utf-8"))
        if DRIFT_RESOLUTION.exists()
        else {}
    )
    drift_resolutions = drift_doc.get("resolutions") or {}
    lean_overrides = reg35.get("lean_overrides", {})
    empirical = reg35.get("empirical_sources", {})
    precision = json.loads(PRECISION_REPORT.read_text(encoding="utf-8")) if PRECISION_REPORT.exists() else {}
    prec_by_name = {d["neurolab_domain"]: d for d in precision.get("domains", [])}

    fsot20 = _parse_expansion_doc(EXPANSION_DOC)
    rows = []
    drift_count = 0
    for fsot_name, f20 in sorted(fsot20.items(), key=lambda x: x[0]):
        neuro = NAME_MAP.get(fsot_name, fsot_name.replace(" ", "_"))
        if neuro not in mod.DOMAINS:
            continue
        cfg = mod.DOMAINS[neuro]
        auth_S = float(mod.domain_scalar(neuro))
        lean = lean_overrides.get(neuro) or empirical.get(neuro, {}).get("lean_domain")
        prec = prec_by_name.get(neuro, {})
        drift = []
        if f20.get("D_eff") is not None and int(cfg.D_eff) != f20["D_eff"]:
            drift.append(f"D_eff auth={int(cfg.D_eff)} fsot20={f20['D_eff']}")
        if f20.get("recent_hits") is not None and int(cfg.hits) != f20["recent_hits"]:
            drift.append(f"hits auth={int(cfg.hits)} fsot20={f20['recent_hits']}")
        if f20.get("observed") is not None and bool(cfg.observed) != f20["observed"]:
            drift.append(f"observed auth={bool(cfg.observed)} fsot20={f20['observed']}")
        if f20.get("canonical_S") is not None and abs(auth_S - f20["canonical_S"]) > 0.05:
            drift.append(f"S auth={auth_S:.6f} fsot20={f20['canonical_S']}")
        resolution = drift_resolutions.get(neuro, {})
        drift_resolved = bool(resolution.get("canonical") == "authority" and drift)
        if drift and not drift_resolved:
            drift_count += 1
        rows.append(
            {
                "fsot20_name": fsot_name,
                "neurolab_domain": neuro,
                "lean_domain": lean,
                "authority_path": str(authority_path),
                "authority": {
                    "D_eff": int(cfg.D_eff),
                    "hits": int(cfg.hits),
                    "delta_psi": float(cfg.delta_psi),
                    "observed": bool(cfg.observed),
                    "S": auth_S,
                },
                "fsot20_canonical": f20,
                "param_drift": drift,
                "drift_resolved": drift_resolved,
                "canonical_source": resolution.get("canonical", "authority"),
                "drift_rationale": resolution.get("rationale"),
                "precision_status": prec.get("precision_status"),
                "median_error_pct": prec.get("median_error_pct"),
                "sign_mismatch": prec.get("sign_mismatch"),
            }
        )

    ext_manifest = ROOT / "data" / "extension_domains_manifest.yaml"
    extra_domains: dict = {
        "Intelligence_Compression": {
            "source": str(FSOT_20_REPO / "IntelligenceCompressor"),
            "status": "fsot20_extension_domain_36",
            "params": {"D_eff": 12, "observed": True, "delta_psi": 0.8, "recent_hits": 1},
            "maps_to_lean": ["neural", "consciousness", "ai"],
            "note": "Attention-weighted observer; not in 35-domain NeuroLab table yet",
        }
    }
    if ext_manifest.exists():
        ext_spec = yaml.safe_load(ext_manifest.read_text(encoding="utf-8"))
        for name, cfg in (ext_spec.get("extension_domains") or {}).items():
            extra_domains[name] = {
                "status": "fsot21_extension_domain",
                "params": {
                    "D_eff": cfg.get("D_eff"),
                    "observed": cfg.get("observed"),
                    "delta_psi": cfg.get("delta_psi"),
                    "recent_hits": cfg.get("recent_hits"),
                },
                "maps_to_lean": cfg.get("maps_to_lean"),
                "benchmark_data": cfg.get("benchmark_data"),
            }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fsot_20_repo": str(FSOT_20_REPO),
        "fsot_20_remote": "https://github.com/dappalumbo91/FSOT-2.0-code.git",
        "authority_path": str(authority_path),
        "domain_count_fsot20_doc": len(fsot20),
        "domain_count_matched_neurolab": len(rows),
        "param_drift_count": drift_count,
        "param_drift_resolved_count": sum(1 for r in rows if r.get("drift_resolved")),
        "drift_resolution_path": str(DRIFT_RESOLUTION) if DRIFT_RESOLUTION.exists() else None,
        "extra_domains": extra_domains,
        "domains": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT 2.0 domain crosswalk")
    parser.add_argument("--json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--yaml", type=Path, default=OUTPUT_YAML)
    args = parser.parse_args()
    doc = build_crosswalk()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    args.yaml.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    print(f"Wrote {args.json}")
    print(f"Wrote {args.yaml}")
    print(f"  matched: {doc['domain_count_matched_neurolab']}/{doc['domain_count_fsot20_doc']}")
    print(f"  param drift (unresolved): {doc['param_drift_count']}")
    print(f"  param drift resolved: {doc.get('param_drift_resolved_count', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())