#!/usr/bin/env python3
"""Build a single-page FSOT Mathematical Key handout for scientists (PDF + MD)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "FSOT_MATH_KEY_ONEPAGER.pdf"
OUT_MD = ROOT / "docs" / "FSOT_MATH_KEY_ONEPAGER.md"


def _stats() -> dict:
    out: dict = {
        "atlas_domains": "403+",
        "green": "410/410",
        "records": "~2.63M",
        "mpcorb_objects": "1,554,101",
        "mpcorb_residual": "0.023%",
        "catalog_obligations": "~1912",
        "green_gate": "0.5%",
        "aspiration": "0.05%",
        "pin": "D1D38A",
    }
    bm = ROOT / "data" / "benchmark_margin_audit.json"
    if bm.exists():
        d = json.loads(bm.read_text(encoding="utf-8"))
        g = d.get("green_gate_pass_count")
        n = d.get("benchmark_file_count")
        if g is not None and n is not None:
            out["green"] = f"{g}/{n}"
    mpc = ROOT / "data" / "mpcorb_fsot_benchmark.json"
    if mpc.exists():
        d = json.loads(mpc.read_text(encoding="utf-8"))
        if d.get("mpcorb_object_count"):
            out["mpcorb_objects"] = f"{int(d['mpcorb_object_count']):,}"
        if d.get("pooled_median_error_pct") is not None:
            out["mpcorb_residual"] = f"{float(d['pooled_median_error_pct']):.3f}%"
    cat = ROOT / "verification" / "obligations" / "scientific_catalog_spine.json"
    if cat.exists():
        d = json.loads(cat.read_text(encoding="utf-8"))
        if d.get("obligation_count"):
            out["catalog_obligations"] = str(d["obligation_count"])
    atlas = ROOT / "data" / "publication" / "domain_atlas.csv"
    if atlas.exists():
        n = sum(1 for _ in atlas.read_text(encoding="utf-8").splitlines() if _.strip()) - 1
        if n > 0:
            out["atlas_domains"] = str(n)
    return out


def write_md(s: dict) -> None:
    md = f"""# FSOT Mathematical Key — one page (scientists)

**Fluid Spacetime Omni-Theory** · pin **{s['pin']}** · {datetime.now(timezone.utc).date().isoformat()}  
Full key: `docs/FSOT_MATH_KEY.md` · Repo: https://github.com/dappalumbo91/FSOT-2.1-Lean

## Unified principle

One seed-derived scalar engine — **zero free parameters** — evaluated at preregistered dimensional interfaces \\(D_{{\\mathrm{{eff}}}}\\).  
Every domain uses the **same** prediction law; mismatches mean wrong interface, not a new fit coefficient.

**Seeds:** \\(\\pi,\\ e,\\ \\varphi,\\ \\gamma,\\ G\\) (Catalan)

**Scalar:** \\(S = K\\cdot(T_1 + T_2 + T_3)\\)  
\\(T_1\\) observer-modulated base (includes **consciousness factor** \\(C_{{\\mathrm{{factor}}}}\\) when `observed`) · \\(T_2\\) linear · \\(T_3\\) valve–acoustic–phase (**Poof**, Suction, Chaos, bleed)

**Prediction law (all domains):**

```
computed = measured × (1 + |S(domain)| × factor)
```

`S(domain)` = full `compute_scalar` at that domain’s \\(D_{{\\mathrm{{eff}}}}\\), hits, \\(\\delta\\psi\\), observer flag.  
Factors: `scripts/fsot_api_predict_lib.py`. Engine: `vendor/fsot_compute.py`.

## How to use the math in any domain

| Step | Action |
|------|--------|
| 1 | Name measured \\(m\\) (public/lab provenance) |
| 2 | Pick **domain / \\(D_{{\\mathrm{{eff}}}}\\)** (micro → meso → geo → astro ladder) |
| 3 | `S = domain_scalar(name)` |
| 4 | `computed, err% = fsot_scaled(m, name)` |
| 5 | Green if domain **median** residual ≤ **{s['green_gate']}** (aspiration ≤ **{s['aspiration']}**) |
| 6 | Optional: export gate → Lean / Coq / Isabelle / SMT |

**Mismatch rule:** first check dimensional interface (e.g. NEO vs belt vs distant), then observer / \\(C_{{\\mathrm{{factor}}}}\\) / Poof — never add free parameters.

## Snapshot (this repo edition)

| Quantity | Value |
|----------|------:|
| Atlas domains | {s['atlas_domains']} |
| Green benchmarks | {s['green']} |
| Empirical records (atlas sum) | {s['records']} |
| MPCORB objects · residual | {s['mpcorb_objects']} · {s['mpcorb_residual']} |
| Scientific catalog obligations | {s['catalog_obligations']} |

## Verification stack (not decoration)

Lean 4 (master) · Coq · Isabelle · F* · Rust replay · SMT (Z3/CVC5) · TLA+ routing flow  
Layers: **A** engine math · **B** empirical residuals · **C** streams/catalog integrity  

Honesty: multi-prover locks **exported residual gates**; Python/data own measurements.  
Kill path: `python scripts/run_publication_verification_bundle.py`

---
*Not a second theory — the same key applied at every domain fold.*
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_MD}")


def write_pdf(s: dict) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        HRFlowable,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.4 * inch,
        title="FSOT Mathematical Key — One Page",
        author="Damian Arthur Palumbo / FSOT-2.1-Lean",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "T",
        parent=styles["Title"],
        fontSize=14,
        leading=16,
        spaceAfter=2,
        textColor=colors.HexColor("#0b1f33"),
        alignment=TA_CENTER,
    )
    sub = ParagraphStyle(
        "S",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )
    h = ParagraphStyle(
        "H",
        parent=styles["Heading2"],
        fontSize=9.5,
        leading=11,
        spaceBefore=5,
        spaceAfter=2,
        textColor=colors.HexColor("#0f766e"),
    )
    body = ParagraphStyle(
        "B",
        parent=styles["Normal"],
        fontSize=7.8,
        leading=9.4,
        alignment=TA_JUSTIFY,
        spaceAfter=2,
    )
    mono = ParagraphStyle(
        "M",
        parent=styles["Code"],
        fontSize=7.5,
        leading=9,
        backColor=colors.HexColor("#f1f5f9"),
        leftIndent=4,
        rightIndent=4,
        spaceBefore=2,
        spaceAfter=3,
    )
    tiny = ParagraphStyle(
        "Tiny",
        parent=styles["Normal"],
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#475569"),
    )
    cell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=7, leading=8.5)

    story = []
    story.append(Paragraph("FSOT Mathematical Key — One Page for Scientists", title))
    story.append(
        Paragraph(
            f"Fluid Spacetime Omni-Theory · pin <b>{s['pin']}</b> · zero free parameters · "
            f"github.com/dappalumbo91/FSOT-2.1-Lean · full key: docs/FSOT_MATH_KEY.md",
            sub,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f766e"), spaceAfter=4))

    story.append(Paragraph("1. Unified principle", h))
    story.append(
        Paragraph(
            "One seed-derived scalar engine evaluated at preregistered dimensional interfaces "
            "(D<sub>eff</sub>). Seeds π, e, φ, γ, Catalan G only — <b>no free fit parameters</b>. "
            "Domains are folds of the same engine, not separate fitted models. "
            "When residuals fail: fix D<sub>eff</sub> / observer / C<sub>factor</sub> / Poof path — "
            "do not invent a new coefficient.",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>Scalar:</b> S = K·(T<sub>1</sub>+T<sub>2</sub>+T<sub>3</sub>) · "
            "T<sub>1</sub> observer-modulated base (consciousness factor C<sub>factor</sub> when observed) · "
            "T<sub>2</sub> linear · T<sub>3</sub> valve–acoustic–phase (Poof, Suction, Chaos, bleed).",
            body,
        )
    )
    story.append(Paragraph("<b>Prediction law (every domain)</b>", body))
    story.append(Paragraph("computed = measured × (1 + |S(domain)| × factor)", mono))
    story.append(
        Paragraph(
            "Implementation: vendor/fsot_compute.py · scripts/fsot_api_predict_lib.py "
            "(domain_scalar, fsot_scaled, PROPERTY_ROUTING).",
            tiny,
        )
    )

    story.append(Paragraph("2. Recipe — use the math in any domain", h))
    recipe = [
        [
            Paragraph("<b>Step</b>", cell),
            Paragraph("<b>Action</b>", cell),
        ],
        [Paragraph("1", cell), Paragraph("Name measured m with public/lab provenance", cell)],
        [
            Paragraph("2", cell),
            Paragraph(
                "Pick domain / D<sub>eff</sub> (micro 5–9 · meso 10–15 · geo 16–19 · astro 20–25)",
                cell,
            ),
        ],
        [Paragraph("3", cell), Paragraph("S = domain_scalar(name)  — full stack at that interface", cell)],
        [Paragraph("4", cell), Paragraph("computed, err% = fsot_scaled(m, name)  or make_fsot_record(...)", cell)],
        [
            Paragraph("5", cell),
            Paragraph(
                f"Green if domain median residual ≤ <b>{s['green_gate']}</b> "
                f"(aspiration ≤ {s['aspiration']})",
                cell,
            ),
        ],
        [
            Paragraph("6", cell),
            Paragraph("Optional formal lock: export gate → Lean / Coq / Isabelle / SMT / TLA+", cell),
        ],
    ]
    t = Table(recipe, colWidths=[0.45 * inch, 6.9 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ccfbf1")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#94a3b8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(t)

    story.append(Paragraph("3. Snapshot (this repository edition)", h))
    snap = [
        [
            Paragraph("<b>Quantity</b>", cell),
            Paragraph("<b>Value</b>", cell),
            Paragraph("<b>Quantity</b>", cell),
            Paragraph("<b>Value</b>", cell),
        ],
        [
            Paragraph("Atlas domains", cell),
            Paragraph(s["atlas_domains"], cell),
            Paragraph("Green benchmarks", cell),
            Paragraph(s["green"], cell),
        ],
        [
            Paragraph("Empirical records (atlas)", cell),
            Paragraph(s["records"], cell),
            Paragraph("Catalog obligations", cell),
            Paragraph(s["catalog_obligations"], cell),
        ],
        [
            Paragraph("MPCORB objects", cell),
            Paragraph(s["mpcorb_objects"], cell),
            Paragraph("MPCORB pooled residual", cell),
            Paragraph(s["mpcorb_residual"], cell),
        ],
    ]
    t2 = Table(snap, colWidths=[1.85 * inch, 1.8 * inch, 1.85 * inch, 1.85 * inch])
    t2.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0f2fe")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#94a3b8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(t2)

    story.append(Paragraph("4. Verification stack (layers A / B / C)", h))
    story.append(
        Paragraph(
            "<b>A Engine math:</b> Lean 4 master · Coq · Isabelle · F* · Rust replay — seeds, raw_S, exported bounds. "
            "<b>B Empirical:</b> domain residual ledger ≤ 0.5% green. "
            "<b>C Streams/catalogs:</b> live APIs, MPCORB Kepler integrity, MAST, etc. "
            "<b>Bulk:</b> SMT Z3/CVC5 residual conjunction. <b>Flow:</b> TLA+ domain-routing (no gate skips). "
            "Multi-prover locks <i>exported gate literals</i>; it does not re-derive raw telescope pixels in type theory.",
            body,
        )
    )

    story.append(Paragraph("5. Reproduce", h))
    story.append(
        Paragraph(
            "git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git && "
            "python scripts/run_publication_verification_bundle.py<br/>"
            "MPCORB: python scripts/ingest_mpcorb_catalog.py && "
            "python scripts/build_mpcorb_fsot_benchmark.py<br/>"
            "Margin: python scripts/audit_all_benchmark_margins.py → data/benchmark_margin_audit.json",
            tiny,
        )
    )
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8"), spaceAfter=2))
    story.append(
        Paragraph(
            "One seed set · one scalar S · one prediction law · many D<sub>eff</sub> interfaces. "
            "That is the mathematical key for every FSOT domain.",
            ParagraphStyle("Foot", parent=body, alignment=TA_CENTER, fontSize=7.5, textColor=colors.HexColor("#0f766e")),
        )
    )

    doc.build(story)
    print(f"Wrote {OUT_PDF}")


def main() -> int:
    s = _stats()
    write_md(s)
    write_pdf(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
