#!/usr/bin/env python3
"""
Allen cohort evaluation + NeuroLab/SMILES bridge + canonical scalar A/B.

Produces data/neuron_cohort_report.json for NeuronCohortPriors.lean generation.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import types
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "neuron_cohort_manifest.yaml"
REPORT_PATH = ROOT / "data" / "neuron_cohort_report.json"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_canonical_adapter import canonical_domain_scalar  # noqa: E402
from neuron_canonical_scalar import bridge_metadata, canonical_neuron_scalar, legacy_micro_scalar  # noqa: E402


def _percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = min(len(s) - 1, max(0, int(p * len(s))))
    return s[idx]


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return 0.0
    return statistics.correlation(xs, ys)


def _infer_stratum(cell: dict, strata_cfg: list[dict]) -> str | None:
    line = str(cell.get("line_name") or "")
    dendrite = str(cell.get("tag__dendrite_type") or "")
    for spec in strata_cfg:
        markers = spec.get("cre_markers") or []
        if any(m in line for m in markers):
            return spec["id"]
        dendrite_types = spec.get("dendrite_types") or []
        if dendrite_types and dendrite in dendrite_types:
            if not any(
                any(m in line for m in other.get("cre_markers") or [])
                for other in strata_cfg
                if other["id"] != spec["id"]
            ):
                return spec["id"]
    return None


def eval_allen_fi_cohort(cells: list[dict], offset_pa: float) -> dict:
    rel_errs: list[float] = []
    preds: list[float] = []
    obs: list[float] = []
    canonical_s: list[float] = []

    for c in cells:
        rate = c.get("ef__avg_firing_rate")
        slope = c.get("ef__f_i_curve_slope")
        thr = c.get("ef__threshold_i_long_square")
        adapt = c.get("ef__adaptation") or 0.0
        if rate is None or slope is None or thr is None:
            continue
        if slope <= 0 or rate <= 0:
            continue
        stim = thr + offset_pa
        pred = slope * max(0.0, stim - thr)
        rel_errs.append(abs(pred - rate) / rate)
        preds.append(pred)
        obs.append(rate)
        canonical_s.append(
            canonical_neuron_scalar(0.1, adaptation_index=float(adapt) if adapt is not None else 0.0)
        )

    return {
        "cell_count": len(rel_errs),
        "fi_median_rel_err": statistics.median(rel_errs) if rel_errs else 1.0,
        "fi_mean_rel_err": statistics.mean(rel_errs) if rel_errs else 1.0,
        "fi_p90_rel_err": _percentile(rel_errs, 0.9),
        "fi_pearson_r": _pearson(preds, obs),
        "canonical_scalar_min": min(canonical_s) if canonical_s else 0.0,
        "canonical_scalar_mean": statistics.mean(canonical_s) if canonical_s else 0.0,
        "canonical_neuroscience_domain_S": canonical_domain_scalar("Neuroscience"),
    }


def _hero_fi_points(hero: dict) -> list[tuple[float, float, float]]:
    default_durations = [2000.0, 2000.0, 1750.0, 1000.0]
    points = []
    for i, row in enumerate(hero.get("sustained_fi") or []):
        dur = default_durations[i] if i < len(default_durations) else 2000.0
        points.append((row["current_nA"], row["measured_Hz"], dur))
    return points


def _patch_scalar(neuron, scalar_mode: str, allen_meas) -> None:
    if scalar_mode == "canonical":

        def _canon_scalar(self, input_current_nA, dendritic_synchrony):
            return canonical_neuron_scalar(
                input_current_nA,
                phase=self.soma.phase,
                dendritic_synchrony=dendritic_synchrony,
                rheobase=self.hybrid.fsot_rheobase,
                phi_coherence=self.hybrid.fsot_coherence,
            )

        neuron.compute_fsot_scalar_contribution = types.MethodType(_canon_scalar, neuron)
    elif scalar_mode == "legacy_override":

        def _legacy_scalar(self, input_current_nA, dendritic_synchrony):
            return legacy_micro_scalar(
                input_current_nA,
                self.soma.phase,
                dendritic_synchrony,
                self.hybrid.fsot_rheobase,
            )

        neuron.compute_fsot_scalar_contribution = types.MethodType(_legacy_scalar, neuron)


def eval_hero_hybrid_fi(hybrid_root: Path, hero_report: Path, scalar_mode: str) -> dict | None:
    """
    Run hero FI sim from hybrid_root cwd so Allen SDK manifest resolves correctly.

    scalar_mode: "native" (model default), "canonical", or "legacy_override".
    Does not inject JSON constants — those are captured outputs, not tuning inputs.
    """
    if not hybrid_root.exists() or not hero_report.exists():
        return None

    hero = json.loads(hero_report.read_text(encoding="utf-8"))
    points = _hero_fi_points(hero)
    if not points:
        return None

    old_cwd = os.getcwd()
    old_path = list(sys.path)
    try:
        os.chdir(hybrid_root)
        if str(hybrid_root) not in sys.path:
            sys.path.insert(0, str(hybrid_root))
        from fsot_allen_parameter_mapping import create_example_l23_pyramidal  # noqa: WPS433
        from fsot_hybrid_neuron_model import FSIOTAllenHybridNeuron  # noqa: WPS433

        allen_meas, hybrid = create_example_l23_pyramidal()
        rows = []
        for current, measured, duration_ms in points:
            neuron = FSIOTAllenHybridNeuron(allen_meas, hybrid)
            if scalar_mode != "native":
                _patch_scalar(neuron, scalar_mode, allen_meas)
            spikes = neuron.simulate(duration_ms=duration_ms, input_current_nA=current)
            model_hz = len(spikes) / (duration_ms / 1000.0)
            rel_err = abs(model_hz - measured) / max(0.1, measured)
            rows.append(
                {"current_nA": current, "measured_Hz": measured, "model_Hz": model_hz, "rel_err": rel_err}
            )

        mean_rel = statistics.mean(r["rel_err"] for r in rows)
        return {
            "scalar_mode": scalar_mode,
            "specimen_id": hero.get("specimen_id", allen_meas.specimen_id),
            "cell_class": hero.get("cell_class", allen_meas.cell_class),
            "data_source": allen_meas.data_source,
            "fi_point_count": len(rows),
            "mean_rel_err": mean_rel,
            "sustained_fi": rows,
            "sim_cwd": str(hybrid_root),
        }
    except ImportError:
        return None
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path


def hero_certified_from_report(hero_report: Path) -> dict | None:
    if not hero_report.exists():
        return None
    hero = json.loads(hero_report.read_text(encoding="utf-8"))
    return {
        "specimen_id": hero.get("specimen_id"),
        "cell_class": hero.get("cell_class"),
        "mean_rel_err": float(hero.get("mean_rel_err", 1.0)),
        "verifier_confidence": float((hero.get("verifier") or {}).get("confidence", 0.0)),
        "fi_point_count": len(hero.get("sustained_fi") or []),
        "source": str(hero_report),
    }


def eval_cohort_strata(cells: list[dict], manifest: dict) -> dict:
    """Per-class Allen FI proxy + held-out (hero excluded) for Tier 8 Lean priors."""
    strata_cfg = manifest.get("strata", {}).get("classes") or []
    hero_id = int(manifest.get("strata", {}).get("hero_specimen_id") or 0)
    offset_pa = float(manifest["fi_proxy"]["stim_offset_pa"])
    buckets: dict[str, list[dict]] = {spec["id"]: [] for spec in strata_cfg}
    unclassified: list[dict] = []
    held_out: list[dict] = []

    for cell in cells:
        sid = cell.get("specimen__id")
        if hero_id and sid == hero_id:
            continue
        held_out.append(cell)
        name = _infer_stratum(cell, strata_cfg)
        if name:
            buckets[name].append(cell)
        else:
            unclassified.append(cell)

    strata_results = {}
    for spec in strata_cfg:
        sid = spec["id"]
        cohort = eval_allen_fi_cohort(buckets.get(sid, []), offset_pa)
        strata_results[sid] = {
            "catalog_cells": len(buckets.get(sid, [])),
            **cohort,
        }

    held = eval_allen_fi_cohort(held_out, offset_pa)
    catalog_coverage = {
        "hero_specimen_excluded": hero_id,
        "classified_catalog_cells": sum(len(v) for v in buckets.values()),
        "unclassified_catalog_cells": len(unclassified),
        "held_out_catalog_cells": len(held_out),
    }
    return {
        "catalog_coverage": catalog_coverage,
        "held_out_fi_proxy": held,
        "strata": strata_results,
    }


def neurolab_bridge(registry: dict) -> dict:
    smiles = registry.get("smiles_lab", {})
    formula = registry.get("formula_corpus", {})
    kb = registry.get("knowledge_base", {})
    bio = registry.get("neurolab_bio", {})
    priors = bio.get("brain_component_priors", {})
    pathways = bio.get("brain_pathways", {})
    strict_n = (
        formula.get("records_total")
        or formula.get("records_strict_empirical")
        or kb.get("strict_empirical")
        or 0
    )
    return {
        "smiles_mapped_records": smiles.get("mapped_records", 0),
        "smiles_median_error_pct": (smiles.get("metadata") or {}).get("median_error_pct", 0),
        "strict_empirical_records": strict_n,
        "brain_component_priors_count": priors.get("count", 0),
        "neurolab_translation_total": bio.get("translation_total", 0),
        "neurolab_brain_pathway_count": pathways.get("count", 0) if isinstance(pathways, dict) else pathways,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Allen neuron cohort evaluation")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    cohort_root = Path(manifest["neuron_cohort_root"])
    hybrid_root = Path(manifest["hybrid_model_root"])
    cells_path = cohort_root / manifest["artifacts"]["cells_json"]
    cells = json.loads(cells_path.read_text(encoding="utf-8"))

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else {}
    hero_path = hybrid_root / manifest.get("hero_report", "inconsistency_rerun_report.json")

    cohort = eval_allen_fi_cohort(cells, manifest["fi_proxy"]["stim_offset_pa"])
    strata = eval_cohort_strata(cells, manifest)
    hero_certified = hero_certified_from_report(hero_path)
    hero_native = eval_hero_hybrid_fi(hybrid_root, hero_path, "native")
    hero_canon = eval_hero_hybrid_fi(hybrid_root, hero_path, "canonical")
    bridge = neurolab_bridge(registry)
    meta = bridge_metadata()

    certified_err = float((hero_certified or {}).get("mean_rel_err") or 1.0)
    canon_err = float((hero_canon or {}).get("mean_rel_err") or 1.0)
    canon_delta = abs(canon_err - certified_err)

    report = {
        "generated_from": str(cells_path),
        "total_cells_in_catalog": len(cells),
        "cohort_fi_proxy": cohort,
        "cohort_strata": strata,
        "hero_certified_fi": hero_certified,
        "hero_hybrid_native_scalar": hero_native,
        "hero_hybrid_canonical_scalar": hero_canon,
        "canonical_scalar_bridge": {
            **meta,
            "hero_canonical_mean_rel_err": canon_err,
            "hero_certified_mean_rel_err": certified_err,
            "canonical_vs_certified_delta": canon_delta,
            "within_few_points": canon_delta <= manifest["verification"].get("canonical_bridge_delta_max", 0.05),
        },
        "neurolab_smiles_bridge": bridge,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  cohort cells: {cohort['cell_count']}")
    print(f"  cohort FI median rel err: {cohort['fi_median_rel_err']:.4f}")
    print(f"  cohort FI pearson r: {cohort['fi_pearson_r']:.4f}")
    if hero_native:
        print(f"  hero native mean rel err: {hero_native['mean_rel_err']:.4f} ({hero_native.get('data_source')})")
    if hero_canon:
        print(f"  hero canonical mean rel err: {hero_canon['mean_rel_err']:.4f} (delta {canon_delta:.4f})")
    held = strata.get("held_out_fi_proxy", {})
    print(f"  held-out cells: {held.get('cell_count', 0)} median err {held.get('fi_median_rel_err', 0):.4f}")
    for sid, row in (strata.get("strata") or {}).items():
        print(f"  stratum {sid}: n={row.get('cell_count')} median={row.get('fi_median_rel_err', 0):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())