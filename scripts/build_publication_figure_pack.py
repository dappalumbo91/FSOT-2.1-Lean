#!/usr/bin/env python3
"""Publication figure pack for peer review — spine walkthrough + contested sector + H0."""

from __future__ import annotations

import argparse
import json
import statistics
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
    gap = 1.28
    fig, ax = plt.subplots(figsize=(11, 8.4), facecolor="white")
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, len(steps) * gap + 0.45)
    ax.axis("off")

    colors = ["#1e3a8a", "#1d4ed8", "#2563eb", "#059669", "#0891b2", "#7c3aed"]
    y = len(steps) * gap
    for i, step in enumerate(steps):
        color = colors[i % len(colors)]
        label = str(step.get("label") or f"Step {step.get('step')}")
        detail = step.get("formula") or step.get("detail")
        if isinstance(detail, dict):
            detail_txt = ", ".join(f"{k}={v}" for k, v in list(detail.items())[:4])
        else:
            detail_txt = str(detail or "")[:140]

        box = FancyBboxPatch(
            (0.45, y - 1.0),
            9.1,
            0.95,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            linewidth=1.2,
            edgecolor=color,
            facecolor="#f8fafc",
        )
        ax.add_patch(box)
        ax.text(0.65, y - 0.28, f"{step.get('step')}. {label}", fontsize=11, fontweight="bold", va="top")
        ax.text(0.65, y - 0.62, detail_txt, fontsize=8.5, va="top", color="#334155")
        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(5, y - gap + 0.06),
                xytext=(5, y - 1.05),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5),
            )
        y -= gap

    recorded = str(walk.get("generated_at") or "")[:10]
    ax.set_title(
        f"FSOT seed spine — recorded chain ({recorded})",
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

    rows = list(contested.get("observables") or [])
    if not rows:
        raise RuntimeError("No contested observables in contested_observables_closure.json")
    rows.sort(key=lambda r: float(r.get("fsot_error_pct") or 0))
    names = [str(r.get("name") or r.get("property")) for r in rows]
    fsot_err = [float(r.get("fsot_error_pct") or 0) for r in rows]
    pooled = float(np.median(fsot_err))
    stored_baseline = (contested.get("panel_summary") or {}).get("current_model_baseline_pct")

    fig, ax = plt.subplots(figsize=(10, max(6, len(names) * 0.42)), facecolor="white")
    y = np.arange(len(names))
    ax.barh(y, fsot_err, height=0.6, color="#059669", label="Stored row error %", alpha=0.9)
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.2, label="catalog gate 0.5%")
    ax.axvline(pooled, color="#1d4ed8", linestyle="-", linewidth=1.2, label=f"median of these rows {pooled:.6g}%")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Relative error of the stored readout (%)")
    ax.set_title(
        f"Contested readouts — median of the {len(rows)} stored row errors is {pooled:.6g}%",
        fontsize=11,
    )
    note = "The 15% typical baseline stored on this panel is not a measured residual, so it is not drawn."
    if stored_baseline is not None:
        note = (
            f"A {stored_baseline:g}% typical baseline is stored on this panel. "
            "It is not a measured residual, so it is not drawn."
        )
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.012, note, fontsize=8, color="#475569")
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

    labels, details, errors = [], [], []
    for r in h0_rows:
        labels.append(str(r.get("name") or "?")[:40])
        unit = str(r.get("unit") or "")
        details.append(
            f"computed {float(r.get('computed') or 0):.6g}   "
            f"measured {float(r.get('measured') or 0):.6g} {unit}"
        )
        errors.append(float(r.get("fsot_error_pct") or 0))

    fig, ax = plt.subplots(figsize=(11, 5.2), facecolor="white")
    y = range(len(labels))
    ax.barh(list(y), errors, color="#2563eb", alpha=0.9)
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.2, label="catalog gate 0.5%")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Stored relative error (%)")
    ax.set_title("Hubble rows stored on the contested closure")
    span = max(errors + [0.5])
    for i, (err, detail) in enumerate(zip(errors, details)):
        ax.text(err + span * 0.03, i, f"{err:.4g}%    {detail}", va="center", fontsize=8, color="#1e293b")
    ax.set_xlim(0, span * 3.4)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figure_empirical_headline(out: Path, empirical: dict) -> None:
    import matplotlib.pyplot as plt

    env = empirical.get("benchmark_envelope") or {}
    labels = [
        "Benchmark files green",
        "Median of prediction medians (%)",
        "Medians at or under 0.5%",
        "Worst record scalar (%)",
        "Unique formulas recompute",
    ]
    median_txt = f"{float(env.get('pooled_median_of_domains_pct', 0)):.15g}"
    values = [
        f"{env.get('green_gate_pass_count', 0)}/{env.get('benchmark_file_count', 0)}",
        median_txt,
        str(env.get("domains_under_0_5pct_median", "")),
        f"{float(env.get('worst_domain_max_scalar_error_pct', 0)):.6g}"
        f"  ({env.get('worst_scalar_domain', '')})",
        f"{(empirical.get('formula_corpus_unique') or {}).get('live_recompute_ok_ratio', 0) * 100:.1f}%",
    ]

    fig, ax = plt.subplots(figsize=(10, 4.4), facecolor="white")
    ax.axis("off")
    ax.set_title("Empirical scoreboard — prediction medians", fontsize=12, fontweight="bold")
    for i, (lab, val) in enumerate(zip(labels, values)):
        ax.text(0.04, 0.78 - i * 0.14, lab, fontsize=11, fontweight="bold", transform=ax.transAxes)
        ax.text(0.48, 0.78 - i * 0.14, val, fontsize=11, color="#1d4ed8", transform=ax.transAxes)
    ax.text(
        0.04,
        0.06,
        "The median is over prediction-domain pooled medians. Ledger B scale-step rows are not in it.",
        fontsize=8,
        color="#475569",
        transform=ax.transAxes,
    )
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
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_verified_desktop_transporter_figure.py")],
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
            "verified_desktop_transporter.png",
        ],
        "data_sources": [
            str(WALKTHROUGH),
            str(CONTESTED),
            str(EMPIRICAL),
        ],
        "contested_pooled_median_pct": (
            float(
                statistics.median(
                    [float(r.get("fsot_error_pct") or 0) for r in (contested.get("observables") or [])]
                )
            )
            if contested.get("observables")
            else None
        ),
        "contested_panel_summary_pooled_median_pct": (contested.get("panel_summary") or {}).get(
            "pooled_median_error_pct"
        ),
        "empirical_median_of_domains_pct": (empirical.get("benchmark_envelope") or {}).get(
            "pooled_median_of_domains_pct"
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding="utf-8")

    print(f"Wrote publication figures to {args.output_dir}")
    for name in manifest["figures"]:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())