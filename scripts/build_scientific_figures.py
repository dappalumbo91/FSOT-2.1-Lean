#!/usr/bin/env python3
"""Publication-style figures from FSOT benchmark audits (domain envelope + calibration)."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MARGIN_AUDIT = ROOT / "data" / "benchmark_margin_audit.json"
PUSHBACK_AUDIT = ROOT / "data" / "scientific_pushback_audit.json"
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
FIG_DIR = ROOT / "data" / "figures"


def _load_manifest_tiers() -> dict[str, int]:
    try:
        import yaml
    except ImportError:
        return {}
    if not MANIFEST.exists():
        return {}
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    out: dict[str, int] = {}
    for name, cfg in (spec.get("extension_domains") or {}).items():
        rel = str((cfg or {}).get("benchmark_data") or "")
        if rel:
            out[Path(rel).name] = int((cfg or {}).get("tier") or 0)
        out[name] = int((cfg or {}).get("tier") or 0)
    return out


def _load_margin_rows() -> list[dict]:
    if not MARGIN_AUDIT.exists():
        raise FileNotFoundError(f"Run audit_all_benchmark_margins.py first: {MARGIN_AUDIT}")
    doc = json.loads(MARGIN_AUDIT.read_text(encoding="utf-8"))
    rows = doc.get("all_domains") or doc.get("rows") or []
    return [r for r in rows if not r.get("excluded")]


def figure_domain_error_envelope(out: Path) -> None:
    import matplotlib.pyplot as plt

    rows = _load_margin_rows()
    medians = [
        float(r.get("scalar_pooled_median_error_pct") or r.get("pooled_median_error_pct") or 0)
        for r in rows
        if (r.get("scalar_count") or 0) > 0
    ]
    medians = [m for m in medians if m >= 0]
    if not medians:
        raise RuntimeError("No scalar medians in benchmark_margin_audit.json")

    fig, ax = plt.subplots(figsize=(10, 5), facecolor="white")
    ax.hist(medians, bins=40, color="#2563eb", edgecolor="#1e3a8a", alpha=0.85)
    ax.axvline(0.05, color="#16a34a", linestyle="--", linewidth=1.5, label="tier_scalar 0.05%")
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.5, label="green_gate 0.5%")
    ax.set_xlabel("Domain pooled scalar median error (%)")
    ax.set_ylabel("Benchmark count")
    ax.set_title(f"FSOT precision envelope — {len(medians)} scalar domains")
    ax.legend()
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)


def figure_predicted_vs_measured(out: Path, *, max_points: int = 800) -> None:
    import matplotlib.pyplot as plt

    data_dir = ROOT / "data"
    xs: list[float] = []
    ys: list[float] = []
    for path in sorted(data_dir.glob("*_benchmark.json")):
        if path.name == "structure_calibration_benchmark.json":
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for rec in doc.get("material_records") or doc.get("records") or []:
            if rec.get("property") in {"pooled_median", "fsot_prediction", "fsot_intrinsic_prediction"}:
                continue
            c, m = rec.get("computed"), rec.get("measured")
            if c is None or m is None:
                continue
            try:
                cf, mf = float(c), float(m)
            except (TypeError, ValueError):
                continue
            if mf == 0 or abs(mf) > 1e12:
                continue
            xs.append(mf)
            ys.append(cf)
            if len(xs) >= max_points:
                break
        if len(xs) >= max_points:
            break

    if len(xs) < 10:
        raise RuntimeError("Insufficient computed/measured pairs for scatter")

    lo = min(min(xs), min(ys))
    hi = max(max(xs), max(ys))

    fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
    ax.scatter(xs, ys, s=8, alpha=0.35, color="#0f766e", edgecolors="none")
    ax.plot([lo, hi], [lo, hi], color="#dc2626", linewidth=1.2, label="y = x")
    ax.set_xlabel("Measured")
    ax.set_ylabel("FSOT computed")
    ax.set_title(f"Predicted vs measured ({len(xs)} points, capped)")
    ax.legend()
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)


def figure_tier_precision_heatmap(out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    tiers = _load_manifest_tiers()
    rows = _load_margin_rows()
    by_tier: dict[int, list[float]] = {}
    for r in rows:
        if (r.get("scalar_count") or 0) <= 0:
            continue
        domain = str(r.get("domain") or r.get("file") or "")
        file_name = str(r.get("file") or "")
        tier = tiers.get(domain) or tiers.get(file_name) or 0
        med = float(r.get("scalar_pooled_median_error_pct") or r.get("pooled_median_error_pct") or 0)
        by_tier.setdefault(tier, []).append(med)

    if not by_tier:
        raise RuntimeError("No tier-bucketed medians for heatmap")

    tier_keys = sorted(t for t in by_tier if t > 0)
    if not tier_keys:
        tier_keys = sorted(by_tier.keys())

    medians = [statistics.median(by_tier[t]) for t in tier_keys]
    counts = [len(by_tier[t]) for t in tier_keys]
    vmax = max(max(medians), 0.05)

    fig, ax = plt.subplots(figsize=(10, max(4, len(tier_keys) * 0.35)), facecolor="white")
    data = np.array(medians).reshape(-1, 1)
    im = ax.imshow(data, aspect="auto", cmap="YlGnBu_r", vmin=0, vmax=vmax)
    ax.set_yticks(range(len(tier_keys)))
    ax.set_yticklabels([f"Tier {t}  (n={counts[i]})" for i, t in enumerate(tier_keys)])
    ax.set_xticks([0])
    ax.set_xticklabels(["Pooled median error (%)"])
    for i, val in enumerate(medians):
        ax.text(0, i, f"{val:.4f}%", ha="center", va="center", color="black", fontsize=9)
    ax.axhline(-0.5, color="white")
    fig.colorbar(im, ax=ax, label="Median error (%)", shrink=0.8)
    ax.set_title("FSOT precision by extension tier (domain-family rollup)")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)


def figure_contested_observables_panel(out: Path) -> None:
    import matplotlib.pyplot as plt

    if not PUSHBACK_AUDIT.exists():
        raise FileNotFoundError(f"Run audit_scientific_pushback_coverage.py first: {PUSHBACK_AUDIT}")
    doc = json.loads(PUSHBACK_AUDIT.read_text(encoding="utf-8"))
    avenues = doc.get("pushback_avenues") or []
    if not avenues:
        raise RuntimeError("No pushback avenues in scientific_pushback_audit.json")

    labels = [str(a.get("avenue") or a.get("status") or "?") for a in avenues]
    covered = [1.0 if a.get("benchmark_coverage") else 0.0 for a in avenues]
    colors = ["#16a34a" if c else "#dc2626" for c in covered]

    fig, ax = plt.subplots(figsize=(10, max(5, len(labels) * 0.45)), facecolor="white")
    y_pos = range(len(labels))
    ax.barh(list(y_pos), covered, color=colors, edgecolor="#1e3a8a", alpha=0.85)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Benchmark coverage (1 = monitored in extension panels)")
    ax.set_title(
        f"Contested / open observables — {len(avenues)} avenues tracked, "
        f"{sum(1 for c in covered if c)} with benchmark rows"
    )
    for i, a in enumerate(avenues):
        ref = str(a.get("reference") or "")[:28]
        sev = str(a.get("severity") or "monitored")
        ax.text(1.02, i, f"{sev} · {ref}", va="center", fontsize=7, color="#374151")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figure_coverage_treemap(out: Path) -> None:
    import matplotlib.pyplot as plt

    audit_path = ROOT / "data" / "full_system_coverage_audit.json"
    if not audit_path.exists():
        raise FileNotFoundError("Run audit_full_system_coverage.py first")
    doc = json.loads(audit_path.read_text(encoding="utf-8"))
    summary = doc.get("summary") or {}
    labels = [
        f"Core 35\n({summary.get('core_total_empirical_records', 0):,} records)",
        f"Extension 347\n({summary.get('extension_panels_verified', 347)} panels)",
        f"Tier A strong\n({summary.get('tier_A_strong', 0)})",
        f"Tier B verified\n({summary.get('tier_B_verified', 0)})",
        f"Tier C thin\n({summary.get('tier_C_thin', 0)})",
    ]
    sizes = [
        summary.get("fsot_formula_core_domains", 35),
        summary.get("extension_panels_verified", 347),
        summary.get("tier_A_strong", 110),
        summary.get("tier_B_verified", 240),
        summary.get("tier_C_thin", 26),
    ]
    colors = ["#1d4ed8", "#059669", "#7c3aed", "#0891b2", "#d97706"]

    fig, ax = plt.subplots(figsize=(9, 6), facecolor="white")
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
    ax.set_title("FSOT scientific surface coverage (376 domains)")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build scientific figure pack from FSOT audits")
    parser.add_argument("--output-dir", type=Path, default=FIG_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    figure_domain_error_envelope(args.output_dir / "domain_error_envelope.png")
    figure_predicted_vs_measured(args.output_dir / "predicted_vs_measured_scatter.png")
    figure_coverage_treemap(args.output_dir / "coverage_surface_pie.png")
    figure_tier_precision_heatmap(args.output_dir / "tier_precision_heatmap.png")
    figure_contested_observables_panel(args.output_dir / "contested_observables_panel.png")

    manifest = {
        "generated_from": str(ROOT),
        "figures": [
            "domain_error_envelope.png",
            "predicted_vs_measured_scatter.png",
            "coverage_surface_pie.png",
            "tier_precision_heatmap.png",
            "contested_observables_panel.png",
        ],
        "domain_median_count": len(
            [
                r
                for r in _load_margin_rows()
                if (r.get("scalar_count") or 0) > 0 and not r.get("excluded")
            ]
        ),
        "pooled_median_of_domains": statistics.median(
            [
                float(r.get("scalar_pooled_median_error_pct") or 0)
                for r in _load_margin_rows()
                if (r.get("scalar_count") or 0) > 0
            ]
        ),
    }
    pub_manifest = args.output_dir / "publication_figure_manifest.json"
    if pub_manifest.exists():
        pub = json.loads(pub_manifest.read_text(encoding="utf-8"))
        for name in pub.get("figures") or []:
            if name not in manifest["figures"]:
                manifest["figures"].append(name)
    (args.output_dir / "figure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote figures to {args.output_dir}")
    for name in manifest["figures"]:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())