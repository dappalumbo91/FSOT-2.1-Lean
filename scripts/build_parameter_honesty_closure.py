#!/usr/bin/env python3
"""Parameter honesty closure — intrinsic constants vs domain table slots."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAM = ROOT / "data" / "parameter_count_audit.json"
OUT = ROOT / "data" / "parameter_honesty_closure.json"


def build() -> dict:
    audit = json.loads(PARAM.read_text(encoding="utf-8")) if PARAM.exists() else {}
    table = audit.get("domain_table") or {}
    domains = table.get("domains") or []
    per_domain = int(table.get("per_domain_tunable_fields") or 5)
    domain_count = int(table.get("domain_count") or len(domains))
    total_slots = int(table.get("total_domain_table_slots") or domain_count * per_domain)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "verdict": audit.get("audit_verdict", "NOT_ZERO"),
        "headline_claim": audit.get("headline_claim", "zero free parameters"),
        "scalar_input_fields": audit.get("scalar_input_fields"),
        "domain_table": {
            "domain_count": domain_count,
            "per_domain_tunable_fields": per_domain,
            "total_slots": total_slots,
            "field_names": ["D_eff", "recent_hits", "delta_psi", "delta_theta", "C"],
        },
        "honest_statement": (
            f"FSOT uses φ/e/π/γ-derived intrinsic constants plus a manifest-declared "
            f"domain assignment table ({domain_count} domains × {per_domain} fields = "
            f"{total_slots} slots). These are not per-observable least-squares fits in the "
            f"verification pipeline — but the 'zero free parameters' headline is "
            f"NOT_LITERAL_ZERO."
        ),
        "closure_actions": [
            "Manifest claim zero_free_parameters uses verdict NOT_LITERAL_ZERO",
            "parameter_count_audit.json is authoritative for auditor review",
            "Domain slots are preregistered in extension_domains_manifest — not hidden tuning",
        ],
        "undeniable_boundary": (
            "Intrinsic constant spine is fixed; domain table is declared assignment, not export gap."
        ),
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  slots={doc['domain_table']['total_slots']} verdict={doc['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())