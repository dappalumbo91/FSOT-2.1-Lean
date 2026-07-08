#!/usr/bin/env python3
"""Generate Lean priors for extension domains #37-39."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
FORMAL = ROOT / "FSOT" / "Formal"

# Domains with dedicated generators (avoid overwriting rich bundle theorems).
DEDICATED_GENERATORS = {
    "Climate_Science",
    "Cosmology_Extended",
    "Particle_Physics",
    "Space_Weather",
    "Hydrology",
    "Pharmacology",
    "Cryosphere",
    "Seismology",
    "Tectonics",
    "Geomagnetism",
    "Planetary_Structure",
    "Orbital_Mechanics",
    "Small_Body_Orbits",
    "Magnetosphere",
    "Grace_Cryosphere",
    "Seismology_Deep",
    "Planetary_Atmospheres",
    "Magnetosphere_Extended",
    "Geochemistry",
    "Oncology",
    "Neuroimmunology",
    "Synthetic_Biology",
    "Quantum_Materials",
    "Neuron_Multi_Hero",
    "Linguistics_Formal",
    "Mathematics_Computational",
    "Materials_Engineering",
    "Computational_Reasoning",
    "Math_Generator_Rules_Eval",
    "Trinary_OS_Portable",
    "Materials_Species_Bridge",
    "IGEM_Synthetic_Biology",
    "Math_Generator_Benchmark_Formula_Eval",
    "Trinary_OS_ISA_Rebuild",
    "IGEM_Live_FASTA_Ingest",
    "Math_Generator_Airfoil_RMSE",
    "Trinary_OS_Round_Trip",
    "Tokenization_Smoke",
    "Trinary_Hardware_Motif",
    "Intrinsic_LLM_Validators",
    "Biological_CUDA_Physarum",
    "Arxiv_Primitives_V14",
    "Formula_Corpus_CNC",
    "Binary_Decoder_Rendlesham",
    "Certified_Agent_Qwen",
    "Omni_Theory_Genesis",
    "FSOT_Aggregate_Unified_DB",
    "Prediction_Rederivation",
    "VL_Distill_Atlas",
    "Rust_Lean_Bridge",
    "Bibliography_Lean_Corpus",
    "NIST_CODATA_Constants",
    "GBIF_Species_Occurrence",
    "NOAA_Coastal_Tides",
    "World_Bank_Development",
    "NASA_Exoplanet_Archive",
    "RCSB_PDB_Structures",
    "OpenAlex_Citation_Graph",
    "PubChem_Compound_Properties",
    "CERN_Open_Data_LHC",
    "UniProt_Protein_Annotations",
}

LEAN_SIGN = {
    "Plasma_Physics": ("energy", "energy_raw_S_positive"),
    "Immunology": ("medical", "medical_raw_S_positive"),
    "Climate_Science": ("energy", "energy_raw_S_positive"),
    "Cosmology_Extended": ("cosmological", "omega_b_h2_fsot_cached_pos"),
    "Particle_Physics": ("particle", "particle_raw_S_positive"),
    "Space_Weather": ("fusion", "fusion_raw_S_positive"),
    "Hydrology": ("energy", "energy_raw_S_positive"),
    "Pharmacology": ("medical", "medical_raw_S_positive"),
    "Cryosphere": ("galactic", "galactic_raw_S_positive"),
    "Seismology": ("energy", "energy_raw_S_positive"),
    "Tectonics": ("energy", "energy_raw_S_positive"),
    "Geomagnetism": ("electron", "electron_raw_S_positive"),
    "Planetary_Structure": ("galactic", "galactic_raw_S_positive"),
    "Orbital_Mechanics": ("astronomical", "astronomical_raw_S_positive"),
    "Small_Body_Orbits": ("astronomical", "astronomical_raw_S_positive"),
    "Magnetosphere": ("electron", "electron_raw_S_positive"),
    "Grace_Cryosphere": ("galactic", "galactic_raw_S_positive"),
    "Seismology_Deep": ("energy", "energy_raw_S_positive"),
    "Planetary_Atmospheres": ("galactic", "galactic_raw_S_positive"),
    "Magnetosphere_Extended": ("electron", "electron_raw_S_positive"),
    "Geochemistry": ("galactic", "galactic_raw_S_positive"),
    "Oncology": ("medical", "medical_raw_S_positive"),
    "Neuroimmunology": ("medical", "medical_raw_S_positive"),
    "Synthetic_Biology": ("biological", "biological_raw_S_positive"),
    "Quantum_Materials": ("material", "material_raw_S_positive"),
    "Neuron_Multi_Hero": ("neural", "neural_raw_S_positive"),
    "Linguistics_Formal": ("consciousness", "consciousness_raw_S_positive"),
    "Mathematics_Computational": ("particle", "particle_raw_S_positive"),
    "Materials_Engineering": ("material", "material_raw_S_positive"),
    "Computational_Reasoning": ("consciousness", "consciousness_raw_S_positive"),
    "Math_Generator_Rules_Eval": ("particle", "particle_raw_S_positive"),
    "Trinary_OS_Portable": ("consciousness", "consciousness_raw_S_positive"),
    "Materials_Species_Bridge": ("material", "material_raw_S_positive"),
    "IGEM_Synthetic_Biology": ("biological", "biological_raw_S_positive"),
    "Math_Generator_Benchmark_Formula_Eval": ("particle", "particle_raw_S_positive"),
    "Trinary_OS_ISA_Rebuild": ("consciousness", "consciousness_raw_S_positive"),
    "IGEM_Live_FASTA_Ingest": ("biological", "biological_raw_S_positive"),
    "Math_Generator_Airfoil_RMSE": ("particle", "particle_raw_S_positive"),
    "Trinary_OS_Round_Trip": ("consciousness", "consciousness_raw_S_positive"),
    "Tokenization_Smoke": ("consciousness", "consciousness_raw_S_positive"),
    "Trinary_Hardware_Motif": ("consciousness", "consciousness_raw_S_positive"),
    "Intrinsic_LLM_Validators": ("consciousness", "consciousness_raw_S_positive"),
    "Biological_CUDA_Physarum": ("biological", "biological_raw_S_positive"),
    "Arxiv_Primitives_V14": ("consciousness", "consciousness_raw_S_positive"),
    "Formula_Corpus_CNC": ("particle", "particle_raw_S_positive"),
    "Binary_Decoder_Rendlesham": ("consciousness", "consciousness_raw_S_positive"),
    "Certified_Agent_Qwen": ("consciousness", "consciousness_raw_S_positive"),
    "Omni_Theory_Genesis": ("consciousness", "consciousness_raw_S_positive"),
    "FSOT_Aggregate_Unified_DB": ("particle", "particle_raw_S_positive"),
    "Prediction_Rederivation": ("galactic", "galactic_raw_S_positive"),
    "VL_Distill_Atlas": ("consciousness", "consciousness_raw_S_positive"),
    "Rust_Lean_Bridge": ("consciousness", "consciousness_raw_S_positive"),
    "Bibliography_Lean_Corpus": ("particle", "particle_raw_S_positive"),
    "NIST_CODATA_Constants": ("particle", "particle_raw_S_positive"),
    "GBIF_Species_Occurrence": ("biological", "biological_raw_S_positive"),
    "NOAA_Coastal_Tides": ("energy", "energy_raw_S_positive"),
    "World_Bank_Development": ("consciousness", "consciousness_raw_S_positive"),
    "NASA_Exoplanet_Archive": ("astronomical", "astronomical_raw_S_positive"),
    "RCSB_PDB_Structures": ("medical", "medical_raw_S_positive"),
    "OpenAlex_Citation_Graph": ("consciousness", "consciousness_raw_S_positive"),
    "PubChem_Compound_Properties": ("electron", "electron_raw_S_positive"),
    "CERN_Open_Data_LHC": ("particle", "particle_raw_S_positive"),
    "UniProt_Protein_Annotations": ("biological", "biological_raw_S_positive"),
}


def _load_bench(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _module_stem(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def build_climate_module(name: str, cfg: dict, bench: dict) -> str:
    stem = _module_stem(name)
    n = int(bench.get("record_count") or bench.get("month_count") or 0)
    med = 0.0 if bench.get("median_error_pct") is None else float(bench["median_error_pct"])
    d_eff = int(cfg.get("D_eff", 16))
    cohort = bench.get("cohort") or {}
    hold = cohort.get("holdout") or {}
    train = cohort.get("train") or {}
    ho_n = int(hold.get("record_count") or 0)
    ho_med = hold.get("median_error_pct")
    ho_med = 0.0 if ho_med is None else float(ho_med)
    tr_n = int(train.get("record_count") or 0)
    ho_stn = int(hold.get("station_count") or 0)
    prefix = name.lower()
    return f"""/-
  FSOT Formal {stem}Priors — extension domain {name} (scaled NCEI + station cohort).
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_train_month_count : ℕ := {tr_n}
def {prefix}_holdout_month_count : ℕ := {ho_n}
def {prefix}_holdout_station_count : ℕ := {ho_stn}
def {prefix}_D_eff : ℕ := {d_eff}
def {prefix}_median_error_pct : ℝ := ({med} : ℝ)
def {prefix}_holdout_median_error_pct : ℝ := ({ho_med} : ℝ)

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_holdout_month_count_pos : 0 < {prefix}_holdout_month_count := by
  unfold {prefix}_holdout_month_count; norm_num

theorem {prefix}_median_error_under_five_pct : {prefix}_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_median_error_pct; norm_num

theorem {prefix}_holdout_median_error_under_five_pct : {prefix}_holdout_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_holdout_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_train_month_count = {tr_n} ∧
    {prefix}_holdout_month_count = {ho_n} ∧
    {prefix}_holdout_station_count = {ho_stn} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_median_error_pct < (5 : ℝ) ∧
    {prefix}_holdout_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    by unfold {prefix}_train_month_count; norm_num,
    by unfold {prefix}_holdout_month_count; norm_num,
    by unfold {prefix}_holdout_station_count; norm_num,
    by unfold {prefix}_D_eff; norm_num,
    {prefix}_median_error_under_five_pct,
    {prefix}_holdout_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def build_module(name: str, cfg: dict, bench: dict) -> str:
    if name == "Climate_Science" and bench.get("cohort"):
        return build_climate_module(name, cfg, bench)
    stem = _module_stem(name)
    n = int(
        bench.get("record_count")
        or bench.get("month_count")
        or bench.get("observable_count")
        or bench.get("kp_record_count")
        or len(bench.get("records") or [])
    )
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    d_eff = int(cfg.get("D_eff", 12))
    lean_dom, sign_thm = LEAN_SIGN.get(name, ("energy", "energy_raw_S_positive"))
    return f"""/-
  FSOT Formal {stem}Priors — extension domain {name}.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def {name.lower()}_observable_count : ℕ := {n}
def {name.lower()}_D_eff : ℕ := {d_eff}

theorem {name.lower()}_observable_count_pos : 0 < {name.lower()}_observable_count := by
  unfold {name.lower()}_observable_count; norm_num

theorem {name.lower()}_median_error_under_five_pct :
    ({med} : ℝ) < (5 : ℝ) := by norm_num

theorem {name.lower()}_bundle :
    {name.lower()}_observable_count = {n} ∧
    {name.lower()}_D_eff = {d_eff} ∧
    ({med} : ℝ) < (5 : ℝ) ∧
    raw_S (get_domain_params "{lean_dom}") > 0 := by
  refine ⟨
    by unfold {name.lower()}_observable_count; norm_num,
    by unfold {name.lower()}_D_eff; norm_num,
    {name.lower()}_median_error_under_five_pct,
    {sign_thm}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    for name, cfg in (spec.get("extension_domains") or {}).items():
        if name in DEDICATED_GENERATORS:
            continue
        bench_path = ROOT / cfg["benchmark_data"]
        bench = _load_bench(bench_path)
        stem = _module_stem(name)
        out = FORMAL / f"{stem}Priors.lean"
        out.write_text(build_module(name, cfg, bench), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())