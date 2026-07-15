# Engine Simulator Fuel Findings

## Goal
Find a gasoline substitute that is:
- more cost-effective
- easier to produce
- more naturally renewable
- lower emissions
- efficient in power delivery

## Current state
- `engine_simulator.py` now models bench engine performance, fuel combustion quality, and detailed exhaust proxies.
- Fuel profiles use explicit production-route economics, including precursor cost, process energy, overhead, catalyst cost, and coproduct credits.
- Plant-based hemp fuels are now modeled as renewable routes with biomass yield and conversion efficiency.

## Fuel profiles
- `gasoline`: fossil baseline, high emissions, no renewable credit.
- `fsot_optimax`: high-energy FSOT gasoline replacement with moderate renewable intermediates.
- `fsot_bio_spark`: bio-derived intermediate fuel with higher renewable share but high production cost.
- `fsot_hemp_eco_blend`: hemp-based alcohol/ether blend targeted for cleaner combustion and lower cost.
- `fsot_waste_hemp_blend`: hemp waste-derived lignocellulosic fuel optimized for cost.
- `fsot_hemp_waste_advanced`: advanced hemp-waste route with explicit extractor metrics and tuned ether/ester balance.
- `fsot_algae_oil_biodiesel`: an aquatic bloom remediation fuel concept that turns harmful algal biomass into renewable biodiesel and recovery credit.

## Advanced hemp route tuning
- A parameter sweep has been added to explore ether/ester ratio, waste-syrup vs performance cofactors, and catalyst cost / coproduct credit sensitivity.
- Additional renewable fuel candidates were added for future exploration: `fsot_mushroom_spore_fuel` and `fsot_green_hydrogen`.
- Increased waste-syrup share and lowered green ether fraction.
- Raised ester booster contribution relative to performance cofactors.
- Reduced catalyst cost and rallied coproduct credit.
- Improved process energy assumptions and overall cost.

## Key findings so far
- The advanced hemp route now has the strongest renewable fraction and a low fuel cost per kWh.
- It also produces much lower CO/NOx/soot/VOC emissions compared to gasoline.
- Explicit metrics now show:
  - `renewable_fraction`
  - `biomass_yield_kg_fuel_per_kg_biomass`
  - `conversion_efficiency`
  - `catalyst_cycle_cost_per_kg`
  - `coproduct_credit_per_kg`
- The simulator also computes a single `renewable replacement rank` for comparing fuels.
- The latest sweep shows the best advanced hemp variant is near the low-ether, moderate-ester range, with a cost below $0.30/kWh and a rank above 0.91.

## Safety note: cannabis-derived fuel emissions
- The fuel is modeled from hemp waste and biomass feedstock, not psychoactive cannabis flower.
- Combustion in an engine breaks down THC and plant cannabinoids into combustion products.
- The exhaust byproducts are chemical pollutants (CO, NOx, soot, aldehydes, formaldehyde, benzene, VOCs, PM2.5), not intoxicating cannabinoids.
- Therefore the fuel is not expected to make people high from normal exhaust exposure.
- The real safety concern is conventional exhaust toxicity and particulate inhalation, not psychoactive effect.

## Next steps
- Continue tuning the advanced hemp route by exploring:
  - lower green ether / higher ester balance
  - more waste-syrup share vs performance cofactors
  - catalyst cost reduction vs coproduct credit tradeoff
- Use the renewable replacement rank to compare candidate fuels directly to gasoline.
- Optionally extend the model to capture actual biomass conversion yields and multi-stage extractor economics.
- Explicitly model harmful aquatic biomass and remediation credit as a separate economic driver.
- Compare this bloom-remediation route directly with hemp, hydrogen, and mushroom fuels in the same framework.
