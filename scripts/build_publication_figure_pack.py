#!/usr/bin/env python3
"""Publication figure pack for peer review — spine walkthrough + contested sector + H0."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FIG_DIR = ROOT / "data" / "figures"
EMPIRICAL = ROOT / "data" / "empirical_accuracy_closure.json"
CONTESTED = ROOT / "data" / "contested_observables_closure.json"
WALKTHROUGH = ROOT / "data" / "publication_spine_walkthrough.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _ensure_walkthrough() -> dict:
    if not WALKTHROUGH.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_publication_spine_walkthrough.py")],
            check=True,
            cwd=str(ROOT),
        )
    return _load(WALKTHROUGH)


def figure_spine_walkthrough(out: Path, walk: dict) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    steps = walk.get("chain") or []
    fig, ax = plt.subplots(figsize=(11, 8), facecolor="white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(steps) + 1)
    ax.axis("off")

    colors = ["#1e3a8a", "#1d4ed8", "#2563eb", "#059669", "#0891b2", "#7c3aed"]
    y = len(steps) + 0.2
    for i, step in enumerate(steps):
        color = colors[i % len(colors)]
        label = str(step.get("label") or f"Step {step.get('step')}")
        detail = step.get("formula") or step.get("detail")
        if isinstance(detail, dict):
            detail_txt = ", ".join(f"{k}={v}" for k, v in list(detail.items())[:4])
        else:
            detail_txt = str(detail or "")[:120]

        box = FancyBboxPatch(
            (0.5, y - 0.85),
            9.0,
            0.9,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            linewidth=1.2,
            edgecolor=color,
            facecolor="#f8fafc",
        )
        ax.add_patch(box)
        ax.text(0.7, y - 0.25, f"{step.get('step')}. {label}", fontsize=11, fontweight="bold", va="top")
        ax.text(0.7, y - 0.55, detail_txt, fontsize=8.5, va="top", color="#334155")
        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(5, y - 0.95),
                xytext=(5, y - 1.15),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5),
            )
        y -= 1.35

    ax.set_title(
        "FSOT Theory of Everything — single seed spine fractals to all observables",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, facecolor="white")
    plt.close(fig)


def figure_contested_fsot_vs_baseline(out: Path, contested: dict) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    rows = contested.get("observables") or []
    if not rows:
        raise RuntimeError("No contested observables in contested_observables_closure.json")

    names = [str(r.get("name") or r.get("property")) for r in rows]
    fsot_err = [float(r.get("fsot_error_pct") or 0) for r in rows]
    baseline = float((contested.get("panel_summary") or {}).get("current_model_baseline_pct") or 15.0)

    fig, ax = plt.subplots(figsize=(10, max(6, len(names) * 0.42)), facecolor="white")
    y = np.arange(len(names))
    ax.barh(y - 0.2, fsot_err, height=0.35, color="#059669", label="FSOT error %", alpha=0.9)
    ax.barh(y + 0.2, [baseline] * len(names), height=0.35, color="#94a3b8", label="ΛCDM/SM typical (no unified pred.)", alpha=0.7)
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.2, label="green gate 0.5%")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Relative error (%)")
    pooled = (contested.get("panel_summary") or {}).get("pooled_median_error_pct")
    ax.set_title(
        f"Contested / open-sector observables — FSOT pooled median {pooled:.4f}% vs {baseline}% baseline",
        fontsize=11,
    )
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figure_h0_landscape(out: Path, contested: dict) -> None:
    import matplotlib.pyplot as plt

    h0_rows = [
        r
        for r in (contested.get("observables") or [])
        if str(r.get("property") or "") == "hubble_constant"
        or str(r.get("property") or "") == "hubble_tension"
    ]
    if not h0_rows:
        raise RuntimeError("No H0 rows in contested closure")

    labels, measured, computed, errors = [], [], [], []
    for r in h0_rows:
        labels.append(str(r.get("name") or "?")[:28])
        measured.append(float(r.get("measured") or 0))
        computed.append(float(r.get("computed") or 0))
        errors.append(float(r.get("fsot_error_pct") or 0))

    x = range(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(11, 5.5), facecolor="white")
    ax.bar([i - width / 2 for i in x], measured, width, label="Literature measured", color="#64748b")
    ax.bar([i + width / 2 for i in x], computed, width, label="FSOT spine computed", color="#2563eb")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("km/s/Mpc (or tension Δ)")
    ax.set_title("Hubble sector — FSOT unified readouts vs public data (Planck, SH0ES, dual-anchor)")
    for i, err in enumerate(errors):
        ax.text(i, max(measured[i], computed[i]) + 0.5, f"{err:.3f}%", ha="center", fontsize=7, color="#059669")
    ax.legend()
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figure_empirical_headline(out: Path, empirical: dict) -> None:
    import matplotlib.pyplot as plt

    env = empirical.get("benchmark_envelope") or {}
    labels = [
        "Domains green",
        "Median-of-domains (%)",
        "Worst max scalar (%)",
        "Unique formulas OK",
        "SOTA panel beats",
    ]
    values = [
        f"{env.get('green_gate_pass_count', 0)}/{env.get('benchmark_file_count', 0)}",
        f"{float(env.get('pooled_median_of_domains_pct', 0)):.5f}",
        f"{float(env.get('worst_domain_max_scalar_error_pct', 0)):.4f}",
        f"{(empirical.get('formula_corpus_unique') or {}).get('live_recompute_ok_ratio', 0) * 100:.1f}%",
        f"{(empirical.get('sota_external_panel') or {}).get('beats_or_meets_count', 0)}/"
        f"{(empirical.get('sota_external_panel') or {}).get('observable_count', 0)}",
    ]

    fig, ax = plt.subplots(figsize=(9, 4), facecolor="white")
    ax.axis("off")
    ax.set_title("FSOT empirical closure headline (single intrinsic spine)", fontsize=12, fontweight="bold")
    for i, (lab, val) in enumerate(zip(labels, values)):
        ax.text(0.05, 0.82 - i * 0.16, lab, fontsize=11, fontweight="bold", transform=ax.transAxes)
        ax.text(0.55, 0.82 - i * 0.16, val, fontsize=11, color="#1d4ed8", transform=ax.transAxes)
    claim = empirical.get("primary_claim") or ""
    ax.text(0.05, 0.05, claim[:200] + ("…" if len(claim) > 200 else ""), fontsize=8, color="#475569", wrap=True, transform=ax.transAxes)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, facecolor="white")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build publication figure pack")
    parser.add_argument("--output-dir", type=Path, default=FIG_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    walk = _ensure_walkthrough()
    empirical = _load(EMPIRICAL)
    contested = _load(CONTESTED)
    if not contested:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_contested_observables_closure.py")],
            check=True,
            cwd=str(ROOT),
        )
        contested = _load(CONTESTED)

    figure_spine_walkthrough(args.output_dir / "spine_walkthrough.png", walk)
    figure_contested_fsot_vs_baseline(args.output_dir / "contested_fsot_vs_lcdm.png", contested)
    figure_h0_landscape(args.output_dir / "h0_landscape.png", contested)
    figure_empirical_headline(args.output_dir / "empirical_headline_summary.png", empirical)

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_verified_desktop_fuel_figure.py")],
        check=True,
        cwd=str(ROOT),
    )

    manifest_path = args.output_dir / "publication_figure_manifest.json"
    manifest = {
        "generated_from": str(ROOT),
        "figures": [
            "spine_walkthrough.png",
            "contested_fsot_vs_lcdm.png",
            "h0_landscape.png",
            "empirical_headline_summary.png",
            "verified_desktop_fuels.png",
        ],
        "data_sources": [
            str(WALKTHROUGH),
            str(CONTESTED),
            str(EMPIRICAL),
        ],
        "contested_pooled_median_pct": (contested.get("panel_summary") or {}).get(
            "pooled_median_error_pct"
        ),
        "empirical_median_of_domains_pct": (empirical.get("benchmark_envelope") or {}).get(
            "pooled_median_of_domains_pct"
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote publication figures to {args.output_dir}")
    for name in manifest["figures"]:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())