# Reverse / conjugate (C13) — claim → panel → kill command

**Purpose:** A skeptic who thinks “FSOT has no reverse world / antimatter / conjugate” should be able to **run machines**. This is the map.

**Pin:** **D1D38A** (`vendor/fsot_compute.py`)  
**Picture:** [`CONCEPTS.md`](CONCEPTS.md) **C13** · **C9** (yin–yang)  
**Ontology write-up:** [`MATTER_ANTIMATTER.md`](MATTER_ANTIMATTER.md)

This page is **not** a Sakharov uniqueness paper and **not** an afterlife catalog. It is the operational conjugate already residual-gated.

---

## What is already represented (do not re-invent)

| Claim (founding language) | Operational object | Live panel | n | Residual | Kill |
|---------------------------|--------------------|------------|--:|----------|------|
| Every emergence has a conjugate | \(\delta\psi\to\delta\psi+\pi\) on Particle \(D_{\mathrm{eff}}=5\) | `data/matter_antimatter_benchmark.json` | 27 | **0.0%** pooled | `conjugate_channel_not_equal_matter` must stay distinct |
| CPT mass equality | \(m=\bar m\) same fluid mode | same | e / p / μ rows | **0.0%** | computed equals PDG particle mass |
| Pair threshold \(2m\) | energy to open both duals | `ee_pair_threshold_MeV` · `ppbar_pair_threshold_MeV` | 2 | **0.0%** | \(2m_e=1.0219979\) MeV · \(2m_p=1876.544\) MeV |
| Why so little antimatter | \(\eta=\mathrm{POOF}^{11}/(\pi\gamma)\) | `eta_baryon_photon` | 1 | **6.13975×10⁻¹⁰ vs 6.14×10⁻¹⁰ (0.004%)** | Planck-class \(\eta\) |
| Matter density | \(\Omega_b h^2=\|S_{\mathrm{cosmo}}\|(1-S_{\mathrm{quant}})\) | `Omega_b_h2` | 1 | **0.022356 vs 0.02237 (0.062%)** | Planck 2018 class |
| Late universe damps bulk antimatter | cosmology \(S<0\) | `cosmology_damping_sign` · `bulk_antimatter_damped_flag` | 2 | **0.0%** | flags stay true |
| Matter preferred over conjugate | \(A=(S_m-S_{\mathrm{conj}})/(\|S_m\|+\|S_{\mathrm{conj}}\|)>0\) | `matter_over_conjugate_preference` | 1 | **0.0%** | preference stays positive |

Authority: PDG 2024 masses · Planck 2018 \(\eta\) / \(\Omega_b h^2\). Builder: `python scripts/build_matter_antimatter_benchmark.py`.

---

## One-command kill path

```powershell
python scripts/audit_parameter_count.py
python scripts/audit_all_benchmark_margins.py
```

Then open `data/matter_antimatter_benchmark.json` and confirm:

1. Domain `Matter_Antimatter` still reports pooled median **0.0%**.  
2. `eta_baryon_photon` is still **~6.14×10⁻¹⁰** (0.004%).  
3. CPT rows are identities (error **0.0%**), not fitted masses.  
4. You do **not** see a second free Lagrangian or a travelogue residual.

If (1)–(3) fail, the C13 *operational* claim is broken. File an issue with the command log and commit SHA.

---

## What stays interpretive (do not promote to residual)

| Founding picture | Why it is not a green-gate row |
|------------------|--------------------------------|
| Reverse world as a place you visit | Conjugate is a **phase flip**, not a destination. |
| Death = 4D decoherence, information not deleted | No public cemetery table. Soul-bridge stays a framework. |
| PFLT as a ticket to the other face | Linguistics panel is a different fold. |
| Full Sakharov path-integral uniqueness | Gap report already lists this as **open research**. |

---

## Related

- Consciousness (same skeptic shape): [`CONSCIOUSNESS_CLAIM_EVIDENCE.md`](CONSCIOUSNESS_CLAIM_EVIDENCE.md)  
- BH→WH valves: [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md)  
- Engine: `vendor/fsot_matter_antimatter.py`
