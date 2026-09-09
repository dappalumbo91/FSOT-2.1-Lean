# APPLY cookbook — Astronomy fold

**Pin:** D1D38A · **core:** `Astronomy` · \(D_{\mathrm{eff}}=20\) · `observed=True` · \(C=\pi^2/\varphi\) · \(\delta\psi=1\) · hits=1.  
**Neighbor:** `Planetary_Science` \(D=21\), \(\delta\psi=0.9\) (body zoom). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §31.  
**Same rung:** `Economics` \(\delta\psi=1.5\), hits=3 (market look). Fold onto \(D=19\).  
**H0 sectors:** Cosmology / Astrophysics — H0 is multi-variant expansion, not a siloed constant.  
**General protocol:** [`APPLY.md`](APPLY.md). JPL mean densities through APPLY — not identity-pad `computed=measured` planetary_structure rows.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Planetary mean density | JPL Horizons (APPLY dual-route) | Identity-pad `computed=measured` rows |
| Local ladder H0 | SH0ES chain 72.856 vs 73.04 (0.252%) | Class bin 73.773 as a 0.5% central |
| Perfect Host 73.49 | local Cepheid ladder / PRED-024 | PRED-001 bridge 70.75 |

Wrong object: \(\lvert S_{\mathrm{astro}}/S_{\mathrm{econ}}\rvert\) vs 1. Same \(D=20\); \(\delta\psi=1\) vs \(1.5\). Fold onto \(D=19\). JWST Perfect Host is the **ladder**, not the global bridge.

---

## 2. Pick the interface

Astronomy is the **sky** zoom. Planetary is the **body** zoom (equalize \(\delta\psi=1\)). Economics is the **market** look at the same rung. Cosmology is the **ceiling** of the same fluid — H0 depends on structures and bubbling, not a single constant.

ISO-SHOES-CLASS-BIN 1% stays **frozen**. Work the chain and the next published mixture. Do **not** retune \(\rho\).

---

## 3. Route

```text
S = domain_scalar("Astronomy")             # D=20, δψ=1, hits=1
computed, err% = fsot_scaled(rho, "Astronomy")
```

Body zoom, **equalize the astronomy look**:

```text
|S(D=20, δψ=1)| / |S(D=21, δψ=1)|  vs  1
```

Look-split vs market **folds onto \(D=19\)**:

```text
|S_astro|/|S_econ|  vs  S(D=19, δψ=1, hits=1)/S(D=19, δψ=1.5, hits=3)
```

| Handle | Form | Use |
|--------|------|-----|
| JPL density | APPLY on Astronomy and Planetary | not identity pad |
| Same-look rung | \(D=20/21\) at \(\delta\psi=1\) vs 1 | sky vs body |
| Sky vs market | look-split onto \(D=19\) | JPL + World Bank YoY |
| H0 sectors | tool \(H_0=H_{0,\mathrm{global}}(1+\rho\varepsilon)\) | chain 0.252%; class bin frozen |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. JPL dual-route and same-look \(D=20/21\) are the tight scalars. Live vs 1 stays **retired**. Perfect Host 73.49 is a **different named object** from PRED-001.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live vs Economics vs 1 | Fold 1.0/1.5 onto \(D=19\) | Stuff \(5/4\) onto this pair |
| 73.49 vs 70.75 | Wrong object (ladder vs bridge) | Kill PRED-001 |
| Class bin 1% | Frozen isolate; work the chain | Retune \(\rho\) 5.05→4.36 |
| Identity-pad densities | Route through APPLY | `computed=measured` as a residual |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing vs 1; retuning \(\rho\); scoring Perfect Host as PRED-001; rewriting frozen `sector_h0_seed.json`.
