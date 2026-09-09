# Worked examples — how to apply FSOT (cells, chemistry, astronomy)

**Pin:** D1D38A · **Law:** \(\hat y = y\,(1+|S(\mathrm{domain})|\,f)\) · **Green:** domain **median** ≤ 0.5%

These are **broken-down** applications on public tables. Same protocol every time.
Full cookbooks: [`APPLY.md`](APPLY.md) · chemistry [`APPLY_CHEMISTRY.md`](APPLY_CHEMISTRY.md) ·
biology/cells [`APPLY_BIO.md`](APPLY_BIO.md) · sky [`APPLY_ASTRONOMY.md`](APPLY_ASTRONOMY.md).

Reproduce the numbers:

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from fsot_api_predict_lib import fsot_scaled, domain_scalar; print(domain_scalar('Chemistry')); print(fsot_scaled(18.015, 'Chemistry'))"
```

---

## Protocol (do not skip)

| Step | Do this | Do not |
|------|---------|--------|
| 1 | Name a **measured** \(m\) with a public table | Invent “measured × 0.999” |
| 2 | Pick the fold (\(D_{\mathrm{eff}}\), observed flag) | Invent a new \(D\) to fit one row |
| 3 | `computed, err% = fsot_scaled(m, domain)` | Least-squares a new \(f\) |
| 4 | Green if the **domain median** ≤ 0.5% | Call one pretty row the whole domain |
| 5 | If ugly: change the **interface** (wrong object or wrong fold) | Add a spring |

---

## 1. Chemical — CRC water (one specimen, three zooms)

**Table:** CRC / IUPAC. **Not:** a fitted Trouton constant or group-additivity \(B\).

| Measured object | Public value | Fold | Computed | err% |
|-----------------|-------------:|------|---------:|-----:|
| Molecular weight | 18.015 g/mol | Chemistry \(D=8\), \(\delta\psi=0.6\), observed | 18.0223 | **0.041%** |
| Melting \(T\) | 273.15 K | Physical_Chemistry \(D=8\), \(\delta\psi=0.5\), observed | 273.196 | **0.017%** |
| Boiling \(T\) | 373.15 K | Physical_Chemistry \(D=8\) | 373.212 | **0.017%** |

Source rows: `data/between_scale_interconnect_benchmark.json` (`water_mw`, `water_Tm`, `water_Tb`).

**What this shows:** composition vs thermo are two **looks** of the same rung, not two theories.
The 0.5 vs 0.6 split is the same grammar as Materials/Optics. Scoring optical \(n_D\) as MW
is a wrong object (route \(n\) on Optics). Scoring first ionization as MW is Atomic/HEP.

**Wrong apply:** \(\lvert S_{\mathrm{chem}}/S_{\mathrm{pc}}\rvert\) vs 1 (~22%) as a 0.5% kill.
That is law D9 (same-view), not a failed CRC residual.

```text
S = domain_scalar("Chemistry")
computed, err = fsot_scaled(18.015, "Chemistry")
```

---

## 2. Cells — human mitochondrial protein genes (NCBI)

**Table:** NCBI RefSeq **NC_012920.1** (human mtDNA). **Not:** a clock-time expression peak,
and **not** Genetics 0.13 Å (sibling product).

Biology is **dark** (`observed=False`, \(D=12\)). Do not flip the observer flag — looking at
the fold changes the object, same rule as QC Hilbert.

| Measured object | Public value | Fold | Computed | err% |
|-----------------|-------------:|------|---------:|-----:|
| MT-ND1 length | 956 bp | Biology \(D=12\), dark | 956 | **0.000%** |
| MT-ND2 length | 1044 bp | Biology | 1042 | **0.192%** |
| MT-CO1 length | 1542 bp | Biology | 1542 | **0.000%** |
| Protein-gene count | 13 | Biology | 13 | **0.000%** |
| Coding-bp sum | 11395 bp | Biology | 11394 | **0.009%** |

Source: `data/biology_strict_empirical.json` (strict median 0.0%).

**Wrong object (keep this one):** coding-bp vs **full** mt genome 16569 bp is **31%**.
That row is marked diagnostic / non-strict. It is **not** stuffed into 0.5%.
The cell’s protein operons are the object; the full circle (rRNA + tRNA + D-loop) is another.

Molecule zoom of the same life tissue is Biochemistry \(D=13\), `observed=True` (amino-acid MW
from CRC). Live mixed \(\lvert S_{\mathrm{bio}}/S_{\mathrm{bc}}\rvert\) vs 1 (~45%) is D9, not a kill.

Genetics product 0.13 Å vs AlphaFold 0.47 Å lives in
[FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics). Do not quote it as this NCBI panel.

```text
S = domain_scalar("Biology")          # dark
computed, err = fsot_scaled(956, "Biology")
```

---

## 3. Astronomical — JPL mean density and Planck \(H_0\)

### 3a. One planet, two zooms (sky vs body)

**Table:** JPL Horizons mean density (g/cm³). **Not:** identity-pad `computed = measured`.

| Body | JPL \(\rho\) | Astronomy \(D=20\) | err% | Planetary_Science \(D=21\) | err% |
|------|-------------:|-------------------:|-----:|---------------------------:|-----:|
| Mercury | 5.427 | 5.42822 | **0.022%** | 5.42825 | **0.023%** |
| Earth | 5.51 | 5.51124 | **0.022%** | 5.51127 | **0.023%** |
| Mars | 3.933 | 3.93388 | **0.022%** | 3.93391 | **0.023%** |

Source: `data/between_scale_interconnect_benchmark.json` (`Earth_rho_astro`, `Earth_rho_pl`, …).

Astronomy is the **sky** zoom. Planetary_Science is the **body** zoom.
The same catalog on the wrong \(D_{\mathrm{eff}}\) is how MPCORB eccentricity sat near **62%**
until Planetary_Science \(D=21\) brought the panel to **0.023%**. Interface, not a fitted \(\varepsilon\).

### 3b. \(H_0\) is sectors, not two cosmologies

| Named object | Measured | FSOT lock | err% | Not |
|--------------|---------:|-----------|-----:|-----|
| Planck 2018 TTTEEE+lowE+lensing | 67.4 km/s/Mpc | Planck-class sector 67.384 | **0.024%** | SH0ES 73.04 as the CMB kill |
| SH0ES R22 published | 73.04 | ladder **chain** 72.86 | **0.25%** | class bin 73.773 as a 0.5% central |
| JWST Perfect Host | 73.49±0.93 | PRED-024 hosts-only 73.80 | **0.42%** | PRED-001 bridge 70.75 |

Source: [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md). Law D1.

```text
S = domain_scalar("Astronomy")
computed, err = fsot_scaled(5.51, "Astronomy")
```

---

## What to copy into a new field (sibling text / simulation)

1. Pin **D1D38A**. Do not fork `vendor/fsot_compute.py`.
2. Name the public table (DOI / catalog ID).
3. Pick the fold from [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md) or
   `python scripts/query_fsot_domain_navigator.py --intent …`.
4. Show one **right object** and one **wrong object** (as above).
5. Green = domain median ≤ 0.5%. Ugly residual → change interface.
6. Product/simulation code can live in a sibling repo. The law stays here.

Coverage of what the engine already gates: [`COVERAGE_REFERENCE.md`](COVERAGE_REFERENCE.md) (477 files).
What we refuse or leave open: [`WHY_NOT_CLAIMED.md`](WHY_NOT_CLAIMED.md).
