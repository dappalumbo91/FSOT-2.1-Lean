# FRB as BH→WH orifice outgassing

**Pin:** D1D38A · **panel:** `data/frb_orifice_outgassing_benchmark.json`  
**Refresh:** `python scripts/ingest_frb_repeaters.py` then `python scripts/build_frb_orifice_benchmark.py`  
**Dump:** CHIME/FRB Catalog 2 (Jia+2026 Zenodo) merged onto the literature seed — **3390** sources. Do not 0.5%-gate the 10-row seed or this dump.

The HVAC / fixed-orifice picture (CONCEPTS C2): mass falls in, compactifies and heats, then the orifice opens (POOF) and the other side outgasses cold. That puncture through the fluid **is** the fast radio burst.

| Picture | Engine |
|---------|--------|
| Fixed-orifice tube | POOF / SUCTION valve |
| Saloon doors flop-flop-flop then rest | Repeater = post-POOF (enough energy to keep the doors moving) |
| Rock through a sheet of paper | One-shot = single rip (not enough energy to repeat) |
| Energy / density / velocity of the outgassing | Puncture energy \(E = w_{\mathrm{ms}}\times F_{\mathrm{Jy\,ms}}\) vs \(e\cdot\mathrm{POOF}\) |
| How long the doors keep flopping before rest | Activity season \(T = D_{\mathrm{particle}}\cdot\pi + 1/\varphi\) days |

**Not** local sky density. That kernel is the H0 angular crowding grammar (PRED-076). It does not set DM excess and it does not decide repeater vs rip.

## What is gated

| Handle | Form | Live |
|--------|------|------|
| Repeater vs rip | \(E \ge e\cdot\mathrm{POOF}\) | **278/293** (94.9%, YELLOW). Catalog 2 dump **3390** sources; width missing on most Cat-2 rows so those are not scored. **Not** a 0.5% gate. |
| Pulse-width class | median repeater / one-shot vs Particle \(D_{\mathrm{eff}}=5\) | **5.0 vs 5 (0%)** |
| Short saloon-door tick | P34 = 1000 s (1 mHz) | 4 periods, 0–2%, **2.5% contested band** (not stuffed into 0.5%) |
| Activity season | \(T = 5\pi + 1/\varphi\) days (Particle orifice cycle + Omori \(c\) rest) | FRB20180916B **16.35 d** vs **16.326 d (0.147%)** |

\(\varphi^6\) days is compactification count — **wrong object** (9.75% vs 16.35 d; ~8.9% vs \(\varphi^6\)). \(2\pi\varphi^2\) days is **0.61%**, over the gate. Neither is stuffed.

## Remedied — not an open isolate

`200\cdot(1+\mathrm{local\_sky\_density})` on DM excess was **66%**, wrong object (IGM path). That formula is **retired** (`REMEDIED_WRONG_APPLY`). Autopsy: [`FRB_INTERFACE_DIAGNOSIS.md`](FRB_INTERFACE_DIAGNOSIS.md). Ledger: [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) remedied table. Do not keep 66% on the open isolate list. Do not reuse the formula.

PRED-052 keeps the 200 pc cm⁻³ **class**. PRED-084 is the orifice. PRED-076 is angular grammar only.

Kill: putting DM back into \(E\); stuffing 66% into 0.5%; fitting a new threshold; retuning POOF; 0.5%-gating \(\varphi^6\) or \(2\pi\varphi^2\).
