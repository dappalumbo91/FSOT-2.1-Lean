# FSOT predictions — explained through the model

**Author:** Damian Arthur Palumbo  
**Repo:** [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) · folder `predictions/`  
**Engine pin:** D1D38A · **zero free parameters**  
**Purpose of this page:** Explain *what* we predict and *why the model says that* — not just dump JSON.

If you only want copy-paste posts for X → [`public/X_READY.md`](public/X_READY.md).  
If you want a one-screen summary → [`public/ONE_PAGER.md`](public/ONE_PAGER.md).

---

## 1. What FSOT is (one breath)

FSOT treats spacetime as one **fluid medium**. Matter, expansion, chemistry, life, and measurement are patterns in that fluid — not separate patchwork theories glued together.

The math starts from five **seed** numbers only (π, e, φ, γ, G). No “knob” is added to rescue a bad prediction. One scalar engine is run across hundreds of scientific domains; a domain is **green** when residual error stays under **0.5%**. Live scoreboard: `docs/CURRENT_STATUS.md`.

**Predictions** are statements frozen in Git *before* or *independent of* the next public data drop. When the drop comes, we score them. We do **not** rewrite the old prediction to look right after the fact.

---

## 2. Why “prediction” here is different from curve-fitting

| Curve-fit habit | FSOT discipline |
|-----------------|-----------------|
| Add a parameter when data disagree | Zero free parameters (pin D1D38A) |
| One “best” H₀ for all instruments | **Many** H₀s — one per measurement *sector* |
| Hide misses | Kill criteria + Git timestamp |
| Only cosmology | Atlas across bio, materials, particle, earth, social, engineering… |

Machine files (YAML/JSON) are the ledger. **This document is the story.**

---

## 2b. Prediction tiers (read this before the big numbers)

The list is **intentionally large**. That only stays honest if tiers stay separate:

| Tier | Name | Lead on X? | What it is |
|------|------|:----------:|------------|
| **A** | Contested / public survey | **Yes** | H₀ multi-tool + hosts + TRGB, S₈, wₐ, N_eff, m_H, Euclid/DESI/Rubin locks — kill criteria vs literature |
| **B** | Empirical atlas | Breadth only | ~472 residual-holds + ~885 scalar locks — “same seeds stay ≤0.5%” |
| **C** | Grounded lab / engineering | Support | Fuel lab, materials, climate, code-genome, zebrafish… |
| **D** | Scaffold / high-speculation | **No** (label if mentioned) | Cold-fusion scaffolds, superheavy islands, transporter stack, warp portal scalars |

**Public rule:** Lead with **Tier A**. Cite **Tier B** as multi-domain strength, not as 1400 separate cosmology kills. Never lead with **Tier D** without saying *exploratory scaffold*.

Full split: [`reports/PREDICTION_TIERS.md`](reports/PREDICTION_TIERS.md) · X blurb: [`public/TIERS_FOR_X.md`](public/TIERS_FOR_X.md)

---

## 3. The heart of the contested sky: black hole ↔ white hole bubble bleed

### The problem everyone sees

Different tools report different expansion rates (Hubble constant H₀):

- Early-universe (CMB / Planck-class): often ~**67–68** km/s/Mpc  
- Local Cepheid ladders (SH0ES-class): often ~**73**  
- TRGB / Carnegie-class: often ~**70**  

People call this the “Hubble tension” and treat it like two cosmologies fighting.

### What FSOT says instead

There is **not** one number that every instrument is “supposed” to see.

Black hole → white hole dynamics push and bleed information through the fluid. Expanding nebulae, sightlines, and how a tool couples to that flow **change which sector of the expansion field you are reading**.

So:

- CMB rulers read a **depleted / early-sector** density  
- Local Cepheid hosts sit in **inflated local-bubble** sectors  
- TRGB ladders sit **in between**  

Same fluid. Different **bubble-density sector**. Different legitimate readout.

### The formula (plain language)

1. Global FSOT background:  
   `H0_global ≈ 68.44` km/s/Mpc  
   (from the seed engine + acoustic bleed terms)

2. Each tool has a **density model** for its sector:  
   `H0_tool = H0_global × (1 + density_model × bleed_fraction)`  
   with `bleed_fraction ≈ 0.015431`

3. **Kill rule:** when that tool’s next published central moves more than the registered band away from the frozen FSOT number, that *tool’s* prediction fails — **not** every other tool.

### What we already locked

| Layer | Count | Idea |
|-------|------:|------|
| Multi-tool H₀ | **25** instruments/methods | Planck, ACT, SPT, DESI BAO, Carnegie TRGB, Freedman JWST, SH0ES, masers, TF, … |
| SH0ES sightlines | **22** host galaxies | Each Cepheid host has its own RA-sector density → own H₀ |
| CCHP TRGB hosts | **22** galaxies | Intermediate ladder; milder density than Cepheids |
| FSOT span (tools) | **~67.4 – 75.1** | Matches the real literature spread *without* inventing two universes |

Tables: `reports/H0_MULTI_TOOL_PREDICTIONS.md`, `H0_SIGHTLINE_PREDICTIONS.md`, `CCHP_TRGB_SIGHTLINE_PREDICTIONS.md`.

**X takeaway:**  
> FSOT doesn’t pick SH0ES *or* Planck. It predicts **both** — and the galaxies between them — because bubble bleed makes the sky sector-dependent.

---

## 4. Beyond the sky: the multi-domain prediction atlas

The model is not a cosmology hobby. The same seed engine is residual-gated on **472** green domain panels. The atlas turns that into **predictions**:

| Kind | Count (approx.) | What it means in English |
|------|----------------:|--------------------------|
| **Residual hold** | 472 | “This whole domain stays ≤0.5% error on refresh.” |
| **Scalar lock** | ~885 | “This specific computed vs measured observable stays on the seed readout.” |
| **Sector portfolio** | 9 | “The whole bio / materials / particle / … *sector* stays green.” |
| **H₀ layers** | 25+22+22+… | Multi-tool + hosts + TRGB as above |
| **Total atlas** | **~1445** | Machine scoreboard in `domain_prediction_atlas.json` |

### Sectors (not only cosmology)

| Sector | Why it matters |
|--------|----------------|
| **bio_med** | Immunology, genomics, zebrafish, pharmacology, species panels |
| **particle_nuclear** | Higgs, CKM, CERN open data, nuclear scales |
| **materials_chem** | CRC, PubChem, fuels, acoustics |
| **earth_climate** | Climate stations, geochemistry, cryosphere |
| **social_econ** | World Bank, finance-style panels |
| **engineering_compute** | Hardware, code genome, trinary OS |
| **astro_gw** | GWOSC, exoplanets, MPCORB, FRB class |
| **cosmology** | H₀, S₈, wₐ, DESI, Euclid watches |

**X takeaway:**  
> If the theory only worked on Hubble, that would be a red flag. The atlas is hundreds of domains under the **same** seeds.

---

## 5. Contested “hard problems” with kill criteria

Separate from residual holds, FSOT registers **falsifiable** locks on open problems science already argues about:

- H₀ bridge scalar (~**70.75**) between Planck and SH0ES  
- S₈ effective lensing (~**0.805**) between Planck and DES  
- Dark-energy evolution **wₐ** (~**−1.018**) vs ΛCDM’s default 0  
- N_eff (~**3.046**), m_H (~**125.25** GeV), FRB DM excess class, lithium factor, …

Each has a **kill string**: what would count as failure when the next survey posts.

Hand list: `preregistered_predictions_manifest.yaml`  
Living watches: `prediction_monitor_registry.yaml`  
Human tables: `reports/PREDICTION_MONITOR.md`

---

## 6. What to watch *next* (time order)

Development **does not freeze** while we wait. Git timestamps already timestamp the claims.

| When | Event | FSOT link |
|------|--------|-----------|
| **12 Nov 2026** (hard date) | **Euclid DR1-Foundation** | S₈ / structure / catalog path (PRED-042 class); full WL later mid-2027 |
| Oct–Dec 2026 | Rubin LSST EDP2 complete | Early structure pathfinder |
| Continuous | DESI, JWST/CCHP/SH0ES papers, CHIME | Can score any week |
| mid-2027 | Euclid DR1 complete | Strongest S₈ / clustering test |

Ranker: `reports/NEAREST_DATA_DROPS.md`  
Policy: `docs/PREDICTION_MONITORING_POLICY.md`

**X takeaway:**  
> Next hard calendar test on the public schedule: **Euclid DR1-Foundation, 12 Nov 2026**. The predictions are already in GitHub with timestamps.

---

## 7. How a claim is checked (skeptic path)

1. Open the commit that contains the prediction (GitHub history).  
2. Read the number + kill criterion in `predictions/`.  
3. When the survey publishes, compare.  
4. Log hold / kill — **do not** edit the old predicted central.  
5. Optional full stack: green gate 472/472, multiprover `overall_ok`, pin D1D38A.

Quick kit: `docs/SKEPTIC_REPLICATION_KIT.md` · `docs/INDEPENDENT_REPRODUCTION.md`

---

## 8. Honest boundaries (post this too)

**Allowed**

- Multi-domain residual-gated framework under a fixed pin  
- Multi-tool and per-host H₀ under bubble-bleed structure  
- Preregistered kills for surveys  

**Not allowed (and we don’t claim)**

- “Peer review finished”  
- “Every contested problem is socially closed”  
- “One H₀ number for all instruments forever”  
- Silent retuning after a drop  

WIP model: wrong residual on a future gate is information. A registered **kill** is a real ledger event.

---

## 9. File map (human vs machine)

| For humans | For machines |
|------------|----------------|
| This file (`EXPLAINED.md`) | `domain_prediction_atlas.json` |
| `public/X_READY.md` | `h0_*_predictions.json` |
| `public/ONE_PAGER.md` | `preregistered_predictions_manifest.yaml` |
| `reports/*.md` | `toe_prereg_freeze.json` |
| `docs/FSOT_EXPLAINED_LAYMAN.md` | `prediction_monitor_report.json` |

Bulk raw catalogs (TRGB host lists, etc.): **external drive** `G:/FSOT-PublicData/` — see `external_data_pointers.json`.

---

## 10. One sentence you can stand on

**FSOT predicts from one seed fluid: many instruments, many domains, many sightlines — scored by residual gates and time-stamped kills, not by rewriting the past.**
