#!/usr/bin/env python3
"""Domain family tree: 35 core folds by D_eff + extension subdomains + between-scale gaps.

This is a coverage map for expansion, not a new theory. The engine is still
S = K(T1+T2+T3) at a preregistered (D_eff, observed). Adjacent D_eff that
have no interconnect residual are the next physical-condition holes.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import DOMAINS  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXT = ROOT / "data" / "extension_domains_manifest.yaml"
ATLAS = ROOT / "data" / "publication" / "domain_atlas.csv"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
OUT_JSON = ROOT / "data" / "domain_family_tree.json"
OUT_MD = ROOT / "docs" / "DOMAIN_FAMILY_TREE.md"

BANDS = [
    (5, 8, "micro / bond / observer-on", "Particle, QM, chemistry — form at the small orifice"),
    (9, 11, "look / compute / sound", "EM, optics, acoustics; QC stays dark on purpose"),
    (12, 16, "life / fluid / weather", "Biology through meteorology — viscosity and C_factor"),
    (17, 21, "bulk / catalogs", "Atmosphere, ocean, rock, planets, astronomy"),
    (22, 25, "deep / ceiling", "QG, particle-astro, astrophysics, cosmology at D=25"),
]

# Residual-gated interconnects that already exist (do not invent new ones here).
FILLED_INTERCONNECTS = [
    {
        "name": "Cepheid PL",
        "cores": ["Acoustics", "Chemistry", "Electromagnetism", "Astronomy"],
        "status": "filled",
        "note": "Period/metals/Wesenheit. Optical+NIR panel 0.135%. Table 2 full sample 0.141%.",
        "artifact": "docs/CEPHEID_PL_PHYSICS.md",
    },
    {
        "name": "BH→WH bubble H0",
        "cores": ["Cosmology", "Astronomy", "Astrophysics"],
        "status": "filled",
        "note": "Multi-tool sectors + ladder chain 0.252%. Class SH0ES 1% stays on 2.5% band.",
        "artifact": "docs/CONCEPTS.md C3 / SH0ES_LADDER_DIAGNOSIS.md",
    },
    {
        "name": "Genetics ChemLink",
        "cores": ["Biology", "Chemistry", "Biochemistry"],
        "status": "filled_sibling",
        "note": "Product 0.13 Å vs AF 0.47 Å. 3-D MDS retired. Sibling owns remaining folds.",
        "artifact": "docs/GENETICS_CLAIM_EVIDENCE.md",
    },
    {
        "name": "MPCORB planetary catalog",
        "cores": ["Planetary_Science", "Astronomy"],
        "status": "filled",
        "note": "Wrong fold ~62% → Planetary_Science D=21 ~0.023%.",
        "artifact": "docs/MPCORB_REFINEMENT_PROCESS.md",
    },
    {
        "name": "Observer / C_factor",
        "cores": ["Neuroscience", "Quantum_Mechanics", "Optics"],
        "status": "filled",
        "note": "Live Homo sapiens 20.003601 vs 20.0 W (0.018%). QC stays dark.",
        "artifact": "docs/CONSCIOUSNESS_CLAIM_EVIDENCE.md",
    },
    {
        "name": "Matter–antimatter conjugate",
        "cores": ["Particle_Physics", "High_Energy_Physics", "Quantum_Mechanics"],
        "status": "filled",
        "note": "C13 reverse/conjugate. η 0.004%.",
        "artifact": "docs/MATTER_ANTIMATTER_CLAIM_EVIDENCE.md",
    },
    {
        "name": "Seed cross-ratios (engine §25)",
        "cores": ["Optics", "Quantum_Optics", "Materials_Science", "Condensed_Matter", "Astronomy", "Planetary_Science"],
        "status": "engine",
        "note": "S_i/S_j identities in fsot_compute.predictions(). Not a residual panel.",
        "artifact": "vendor/fsot_compute.py §25",
    },
    {
        "name": "Between-scale interconnects (wave/fluid/fridge/orifice/ceiling/social/seis-geo)",
        "cores": [
            "Acoustics",
            "Seismology",
            "Fluid_Dynamics",
            "Oceanography",
            "Atmospheric_Physics",
            "Thermodynamics",
            "Cosmology",
            "Nuclear_Physics",
            "Particle_Physics",
            "Quantum_Gravity",
            "Geophysics",
            "Materials_Science",
            "Optics",
        ],
        "status": "filled",
        "note": "PREM+NDBC+ENDF+Carnot+QG+social+seis-geo. Pooled ~0.03% GREEN.",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md",
    },
]

# Physical-condition holes: adjacent or functionally coupled scales with no interconnect panel.
SCALE_GAPS = [
    {
        "name": "Developmental mechanics (sibling-owned)",
        "cores": ["Biology", "Fluid_Dynamics", "Neuroscience"],
        "why": "Zebrafish 0.358% is inside 0.5%. Genetics product freeze 2026-08-17 is quoted in the hub.",
        "fill_looks_like": "Do not densify zebrafish here. CASP/CAMEO blind is OPEN (docs/CASP_CAMEO_BLIND_PROTOCOL.md).",
    },
]


def _load_extensions() -> dict:
    if yaml is None or not EXT.is_file():
        return {}
    doc = yaml.safe_load(EXT.read_text(encoding="utf-8")) or {}
    return doc.get("extension_domains") or {}


def _load_atlas() -> list[dict]:
    if not ATLAS.is_file():
        return []
    with ATLAS.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _load_margin() -> dict[str, dict]:
    if not MARGIN.is_file():
        return {}
    doc = json.loads(MARGIN.read_text(encoding="utf-8"))
    out = {}
    for row in doc.get("all_domains") or []:
        name = str(row.get("domain") or row.get("file") or "")
        out[name] = row
    return out


def _band_for(d_eff: int) -> str:
    for lo, hi, title, _ in BANDS:
        if lo <= d_eff <= hi:
            return f"D={lo}–{hi} {title}"
    return "unbanded"


def main() -> int:
    ext = _load_extensions()
    atlas = _load_atlas()
    margin = _load_margin()
    cores = []
    for name, cfg in DOMAINS.items():
        cores.append(
            {
                "name": name,
                "D_eff": int(cfg.D_eff),
                "observed": bool(cfg.observed),
                "hits": int(cfg.hits),
                "band": _band_for(int(cfg.D_eff)),
            }
        )
    cores.sort(key=lambda r: (r["D_eff"], r["name"]))

    children: dict[str, list[dict]] = defaultdict(list)
    ext_rows = []
    for name, spec in ext.items():
        d_eff = int(spec.get("D_eff") or 0)
        maps = [str(x) for x in (spec.get("maps_to_lean") or [])]
        row = {
            "name": name,
            "D_eff": d_eff,
            "maps_to_lean": maps,
            "benchmark": spec.get("benchmark_data") or spec.get("benchmark_script"),
            "note": spec.get("note") or "",
            "band": _band_for(d_eff) if d_eff else "unbanded",
        }
        m = margin.get(name)
        if m:
            row["pooled_median_error_pct"] = m.get("pooled_median_error_pct")
            row["records"] = m.get("records")
        ext_rows.append(row)
        # attach to nearest core by D_eff
        nearest = min(cores, key=lambda c: abs(c["D_eff"] - d_eff) if d_eff else 99)
        children[nearest["name"]].append(row)

    atlas_by_kind = defaultdict(int)
    for a in atlas:
        atlas_by_kind[a.get("kind") or ""] += 1

    tree = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "claim": (
            "One 25-D fluid. Core folds are D_eff slices. Extensions are subdomains "
            "of a slice, not other ontologies. Gaps are missing interconnects between slices."
        ),
        "core_count": len(cores),
        "extension_count": len(ext_rows),
        "atlas_rows": len(atlas),
        "atlas_by_kind": dict(atlas_by_kind),
        "bands": [
            {"lo": lo, "hi": hi, "title": title, "said": said, "cores": [c["name"] for c in cores if lo <= c["D_eff"] <= hi]}
            for lo, hi, title, said in BANDS
        ],
        "cores": cores,
        "extensions": ext_rows,
        "children_by_core": {k: v for k, v in children.items()},
        "filled_interconnects": FILLED_INTERCONNECTS,
        "scale_gaps": SCALE_GAPS,
    }
    OUT_JSON.write_text(json.dumps(tree, indent=2), encoding="utf-8")

    lines = [
        "# Domain family tree — folds, subdomains, between-scale gaps",
        "",
        f"**Generated:** `{tree['generated_at']}` · pin **D1D38A**  ",
        "**Regenerate:** `python scripts/build_domain_family_tree.py`",
        "",
        "This is a **directory of slices**, not 400 theories. Reality is one 25-D fluid",
        "([`CONCEPTS.md`](CONCEPTS.md) C8). A domain is a `(D_eff, observed)` interface.",
        "An extension is a subdomain of a slice. A gap is a **missing interconnect**",
        "between slices (`κ_ij`), not a missing spring constant.",
        "",
        f"Core folds **{len(cores)}** · extension subdomains **{len(ext_rows)}** · atlas named rows **{len(atlas)}**.",
        "Green-file count stays in [`CURRENT_STATUS.md`](CURRENT_STATUS.md) (do not mix ledgers:",
        "[`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md)).",
        "",
        "## How to read this",
        "",
        "| You want… | Look at |",
        "|-----------|---------|",
        "| The engine | `vendor/fsot_compute.py` `DOMAINS` |",
        "| Picture | [`CONCEPTS.md`](CONCEPTS.md) C1–C13 · [`FOUNDING_ARCHIVE_VIEW.md`](FOUNDING_ARCHIVE_VIEW.md) |",
        "| Apply without LSQ | [`APPLY.md`](APPLY.md) |",
        "| Hubble is not one number | C3 — structure + bubble, not a 60° RA silo |",
        "",
        "## The tree (core folds by compactification depth)",
        "",
        "Extension columns attach by **nearest \(D_{\\mathrm{eff}}\)**, not by Lean name.",
        "Machine map: `data/domain_family_tree.json`.",
        "",
    ]
    for lo, hi, title, said in BANDS:
        band_cores = [c for c in cores if lo <= c["D_eff"] <= hi]
        lines.append(f"### D = {lo}–{hi} — {title}")
        lines.append("")
        lines.append(said + ".")
        lines.append("")
        lines.append("| Core fold | D_eff | observed | Extension subdomains (nearest D) |")
        lines.append("|-----------|------:|:--------:|----------------------------------|")
        for c in band_cores:
            kids = children.get(c["name"]) or []
            kid_s = ", ".join(k["name"] for k in kids[:12])
            if len(kids) > 12:
                kid_s += f" … +{len(kids) - 12}"
            if not kid_s:
                kid_s = "—"
            obs = "yes" if c["observed"] else "dark"
            lines.append(f"| **{c['name']}** | {c['D_eff']} | {obs} | {kid_s} |")
        lines.append("")

    lines += [
        "## Interconnects already gated (do not re-litigate)",
        "",
        "| Interconnect | Cores | Status | Where |",
        "|--------------|-------|--------|-------|",
    ]
    for ic in FILLED_INTERCONNECTS:
        lines.append(
            f"| {ic['name']} | {', '.join(ic['cores'])} | {ic['status']} | {ic['artifact']} |"
        )
    lines += [
        "",
        "## Between-scale gaps (physical conditions still siloed)",
        "",
        "These are the next expansion targets. Fill with **measured public tables** and",
        "the mismatch rule (wrong `D_eff` first). Forbidden: extra coefficient, stuffing",
        "SH0ES class 1% into 0.5%, inventing unpublished tech numerics.",
        "",
        "| Gap | Cores | Why it is one fluid | What “filled” looks like |",
        "|-----|-------|---------------------|--------------------------|",
    ]
    for g in SCALE_GAPS:
        lines.append(
            f"| **{g['name']}** | {', '.join(g['cores'])} | {g['why']} | {g['fill_looks_like']} |"
        )
    lines += [
        "",
        "## Largest empirical pooled residuals (still green)",
        "",
        "Process/certificate C_thin spines (TOE ledgers, rust-lean bridge) are not these.",
        "Push **measured** panels with APPLY. Zebrafish 0.358% was the worst; D_eff metadata",
        "is now 12 (biology), matching the connective engine — not astrophysics 24.",
        "",
        "| Domain | Records | Pooled % |",
        "|--------|--------:|---------:|",
    ]
    ranked = sorted(
        (r for r in margin.values() if r.get("records") and r.get("pooled_median_error_pct")),
        key=lambda r: -float(r.get("pooled_median_error_pct") or 0),
    )
    for r in ranked[:12]:
        if (r.get("records") or 0) < 20 and float(r.get("pooled_median_error_pct") or 0) == 0:
            continue
        lines.append(
            f"| {r.get('domain') or r.get('file')} | {r.get('records')} | "
            f"{float(r.get('pooled_median_error_pct') or 0):.4f} |"
        )
    lines += [
        "",
        "Kill: treating the family tree as a request for more free parameters.",
        "More domains strengthen Label A only. Label B T1–T6 is frozen.",
        "",
        "Related: [`HOLE_AUDIT.md`](HOLE_AUDIT.md) · [`SYSTEM_DIRECTORY.md`](SYSTEM_DIRECTORY.md) ·",
        "[`APPLY.md`](APPLY.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    print(f"  cores={len(cores)} extensions={len(ext_rows)} gaps={len(SCALE_GAPS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
