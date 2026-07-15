import engine_simulator as m
fuels = m.load_fuel_profiles()
base = fuels['fsot_hemp_waste_grounded']
variant = m.make_hemp_advanced_variant(
    base,
    ether_frac=0.05,
    ester_frac=0.09,
    cofactor_frac=0.05,
    catalyst_cost=0.05,
    coproduct_credit=0.05,
    biomass_yield=0.60,
)
print('id', variant.id)
print('composition', variant.composition)
print('lhv', variant.lhv_kj_per_kg)
print('stoich_afr', variant.stoich_afr)
print('density', variant.density_kg_m3)
print('process_energy', variant.process_energy_kj_per_kg)
print('production_cost', variant.production_cost_per_kg)
print('conversion_efficiency', variant.conversion_efficiency)
print('renewable_fraction', variant.renewable_fraction)
print('production_route', variant.production_route)
print('byproducts', variant.byproducts)
print('catalyst_cycle_cost', variant.catalyst_cycle_cost_per_kg)
print('coproduct_credit', variant.coproduct_credit_per_kg)
