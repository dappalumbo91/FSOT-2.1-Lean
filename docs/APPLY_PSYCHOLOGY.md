# APPLY cookbook — Psychology (psychometric fold)

**Pin:** D1D38A · **core:** `Psychology` · \(D_{\mathrm{eff}}=16\) · `observed=True` · \(\delta\psi=1.15\).  
**Neighbors:** Fluid / Nuclear / Thermo \(D=15\); Meteorology \(D=16\), dark; Atmospheric / Ocean \(D=17\), dark; Ecology \(D=15\), dark.  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §37.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Cronbach \(\alpha\) typical | Nunnally 1978 convention (0.85) | Invented brain watts |
| Test–retest \(r\) | literature psychometric anchor (0.80) | OpenAlex citation counts |
| Cohen's \(d\) small/medium/large | Cohen 1988 (0.2 / 0.5 / 0.8) | Formula-corpus identity pads (pH, bond angles) |
| Median RT / Stroop interference | psychometrics RCT anchors (250 ms / 100 ms) | Consciousness 20 W (that is Neuroscience) |

Source in-repo: `data/psychology_psychometrics_depth_panel_benchmark.json`, `ingest_source = psychometrics_rct_literature_anchors`. Dual-route the **measured** column through APPLY.

---

## 2. Pick the interface

Psychology is the **psychometric scale** zoom (observer string on). Dark neighbors stay dark. Do **not** invent watts. Do **not** use OpenAlex `cited_by_count` as a psychology residual (wrong object: bibliography).

---

## 3. Route

```text
S = domain_scalar("Psychology")            # D=16, observed
computed, err% = fsot_scaled(m, "Psychology")
```
