# Engine Simulator

This folder contains a standard-engine simulator prototype to model engine performance, air/fuel ratio, ignition timing, and basic fuel consumption.

## Files

- `engine_specs.json` — initial engine specifications for a high-efficiency modern Atkinson engine and a lower-efficiency older V8.
- `fuel_profiles.json` — baseline gasoline and FSOT candidate fuel profiles with production routes, precursor costs, and emission/byproduct proxies.
- `REAL_DATA_PROVENANCE.md` — documented data grounding policy, sources, verification rules, and fuel profile provenance.
- `engine_simulator.py` — engine simulation logic and command-line interface with production cost, Monte Carlo, and exhaust chemistry proxy support.

## Usage

Run the engine simulator from the `Fuel Lab` workspace root:

```powershell
python engine_simulator\engine_simulator.py --list-engines
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine chevy_5_7l_v8_1990 --scan
python engine_simulator\engine_simulator.py --list-fuel-profiles
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_optimax --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --compare-fuels --fuel-profiles gasoline,fsot_optimax,fsot_bio_spark --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_bio_spark --monte-carlo --trials 20
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_hemp_eco_blend --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_waste_hemp_blend --monte-carlo --trials 20
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_hemp_waste_advanced --rpm 2200 --throttle 1.0 --afr 12.4 --spark-advance 19.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --sweep-hemp-advanced
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --refine-hemp-route
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_mushroom_spore_fuel --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_green_hydrogen --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --fuel-profile fsot_algae_oil_biodiesel --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --compare-fuels --fuel-profiles fsot_hemp_waste_advanced,fsot_mushroom_spore_fuel,fsot_green_hydrogen,fsot_algae_oil_biodiesel --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --blend-fuels --fuel-profiles fsot_hemp_waste_advanced,fsot_mushroom_spore_fuel,fsot_algae_oil_biodiesel --blend-weights 0.4,0.3,0.3 --rpm 2200 --throttle 1.0 --detailed
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --blend-sweep --fuel-profiles fsot_hemp_waste_advanced,fsot_algae_oil_biodiesel,fsot_green_hydrogen --blend-sweep-step 0.1 --blend-sweep-top 12 --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --compare-fuels --fuel-profiles fsot_hemp_waste_advanced,fsot_algae_oil_biodiesel --results-output engine_simulator\results\compare_20260526 --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --engine prius_1_8_atkinson --blend-sweep --fuel-profiles fsot_hemp_waste_advanced,fsot_algae_oil_biodiesel --blend-sweep-step 0.2 --blend-sweep-top 5 --results-output engine_simulator\results\blend_sweep_20260526 --rpm 2200 --throttle 1.0
python engine_simulator\engine_simulator.py --ground-fuel-profiles --fuel-profile-ids fsot_hemp_waste_advanced,fsot_algae_oil_biodiesel --grounded-output engine_simulator\results\grounded_fuel_profiles.json
python engine_simulator\engine_simulator.py --fetch-fuel-data --fuel-profile-ids fsot_mushroom_spore_fuel,fsot_green_hydrogen,fsot_algae_oil_biodiesel --save-fuel-data fuel_profile_compound_lookup.json

# Detailed output includes formaldehyde, benzene, PM2.5, VOC yield proxies, and the new FSOT score when `--detailed` is enabled.

## Plant-based exploration
- New hemp-derived FSOT candidates are included for lower-cost plant chemistry and lignocellulosic feedstock routes.
- These profiles test biomass-derived alcohol/ether/ester pathways and cost-reduction from hemp waste feedstocks.
- The advanced hemp route now includes an explicit extractor model with catalyst cycle cost, coproduct credit, biomass yield, conversion efficiency, and a renewable replacement rank.
- Findings are documented in `FUEL_FINDINGS.md`.
```

## Next step

Once the standard engine model is running, we can extend this into an FSOT conversion layer that maps the same simulation state into FSOT scalar math and fuel proxy variables.
