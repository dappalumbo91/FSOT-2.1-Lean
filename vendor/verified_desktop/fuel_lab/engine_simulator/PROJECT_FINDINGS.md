# Engine Simulator Project Findings

## Review summary

This project now supports an FSOT-oriented bench engine simulator with:

- A full CLI-driven simulation engine in `engine_simulator.py`.
- Fuel profile definitions and economic/emissions metadata in `fuel_profiles.json`.
- Baseline gasoline and multiple FSOT candidate fuels, including hemp, mushroom, hydrogen, and algal remediation concepts.
- Detailed simulation outputs for brake power, thermal efficiency, BSFC, emissions proxies, cost, and remediation credit.
- Blend support for arbitrary weighted mixes of fuel profiles.
- Automated blend-sweep search to find optimal weight combinations over candidate fuel sets.
- Compound lookup support via PubChem/NIST lookup overrides for real ground-truth chemistry.
- Documentation in `REAL_DATA_PROVENANCE.md`, `README.md`, and planning notes in `FUEL_SIMULATION_PLAN.md`.

## What we have now

### Core assets

- `engine_simulator/engine_simulator.py`
  - `FuelSpec` and `EngineSpec` dataclasses
  - combustion and bench-performance model
  - fuel production economics and exhaust proxies
  - blend generation and blend sweep
  - Monte Carlo and compare-fuels modes
  - `--fetch-fuel-data` real compound lookup support

- `engine_simulator/fuel_profiles.json`
  - Baseline `gasoline`
  - FSOT fuels: `fsot_optimax`, `fsot_bio_spark`, `fsot_hemp_eco_blend`, `fsot_waste_hemp_blend`, `fsot_hemp_waste_advanced`
  - New candidate routes: `fsot_mushroom_spore_fuel`, `fsot_green_hydrogen`, `fsot_algae_oil_biodiesel`

- `engine_simulator/README.md`
  - CLI usage examples including the new `--blend-sweep` mode.

- `engine_simulator/FUEL_FINDINGS.md`
  - existing project summary and hypothesis tracking.

- `engine_simulator/FUEL_SIMULATION_PLAN.md`
  - baseline simulation plan and longer-term goals.

### Verified capabilities

- Baseline engine comparison across fuels
- Detailed bench metrics including coolant/oil, friction, and net power
- Renewable score ranking across fuels
- Blend evaluation with component-by-component comparison
- Blend-sweep search returning top candidates
- Hemp-heavy, mushroom, hydrogen, and algae remediation routes modeled
- Remediation credit incorporated into fuel economics

## Most promising directions

### 1. Validate and ground fuel parameters with real data

- Map key fuel profile fields to actual species and measured properties.
- Use real chemical/thermo data for: LHV, stoich AFR, density, volatility, and emissions proxies.
- Confirm or revise production costs, catalyst costs, and coproduct credits using available supplier/data sources.

### 2. Refine route-specific production modeling

- Make each route a true production pathway instead of a simple weighted blend.
- Add explicit biomass/precursor mass balance for hemp, mushroom, algae, and hydrogen.
- Model remediation credit separately from fuel economics, with a dedicated credit/penalty term.
- Add yield and loss factors for multistage conversion and product recovery.

### 3. Strengthen the FSOT evaluation framework

- Add an FSOT-aligned scoring metric that maps fuel variables into a theory-based replacement score.
- Capture FSOT observables like renewable leverage, emissions reduction, and fuel conversion efficiency in a composite index.
- Use the engine model outputs to feed a small FSOT scalar layer rather than only raw proxies.

### 4. Expand blend optimization and search

- Add smarter optimizers beyond pure grid sweep (e.g. adaptive search, local refinement, Pareto frontier).
- Track blend tradeoffs between cost, emissions, renewable fraction, and remediation benefit.
- Support constrained blends (minimum renewable content, maximum hydrogen share, etc.).

### 5. Add richer validation and reporting

- Record best candidate fuels and blend results in a single evolving findings document.
- Add a concise `best-candidates` table for each run/experiment.
- Store sweep results to JSON or CSV so results can be compared over time.

## Recommended immediate next step

1. Lock in the current candidate set and run a full comparison across:
   - `fsot_hemp_waste_advanced`
   - `fsot_algae_oil_biodiesel`
   - `fsot_mushroom_spore_fuel`
   - `fsot_green_hydrogen`
   - `fsot_optimax`
   - `gasoline`

2. Run `--blend-sweep` for the top renewable candidates and capture the top 5 blends.

3. Update fuel profiles with either real compound data or tighter proxy assumptions for each route.

4. Add a `best_candidates` section to this findings document after each major experiment.

## Short-term project roadmap

- [ ] Confirm candidate fuel parameters from published fuel chemistry sources.
- [ ] Add explicit route/yield modeling for hemp waste and algae remediation.
- [ ] Build a Pareto optimizer for blend tradeoffs.
- [x] Add a results logger so we can compare experiments across days.
- [x] Ground fuel profiles from measured compound properties.
- [x] Create a documented real data provenance policy to prevent mistaken assumptions about data grounding.
- [ ] Add a lightweight FSOT metric layer for final ranking.

## Latest experiment results

### Candidate comparison (Prius 1.8L at 2200 RPM, full throttle)

| Fuel profile | FSOT score | Renewable rank | Cost ($/kWh) | Toxicity index | Renewable fraction |
|---|---|---|---|---|---|
| `fsot_hemp_waste_advanced` | 0.783 | 0.842 | 0.27 | 0.167 | 0.99 |
| `fsot_algae_oil_biodiesel` | 0.718 | 0.823 | 0.58 | 0.206 | 0.96 |
| `fsot_green_hydrogen` | 0.552 | 0.771 | 0.69 | 0.053 | 0.99 |
| `fsot_mushroom_spore_fuel` | 0.671 | 0.757 | 0.56 | 0.218 | 0.97 |

### Blend sweep summary

- The new `--blend-sweep` system now evaluates candidate blends across a grid of weight combinations, ranking by FSOT score and exposing a Pareto frontier.
- The highest FSOT-scored blend is currently the pure `fsot_hemp_waste_advanced` route.
- The Pareto frontier contains 11 non-dominated candidates, showing a tradeoff between low cost / high FSOT score and lower toxicity through hydrogen shares.
- Early frontier points show a smooth transition from hemp-dominant cost efficiency to hydrogen-enriched low-toxicity blends.

### Findings to track

- `fsot_hemp_waste_advanced` remains the strongest overall route in this current proxy model.
- `fsot_hemp_waste_grounded` is the first fully grounded hemp route and shows the real-data-derived result: lower LHV, higher cost, and higher emissions than the original route assumptions.
- `fsot_algae_oil_biodiesel` is the strongest remediation route, but cost and toxicity still lag hemp.
- `fsot_green_hydrogen` is the cleanest route by toxicity, but it carries a cost penalty.
- `fsot_mushroom_spore_fuel` is a useful intermediate route for future low-cost fungal chemistry optimization.

## Notes

- The current simulator is strong on route exploration and high-level comparison, but still relies on proxy numbers rather than fully calibrated chemistry.
- The blend/sweep feature is a powerful capability; it should now be used for systematic candidate selection rather than ad hoc mixes.
- The most valuable path is to keep this grounded in measurable fuel/production data while using FSOT as the comparison framework.
