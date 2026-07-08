#!/usr/bin/env python3
"""Generate Lean priors for all Tier 38 public API extension domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402
from tier38_public_data_lib import BUILDERS, TIER38_DOMAINS  # noqa: E402

TIER38_LEAN = {
    "NIST_CODATA_Constants": ("nist_codata_constants", "particle", "particle_raw_S_positive", "NistCodataConstantsPriors"),
    "GBIF_Species_Occurrence": ("gbif_species_occurrence", "biological", "biological_raw_S_positive", "GbifSpeciesOccurrencePriors"),
    "NOAA_Coastal_Tides": ("noaa_coastal_tides", "energy", "energy_raw_S_positive", "NoaaCoastalTidesPriors"),
    "World_Bank_Development": ("world_bank_development", "consciousness", "consciousness_raw_S_positive", "WorldBankDevelopmentPriors"),
    "NASA_Exoplanet_Archive": ("nasa_exoplanet_archive", "astronomical", "astronomical_raw_S_positive", "NasaExoplanetArchivePriors"),
    "RCSB_PDB_Structures": ("rcsb_pdb_structures", "medical", "medical_raw_S_positive", "RcsbPdbStructuresPriors"),
    "OpenAlex_Citation_Graph": ("openalex_citation_graph", "consciousness", "consciousness_raw_S_positive", "OpenalexCitationGraphPriors"),
    "PubChem_Compound_Properties": ("pubchem_compound_properties", "electron", "electron_raw_S_positive", "PubchemCompoundPropertiesPriors"),
    "CERN_Open_Data_LHC": ("cern_open_data_lhc", "particle", "particle_raw_S_positive", "CernOpenDataLhcPriors"),
    "UniProt_Protein_Annotations": ("uniprot_protein_annotations", "biological", "biological_raw_S_positive", "UniprotProteinAnnotationsPriors"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=TIER38_DOMAINS, action="append")
    args = parser.parse_args()
    domains = args.only or TIER38_DOMAINS
    for domain in domains:
        bench_name, _ = BUILDERS[domain]
        bench = json.loads((ROOT / "data" / bench_name).read_text(encoding="utf-8"))
        prefix, lean_domain, sign_th, module_stem = TIER38_LEAN[domain]
        text = extension_priors_lean(
            module_title=f"FSOT Formal {module_stem} — Tier 38 public API ({domain}).",
            generator="scripts/gen_tier38_public_data_lean.py",
            prefix=prefix,
            sign_theorem=sign_th,
            lean_domain=lean_domain,
            n=int(bench.get("record_count") or 0),
            med=float(bench.get("median_error_pct") or 0.0),
            d_eff=int(bench.get("D_eff", 12)),
        )
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())