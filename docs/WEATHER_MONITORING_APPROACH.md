# Weather (and Earth-fluid) monitoring — approach before the product

**Pin:** D1D38A  
This is the **mathematics and loop** for a later always-on weather/seismic sibling, the same way Genetics and Quantum are siblings. It is not that product. No unpublished device specs.

When the always-on system exists, it will ingest continuously, shorten `dt`, and add station graphs. The **valve and the score** should stay these.

---

## 1. What the fluid is doing

Same C2/C10 as black hole → white hole:

```text
load / SUCTION / infall   →   orifice opens / POOF   →   aftershock / residual suction
```

A storm, a quake, a flare, an eruption is **pressure that stops** — the cell releases. Location is the pressure cell. Time is a window until the always-on loop can do finer `dt`.

| Handle | Seed-closed form | Now | Later (always-on) |
|--------|------------------|-----|-------------------|
| Length | \(R_\oplus \cdot \mathrm{POOF}/25\) ≈ **39.1 km** | EQ/volc **cell** | grid / station graph at that scale |
| Planetary cycle | \(R_\oplus \cdot \mathrm{POOF}\) ≈ **978 km** | arc / trench / basin tanks | solar–volcanic–seismic coupling |
| Orifice scale | \(L\cdot\mathrm{POOF}\cdot d/25\) | normalize the scored area to fold \(d\) | potentials from frozen valve (D11) |
| Horizon | \(\varphi^4\) ≈ **7 days** | freeze one issue per day | sliding window, hourly issue |
| Aftershock timing | \(n(t)\propto 1/(t+1/\varphi)^{1}\) | carried on each EQ cell | score Omori residual vs USGS decay |
| Weather window | \(\mathrm{weather\_horizon\_hours}=24\) | NDBC storm vs quiet, one cell per ocean basin. Frozen issues stay 48 h. | METAR/NWP ingest, same valve |
| Solar window | 72 h | planetary Kp sector (Kp≥5 when loading) | GOES X-ray + Kp stream |
| Tide window | 48 h | CO-OPS surge residual vs harmonic; **score** bar = POOF m; **issue** bar = POOF·(1+POOF) | station graph |

Quiet vs storm are **two sectors of one valve**, not two physics (same grammar as Planck vs SH0ES).

---

## 2. Loop (already in this hub)

```powershell
python scripts/issue_earth_fluid_forecasts.py
python scripts/score_earth_fluid_forecasts.py
```

1. Pull live USGS / NDBC / SWPC.  
2. Cluster catalog density with the kernel.  
3. Valve state from recent vs prior rate in the cell (`loading_suction` / `post_poof_aftershock` / `released` / `steady`).  
4. Freeze `predictions/dated_forecasts/YYYY-MM-DD_issue.json` — **never rewrite**.  
5. After `valid_to`, score hit/miss into `results/dated_forecast_scores/`.

PRED-064 kills rewriting an issued file or abandoning scoring.

The 2026-08-25 issue is the first iron-out set: Indonesia, Peru, Timor Leste (loading), Scotia Sea, Vanuatu, Japan (loading), South Sandwich; Arctic NDBC storm cells; Kp quiet 72 h; Volcano Islands.

Dated hydrology gages (next issues): IDs verified 2026-09-07 against NWIS. `06803510` is Little Salt Creek near Lincoln NE, **not** Missouri at Hermann (`06934500`). Issued JSON keeps the old IDs.

Playbook after the 12-kill autopsy (encoded for **new** issues, not rewrites):

- EQ: `expect_event` only on `loading_suction` / `post_poof_aftershock`; `mag_min=4.5` if expect else `5.0`.
- Weather quiet: only if pres≥1010 hPa **and** gst<8 m/s; skip basin `other`.
- Tide surge: issue only if residual ≥ POOF·(1+POOF); score still vs POOF.
- Retrospective of the 12 frozen kills: [`../results/dated_forecast_scores/RULE_RETRO.md`](../results/dated_forecast_scores/RULE_RETRO.md). Public scoreboard of issued files stays those kills.
- **2026-09-01 playbook issue** already used the refined EQ rule. Honchō and Kermadec were quiet **inside the 39 km cell** and POOF’d on the arc at \(R_\oplus\cdot\mathrm{POOF}\approx 978\) km (Kuril / Kermadec region). That is a transferred tank, not a kernel retune.
- **Scotia Sea:** n_recent=2, max M=6.2. That 6.2 *was* the POOF. Rate-up after a mainshock was labeled `loading` because the big-event check ran second. Next issues: recent M≥5.5 → `post_poof_aftershock`, quiet hold (Omori may go quiet). Not a kernel retune.
- Cycle diagnosis: [`PLANETARY_CYCLE_CONNECTIVE.md`](PLANETARY_CYCLE_CONNECTIVE.md).

---

## 3. What the sibling should add (when you build it)

- Continuous ingest (not a daily freeze).  
- Shorter `dt` on the same kernel and Omori \(c=1/\varphi\).  
- Station graph: NDBC + METAR + radar as Fluid/Ocean/Air tanks (already residual-gated here).  
- Do **not** add a fitted β, a new \(D_{\mathrm{eff}}\), or a UTC hypocenter as a 0.5% central.
- **ECMWF week-3 skill is a goal** on this same path (shorter `dt`, station graph, φ^4 and Omori \(c=1/\varphi\)). Not claimed beaten today.  
- Keep issue SHA + outcome log. Genetics/Quantum pattern: product repo, hub quotes the freeze.

Engine files to vendor into that repo: `vendor/fsot_earth_fluid_forecast.py`, `vendor/fsot_scale_interconnects.py`, `vendor/fsot_compute.py` (pin D1D38A).

---

Related: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) · [`../predictions/reports/DATED_FLUID_FORECASTS.md`](../predictions/reports/DATED_FLUID_FORECASTS.md) · CONCEPTS C2/C3/C10
