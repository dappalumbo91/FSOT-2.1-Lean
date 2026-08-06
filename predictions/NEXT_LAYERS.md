# Next prediction layers (roadmap)

**Status:** WIP Theory-of-Everything *candidate* under frozen Label A/B checklists — **not** peer-reviewed closure. Math + multi-domain residual gates are the public evidence surface; social proof is separate.

**Discipline:** expand **Tier A** (survey/literature kills) and **Tier C** (lab/open catalogs) first. Grow Tier B only as regression. Keep Tier D labeled.

---

## 1. What you can look at *right now* (current status)

| Surface | Status (session snapshot) | What to do |
|---------|---------------------------|------------|
| Green gate | **472/472** · pin **D1D38A** | Baseline health — always re-check after engine work |
| Tier A hand PREDs | **16** core contested locks | Scoreboard for X + kills |
| Multi-tool H₀ | **25** instruments | Compare any new H₀ paper *to its tool row only* |
| SH0ES hosts | **22** sightline H₀ | New Cepheid/JWST host papers → per-host score |
| CCHP TRGB hosts | **22** intermediate H₀ | New Freedman/CCHP papers → per-host score |
| Atlas | **~1445** (472 residual + 885 scalar + …) | Breadth claim, not 1445 cosmology kills |
| Monitor watches | 14 active · 8 local green hold · 6 open predata | `python scripts/run_prediction_monitor.py` |
| **Nearest hard drop** | **Euclid DR1-Foundation · 12 Nov 2026** | Highest-priority calendar watch |

**Look at weekly (no freeze of development):**

1. Any new **local H₀ / TRGB / SH0ES / CCHP** paper → multi-tool + host tables  
2. **DESI / BAO / wₐ** papers → PRED-043 / PRED-046  
3. **LVK / GWOSC** alerts or catalog notes → PRED-048 + GWTC panel  
4. Full monitor: `python scripts/run_prediction_monitor.py --online`

---

## 2. Philosophy of the next layer

You already have:

- **Cosmology tension grammar** (bubble bleed → multi-tool + sightline H₀)  
- **Atlas regression** (same seeds, ≤0.5% everywhere green)  
- **Scaffold vault** (Tier D — do not lead)

The ToE *claim shape* is: **one seed fluid → many empirical sectors**.  
The next high-value predictions are therefore **cross-domain connections that are still falsifiable against open data you already ingest** — not more transporter scaffolds.

Priority order:

1. **Open catalogs you already run at scale** (MPCORB, Gaia, DESI, PubChem, GWTC, climate)  
2. **Particle / flavor residuals you already deep-panel** (CKM/PMNS, Higgs branching)  
3. **Multi-messenger bridges** (GW + EM + FRB already in bubble/FRB spine)  
4. **Materials / fuel / chemistry** as engineering-facing Tier C kills  
5. Only then speculative Tier D design predictions  

---

## 3. Recommended next layers (ranked)

### Layer 1 — **Catalog-native Tier A/C locks** (highest ROI)

You already hold huge residual-green catalogs. Turn **named observables** into PREDs with survey-style kills:

| Domain (already green) | Scale | Next prediction style |
|------------------------|------:|------------------------|
| **MPCORB** minor planets | ~1.5M rec | Orbital-element class residuals; near-Earth object subgroup holds; *not* one free ε per asteroid |
| **Gaia DR3** | thousands+ | Parallax / proper-motion class locks; distance-ladder adjacent astrometry |
| **DESI EDR** tables | ~97k | BAO / redshift-slice residual holds beyond single wₐ |
| **PubChem / CRC** | thousands | Property-class locks (logP, IE, bond energies) as open-chem Tier C |
| **GWTC / GWOSC** | catalogs | Event-rate class + chirp-mass ladder residual holds (not only “panel ≤0.5%”) |
| **NASA exoplanet archive** | ~2k | Radius–period–insolation architecture locks |
| **Climate / NCEI** | ~17k | Station-class residual holds under continuous refresh |

**Why this layer:** public data, already in the monorepo, multi-resource, granular — matches “empirically backed against real data.”

### Layer 2 — **Particle / nuclear precision spine** (ToE-facing, literature kills)

You already have `toe_ckm_pmns`, Higgs mass/branching, particle physics benchmarks.

| Prediction family | Kill surface |
|-------------------|--------------|
| CKM magnitudes / unitarity triangle residual class | PDG updates |
| PMNS angles residual class | neutrino global fits |
| Higgs branching pattern holds | ATLAS/CMS combinations |
| α_s(M_Z), electroweak ladder (if already in gr_sm) | PDG / lattice |

**Why:** classical ToE language expects flavor + mass structure, not only H₀.

### Layer 3 — **Multi-messenger / bubble-bleed bridges** (new *physics connections*)

This is the “new physics connections” layer that still stays on your existing spine:

| Bridge | Idea | Data you already touch |
|--------|------|-------------------------|
| **FRB DM × bubble density** | Sightline DM excess tracks same density grammar as H₀ sectors | CHIME / FRB panels |
| **GW standard sirens × H₀ sector** | Sparse sirens should land mid-sector (~70), not SH0ES-only | LVK / GWOSC |
| **Nebula outgassing × local H₀** | Already in cosmology bubble bleed | nebula + sector H₀ seeds |
| **Compact binaries × FSOT scalar** | Panel residuals as catalog grows | GWTC open |

**Why:** uses the *same* BH→WH bleed story across messengers — distinctive ToE signature, still scoreable.

### Layer 4 — **Stage-IV structure (calendar-bound Tier A)**

Already partially registered; deepen rather than invent:

- Euclid DR1-Foundation (Nov 2026) → imaging/catalog pathfinders  
- Euclid DR1 complete (mid-2027) → S₈ / clustering posteriors  
- Rubin EDP2 / early science → structure pathfinders  
- DESI joint BAO + w₀/wₐ  

### Layer 5 — **Earth / bio open streams** (Tier C, continuous)

| Stream | Prediction style |
|--------|------------------|
| Climate station cohorts | Holdout residual ceilings under refresh |
| Longevity / NCBI / immunology panels | Panel residual + named scalar locks |
| GBIF / species | Occurrence structure holds |

Good for “not only cosmology” narrative; lower single-drop drama than Euclid.

### Layer 6 — **Defer (Tier D vault)**

Cold-fusion scaffolds, superheavy Z islands, transporter, warp portal — keep registered, **do not expand as the public ToE scoreboard** until A–C are saturated.

---

## 4. Suggested build order (practical)

| Step | Deliverable | Effort |
|------|-------------|--------|
| **Now** | Weekly monitor + score any new H₀/TRGB/DESI/LVK paper vs Tier A | Low |
| **Next build** | `build_catalog_prediction_layer.py` — PREDs from MPCORB / Gaia / DESI / GWTC / PubChem top scalars with kills | Medium |
| **Then** | CKM/PMNS/Higgs **hand** PRED block (Tier A particle) from existing toe panels | Medium |
| **Then** | Multi-messenger bridge PREDs (FRB×density, siren×sector) | Medium |
| **Ongoing** | Euclid/Rubin watch only — no freeze of model work | Low |

---

## 5. Honest ToE framing (for X and docs)

**Allowed now**

- “Seed-locked multi-domain framework with preregistered kills and sub-percent residual gates on hundreds of open panels.”  
- “ToE *candidate* under our frozen Label A/B checklist (see `docs/TOE_CLAIM_BOUNDARIES.md`).”  
- “Math + empirical ledger; peer review still open.”

**Not allowed**

- “Proven ToE / peer-reviewed finished.”  
- Leading with Tier D as if equal to Euclid H₀ locks.  
- Treating 1445 atlas rows as 1445 independent cosmology discoveries.

Math doesn’t “finish social science” — it **locks claims that can fail**. That is the position of strength.

---

## 6. Commands

```powershell
python scripts/run_prediction_monitor.py --online
python scripts/rank_nearest_data_drops.py
python scripts/build_prediction_tiers.py
# After next layer ships:
# python scripts/build_catalog_prediction_layer.py   # (to implement)
```
