"""VibraFSOT register experiment + FSOTLean MC alignment — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_vibra_progress(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_mc_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_vibra(vibra: dict, mc: dict) -> dict[str, Any]:
    meta = vibra.get("metadata", {})
    vib_sum = vibra.get("summaries", {}).get("vib", {})
    trials = vibra.get("vib_trials", [])
    pattern_stability = trials[0].get("pattern_stability") if trials else None
    mc_obs = mc.get("observer_stability_mc", {})
    cp = str(mc_obs.get("checkpoints", [5])[0])
    cp_stats = mc_obs.get("per_checkpoint", {}).get(cp, {})
    ai = mc.get("ai", {})
    return {
        "d_eff": meta.get("d_eff"),
        "base_freq_hz": meta.get("base_freq_hz"),
        "trial_count": meta.get("trials"),
        "vib_stability_mean": vib_sum.get("stability_mean"),
        "vib_S_mean": vib_sum.get("S_mean"),
        "pattern_stability": pattern_stability,
        "relative_improvement_percent": vibra.get("summaries", {}).get("relative_improvement_percent"),
        "mc_trials": mc_obs.get("trials"),
        "mc_checkpoint": int(cp) if cp.isdigit() else 5,
        "mc_prob_non_decrease": cp_stats.get("prob_non_decrease"),
        "mc_mean_delta_stability": cp_stats.get("mean_delta_stability"),
        "ai_avg_raw_S": ai.get("avg_raw_S"),
        "ai_prob_positive": ai.get("prob_positive"),
    }