#!/usr/bin/env python3
"""Host + pathogen two-system smoke (public lengths). Not a person diagnosis.

Product freeze lives in FSOT-Genetics. This hub smoke shows the coupling:
  S_host  = Biology (dark)
  S_path  = Biochemistry (molecule zoom; Immunology is an extension of this core)
  κ_ij    = R7 bleed
  process time at D=12 and D=13

Public NCBI objects (documented accessions, no key):
  Host: human mt MT-ND1 956 bp  NC_012920.1
  Pathogen: SARS-CoV-2 spike CDS 3822 bp  NC_045512.2

Kill: person-level onset as a 0.5% central. Kill: flipping Biology observed.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import domain_scalar, fsot_scaled  # noqa: E402
from fsot_earth_fluid_forecast import (  # noqa: E402
    kappa_named,
    process_ceiling_days,
    process_time_days,
    valve_split,
)

OUT = ROOT / "data" / "sickness_two_system_smoke.json"

# Public NCBI RefSeq lengths (coding sequence). Not a fitted codon table.
HOSTS = [
    {
        "name": "MT-ND1",
        "accession": "NC_012920.1",
        "measured_bp": 956,
        "domain": "Biology",
        "source": "NCBI RefSeq human mitochondrial genome",
    },
    {
        "name": "MT-CO1",
        "accession": "NC_012920.1",
        "measured_bp": 1542,
        "domain": "Biology",
        "source": "NCBI RefSeq human mitochondrial genome",
    },
    {
        "name": "MT-ND2",
        "accession": "NC_012920.1",
        "measured_bp": 1044,
        "domain": "Biology",
        "source": "NCBI RefSeq human mitochondrial genome",
    },
]
PATHOGENS = [
    {
        "name": "S_spike_CDS",
        "accession": "NC_045512.2",
        "measured_bp": 3822,
        "domain": "Biochemistry",
        "source": "NCBI RefSeq SARS-CoV-2 Wuhan-Hu-1 spike CDS",
    },
    {
        "name": "N_nucleocapsid_CDS",
        "accession": "NC_045512.2",
        "measured_bp": 1260,
        "domain": "Biochemistry",
        "source": "NCBI RefSeq SARS-CoV-2 Wuhan-Hu-1 nucleocapsid CDS",
    },
]


def _score(row: dict) -> dict:
    c, e = fsot_scaled(row["measured_bp"], row["domain"])
    return {**row, "computed_bp": c, "error_pct": e, "S": domain_scalar(row["domain"])}


def main() -> int:
    hosts = [_score(h) for h in HOSTS]
    paths = [_score(p) for p in PATHOGENS]
    kap = kappa_named("Biology", "Biochemistry")
    p_fire, p_hold = valve_split()
    tau0 = process_ceiling_days()
    host_med = sorted(h["error_pct"] for h in hosts)[len(hosts) // 2]
    path_med = sorted(p["error_pct"] for p in paths)[len(paths) // 2]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "product": "FSOT-Genetics (sibling). Hub smoke only.",
        "host": hosts[0],
        "pathogen": paths[0],
        "hosts": hosts,
        "pathogens": paths,
        "host_median_error_pct": host_med,
        "pathogen_median_error_pct": path_med,
        "kappa_host_pathogen": kap,
        "poof_hold": p_fire,
        "suction_hold": p_hold,
        "process_time_days_host_d12": process_time_days(tau0, 12.0),
        "process_time_days_path_d13": process_time_days(tau0, 13.0),
        "emergence_note": (
            "Two systems on one pin. Coupling is κ, not a new ε. "
            "Class residuals already live (epidemiology panel 0.015%). "
            "Person-level onset needs a Genetics product freeze on public "
            "pathogen+host structure — this smoke is the coupling."
        ),
        "kill": "Individual diagnosis/onset as a 0.5% central. Flip Biology observed.",
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        f"host_med {host_med:.4f}%  path_med {path_med:.4f}%  n_h={len(hosts)} n_p={len(paths)} "
        f"kappa={kap:.6f}  tau_h={payload['process_time_days_host_d12']:.3f}d "
        f"tau_p={payload['process_time_days_path_d13']:.3f}d"
    )
    if host_med > 0.5 or path_med > 0.5:
        print("FAIL: length residual > 0.5% on a public CDS", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
