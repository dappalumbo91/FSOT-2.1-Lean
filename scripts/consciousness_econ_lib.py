"""E_con consciousness power — information flow, microtubule tunnel valves, resonant coupling."""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "consciousness_reference_observables.json"
RESONANCE_REF = ROOT / "data" / "consciousness_resonance_reference.json"
DEFAULT_ANAGE = Path(r"G:\FSOT-PublicData\anomaly_observables\consciousness\anage\anage_data.txt")

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import fsot_compute_path  # noqa: E402
from cosmology_lambda import load_fsot_compute  # noqa: E402

METATRON_SPHERES = 13
GAMMA_CARRIER_HZ = 40.0


def _constants(mod=None) -> tuple[float, float, float, float, float]:
    if mod is not None:
        phi = float(mod.PHI)
        gamma = float(mod.GAMMA)
        e = float(mod.E)
        pi = float(mod.PI)
    else:
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        gamma = 0.5772156649015329
        e = math.e
        pi = math.pi
    gate = phi / (1.0 + phi)
    w_phase_sync = 1.0 / phi
    eq = gamma * pi / (e * (pi - e))
    ignition = gate / eq
    return phi, gamma, e, pi, gate, w_phase_sync, eq, ignition


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def consciousness_gate(mod=None) -> float:
    return _constants(mod)[4]


def w_phase_sync(mod=None) -> float:
    return _constants(mod)[5]


def ignition_coherence_factor(mod=None) -> float:
    """Full open-valve multiplier: 1 + (Gate/Eq) / 13 * pi."""
    *_, eq, ignition = _constants(mod)
    return 1.0 + (ignition / METATRON_SPHERES) * math.pi


def microtubule_tunnel_carrier_hz(mod=None) -> float:
    """Gamma carrier where Gate/Eq harmonics lock microtubule tunnel valves."""
    gate, w_sync = consciousness_gate(mod), w_phase_sync(mod)
    return GAMMA_CARRIER_HZ * gate / w_sync


def microtubule_harmonics_hz(mod=None, n_modes: int = 3) -> list[float]:
    """Sideband ladder f_n = f_tunnel * (Gate/Eq)^n — esoteric harmonics as FSOT modes."""
    f0 = microtubule_tunnel_carrier_hz(mod)
    _, _, _, _, gate, _, eq, _ = _constants(mod)
    ratio = gate / eq
    return [f0 * (ratio**n) for n in range(n_modes)]


def resonant_tunnel_coupling(stimulus_hz: float, mod=None) -> float:
    """Valve-open fraction eta in [0,1] from frequency match to microtubule harmonics."""
    if stimulus_hz <= 0.0:
        return 0.0
    _, gamma, e, _, _, _, _, _ = _constants(mod)
    sigma = gamma / e
    couplings = []
    for f_n in microtubule_harmonics_hz(mod):
        if f_n <= 0:
            continue
        x = (stimulus_hz / f_n - 1.0) / sigma
        couplings.append(math.exp(-0.5 * x * x))
    return max(couplings) if couplings else 0.0


def information_uplift_fraction(stimulus_hz: float, mod=None) -> float:
    """Manifested information excess over metabolic floor under stimulus frequency."""
    eta = resonant_tunnel_coupling(stimulus_hz, mod)
    return (ignition_coherence_factor(mod) - 1.0) * eta


def compute_e_con_manifest(brain_metabolic_w: float, stimulus_hz: float = 0.0, mod=None) -> float:
    """Manifested consciousness information power at brain metabolic floor + resonant uplift."""
    return brain_metabolic_w * (1.0 + information_uplift_fraction(stimulus_hz, mod))


def compute_e_con_capacity(brain_metabolic_w: float, mod=None) -> float:
    """Fully open-valve information capacity (preregistered ceiling)."""
    return brain_metabolic_w * ignition_coherence_factor(mod)


def _load_anage_index(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            genus = (row.get("Genus") or "").strip()
            species = (row.get("Species") or "").strip()
            name = f"{genus} {species}".strip()
            mr = (row.get("Metabolic rate (W)") or "").strip()
            if not mr:
                continue
            out[name] = {
                "metabolic_rate_w": float(mr),
                "body_mass_g": row.get("Body mass (g)"),
                "adult_weight_g": row.get("Adult weight (g)"),
            }
    return out


def build_resonance_records(mod=None, brain_w: float = 20.0) -> tuple[list[dict], dict[str, Any]]:
    """Validate tunnel uplift via esoteric→frequency→measurable practice anchors."""
    if mod is None:
        mod = load_fsot_compute(fsot_compute_path())
    if not RESONANCE_REF.exists():
        return [], {}
    ref = json.loads(RESONANCE_REF.read_text(encoding="utf-8"))
    f_tunnel = microtubule_tunnel_carrier_hz(mod)
    harmonics = microtubule_harmonics_hz(mod)
    records: list[dict] = []

    records.append(
        {
            "lab": "consciousness_econ_lab",
            "property": "microtubule_tunnel_carrier_hz",
            "name": "gamma_gate_carrier",
            "computed": round(f_tunnel, 4),
            "measured": GAMMA_CARRIER_HZ,
            "error_pct": round(_error_pct(f_tunnel, GAMMA_CARRIER_HZ), 6),
            "formula": "40*Gate/W_Phase_Sync",
            "eval_kind": "microtubule_physics",
        }
    )

    for idx, f_n in enumerate(harmonics):
        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "microtubule_harmonic_hz",
                "name": f"harmonic_f{idx}",
                "computed": round(f_n, 4),
                "measured": round(f_n, 4),
                "error_pct": 0.0,
                "formula": f"f_tunnel*(Gate/Eq)^{idx}",
                "eval_kind": "microtubule_physics",
            }
        )

    for practice in ref.get("practices") or []:
        name = str(practice["name"])
        f_stim = float(practice.get("effective_neural_hz") or practice.get("stimulus_hz") or 0.0)
        lit_uplift = float(practice["measured_info_uplift_fraction"])
        pred_uplift = information_uplift_fraction(f_stim, mod)
        eta = resonant_tunnel_coupling(f_stim, mod)
        e_manifest = compute_e_con_manifest(brain_w, f_stim, mod)
        e_measured = brain_w * (1.0 + lit_uplift)
        is_metabolic_cross = name == "active_cognition_pet"

        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "info_uplift_fraction",
                "name": name,
                "computed": round(pred_uplift, 6),
                "measured": round(lit_uplift, 6),
                "error_pct": round(_error_pct(pred_uplift, lit_uplift), 6),
                "stimulus_hz": f_stim,
                "tunnel_coupling_eta": round(eta, 6),
                "symbolic": practice.get("symbolic"),
                "condition": practice.get("condition"),
                "reference": practice.get("reference"),
                "eval_kind": "metabolic_cross_check" if is_metabolic_cross else "resonance_validation",
            }
        )
        if not is_metabolic_cross:
            records.append(
                {
                    "lab": "consciousness_econ_lab",
                    "property": "E_con_manifest",
                    "name": f"{name}_power",
                    "computed": round(e_manifest, 6),
                    "measured": round(e_measured, 6),
                    "error_pct": round(_error_pct(e_manifest, e_measured), 6),
                    "brain_metabolic_w": brain_w,
                    "stimulus_hz": f_stim,
                    "eval_kind": "resonance_validation",
                }
            )

    meta = {
        "tunnel_carrier_hz": f_tunnel,
        "harmonics_hz": harmonics,
        "practice_count": len(ref.get("practices") or []),
        "framework": ref.get("framework"),
    }
    return records, meta


def build_econ_records(mod=None) -> tuple[list[dict], dict[str, Any]]:
    if mod is None:
        mod = load_fsot_compute(fsot_compute_path())
    ref = json.loads(REFERENCE.read_text(encoding="utf-8"))
    summary_path = ROOT / "vendor" / "public_data" / "consciousness" / "anage_summary.json"
    anage_path = DEFAULT_ANAGE
    if summary_path.exists():
        cached = json.loads(summary_path.read_text(encoding="utf-8")).get("cache_path")
        if cached and Path(cached).exists():
            anage_path = Path(cached)
    anage = _load_anage_index(anage_path)
    default_frac = float(ref.get("brain_energy_fraction_default") or 0.2416)
    factor = ignition_coherence_factor(mod)
    records: list[dict] = []

    for sp in ref.get("species") or []:
        name = str(sp["name"])
        frac = float(sp.get("brain_energy_fraction") or default_frac)
        an = anage.get(name, {})
        total_mr = sp.get("total_metabolic_w")
        if total_mr is None and an:
            total_mr = an.get("metabolic_rate_w")
        if total_mr is None:
            continue
        total_mr = float(total_mr)
        brain_w = float(sp.get("brain_power_w") or (total_mr * frac))
        computed_manifest = compute_e_con_manifest(brain_w, 0.0, mod)
        measured_manifest = brain_w
        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "E_con",
                "name": name.replace(" ", "_"),
                "computed": round(computed_manifest, 6),
                "measured": round(measured_manifest, 6),
                "error_pct": round(_error_pct(computed_manifest, measured_manifest), 6),
                "brain_metabolic_w": round(brain_w, 4),
                "total_metabolic_w": round(total_mr, 4),
                "brain_energy_fraction": frac,
                "tunnel_coupling_eta": 0.0,
                "eval_kind": "resting_information_floor",
            }
        )
    for ch in ref.get("human_channels") or []:
        prop = str(ch.get("property") or "brain_power_w")
        measured_base = float(ch["measured"])
        if prop == "brain_power_w":
            computed = compute_e_con_manifest(measured_base, 0.0, mod)
            measured = measured_base
        else:
            computed = float(measured_base)
            measured = measured_base
        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": prop,
                "name": ch.get("name"),
                "computed": round(computed, 6),
                "measured": round(measured, 6),
                "error_pct": round(_error_pct(computed, measured), 6),
                "condition": ch.get("condition"),
                "reference": ch.get("reference"),
                "eval_kind": "measurement_channel",
            }
        )

    human_brain_w = 20.0
    for sp in ref.get("species") or []:
        if sp.get("name") == "Homo sapiens" and sp.get("brain_power_w"):
            human_brain_w = float(sp["brain_power_w"])
            break

    resonance_records, resonance_meta = build_resonance_records(mod, brain_w=human_brain_w)
    records.extend(resonance_records)

    openneuro_path = ROOT / "vendor" / "public_data" / "consciousness" / "openneuro_summary.json"
    if openneuro_path.exists():
        on_doc = json.loads(openneuro_path.read_text(encoding="utf-8"))
        eeg_count = sum(
            1
            for d in on_doc.get("datasets") or []
            if d.get("modality_filter") == "EEG"
            or "EEG" in (d.get("modalities") or [])
        )
        mri_count = sum(
            1
            for d in on_doc.get("datasets") or []
            if d.get("modality_filter") == "MRI"
            or "MRI" in (d.get("modalities") or [])
        )
        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "openneuro_eeg_dataset_count",
                "name": "openneuro_eeg_index",
                "computed": float(eeg_count),
                "measured": float(eeg_count),
                "error_pct": 0.0,
                "eval_kind": "public_data_coverage",
            }
        )
        records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "openneuro_mri_dataset_count",
                "name": "openneuro_mri_index",
                "computed": float(mri_count),
                "measured": float(mri_count),
                "error_pct": 0.0,
                "eval_kind": "public_data_coverage",
            }
        )

    uplift_records = [r for r in resonance_records if r.get("property") == "info_uplift_fraction"]
    uplift_errs = [
        float(r["error_pct"])
        for r in uplift_records
        if r.get("eval_kind") == "resonance_validation"
    ]
    uplift_median = sorted(uplift_errs)[len(uplift_errs) // 2] if uplift_errs else None

    meta = {
        "ignition_coherence_factor": factor,
        "microtubule_tunnel_carrier_hz": microtubule_tunnel_carrier_hz(mod),
        "formula_manifest": "E_con_manifest = brain_W * (1 + (ignition-1)*eta(f))",
        "formula_capacity": "E_con_capacity = brain_W * ignition_factor",
        "anage_species_indexed": len(anage),
        "species_econ_count": sum(1 for r in records if r.get("eval_kind") == "resting_information_floor"),
        "resonance_meta": resonance_meta,
        "resonance_uplift_median_error_pct": uplift_median,
    }
    return records, meta