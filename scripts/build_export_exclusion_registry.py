#!/usr/bin/env python3
"""Document Lean theorems not exported as cross-proof obligations — honest export gap registry."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
OBLIGATIONS = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OUT = ROOT / "data" / "export_exclusion_registry.json"

THM_RE = re.compile(r"(?:theorem|lemma)\s+(\w+)\b")
EXPORT_SKIP_MARKERS = (
    "sorry",
    "admit",
    "axiom ",
    "private theorem",
    "noncomputable",
)


def _lean_theorems() -> dict[str, list[str]]:
    by_module: dict[str, list[str]] = {}
    for path in sorted(FORMAL.glob("*.lean")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        names = THM_RE.findall(text)
        if names:
            by_module[path.name] = names
    return by_module


def _exported_ids() -> set[str]:
    if not OBLIGATIONS.exists():
        return set()
    doc = json.loads(OBLIGATIONS.read_text(encoding="utf-8"))
    return {str(ob.get("id") or "") for ob in doc.get("obligations") or [] if ob.get("id")}


def _exclusion_reason(path: Path, name: str, text: str) -> str:
    if path.name.startswith("CrossProof"):
        return "cross_proof_meta_module"
    if "norm_num" not in text and path.name != "Bounds.lean":
        return "no_norm_num_certificate_in_module"
    if any(m in text for m in EXPORT_SKIP_MARKERS):
        return "contains_non_exportable_proof_markers"
    if name.endswith("_bundle") or "bundle" in name.lower():
        return "structural_bundle_theorem"
    if "Priors" not in path.name and path.name != "Bounds.lean":
        return "extended_formal_not_in_export_spine"
    return "not_matched_by_cross_proof_export_patterns"


def build() -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    by_module = _lean_theorems()
    exported = _exported_ids()
    exclusions: list[dict] = []
    reason_counts: Counter[str] = Counter()

    for module, names in by_module.items():
        path = FORMAL / module
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in names:
            if name in exported:
                continue
            reason = _exclusion_reason(path, name, text)
            reason_counts[reason] += 1
            exclusions.append(
                {
                    "theorem": name,
                    "module": module,
                    "reason": reason,
                }
            )

    total = sum(len(v) for v in by_module.values())
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "lean_theorem_count": total,
        "exported_obligation_count": len(exported),
        "unexported_theorem_count": len(exclusions),
        "export_fraction_pct": round(100.0 * len(exported) / total, 2) if total else None,
        "by_reason": dict(reason_counts),
        "exclusions": exclusions,
        "remedy": (
            "Extend export_full_formal_obligations.py for structural/bundle patterns, "
            "or keep exclusions documented here with explicit reasons."
        ),
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(
        f"  theorems: {doc['lean_theorem_count']}  exported: {doc['exported_obligation_count']}  "
        f"unexported: {doc['unexported_theorem_count']}"
    )
    print(f"  by_reason: {doc['by_reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())