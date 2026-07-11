#!/usr/bin/env python3
"""Audit FSOT engine tunable parameters vs zero-parameter headline claims."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import ScalarInput, _build_domains  # noqa: E402

OUTPUT_JSON = ROOT / "data" / "parameter_count_audit.json"
MANIFEST = ROOT / "data" / "honest_claims_manifest.yaml"
COMPUTE_PATH = ROOT / "vendor" / "fsot_compute.py"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"

# Literals in fsot_compute.py that are not derived from φ, e, π, γ closed forms.
TUNABLE_LITERAL_PATTERNS = (
    r'mpf\("0\.99"\)',
    r'mpf\("0\.01"\)',
    r'mpf\("0\.85"\)',
    r'mpf\("0\.5"\)',
    r'mpf\("0\.6"\)',
    r'mpf\("0\.7"\)',
    r"0\.01 \* g_cat",
)


def _scalar_input_field_count() -> int:
    return len(fields(ScalarInput))


def _domain_table_tunables() -> dict:
    domains = _build_domains()
    per_domain = []
    for name, cfg in sorted(domains.items()):
        per_domain.append(
            {
                "domain": name,
                "D_eff": cfg.D_eff,
                "recent_hits": cfg.hits,
                "delta_psi": str(cfg.delta_psi),
                "delta_theta": str(cfg.delta_theta),
                "C": str(cfg.C),
            }
        )
    return {
        "domain_count": len(per_domain),
        "per_domain_tunable_fields": 5,
        "total_domain_table_slots": len(per_domain) * 5,
        "domains": per_domain,
    }


def _extension_domain_tunables() -> dict:
    if yaml is None or not EXT_MANIFEST.exists():
        return {"extension_domain_count": 0, "domains": []}
    spec = yaml.safe_load(EXT_MANIFEST.read_text(encoding="utf-8"))
    rows = []
    for name, cfg in sorted((spec.get("extension_domains") or {}).items()):
        rows.append(
            {
                "domain": name,
                "D_eff": cfg.get("D_eff"),
                "delta_psi": cfg.get("delta_psi"),
                "recent_hits": cfg.get("recent_hits"),
            }
        )
    return {
        "extension_domain_count": len(rows),
        "per_extension_tunable_fields": 3,
        "total_extension_slots": len(rows) * 3,
        "domains": rows,
    }


def _literal_hits(source: str) -> list[dict]:
    hits: list[dict] = []
    for pat in TUNABLE_LITERAL_PATTERNS:
        for m in re.finditer(pat, source):
            line = source.count("\n", 0, m.start()) + 1
            hits.append({"pattern": pat, "line": line, "match": m.group(0)})
    return hits


def build_audit() -> dict:
    compute_src = COMPUTE_PATH.read_text(encoding="utf-8") if COMPUTE_PATH.exists() else ""
    domain_table = _domain_table_tunables()
    extension = _extension_domain_tunables()
    scalar_fields = _scalar_input_field_count()
    literal_hits = _literal_hits(compute_src)

    # Count distinct non-default ScalarInput slots exercised per domain row.
    empirical_tunables = (
        scalar_fields
        + domain_table["total_domain_table_slots"]
        + extension["total_extension_slots"]
        + len(literal_hits)
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline_claim": "zero free parameters",
        "audit_verdict": "NOT_ZERO — intrinsic constants + per-domain assignment table",
        "scalar_input_fields": scalar_fields,
        "scalar_input_note": "24-field ScalarInput; defaults overridden per domain/benchmark",
        "domain_table": domain_table,
        "extension_domains": extension,
        "literal_coefficient_hits": literal_hits,
        "literal_coefficient_count": len(literal_hits),
        "empirical_tunable_slot_estimate": empirical_tunables,
        "honest_framing": (
            "FSOT uses a fixed closed-form constant spine (φ, e, π, γ, …) with "
            "deterministic per-domain D_eff / δψ / hits assignments — not a fit-to-data "
            "parameter vector, but not literally zero knobs."
        ),
        "what_is_actually_zero_fit": [
            "No per-observable least-squares tuning in the verification pipeline",
            "SHA-256 gate on fsot_compute.py prevents silent engine drift",
            "Domain assignments are manifest-declared, not optimized per benchmark row",
        ],
    }


def main() -> int:
    if yaml is None:
        print("FAIL: PyYAML required", file=sys.stderr)
        return 1
    audit = build_audit()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("=== FSOT parameter count audit ===")
    print(f"  scalar_input_fields: {audit['scalar_input_fields']}")
    print(f"  domain_table_slots: {audit['domain_table']['total_domain_table_slots']}")
    print(f"  extension_slots: {audit['extension_domains']['total_extension_slots']}")
    print(f"  literal_coefficients: {audit['literal_coefficient_count']}")
    print(f"  verdict: {audit['audit_verdict']}")
    print(f"  wrote: {OUTPUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())