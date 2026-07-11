#!/usr/bin/env python3
"""Export cross-proof obligations from the full FSOT/Formal corpus."""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    FORMAL,
    load_formal_extended_globals,
    make_unique_coq_ids,
    obligation_margin_violation,
    obligation_provable,
    parse_formal_module,
)

EXTENDED_FORMAL_MODULES = (
    "Theorems.lean",
    "Bounds.lean",
    "Domains.lean",
    "Cosmology.lean",
    "Genomic.lean",
    "Lab.lean",
    "ProteinFormulas.lean",
    "LeanProofsBridge.lean",
    "CosmologyLab.lean",
    "PhotonicForge.lean",
    "CosmologyWave4.lean",
    "CrossProofConnectivePriors.lean",
    "DomainCoveragePriors.lean",
    "NeuronCohortStrataPriors.lean",
    "DomainPrecisionPriors.lean",
    "TrinaryOSPriors.lean",
    "SotaCompetitivenessPriors.lean",
)
from fsot_label_registry_lib import annotate_obligation  # noqa: E402
from undeniable_gap_lib import enrich_obligation_labels  # noqa: E402

OUT = ROOT / "verification" / "obligations" / "full_formal_spine.json"
PRIORS_OUT = ROOT / "verification" / "obligations" / "full_priors_spine.json"


def _export_sources() -> tuple[list[dict], dict]:
    global_r, global_n, global_z = load_formal_extended_globals()
    all_ob: list[dict] = []
    modules_hit = 0
    by_tier: Counter[str] = Counter()
    by_kind: Counter[str] = Counter()

    priors_paths = sorted(
        p for p in FORMAL.glob("*Priors.lean") if not p.stem.startswith("CrossProof")
    )
    other_paths = [FORMAL / name for name in EXTENDED_FORMAL_MODULES]

    seen_paths: set[Path] = set()
    ordered_paths: list[tuple[Path, str, bool]] = []
    for p in priors_paths:
        if p in seen_paths:
            continue
        seen_paths.add(p)
        ordered_paths.append((p, "priors", True))
    for p in other_paths:
        if not p.exists() or p in seen_paths:
            continue
        seen_paths.add(p)
        tier = "bounds" if p.name == "Bounds.lean" else "extended"
        ordered_paths.append((p, tier, p.name != "Bounds.lean"))

    for path, tier, require_norm_num in ordered_paths:
        obs = parse_formal_module(
            path,
            require_norm_num=require_norm_num,
            global_r=global_r,
            global_n=global_n,
            global_z=global_z,
            source_tier=tier,
        )
        if obs:
            modules_hit += 1
            all_ob.extend(obs)
            by_tier[tier] += len(obs)

    all_ob = make_unique_coq_ids(all_ob)
    for ob in all_ob:
        by_kind[ob["kind"]] += 1
        if ob.get("kind") == "bundle_conj":
            ob["provable"] = obligation_provable(ob)
            if not ob["provable"]:
                ob["unprovable_reason"] = "structural_bundle_excluded"
                ob["exclusion_class"] = "structural_bundle"
        else:
            violation = obligation_margin_violation(ob)
            if violation:
                ob["margin_violation"] = violation
                ob["provable"] = False
                ob["unprovable_reason"] = "margin_violation"
                ob["exclusion_class"] = "margin_violation"
            else:
                ob["provable"] = obligation_provable(ob)

    meta = {
        "modules_hit": modules_hit,
        "by_tier": dict(by_tier),
        "by_kind": dict(by_kind),
    }
    return all_ob, meta


def main() -> int:
    obligations, meta = _export_sources()
    obligations = [enrich_obligation_labels(annotate_obligation(ob)) for ob in obligations]
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "2.0",
        "tier": "80_full_formal_spine",
        "obligation_count": len(obligations),
        "modules_exported": meta["modules_hit"],
        "by_tier": meta["by_tier"],
        "by_kind": meta["by_kind"],
        "obligations": obligations,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    priors_only = [ob for ob in obligations if ob.get("source_tier") == "priors"]
    priors_doc = {
        "generated_at": doc["generated_at"],
        "version": "1.1",
        "tier": "79b_full_priors_spine",
        "obligation_count": len(priors_only),
        "modules_exported": len({ob["lean_module"] for ob in priors_only}),
        "obligations": priors_only,
    }
    PRIORS_OUT.write_text(json.dumps(priors_doc, indent=2), encoding="utf-8")

    print(f"Wrote {OUT} ({len(obligations)} obligations from {meta['modules_hit']} modules)")
    print(f"  by_tier: {meta['by_tier']}")
    print(f"  by_kind: {meta['by_kind']}")
    print(f"Wrote {PRIORS_OUT} ({len(priors_only)} priors obligations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())