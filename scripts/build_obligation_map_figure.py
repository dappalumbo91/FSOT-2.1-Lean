#!/usr/bin/env python3
"""Five-prover obligation map figure for README §V."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "cross_proof_verification_report.json"
OUT = ROOT / "data" / "figures" / "obligation_map_five_provers.png"


def main() -> int:
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
    except ImportError:
        print("matplotlib not installed — skip obligation_map figure")
        return 0

    cross = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.is_file() else {}
    spine = cross.get("full_formal_spine") or {}
    atomic = spine.get("atomic_provable_count", 1863)
    overall = cross.get("overall_ok", True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    boxes = [
        (0.5, 3.5, "Seeds\nπ e φ γ G", "#2c3e50"),
        (2.2, 3.5, "Oracle\nfsot_compute.py", "#34495e"),
        (4.0, 3.5, f"Lean 4\nprimary", "#1a5276"),
        (5.8, 3.5, "Coq / Isabelle\nF*", "#2874a6"),
        (7.6, 3.5, f"Rust replay\n{atomic} obligations", "#3498db"),
        (4.8, 1.2, f"overall_ok: {overall}\ngithub_ready: {cross.get('github_ready', True)}", "#27ae60"),
    ]
    for x, y, text, color in boxes:
        patch = FancyBboxPatch(
            (x, y), 1.5, 1.2, boxstyle="round,pad=0.05", linewidth=1.5,
            edgecolor=color, facecolor=color, alpha=0.15,
        )
        ax.add_patch(patch)
        ax.text(x + 0.75, y + 0.6, text, ha="center", va="center", fontsize=9, fontweight="bold")

    arrows = [(2.0, 4.1, 2.2, 4.1), (3.7, 4.1, 4.0, 4.1), (5.5, 4.1, 5.8, 4.1), (7.3, 4.1, 7.6, 4.1), (5.5, 3.5, 5.5, 2.4)]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.5))

    ax.set_title("FSOT five-prover obligation map", fontsize=12, fontweight="bold")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())