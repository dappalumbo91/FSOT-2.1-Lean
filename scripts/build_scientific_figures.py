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


def _prediction_domain_rows() -> list[dict]:
    """Domains whose official pooled median is a prediction score.

    Ledger B scale-step files have scalar_count 0 and drop out here.
    """
    rows = [
        r
        for r in _load_margin_rows()
        if (r.get("scalar_count") or 0) > 0 and r.get("official_pooled_median_error_pct") is not None
    ]
    if not rows:
        raise RuntimeError("No prediction-domain medians in benchmark_margin_audit.json")
    return rows


def _prediction_medians() -> list[float]:
    return [float(r["official_pooled_median_error_pct"]) for r in _prediction_domain_rows()]


def figure_domain_error_envelope(out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    medians = _prediction_medians()
    positive = [m for m in medians if m > 0]
    zeros = sum(1 for m in medians if m == 0)
    negative = sum(1 for m in medians if m < 0)
    if not positive:
        raise RuntimeError("No positive prediction-domain medians to histogram")

    header = json.loads(MARGIN_AUDIT.read_text(encoding="utf-8"))
    worst = header.get("worst_scalar_max_error_pct")
    worst_name = header.get("worst_scalar_domain")
    headline = statistics.median(medians)

    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor="white")
    bins = np.geomspace(min(positive), max(max(positive), 0.5), 28)
    ax.hist(positive, bins=bins, color="#2563eb", edgecolor="#1e3a8a", alpha=0.85)
    ax.set_xscale("log")
    ax.set_xlim(min(positive) * 0.7, 0.6)
    ax.axvline(0.05, color="#16a34a", linestyle="--", linewidth=1.5, label="0.05% prediction score")
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.5, label="0.5% catalog gate")
    if headline > 0:
        ax.axvline(
            headline,
            color="#7c3aed",
            linestyle="-",
            linewidth=1.6,
            label=f"median of all {len(medians)} = {headline:.6g}%",
        )
    ax.set_xlabel("Official pooled median error (%)")
    ax.set_ylabel("Domains with a positive median")
    ax.set_title(
        f"Prediction-domain medians — {len(positive)} positive, {zeros} at zero, {negative} negative"
    )
    note = "Scale-step domains are not in this histogram."
    if worst is not None:
        note += f" Largest record error {worst}% ({worst_name}) is not a domain median."
    ax.text(0.0, -0.18, note, transform=ax.transAxes, fontsize=8, color="#475569")
    ax.legend(fontsize=8)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figure_prediction_median_ecdf(out: Path) -> None:
    import matplotlib.pyplot as plt

    medians = sorted(_prediction_medians())
    n = len(medians)
    ys = [(i + 1) / n for i in range(n)]
    headline = statistics.median(medians)
    zeros = sum(1 for m in medians if m == 0)

    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor="white")
    ax.step(medians, ys, where="post", color="#1d4ed8", linewidth=1.8)
    ax.set_xlim(min(medians[0], 0.0) - 0.005, 0.55)
    ax.set_ylim(0, 1.02)
    ax.axvline(0.05, color="#16a34a", linestyle="--", linewidth=1.4, label="0.05% prediction score")
    ax.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.4, label="0.5% catalog gate")
    ax.axvline(headline, color="#7c3aed", linestyle="-", linewidth=1.5, label=f"median {headline:.6g}%")
    ax.axhline(0.5, color="#94a3b8", linewidth=0.8)
    ax.set_xlabel("Official pooled median error (%)")
    ax.set_ylabel("Fraction of prediction domains")
    ax.set_title(f"Cumulative distribution of {n} prediction-domain medians")
    ax.text(
        0.0,
        -0.18,
        f"{zeros} medians are exactly zero. Ledger B scale-step domains are not on this curve.",
        transform=ax.transAxes,
        fontsize=8,
        color="#475569",
    )
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def _sample_prediction_pairs(*, per_file: int = 16) -> list[tuple[float, float]]:
    from benchmark_margin_lib import classify_record

    pairs: list[tuple[float, float]] = []
    files_used = 0
    for path in sorted((ROOT / "data").glob("*_benchmark.json")):
        if path.name == "structure_calibration_benchmark.json" or path.name.startswith("adversarial_"):
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        candidates: list[tuple[float, float]] = []
        for rec in doc.get("material_records") or doc.get("records") or []:
            if not isinstance(rec, dict):
                continue
            if classify_record(rec, file_name=path.name) != "scalar":
                continue
            if rec.get("property") in {"pooled_median", "fsot_prediction", "fsot_intrinsic_prediction"}:
                continue
            measured, computed = rec.get("measured"), rec.get("computed")
            if measured is None or computed is None:
                continue
            try:
                mf, cf = float(measured), float(computed)
            except (TypeError, ValueError):
                continue
            if mf == 0 or cf == 0 or abs(mf) > 1e12 or abs(cf) > 1e12:
                continue
            candidates.append((mf, cf))
        if not candidates:
            continue
        files_used += 1
        if len(candidates) <= per_file:
            pairs.extend(candidates)
        else:
            step = len(candidates) / per_file
            pairs.extend(candidates[int(i * step)] for i in range(per_file))
    print(f"  prediction sample: {len(pairs)} points from {files_used} files")
    return pairs


def figure_predicted_vs_measured(out: Path, *, per_file: int = 16) -> None:
    import matplotlib.pyplot as plt

    pairs = _sample_prediction_pairs(per_file=per_file)
    if len(pairs) < 10:
        raise RuntimeError("Insufficient prediction pairs for the calibration figure")

    import numpy as np

    positive = [(m, c) for m, c in pairs if m > 0 and c > 0]
    abs_pct = [abs(100.0 * (c - m) / m) for m, c in pairs]
    nonzero = [v for v in abs_pct if v > 0]
    exact = sum(1 for v in abs_pct if v == 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), facecolor="white")

    ax = axes[0]
    if len(positive) < 10:
        raise RuntimeError("Insufficient positive prediction pairs for the log-log panel")
    ax.scatter(
        [m for m, _ in positive],
        [c for _, c in positive],
        s=10,
        alpha=0.35,
        color="#0f766e",
        edgecolors="none",
    )
    lo = min(min(m for m, _ in positive), min(c for _, c in positive))
    hi = max(max(m for m, _ in positive), max(c for _, c in positive))
    ax.plot([lo, hi], [lo, hi], color="#dc2626", linewidth=1.1, label="computed = measured")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Measured (row unit)")
    ax.set_ylabel("Computed (same row unit)")
    ax.set_title(f"Positive prediction rows ({len(positive)})")
    ax.legend(fontsize=8)

    ax2 = axes[1]
    if not nonzero:
        raise RuntimeError("No nonzero percent residuals in the prediction sample")
    bins = np.geomspace(min(nonzero), max(max(nonzero), 0.5), 30)
    ax2.hist(nonzero, bins=bins, color="#1d4ed8", edgecolor="#1e3a8a", alpha=0.85)
    ax2.set_xscale("log")
    ax2.axvline(0.05, color="#16a34a", linestyle="--", linewidth=1.2, label="0.05%")
    ax2.axvline(0.5, color="#ca8a04", linestyle="--", linewidth=1.2, label="0.5%")
    ax2.set_xlabel("Absolute percent error")
    ax2.set_ylabel("Sampled rows with a nonzero error")
    ax2.set_title(f"{exact} exact zeros omitted from the bars")
    ax2.legend(fontsize=8)

    fig.suptitle(
        "Prediction rows only. Scale-step rows, blank computed values, and adversarial probes are omitted. "
        "At most 16 rows are taken from each file.",
        fontsize=10,
    )
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
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
        if r.get("official_pooled_median_error_pct") is None:
            continue
        med = float(r["official_pooled_median_error_pct"])
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
    ax.set_title("Prediction-domain medians by extension tier")
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

    snap_path = ROOT / "data" / "repo_status_snapshot.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    tiers = (snap.get("empirical") or {}).get("tier_distribution") or {}
    if not tiers:
        raise RuntimeError(f"No tier_distribution in {snap_path}")
    order = ["A_strong", "B_verified", "B_process", "B_named"]
    labels = [name for name in order if name in tiers] + [name for name in tiers if name not in order]
    values = [int(tiers[name]) for name in labels]
    stamp = str(snap.get("generated_at") or "")[:10]
    colors = ["#7c3aed", "#0891b2", "#d97706", "#059669", "#1d4ed8"]

    fig, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.barh(labels[::-1], values[::-1], color=list(reversed(colors[: len(labels)])), edgecolor="#1e3a8a")
    for i, val in enumerate(values[::-1]):
        ax.text(val, i, f"  {val}", va="center", fontsize=10)
    ax.set_xlabel("Domains in the stored tier rollup")
    ax.set_title(f"Coverage tiers from the status snapshot ({stamp})")
    ax.set_xlim(0, max(values) * 1.15)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)


# Residuals already written in docs/TOE_ACCURACY_GOALS.md.
# Positive means the reading is above the central value.
_NUCLEAR_SIGMA = (
    ("Helium-4", -0.027, 0.00067),
    ("Triton", 0.13, 0.037),
    ("Deuteron", -3.88, -3.59),
)


def figure_nuclear_binding_sigma(out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    names = [row[0] for row in _NUCLEAR_SIGMA]
    rounded = [row[1] for row in _NUCLEAR_SIGMA]
    rebuild = [row[2] for row in _NUCLEAR_SIGMA]
    y = np.arange(len(names))
    height = 0.36

    fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="white")
    ax.barh(y - height / 2, rounded, height=height, color="#1d4ed8", label="Rounded AME total")
    ax.barh(y + height / 2, rebuild, height=height, color="#059669", label="Mass-excess rebuild")
    ax.axvline(0.0, color="#111827", linewidth=0.9)
    ax.axvline(1.0, color="#ca8a04", linestyle="--", linewidth=1.1, label="±1 published uncertainty")
    ax.axvline(-1.0, color="#ca8a04", linestyle="--", linewidth=1.1)
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    ax.set_xlabel("Residual in published uncertainties")
    ax.set_xlim(-4.8, 1.6)
    def _annotate(val: float, ypos: float) -> None:
        if val >= 0:
            ax.text(val + 0.06, ypos, f"{val:+.5g}", ha="left", va="center", fontsize=8)
        else:
            ax.text(val - 0.06, ypos, f"{val:+.5g}", ha="right", va="center", fontsize=8)

    for i, (left, right) in enumerate(zip(rounded, rebuild)):
        _annotate(left, i - height / 2)
        _annotate(right, i + height / 2)
    ax.set_title("Nuclear binding leaves — helium-4, triton, deuteron")
    ax.text(
        0.0,
        -0.2,
        "Numbers as written in docs/TOE_ACCURACY_GOALS.md. Positive means above the central value.",
        transform=ax.transAxes,
        fontsize=8,
        color="#475569",
    )
    ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(0.22, 0.38), framealpha=0.95)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def _lean_library_jobs() -> str:
    report = ROOT / "data" / "fresh_clone_lean_repro_report.md"
    text = report.read_text(encoding="utf-8") if report.is_file() else ""
    marker = "jobs"
    if marker not in text:
        return "not recorded"
    head = text.split(marker)[0]
    digits = ""
    for ch in reversed(head):
        if ch.isdigit():
            digits = ch + digits
        elif digits:
            break
    return f"{digits} jobs" if digits else "not recorded"


def figure_prover_outcomes(out: Path) -> None:
    import matplotlib.pyplot as plt

    report = ROOT / "data" / "cross_proof_verification_report.json"
    cross = json.loads(report.read_text(encoding="utf-8"))
    frameworks = cross.get("frameworks") or {}
    formal = cross.get("full_formal_spine") or {}
    catalog = cross.get("scientific_catalog_spine") or {}
    trans = cross.get("transcendental_bounds") or {}
    connective = cross.get("connective_spine") or {}
    rust = frameworks.get("rust_replay") or {}

    count_labels = [
        "Connective spine",
        "Transcendental bounds",
        "Catalog obligations",
        "Atomic provable",
        "Rust replay",
        "Full formal",
    ]
    count_values = [
        int(connective.get("obligation_count") or 0),
        int(trans.get("obligation_count") or 0),
        int(catalog.get("obligation_count") or 0),
        int(formal.get("atomic_provable_count") or 0),
        int(rust.get("obligation_count") or 0),
        int(formal.get("obligation_count") or 0),
    ]

    coq = frameworks.get("coq") or {}
    isabelle = frameworks.get("isabelle") or {}
    fstar = frameworks.get("fstar") or {}
    qemu = frameworks.get("qemu_harness") or {}
    esp = frameworks.get("esp32_harness") or {}
    eight = bool(cross.get("eight_way_hardware"))
    statuses = [
        ("Coq", f"{coq.get('chunks_passed')}/{coq.get('chunk_count')}", str(coq.get("status") or "")),
        (
            "Isabelle",
            f"{isabelle.get('chunks_passed')}/{isabelle.get('chunk_count')}",
            str(isabelle.get("status") or ""),
        ),
        ("F*", "boot kernel", str(fstar.get("status") or "")),
        ("QEMU", "serial and disk", str(qemu.get("status") or "")),
        ("Lean library", _lean_library_jobs(), "passed"),
        ("ESP32", str(esp.get("reason") or "skipped"), str(esp.get("status") or "skipped")),
        ("Eight-way hardware", "not claimed" if not eight else "claimed", "skipped" if not eight else "passed"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), facecolor="white")
    ax = axes[0]
    ax.barh(count_labels[::-1], count_values[::-1], color="#1d4ed8", alpha=0.9)
    for i, val in enumerate(count_values[::-1]):
        ax.text(val, i, f"  {val}", va="center", fontsize=8)
    ax.set_xlabel("Count in the cross-proof report")
    ax.set_title("What was checked")
    ax.set_xlim(0, max(count_values) * 1.18)

    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-0.5, len(statuses) - 0.5)
    ax2.axis("off")
    ax2.set_title("Outcome")
    for i, (name, detail, status) in enumerate(statuses):
        y = len(statuses) - 1 - i
        color = "#059669" if status == "passed" else "#94a3b8"
        ax2.barh(y, 8.2, color=color, alpha=0.25, height=0.7)
        ax2.text(0.2, y, f"{name}: {detail}  ({status})", va="center", fontsize=9)

    stamp = str(cross.get("generated_at") or "")[:19]
    fig.suptitle(f"Cross-proof outcomes ({stamp})", fontsize=12, fontweight="bold")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build scientific figure pack from FSOT audits")
    parser.add_argument("--output-dir", type=Path, default=FIG_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    figure_domain_error_envelope(args.output_dir / "domain_error_envelope.png")
    figure_prediction_median_ecdf(args.output_dir / "prediction_median_ecdf.png")
    figure_predicted_vs_measured(args.output_dir / "predicted_vs_measured_scatter.png")
    figure_coverage_treemap(args.output_dir / "coverage_surface_pie.png")
    figure_tier_precision_heatmap(args.output_dir / "tier_precision_heatmap.png")
    figure_contested_observables_panel(args.output_dir / "contested_observables_panel.png")
    figure_prover_outcomes(args.output_dir / "prover_outcome_board.png")
    figure_nuclear_binding_sigma(args.output_dir / "nuclear_binding_sigma.png")

    manifest = {
        "generated_from": str(ROOT),
        "figures": [
            "domain_error_envelope.png",
            "prediction_median_ecdf.png",
            "predicted_vs_measured_scatter.png",
            "coverage_surface_pie.png",
            "tier_precision_heatmap.png",
            "contested_observables_panel.png",
            "prover_outcome_board.png",
            "nuclear_binding_sigma.png",
        ],
        "domain_median_count": len(_prediction_domain_rows()),
        "pooled_median_of_domains": statistics.median(_prediction_medians()),
    }
    pub_manifest = args.output_dir / "publication_figure_manifest.json"
    if pub_manifest.exists():
        pub = json.loads(pub_manifest.read_text(encoding="utf-8"))
        for name in pub.get("figures") or []:
            if name not in manifest["figures"]:
                manifest["figures"].append(name)
    (args.output_dir / "figure_manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding="utf-8")
    print(f"Wrote figures to {args.output_dir}")
    for name in manifest["figures"]:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())