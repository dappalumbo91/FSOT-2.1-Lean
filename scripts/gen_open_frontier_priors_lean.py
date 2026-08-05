#!/usr/bin/env python3
"""Generate Lean *Priors.lean modules for open-science / frontier residual panels.

Same pattern as gen_tiers_68_70_lean.py. Numbers come only from green benchmark
JSON built with make_fsot_record / fsot_scaled (FSOT mathematics only).

Feeds export_full_priors_obligations.py → multi-prover spine.
Scientific catalog obligations also re-export all green domains from
benchmark_margin_audit.json via export_scientific_catalog_obligations.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

# (benchmark_file, lean_prefix, d_eff)
FRONTIER_BENCHES: list[tuple[str, str, int]] = [
    ("jarvis_dft_open_panel_benchmark.json", "jarvis_dft_open_panel", 16),
    ("cod_optimade_structures_benchmark.json", "cod_optimade_structures", 14),
    ("world_bank_macro_open_benchmark.json", "world_bank_macro_open", 18),
    ("nufit_neutrino_open_benchmark.json", "nufit_neutrino_open", 14),
    ("gwtc_catalog_open_benchmark.json", "gwtc_catalog_open", 18),
    ("nuclear_iaea_open_benchmark.json", "nuclear_iaea_open", 16),
    ("nist_asd_spectroscopy_open_benchmark.json", "nist_asd_spectroscopy_open", 12),
    ("owid_epidemiology_open_benchmark.json", "owid_epidemiology_open", 16),
    ("ncei_climate_open_benchmark.json", "ncei_climate_open", 14),
    ("lmfdb_oeis_math_open_benchmark.json", "lmfdb_oeis_math_open", 14),
    ("chembl_deep_open_benchmark.json", "chembl_deep_open", 14),
    ("exoplanet_archive_depth_open_benchmark.json", "exoplanet_archive_depth_open", 16),
    ("openneuro_depth_open_benchmark.json", "openneuro_depth_open", 14),
    ("desi_public_depth_open_benchmark.json", "desi_public_depth_open", 18),
    ("pdg_live_depth_open_benchmark.json", "pdg_live_depth_open", 14),
    ("gaia_dr3_source_sample_open_benchmark.json", "gaia_dr3_source_sample_open", 18),
    ("simbad_identity_depth_open_benchmark.json", "simbad_identity_depth_open", 16),
    ("lmfdb_elliptic_curves_open_benchmark.json", "lmfdb_elliptic_curves_open", 14),
    ("gwas_catalog_depth_open_benchmark.json", "gwas_catalog_depth_open", 14),
    ("pubchem_depth_open_benchmark.json", "pubchem_depth_open", 14),
    ("openalex_citation_depth_open_benchmark.json", "openalex_citation_depth_open", 12),
    ("uniprot_proteome_slice_open_benchmark.json", "uniprot_proteome_slice_open", 14),
    ("alphafold_batch_meta_open_benchmark.json", "alphafold_batch_meta_open", 14),
    ("rcsb_structure_batch_open_benchmark.json", "rcsb_structure_batch_open", 14),
    ("oeis_family_sweep_open_benchmark.json", "oeis_family_sweep_open", 14),
    ("usgs_seismic_history_open_benchmark.json", "usgs_seismic_history_open", 16),
    ("noaa_tides_multi_station_open_benchmark.json", "noaa_tides_multi_station_open", 16),
    ("gbif_taxon_depth_open_benchmark.json", "gbif_taxon_depth_open", 14),
    ("zenodo_records_depth_open_benchmark.json", "zenodo_records_depth_open", 12),
    # wave 3
    ("endf_iaea_nuclear_open_benchmark.json", "endf_iaea_nuclear_open", 16),
    ("nist_asd_multi_species_open_benchmark.json", "nist_asd_multi_species_open", 12),
    ("desi_edr_table_slice_open_benchmark.json", "desi_edr_table_slice_open", 18),
    ("gwosc_strain_metadata_open_benchmark.json", "gwosc_strain_metadata_open", 18),
    ("codata_full_table_open_benchmark.json", "codata_full_table_open", 12),
    ("desi_edr_fits_residual_benchmark.json", "desi_edr_fits_residual", 18),
]


def _to_module_stem(prefix: str) -> str:
    parts = prefix.split("_")
    return "".join(p[:1].upper() + p[1:] for p in parts if p) + "Priors"


def build_lean(prefix: str, module_stem: str, n: int, pooled: float, headline: float, d_eff: int) -> str:
    pooled_s = f"{pooled:.12g}"
    headline_s = f"{headline:.12g}"
    return f"""/-
  FSOT Formal {module_stem} — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled_s} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline_s} : ℝ)
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_D_eff = {d_eff} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · unfold {prefix}_D_eff; norm_num
  · exact {prefix}_pooled_median_under_half_pct

end
"""


def main() -> int:
    FORMAL.mkdir(parents=True, exist_ok=True)
    wrote = 0
    missing: list[str] = []
    for bench_name, prefix, d_eff in FRONTIER_BENCHES:
        path = DATA / bench_name
        if not path.exists():
            missing.append(bench_name)
            continue
        bench = json.loads(path.read_text(encoding="utf-8"))
        n = int(bench.get("observable_count") or bench.get("record_count") or 0)
        pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 99.0)
        headline = float(bench.get("headline_median_error_pct") or pooled)
        if pooled >= 0.5 or n <= 0:
            print(f"SKIP (not green): {bench_name} n={n} pooled={pooled}", file=sys.stderr)
            continue
        module_stem = _to_module_stem(prefix)
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(build_lean(prefix, module_stem, n, pooled, headline, d_eff), encoding="utf-8")
        wrote += 1
        print(f"Wrote {out.relative_to(ROOT)} n={n} pooled={pooled:.6g}%")

    if missing:
        print(f"Missing ({len(missing)}): {missing}", file=sys.stderr)
    print(f"Generated {wrote} Lean prior modules for open frontiers")
    return 0 if wrote else 1


if __name__ == "__main__":
    raise SystemExit(main())
