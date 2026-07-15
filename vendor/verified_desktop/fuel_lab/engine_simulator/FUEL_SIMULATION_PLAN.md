# Fuel Simulation Plan

## Current baseline fuel

The current engine simulator is using a standard gasoline-equivalent baseline.

- `engine_specs.json` defines `fuel_type: "gasoline"` for the Prius and V8 specs.
- `engine_simulator.py` maps fuel type to energy content using:
  - gasoline: `44,000 kJ/kg`
  - diesel: `42,500 kJ/kg`
  - ethanol: `30,000 kJ/kg`
- The simulation is therefore a regular gasoline-style baseline, not the new FSOT-designed fuel.

## What this means

- The Prius profile we ran is a gasoline-equivalent engine case.
- The power/efficiency numbers are computed against a conventional fuel energy density.
- That is the proper baseline for comparison to gasoline performance.

## Goal

Find an alternative fuel that:

1. is equal to or better than gasoline in performance and power output
2. is more fuel efficient
3. is cleaner and lower-hazard
4. can be compared side-by-side under the same engine load conditions

## Next steps

1. Add a `FuelSpec`/fuel profile layer to the simulator.
   - include FSOT candidate fuel properties
   - include LHV, stoich AFR, emissions proxy, clean index, flame speed proxy
2. Add a second engine or second fuel-case run for the same engine geometry.
   - run `gasoline` baseline and `FSOT fuel` side-by-side
   - compare brake power, thermal efficiency, fuel flow, BSFC, and clean indices
3. Add a parallel simulation mode.
   - spawn multiple engine/fuel combinations under the same conditions
   - isolate each engine by fuel and air/fuel mixture
   - compute a Monte Carlo sweep over AFR, spark timing, throttle, and RPM
4. Add engine-stress/failure proxies.
   - detect overly lean/rich mixtures
   - identify spark timing offsets that reduce efficiency or break assumptions
   - flag conditions that are likely to damage the engine

## Use of existing FSOT reference

The folder `C:\Users\damia\Desktop\FSOT_Machine_And_Molecule` is a strong source for this work.

- It includes a chemical/SMILES simulator and embedded species catalog.
- It already encodes FSOT-derived formulas for chemical properties and fluid behavior.
- We can use that data to build a cleaner, FSOT-driven fuel profile:
  - fuel species thermodynamics
  - flammability and hazard class
  - diffusion and heat-transfer proxies
  - clean combustion metrics

## How to run the baseline now

```powershell
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --scan
```

## Proposed file changes

- new `FuelSpec` dataclass in `engine_simulator.py`
- fuel profiles in `engine_specs.json` or a new `fuel_profiles.json`
- a `--compare` or `--parallel` mode that evaluates multiple fuel cases together
- a Monte Carlo mode for AFR / timing / throttle exploration
