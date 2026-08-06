#!/usr/bin/env python3
"""Classify predictions/ into public tiers (A–D) for honest communication.

Tier A — Contested / public-survey: highest falsifiability against literature drops
Tier B — Empirical atlas: residual + scalar holds (regression strength)
Tier C — Grounded engineering / lab panels (seed-locked but not survey cosmology)
Tier D — Scaffold / high-speculation: exploratory PREDs; not marketed as survey kills

Outputs:
  predictions/prediction_tiers.json
  predictions/reports/PREDICTION_TIERS.md
  predictions/public/TIERS_FOR_X.md
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT / "predictions"
PREREG = PRED / "preregistered_predictions_manifest.yaml"
ATLAS = PRED / "domain_prediction_atlas.json"
H0_MULTI = PRED / "h0_multi_tool_predictions.json"
OUT_JSON = PRED / "prediction_tiers.json"
OUT_MD = PRED / "reports" / "PREDICTION_TIERS.md"
OUT_X = PRED / "public" / "TIERS_FOR_X.md"

# Hand PRED ids that confront public surveys / standard literature
TIER_A_HAND = {
    "PRED-001",  # H0 bridge
    "PRED-002",  # S8
    "PRED-004",  # muon g-2 direction
    "PRED-005",  # lithium
    "PRED-024",  # dual anchor bubble
    "PRED-042",  # Euclid S8
    "PRED-043",  # wa
    "PRED-044",  # Rubin S8
    "PRED-046",  # DESI H0
    "PRED-047",  # N_eff
    "PRED-048",  # LVK panel
    "PRED-049",  # mH
    "PRED-050",  # muon g-2 hold
    "PRED-051",  # JWST H0 bridge
    "PRED-052",  # FRB DM
    "PRED-053",  # JWST high-z hold
}

# Grounded lab / engineering (not scaffold fiction)
TIER_C_HAND = {
    "PRED-003",  # code genome
    "PRED-006",  # acoustic materials
    "PRED-007",  # ionosphere
    "PRED-008",  # phi morphogen
    "PRED-025",  # FPC tau
    "PRED-034",  # fuel lab
    "PRED-035",  # machine molecule
    "PRED-037",  # BH/WH cycle live panel
    "PRED-054",  # climate NCEI
    "PRED-055",  # zebrafish
}

# Everything else hand-curated with Scaffold in domain name → D
SCAFFOLD_MARKERS = (
    "scaffold",
    "transporter",
    "warp_bh_wh_portal",
    "cold_fusion",
    "undiscovered_element",
    "distant_island",
    "fusion_decay",
    "metamaterial_fluid_design",
    "periodic_extension",
    "z120",
    "z126",
    "z164",
    "heavy_ion_lab",
    "natural_formation_element",
)

TIER_DEFS = {
    "A": {
        "name": "Contested / public survey",
        "audience": "X, skeptics, survey confrontations",
        "meaning": (
            "Falsifiable against independent literature and named data drops "
            "(Euclid, DESI, SH0ES, PDG, LVK, …). Highest epistemic weight."
        ),
        "include_in_public_headline": True,
    },
    "B": {
        "name": "Empirical atlas (regression)",
        "audience": "engine health, multi-domain claim",
        "meaning": (
            "Residual-hold and scalar-lock surface across green domains. "
            "Shows same seeds stay ≤0.5% — useful, but less distinctive per item "
            "than Tier A survey locks."
        ),
        "include_in_public_headline": False,
    },
    "C": {
        "name": "Grounded engineering / lab",
        "audience": "applications, open lab panels",
        "meaning": (
            "Seed-locked panels with real thermochemistry / materials / climate / "
            "code-genome style anchors. Not high-energy survey cosmology, not fiction scaffold."
        ),
        "include_in_public_headline": True,
    },
    "D": {
        "name": "Scaffold / high-speculation",
        "audience": "research roadmap only — do not lead X with these",
        "meaning": (
            "Exploratory PREDs (cold-fusion scaffolds, superheavy islands, transporter "
            "stack, warp portal scalars). Registered for completeness and future lab "
            "design — NOT equivalent to Tier A survey kills. Must be labeled when shared."
        ),
        "include_in_public_headline": False,
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_yaml(path: Path) -> dict:
    import yaml

    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _hand_tier(pid: str, domain: str, name: str) -> str:
    if pid in TIER_A_HAND:
        return "A"
    if pid in TIER_C_HAND:
        return "C"
    blob = f"{domain} {name}".lower()
    if any(m in blob for m in SCAFFOLD_MARKERS):
        return "D"
    if pid in TIER_A_HAND:
        return "A"
    # default remaining hand items to C if empirical-sounding else D
    if any(x in blob for x in ("panel", "benchmark", "lab", "live")):
        return "C"
    return "D"


def _atlas_tier(kind: str) -> str:
    if kind in {
        "multi_tool_h0",
        "h0_sightline_host",
        "h0_sightline_sector",
        "h0_trgb_host",
        "h0_trgb_sector",
    }:
        return "A"
    if kind in {"residual_hold", "scalar_lock", "sector_portfolio_hold"}:
        return "B"
    return "B"


def build() -> dict:
    prereg = _load_yaml(PREREG)
    atlas = _load_json(ATLAS)
    h0 = _load_json(H0_MULTI)

    by_tier: dict[str, list] = defaultdict(list)

    for p in prereg.get("predictions") or []:
        pid = str(p.get("id") or "")
        domain = str(p.get("domain") or "")
        name = str(p.get("name") or "")
        tier = _hand_tier(pid, domain, name)
        by_tier[tier].append(
            {
                "id": pid,
                "source": "hand_prereg",
                "name": name,
                "domain": domain,
                "fsot_predicted": p.get("fsot_predicted"),
                "unit": p.get("unit"),
                "discriminant": p.get("discriminant"),
                "future_survey": p.get("future_survey"),
                "tier": tier,
            }
        )

    # H0 multi-tool always Tier A (even if also in atlas)
    for t in h0.get("tools") or []:
        by_tier["A"].append(
            {
                "id": t.get("pred_id") or t.get("id"),
                "source": "h0_multi_tool",
                "name": t.get("name"),
                "domain": "Hubble_Multi_Tool_Bubble_Bleed",
                "fsot_predicted": t.get("fsot_predicted_h0"),
                "unit": "km/s/Mpc",
                "tier": "A",
                "tool_class": t.get("tool_class"),
            }
        )

    atlas_counts = defaultdict(int)
    for p in atlas.get("predictions") or []:
        kind = str(p.get("kind") or "")
        tier = _atlas_tier(kind)
        atlas_counts[(tier, kind)] += 1
        # only enumerate headline subsets for A; B is counted not fully listed
        if tier == "A":
            by_tier["A"].append(
                {
                    "id": p.get("id"),
                    "source": "atlas",
                    "kind": kind,
                    "name": p.get("name"),
                    "domain": p.get("domain"),
                    "fsot_predicted": p.get("fsot_predicted"),
                    "unit": p.get("unit"),
                    "tier": "A",
                }
            )

    summary = {
        "hand_by_tier": {
            t: sum(1 for x in by_tier[t] if x.get("source") == "hand_prereg")
            for t in "ABCD"
        },
        "atlas_kind_counts": {f"{t}/{k}": n for (t, k), n in sorted(atlas_counts.items())},
        "tier_A_list_count": len(by_tier["A"]),
        "tier_B_note": (
            "Tier B is the full residual_hold + scalar_lock + sector_portfolio "
            "surface in domain_prediction_atlas.json — not fully expanded here."
        ),
        "atlas_summary": atlas.get("summary") or {},
    }

    # Deduplicate Tier A by id (hand + multi-tool + atlas overlap)
    seen = set()
    tier_a_unique = []
    for item in by_tier["A"]:
        iid = str(item.get("id") or "")
        if iid in seen:
            continue
        seen.add(iid)
        tier_a_unique.append(item)
    by_tier["A"] = tier_a_unique

    headline = [
        x
        for x in by_tier["A"]
        if x.get("source") == "hand_prereg"
        or (x.get("source") == "h0_multi_tool")
    ]

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "authority_pin_prefix": "D1D38A",
        "purpose": (
            "Separate high-weight contested survey predictions from atlas regression "
            "holds and scaffold/speculation so public communication stays honest."
        ),
        "tier_definitions": TIER_DEFS,
        "summary": summary,
        "headline_tier_A": headline,
        "tiers": {
            "A": by_tier["A"],
            "C": [x for x in by_tier["C"] if x.get("source") == "hand_prereg"],
            "D": [x for x in by_tier["D"] if x.get("source") == "hand_prereg"],
            "B": {
                "description": TIER_DEFS["B"]["meaning"],
                "atlas_path": "predictions/domain_prediction_atlas.json",
                "counts": summary["atlas_summary"].get("by_kind")
                or summary.get("atlas_kind_counts"),
            },
        },
        "public_communication_rule": (
            "Lead with Tier A. Support with Tier B breadth and Tier C labs. "
            "Never lead X posts with Tier D without explicit 'scaffold/exploratory' label."
        ),
    }
    return doc


def write_md(doc: dict) -> None:
    lines = [
        "# Prediction tiers (A–D)",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A*",
        "",
        str(doc.get("purpose") or ""),
        "",
        f"**Public rule:** {doc.get('public_communication_rule')}",
        "",
        "## Tier definitions",
        "",
        "| Tier | Name | Lead on X? | Meaning |",
        "|------|------|:----------:|---------|",
    ]
    for tid, tdef in (doc.get("tier_definitions") or {}).items():
        lead = "Yes" if tdef.get("include_in_public_headline") else "No*"
        if tid == "C":
            lead = "Support"
        lines.append(
            f"| **{tid}** | {tdef['name']} | {lead} | {tdef['meaning'][:120]}… |"
        )
    lines.append("")
    lines.append("\\*Tier B: cite as *breadth* (472 domains green), not as individual survey kills.")
    lines.append("")

    s = doc.get("summary") or {}
    lines.extend(
        [
            "## Counts",
            "",
            f"| Hand PREDs by tier | Count |",
            f"|--------------------|------:|",
        ]
    )
    for t, n in (s.get("hand_by_tier") or {}).items():
        lines.append(f"| {t} | {n} |")

    lines.extend(
        [
            "",
            f"| Tier A enumerated IDs (unique) | {s.get('tier_A_list_count')} |",
            "",
            "## Tier A — contested / public survey (headline)",
            "",
            "| ID | Source | Name / tool | FSOT | Unit |",
            "|----|--------|-------------|-----:|------|",
        ]
    )
    for x in doc.get("headline_tier_A") or []:
        lines.append(
            f"| `{x.get('id')}` | {x.get('source')} | {x.get('name')} | "
            f"{x.get('fsot_predicted')} | {x.get('unit') or ''} |"
        )

    lines.extend(
        [
            "",
            "### Full multi-tool + host H₀",
            "",
            "See `reports/H0_MULTI_TOOL_PREDICTIONS.md`, `H0_SIGHTLINE_PREDICTIONS.md`, "
            "`CCHP_TRGB_SIGHTLINE_PREDICTIONS.md` (all **Tier A**).",
            "",
            "## Tier C — grounded engineering / lab (hand)",
            "",
            "| ID | Domain | Name |",
            "|----|--------|------|",
        ]
    )
    for x in (doc.get("tiers") or {}).get("C") or []:
        lines.append(f"| `{x.get('id')}` | {x.get('domain')} | {x.get('name')} |")

    lines.extend(
        [
            "",
            "## Tier D — scaffold / high-speculation (hand)",
            "",
            "**Do not lead public claims with these.** Label as exploratory / design scaffold.",
            "",
            "| ID | Domain | Name |",
            "|----|--------|------|",
        ]
    )
    for x in (doc.get("tiers") or {}).get("D") or []:
        lines.append(f"| `{x.get('id')}` | {x.get('domain')} | {x.get('name')} |")

    lines.extend(
        [
            "",
            "## Tier B — empirical atlas",
            "",
            str(((doc.get("tiers") or {}).get("B") or {}).get("description") or ""),
            "",
            f"Full surface: `{(doc.get('tiers') or {}).get('B', {}).get('atlas_path')}`",
            "",
            "Refresh: `python scripts/build_prediction_tiers.py`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_x(doc: dict) -> None:
    hand = (doc.get("summary") or {}).get("hand_by_tier") or {}
    lines = [
        "# Prediction tiers — short copy for X",
        "",
        "## How to talk about the list (honest)",
        "",
        "FSOT predictions come in **four tiers**. Mixing them confuses people.",
        "",
        f"**Tier A** — Contested / public survey (lead with this): H₀ multi-tool + bridge, S₈, wₐ, N_eff, m_H, FRB, LVK, Euclid/Rubin/DESI locks. Hand PREDs in A: **{hand.get('A', 0)}** + 25 instruments + host/TRGB sightlines.",
        "",
        f"**Tier B** — Empirical atlas (~1400 residual + scalar locks): proves same seeds stay green across 472 domains. Cite as *breadth*, not as 1400 separate cosmology kills.",
        "",
        f"**Tier C** — Grounded lab/engineering (hand **{hand.get('C', 0)}**): fuel, materials, climate, code-genome, zebrafish holds.",
        "",
        f"**Tier D** — Scaffold / high-speculation (hand **{hand.get('D', 0)}**): cold-fusion scaffolds, superheavy Z islands, transporter stack, warp portal scalars. **Registered for the roadmap — not survey kills. Label if you mention them.**",
        "",
        "## One post",
        "",
        "My prediction list is tiered on purpose:",
        "",
        "A = public survey kills (H₀ sectors, S₈, wₐ, Euclid…)",
        "B = multi-domain green holds (same seeds, ≤0.5%)",
        "C = lab/engineering panels",
        "D = exploratory scaffolds (labeled, not leading claims)",
        "",
        "Git timestamps. Zero free parameters. No silent retune.",
        "",
        "github.com/dappalumbo91/FSOT-2.1-Lean → predictions/",
        "",
        "Full table: predictions/reports/PREDICTION_TIERS.md",
        "",
    ]
    OUT_X.parent.mkdir(parents=True, exist_ok=True)
    OUT_X.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    write_x(doc)
    s = doc["summary"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_X}")
    print(f"  hand_by_tier={s.get('hand_by_tier')} tier_A_unique={s.get('tier_A_list_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
