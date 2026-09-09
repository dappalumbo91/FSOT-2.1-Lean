# Sickness two-system — host + pathogen (public data)

**Pin:** D1D38A · **Product:** [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics) · **Hub:** coupling smoke

Person-level onset is **not** a 0.5% central today. The work is to couple two
systems on the same pin with **public structure**, then iron the outcome in
Genetics.

---

## Two systems, one fluid

| System | Fold | Public object (this smoke) |
|--------|------|----------------------------|
| Host | Biology \(D=12\), **dark** | NCBI `NC_012920.1` MT-ND1 **956 bp** |
| Pathogen | Biochemistry \(D=13\), observed | NCBI `NC_045512.2` spike CDS **3822 bp** |
| Coupling | \(\kappa_{ij}\) (R7) | Biology ↔ Biochemistry |
| Time | D12 process time | \(d=12\) host tick, \(d=13\) pathogen tick |

Do **not** flip Biology `observed`. Looking at the host fold changes the object.

Class residuals already gated: epidemiology panel **0.015%** (PRED-069). That is
the *wave class*, not a city outbreak date and not “this person gets sick on Tuesday.”

---

## What “getting the data” means

Open, no key (policy: [`OPEN_SCIENCE_ONLY_POLICY.md`](OPEN_SCIENCE_ONLY_POLICY.md)):

| Need | Source |
|------|--------|
| Host gene / protein lengths | NCBI RefSeq (already used for mt operons) |
| Pathogen CDS / protein | NCBI viral RefSeq (spike, HA, NA, …) |
| Population class rates | World Bank / WHO health indicators (already in epidemiology panel) |
| Structure product | Genetics freeze — homologs, not sequence-only AF |

Clinical EHR and named-patient onset stay **out of band** (credentials). The
two-system sim uses public genomes + class rates.

---

## How the sim emerges

1. `S_host = domain_scalar("Biology")`, `S_path = domain_scalar("Biochemistry")`.
2. \(\kappa = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_h||S_p|/(1+|D_h-D_p|/25)\).
3. Valve split \(\mathrm{POOF}/(\mathrm{POOF}+\mathrm{SUCTION})\) — fire vs hold.
4. Process windows at \(d=12\) and \(d=13\) (not a UTC onset stamp).
5. Genetics product: structure of host receptor vs pathogen protein (Å objects
   stay sibling-owned; do not quote 0.13 Å as sequence-only).

Smoke: `python scripts/smoke_sickness_two_system.py` → `data/sickness_two_system_smoke.json`

Kill: individual diagnosis as a 0.5% central. Kill: mixing cryo-EM FSC Å with
the product. Kill: flipping Biology dark.
