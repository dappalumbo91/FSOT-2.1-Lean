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
    load_scalar_constants,
    make_unique_coq_ids,
    parse_formal_module,
)

OUT = ROOT / "verification" / "obligations" / "full_formal_spine.json"
PRIORS_OUT = ROOT / "verification" / "obligations" / "full_priors_spine.json"


def _export_sources() -> tuple[list[dict], dict]:
    scalar_r = load_scalar_constants()
    all_ob: list[dict] = []
    modules_hit = 0
    by_tier: Counter[str] = Counter()
    by_kind: Counter[str] = Counter()

    priors_paths = sorted(
        p for p in FORMAL.glob("*Priors.lean") if not p.stem.startswith("CrossProof")
    )
    other_paths = [
        FORMAL / "Bounds.lean",
        FORMAL / "CrossProofConnectivePriors.lean",
        FORMAL / "DomainCoveragePriors.lean",
        FORMAL / "NeuronCohortStrataPriors.lean",
        FORMAL / "DomainPrecisionPriors.lean",
        FORMAL / "BrainPriors.lean",
        FORMAL / "CodonPriors.lean",
        FORMAL / "ProteinPriors.lean",
        FORMAL / "TrinaryOSPriors.lean",
        FORMAL / "SotaCompetitivenessPriors.lean",
    ]

    seen_paths: set[Path] = set()
    ordered_paths: list[tuple[Path, str, bool]] = []
    for p in priors_paths:
        ordered_paths.append((p, "priors", True))
    for p in other_paths:
        if p.exists() and p not in seen_paths:
            tier = "bounds" if p.name == "Bounds.lean" else "extended"
            ordered_paths.append((p, tier, p.name != "Bounds.lean"))

    for path, tier, require_norm_num in ordered_paths:
        seen_paths.add(path)
        obs = parse_formal_module(
            path,
            require_norm_num=require_norm_num,
            global_r=scalar_r,
            source_tier=tier,
        )
        if obs:
            modules_hit += 1
            all_ob.extend(obs)
            by_tier[tier] += len(obs)

    all_ob = make_unique_coq_ids(all_ob)
    for ob in all_ob:
        by_kind[ob["kind"]] += 1

    meta = {
        "modules_hit": modules_hit,
        "by_tier": dict(by_tier),
        "by_kind": dict(by_kind),
    }
    return all_ob, meta


def main() -> int:
    obligations, meta = _export_sources()
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